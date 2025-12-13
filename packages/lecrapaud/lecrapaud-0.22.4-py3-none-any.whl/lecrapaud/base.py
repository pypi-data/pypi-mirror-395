"""LeCrapaud API module.

This module provides the main interface for the LeCrapaud machine learning pipeline.
It allows for end-to-end ML workflows including data preprocessing, feature engineering,
model training, and prediction.

Basic Usage:
    # Create a new experiment
    experiment = LeCrapaud(data=data, target_numbers=[1], target_clf=[1])

    # Train the model
    experiment.fit(data)

    # Make predictions
    predictions, scores_reg, scores_clf = experiment.predict(new_data)

    # Load existing experiment
    experiment = LeCrapaud(id=123)
    predictions = experiment.predict(new_data)

    # Class methods for experiment management
    best_exp = LeCrapaud.get_best_experiment_by_name('my_experiment')
    all_exps = LeCrapaud.list_experiments('my_experiment')
"""

import joblib
import pandas as pd
import ast
import os
import logging
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from lecrapaud.db.session import init_db
from lecrapaud.feature_selection import FeatureSelector
from lecrapaud.model_preprocessing import ModelPreprocessor
from lecrapaud.model_selection import (
    ModelSelector,
    BaseModel,
    evaluate,
    load_model,
    plot_threshold,
    plot_evaluation_for_classification,
)
from lecrapaud.feature_engineering import FeatureEngineering
from lecrapaud.feature_preprocessing import FeaturePreprocessor
from lecrapaud.experiment import create_experiment
from lecrapaud.db import Experiment
from lecrapaud.search_space import normalize_models_idx, all_models
from lecrapaud.utils import logger
from lecrapaud.directories import tmp_dir


class LeCrapaud:
    """
    Unified LeCrapaud class for machine learning experiments.

    This class provides both the ML pipeline functionality and experiment management.
    It can be initialized either with new data to create an experiment or with an
    experiment ID to load an existing one.

    Usage:
        # Create new experiment
        experiment = LeCrapaud(data=df, target_numbers=[1, 2], ...)

        # Load existing experiment
        experiment = LeCrapaud(id=123)

        # Train the model
        experiment.fit(data)

        # Make predictions
        predictions = experiment.predict(new_data)

    Args:
        id (int, optional): ID of an existing experiment to load
        data (pd.DataFrame, optional): Input data for a new experiment
        uri (str, optional): Database connection URI
        **kwargs: Additional configuration parameters
    """

    def __init__(
        self, id: int = None, data: pd.DataFrame = None, uri: str = None, **kwargs
    ):
        """Initialize LeCrapaud with either new or existing experiment."""
        # Initialize database connection
        init_db(uri=uri)

        if id:
            # Load existing experiment
            self.experiment = Experiment.get(id)
            # Context from DB takes precedence over kwargs
            effective_kwargs = {
                **self.DEFAULT_PARAMS,
                **kwargs,
                **self.experiment.context,
            }
        else:
            if data is None:
                raise ValueError(
                    "Either id or data must be provided. Data can be a path to a folder containing trained models"
                )
            # New experiment: merge defaults with provided kwargs
            effective_kwargs = {**self.DEFAULT_PARAMS, **kwargs}

        # Normalize models_idx if present
        if "models_idx" in effective_kwargs:
            effective_kwargs["models_idx"] = normalize_models_idx(
                effective_kwargs["models_idx"]
            )

        # Set all parameters as instance attributes
        for key, value in effective_kwargs.items():
            setattr(self, key, value)

        # Create experiment if new
        if not id:
            self.experiment = create_experiment(data=data, **effective_kwargs)

        # Create directories
        experiment_dir = f"{tmp_dir}/{self.experiment.name}"
        preprocessing_dir = f"{experiment_dir}/preprocessing"
        data_dir = f"{experiment_dir}/data"
        os.makedirs(preprocessing_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)

    # Default values for all experiment parameters
    DEFAULT_PARAMS = {
        # Feature Engineering
        "columns_drop": [],
        "columns_boolean": [],
        "columns_date": [],
        "columns_te_groupby": [],
        "columns_te_target": [],
        "for_training": True,
        # Preprocessing
        "time_series": False,
        "val_size": 0.2,
        "test_size": 0.2,
        "columns_pca": [],
        "pca_temporal": [],
        "pca_cross_sectional": [],
        "columns_onehot": [],
        "columns_binary": [],
        "columns_ordinal": [],
        "columns_frequency": [],
        # Feature Selection
        "percentile": 20,
        "corr_threshold": 80,
        "max_features": 50,
        "max_p_value_categorical": 0.05,
        # Model Selection
        "target_numbers": [],
        "target_clf": [],
        "models_idx": [],
        "max_timesteps": 120,
        "perform_hyperopt": True,
        "number_of_trials": 20,
        "perform_crossval": False,
        "plot": True,
        "preserve_model": True,
        "target_clf_thresholds": {},
        # Data structure
        "date_column": None,
        "group_column": None,
    }

    @classmethod
    def get_default_params(cls):
        """Get the default parameters for experiments."""
        return cls.DEFAULT_PARAMS.copy()

    def get_effective_context(self):
        """Get the effective context (merged defaults + experiment context)."""
        return {k: getattr(self, k, v) for k, v in self.DEFAULT_PARAMS.items()}

    @classmethod
    def get_last_experiment_by_name(cls, name: str, **kwargs):
        """Retrieve the last experiment by name."""
        return cls(id=Experiment.get_last_by_name(name).id, **kwargs)

    @classmethod
    def get_best_experiment_by_name(cls, name: str, **kwargs):
        """Retrieve the best experiment by score."""
        best_exp = Experiment.get_best_by_score(name=name)
        if not best_exp:
            return None
        return cls(id=best_exp.id, **kwargs)

    @classmethod
    def list_experiments(cls, name: str = None, limit: int = 1000):
        """List all experiments in the database."""
        return [
            cls(id=exp.id) for exp in Experiment.get_all_by_name(name=name, limit=limit)
        ]

    @classmethod
    def compare_experiment_scores(cls, name: str):
        """Compare scores of experiments with matching names."""
        experiments = cls.list_experiments(name=name)

        if not experiments:
            return {"error": f"No experiments found with name containing '{name}'"}

        comparison = {}

        for exp in experiments:
            for model_sel in exp.experiment.model_selections:
                if model_sel.best_score:
                    scores = {
                        "rmse": model_sel.best_score["rmse"],
                        "logloss": model_sel.best_score["logloss"],
                        "accuracy": model_sel.best_score["accuracy"],
                        "f1": model_sel.best_score["f1"],
                        "roc_auc": model_sel.best_score["roc_auc"],
                    }
                    target_name = model_sel.target.name
                    comparison[exp.experiment.name][target_name] = scores
                else:
                    logger.warning(
                        f"No best score found for experiment {exp.experiment.name} and target {model_sel.target.name}"
                    )

        return comparison

    # Main ML Pipeline Methods
    # ========================

    def fit(self, data, best_params=None):
        """
        Fit the complete ML pipeline on the provided data.

        Args:
            data (pd.DataFrame): Input training data
            best_params (dict, optional): Pre-defined best parameters

        Returns:
            self: Returns self for chaining
        """
        logger.info("Running training...")

        # Step 1: Feature Engineering
        logger.info("Starting feature engineering...")
        feature_eng = FeatureEngineering(experiment=self.experiment)
        feature_eng.fit(data)
        data_eng = feature_eng.get_data()
        logger.info("Feature engineering done.")

        # Step 2: Feature Preprocessing (split data)
        logger.info("Starting feature preprocessing...")
        from lecrapaud.feature_preprocessing import split_data

        train, val, test = split_data(data_eng, experiment=self.experiment)

        # Apply feature preprocessing transformations
        feature_preprocessor = FeaturePreprocessor(experiment=self.experiment)
        feature_preprocessor.fit(train)
        train = feature_preprocessor.transform(train)
        if val is not None:
            val = feature_preprocessor.transform(val)
        if test is not None:
            test = feature_preprocessor.transform(test)
        logger.info("Feature preprocessing done.")

        # Step 3: Feature Selection (for each target)
        logger.info("Starting feature selection...")
        for target_number in self.target_numbers:
            feature_selector = FeatureSelector(
                experiment=self.experiment, target_number=target_number
            )
            feature_selector.fit(train)

        # Refresh experiment to get updated features
        self.experiment = Experiment.get(self.experiment.id)
        all_features = self.experiment.get_all_features(
            date_column=self.date_column, group_column=self.group_column
        )
        joblib.dump(
            all_features, f"{self.experiment.path}/preprocessing/all_features.pkl"
        )
        logger.info("Feature selection done.")

        # Step 4: Model Preprocessing (scaling)
        logger.info("Starting model preprocessing...")
        model_preprocessor = ModelPreprocessor(experiment=self.experiment)

        # Fit and transform training data, then transform val/test
        model_preprocessor.fit(train)
        train_scaled = model_preprocessor.transform(train)
        val_scaled = model_preprocessor.transform(val) if val is not None else None
        test_scaled = model_preprocessor.transform(test) if test is not None else None

        # Create data dict for model selection (keep both raw and scaled splits)
        std_data = {
            "train": train,
            "val": val,
            "test": test,
            "train_scaled": train_scaled,
            "val_scaled": val_scaled,
            "test_scaled": test_scaled,
        }

        # Handle time series reshaping if needed
        reshaped_data = None
        # Check if any model requires recurrent processing
        need_reshaping = (
            any(all_models[i].get("recurrent") for i in self.models_idx)
            and self.time_series
        )

        if need_reshaping:
            # Sanity check: make sure we have enough data for max_timesteps
            if (
                self.group_column
                and train_scaled.groupby(self.group_column).size().min()
                < self.max_timesteps
            ) or train_scaled.shape[0] < self.max_timesteps:
                raise ValueError(
                    f"Not enough data for group_column {self.group_column} to reshape data for recurrent models"
                )

            from lecrapaud.model_preprocessing import reshape_time_series

            features = self.experiment.get_all_features(
                date_column=self.date_column, group_column=self.group_column
            )
            reshaped_data = reshape_time_series(
                self.experiment,
                features,
                train_scaled,
                val_scaled,
                test_scaled,
                timesteps=self.max_timesteps,
            )
        logger.info("Model preprocessing done.")

        # Step 5: Model Selection (for each target)
        logger.info("Starting model selection...")
        self.models_ = {}
        for target_number in self.target_numbers:
            model_selector = ModelSelector(
                experiment=self.experiment, target_number=target_number
            )
            model_selector.fit(
                std_data, reshaped_data=reshaped_data, best_params=best_params
            )
            self.models_[target_number] = model_selector.get_best_model()
        logger.info("Model selection done.")

        return self

    def predict(self, new_data, verbose: int = 0):
        """
        Make predictions on new data using the trained pipeline.

        Args:
            new_data (pd.DataFrame): Input data for prediction
            verbose (int): Verbosity level (0=warnings only, 1=all logs)

        Returns:
            tuple: (predictions_df, scores_regression, scores_classification)
        """
        # for scores if TARGET is in columns
        scores_reg = []
        scores_clf = []

        if verbose == 0:
            logger.setLevel(logging.WARNING)

        logger.warning("Running prediction...")

        # Apply the same preprocessing pipeline as training
        # Step 1: Feature Engineering
        feature_eng = FeatureEngineering(experiment=self.experiment)
        feature_eng.fit(new_data)
        data = feature_eng.get_data()

        # Step 2: Feature Preprocessing (no splitting for prediction)
        feature_preprocessor = FeaturePreprocessor(experiment=self.experiment)
        # Load existing transformations and apply
        data = feature_preprocessor.transform(data)

        # Step 3: Model Preprocessing (scaling)
        model_preprocessor = ModelPreprocessor(experiment=self.experiment)
        # Apply existing scaling
        scaled_data = model_preprocessor.transform(data)

        # Step 4: Time series reshaping if needed
        reshaped_data = None
        # Check if any model requires recurrent processing
        need_reshaping = (
            any(all_models[i].get("recurrent") for i in self.models_idx)
            and self.time_series
        )

        if need_reshaping:
            # Sanity check: make sure we have enough data for max_timesteps
            if (
                self.group_column
                and scaled_data.groupby(self.group_column).size().min()
                < self.max_timesteps
            ) or scaled_data.shape[0] < self.max_timesteps:
                raise ValueError(
                    f"Not enough data for group_column {self.group_column} to reshape data for recurrent models"
                )

            from lecrapaud.model_preprocessing import reshape_time_series

            all_features = self.experiment.get_all_features(
                date_column=self.date_column, group_column=self.group_column
            )
            # For prediction, we reshape the entire dataset
            reshaped_data = reshape_time_series(
                self.experiment, all_features, scaled_data, timesteps=self.max_timesteps
            )
            reshaped_data = reshaped_data[
                "x_train_reshaped"
            ]  # Only need X data for prediction

        # Step 5: Predict for each target
        for target_number in self.target_numbers:
            # Load the trained model
            target_dir = f"{self.experiment.path}/TARGET_{target_number}"
            model = BaseModel(path=target_dir, target_number=target_number)

            # Get features for this target
            all_features = self.experiment.get_all_features(
                date_column=self.date_column, group_column=self.group_column
            )
            features = self.experiment.get_features(target_number)

            # Prepare prediction data
            if model.recurrent:
                features_idx = [
                    i for i, e in enumerate(all_features) if e in set(features)
                ]
                x_pred = reshaped_data[:, :, features_idx]
            else:
                x_pred = scaled_data[features] if model.need_scaling else data[features]

            # Make prediction
            y_pred = model.predict(x_pred)

            # Fix index for recurrent models
            if model.recurrent:
                y_pred.index = new_data.index

            # Unscale prediction if needed
            if (
                model.need_scaling
                and model.target_type == "regression"
                and model.scaler_y is not None
            ):
                y_pred = pd.Series(
                    model.scaler_y.inverse_transform(
                        y_pred.values.reshape(-1, 1)
                    ).flatten(),
                    index=new_data.index,
                )
                y_pred.name = "PRED"

            # Evaluate if target is present in new_data
            target_col = next(
                (
                    col
                    for col in new_data.columns
                    if col.upper() == f"TARGET_{target_number}"
                ),
                None,
            )
            if target_col is not None:
                y_true = new_data[target_col]
                prediction = pd.concat([y_true, y_pred], axis=1)
                prediction.rename(columns={target_col: "TARGET"}, inplace=True)
                score = evaluate(
                    prediction,
                    target_type=model.target_type,
                )
                score["TARGET"] = f"TARGET_{target_number}"

                if model.target_type == "classification":
                    scores_clf.append(score)
                else:
                    scores_reg.append(score)

            # Add predictions to the output dataframe
            if isinstance(y_pred, pd.DataFrame):
                y_pred = y_pred.add_prefix(f"TARGET_{target_number}_")
                new_data = pd.concat([new_data, y_pred], axis=1)
            else:
                y_pred.name = f"TARGET_{target_number}_PRED"
                new_data = pd.concat([new_data, y_pred], axis=1)

        # Format scores
        if len(scores_reg) > 0:
            scores_reg = pd.DataFrame(scores_reg).set_index("TARGET")
        if len(scores_clf) > 0:
            scores_clf = pd.DataFrame(scores_clf).set_index("TARGET")

        return new_data, scores_reg, scores_clf

    def get_scores(self, target_number: int):
        return pd.read_csv(
            f"{self.experiment.path}/TARGET_{target_number}/scores_tracking.csv"
        )

    def get_prediction(self, target_number: int, model_name: str):
        return pd.read_csv(
            f"{self.experiment.path}/TARGET_{target_number}/{model_name}/prediction.csv"
        )

    def get_feature_summary(self):
        return pd.read_csv(f"{self.experiment.path}/feature_summary.csv")

    def get_threshold(self, target_number: int):
        thresholds = joblib.load(
            f"{self.experiment.path}/TARGET_{target_number}/thresholds.pkl"
        )
        if isinstance(thresholds, str):
            thresholds = ast.literal_eval(thresholds)

        return thresholds

    def load_model(self, target_number: int, model_name: str = None):

        if not model_name:
            return load_model(f"{self.experiment.path}/TARGET_{target_number}")

        return load_model(f"{self.experiment.path}/TARGET_{target_number}/{model_name}")

    def plot_feature_importance(
        self, target_number: int, model_name="linear", top_n=30
    ):
        """
        Plot feature importance ranking.

        Args:
            target_number (int): Target variable number
            model_name (str): Name of the model to load
            top_n (int): Number of top features to display
        """
        model = self.load_model(target_number, model_name)
        experiment = self.experiment

        # Get feature names
        feature_names = experiment.get_features(target_number)

        # Get feature importances based on model type
        if hasattr(model, "feature_importances_"):
            # For sklearn tree models
            importances = model.feature_importances_
            importance_type = "Gini"
        elif hasattr(model, "get_score"):
            # For xgboost models
            importance_dict = model.get_score(importance_type="weight")
            importances = np.zeros(len(feature_names))
            for i, feat in enumerate(feature_names):
                if feat in importance_dict:
                    importances[i] = importance_dict[feat]
            importance_type = "Weight"
        elif hasattr(model, "feature_importance"):
            # For lightgbm models
            importances = model.feature_importance(importance_type="split")
            importance_type = "Split"
        elif hasattr(model, "get_feature_importance"):
            importances = model.get_feature_importance()
            importance_type = "Feature importance"
        elif hasattr(model, "coef_"):
            # For linear models
            importances = np.abs(model.coef_.flatten())
            importance_type = "Absolute coefficient"
        else:
            raise ValueError(
                f"Model {model_name} does not support feature importance calculation"
            )

        # Create a DataFrame for easier manipulation
        importance_df = pd.DataFrame(
            {"feature": feature_names[: len(importances)], "importance": importances}
        )

        # Sort features by importance and take top N
        importance_df = importance_df.sort_values("importance", ascending=False).head(
            top_n
        )

        # Create the plot
        plt.figure(figsize=(10, max(6, len(importance_df) * 0.3)))
        ax = sns.barplot(
            data=importance_df,
            x="importance",
            y="feature",
            palette="viridis",
            orient="h",
        )

        # Add value labels
        for i, v in enumerate(importance_df["importance"]):
            ax.text(v, i, f"{v:.4f}", color="black", ha="left", va="center")

        plt.title(f"Feature Importance ({importance_type})")
        plt.tight_layout()
        plt.show()

        return importance_df

    def plot_evaluation_for_classification(
        self, target_number: int, model_name="linear"
    ):
        prediction = self.get_prediction(target_number, model_name)
        thresholds = self.get_threshold(target_number)

        plot_evaluation_for_classification(prediction)

        for class_label, metrics in thresholds.items():
            threshold = metrics["threshold"]
            precision = metrics["precision"]
            recall = metrics["recall"]
            if threshold is not None:
                tmp_pred = prediction[["TARGET", "PRED", class_label]].copy()
                tmp_pred.rename(columns={class_label: 1}, inplace=True)
                print(f"Class {class_label}:")
                plot_threshold(tmp_pred, threshold, precision, recall)
            else:
                print(f"No threshold found for class {class_label}")

    def get_best_params(self, target_number: int = None) -> dict:
        """
        Load the best parameters for the experiment.

        Args:
            target_number (int, optional): If provided, returns parameters for this specific target.
                                         If None, returns parameters for all targets.

        Returns:
            dict: Dictionary containing the best parameters. If target_number is provided,
                  returns parameters for that target only. Otherwise, returns a dictionary
                  with target numbers as keys.
        """
        import json
        import os

        params_file = os.path.join(
            self.experiment.path, "preprocessing", "all_targets_best_params.json"
        )

        if not os.path.exists(params_file):
            raise FileNotFoundError(
                f"Best parameters file not found at {params_file}. "
                "Make sure to fit model training first."
            )

        try:
            with open(params_file, "r") as f:
                all_params = json.load(f)

            # Convert string keys to integers
            all_params = {int(k): v for k, v in all_params.items()}

            if target_number is not None:
                if target_number not in all_params:
                    available_targets = list(all_params.keys())
                    raise ValueError(
                        f"No parameters found for target {target_number}. "
                        f"Available targets: {available_targets}"
                    )
                return all_params[target_number]

            return all_params

        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing best parameters file: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading best parameters: {str(e)}")

"""
Dataset Validation Component for Feature Selection.

This component handles all validation logic for the feature selection stage,
including prerequisite checks, data validation, and error handling.
"""

import streamlit as st
from Builder import ModelStage
from typing import Dict, Any, List, Optional


class DatasetValidationComponent:
    """Handles dataset validation for feature selection."""

    def __init__(self, builder, logger=None):
        """
        Initialize the validation component.

        Args:
            builder: Builder instance containing the dataset
            logger: Optional logger instance for tracking errors
        """
        self.builder = builder
        self.logger = logger

    def validate_and_handle_errors(self) -> bool:
        """
        Perform all validation checks and handle errors.

        Returns:
            bool: True if validation passes, False if errors were found
        """
        # Check preprocessing completion
        if not self._check_preprocessing_completion():
            return False

        # Validate data consistency
        if not self._validate_data_consistency():
            return False

        # Additional data validation checks
        if not self._validate_data_quality():
            return False

        return True

    def _check_preprocessing_completion(self) -> bool:
        """
        Check if preprocessing stage is complete.

        Returns:
            bool: True if preprocessing is complete
        """
        if not self.builder.stage_completion.get(ModelStage.DATA_PREPROCESSING, False):
            st.error("Please complete the preprocessing stage first.")

            if self.logger:
                self.logger.log_error(
                    "Feature Selection Access Denied",
                    {
                        "reason": "Preprocessing not completed",
                        "current_stage": "FEATURE_SELECTION",
                        "required_stage": "DATA_PREPROCESSING"
                    }
                )

            if st.button("Return to Preprocessing"):
                self.builder.current_stage = ModelStage.DATA_PREPROCESSING
                if self.logger:
                    self.logger.log_stage_transition("FEATURE_SELECTION", "DATA_PREPROCESSING")
                st.switch_page("pages/3_Data_Preprocessing.py")

            return False

        return True

    def _validate_data_consistency(self) -> bool:
        """
        Validate basic data consistency.

        Returns:
            bool: True if data is consistent
        """
        # Check if required data exists
        if (self.builder.training_data is None or
            self.builder.testing_data is None or
            self.builder.target_column is None):

            st.error("Missing required data. Please return to preprocessing.")
            self._render_return_button()
            return False

        # Import and use data processing utilities
        from components.feature_selection.utils.data_processing_utils import (
            synchronize_data_splits,
            validate_data_consistency
        )

        # Synchronize data splits
        sync_result = synchronize_data_splits(self.builder)
        if not sync_result["success"]:
            st.error(f"Data synchronization failed: {sync_result['message']}")
            self._render_return_button()
            return False

        # Validate data consistency
        validation_result = validate_data_consistency(self.builder)
        if not validation_result["success"]:
            st.error("⚠️ Data Consistency Error")
            for error in validation_result["errors"]:
                st.error(f"• {error['message']}")

            if self.logger:
                for error in validation_result["errors"]:
                    self.logger.log_error(
                        f"Data Validation Error: {error['type']}",
                        error.get('details', {})
                    )

            self._render_return_button()
            return False

        return True

    def _validate_data_quality(self) -> bool:
        """
        Validate data quality including missing values and string columns.

        Returns:
            bool: True if data quality is acceptable
        """
        validation_failed = False
        validation_messages = []

        # Check for missing values in both training and testing data
        missing_train = self.builder.training_data.isnull().sum().sum()
        missing_test = self.builder.testing_data.isnull().sum().sum()

        if missing_train > 0 or missing_test > 0:
            validation_failed = True
            validation_messages.append(
                f"Found missing values: {missing_train} in training data, {missing_test} in testing data"
            )
            if self.logger:
                self.logger.log_error(
                    "Data Validation Failed",
                    {
                        "error_type": "missing_values",
                        "missing_train": int(missing_train),
                        "missing_test": int(missing_test)
                    }
                )

        # Check for string columns (excluding the target column)
        string_cols_train = self.builder.training_data.select_dtypes(include=['object']).columns
        string_cols_test = self.builder.testing_data.select_dtypes(include=['object']).columns

        # Remove target column from the string columns list if it's a string column
        if self.builder.target_column in string_cols_train:
            string_cols_train = string_cols_train.drop(self.builder.target_column)
        if self.builder.target_column in string_cols_test:
            string_cols_test = string_cols_test.drop(self.builder.target_column)

        if len(string_cols_train) > 0 or len(string_cols_test) > 0:
            validation_failed = True
            validation_messages.append(
                f"Found string columns that need encoding:\n"
                f"Training data: {list(string_cols_train)}\n"
                f"Testing data: {list(string_cols_test)}"
            )
            if self.logger:
                self.logger.log_error(
                    "Data Validation Failed",
                    {
                        "error_type": "string_columns",
                        "string_cols_train": list(string_cols_train),
                        "string_cols_test": list(string_cols_test)
                    }
                )

        if validation_failed:
            st.error("⚠️ Data Preprocessing Validation Failed")
            st.error(
                "The following issues were found with your data:\n" +
                "\n".join(f"- {msg}" for msg in validation_messages)
            )
            self._render_return_button()
            return False

        return True

    def _render_return_button(self) -> None:
        """Render a return to preprocessing button."""
        if st.button("Return to Preprocessing"):
            self.builder.current_stage = ModelStage.DATA_PREPROCESSING
            if self.logger:
                self.logger.log_stage_transition("FEATURE_SELECTION", "DATA_PREPROCESSING")
            st.switch_page("pages/3_Data_Preprocessing.py")

    def check_target_column_exists(self) -> bool:
        """
        Check if target column exists in the data.

        Returns:
            bool: True if target column exists
        """
        try:
            if self.builder.target_column not in self.builder.training_data.columns:
                st.error(f"Missing target column '{self.builder.target_column}' in training data.")
                self._log_missing_target_error("training")
                self._render_return_button()
                return False

            if self.builder.target_column not in self.builder.testing_data.columns:
                st.error(f"Missing target column '{self.builder.target_column}' in testing data.")
                self._log_missing_target_error("testing")
                self._render_return_button()
                return False

            return True

        except Exception as e:
            st.error(f"Error checking target column: {str(e)}")
            if self.logger:
                self.logger.log_error(
                    "Target Column Check Failed",
                    {"error": str(e)}
                )
            self._render_return_button()
            return False

    def _log_missing_target_error(self, data_type: str) -> None:
        """Log missing target column error."""
        if self.logger:
            if data_type == "training":
                available_columns = list(self.builder.training_data.columns) if self.builder.training_data is not None else []
            else:
                available_columns = list(self.builder.testing_data.columns) if self.builder.testing_data is not None else []

            self.logger.log_error(
                "Feature Selection Missing Target Column",
                {
                    "data_type": data_type,
                    "target_column": self.builder.target_column,
                    "available_columns": available_columns
                }
            )

    def validate_feature_analysis_prerequisites(self) -> bool:
        """
        Validate that prerequisites for feature analysis are met.

        Returns:
            bool: True if prerequisites are met
        """
        # Check that X_train and related splits exist and are properly sized
        if (not hasattr(self.builder, 'X_train') or
            self.builder.X_train is None or
            len(self.builder.X_train) == 0):
            st.error("Training features not available. Please return to preprocessing.")
            self._render_return_button()
            return False

        if (not hasattr(self.builder, 'X_test') or
            self.builder.X_test is None or
            len(self.builder.X_test) == 0):
            st.error("Testing features not available. Please return to preprocessing.")
            self._render_return_button()
            return False

        if (not hasattr(self.builder, 'y_train') or
            self.builder.y_train is None or
            len(self.builder.y_train) == 0):
            st.error("Training targets not available. Please return to preprocessing.")
            self._render_return_button()
            return False

        if (not hasattr(self.builder, 'y_test') or
            self.builder.y_test is None or
            len(self.builder.y_test) == 0):
            st.error("Testing targets not available. Please return to preprocessing.")
            self._render_return_button()
            return False

        return True

    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation status.

        Returns:
            Dictionary with validation summary
        """
        return {
            "preprocessing_complete": self.builder.stage_completion.get(
                ModelStage.DATA_PREPROCESSING, False
            ),
            "training_data_available": self.builder.training_data is not None,
            "testing_data_available": self.builder.testing_data is not None,
            "target_column_set": self.builder.target_column is not None,
            "feature_splits_available": (
                hasattr(self.builder, 'X_train') and
                self.builder.X_train is not None and
                len(self.builder.X_train) > 0
            ),
            "data_shapes": {
                "training_shape": self.builder.training_data.shape if self.builder.training_data is not None else None,
                "testing_shape": self.builder.testing_data.shape if self.builder.testing_data is not None else None,
                "X_train_shape": self.builder.X_train.shape if hasattr(self.builder, 'X_train') and self.builder.X_train is not None else None,
                "X_test_shape": self.builder.X_test.shape if hasattr(self.builder, 'X_test') and self.builder.X_test is not None else None
            }
        }
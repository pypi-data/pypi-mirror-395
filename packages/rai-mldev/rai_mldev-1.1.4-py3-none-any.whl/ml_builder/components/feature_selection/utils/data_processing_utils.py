"""
Data processing utilities for feature selection operations.

This module contains utility functions for data validation, cleaning, and processing
operations used throughout the feature selection pipeline.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Tuple, Any, Optional


def check_and_remove_duplicates(data: pd.DataFrame,
                               data_type: str = "Data",
                               target_column: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Check and remove duplicates from a dataset.

    Args:
        data (pd.DataFrame): The dataset to check for duplicates
        data_type (str): Description of the data type (e.g., "Training", "Testing")
        target_column (str): Name of the target column for partial duplicate checking

    Returns:
        tuple: (cleaned_data, duplicate_stats)
            - cleaned_data: DataFrame with duplicates removed
            - duplicate_stats: Dict with statistics about duplicates found and removed

    Example usage:
        # For any dataset with duplicates
        cleaned_df, stats = check_and_remove_duplicates(
            my_dataframe,
            data_type="Custom Dataset",
            target_column="target"
        )

        # Without target column (only exact duplicates)
        cleaned_df, stats = check_and_remove_duplicates(
            my_dataframe,
            data_type="Feature Data"
        )
    """
    initial_row_count = len(data)
    duplicate_stats = {
        'initial_rows': initial_row_count,
        'exact_duplicates_found': 0,
        'partial_duplicates_found': 0,
        'final_rows': initial_row_count,
        'total_reduction': 0,
        'reduction_percentage': 0.0
    }

    # Create a copy to work with
    cleaned_data = data.copy()

    # Check for exact duplicates
    exact_duplicates = cleaned_data.duplicated().sum()
    duplicate_stats['exact_duplicates_found'] = int(exact_duplicates)

    if exact_duplicates > 0:
        cleaned_data = cleaned_data.drop_duplicates(keep='first')
        rows_after_exact = len(cleaned_data)

        # Track duplicate removal
        if 'feature_selection_tracking' in st.session_state:
            st.session_state.feature_selection_tracking['duplicates_removed'] = True

        # Log exact duplicate removal
        if 'logger' in st.session_state:
            st.session_state.logger.log_calculation(
                f"{data_type} Data Duplicate Removal",
                {
                    "exact_duplicates_removed": int(exact_duplicates),
                    "initial_rows": initial_row_count,
                    "rows_after_exact": rows_after_exact
                }
            )
    else:
        rows_after_exact = len(cleaned_data)

    # Check for partial duplicates if target column is provided
    if target_column and target_column in cleaned_data.columns:
        non_target_cols = [col for col in cleaned_data.columns if col != target_column]
        partial_duplicates = cleaned_data.duplicated(subset=non_target_cols).sum()
        duplicate_stats['partial_duplicates_found'] = int(partial_duplicates)

        if partial_duplicates > 0:
            cleaned_data = cleaned_data.drop_duplicates(subset=non_target_cols)
            final_row_count = len(cleaned_data)

            # Track duplicate removal
            if 'feature_selection_tracking' in st.session_state:
                st.session_state.feature_selection_tracking['duplicates_removed'] = True

            # Log partial duplicate removal
            if 'logger' in st.session_state:
                st.session_state.logger.log_calculation(
                    f"{data_type} Data Duplicate Removal",
                    {
                        "partial_duplicates_removed": int(partial_duplicates),
                        "rows_after_exact": rows_after_exact,
                        "final_rows": final_row_count
                    }
                )
        else:
            final_row_count = len(cleaned_data)
    else:
        final_row_count = len(cleaned_data)

    # Calculate final statistics
    total_reduction = initial_row_count - final_row_count
    reduction_percentage = (total_reduction / initial_row_count) * 100 if initial_row_count > 0 else 0

    duplicate_stats.update({
        'final_rows': final_row_count,
        'total_reduction': total_reduction,
        'reduction_percentage': reduction_percentage
    })

    # Log summary if any duplicates were removed
    if duplicate_stats['exact_duplicates_found'] > 0 or duplicate_stats['partial_duplicates_found'] > 0:
        if 'logger' in st.session_state:
            st.session_state.logger.log_calculation(
                f"{data_type} Data Duplicate Removal Summary",
                duplicate_stats
            )

    return cleaned_data, duplicate_stats


def synchronize_data_splits(builder) -> Dict[str, Any]:
    """
    Synchronize X_train, X_test, y_train, y_test with training_data and testing_data.

    Args:
        builder: The Builder instance containing the dataset

    Returns:
        Dict containing synchronization results and any errors
    """
    try:
        # Log current state for debugging
        current_state = {
            "training_data_cols": len(builder.training_data.columns),
            "testing_data_cols": len(builder.testing_data.columns),
            "target_column": builder.target_column
        }

        # Check if X_train exists and log its state
        if hasattr(builder, 'X_train') and builder.X_train is not None:
            current_state["x_train_cols"] = len(builder.X_train.columns)
            current_state["x_train_features"] = list(builder.X_train.columns)

        # Get expected features from training_data
        expected_features = [col for col in builder.training_data.columns
                           if col != builder.target_column]
        current_state["expected_features"] = expected_features

        if 'logger' in st.session_state:
            st.session_state.logger.log_user_action(
                "Data Synchronization Check",
                current_state
            )

        # Always rebuild from authoritative source (training_data and testing_data)
        builder.X_train = builder.training_data.drop(columns=[builder.target_column])
        builder.X_test = builder.testing_data.drop(columns=[builder.target_column])
        builder.y_train = builder.training_data[builder.target_column]
        builder.y_test = builder.testing_data[builder.target_column]

        # Log the final state after synchronization
        final_state = {
            "X_train_cols": len(builder.X_train.columns),
            "X_test_cols": len(builder.X_test.columns),
            "y_train_len": len(builder.y_train),
            "y_test_len": len(builder.y_test),
            "X_train_features": list(builder.X_train.columns),
            "training_data_cols": len(builder.training_data.columns),
            "testing_data_cols": len(builder.testing_data.columns)
        }
        if 'logger' in st.session_state:
            st.session_state.logger.log_user_action(
                "Data Synchronization Complete",
                final_state
            )

        return {
            "success": True,
            "message": "Data synchronization completed successfully",
            "final_state": final_state
        }

    except Exception as e:
        error_msg = f"Data synchronization failed: {str(e)}"
        if 'logger' in st.session_state:
            st.session_state.logger.log_error(
                "Data Synchronization Error",
                {"error": error_msg}
            )
        return {
            "success": False,
            "message": error_msg
        }


def validate_data_consistency(builder) -> Dict[str, Any]:
    """
    Validate data consistency between features and targets.

    Args:
        builder: The Builder instance containing the dataset

    Returns:
        Dict containing validation results
    """
    validation_results = {
        "success": True,
        "errors": [],
        "warnings": []
    }

    try:
        # Verify data consistency
        if (len(builder.X_train) != len(builder.y_train) or
            len(builder.X_test) != len(builder.y_test)):

            error_details = {
                "X_train_length": len(builder.X_train),
                "y_train_length": len(builder.y_train),
                "X_test_length": len(builder.X_test),
                "y_test_length": len(builder.y_test)
            }

            validation_results["success"] = False
            validation_results["errors"].append({
                "type": "length_mismatch",
                "message": "Data consistency error: Feature and target lengths don't match",
                "details": error_details
            })

            if 'logger' in st.session_state:
                st.session_state.logger.log_error(
                    "Feature Selection Data Consistency Error",
                    error_details
                )

        # Check for missing target column
        if builder.target_column not in builder.training_data.columns:
            validation_results["success"] = False
            validation_results["errors"].append({
                "type": "missing_target",
                "message": f"Missing target column '{builder.target_column}' in training data",
                "details": {
                    "target_column": builder.target_column,
                    "available_columns": list(builder.training_data.columns)
                }
            })

        if builder.target_column not in builder.testing_data.columns:
            validation_results["success"] = False
            validation_results["errors"].append({
                "type": "missing_target",
                "message": f"Missing target column '{builder.target_column}' in testing data",
                "details": {
                    "target_column": builder.target_column,
                    "available_columns": list(builder.testing_data.columns)
                }
            })

    except Exception as e:
        validation_results["success"] = False
        validation_results["errors"].append({
            "type": "validation_error",
            "message": f"Validation failed: {str(e)}",
            "details": {"exception": str(e)}
        })

    return validation_results


def clean_missing_values(builder) -> Dict[str, Any]:
    """
    Clean missing values from training and testing data.

    Args:
        builder: The Builder instance containing the dataset

    Returns:
        Dict containing cleaning results
    """
    cleaning_results = {
        "success": True,
        "training_cleaned": False,
        "testing_cleaned": False,
        "missing_stats": {}
    }

    try:
        # Check training data for missing values
        missing_values_train = builder.training_data.isnull().sum()
        if (missing_values_train > 0).any():
            initial_rows = len(builder.training_data)
            builder.training_data = builder.training_data.dropna()
            final_rows = len(builder.training_data)

            cleaning_results["training_cleaned"] = True
            cleaning_results["missing_stats"]["training"] = {
                "initial_rows": initial_rows,
                "final_rows": final_rows,
                "rows_removed": initial_rows - final_rows,
                "missing_by_column": missing_values_train.to_dict()
            }

            # Log missing values removed
            if 'logger' in st.session_state:
                st.session_state.logger.log_calculation(
                    "Missing Values Removed",
                    cleaning_results["missing_stats"]["training"]
                )

        # Check testing data for missing values
        missing_values_test = builder.testing_data.isnull().sum()
        if (missing_values_test > 0).any():
            initial_rows = len(builder.testing_data)
            builder.testing_data = builder.testing_data.dropna()
            final_rows = len(builder.testing_data)

            cleaning_results["testing_cleaned"] = True
            cleaning_results["missing_stats"]["testing"] = {
                "initial_rows": initial_rows,
                "final_rows": final_rows,
                "rows_removed": initial_rows - final_rows,
                "missing_by_column": missing_values_test.to_dict()
            }

            # Log missing values removed
            if 'logger' in st.session_state:
                st.session_state.logger.log_calculation(
                    "Missing Values Removed",
                    cleaning_results["missing_stats"]["testing"]
                )

    except Exception as e:
        cleaning_results["success"] = False
        cleaning_results["error"] = str(e)

        if 'logger' in st.session_state:
            st.session_state.logger.log_error(
                "Missing Values Cleaning Error",
                {"error": str(e)}
            )

    return cleaning_results
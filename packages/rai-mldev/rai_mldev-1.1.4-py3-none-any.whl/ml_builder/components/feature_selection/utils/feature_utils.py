"""
Feature utility functions for the feature selection component.

This module contains utility functions for managing feature updates and removals
across the ML pipeline, extracted from the main Builder class for better modularity.
"""
from typing import Dict, List, Any
import pandas as pd


def update_features(builder, features_to_remove: List[str]) -> Dict[str, Any]:
    """
    Update feature set by removing specified features from the builder's data.

    Args:
        builder: The Builder instance containing the dataset
        features_to_remove: List of feature names to remove

    Returns:
        Dict containing:
        - success: bool indicating if the operation was successful
        - message: str explaining the result
        - info: Dict containing details about the update if successful
    """
    if builder.X_train is None or builder.X_test is None:
        return {
            "success": False,
            "message": "No data available for feature update"
        }

    try:
        # Verify features exist before removal
        missing_features = [f for f in features_to_remove if f not in builder.X_train.columns]
        if missing_features:
            return {
                "success": False,
                "message": f"Features not found in dataset: {missing_features}"
            }

        # Update training_data and testing_data first (these are the authoritative sources)
        if hasattr(builder, 'training_data') and builder.training_data is not None:
            # Only remove features that exist in training_data
            features_in_training = [f for f in features_to_remove if f in builder.training_data.columns]
            if features_in_training:
                builder.training_data = builder.training_data.drop(columns=features_in_training)

        if hasattr(builder, 'testing_data') and builder.testing_data is not None:
            # Only remove features that exist in testing_data
            features_in_testing = [f for f in features_to_remove if f in builder.testing_data.columns]
            if features_in_testing:
                builder.testing_data = builder.testing_data.drop(columns=features_in_testing)

        # Now rebuild X_train, X_test, y_train, y_test from the updated training/testing data
        # This ensures consistency across all data structures
        if builder.training_data is not None and builder.target_column in builder.training_data.columns:
            builder.X_train = builder.training_data.drop(columns=[builder.target_column])
            builder.y_train = builder.training_data[builder.target_column]

        if builder.testing_data is not None and builder.target_column in builder.testing_data.columns:
            builder.X_test = builder.testing_data.drop(columns=[builder.target_column])
            builder.y_test = builder.testing_data[builder.target_column]

        # Verify data consistency after update
        if (len(builder.X_train) != len(builder.y_train) if builder.y_train is not None else True) or \
                (len(builder.X_test) != len(builder.y_test) if builder.y_test is not None else True):
            return {
                "success": False,
                "message": "Data consistency check failed after feature removal"
            }

        # Clear any cached model data to prevent stale feature importance scores
        if hasattr(builder, 'model') and builder.model is not None:
            builder.model = None
            if hasattr(builder, 'logger') and builder.logger is not None:
                builder.logger.log_user_action("Model Cache Cleared", {
                    "reason": "Features updated",
                    "removed_features": features_to_remove
                })

        return {
            "success": True,
            "message": "Features updated successfully",
            "info": {
                "removed_features": features_to_remove,
                "remaining_features": list(builder.X_train.columns),
                "data_consistency": "verified"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating features: {str(e)}"
        }
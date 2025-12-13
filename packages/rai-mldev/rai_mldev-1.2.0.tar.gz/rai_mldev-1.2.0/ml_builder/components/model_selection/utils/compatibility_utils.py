"""
Compatibility checking utilities for model selection.

Contains functions to check if models are compatible with the current dataset
and problem setup.
"""

def check_xgboost_compatibility(data, target_column, problem_type):
    """
    Check if XGBoost is compatible with the current multiclass setup.
    XGBoost expects class labels to start from 0 for multiclass classification.

    Args:
        data: DataFrame containing the data
        target_column: Name of the target column
        problem_type: Type of ML problem

    Returns:
        bool: True if XGBoost is compatible, False otherwise
    """
    if problem_type == "multiclass_classification":
        unique_classes = sorted(data[target_column].unique())
        # XGBoost expects classes to start from 0 and be consecutive
        expected_classes = list(range(len(unique_classes)))
        if unique_classes != expected_classes:
            return False
    return True
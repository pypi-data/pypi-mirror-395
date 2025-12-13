"""
Nonlinearity detection utilities for model selection.

Contains functions to detect non-linear relationships between features and target
variables to help guide model selection.
"""

import numpy as np
from scipy.stats import pearsonr
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif


def detect_nonlinearity(data, target_column, problem_type):
    """
    Detect if there are non-linear relationships between features and target
    by comparing Pearson correlation with mutual information.

    Args:
        data: DataFrame containing the data
        target_column: Name of the target column
        problem_type: Type of ML problem

    Returns:
        bool: True if significant non-linear relationships are detected
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]

    # Only consider numerical features
    numerical_features = X.select_dtypes(include=['int8', 'int16', 'int32', 'int64','float16', 'float32', 'float64']).columns
    if len(numerical_features) == 0:
        return False

    X_num = X[numerical_features]

    # Calculate Pearson correlations
    pearson_scores = []
    for col in X_num.columns:
        score, _ = pearsonr(X_num[col], y)
        pearson_scores.append(abs(score))

    # Calculate mutual information
    # Handle both binary and multiclass classification
    if problem_type in ["classification", "binary_classification", "multiclass_classification"]:
        mi_scores = mutual_info_classif(X_num, y)
    else:
        mi_scores = mutual_info_regression(X_num, y)

    # Normalize mutual information scores to [0,1]
    if np.max(mi_scores) > 0:
        mi_scores = mi_scores / np.max(mi_scores)

    # Compare scores - if mutual information is significantly higher than
    # Pearson correlation for any feature, this suggests non-linear relationships
    for p_score, mi_score in zip(pearson_scores, mi_scores):
        if mi_score > 0.5 and mi_score > (p_score + 0.3):  # Significant non-linear relationship detected
            return True

    return False
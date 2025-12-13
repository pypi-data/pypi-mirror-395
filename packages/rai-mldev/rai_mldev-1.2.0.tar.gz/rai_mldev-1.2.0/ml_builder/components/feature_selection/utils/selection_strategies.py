"""
Feature selection strategies and utilities.

This module contains the logic for different feature selection strategies,
including low importance removal, correlation-based selection, and manual selection.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple


def categorize_features_by_importance(feature_scores: pd.DataFrame,
                                    critical_threshold: float = 0.001,
                                    high_concern_threshold: float = 0.01,
                                    moderate_concern_threshold: float = 0.05) -> Dict[str, List[str]]:
    """
    Categorize features into different importance tiers.

    Args:
        feature_scores: DataFrame with feature importance scores
        critical_threshold: Threshold for critical features (extremely low importance)
        high_concern_threshold: Threshold for high concern features
        moderate_concern_threshold: Threshold for moderate concern features

    Returns:
        Dictionary with categorized feature lists
    """
    critical_features = feature_scores[
        feature_scores['importance'] < critical_threshold
    ]['feature'].tolist()

    high_concern_features = feature_scores[
        (feature_scores['importance'] >= critical_threshold) &
        (feature_scores['importance'] <= high_concern_threshold)
    ]['feature'].tolist()

    moderate_concern_features = feature_scores[
        (feature_scores['importance'] > high_concern_threshold) &
        (feature_scores['importance'] <= moderate_concern_threshold)
    ]['feature'].tolist()

    return {
        "critical": critical_features,
        "high_concern": high_concern_features,
        "moderate_concern": moderate_concern_features
    }


def find_minimal_correlation_features(X_train: pd.DataFrame,
                                    min_correlation_threshold: float = 0.1) -> List[str]:
    """
    Find features with minimal correlation to other features.

    Args:
        X_train: Training feature dataset
        min_correlation_threshold: Minimum threshold for total correlation

    Returns:
        List of features with minimal correlation
    """
    minimal_correlation_features = []

    if len(X_train.columns) > 1:
        feature_corr_matrix = X_train.corr().abs()
        for feat in X_train.columns:
            total_correlation = feature_corr_matrix[feat].sum() - 1.0  # Exclude self-correlation
            if total_correlation < min_correlation_threshold:
                minimal_correlation_features.append(feat)

    return minimal_correlation_features


def create_tiered_feature_analysis(X_train: pd.DataFrame,
                                 feature_scores: pd.DataFrame,
                                 critical_threshold: float = 0.001,
                                 high_concern_threshold: float = 0.01,
                                 moderate_concern_threshold: float = 0.05,
                                 min_correlation_threshold: float = 0.1) -> List[Dict[str, Any]]:
    """
    Create comprehensive tiered analysis of features for selection.

    Args:
        X_train: Training feature dataset
        feature_scores: DataFrame with feature importance scores
        critical_threshold: Threshold for critical features
        high_concern_threshold: Threshold for high concern features
        moderate_concern_threshold: Threshold for moderate concern features
        min_correlation_threshold: Minimum correlation threshold

    Returns:
        List of dictionaries containing feature analysis data
    """
    # Categorize features by importance tiers
    importance_categories = categorize_features_by_importance(
        feature_scores, critical_threshold, high_concern_threshold, moderate_concern_threshold
    )

    # Find features with minimal correlation
    minimal_correlation_features = find_minimal_correlation_features(
        X_train, min_correlation_threshold
    )

    # Combine critical features (very low importance OR minimal correlation)
    critical_features_combined = list(set(
        importance_categories["critical"] + minimal_correlation_features
    ))

    # Create comprehensive feature analysis
    feature_analysis_data = []
    all_flagged_features = critical_features_combined + importance_categories["high_concern"]

    # Calculate correlation matrix once if needed
    feature_corr_matrix = None
    if len(X_train.columns) > 1:
        feature_corr_matrix = X_train.corr().abs()

    for feat in all_flagged_features:
        importance_row = feature_scores[feature_scores['feature'] == feat]
        importance = importance_row['importance'].values[0] if len(importance_row) > 0 else 0

        # Determine category and reason
        if feat in critical_features_combined:
            category = "🚨 Critical"
            is_critical = True
            if (feat in importance_categories["critical"] and
                feat in minimal_correlation_features):
                if feature_corr_matrix is not None:
                    total_corr = feature_corr_matrix[feat].sum() - 1.0
                    reason = f"Extremely low importance + Minimal correlation ({total_corr:.3f})"
                else:
                    reason = "Extremely low importance + Single feature"
            elif feat in importance_categories["critical"]:
                reason = "Extremely low importance (< 0.001)"
            else:  # minimal correlation
                if feature_corr_matrix is not None:
                    total_corr = feature_corr_matrix[feat].sum() - 1.0
                    reason = f"Minimal correlation ({total_corr:.3f})"
                else:
                    reason = "Single feature dataset"
        else:
            category = "⚠️ High Concern"
            is_critical = False
            if feature_corr_matrix is not None:
                total_corr = feature_corr_matrix[feat].sum() - 1.0
                avg_corr = (feature_corr_matrix.sum().sum() /
                           (len(feature_corr_matrix.columns) * (len(feature_corr_matrix.columns) - 1)))
                if total_corr > avg_corr:
                    reason = f"Low importance + High correlation ({total_corr:.3f})"
                else:
                    reason = f"Low importance + Unique information ({total_corr:.3f})"
            else:
                reason = "Low importance + Single feature"

        feature_analysis_data.append({
            "Remove": is_critical,  # Pre-check critical features
            "Feature": feat,
            "Category": category,
            "Importance": f"{importance:.6f}",
            "Reason": reason
        })

    return feature_analysis_data


def get_available_selection_strategies(feature_scores: pd.DataFrame,
                                     correlations: List[Dict[str, Any]],
                                     low_importance_threshold: float = 0.01) -> List[str]:
    """
    Determine which selection strategies are available based on the data.

    Args:
        feature_scores: DataFrame with feature importance scores
        correlations: List of correlation dictionaries
        low_importance_threshold: Threshold for considering features as low importance

    Returns:
        List of available strategy names
    """
    available_strategies = ["Manual Selection"]  # Always available

    # Check if low importance features exist
    low_importance_features = feature_scores[
        feature_scores['importance'] <= low_importance_threshold
    ]['feature'].tolist()

    if low_importance_features:
        available_strategies.append("Remove Low Importance")

    # Check if correlation groups exist
    if correlations:
        available_strategies.append("Remove One from Correlated Groups")

    return available_strategies


def create_features_by_category(protected_attributes: List[str],
                               low_importance_features: List[str],
                               correlations: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Create the features categorization dictionary for display.

    Args:
        protected_attributes: List of protected attribute features
        low_importance_features: List of low importance features
        correlations: List of correlation dictionaries

    Returns:
        Dictionary categorizing features with display information
    """
    # Get correlated features
    correlated_features = list(set([
        c['feature1'] for c in correlations
    ] + [c['feature2'] for c in correlations]))

    return {
        "Protected Attributes": {
            "features": protected_attributes,
            "description": "Features that could introduce bias",
            "icon": "🚨",
            "color": "red"
        },
        "Low Importance Features": {
            "features": low_importance_features,
            "description": "Features with minimal predictive power",
            "icon": "⚠️",
            "color": "orange"
        },
        "Highly Correlated Features": {
            "features": correlated_features,
            "description": "Features with strong relationships",
            "icon": "🔗",
            "color": "blue"
        },
    }


def apply_selection_strategy(builder,
                           strategy: str,
                           feature_scores: pd.DataFrame,
                           correlations: List[Dict[str, Any]],
                           selected_features: List[str] = None) -> Dict[str, Any]:
    """
    Apply the selected feature selection strategy.

    Args:
        builder: Builder instance
        strategy: Selection strategy name
        feature_scores: DataFrame with feature importance scores
        correlations: List of correlation dictionaries
        selected_features: Custom selected features (for manual selection)

    Returns:
        Dictionary with application results
    """
    try:
        if strategy == "Manual Selection":
            if not selected_features:
                return {
                    "success": False,
                    "message": "No features selected for manual removal"
                }
            features_to_remove = selected_features

        elif strategy == "Remove Low Importance":
            # This would be handled by the component's interactive selection
            return {
                "success": False,
                "message": "Low importance removal requires interactive selection"
            }

        elif strategy == "Remove One from Correlated Groups":
            # This would be handled by the component's interactive selection
            return {
                "success": False,
                "message": "Correlation removal requires interactive selection"
            }

        else:
            return {
                "success": False,
                "message": f"Unknown selection strategy: {strategy}"
            }

        # Apply the feature removal
        update_result = builder.update_features(features_to_remove)
        if update_result["success"]:
            return {
                "success": True,
                "message": "Feature selection applied successfully",
                "removed_features": features_to_remove,
                "remaining_features": list(builder.X_train.columns)
            }
        else:
            return {
                "success": False,
                "message": update_result["message"]
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error applying selection strategy: {str(e)}"
        }


def calculate_selection_impact(initial_features: int,
                             current_features: int,
                             removed_features: List[str]) -> Dict[str, Any]:
    """
    Calculate the impact of feature selection.

    Args:
        initial_features: Number of features at start
        current_features: Current number of features
        removed_features: List of removed features

    Returns:
        Dictionary with impact metrics
    """
    features_removed = len(removed_features)
    reduction_percentage = (features_removed / initial_features * 100) if initial_features > 0 else 0

    return {
        "initial_features": initial_features,
        "current_features": current_features,
        "features_removed": features_removed,
        "removed_features_list": removed_features,
        "reduction_percentage": reduction_percentage,
        "features_remaining": current_features
    }
"""
Feature Importance Analysis Utilities

This module contains utility functions for analyzing feature importance and related
responsible AI considerations. Originally extracted from Builder.analyse_feature_importance()
to improve modularity and code reuse.
"""

from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


def preprocess_features_for_importance(X_train: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Preprocess features for importance analysis by handling categorical data.

    Args:
        X_train: Training features DataFrame

    Returns:
        Tuple of (processed_dataframe, original_feature_names)
    """
    # Create processed copies of the data
    X_train_processed = X_train.copy()

    # Store original feature names for consistency
    original_feature_names = list(X_train_processed.columns)

    # Process each column based on its content
    for col in X_train_processed.columns:
        column_data = X_train_processed[col]

        # Try to convert to numeric first
        try:
            numeric_data = pd.to_numeric(column_data, errors='raise')
            X_train_processed[col] = numeric_data
            continue
        except (ValueError, TypeError):
            pass

        # If not numeric, handle categorical data
        unique_values = column_data.nunique()
        if unique_values <= 10:  # Threshold for categorical
            X_train_processed[col] = pd.Categorical(column_data).codes
        else:
            # For high cardinality strings, use hash encoding
            X_train_processed[col] = pd.util.hash_array(column_data.fillna(''), num_items=100)

    return X_train_processed, original_feature_names


def analyze_protected_attributes(feature_names: List[str]) -> List[str]:
    """
    Identify potentially protected attributes in the feature set.

    Args:
        feature_names: List of feature names to analyze

    Returns:
        List of feature names that might be protected attributes
    """
    protected_attributes = []
    protected_keywords = ['gender', 'sex', 'race', 'ethnicity', 'age', 'religion',
                          'nationality', 'marital', 'disability', 'orientation']

    for col in feature_names:
        if any(keyword in col.lower() for keyword in protected_keywords):
            protected_attributes.append(col)

    return protected_attributes


def calculate_feature_correlations(X_train_processed: pd.DataFrame,
                                 original_feature_names: List[str],
                                 threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Calculate correlations between features.

    Args:
        X_train_processed: Processed training features
        original_feature_names: Original feature names to use in output
        threshold: Correlation threshold (default 0.7)

    Returns:
        List of correlation dictionaries
    """
    correlations = []
    corr_matrix = X_train_processed.corr()

    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                correlations.append({
                    'feature1': original_feature_names[i],
                    'feature2': original_feature_names[j],
                    'correlation': float(corr_matrix.iloc[i, j])
                })

    return correlations


def analyze_data_quality(X_train: pd.DataFrame, original_feature_names: List[str]) -> List[Dict[str, Any]]:
    """
    Analyze data quality issues in the feature set.

    Args:
        X_train: Original training features
        original_feature_names: Feature names to analyze

    Returns:
        List of quality issue dictionaries
    """
    quality_issues = []

    for col in original_feature_names:
        # Check for missing values
        missing_pct = X_train[col].isnull().mean()
        if missing_pct > 0.05:
            quality_issues.append({
                'feature': col,
                'issue': f'High missing values ({missing_pct:.1%})',
                'recommendation': 'Consider imputation or feature removal'
            })

        # Check for skewness in numeric columns
        if pd.api.types.is_numeric_dtype(X_train[col]):
            skewness = X_train[col].skew()
            if abs(skewness) > 2:
                quality_issues.append({
                    'feature': col,
                    'issue': f'High skewness ({skewness:.2f})',
                    'recommendation': 'Consider applying log or power transformation'
                })

        # Check for high cardinality only in non-numeric columns
        if not pd.api.types.is_numeric_dtype(X_train[col]):
            unique_ratio = X_train[col].nunique() / len(X_train)
            if unique_ratio > 0.9:
                quality_issues.append({
                    'feature': col,
                    'issue': 'High cardinality',
                    'recommendation': 'Consider feature engineering or dimensionality reduction'
                })

    return quality_issues


def calculate_feature_importance(X_train_processed: pd.DataFrame,
                               y_train: pd.Series,
                               problem_type: str,
                               original_feature_names: List[str]) -> Tuple[np.ndarray, go.Figure]:
    """
    Calculate feature importance using Random Forest and create visualization.

    Args:
        X_train_processed: Processed training features
        y_train: Training targets
        problem_type: Type of problem (classification/regression)
        original_feature_names: Original feature names for labeling

    Returns:
        Tuple of (importance_scores, plotly_figure)
    """
    # Handle both binary and multiclass classification
    is_classification = problem_type in ["binary_classification", "multiclass_classification", "classification"]
    temp_model = (RandomForestClassifier if is_classification
                  else RandomForestRegressor)(n_estimators=100, random_state=42)

    temp_model.fit(X_train_processed, y_train)
    importance_scores = temp_model.feature_importances_

    # Create feature scores DataFrame using original feature names
    feature_scores = pd.DataFrame({
        'feature': original_feature_names,
        'importance': importance_scores
    }).sort_values('importance', ascending=False)

    # Create visualization
    fig = px.bar(
        feature_scores,
        x='feature',
        y='importance',
        title='Feature Importance Scores'
    )

    return importance_scores, fig


def get_low_importance_features(feature_scores_df: pd.DataFrame,
                              importance_scores: np.ndarray) -> List[str]:
    """
    Identify features with low importance (bottom 10%).

    Args:
        feature_scores_df: DataFrame with feature names and importance scores
        importance_scores: Array of importance scores

    Returns:
        List of low importance feature names
    """
    threshold = np.percentile(importance_scores, 10)
    low_importance = feature_scores_df[feature_scores_df['importance'] <= threshold]['feature'].tolist()
    return low_importance


def validate_data_consistency(X_train: pd.DataFrame, y_train: pd.Series) -> Tuple[bool, str]:
    """
    Validate that training data is consistent and ready for analysis.

    Args:
        X_train: Training features
        y_train: Training targets

    Returns:
        Tuple of (is_valid, error_message)
    """
    if X_train is None or y_train is None:
        return False, "Training data not available for feature importance analysis"

    if len(X_train) != len(y_train):
        return False, f"Data length mismatch: X_train has {len(X_train)} rows, y_train has {len(y_train)} rows"

    return True, ""


def create_error_response(message: str) -> Dict[str, Any]:
    """
    Create a standardized error response for feature importance analysis.

    Args:
        message: Error message to include

    Returns:
        Standardized error response dictionary
    """
    return {
        "success": False,
        "message": message,
        "feature_scores": [],
        "visualization": None,
        "responsible_ai": {
            "protected_attributes": [],
            "correlations": [],
            "quality_issues": [],
            "low_importance_features": []
        }
    }


def analyze_feature_importance(X_train: pd.DataFrame,
                             y_train: pd.Series,
                             problem_type: str) -> Dict[str, Any]:
    """
    Main function to analyze feature importance and related responsible AI considerations.

    This is the core analysis function that was extracted from Builder.analyse_feature_importance().
    It handles all the computation while the Builder method manages state and logging.

    Args:
        X_train: Training features DataFrame
        y_train: Training targets Series
        problem_type: Type of ML problem (classification/regression)

    Returns:
        Dictionary containing analysis results in the exact same format as the original method
    """
    try:
        # Validate data consistency
        is_valid, error_msg = validate_data_consistency(X_train, y_train)
        if not is_valid:
            return create_error_response(error_msg)

        # Preprocess features for importance analysis
        X_train_processed, original_feature_names = preprocess_features_for_importance(X_train)

        # Verify processed data consistency
        if len(X_train_processed.columns) != len(original_feature_names):
            return create_error_response("Feature processing resulted in column count mismatch")

        # Analyze protected attributes
        protected_attributes = analyze_protected_attributes(original_feature_names)

        # Calculate feature correlations
        correlations = calculate_feature_correlations(X_train_processed, original_feature_names)

        # Analyze data quality
        quality_issues = analyze_data_quality(X_train, original_feature_names)

        # Calculate feature importance
        importance_scores, fig = calculate_feature_importance(
            X_train_processed, y_train, problem_type, original_feature_names
        )

        # Create feature scores DataFrame for consistency with original
        feature_scores = pd.DataFrame({
            'feature': original_feature_names,
            'importance': importance_scores
        }).sort_values('importance', ascending=False)

        # Identify low importance features
        low_importance = get_low_importance_features(feature_scores, importance_scores)

        return {
            "success": True,
            "feature_scores": feature_scores.to_dict('records'),
            "visualization": fig,
            "responsible_ai": {
                "protected_attributes": protected_attributes,
                "correlations": correlations,
                "quality_issues": quality_issues,
                "low_importance_features": low_importance
            }
        }

    except Exception as e:
        return create_error_response(f"Error analyzing feature importance: {str(e)}")
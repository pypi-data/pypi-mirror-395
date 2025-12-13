"""
Protected Attributes Detection Utilities

This module contains utilities for automatically detecting potential protected attributes
in datasets for fairness analysis and responsible AI considerations.

Extracted from Builder.py to improve code organization and reusability.
"""

import pandas as pd
from typing import List


def get_protected_attributes(X_data: pd.DataFrame) -> List[str]:
    """
    Automatically detect potential protected attributes in the dataset.

    Args:
        X_data: DataFrame containing features to analyze

    Returns:
        List[str]: List of column names that might be protected attributes
    """
    if X_data is None or X_data.empty:
        return []

    protected_attributes = []

    # Common protected attribute names (case insensitive)
    protected_keywords = [
        'gender', 'sex', 'race', 'ethnicity', 'nationality', 'religion',
        'age', 'disability', 'marital', 'family', 'pregnancy', 'veteran',
        'income', 'education', 'minority', 'demographic', 'origin'
    ]

    # Check column names for protected attribute keywords
    for col in X_data.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in protected_keywords):
            protected_attributes.append(col)

    # Also check for categorical columns with few unique values
    for col in X_data.select_dtypes(include=['object', 'category']).columns:
        if col not in protected_attributes:
            unique_values = X_data[col].nunique()
            # Categorical columns with 2-10 unique values might be protected attributes
            if 2 <= unique_values <= 10:
                protected_attributes.append(col)

    return protected_attributes


def analyze_protected_attribute_distribution(X_data: pd.DataFrame,
                                           y_data: pd.Series,
                                           protected_attr: str) -> dict:
    """
    Analyze the distribution of a protected attribute across target classes.

    Args:
        X_data: Features DataFrame
        y_data: Target variable Series
        protected_attr: Name of the protected attribute to analyze

    Returns:
        dict: Analysis results including distribution statistics
    """
    if protected_attr not in X_data.columns:
        return {"success": False, "message": f"Protected attribute '{protected_attr}' not found"}

    try:
        # Get distribution of protected attribute
        attr_distribution = X_data[protected_attr].value_counts()

        # Get distribution across target classes
        cross_tab = pd.crosstab(X_data[protected_attr], y_data, normalize='index')

        # Calculate basic statistics
        unique_values = X_data[protected_attr].nunique()
        missing_pct = X_data[protected_attr].isnull().mean() * 100

        return {
            "success": True,
            "attribute": protected_attr,
            "unique_values": int(unique_values),
            "missing_percentage": float(missing_pct),
            "distribution": attr_distribution.to_dict(),
            "target_distribution": cross_tab.to_dict(),
            "summary": {
                "most_common": attr_distribution.index[0] if len(attr_distribution) > 0 else None,
                "least_common": attr_distribution.index[-1] if len(attr_distribution) > 0 else None,
                "imbalance_ratio": float(attr_distribution.max() / attr_distribution.min()) if attr_distribution.min() > 0 else float('inf')
            }
        }
    except Exception as e:
        return {"success": False, "message": f"Error analyzing protected attribute: {str(e)}"}


def check_fairness_requirements(protected_attributes: List[str],
                               model_type: str = None) -> dict:
    """
    Check if the model meets basic fairness requirements based on detected protected attributes.

    Args:
        protected_attributes: List of detected protected attributes
        model_type: Type of model being used

    Returns:
        dict: Fairness requirements and recommendations
    """
    requirements = {
        "has_protected_attributes": len(protected_attributes) > 0,
        "protected_count": len(protected_attributes),
        "attributes": protected_attributes,
        "recommendations": [],
        "warnings": []
    }

    if len(protected_attributes) > 0:
        requirements["warnings"].append(
            f"Detected {len(protected_attributes)} potential protected attributes: {', '.join(protected_attributes)}"
        )
        requirements["recommendations"].extend([
            "Conduct bias analysis on detected protected attributes",
            "Consider implementing fairness constraints during model training",
            "Monitor model performance across different demographic groups",
            "Document potential bias mitigation strategies"
        ])
    else:
        requirements["recommendations"].append(
            "No obvious protected attributes detected, but manual review is still recommended"
        )

    # Model-specific recommendations
    if model_type:
        if model_type.lower() in ['xgboost', 'lightgbm', 'gradient_boosting']:
            requirements["recommendations"].append(
                f"For {model_type} models, consider using feature importance to identify indirect discrimination"
            )
        elif model_type.lower() in ['neural_network', 'mlp']:
            requirements["recommendations"].append(
                "For neural network models, consider adversarial debiasing techniques"
            )

    return requirements
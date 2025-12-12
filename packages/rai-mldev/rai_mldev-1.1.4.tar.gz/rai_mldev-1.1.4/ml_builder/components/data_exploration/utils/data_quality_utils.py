"""
Data Quality Analysis Utilities

This module contains utility functions for analyzing data quality metrics.
Extracted from Builder.analyse_data_quality() to improve code organization.
"""
from typing import Dict, Any
import pandas as pd
import numpy as np


def analyze_data_quality(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze the quality of the provided dataset.

    This function calculates comprehensive quality metrics for each column including:
    - Quality Score: Weighted combination of completeness, consistency, and validity
    - Completeness: Percentage of non-missing values
    - Consistency: Data type and range consistency
    - Validity: Data accuracy and correctness
    - Missing Values: Percentage of missing values
    - Unique Values: Percentage of unique values

    Args:
        data: The pandas DataFrame to analyze

    Returns:
        Dictionary containing success status and data quality metrics for each column
    """
    try:
        data_quality = {}

        for col in data.columns:
            missing_pct = data[col].isnull().mean() * 100
            unique_pct = (data[col].nunique() / len(data)) * 100

            # Calculate basic metrics
            try:
                expected_type = data[col].dtype
                type_consistency = sum(isinstance(x, type(data[col].iloc[0]))
                                       for x in data[col]) / len(data) * 100

                if np.issubdtype(expected_type, np.number):
                    q1, q3 = data[col].quantile([0.25, 0.75])
                    iqr = q3 - q1

                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    range_consistency = sum((data[col] >= lower_bound) &
                                            (data[col] <= upper_bound)) / len(data) * 100
                else:
                    range_consistency = 100

                consistency_score = (type_consistency + range_consistency) / 2
            except Exception:
                consistency_score = 0

            try:
                if np.issubdtype(expected_type, np.number):
                    validity_score = sum(~np.isnan(data[col].astype(float))) / len(data) * 100
                else:
                    validity_score = sum(data[col].astype(str).str.strip() != '') / len(data) * 100
            except Exception:
                validity_score = 0

            completeness_score = 100 - missing_pct

            quality_score = (
                    0.4 * completeness_score +
                    0.3 * consistency_score +
                    0.3 * validity_score
            )

            data_quality[col] = {
                "Quality Score": float(quality_score),
                "Completeness": float(completeness_score),
                "Consistency": float(consistency_score),
                "Validity": float(validity_score),
                "Missing Values (%)": float(missing_pct),
                "Unique Values (%)": float(unique_pct)
            }

        return {
            "success": True,
            "data_quality": data_quality
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error analyzing data quality: {str(e)}"
        }
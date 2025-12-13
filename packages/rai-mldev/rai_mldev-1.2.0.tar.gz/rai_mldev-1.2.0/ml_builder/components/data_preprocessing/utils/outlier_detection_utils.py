"""
Outlier Detection Utilities

This module contains utility functions for outlier detection and handling
that were moved from Builder.py to improve code organization and maintainability.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np
import traceback


def handle_outliers(training_data: pd.DataFrame, column: str, strategy: str) -> Dict[str, Any]:
    """
    Handle outliers in a specified column using the chosen strategy.

    Args:
        training_data: DataFrame containing the training data
        column: The column to handle outliers in
        strategy: The strategy to use ('Remove', 'Remove Extreme', 'Cap', 'Isolation Forest', or 'None')

    Returns:
        dict: Result of the operation with success status, message, and modified data
    """
    try:
        # Validate inputs
        if column not in training_data.columns:
            return {
                "success": False,
                "message": f"Column '{column}' not found in the training data"
            }

        if strategy not in ["Remove", "Remove Extreme", "Cap", "Isolation Forest", "None"]:
            return {
                "success": False,
                "message": f"Invalid strategy '{strategy}'. Must be 'Remove', 'Remove Extreme', 'Cap', 'Isolation Forest', or 'None'"
            }

        if strategy == "None":
            return {
                "success": True,
                "message": "No outlier handling applied as per strategy",
                "modified": False,
                "data": training_data
            }

        # Skip if column is not numeric
        if not pd.api.types.is_numeric_dtype(training_data[column]):
            return {
                "success": False,
                "message": f"Column '{column}' is not numeric and cannot be processed for outliers"
            }

        # Check if column is binary
        if training_data[column].nunique() <= 2:
            return {
                "success": False,
                "message": f"Column '{column}' has {training_data[column].nunique()} unique values and should not be processed for outliers"
            }

        # Create a copy to avoid modifying the original data
        data_copy = training_data.copy()

        # Get data and reshape for processing
        data = data_copy[column].to_numpy().reshape(-1, 1)

        if strategy == "Isolation Forest":
            # Import at function level to avoid unnecessary imports
            from sklearn.ensemble import IsolationForest

            # Use Isolation Forest to identify outliers
            iso_forest = IsolationForest(contamination='auto', random_state=42)
            outlier_predictions = iso_forest.fit_predict(data)
            # Isolation Forest returns 1 for inliers and -1 for outliers
            outlier_mask = outlier_predictions == -1
            outlier_count = np.sum(outlier_mask)

            # Remove rows with outliers detected by Isolation Forest
            inlier_mask = ~outlier_mask  # Convert to inlier mask (keeping non-outliers)
            data_copy = data_copy.loc[inlier_mask]

        else:
            # For other strategies, use the IQR method to identify outliers
            flat_data = data.flatten()
            q1 = np.percentile(flat_data, 25)
            q3 = np.percentile(flat_data, 75)
            iqr = q3 - q1

            # Use different multipliers based on strategy
            if strategy == "Remove Extreme":
                # Use 3*IQR for extreme outliers (Tukey's far outliers)
                lower_bound = q1 - 3 * iqr
                upper_bound = q3 + 3 * iqr
            else:
                # Use 1.5*IQR for standard outliers and capping
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

            # Count outliers before handling
            outlier_mask = (flat_data < lower_bound) | (flat_data > upper_bound)
            outlier_count = np.sum(outlier_mask)

            # Apply strategy
            if strategy in ["Remove", "Remove Extreme"]:
                mask = ~outlier_mask
                data_copy = data_copy.loc[mask]

            elif strategy == "Cap":
                data_copy[column] = np.clip(flat_data, lower_bound, upper_bound)

        return {
            "success": True,
            "message": f"Outliers handled successfully. Processed {outlier_count} outliers using '{strategy}' strategy",
            "modified": True,
            "outlier_count": int(outlier_count),
            "data": data_copy
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error handling outliers: {str(e)}"
        }


def suggest_outlier_strategies(training_data: pd.DataFrame, target_column: str) -> Dict[str, Any]:
    """
    Suggest strategies for handling outliers in numerical columns.

    Args:
        training_data: DataFrame containing the training data
        target_column: Name of the target column

    Returns:
        dict: Success status, message, and outlier handling suggestions for each numeric column
    """
    if training_data is None:
        return {
            "success": False,
            "message": "No training data available for analysis"
        }

    try:
        suggestions = {}
        # Get only numeric columns for outlier analysis
        numeric_cols = training_data.select_dtypes(include=['int64', 'float64']).columns

        for column in numeric_cols:
            # Skip binary columns
            if training_data[column].nunique() <= 2:
                suggestions[column] = {
                    "strategy": "None",
                    "reason": f"This column has only {training_data[column].nunique()} unique values and should not be processed for outliers."
                }
                continue

            # Get sample size
            n_samples = len(training_data)

            # Calculate skewness for distribution analysis
            skewness = training_data[column].skew()

            # Check if the column is a potential ID or index column (high cardinality)
            cardinality_ratio = training_data[column].nunique() / n_samples
            is_potential_id = cardinality_ratio > 0.9 and training_data[column].nunique() > 100

            if is_potential_id:
                suggestions[column] = {
                    "strategy": "None",
                    "reason": f"This column has high cardinality ({training_data[column].nunique()} unique values) and may be an ID or index column.",
                    "stats": {
                        "unique_values": int(training_data[column].nunique()),
                        "cardinality_ratio": float(cardinality_ratio),
                        "skewness": float(skewness)
                    }
                }
                continue

            # Determine best outlier detection method based on sample size and distribution
            if n_samples >= 30 and abs(skewness) > 2:  # Use Isolation Forest for skewed data with sufficient samples
                from sklearn.ensemble import IsolationForest

                # Reshape column data for Isolation Forest
                data = training_data[column].to_numpy().reshape(-1, 1)

                # Use Isolation Forest with auto contamination
                iso_forest = IsolationForest(contamination='auto', random_state=42)
                outlier_predictions = iso_forest.fit_predict(data)

                # Count outliers (values with prediction -1)
                outlier_mask = outlier_predictions == -1
                outlier_count = np.sum(outlier_mask)
                outlier_percentage = (outlier_count / n_samples) * 100
            else:
                # Fall back to traditional IQR method for approximate normal distributions or small samples
                data = training_data[column].to_numpy()
                q1 = np.percentile(data, 25)
                q3 = np.percentile(data, 75)
                iqr = q3 - q1

                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                # Find outliers
                outlier_mask = (data < lower_bound) | (data > upper_bound)
                outlier_count = np.sum(outlier_mask)
                outlier_percentage = (outlier_count / n_samples) * 100

                # Also calculate extreme outliers (3*IQR) for recommendation logic
                extreme_lower_bound = q1 - 3 * iqr
                extreme_upper_bound = q3 + 3 * iqr
                extreme_outlier_mask = (data < extreme_lower_bound) | (data > extreme_upper_bound)
                extreme_outlier_count = np.sum(extreme_outlier_mask)
                extreme_outlier_percentage = (extreme_outlier_count / n_samples) * 100

            # Skip target column from recommendations but collect info for display
            if column == target_column:
                continue  # Skip target column from recommendations
            elif outlier_percentage > 25:
                suggestions[column] = {
                    "strategy": "None",
                    "reason": f"{outlier_percentage:.1f}% of values are potential outliers. The data might have a natural skew or non-normal distribution.",
                    "stats": {
                        "outlier_count": int(outlier_count),
                        "outlier_percentage": float(outlier_percentage),
                        "skewness": float(skewness)
                    }
                }
            elif outlier_percentage > 10:
                suggestions[column] = {
                    "strategy": "Cap",
                    "reason": f"{outlier_percentage:.1f}% of values are outliers. Capping at boundaries will preserve data structure while managing extreme values.",
                    "stats": {
                        "outlier_count": int(outlier_count),
                        "outlier_percentage": float(outlier_percentage),
                        "skewness": float(skewness)
                    }
                }
            elif abs(skewness) > 3:
                if n_samples >= 30:
                    suggestions[column] = {
                        "strategy": "Isolation Forest",
                        "reason": f"The data is highly skewed (skewness = {skewness:.2f}). Isolation Forest is effective for detecting and removing outliers in skewed distributions.",
                        "stats": {
                            "outlier_count": int(outlier_count),
                            "outlier_percentage": float(outlier_percentage),
                            "skewness": float(skewness)
                        }
                    }
                else:
                    suggestions[column] = {
                        "strategy": "Cap",
                        "reason": f"The data is skewed (skewness = {skewness:.2f}) but has a small sample size ({n_samples}). Using Cap for stability.",
                        "stats": {
                            "outlier_count": int(outlier_count),
                            "outlier_percentage": float(outlier_percentage),
                            "skewness": float(skewness)
                        }
                    }
            elif outlier_percentage < 1:
                suggestions[column] = {
                    "strategy": "Remove",
                    "reason": f"Only {outlier_percentage:.1f}% of values are outliers. These few extreme values can be safely removed.",
                    "stats": {
                        "outlier_count": int(outlier_count),
                        "outlier_percentage": float(outlier_percentage),
                        "skewness": float(skewness)
                    }
                }
            elif 'extreme_outlier_percentage' in locals() and extreme_outlier_percentage < outlier_percentage * 0.3 and extreme_outlier_count > 0:
                # Recommend Remove Extreme when extreme outliers are much fewer than regular outliers
                # This indicates there are both borderline outliers (that might be valid) and truly extreme ones
                suggestions[column] = {
                    "strategy": "Remove Extreme",
                    "reason": f"Found {extreme_outlier_count} extreme outliers ({extreme_outlier_percentage:.1f}%) vs {outlier_count} total outliers ({outlier_percentage:.1f}%). Remove Extreme targets only truly aberrant values while preserving borderline cases.",
                    "stats": {
                        "outlier_count": int(outlier_count),
                        "outlier_percentage": float(outlier_percentage),
                        "extreme_outlier_count": int(extreme_outlier_count),
                        "extreme_outlier_percentage": float(extreme_outlier_percentage),
                        "skewness": float(skewness)
                    }
                }
            else:
                if n_samples >= 30 and abs(skewness) > 2:
                    suggestions[column] = {
                        "strategy": "Isolation Forest",
                        "reason": f"{outlier_percentage:.1f}% of values are outliers in a skewed distribution. Isolation Forest is better at identifying and removing complex outlier patterns.",
                        "stats": {
                            "outlier_count": int(outlier_count),
                            "outlier_percentage": float(outlier_percentage),
                            "skewness": float(skewness)
                        }
                    }
                else:
                    suggestions[column] = {
                        "strategy": "Cap",
                        "reason": f"{outlier_percentage:.1f}% of values are outliers in an approximately normal distribution. Capping is recommended to preserve data points.",
                        "stats": {
                            "outlier_count": int(outlier_count),
                            "outlier_percentage": float(outlier_percentage),
                            "skewness": float(skewness)
                        }
                    }

        # Analyze target column separately if it exists and is numeric
        target_info = None
        if (target_column and
                target_column in training_data.columns and
                pd.api.types.is_numeric_dtype(training_data[target_column])):

            target_data = training_data[target_column].to_numpy()
            q1_target = np.percentile(target_data, 25)
            q3_target = np.percentile(target_data, 75)
            iqr_target = q3_target - q1_target
            lower_bound_target = q1_target - 1.5 * iqr_target
            upper_bound_target = q3_target + 1.5 * iqr_target
            target_outlier_mask = (target_data < lower_bound_target) | (target_data > upper_bound_target)
            target_outlier_count = np.sum(target_outlier_mask)
            target_outlier_percentage = (target_outlier_count / len(training_data)) * 100
            target_skewness = training_data[target_column].skew()

            # Calculate extreme outliers for target
            extreme_lower_target = q1_target - 3 * iqr_target
            extreme_upper_target = q3_target + 3 * iqr_target
            extreme_target_outlier_mask = (target_data < extreme_lower_target) | (
                        target_data > extreme_upper_target)
            extreme_target_outlier_count = np.sum(extreme_target_outlier_mask)
            extreme_target_outlier_percentage = (extreme_target_outlier_count / len(training_data)) * 100

            # Generate appropriate message based on target outlier analysis
            if target_outlier_percentage > 15:
                message = f"Your target variable '{target_column}' has {target_outlier_percentage:.1f}% outliers. This might indicate a highly skewed distribution or rare valuable cases. Consider domain knowledge before any target modifications."
                severity = "info"
            elif extreme_target_outlier_percentage > 2:
                message = f"Your target variable '{target_column}' has {extreme_target_outlier_count} extreme outliers ({extreme_target_outlier_percentage:.1f}%). These might be data entry errors or extremely rare cases worth investigating."
                severity = "warning"
            elif target_outlier_percentage > 5:
                message = f"Your target variable '{target_column}' has {target_outlier_percentage:.1f}% outliers. These might represent important rare cases that should generally be preserved."
                severity = "info"
            else:
                message = f"Your target variable '{target_column}' appears to have a well-behaved distribution with {target_outlier_percentage:.1f}% outliers."
                severity = "success"

            target_info = {
                "column": target_column,
                "message": message,
                "severity": severity,
                "stats": {
                    "outlier_count": int(target_outlier_count),
                    "outlier_percentage": float(target_outlier_percentage),
                    "extreme_outlier_count": int(extreme_target_outlier_count),
                    "extreme_outlier_percentage": float(extreme_target_outlier_percentage),
                    "skewness": float(target_skewness)
                }
            }
        return {
            "success": True,
            "suggestions": suggestions,
            "columns_analysed": len(suggestions),
            "target_analysis": target_info
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating suggestions: {str(e)}",
            "traceback": traceback.format_exc()
        }
"""
Binning Utilities

This module contains utility functions for feature binning strategies and operations
that were moved from Builder.py to improve code organization and maintainability.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from optbinning import OptimalBinning, ContinuousOptimalBinning


def suggest_binning_strategies(data: pd.DataFrame, target_column: str) -> Dict[str, Any]:
    """Suggest binning strategies for numerical and categorical variables.

    Args:
        data: DataFrame to analyze for binning strategies
        target_column: Name of the target column

    Returns:
        Dict containing success status and binning suggestions
    """
    if data is None:
        return {"success": False, "message": "No data provided"}

    try:
        suggestions = {}

        # Skip processing if target column is not in the dataset
        if target_column not in data.columns:
            return {"success": False, "message": "Target column not found in dataset"}

        # Handle numeric columns
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        # Handle categorical columns
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()

        # Remove target column from both lists if present
        for col_list in [numeric_cols, categorical_cols]:
            if target_column in col_list:
                col_list.remove(target_column)

        # Identify binary features more efficiently (both numeric and categorical)
        nunique_series = data.nunique()
        binary_features = nunique_series[nunique_series == 2].index.tolist()

        # Remove binary features from numeric and categorical columns
        numeric_cols = [col for col in numeric_cols if col not in binary_features]
        categorical_cols = [col for col in categorical_cols if col not in binary_features]

        # Add binary features to suggestions with "None" strategy
        for col in binary_features:
            suggestions[col] = {
                "strategy": "None",
                "reason": "This is a binary feature and does not need binning.",
                "needs_binning": False
            }

        target_type = "continuous" if pd.api.types.is_numeric_dtype(data[target_column]) else "binary"

        # Precompute target values once to avoid repetition
        target_values = data[target_column]
        if not pd.api.types.is_numeric_dtype(target_values):
            target_values = pd.Categorical(target_values).codes

        # Process numeric columns
        _process_numeric_columns(data, numeric_cols, suggestions, target_type, target_values)

        # Process categorical columns
        _process_categorical_columns(data, categorical_cols, suggestions, target_type, target_values)

        return {"success": True, "suggestions": suggestions}
    except Exception as e:
        return {"success": False, "message": f"Error suggesting binning strategies: {str(e)}"}


def apply_binning(
    training_data: pd.DataFrame,
    testing_data: pd.DataFrame,
    strategy_dict: Dict[str, Dict[str, Any]],
    target_column: str
) -> Dict[str, Any]:
    """Apply binning strategies to specified columns.

    Args:
        training_data: Training DataFrame to apply binning to
        testing_data: Testing DataFrame to apply binning to (can be None)
        strategy_dict: Dictionary mapping column names to binning strategies
        target_column: Name of the target column

    Returns:
        Dict containing success status, modified data, and binning results
    """
    if training_data is None:
        return {"success": False, "message": "No training data provided"}

    try:
        # Create copies to avoid modifying original data
        training_copy = training_data.copy()
        testing_copy = testing_data.copy() if testing_data is not None else None

        modified_columns = []
        dropped_columns = []
        bin_ranges = {}
        unchanged_columns = []  # Track columns that weren't actually changed by binning

        # Skip processing if target column is not in the dataset
        if target_column not in training_copy.columns:
            return {"success": False, "message": "Target column not found in dataset"}

        # Precompute target type and values once
        target_type = "continuous" if pd.api.types.is_numeric_dtype(training_copy[target_column]) else "binary"
        target_values = training_copy[target_column]
        if not pd.api.types.is_numeric_dtype(target_values):
            target_values = pd.Categorical(target_values).codes

        # Process each column based on its strategy
        for column, params in strategy_dict.items():
            if column not in training_copy.columns:
                continue

            strategy = params.get("strategy")
            if strategy is None or strategy == "None":
                unchanged_columns.append(column)
                continue

            try:
                _apply_binning_to_column(
                    training_copy, column, params, target_type, target_values,
                    modified_columns, dropped_columns, unchanged_columns, bin_ranges
                )
            except Exception as e:
                return {"success": False, "message": f"Error applying binning to {column}: {str(e)}"}

        # Apply binning to testing data if provided
        if testing_copy is not None:
            _apply_binning_to_testing_data(testing_copy, dropped_columns, modified_columns, bin_ranges)

        return {
            "success": True,
            "message": "Binning applied successfully",
            "training_data": training_copy,
            "testing_data": testing_copy,
            "modified_columns": modified_columns,
            "dropped_columns": dropped_columns,
            "unchanged_columns": unchanged_columns,
            "bin_ranges": bin_ranges
        }
    except Exception as e:
        return {"success": False, "message": f"Error applying binning: {str(e)}"}


def _process_numeric_columns(data, numeric_cols, suggestions, target_type, target_values):
    """Helper method to process numeric columns for binning suggestions."""
    for column in numeric_cols:
        try:
            # Analyse distribution
            unique_count = data[column].nunique()
            skewness = data[column].skew()
            n_samples = len(data)

            # Check for skewed numerical features with low cardinality
            if abs(skewness) > 2 and unique_count < 10:
                suggestions[column] = {
                    "strategy": "Optimal",
                    "reason": f"""This feature is highly skewed (skewness = {skewness:.2f}) and has low cardinality ({unique_count} unique values).
                    We recommend optimal binning because:
                    - The skewness suggests non-linear patterns
                    - The low number of unique values makes it more suitable as a categorical feature
                    - Binning will help capture value groups that are meaningful for prediction""",
                    "needs_binning": True,
                    "convert_to_categorical": True
                }
                continue

            # Only suggest binning for highly skewed features
            if abs(skewness) <= 2:
                suggestions[column] = {
                    "strategy": "None",
                    "reason": f"""This feature has a relatively normal distribution (skewness = {skewness:.2f}).
                    Binning is most useful for features that are highly skewed or have outliers.
                    This feature looks good as it is!""",
                    "needs_binning": False
                }
                continue

            if unique_count < 10:
                suggestions[column] = {
                    "strategy": "None",
                    "reason": f"""This feature only has {unique_count} unique values, which is too few for meaningful binning.
                    Binning works best with continuous variables that have many different values.""",
                    "needs_binning": False
                }
            else:
                _try_optimal_binning_numeric(column, data, unique_count, skewness, n_samples,
                                             target_type, target_values, suggestions)
        except Exception as e:
            suggestions[column] = {
                "strategy": "None",
                "reason": f"Error analyzing column: {str(e)}",
                "needs_binning": False
            }


def _try_optimal_binning_numeric(column, data, unique_count, skewness, n_samples, target_type, target_values,
                                 suggestions):
    """Try to apply optimal binning to numeric columns and capture results."""
    try:
        # Optimize OptBinning configuration
        min_n_bins = 3
        max_n_bins = max(min_n_bins, min(20, unique_count // 5))  # Ensure max_n_bins >= min_n_bins
        min_bin_size = max(0.05, 1 / np.sqrt(n_samples))

        if target_type == "binary":
            binning = OptimalBinning(
                name=column,
                dtype="numerical",
                max_n_bins=max_n_bins,
                min_bin_size=min_bin_size,
                monotonic_trend="auto",
                min_prebin_size=0.01,
                max_pvalue=0.05,
                min_n_bins=min_n_bins,
                max_n_prebins=50,
                cat_cutoff=0.05
            )
        else:
            binning = ContinuousOptimalBinning(
                name=column,
                dtype="numerical",
                max_n_bins=max_n_bins,
                min_bin_size=min_bin_size,
                monotonic_trend="auto",
                min_prebin_size=0.01,
                min_n_bins=min_n_bins,
                max_n_prebins=50
            )

        # Fit the binning model
        binning.fit(data[column], target_values)
        n_bins_optimal = len(binning.splits) + 1

        # Use OptBinning's suggestion if it found meaningful splits
        if n_bins_optimal > 1:
            suggestions[column] = {
                "strategy": "Optimal",
                "reason": f"""This feature is highly skewed (skewness = {skewness:.2f}).
                Optimal binning will help:
                - Make the distribution more balanced
                - Capture non-linear patterns with the target
                - Handle outliers naturally
                - Create statistically significant bins
                - Maximize predictive power""",
                "needs_binning": True,
                "n_bins": n_bins_optimal
            }
        else:
            suggestions[column] = {
                "strategy": "None",
                "reason": "No statistically significant bin splits were found for this feature.",
                "needs_binning": False
            }
    except Exception as e:
        suggestions[column] = {
            "strategy": "None",
            "reason": f"Unable to determine optimal binning strategy: {str(e)}",
            "needs_binning": False
        }


def _process_categorical_columns(data, categorical_cols, suggestions, target_type, target_values):
    """Helper method to process categorical columns for binning suggestions."""
    for column in categorical_cols:
        try:
            unique_count = data[column].nunique()
            n_samples = len(data)

            if unique_count <= 5:
                suggestions[column] = {
                    "strategy": "None",
                    "reason": f"This categorical feature only has {unique_count} unique values, which is few enough to use directly.",
                    "needs_binning": False
                }
                continue

            # For high cardinality categorical variables
            _try_optimal_binning_categorical(column, data, unique_count, n_samples,
                                            target_type, target_values, suggestions)
        except Exception as e:
            suggestions[column] = {
                "strategy": "None",
                "reason": f"Error analyzing column: {str(e)}",
                "needs_binning": False
            }


def _try_optimal_binning_categorical(column, data, unique_count, n_samples, target_type, target_values,
                                     suggestions):
    """Try to apply optimal binning to categorical columns and capture results."""
    try:
        min_n_bins = 3
        max_n_bins = max(min_n_bins, min(10, unique_count // 3))  # Ensure max_n_bins >= min_n_bins
        min_bin_size = max(0.05, 1 / np.sqrt(n_samples))

        if target_type == "binary":
            binning = OptimalBinning(
                name=column,
                dtype="categorical",
                max_n_bins=max_n_bins,
                min_bin_size=min_bin_size,
                cat_cutoff=0.05,
                max_pvalue=0.05,
                min_n_bins=min_n_bins
            )
        else:
            binning = ContinuousOptimalBinning(
                name=column,
                dtype="categorical",
                max_n_bins=max_n_bins,
                min_bin_size=min_bin_size,
                min_n_bins=min_n_bins
            )

        # Fit the binning model
        binning.fit(data[column], target_values)

        suggestions[column] = {
            "strategy": "Optimal",
            "reason": f"""This categorical feature has {unique_count} unique values, which is relatively high.
            Optimal binning will:
            - Group similar categories based on target relationship
            - Create statistically significant bins
            - Handle rare categories effectively
            - Maximize predictive power""",
            "needs_binning": True,
            "n_bins": max_n_bins
        }
    except Exception as e:
        suggestions[column] = {
            "strategy": "None",
            "reason": f"Unable to determine optimal binning strategy: {str(e)}",
            "needs_binning": False
        }


def _apply_binning_to_column(data, column, params, target_type, target_values,
                             modified_columns, dropped_columns, unchanged_columns, bin_ranges):
    """Apply binning to a single column based on the strategy."""
    binned_col = f"{column}_binned"
    strategy = params.get("strategy")
    convert_to_categorical = params.get("convert_to_categorical", False)
    is_categorical = data[column].dtype == 'object' or data[column].dtype.name == 'category'

    # Handle direct categorical conversion
    if convert_to_categorical:
        _convert_numerical_to_categorical(
            data, column, binned_col, modified_columns, dropped_columns, bin_ranges
        )
        return

    # Handle optimal binning
    if strategy == "Optimal":
        n_samples = len(data)
        unique_count = data[column].nunique()

        # Get binning parameters
        binning_params = _get_optimal_binning_params(n_samples, unique_count, is_categorical)

        # Apply optimal binning
        _apply_optimal_binning(
            data, column, binned_col, is_categorical, target_type, target_values,
            binning_params, unique_count, modified_columns, dropped_columns,
            unchanged_columns, bin_ranges
        )


def _convert_numerical_to_categorical(data, column, binned_col,
                                      modified_columns, dropped_columns, bin_ranges):
    """Convert numerical column to categorical."""
    unique_values = sorted(data[column].unique())
    value_map = {val: f"category_{i + 1}" for i, val in enumerate(unique_values)}
    data[binned_col] = data[column].map(value_map).astype('category')

    bin_ranges[binned_col] = {f"category_{i + 1}": [str(val)] for i, val in enumerate(unique_values)}
    modified_columns.append(binned_col)
    dropped_columns.append(column)
    data.drop(columns=[column], inplace=True)


def _get_optimal_binning_params(n_samples, unique_count, is_categorical=False):
    """Get optimal binning parameters based on data characteristics."""
    min_n_bins = 3
    max_n_bins = max(min_n_bins, min(20 if not is_categorical else 10,
                                     unique_count // (5 if not is_categorical else 3)))
    min_bin_size = max(0.05, 1 / np.sqrt(n_samples))

    common_params = {
        "min_n_bins": min_n_bins,
        "max_n_bins": max_n_bins,
        "min_bin_size": min_bin_size,
    }

    if is_categorical:
        return common_params

    return {
        **common_params,
        "monotonic_trend": "auto",
        "min_prebin_size": 0.01,
        "max_n_prebins": 50,
    }


def _apply_optimal_binning(data, column, binned_col, is_categorical, target_type,
                           target_values, binning_params, unique_count, modified_columns,
                           dropped_columns, unchanged_columns, bin_ranges):
    """Apply optimal binning to a column."""
    # Configure binning based on data type
    binning_class = OptimalBinning if target_type == "binary" else ContinuousOptimalBinning
    additional_params = {"cat_cutoff": 0.05, "max_pvalue": 0.05} if target_type == "binary" else {}

    binning = binning_class(
        name=column,
        dtype="categorical" if is_categorical else "numerical",
        **binning_params,
        **additional_params
    )

    # Fit and transform data
    binning.fit(data[column], target_values)
    data[binned_col] = binning.transform(data[column], metric="indices")

    if is_categorical:
        _handle_categorical_binning(
            data, column, binned_col, binning, unique_count,
            modified_columns, dropped_columns, unchanged_columns, bin_ranges
        )
    else:
        _handle_numerical_binning(
            data, column, binned_col, binning,
            modified_columns, dropped_columns, unchanged_columns, bin_ranges
        )


def _handle_categorical_binning(data, column, binned_col, binning, original_unique_count,
                                modified_columns, dropped_columns, unchanged_columns, bin_ranges):
    """Handle categorical optimal binning results."""
    binned_unique_count = data[binned_col].nunique()

    # Skip if binning didn't reduce cardinality
    if binned_unique_count >= original_unique_count:
        data.drop(columns=[binned_col], inplace=True)
        unchanged_columns.append(column)
        return

    # Create category mappings
    unique_values = data[column].unique()
    bin_assignments = binning.transform(unique_values, metric="indices")

    category_mappings = {}
    for value, bin_num in zip(unique_values, bin_assignments):
        bin_id = str(int(bin_num))
        if bin_id not in category_mappings:
            category_mappings[bin_id] = []
        category_mappings[bin_id].append(str(value))

    bin_ranges[binned_col] = category_mappings
    data[binned_col] = data[binned_col].astype('category')

    modified_columns.append(binned_col)
    dropped_columns.append(column)
    data.drop(columns=[column], inplace=True)


def _handle_numerical_binning(data, column, binned_col, binning,
                              modified_columns, dropped_columns, unchanged_columns, bin_ranges):
    """Handle numerical optimal binning results."""
    splits = binning.splits

    if len(splits) > 0:
        bin_edges = [-np.inf] + list(splits) + [np.inf]
        bin_ranges[binned_col] = list(zip(bin_edges[:-1], bin_edges[1:]))

        data[binned_col] = data[binned_col].astype('category')
        modified_columns.append(binned_col)
        dropped_columns.append(column)
        data.drop(columns=[column], inplace=True)
    else:
        data.drop(columns=[binned_col], inplace=True)
        unchanged_columns.append(column)


def _apply_binning_to_testing_data(testing_data, dropped_columns, modified_columns, bin_ranges):
    """Apply binning transformations to testing data."""
    for orig_col, binned_col in zip(dropped_columns, modified_columns):
        if binned_col in bin_ranges and orig_col in testing_data.columns:
            is_categorical = (testing_data[orig_col].dtype == 'object' or
                              testing_data[orig_col].dtype.name == 'category')

            if is_categorical:
                _apply_categorical_binning_to_testing(testing_data, orig_col, binned_col, bin_ranges)
            else:
                _apply_numerical_binning_to_testing(testing_data, orig_col, binned_col, bin_ranges)


def _apply_categorical_binning_to_testing(testing_data, orig_col, binned_col, bin_ranges):
    """Apply categorical binning to testing data."""
    category_mappings = bin_ranges[binned_col]
    # Create a map from original values to bin indices
    value_to_bin = {}
    for bin_id, categories in category_mappings.items():
        for category in categories:
            value_to_bin[category] = bin_id

    # Apply the mapping
    testing_data[binned_col] = testing_data[orig_col].astype(str).map(value_to_bin)
    testing_data[binned_col] = testing_data[binned_col].astype('category')

    # Drop the original column
    testing_data.drop(columns=[orig_col], inplace=True)


def _apply_numerical_binning_to_testing(testing_data, orig_col, binned_col, bin_ranges):
    """Apply numerical binning to testing data."""
    bin_edges = bin_ranges[binned_col]

    # Create a function to assign values to bins
    def assign_bin(x):
        for i, (lower, upper) in enumerate(bin_edges):
            if lower < x <= upper or (np.isneginf(lower) and x <= upper) or (np.isposinf(upper) and x > lower):
                return i
        return np.nan

    # Apply binning
    testing_data[binned_col] = testing_data[orig_col].apply(assign_bin)
    testing_data[binned_col] = testing_data[binned_col].astype('category')

    # Drop the original column
    testing_data.drop(columns=[orig_col], inplace=True)
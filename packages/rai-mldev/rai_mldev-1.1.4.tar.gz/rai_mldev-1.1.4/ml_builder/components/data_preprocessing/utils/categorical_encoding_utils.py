"""
Categorical Encoding Utilities

This module contains utility functions for categorical variable encoding strategies
that were moved from Builder.py to improve code organization and maintainability.
"""

from typing import Dict, Any
import pandas as pd
import traceback


def suggest_encoding_strategies(data: pd.DataFrame, target_column: str = None) -> Dict[str, Any]:
    """Suggest encoding strategies for categorical variables.

    Args:
        data: DataFrame to analyze for encoding strategies
        target_column: Name of the target column (optional, for filtering)

    Returns:
        Dict containing success status and encoding suggestions
    """
    if data is None:
        return {"success": False, "message": "No data provided"}

    try:
        # Update to detect both object and category dtypes
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        suggestions = {}

        for col in categorical_cols:
            # Skip target column if specified
            if target_column and col == target_column:
                continue

            unique_count = data[col].nunique()
            total_count = len(data)
            cardinality_ratio = unique_count / total_count

            if cardinality_ratio > 0.5:
                suggestions[col] = {
                    "strategy": "target",
                    "reason": f"High cardinality ({unique_count} unique values) - target encoding recommended"
                }
            elif unique_count <= 2:
                suggestions[col] = {
                    "strategy": "label",
                    "reason": "Binary categorical variable - label encoding recommended"
                }
            elif unique_count <= 10:
                suggestions[col] = {
                    "strategy": "onehot",
                    "reason": f"Low cardinality ({unique_count} categories) - one-hot encoding recommended"
                }
            else:
                suggestions[col] = {
                    "strategy": "target",
                    "reason": f"Medium-high cardinality ({unique_count} categories) - target encoding recommended"
                }

        return {
            "success": True,
            "suggestions": suggestions
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error suggesting encoding strategies: {str(e)}"
        }


def handle_categorical_data(
    data: pd.DataFrame,
    handling_dict: Dict[str, Dict],
    target_column: str,
    encoding_mappings: Dict[str, Any] = None,
    is_training: bool = True
) -> Dict[str, Any]:
    """Handle categorical variables with encoding or dropping options.

    Args:
        data: DataFrame to process
        handling_dict: Dictionary with column names as keys and encoding strategies as values
        target_column: Name of the target column
        encoding_mappings: Dictionary to store/retrieve encoding mappings
        is_training: Whether this is being called on training data (to fit encoders) or test data (to apply existing encodings)

    Returns:
        Dict containing success status, modified data, and encoding mappings
    """
    if data is None:
        return {"success": False, "message": "No data provided"}

    if encoding_mappings is None:
        encoding_mappings = {}

    try:
        from sklearn.preprocessing import LabelEncoder, OneHotEncoder

        data_copy = data.copy()
        strategies_applied = {}
        modified_columns = []
        dropped_columns = []

        # Create OneHotEncoder for all columns that need it
        onehot_columns = [
            col for col, strategy in handling_dict.items()
            if strategy.get("method") == "onehot"
        ]

        if onehot_columns:
            # Version-agnostic OneHotEncoder initialization
            try:
                # Try newer scikit-learn version syntax
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            except TypeError:
                # Fall back to older scikit-learn version syntax
                encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')

        for column, strategy in handling_dict.items():
            # Skip if column is the target or if column doesn't exist in the data
            if column == target_column or column not in data_copy.columns:
                continue

            method = strategy["method"]

            if method == "drop_column":
                data_copy = data_copy.drop(columns=[column])
                strategies_applied[column] = "Dropped column"
                dropped_columns.append(column)
                # Clear any existing mapping for dropped columns if we're in training mode
                if is_training and column in encoding_mappings:
                    del encoding_mappings[column]

            elif method == "drop_rows":
                values_to_drop = strategy["values"]
                initial_rows = len(data_copy)
                data_copy = data_copy[~data_copy[column].isin(values_to_drop)]
                rows_dropped = initial_rows - len(data_copy)
                strategies_applied[column] = f"Dropped {rows_dropped} rows with values: {values_to_drop}"
                modified_columns.append(column)

            elif method == "label":
                if is_training:
                    # Training mode: fit encoder and store mapping
                    le = LabelEncoder()
                    original_values = data_copy[column].astype(str).unique()
                    data_copy[column] = le.fit_transform(data_copy[column].astype(str))

                    # Create mappings: original value → encoded value
                    # This is the natural way people think about encoding
                    encoded_values = le.transform(le.classes_)
                    mapping = dict(zip(le.classes_, encoded_values))

                    # Create reverse mapping for decoding if needed
                    reverse_mapping = dict(zip(encoded_values, le.classes_))

                    strategies_applied[column] = {
                        "method": "Label Encoding",
                        "mapping": mapping
                    }

                    # Store mapping with original values for display and future use
                    encoding_mappings[column] = {
                        "method": "Label Encoding",
                        "mapping": mapping,
                        "reverse_mapping": reverse_mapping,
                        "original_values": original_values.tolist(),
                        "encoded_values": encoded_values.tolist(),
                        "classes": le.classes_.tolist()
                    }
                else:
                    # Test mode: apply existing mapping
                    if column in encoding_mappings and encoding_mappings[column]["method"] == "Label Encoding":
                        # Create a mapping function that handles unseen categories
                        mapping = encoding_mappings[column]["mapping"]

                        # Apply mapping with fallback for unseen values
                        def apply_mapping(val):
                            val_str = str(val)
                            if val_str in mapping:
                                return mapping[val_str]
                            else:
                                # Use -1 or some other indicator for unseen values
                                return -1

                        data_copy[column] = data_copy[column].astype(str).apply(apply_mapping)
                        strategies_applied[column] = {
                            "method": "Label Encoding (applied from training)",
                            "unseen_values_handled": True
                        }
                    else:
                        # No mapping available
                        return {
                            "success": False,
                            "message": f"No label encoding mapping found for column {column}"
                        }

                modified_columns.append(column)

            elif method == "onehot":
                if is_training:
                    # Training mode: fit and transform
                    # Prepare the data for transformation
                    column_data = data_copy[[column]].astype(str)

                    # Fit and transform the data
                    encoded_data = encoder.fit_transform(column_data)

                    # Get feature names from the encoder and clean them up
                    feature_names = [
                        f"{column}_{val.split('_')[-1]}" for val in encoder.get_feature_names_out([column])
                    ]

                    # Convert to DataFrame and add to original data
                    encoded_df = pd.DataFrame(
                        encoded_data,
                        columns=feature_names,
                        index=data_copy.index
                    )

                    # Store mapping information
                    # Store the categories explicitly instead of relying on the encoder object
                    categories = encoder.categories_[0].tolist()
                    encoding_mappings[column] = {
                        "method": "One-Hot Encoding",
                        "original_values": column_data[column].unique().tolist(),
                        "new_columns": feature_names,
                        "categories": categories,
                        "encoder": encoder  # Still store the encoder as a backup
                    }

                    # Drop original column and add encoded columns
                    data_copy = data_copy.drop(columns=[column])
                    data_copy = pd.concat([data_copy, encoded_df], axis=1)

                    strategies_applied[column] = {
                        "method": "One-Hot Encoding",
                        "new_columns": feature_names
                    }
                else:
                    # Test mode: transform using the fitted encoder
                    if column in encoding_mappings and encoding_mappings[column]["method"] == "One-Hot Encoding":
                        try:
                            # First try with the stored encoder
                            if "encoder" in encoding_mappings[column]:
                                column_data = data_copy[[column]].astype(str)
                                encoder = encoding_mappings[column]["encoder"]
                                feature_names = encoding_mappings[column]["new_columns"]

                                # Transform the data (handle_unknown='ignore' will handle new categories)
                                encoded_data = encoder.transform(column_data)

                                # Convert to DataFrame and add to original data
                                encoded_df = pd.DataFrame(
                                    encoded_data,
                                    columns=feature_names,
                                    index=data_copy.index
                                )

                                # Drop original column and add encoded columns
                                data_copy = data_copy.drop(columns=[column])
                                data_copy = pd.concat([data_copy, encoded_df], axis=1)

                                strategies_applied[column] = {
                                    "method": "One-Hot Encoding (applied from training)",
                                    "new_columns": feature_names
                                }
                            else:
                                raise ValueError("Encoder not found in mapping")
                        except Exception as enc_error:
                            # Fallback to manual encoding if the encoder fails
                            if "categories" in encoding_mappings[column]:
                                categories = encoding_mappings[column]["categories"]
                                feature_names = encoding_mappings[column]["new_columns"]

                                # Manual one-hot encoding
                                for category, feature_name in zip(categories, feature_names):
                                    data_copy[feature_name] = (data_copy[column].astype(str) == category).astype(int)

                                # Drop original column
                                data_copy = data_copy.drop(columns=[column])

                                strategies_applied[column] = {
                                    "method": "One-Hot Encoding (manually applied from training)",
                                    "new_columns": feature_names
                                }
                            else:
                                # Fallback to original implementation
                                original_values = encoding_mappings[column]["original_values"]
                                feature_names = encoding_mappings[column]["new_columns"]

                                # Create a one-hot encoding manually
                                for value, feature_name in zip(original_values, feature_names):
                                    data_copy[feature_name] = (data_copy[column].astype(str) == value).astype(int)

                                # Drop original column
                                data_copy = data_copy.drop(columns=[column])

                                strategies_applied[column] = {
                                    "method": "One-Hot Encoding (manually applied from training)",
                                    "new_columns": feature_names
                                }
                    else:
                        # No mapping available
                        return {
                            "success": False,
                            "message": f"No one-hot encoding mapping found for column {column}"
                        }

                modified_columns.append(column)

            elif method == "target":
                if is_training:
                    # Use mean target encoding
                    target_means = data_copy.groupby(column)[target_column].mean()
                    original_values = data_copy[column].unique()
                    # Map the values
                    data_copy[column] = data_copy[column].map(target_means)
                    mapping = target_means.to_dict()
                    strategies_applied[column] = {
                        "method": "Target Encoding",
                        "mapping": mapping
                    }
                    # Store mapping with original values for display
                    encoding_mappings[column] = {
                        "method": "Target Encoding",
                        "mapping": mapping,
                        "original_values": original_values.tolist(),
                        "target_means": target_means.tolist()
                    }
                else:
                    # Test mode: apply existing mapping
                    if column in encoding_mappings and encoding_mappings[column]["method"] == "Target Encoding":
                        mapping = encoding_mappings[column]["mapping"]
                        global_mean = sum(mapping.values()) / len(mapping) if mapping else 0

                        # Apply mapping with fallback for unseen values
                        def apply_target_mapping(val):
                            if val in mapping:
                                return mapping[val]
                            else:
                                # Use global mean for unseen values
                                return global_mean

                        data_copy[column] = data_copy[column].apply(apply_target_mapping)
                        strategies_applied[column] = {
                            "method": "Target Encoding (applied from training)",
                            "unseen_values_handled": True
                        }
                    else:
                        # No mapping available
                        return {
                            "success": False,
                            "message": f"No target encoding mapping found for column {column}"
                        }

                modified_columns.append(column)

        return {
            "success": True,
            "message": "Categorical variables handled successfully",
            "data": data_copy,
            "strategies_applied": strategies_applied,
            "modified_columns": modified_columns,
            "dropped_columns": dropped_columns,
            "new_shape": data_copy.shape,
            "encoding_mappings": encoding_mappings  # Include mappings in the response
        }
    except Exception as e:
        traceback_str = traceback.format_exc()
        return {
            "success": False,
            "message": f"Error handling categorical data: {str(e)}",
            "traceback": traceback_str
        }
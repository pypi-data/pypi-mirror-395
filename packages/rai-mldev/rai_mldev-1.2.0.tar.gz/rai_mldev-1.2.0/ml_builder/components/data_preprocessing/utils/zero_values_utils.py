"""
Zero Values Analysis Utilities

This module contains utility functions for zero values analysis and handling
that were moved from Builder.py to improve code organization and maintainability.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


def analyse_zero_values(data: pd.DataFrame) -> Dict[str, Any]:
    """Analyse zero values in numerical columns, excluding binary features.

    Args:
        data: DataFrame to analyze for zero values

    Returns:
        Dict containing success status and zero values statistics
    """
    if data is None:
        return {
            "success": False,
            "message": "No data provided"
        }

    try:
        # Get numerical columns
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns

        # Filter out binary columns (those with only 0s and 1s)
        non_binary_cols = [
            col for col in numeric_cols
            if not set(data[col].unique()).issubset({0, 1, np.nan})
        ]

        # Analyse zeros in each column
        zero_stats = {}
        for col in non_binary_cols:
            zeros_count = (data[col] == 0).sum()
            if zeros_count > 0:
                zero_stats[col] = {
                    'count': zeros_count,
                    'percentage': (zeros_count / len(data) * 100)
                }

        return {
            "success": True,
            "stats": zero_stats
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error analyzing zero values: {str(e)}"
        }


def handle_zero_values(data: pd.DataFrame, strategy_dict: Dict[str, str]) -> Dict[str, Any]:
    """Handle zero values according to specified strategies.

    Args:
        data: DataFrame to process
        strategy_dict: Dictionary mapping column names to strategies ('remove', 'null', 'keep')

    Returns:
        Dict containing success status, modified data, and operation results
    """
    if data is None:
        return {
            "success": False,
            "message": "No data provided"
        }

    try:
        modified_data = data.copy()
        modified_columns = []
        attempted_columns = list(strategy_dict.keys())
        results_by_column = {}

        for column, strategy in strategy_dict.items():
            # Check if column exists in the dataset
            if column not in modified_data.columns:
                results_by_column[column] = {
                    "success": False,
                    "reason": "Column not found in dataset",
                    "strategy": strategy
                }
                continue

            # Track results for each column
            column_result = {
                "strategy": strategy,
                "success": True,
                "zeros_before": int((modified_data[column] == 0).sum())
            }

            if strategy == "remove":
                # Keep track of original length
                original_len = len(modified_data)
                modified_data = modified_data[modified_data[column] != 0]
                rows_removed = original_len - len(modified_data)

                column_result["rows_removed"] = rows_removed

                if rows_removed > 0:
                    modified_columns.append(column)
                    column_result["modified"] = True
                else:
                    column_result["modified"] = False
                    column_result["reason"] = "No rows removed - possibly no zeros found despite initial analysis"

            elif strategy == "null":
                # Only modify if there are zeros to convert
                zeros_mask = modified_data[column] == 0
                zeros_count = zeros_mask.sum()

                if zeros_count > 0:
                    modified_data.loc[zeros_mask, column] = None
                    modified_columns.append(column)
                    column_result["zeros_converted"] = int(zeros_count)
                    column_result["modified"] = True
                else:
                    column_result["zeros_converted"] = 0
                    column_result["modified"] = False
                    column_result["reason"] = "No zeros found to convert despite initial analysis"

            # "keep" strategy requires no action
            elif strategy == "keep":
                column_result["modified"] = False
                column_result["reason"] = "Keep strategy selected - no changes needed"

            results_by_column[column] = column_result

        return {
            "success": True,
            "message": "Zero values handled successfully",
            "data": modified_data,
            "modified_columns": modified_columns,
            "attempted_columns": attempted_columns,
            "column_results": results_by_column
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error handling zero values: {str(e)}"
        }
"""
Missing Values Analysis Utilities

This module contains utility functions for analyzing missing values patterns in datasets.
Extracted from Builder.analyse_missing_values() to improve code organization.
"""
from typing import Dict, Any
import pandas as pd
import plotly.express as px


def analyze_missing_values(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze missing values and their patterns in a dataset.

    Args:
        data: The pandas DataFrame to analyze

    Returns:
        Dictionary containing missing value statistics and visualizations
    """
    if data is None:
        return {"error": "No data provided"}

    try:
        # Calculate missing value statistics
        missing_stats = {
            'total_missing': data.isnull().sum().sum(),
            'missing_by_column': data.isnull().sum().to_dict(),
            'missing_percentage': (data.isnull().sum() / len(data) * 100).to_dict()
        }

        # Create missing values heatmap
        fig_missing = px.imshow(
            data.isnull(),
            title='Missing Values Pattern',
            labels={'color': 'Missing'},
            color_continuous_scale=['#ffffff', '#ff0000']
        )

        # Analyze relationships between missing values
        missing_correlations = data.isnull().corr()
        fig_corr = px.imshow(
            missing_correlations,
            title='Missing Value Correlations',
            labels={'color': 'Correlation'},
            color_continuous_scale='RdBu'
        )

        return {
            "success": True,
            "stats": missing_stats,
            "visualisations": {
                "pattern": fig_missing,
                "correlations": fig_corr
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error analyzing missing values: {str(e)}"
        }
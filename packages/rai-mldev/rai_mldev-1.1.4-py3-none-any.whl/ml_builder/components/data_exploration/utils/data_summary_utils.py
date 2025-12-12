"""
Data Summary Utilities

This module contains utility functions for generating data summaries and visualizations
that were extracted from the Builder.get_data_summary() method to improve code organization
and reusability.
"""
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from dython.nominal import identify_nominal_columns, associations


def generate_feature_associations(data: pd.DataFrame, target_column: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate feature associations using dython library.

    Args:
        data: The pandas DataFrame to analyze
        target_column: Optional target column name. If provided, will be included in associations

    Returns:
        Dictionary containing associations matrix data and metadata
    """
    try:
        # Create a copy of the data for associations
        data_for_assoc = data.copy()

        # Convert all object columns to category
        for col in data_for_assoc.select_dtypes(['object']):
            data_for_assoc[col] = data_for_assoc[col].astype('category')

        # Handle multiclass classification target properly
        categorical_features = []

        # Check if target should be treated as categorical based on session state
        if (target_column and
            hasattr(st.session_state, 'problem_type') and
            st.session_state.problem_type in ['binary_classification', 'multiclass_classification'] and
            target_column in data_for_assoc.columns):
            # Force target to be treated as categorical for classification problems
            data_for_assoc[target_column] = data_for_assoc[target_column].astype('category')
            categorical_features.append(target_column)

        # Identify other categorical columns using dython
        auto_categorical = identify_nominal_columns(data_for_assoc)
        categorical_features.extend([col for col in auto_categorical if col not in categorical_features])

        # Remove duplicates
        categorical_features = list(set(categorical_features))

        # Handle any missing values
        # if feature is categorical, fill with mode, if numeric, fill with median
        for col in data_for_assoc.columns:
            if data_for_assoc[col].dtype in ['object', 'category']:
                mode_val = data_for_assoc[col].mode()
                if len(mode_val) > 0:
                    data_for_assoc[col] = data_for_assoc[col].fillna(mode_val.iloc[0])
            else:
                data_for_assoc[col] = data_for_assoc[col].fillna(data_for_assoc[col].median())

        # Calculate associations with error handling
        complete_correlation = associations(
            data_for_assoc,
            nominal_columns=categorical_features,
            plot=False,
            compute_only=True
        )

        # Get correlation matrix from the dictionary
        df_complete_corr = pd.DataFrame(
            complete_correlation['corr'],
            index=data_for_assoc.columns,
            columns=data_for_assoc.columns
        )

        # Convert to numpy array and handle any non-finite values
        corr_values = df_complete_corr.values
        corr_values = np.nan_to_num(corr_values, nan=0)

        # Convert the correlation matrix to a regular DataFrame with rounded values
        df_display = pd.DataFrame(
            np.round(corr_values, 2),
            index=df_complete_corr.index,
            columns=df_complete_corr.columns
        )

        return {
            "success": True,
            "associations_matrix": {
                "data": df_display,
                "styled": df_complete_corr.style.background_gradient(
                    cmap='coolwarm',
                    axis=None
                ).format(precision=2)
            },
            "correlation_values": corr_values,
            "categorical_features": categorical_features,
            "columns": df_complete_corr.columns.tolist(),
            "index": df_complete_corr.index.tolist()
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error calculating feature associations: {str(e)}",
            "associations_matrix": None
        }


def generate_associations_visualization(associations_data: Dict[str, Any]) -> Optional[Any]:
    """
    Generate the associations heatmap visualization using plotly.

    Args:
        associations_data: Dictionary returned by generate_feature_associations()

    Returns:
        Plotly figure object or None if error
    """
    try:
        if not associations_data["success"]:
            return None

        corr_values = associations_data["correlation_values"]
        columns = associations_data["columns"]
        index = associations_data["index"]

        # Create heatmap using plotly
        associations_fig = px.imshow(
            corr_values,
            x=columns,
            y=index,
            color_continuous_scale='RdBu',
            aspect='auto',
            title='Feature Associations Heatmap',
            zmin=-1,
            zmax=1
        )

        # Update layout
        associations_fig.update_layout(
            height=800,
            width=800,
            xaxis_tickangle=-45
        )

        # Add text annotations
        associations_fig.update_traces(
            text=np.round(corr_values, 2),
            texttemplate="%{text}"
        )

        return associations_fig

    except Exception as e:
        print(f"Error creating associations visualization: {str(e)}")
        return None


def get_basic_data_info(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Get basic data information including dtypes and missing values.

    Args:
        data: The pandas DataFrame to analyze

    Returns:
        Dictionary containing basic data information
    """
    try:
        return {
            "success": True,
            "dtypes": {col: str(dtype) for col, dtype in data.dtypes.to_dict().items()},
            "missing_values": data.isnull().sum().to_dict(),
            "shape": data.shape,
            "columns": data.columns.tolist()
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting basic data info: {str(e)}"
        }


def generate_data_summary(data: pd.DataFrame, target_column: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a comprehensive data summary with only the essential components needed
    by the data exploration page and its components.

    Args:
        data: The pandas DataFrame to analyze
        target_column: Optional target column name

    Returns:
        Dictionary containing summary data and visualizations
    """
    if data is None:
        return {"error": "No data provided"}

    try:
        # Get basic data info
        basic_info = get_basic_data_info(data)
        if not basic_info["success"]:
            return {"error": basic_info["error"]}

        # Generate feature associations
        associations_data = generate_feature_associations(data, target_column)

        # Create visualizations dictionary
        figs = {}
        associations_matrix = None

        if associations_data["success"]:
            # Generate associations visualization
            associations_fig = generate_associations_visualization(associations_data)
            if associations_fig is not None:
                figs["associations"] = associations_fig

            associations_matrix = associations_data["associations_matrix"]

        return {
            "summary": data.describe().to_dict(),  # Add basic summary statistics for compatibility
            "dtypes": basic_info["dtypes"],
            "missing_values": basic_info["missing_values"],
            "visualisations": figs,
            "associations_matrix": associations_matrix
        }

    except Exception as e:
        return {
            "error": f"Error generating data summary: {str(e)}"
        }
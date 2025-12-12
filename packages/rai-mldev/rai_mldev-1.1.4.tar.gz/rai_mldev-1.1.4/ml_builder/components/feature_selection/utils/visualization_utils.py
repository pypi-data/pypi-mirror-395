"""
Visualization utilities for feature selection components.

This module contains functions for creating various plots and visualizations
used in the feature selection process.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from typing import List, Dict, Any, Tuple


def create_feature_importance_plot(feature_scores: pd.DataFrame,
                                 title: str = "Feature Importance Distribution") -> go.Figure:
    """
    Create an enhanced feature importance bar plot.

    Args:
        feature_scores: DataFrame with 'feature' and 'importance' columns
        title: Title for the plot

    Returns:
        Plotly Figure object
    """
    importance_fig = go.Figure()
    importance_fig.add_trace(go.Bar(
        x=feature_scores['feature'],
        y=feature_scores['importance'],
        marker_color=np.where(feature_scores['importance'] > 0.1, 'rgb(26, 118, 255)',
                            np.where(feature_scores['importance'] > 0.05, 'rgb(158, 201, 255)',
                                    'rgb(224, 236, 255)')),
        hovertemplate='<b>%{x}</b><br>Importance: %{y:.3f}<extra></extra>'
    ))
    importance_fig.update_layout(
        title=title,
        xaxis_title='Features',
        yaxis_title='Importance Score',
        showlegend=False,
        height=500,
        xaxis={'tickangle': 45},
        yaxis={'range': [0, max(feature_scores['importance']) * 1.1]} if len(feature_scores) > 0 else None,
        annotations=[
            dict(
                x=0.5,
                y=1.1,
                xref='paper',
                yref='paper',
                text='Higher bars indicate more important features',
                showarrow=False,
                font=dict(size=12)
            )
        ]
    )
    # Add threshold lines
    importance_fig.add_hline(y=0.1, line_dash="dash", line_color="blue",
                           annotation_text="High Importance")
    importance_fig.add_hline(y=0.05, line_dash="dash", line_color="lightblue",
                           annotation_text="Medium Importance")
    return importance_fig


def create_low_importance_plot(low_imp_scores: pd.DataFrame,
                             title: str = "Low Importance Features") -> go.Figure:
    """
    Create a plot specifically for low importance features.

    Args:
        low_imp_scores: DataFrame with low importance features
        title: Title for the plot

    Returns:
        Plotly Figure object
    """
    low_imp_fig = go.Figure(data=[go.Bar(
        x=low_imp_scores['feature'],
        y=low_imp_scores['importance'],
        marker_color='lightcoral',
        hovertemplate='<b>%{x}</b><br>Importance: %{y:.3f}<extra></extra>'
    )])

    low_imp_fig.update_layout(
        title=title,
        xaxis_title='Features',
        yaxis_title='Importance Score',
        showlegend=False,
        height=300,
        xaxis={'tickangle': 45}
    )

    return low_imp_fig


def create_correlation_network_plot(correlations: List[Dict[str, Any]],
                                  title: str = "Feature Correlation Network") -> go.Figure:
    """
    Create a network visualization of feature correlations.

    Args:
        correlations: List of correlation dictionaries with 'feature1', 'feature2', 'correlation'
        title: Title for the plot

    Returns:
        Plotly Figure object
    """
    corr_fig = go.Figure()
    edges_x = []
    edges_y = []
    edge_text = []

    # Create a simple force-directed layout
    n_features = len(set([c['feature1'] for c in correlations] +
                      [c['feature2'] for c in correlations]))
    radius = 1
    angle = 2 * math.pi / n_features if n_features > 0 else 0
    feature_positions = {}

    # Assign positions to features
    i = 0
    for corr in correlations:
        for feat in [corr['feature1'], corr['feature2']]:
            if feat not in feature_positions:
                feature_positions[feat] = (
                    radius * math.cos(i * angle),
                    radius * math.sin(i * angle)
                )
                i += 1

    # Create edges
    for corr in correlations:
        x0, y0 = feature_positions[corr['feature1']]
        x1, y1 = feature_positions[corr['feature2']]
        edges_x.extend([x0, x1, None])
        edges_y.extend([y0, y1, None])
        edge_text.append(f"{corr['feature1']} - {corr['feature2']}: {corr['correlation']:.2f}")

    # Add edges
    corr_fig.add_trace(go.Scatter(
        x=edges_x, y=edges_y,
        line=dict(width=1, color='#888'),
        hoverinfo='text',
        text=edge_text,
        mode='lines'
    ))

    # Add nodes
    node_x = [pos[0] for pos in feature_positions.values()]
    node_y = [pos[1] for pos in feature_positions.values()]

    corr_fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=list(feature_positions.keys()),
        textposition="top center",
        marker=dict(
            size=20,
            color='lightblue',
            line_width=2
        )
    ))

    corr_fig.update_layout(
        title=title,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400
    )

    return corr_fig


def create_feature_status_plot(feature_ranking: List[Dict[str, Any]],
                             title: str = "Feature Importance by Status") -> go.Figure:
    """
    Create a plot showing feature importance colored by status (for Boruta results).

    Args:
        feature_ranking: List of dictionaries with feature, importance, and status
        title: Title for the plot

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    # Add bars for each feature status
    colors = {
        "Confirmed": "rgba(46, 204, 113, 0.8)",
        "Tentative": "rgba(241, 196, 15, 0.8)",
        "Rejected": "rgba(231, 76, 60, 0.8)"
    }

    for status in ["Confirmed", "Tentative", "Rejected"]:
        features = [f for f in feature_ranking if f["status"] == status]
        if features:
            fig.add_trace(go.Bar(
                name=status,
                x=[f["feature"] for f in features],
                y=[f["importance"] for f in features],
                marker_color=colors[status],
                hovertemplate="<b>%{x}</b><br>" +
                            "Importance: %{y:.3f}<br>" +
                            f"Status: {status}<extra></extra>"
            ))

    fig.update_layout(
        title=title,
        xaxis_title="Features",
        yaxis_title="Importance Score",
        barmode='group',
        height=500,
        xaxis={'tickangle': 45},
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )

    return fig


def create_selection_summary_table(selected_features: List[str],
                                 features_by_category: Dict[str, Dict[str, Any]],
                                 feature_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary table for selected features.

    Args:
        selected_features: List of features selected for removal
        features_by_category: Dictionary categorizing features
        feature_scores: DataFrame with feature importance scores

    Returns:
        DataFrame with summary information
    """
    summary_data = []
    for feat in selected_features:
        categories = []
        for category, info in features_by_category.items():
            if feat in info["features"]:
                categories.append(f"{info['icon']} {category}")

        # Get feature importance if available
        importance = None
        if len(feature_scores) > 0:
            matching_scores = feature_scores[feature_scores['feature'] == feat]['importance']
            if len(matching_scores) > 0:
                importance = matching_scores.values[0]

        summary_data.append({
            "Feature": feat,
            "Categories": " ".join(categories),
            "Importance": f"{importance:.3f}" if importance is not None else "N/A"
        })

    return pd.DataFrame(summary_data)


def get_feature_importance_stats(feature_scores: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate feature importance statistics for display.

    Args:
        feature_scores: DataFrame with feature importance scores

    Returns:
        Dictionary with importance statistics
    """
    if len(feature_scores) == 0:
        return {
            "total_features": 0,
            "high_importance": 0,
            "medium_importance": 0,
            "low_importance": 0,
            "mean_importance": 0,
            "median_importance": 0
        }

    return {
        "total_features": len(feature_scores),
        "high_importance": len(feature_scores[feature_scores['importance'] > 0.1]),
        "medium_importance": len(feature_scores[
            (feature_scores['importance'] <= 0.1) &
            (feature_scores['importance'] > 0.05)
        ]),
        "low_importance": len(feature_scores[feature_scores['importance'] <= 0.05]),
        "mean_importance": feature_scores['importance'].mean(),
        "median_importance": feature_scores['importance'].median()
    }


def create_dataset_metrics_display(builder) -> Dict[str, Any]:
    """
    Create metrics for current dataset display.

    Args:
        builder: Builder instance containing the dataset

    Returns:
        Dictionary with dataset metrics
    """
    curr_features = len(builder.X_train.columns)

    numerical_features = len(builder.X_train.select_dtypes(
        include=['int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    ).columns)

    categorical_features = len(builder.X_train.select_dtypes(
        exclude=['int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    ).columns)

    return {
        "total_features": curr_features,
        "numerical_features": numerical_features,
        "categorical_features": categorical_features,
        "numerical_percentage": (numerical_features/curr_features)*100 if curr_features > 0 else 0,
        "categorical_percentage": (categorical_features/curr_features)*100 if curr_features > 0 else 0
    }
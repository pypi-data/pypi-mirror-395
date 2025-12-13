"""
SHAP Visualization Utilities

This module contains visualization utilities for SHAP explanations including
force plots, waterfall charts, radar charts, and custom JSON encoding.

Extracted from what_if_analysis.py to improve code organization and reusability.
"""

import json
import numpy as np
import pandas as pd
import shap
import streamlit as st
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional


def create_force_plot(explainer_expected_value: float, shap_values: np.ndarray, feature_names: List[str]) -> go.Figure:
    """Create and cache force plot for SHAP values."""
    # Ensure we have single-sample SHAP values (1D array)
    if isinstance(shap_values, np.ndarray) and shap_values.ndim > 1:
        shap_values = shap_values.flatten() if shap_values.shape[0] == 1 else shap_values[0]
    
    # Validate dimensions match
    if len(shap_values) != len(feature_names):
        # Try to fix by truncating or padding
        if len(shap_values) > len(feature_names):
            shap_values = shap_values[:len(feature_names)]
        elif len(shap_values) < len(feature_names):
            feature_names = feature_names[:len(shap_values)]
    
    try:
        # Try new SHAP v0.20+ API first
        try:
            force_plot = shap.plots.force(
                explainer_expected_value,
                shap_values,
                feature_names=feature_names,
                matplotlib=True,
                show=False
            )
        except (ValueError, TypeError) as e:
            if "multiple samples" in str(e).lower() or "length of features" in str(e).lower():
                # If matplotlib fails due to multiple samples or dimension mismatch, use matplotlib=False
                force_plot = shap.plots.force(
                    explainer_expected_value,
                    shap_values,
                    feature_names=feature_names,
                    matplotlib=False,
                    show=False
                )
            else:
                raise e
    except AttributeError:
        # Fallback to old API for older SHAP versions
        try:
            force_plot = shap.force_plot(
                explainer_expected_value,
                shap_values,
                feature_names=feature_names,
                matplotlib=True,
                show=False
            )
        except (ValueError, TypeError) as e:
            if "multiple samples" in str(e).lower() or "length of features" in str(e).lower():
                # If matplotlib fails due to multiple samples or dimension mismatch, use matplotlib=False
                force_plot = shap.force_plot(
                    explainer_expected_value,
                    shap_values,
                    feature_names=feature_names,
                    matplotlib=False,
                    show=False
                )
            else:
                raise e
    return force_plot


@st.cache_data
def create_waterfall_chart(feature_importance: pd.DataFrame, selected_feature: str, 
                          baseline: float, hybrid: float, target: float) -> go.Figure:
    """Create and cache waterfall chart for feature importance visualization."""
    direction_color = 'rgba(50, 171, 96, 0.7)' if hybrid > baseline else 'rgba(219, 64, 82, 0.7)'
    feature_impact = hybrid - baseline
    
    scenarios = [f"Baseline", f"Only {selected_feature}<br>changed", "Final"]
    values = [baseline, hybrid, target]
    colors = ['rgba(55, 128, 191, 0.7)', direction_color, 'rgba(219, 64, 82, 0.7)']
    
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=scenarios,
        y=values,
        marker_color=colors,
        text=[f"{x:.4f}" for x in values],
        textposition='auto'
    ))
    
    # Add connecting line
    fig.add_trace(go.Scatter(
        x=scenarios,
        y=values,
        mode='lines',
        line=dict(color='black', width=1, dash='dot'),
        showlegend=False
    ))
    
    # Add annotations
    annotations = [
        dict(
            x=0,
            y=baseline,
            text=f"Baseline<br>{baseline:.4f}",
            showarrow=False,
            font=dict(color="black"),
            align="center",
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
            opacity=0.8
        ),
        dict(
            x=1,
            y=hybrid,
            text=f"Impact of {selected_feature}<br>{feature_impact:+.4f}",
            showarrow=True,
            arrowhead=3,
            arrowcolor=direction_color,
            arrowwidth=2,
            arrowsize=1,
            font=dict(color="black"),
            align="center",
            bgcolor="white",
            bordercolor=direction_color,
            borderwidth=1,
            borderpad=4,
            opacity=0.8
        ),
        dict(
            x=2,
            y=target,
            text=f"Final<br>{target:.4f}",
            showarrow=False,
            font=dict(color="black"),
            align="center",
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
            opacity=0.8
        )
    ]
    
    fig.update_layout(
        title=f"Impact of changing only '{selected_feature}'",
        xaxis_title="Scenarios",
        yaxis_title="Prediction Value",
        height=500,
        annotations=annotations,
        hovermode="x"
    )
    
    return fig


@st.cache_data
def create_radar_chart(features: List[str], normalized_importance: np.ndarray) -> go.Figure:
    """Create and cache radar chart for feature importance visualization."""
    radar_features = features.copy()
    radar_features.append(radar_features[0])
    radar_data = np.append(normalized_importance, normalized_importance[0])
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=radar_data,
        theta=radar_features,
        fill='toself',
        name="Feature Importance",
        line_color='rgba(50, 171, 96, 0.7)',
        fillcolor='rgba(50, 171, 96, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                title="Importance"
            )
        ),
        title="Feature Importance in Prediction Difference",
        height=500,
        showlegend=True
    )
    
    return fig


def create_shap_summary_plot(shap_values: np.ndarray, feature_data: np.ndarray, feature_names: List[str], problem_type: str = "classification"):
    """Create and cache SHAP summary plot.
    
    Args:
        shap_values: SHAP values array (n_samples, n_features)
        feature_data: Feature values array (n_samples, n_features)
        feature_names: List of feature names
        problem_type: Type of ML problem (classification, regression)
    
    Returns:
        Matplotlib figure object
    """
    import matplotlib.pyplot as plt
    
    # Close any existing plots
    plt.close('all')
    
    # Create a new figure for the summary plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create SHAP summary plot
    # This is a beeswarm/dot plot showing feature values and their impacts
    shap.summary_plot(
        shap_values, 
        feature_data,
        feature_names=feature_names,
        show=False,
        plot_type="dot"
    )
    
    # Get the current figure (shap.summary_plot creates its own)
    summary_fig = plt.gcf()
    
    # Add problem type to title for clarity
    if problem_type in ["binary_classification", "multiclass_classification", "classification"]:
        title_suffix = " (Classification)"
    else:
        title_suffix = " (Regression)"
    
    current_title = summary_fig.axes[0].get_title()
    if not current_title:
        summary_fig.axes[0].set_title(f"SHAP Summary Plot{title_suffix}")
    else:
        summary_fig.axes[0].set_title(f"{current_title}{title_suffix}")
    
    plt.tight_layout()
    
    return summary_fig


def create_interactive_shap_summary_plot(
    shap_values: np.ndarray, 
    feature_data: np.ndarray, 
    feature_names: List[str], 
    problem_type: str = "classification",
    max_display: int = 20,
    selected_features: Optional[List[str]] = None
) -> go.Figure:
    """Create an interactive Plotly version of SHAP summary plot with rich tooltips.
    
    Args:
        shap_values: SHAP values array (n_samples, n_features)
        feature_data: Feature values array (n_samples, n_features)
        feature_names: List of feature names
        problem_type: Type of ML problem (classification, regression)
        max_display: Maximum number of features to display
        selected_features: List of specific features to show (if None, show top features)
    
    Returns:
        Plotly figure object with interactive features
    """
    
    # Calculate mean absolute SHAP values for each feature to determine importance
    feature_importance = np.abs(shap_values).mean(axis=0)
    
    # Get indices of top features by importance
    if selected_features:
        # Filter to only selected features
        feature_indices = [i for i, name in enumerate(feature_names) if name in selected_features]
    else:
        # Get top N features by importance
        feature_indices = np.argsort(feature_importance)[-max_display:][::-1]
    
    # Create figure
    fig = go.Figure()
    
    # Normalize feature values for color mapping (0 to 1)
    # We'll do this per feature to handle different scales
    
    # Add traces for each feature (from top to bottom)
    y_position = len(feature_indices) - 1  # Start from top
    
    for idx, feat_idx in enumerate(feature_indices):
        feature_name = feature_names[feat_idx]
        
        # Get SHAP values and feature values for this feature
        feat_shap = shap_values[:, feat_idx]
        feat_values = feature_data[:, feat_idx]
        
        # Normalize feature values for color (0 to 1)
        feat_min, feat_max = feat_values.min(), feat_values.max()
        if feat_max > feat_min:
            feat_normalized = (feat_values - feat_min) / (feat_max - feat_min)
        else:
            feat_normalized = np.ones_like(feat_values) * 0.5
        
        # Add jitter to y-position for beeswarm effect
        np.random.seed(42 + feat_idx)  # Consistent jitter
        y_jitter = np.random.uniform(-0.3, 0.3, len(feat_shap))
        y_positions = np.full(len(feat_shap), y_position) + y_jitter
        
        # Create hover text with detailed information
        hover_texts = []
        for i, (shap_val, feat_val) in enumerate(zip(feat_shap, feat_values)):
            impact = "increases" if shap_val > 0 else "decreases"
            if problem_type == "regression":
                impact_text = f"{impact} prediction"
            else:
                impact_text = f"{impact} probability"
            
            # Format feature value
            if isinstance(feat_val, (int, np.integer)):
                feat_val_str = f"{feat_val}"
            else:
                feat_val_str = f"{feat_val:.4f}"
            
            hover_text = (
                f"<b>{feature_name}</b><br>"
                f"Feature Value: {feat_val_str}<br>"
                f"SHAP Value: {shap_val:.4f}<br>"
                f"Impact: {impact_text}<br>"
                f"Sample: {i}<br>"
                f"<br>"
                f"<i>Higher SHAP = stronger positive impact</i>"
            )
            hover_texts.append(hover_text)
        
        # Add scatter trace for this feature
        fig.add_trace(go.Scatter(
            x=feat_shap,
            y=y_positions,
            mode='markers',
            name=feature_name,
            marker=dict(
                size=8,
                color=feat_normalized,
                colorscale='RdBu_r',  # Red (high) to Blue (low)
                cmin=0,
                cmax=1,
                line=dict(width=0.5, color='rgba(0,0,0,0.3)'),
                opacity=0.8
            ),
            text=hover_texts,
            hovertemplate='%{text}<extra></extra>',
            showlegend=False
        ))
        
        y_position -= 1  # Move down for next feature
    
    # Update layout
    title_suffix = " (Classification)" if problem_type in ["binary_classification", "multiclass_classification", "classification"] else " (Regression)"
    
    fig.update_layout(
        title={
            'text': f"Interactive SHAP Summary Plot{title_suffix}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        xaxis=dict(
            title='SHAP Value (Impact on Model Output)',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='rgba(0,0,0,0.3)',
            gridcolor='rgba(200,200,200,0.2)',
            showgrid=True
        ),
        yaxis=dict(
            title='',
            tickmode='array',
            tickvals=list(range(len(feature_indices))),
            ticktext=[feature_names[feat_idx] for feat_idx in feature_indices[::-1]],  # Reversed for display
            gridcolor='rgba(200,200,200,0.2)',
            showgrid=True
        ),
        height=max(500, len(feature_indices) * 30),
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=200, r=50, t=80, b=50),
        font=dict(size=11)
    )
    
    # Add a colorbar to show feature value scale
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(
            colorscale='RdBu_r',
            showscale=True,
            cmin=0,
            cmax=1,
            colorbar=dict(
                title="Feature<br>Value",
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Low', 'High'],
                len=0.5,
                yanchor='middle',
                y=0.5
            )
        ),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add annotations
    fig.add_annotation(
        text="← Decreases Prediction | Increases Prediction →",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.08,
        showarrow=False,
        font=dict(size=11, color='gray'),
        xanchor='center'
    )
    
    return fig


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling numpy and special types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bool):
            return str(obj)
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

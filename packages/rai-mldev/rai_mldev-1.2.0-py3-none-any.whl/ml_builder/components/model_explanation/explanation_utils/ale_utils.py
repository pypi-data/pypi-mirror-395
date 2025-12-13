"""
Accumulated Local Effects (ALE) Utilities

This module contains utilities for generating Accumulated Local Effects plots
for model interpretation and feature effect analysis.

Extracted from Builder.py to improve code organization and reusability.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import traceback
from typing import Optional, Dict, Any


def generate_ale(model_dict: Dict[str, Any],
                X_train: pd.DataFrame,
                X_test: pd.DataFrame,
                feature_name: str,
                num_bins: int = 50,
                sample_size: int = 5000) -> Optional[go.Figure]:
    """
    Generate Accumulated Local Effects Plot for a feature with optimizations for large datasets.

    Args:
        model_dict: Dictionary containing model information
        X_train: Training features
        X_test: Test features
        feature_name: Name of the feature to analyze
        num_bins: Number of bins to use for continuous features
        sample_size: Maximum number of samples to use for calculation

    Returns:
        Plotly Figure object or None if generation fails
    """
    try:
        print(f"\nDiagnostic info for feature: {feature_name}")
        print(f"Model type: {type(model_dict['model']).__name__}")

        # Check if model exists and has predict method
        if not model_dict or not hasattr(model_dict["model"], "predict"):
            print("Error: Model not properly initialized or missing predict method")
            return None

        # Check if feature exists in both training and test data
        if feature_name not in X_train.columns:
            print(f"Error: Feature '{feature_name}' not found in training data")
            print(f"Available training features: {list(X_train.columns)}")
            return None
        if feature_name not in X_test.columns:
            print(f"Error: Feature '{feature_name}' not found in test data")
            print(f"Available test features: {list(X_test.columns)}")
            return None

        # Print data info
        print(f"Training data shape: {X_train.shape}")
        print(f"Test data shape: {X_test.shape}")

        # Combine train and test data for better distribution representation
        X_combined = pd.concat([X_train, X_test])
        print(f"Combined data shape: {X_combined.shape}")

        # Validate parameters
        dataset_size = len(X_combined)
        sample_size = min(sample_size, dataset_size)
        num_bins = min(num_bins, dataset_size // 10)
        print(f"Dataset size: {dataset_size}, Sample size: {sample_size}, Num bins: {num_bins}")

        # Sample data if needed
        X_sample = _sample_data_for_ale(X_combined, model_dict, sample_size)
        print(f"Final sample shape: {X_sample.shape}")

        # Get feature values and create bins
        feature_values = _prepare_feature_values(X_sample, feature_name, num_bins)
        if feature_values is None:
            return None

        # Calculate ALE values
        ale_values = _calculate_ale_values(model_dict["model"], X_sample, feature_name, feature_values)
        if ale_values is None:
            return None

        # Create visualization
        return _create_ale_visualization(feature_values, ale_values, X_sample, feature_name, sample_size)

    except Exception as e:
        print(f"Error generating ALE plot: {str(e)}")
        traceback.print_exc()
        return None


def _sample_data_for_ale(X_combined: pd.DataFrame, model_dict: Dict, sample_size: int) -> pd.DataFrame:
    """Sample data for ALE calculation, using stratified sampling for classification if possible."""
    dataset_size = len(X_combined)

    if dataset_size <= sample_size:
        return X_combined

    try:
        # Use stratified sampling if target is categorical
        if hasattr(model_dict["model"], "classes_"):
            print("Using stratified sampling for classification problem")
            # This would require target data, so fallback to random sampling
            print("Falling back to random sampling as target data not available")
            sample_indices = np.random.choice(dataset_size, sample_size, replace=False)
        else:
            print("Using random sampling for regression problem")
            sample_indices = np.random.choice(dataset_size, sample_size, replace=False)
        return X_combined.iloc[sample_indices]
    except Exception as e:
        print(f"Error during sampling: {str(e)}")
        print("Falling back to using full dataset")
        return X_combined


def _prepare_feature_values(X_sample: pd.DataFrame, feature_name: str, num_bins: int) -> Optional[np.ndarray]:
    """Prepare feature values for ALE calculation by creating appropriate bins."""
    # Get feature values and handle different data types
    feature_values = X_sample[feature_name].sort_values().unique()
    print(f"Number of unique values for {feature_name}: {len(feature_values)}")
    print(f"Feature value range: [{feature_values[0]}, {feature_values[-1]}]")

    if len(feature_values) < 2:
        print(f"Error: Not enough unique values in feature {feature_name}")
        return None

    # For continuous features, create bins
    if len(feature_values) > num_bins:
        print(f"Creating {num_bins} bins for continuous feature")
        bins = np.percentile(feature_values, np.linspace(0, 100, num_bins))
        feature_values = np.unique(bins)
        print(f"Number of unique bin edges: {len(feature_values)}")

    # Ensure we have enough bins
    if len(feature_values) < 2:
        print(f"Error: Not enough distinct values after binning for feature {feature_name}")
        return None

    return feature_values


def _calculate_ale_values(model, X_sample: pd.DataFrame, feature_name: str, feature_values: np.ndarray) -> Optional[np.ndarray]:
    """Calculate ALE values using vectorized computation."""
    # Vectorized ALE calculation with progress tracking
    ale_values = []
    X_lower = X_sample.copy()
    X_upper = X_sample.copy()

    print("Starting ALE calculation...")
    for i in range(len(feature_values) - 1):
        try:
            # Update feature values for all samples at once
            X_lower[feature_name] = feature_values[i]
            X_upper[feature_name] = feature_values[i + 1]

            # Batch predictions
            with np.errstate(divide='ignore', invalid='ignore'):
                preds_lower = model.predict(X_lower)
                preds_upper = model.predict(X_upper)
                local_effect = np.nanmean(preds_upper - preds_lower)
                ale_values.append(local_effect)

                if i % 10 == 0:  # Print progress every 10 bins
                    print(f"Processed {i+1}/{len(feature_values)-1} intervals")
        except Exception as e:
            print(f"Error in prediction at bin {i}")
            print(f"Lower value: {feature_values[i]}, Upper value: {feature_values[i+1]}")
            print(f"Error details: {str(e)}")
            traceback.print_exc()
            return None

    print("ALE calculation completed")
    print(f"Number of ALE values: {len(ale_values)}")

    # Accumulate effects
    ale_values = np.cumsum([0] + ale_values)

    # Center the effects around zero
    ale_values = ale_values - np.nanmean(ale_values)
    print(f"ALE value range: [{min(ale_values):.4f}, {max(ale_values):.4f}]")

    return ale_values


def _create_ale_visualization(feature_values: np.ndarray, ale_values: np.ndarray,
                            X_sample: pd.DataFrame, feature_name: str, sample_size: int) -> go.Figure:
    """Create ALE plot visualization using Plotly."""
    try:
        print("Creating visualization...")
        fig = go.Figure()

        # Add ALE line
        fig.add_trace(go.Scatter(
            x=feature_values,
            y=ale_values,
            mode='lines',
            name='Local Effect',
            line=dict(color='rgb(44, 160, 44)', width=2)
        ))

        # Add distribution markers
        y_min = min(ale_values)
        y_range = max(ale_values) - y_min
        rug_height = y_range * 0.03

        fig.add_trace(go.Scatter(
            x=X_sample[feature_name],
            y=[y_min - rug_height] * len(X_sample),
            mode='markers',
            name='Data Distribution',
            marker=dict(
                color='rgba(0,0,0,0.1)',
                symbol='line-ns',
                size=12,
                line=dict(width=0.5)
            ),
            hoverinfo='skip'
        ))

        # Add zero line
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="gray",
            annotation_text="No Effect"
        )

        # Update layout
        fig.update_layout(
            title={
                'text': f'Accumulated Local Effects for {feature_name}<br><sup>{sample_size:,} samples, {len(feature_values)} bins</sup>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis_title=feature_name,
            yaxis_title='Change in Prediction',
            hovermode='x unified',
            showlegend=True,
            # Move sample size info to a more visible annotation
            annotations=[
                dict(
                    text=f"Sample size: {sample_size:,}<br>Bins: {len(feature_values)}",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=1,
                    y=1,
                    align="right",
                    font={'size': 12}
                )
            ]
        )

        # Update y-axis range
        fig.update_yaxes(range=[y_min - 2*rug_height, max(ale_values) * 1.05])

        print("Visualization created successfully")
        return fig

    except Exception as e:
        print(f"Error creating visualization: {str(e)}")
        traceback.print_exc()
        return None


def generate_ale_for_multiple_features(model_dict: Dict[str, Any],
                                     X_train: pd.DataFrame,
                                     X_test: pd.DataFrame,
                                     features: list,
                                     num_bins: int = 50,
                                     sample_size: int = 5000) -> Dict[str, go.Figure]:
    """
    Generate ALE plots for multiple features.

    Args:
        model_dict: Dictionary containing model information
        X_train: Training features
        X_test: Test features
        features: List of feature names to analyze
        num_bins: Number of bins to use for continuous features
        sample_size: Maximum number of samples to use for calculation

    Returns:
        Dictionary mapping feature names to ALE plots
    """
    ale_plots = {}

    for feature in features:
        print(f"\nGenerating ALE plot for feature: {feature}")
        ale_plot = generate_ale(model_dict, X_train, X_test, feature, num_bins, sample_size)
        if ale_plot is not None:
            ale_plots[feature] = ale_plot
        else:
            print(f"Failed to generate ALE plot for feature: {feature}")

    return ale_plots


def analyze_ale_effects(ale_values: np.ndarray, feature_values: np.ndarray, feature_name: str) -> Dict[str, Any]:
    """
    Analyze ALE effects to provide insights about feature behavior.

    Args:
        ale_values: Array of ALE values
        feature_values: Array of feature values
        feature_name: Name of the feature

    Returns:
        Dictionary containing analysis results
    """
    try:
        # Calculate basic statistics
        max_effect = np.max(ale_values)
        min_effect = np.min(ale_values)
        effect_range = max_effect - min_effect

        # Find points of maximum effect
        max_idx = np.argmax(ale_values)
        min_idx = np.argmin(ale_values)

        # Calculate monotonicity
        differences = np.diff(ale_values)
        monotonic_increasing = np.all(differences >= 0)
        monotonic_decreasing = np.all(differences <= 0)

        # Calculate effect strength
        effect_strength = effect_range / (np.std(ale_values) + 1e-8)  # Avoid division by zero

        analysis = {
            "feature_name": feature_name,
            "effect_range": float(effect_range),
            "max_effect": float(max_effect),
            "min_effect": float(min_effect),
            "max_effect_at": float(feature_values[max_idx]),
            "min_effect_at": float(feature_values[min_idx]),
            "monotonic_increasing": bool(monotonic_increasing),
            "monotonic_decreasing": bool(monotonic_decreasing),
            "effect_strength": float(effect_strength),
            "interpretation": _interpret_ale_effects(effect_range, monotonic_increasing, monotonic_decreasing, effect_strength)
        }

        return analysis

    except Exception as e:
        return {
            "feature_name": feature_name,
            "error": f"Error analyzing ALE effects: {str(e)}"
        }


def _interpret_ale_effects(effect_range: float, monotonic_increasing: bool,
                         monotonic_decreasing: bool, effect_strength: float) -> str:
    """Generate interpretation of ALE effects."""
    if effect_range < 0.01:
        return "Feature has minimal effect on predictions"

    if monotonic_increasing:
        return "Feature has a consistently positive effect (monotonic increasing)"
    elif monotonic_decreasing:
        return "Feature has a consistently negative effect (monotonic decreasing)"
    elif effect_strength > 2.0:
        return "Feature has strong non-linear effects on predictions"
    elif effect_strength > 1.0:
        return "Feature has moderate non-linear effects on predictions"
    else:
        return "Feature has weak effects on predictions"


def compare_ale_plots(ale_results: Dict[str, go.Figure],
                     feature_importance: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Compare ALE plots across multiple features to identify patterns.

    Args:
        ale_results: Dictionary mapping feature names to ALE plots
        feature_importance: Optional dictionary of feature importance scores

    Returns:
        Dictionary containing comparison analysis
    """
    if not ale_results:
        return {"error": "No ALE results provided"}

    comparison = {
        "total_features": len(ale_results),
        "features_analyzed": list(ale_results.keys()),
        "summary": {}
    }

    # If feature importance is provided, correlate with ALE effects
    if feature_importance:
        importance_correlation = {}
        for feature in ale_results.keys():
            if feature in feature_importance:
                importance_correlation[feature] = feature_importance[feature]

        comparison["importance_correlation"] = importance_correlation

    return comparison
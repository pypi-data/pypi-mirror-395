"""
Visualization utilities for ML model evaluation.

This module contains pure visualization functions that generate Plotly figures
for machine learning model evaluation, separated from Streamlit-specific logic.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Optional, Tuple, Union, Any


@st.cache_data(show_spinner=False)
def create_precision_recall_curve(_y_test, _y_prob):
    """Create precision-recall curve with AUC score."""
    from sklearn.metrics import precision_recall_curve, average_precision_score

    # Assign to local variables (underscore prefix prevents hashing issues)
    y_test, y_prob = _y_test, _y_prob

    precision, recall, thresholds = precision_recall_curve(y_test, y_prob)
    avg_precision = average_precision_score(y_test, y_prob)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=recall, 
        y=precision, 
        name=f'PR Curve (AP = {avg_precision:.3f})',
        line=dict(color='blue', width=2)
    ))
    
    # Add baseline (random classifier)
    positive_ratio = y_test.mean()
    fig.add_trace(go.Scatter(
        x=[0, 1], 
        y=[positive_ratio, positive_ratio], 
        name=f'Random Baseline ({positive_ratio:.3f})',
        line=dict(dash='dash', color='red')
    ))
    
    fig.update_layout(
        title='Precision-Recall Curve',
        xaxis_title='Recall (Sensitivity)',
        yaxis_title='Precision',
        showlegend=True,
        height=400
    )
    
    return fig


@st.cache_data(show_spinner=False)
def create_multiclass_probability_distribution_plot(_y_test, _y_prob_matrix):
    """Show distribution of prediction probabilities for multiclass classification."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Assign to local variables (underscore prefix prevents hashing issues)
    y_test, y_prob_matrix = _y_test, _y_prob_matrix
    
    # Get unique classes and create class names
    unique_classes = sorted(list(set(y_test)))
    class_names = [str(cls) for cls in unique_classes]
    n_classes = len(unique_classes)
    
    # Create a cleaner approach: show confidence distribution by actual class
    # This is more interpretable than overlapping histograms
    
    # Get max probabilities (confidence) and predicted classes
    max_probs = np.max(y_prob_matrix, axis=1)
    predicted_classes = np.argmax(y_prob_matrix, axis=1)
    
    # Create subplot structure - one subplot per actual class
    n_cols = min(3, n_classes)
    n_rows = (n_classes + n_cols - 1) // n_cols
    
    subplot_titles = [f'Confidence Distribution for True Class {cls}' for cls in class_names]
    fig = make_subplots(
        rows=n_rows, 
        cols=n_cols,
        subplot_titles=subplot_titles,
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    # Color palette - use intuitive colors
    green_color = '#28a745'  # Green for correct predictions
    red_color = '#dc3545'  # Red for incorrect predictions
    
    # For each actual class, show confidence distribution split by correctness
    for class_idx, actual_class in enumerate(unique_classes):
        row = (class_idx // n_cols) + 1
        col = (class_idx % n_cols) + 1
        
        # Get samples for this actual class
        class_mask = y_test == actual_class
        if np.sum(class_mask) == 0:
            continue
            
        class_max_probs = max_probs[class_mask]
        class_predicted = predicted_classes[class_mask]
        
        # Split into correct and incorrect predictions
        # For this actual class, correct means predicted class matches actual class
        correct_mask = class_predicted == actual_class
        incorrect_mask = class_predicted != actual_class
        
        # Add histogram for correct predictions
        if np.sum(correct_mask) > 0:
            fig.add_trace(
                go.Histogram(
                    x=class_max_probs[correct_mask],
                    name='Correct Predictions',
                    marker_color=green_color,
                    opacity=0.7,
                    nbinsx=20,
                    legendgroup='correct',
                    showlegend=(class_idx == 0),
                    hovertemplate='<b>Correct Predictions</b><br>' +
                                 f'True Class: {actual_class}<br>' +
                                 'Confidence: %{x:.3f}<br>' +
                                 'Count: %{y}<br>' +
                                 '<extra></extra>'
                ),
                row=row, col=col
            )
        
        # Add histogram for incorrect predictions
        if np.sum(incorrect_mask) > 0:
            fig.add_trace(
                go.Histogram(
                    x=class_max_probs[incorrect_mask],
                    name='Incorrect Predictions',
                    marker_color=red_color,
                    opacity=0.7,
                    nbinsx=20,
                    legendgroup='incorrect',
                    showlegend=(class_idx == 0),
                    hovertemplate='<b>Incorrect Predictions</b><br>' +
                                 f'True Class: {actual_class}<br>' +
                                 'Confidence: %{x:.3f}<br>' +
                                 'Count: %{y}<br>' +
                                 '<extra></extra>'
                ),
                row=row, col=col
            )
        
        # Update subplot axes
        fig.update_xaxes(title_text="Model Confidence", row=row, col=col, range=[0, 1])
        fig.update_yaxes(title_text="Count", row=row, col=col)
        
        # Add accuracy text annotation
        accuracy = np.sum(correct_mask) / len(class_mask) if len(class_mask) > 0 else 0
        
        # Calculate correct axis reference for subplot
        subplot_number = (row - 1) * n_cols + col
        if subplot_number == 1:
            xref, yref = "x domain", "y domain"
        else:
            xref, yref = f"x{subplot_number} domain", f"y{subplot_number} domain"
        
        fig.add_annotation(
            x=0.98, y=0.95,
            xref=xref, yref=yref,
            text=f"Accuracy: {accuracy:.1%}",
            showarrow=False,
            font=dict(size=10, color="black"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1
        )
    
    # Update main layout
    fig.update_layout(
        title='Model Confidence Distribution by True Class',
        height=max(400, 280 * n_rows),
        barmode='overlay',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,  # Higher up to prevent overlap with subplot titles
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=80)  # Add top margin to accommodate legend
    )
    
    return fig


@st.cache_data(show_spinner=False)
def create_probability_distribution_plot(_y_test, _y_prob, optimal_threshold: Optional[float] = None,
                                        has_optimal_threshold: bool = False):
    """Show distribution of prediction probabilities by class.

    Args:
        _y_test: True labels (underscore prevents hashing)
        _y_prob: Predicted probabilities (underscore prevents hashing)
        optimal_threshold: Optional optimal threshold value
        has_optimal_threshold: Whether to show optimal threshold line
    """
    # Assign to local variables (underscore prefix prevents hashing issues)
    y_test, y_prob = _y_test, _y_prob

    prob_df = pd.DataFrame({
        'Probability': y_prob,
        'Actual_Class': y_test.astype(str)
    })
    
    fig = px.histogram(
        prob_df,
        x='Probability',
        color='Actual_Class',
        barmode='overlay',
        opacity=0.7,
        nbins=30,
        title='Distribution of Prediction Probabilities by Actual Class',
        labels={'Actual_Class': 'Actual Class'},
        color_discrete_map={'0': 'blue', '1': 'red'}  # Explicit color mapping: blue for class 0, red for class 1
    )
    
    # Add default threshold line
    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="gray",
        annotation_text="Default Threshold (0.5)",
        annotation_position="top"
    )
    
    # Add optimal threshold line if different from default
    if has_optimal_threshold and optimal_threshold is not None:
        fig.add_vline(
            x=optimal_threshold,
            line_dash="solid",
            line_color="red",
            annotation_text=f"Optimal Threshold ({optimal_threshold:.3f})",
            annotation_position="bottom"
        )
        
        # Update title to reflect optimization
        fig.update_layout(
            title='Distribution of Prediction Probabilities by Actual Class (with Optimal Threshold)'
        )
    
    fig.update_layout(height=400)
    
    return fig


@st.cache_data(show_spinner=False)
def create_classification_error_by_confidence_plot(_y_test, _y_pred, _y_prob):
    """Show how classification errors vary by prediction confidence with calibration analysis."""
    try:
        from sklearn.calibration import calibration_curve
        from sklearn.isotonic import IsotonicRegression

        # Assign to local variables (underscore prefix prevents hashing issues)
        y_test, y_pred, y_prob = _y_test, _y_pred, _y_prob

        # Calculate prediction confidence and correctness
        # Detect binary vs multiclass based on the number of classes, not array shape
        is_binary = len(np.unique(y_test)) == 2
        
        if is_binary:
            # Binary classification - extract positive class probability and calculate confidence
            if len(y_prob.shape) == 1:
                # Already just the positive class probability
                prob_positive = y_prob
            else:
                # Full probability matrix - extract positive class probability
                prob_positive = y_prob[:, 1]
            
            confidence = np.maximum(prob_positive, 1 - prob_positive)
        else:
            # Multi-class - confidence is the maximum probability
            confidence = np.max(y_prob, axis=1)
            # For multi-class, use probability of predicted class
            predicted_class_idx = np.argmax(y_prob, axis=1)
            prob_positive = y_prob[np.arange(len(y_prob)), predicted_class_idx]
        
        is_correct = (y_test == y_pred).astype(int)
        
        # Create confidence bins for the main plot
        n_bins = min(10, len(np.unique(confidence)))
        if n_bins < 2:
            return None, None
            
        confidence_bins = pd.qcut(confidence, n_bins, duplicates='drop')
        
        error_df = pd.DataFrame({
            'Confidence': confidence,
            'Confidence_Bin': confidence_bins.astype(str),
            'Is_Correct': is_correct,
            'Error_Rate': 1 - is_correct
        })
        
        # Calculate error rate by confidence bin
        bin_stats = error_df.groupby('Confidence_Bin').agg({
            'Error_Rate': ['mean', 'count'],
            'Confidence': 'mean'
        }).round(3)
        
        bin_stats.columns = ['Error_Rate', 'Sample_Count', 'Avg_Confidence']
        bin_stats = bin_stats.reset_index()
        
        # Create the main plot with bars
        fig = go.Figure()
        
        # Add the bar chart using average confidence values for x-axis
        fig.add_trace(go.Bar(
            x=bin_stats['Avg_Confidence'],
            y=bin_stats['Error_Rate'],
            name='Error Rate',
            marker_color='lightblue',
            width=0.05,  # Narrower bars since we're using continuous x-axis
            hovertemplate='<b>Confidence Range</b>: %{customdata[2]}<br>' +
                         '<b>Error Rate</b>: %{y:.3f}<br>' +
                         '<b>Avg Confidence</b>: %{x:.3f}<br>' +
                         '<b>Sample Count</b>: %{customdata[1]}<br>' +
                         '<extra></extra>',
            customdata=list(zip(bin_stats['Avg_Confidence'], bin_stats['Sample_Count'], bin_stats['Confidence_Bin']))
        ))

        # Add trend line using polynomial fit with actual confidence values
        if len(bin_stats) >= 3:
            try:
                # Use actual average confidence values for polynomial fitting
                x_confidence = bin_stats['Avg_Confidence'].values
                y_values = bin_stats['Error_Rate'].values

                # Use linear fit for small datasets to avoid overfitting
                poly_degree = 1 if len(x_confidence) <= 4 else min(2, len(x_confidence) - 1)
                z = np.polyfit(x_confidence, y_values, poly_degree)
                p = np.poly1d(z)

                # Generate smooth trend line across the confidence range
                x_smooth = np.linspace(x_confidence.min(), x_confidence.max(), 100)
                trend_y_values = p(x_smooth)

                # Constrain trend line values to valid error rate range [0, 1]
                trend_y_values = np.clip(trend_y_values, 0.0, 1.0)

                fig.add_trace(go.Scatter(
                    x=x_smooth,
                    y=trend_y_values,
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', width=3),
                    hovertemplate='<b>Trend</b><br>' +
                                 'Confidence: %{x:.3f}<br>' +
                                 'Error Rate: %{y:.3f}<br>' +
                                 '<extra></extra>'
                ))
            except:
                pass  # Skip trend line if fitting fails
        
        # Calculate calibration metrics for both binary and multiclass classification
        calibration_info = None
        calibration_error_message = None
        
        try:
            if is_binary:  # Binary classification
                try:
                    # Calculate calibration curve
                    fraction_of_positives, mean_predicted_value = calibration_curve(
                        y_test, prob_positive, n_bins=min(10, len(np.unique(prob_positive)))
                    )
                    
                    # Calculate Brier score (lower is better)
                    brier_score = np.mean((prob_positive - y_test) ** 2)
                    
                    # Calculate Expected Calibration Error (ECE)
                    bin_boundaries = np.linspace(0, 1, 11)
                    bin_lowers = bin_boundaries[:-1]
                    bin_uppers = bin_boundaries[1:]
                    
                    ece = 0
                    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
                        in_bin = (prob_positive > bin_lower) & (prob_positive <= bin_upper)
                        prop_in_bin = in_bin.mean()
                        
                        if prop_in_bin > 0 and np.sum(in_bin) > 0:
                            accuracy_in_bin = y_test[in_bin].mean()
                            avg_confidence_in_bin = prob_positive[in_bin].mean()
                            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
                    
                    calibration_info = {
                        'brier_score': brier_score,
                        'ece': ece,
                        'fraction_of_positives': fraction_of_positives,
                        'mean_predicted_value': mean_predicted_value,
                        'is_binary': True
                    }
                except Exception as e:
                    calibration_error_message = f"Binary calibration metrics failed: {str(e)}"
                    
            else:  # Multiclass classification
                try:
                    # Ensure y_prob is the full probability matrix
                    if len(y_prob.shape) == 1:
                        # If y_prob is 1D (max probabilities), we need the full matrix
                        # This should have been passed as the full matrix, but let's handle this case
                        calibration_error_message = "Full probability matrix not available for multiclass calibration"
                    else:
                        # Create one-hot encoded true labels for multiclass Brier score
                        from sklearn.preprocessing import LabelBinarizer
                        lb = LabelBinarizer()
                        y_true_onehot = lb.fit_transform(y_test)
                        
                        # Handle case where LabelBinarizer might return 1D array for 2 classes
                        if len(y_true_onehot.shape) == 1:
                            # Convert to 2D array for 2-class case
                            y_true_onehot = np.column_stack([1 - y_true_onehot, y_true_onehot])
                        
                        # Ensure dimensions match
                        if y_true_onehot.shape[1] != y_prob.shape[1]:
                            calibration_error_message = f"Dimension mismatch: y_true_onehot has {y_true_onehot.shape[1]} classes, y_prob has {y_prob.shape[1]} classes"
                        else:
                            # Multiclass Brier score: mean squared difference between predicted probs and one-hot true labels
                            brier_score = np.mean(np.sum((y_prob - y_true_onehot) ** 2, axis=1))
                            
                            # Multiclass Expected Calibration Error (ECE)
                            # Use max probability and check if predicted class matches true class
                            max_probs = np.max(y_prob, axis=1)
                            predicted_classes = np.argmax(y_prob, axis=1)
                            
                            # Convert y_test to numeric if it's not already and handle class mapping
                            correct_predictions = None
                            try:
                                # Handle different input types for y_test
                                if hasattr(y_test, 'dtype'):  # pandas Series or numpy array
                                    if hasattr(y_test, 'iloc'):  # pandas Series
                                        if y_test.dtype == 'object' or isinstance(y_test.iloc[0], str):
                                            # Handle string/object labels - need to create mapping
                                            unique_labels = sorted(y_test.unique())
                                            label_to_int = {label: i for i, label in enumerate(unique_labels)}
                                            y_test_numeric = y_test.map(label_to_int)
                                        else:
                                            y_test_numeric = y_test
                                    else:  # numpy array
                                        if y_test.dtype == 'object' or (len(y_test) > 0 and isinstance(y_test[0], str)):
                                            # Handle string/object labels
                                            unique_labels = sorted(np.unique(y_test))
                                            label_to_int = {label: i for i, label in enumerate(unique_labels)}
                                            y_test_numeric = np.array([label_to_int[label] for label in y_test])
                                        else:
                                            y_test_numeric = y_test
                                else:
                                    y_test_numeric = np.array(y_test)
                                
                                # Get unique classes in order
                                unique_classes = np.unique(y_test_numeric)
                                n_unique_classes = len(unique_classes)
                                
                                if n_unique_classes != y_prob.shape[1]:
                                    calibration_error_message = f"Class count mismatch: {n_unique_classes} unique classes in y_test, {y_prob.shape[1]} classes in predictions"
                                else:
                                    # Map predicted class indices to actual class labels if needed
                                    if not np.array_equal(unique_classes, np.arange(n_unique_classes)):
                                        # Classes are not 0, 1, 2, ... - need to map
                                        class_mapping = {i: cls for i, cls in enumerate(sorted(unique_classes))}
                                        predicted_classes_mapped = np.array([class_mapping.get(pred, pred) for pred in predicted_classes])
                                        correct_predictions = (predicted_classes_mapped == y_test_numeric).astype(int)
                                    else:
                                        correct_predictions = (predicted_classes == y_test_numeric).astype(int)
                            except Exception as class_mapping_error:
                                calibration_error_message = f"Class mapping failed: {str(class_mapping_error)}"
                            
                            # Calculate ECE with error handling - moved outside exception handler
                            if correct_predictions is not None and calibration_error_message is None:
                                try:
                                    bin_boundaries = np.linspace(0, 1, 11)
                                    bin_lowers = bin_boundaries[:-1]
                                    bin_uppers = bin_boundaries[1:]
                                    
                                    ece = 0
                                    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
                                        in_bin = (max_probs > bin_lower) & (max_probs <= bin_upper)
                                        prop_in_bin = in_bin.mean()
                                        
                                        if prop_in_bin > 0 and np.sum(in_bin) > 0:
                                            accuracy_in_bin = correct_predictions[in_bin].mean()
                                            avg_confidence_in_bin = max_probs[in_bin].mean()
                                            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
                                    
                                    calibration_info = {
                                        'brier_score': brier_score,
                                        'ece': ece,
                                        'is_binary': False
                                    }
                                except Exception as ece_error:
                                    calibration_error_message = f"ECE calculation failed: {str(ece_error)}"
                            else:
                                if calibration_error_message is None:
                                    calibration_error_message = "Could not calculate correct predictions for ECE"
                except Exception as e:
                    calibration_error_message = f"Multiclass calibration metrics failed: {str(e)}"
                    
        except Exception as e:
            calibration_error_message = f"Calibration metrics calculation failed: {str(e)}"
        
        # Add error message to calibration_info if metrics failed
        if calibration_error_message:
            calibration_info = {
                'error': calibration_error_message,
                'is_binary': is_binary
            }
        
        # Update layout
        fig.update_layout(
            title='Error Rate by Prediction Confidence',
            xaxis_title='Prediction Confidence (0 = Low → 1 = High)',
            yaxis_title='Error Rate',
            height=400,
            showlegend=True,
            legend=dict(x=0.02, y=0.98),
            hovermode='closest'
        )

        # Set x-axis range dynamically based on actual data, with small padding
        x_min = max(0, bin_stats['Avg_Confidence'].min() - 0.05)  # 5% padding below minimum
        x_max = min(1, bin_stats['Avg_Confidence'].max() + 0.05)  # 5% padding above maximum

        # Ensure we have a reasonable range (at least 0.2 wide)
        range_width = x_max - x_min
        if range_width < 0.2:
            center = (x_min + x_max) / 2
            x_min = max(0, center - 0.1)
            x_max = min(1, center + 0.1)

        fig.update_xaxes(
            range=[x_min, x_max],
            tickformat='.2f'
        )
        
        return fig, calibration_info
        
    except Exception as e:
        print(f"Error creating confidence error plot: {e}")
        return None, None


@st.cache_data(show_spinner=False)
def create_classification_confusion_by_features_plot(_y_test, _y_pred, _X_test, _model=None):
    """Show confusion patterns across different feature ranges with multi-feature analysis."""
    try:
        # Assign to local variables (underscore prefix prevents hashing issues)
        y_test, y_pred, X_test, model = _y_test, _y_pred, _X_test, _model

        numeric_cols = X_test.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return None
            
        # Try to get feature importance to prioritize features
        features_to_analyze = list(numeric_cols[:6])  # Default: first 6 features
        
        if model is not None:
            try:
                # Get feature importance if available
                importance = None
                if hasattr(model, 'feature_importances_'):
                    importance = model.feature_importances_
                elif hasattr(model, 'coef_'):
                    importance = np.abs(model.coef_).flatten()
                
                if importance is not None and len(importance) == len(X_test.columns):
                    # Create importance DataFrame
                    importance_df = pd.DataFrame({
                        'feature': X_test.columns,
                        'importance': importance
                    })
                    
                    # Filter for numeric columns and sort by importance
                    numeric_importance = importance_df[importance_df['feature'].isin(numeric_cols)]
                    numeric_importance = numeric_importance.sort_values('importance', ascending=False)
                    
                    # Use top 6 most important numeric features
                    features_to_analyze = list(numeric_importance['feature'][:6])
            except:
                pass  # Fall back to default selection
        
        # Calculate errors
        is_correct = (y_test == y_pred).astype(int)
        error_rate = 1 - is_correct
        
        # Create subplots for multiple features
        n_features = len(features_to_analyze)
        n_cols = min(3, n_features)
        n_rows = (n_features + n_cols - 1) // n_cols
        
        fig = make_subplots(
            rows=n_rows, 
            cols=n_cols,
            subplot_titles=[f'Error Rate by {feat}' for feat in features_to_analyze],
            vertical_spacing=0.4,
            horizontal_spacing=0.1
        )
        
        for idx, feature_col in enumerate(features_to_analyze):
            row = (idx // n_cols) + 1
            col = (idx % n_cols) + 1
            
            feature_values = X_test[feature_col]
            
            # Create bins for this feature
            n_bins = min(6, len(np.unique(feature_values)))
            if n_bins < 2:
                continue
                
            try:
                feature_bins = pd.qcut(feature_values, n_bins, duplicates='drop')
            except:
                feature_bins = pd.cut(feature_values, n_bins)
            
            # Calculate error rate by bin
            bin_df = pd.DataFrame({
                'Feature_Bin': feature_bins.astype(str),
                'Error_Rate': error_rate
            })
            
            bin_stats = bin_df.groupby('Feature_Bin')['Error_Rate'].agg(['mean', 'count']).reset_index()
            bin_stats.columns = ['Feature_Bin', 'Error_Rate', 'Sample_Count']
            
            # Add to subplot
            fig.add_trace(
                go.Bar(
                    x=bin_stats['Feature_Bin'],
                    y=bin_stats['Error_Rate'],
                    name=feature_col,
                    showlegend=False,
                    hovertemplate=f'<b>{feature_col}</b><br>' +
                                'Range: %{x}<br>' +
                                'Error Rate: %{y:.3f}<br>' +
                                'Samples: %{customdata}<br>' +
                                '<extra></extra>',
                    customdata=bin_stats['Sample_Count']
                ),
                row=row, col=col
            )
        
        # Update layout
        fig.update_layout(
            height=300 * n_rows,
            title_text="Error Patterns Across Feature Ranges",
            title_x=0.5,
            showlegend=False
        )
        
        # Update all subplot axes
        fig.update_xaxes(title_text="Feature Range", tickangle=45)
        fig.update_yaxes(title_text="Error Rate")
        
        return fig
        
    except Exception as e:
        print(f"Error creating multi-feature confusion plot: {e}")
        return None


def has_feature_importance_support(model):
    """Check if model supports feature importance, including calibrated models."""
    # Check direct model support
    if (hasattr(model, 'feature_importances_') or 
        hasattr(model, 'coef_') or 
        hasattr(model, 'feature_importances')):
        return True
    
    # Check if it's a calibrated model with underlying support
    if hasattr(model, 'base_estimator') or hasattr(model, 'estimator'):
        # sklearn CalibratedClassifierCV uses base_estimator (older) or estimator (newer)
        base_model = getattr(model, 'base_estimator', None) or getattr(model, 'estimator', None)
        if base_model is not None:
            return (hasattr(base_model, 'feature_importances_') or 
                   hasattr(base_model, 'coef_') or 
                   hasattr(base_model, 'feature_importances'))
    
    # Check if it's a calibrated model with calibrated_classifiers_ attribute
    if hasattr(model, 'calibrated_classifiers_'):
        # Multiple calibrated classifiers - check the first one
        try:
            if len(model.calibrated_classifiers_) > 0:
                first_calibrated = model.calibrated_classifiers_[0]
                if hasattr(first_calibrated, 'base_estimator') or hasattr(first_calibrated, 'estimator'):
                    base_model = getattr(first_calibrated, 'base_estimator', None) or getattr(first_calibrated, 'estimator', None)
                    if base_model is not None:
                        return (hasattr(base_model, 'feature_importances_') or 
                               hasattr(base_model, 'coef_') or 
                               hasattr(base_model, 'feature_importances'))
        except:
            pass
    
    return False


def get_feature_importance_from_model(model):
    """Extract feature importance from model, including calibrated models."""
    # Direct model check
    if hasattr(model, 'feature_importances_'):
        return model.feature_importances_, "Tree-based Model Importance (Gini/MSE)"
    elif hasattr(model, 'coef_'):
        if len(model.coef_.shape) == 1:
            return np.abs(model.coef_), "Linear Model Importance (|Coefficients|)"
        else:
            return np.mean(np.abs(model.coef_), axis=0), "Linear Model Importance (|Coefficients|)"
    elif hasattr(model, 'feature_importances'):
        return model.feature_importances, "Feature Importance"
    
    # Check calibrated models
    base_model = None
    
    # Try different ways to access the base estimator
    if hasattr(model, 'base_estimator'):
        base_model = model.base_estimator
    elif hasattr(model, 'estimator'):
        base_model = model.estimator
    elif hasattr(model, 'calibrated_classifiers_'):
        try:
            if len(model.calibrated_classifiers_) > 0:
                first_calibrated = model.calibrated_classifiers_[0]
                if hasattr(first_calibrated, 'base_estimator'):
                    base_model = first_calibrated.base_estimator
                elif hasattr(first_calibrated, 'estimator'):
                    base_model = first_calibrated.estimator
        except:
            pass
    
    if base_model is not None:
        if hasattr(base_model, 'feature_importances_'):
            return base_model.feature_importances_, "Tree-based Model Importance (Gini/MSE) [from calibrated model]"
        elif hasattr(base_model, 'coef_'):
            if len(base_model.coef_.shape) == 1:
                return np.abs(base_model.coef_), "Linear Model Importance (|Coefficients|) [from calibrated model]"
            else:
                return np.mean(np.abs(base_model.coef_), axis=0), "Linear Model Importance (|Coefficients|) [from calibrated model]"
        elif hasattr(base_model, 'feature_importances'):
            return base_model.feature_importances, "Feature Importance [from calibrated model]"
    
    return None, None


@st.cache_data(show_spinner=False)
def create_pure_feature_importance_plot(_model, _feature_names):
    """Create feature importance plot without session state dependencies."""
    try:
        # Assign to local variables (underscore prefix prevents hashing issues)
        model, feature_names = _model, _feature_names

        # Get feature importance values and display type
        importance_values, display_type = get_feature_importance_from_model(model)
        
        if importance_values is None:
            return None
        
        if importance_values is None or len(importance_values) == 0:
            return None
            
        # Ensure we have the right number of feature names
        if len(feature_names) != len(importance_values):
            feature_names = [f"Feature_{i}" for i in range(len(importance_values))]
        
        # Create DataFrame and sort by importance
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance_values
        }).sort_values('Importance', ascending=True)

        # Take top 20 features to avoid cluttered plots
        if len(importance_df) > 20:
            importance_df = importance_df.tail(20)
            
        # Create the plot
        fig = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            title=f'Feature Importance ({display_type})',
            labels={'Importance': f'{display_type}', 'Feature': 'Features'}
        )
        
        # Update layout for better readability
        fig.update_layout(
            height=max(500, len(importance_df) * 25),
            xaxis_title=display_type,
            yaxis_title='Features',
            showlegend=False
        )
        
        # Add value labels on bars for better readability
        fig.update_traces(
            texttemplate='%{x:.3f}',
            textposition='outside'
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating feature importance plot: {e}")
        return None


@st.cache_data(show_spinner=False)
def create_error_by_prediction_range_plot(_y_test, _y_pred):
    """Show how errors vary across prediction ranges."""
    try:
        # Assign to local variables (underscore prefix prevents hashing issues)
        y_test, y_pred = _y_test, _y_pred

        # Create prediction bins
        n_bins = min(10, len(np.unique(y_pred)))
        if n_bins < 2:
            return None
            
        pred_bins = pd.qcut(y_pred, n_bins, duplicates='drop')
        
        error_df = pd.DataFrame({
            'Actual': y_test,
            'Predicted': y_pred,
            'Error': y_test - y_pred,
            'Abs_Error': np.abs(y_test - y_pred),
            'Prediction_Range': pred_bins.astype(str)
        })
        
        # Box plot of absolute errors by prediction range
        fig = px.box(
            error_df,
            x='Prediction_Range',
            y='Abs_Error',
            title='Absolute Error Distribution by Prediction Range'
        )
        
        fig.update_xaxes(title='Prediction Range')
        fig.update_yaxes(title='Absolute Error')
        fig.update_layout(height=400)
        
        return fig
    except:
        return None


@st.cache_data(show_spinner=False)
def create_cooks_distance_plot(_y_test, _y_pred, _X_test):
    """Create simplified Cook's distance plot to identify influential points."""
    try:
        # Assign to local variables (underscore prefix prevents hashing issues)
        y_test, y_pred, X_test = _y_test, _y_pred, _X_test

        residuals = y_test - y_pred
        
        # Simplified influence measure based on residuals and predictions
        # This is an approximation since true Cook's distance requires more complex calculations
        standardized_residuals = np.abs(residuals) / np.std(residuals)
        prediction_leverage = np.abs(y_pred - np.mean(y_pred)) / np.std(y_pred)
        
        # Combine residual magnitude with prediction extremeness
        influence_score = standardized_residuals * (1 + prediction_leverage)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.arange(len(influence_score)),
            y=influence_score,
            mode='markers',
            name="Influence Score",
            marker=dict(
                color=influence_score,
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Influence Score")
            ),
            text=[f"Residual: {r:.3f}<br>Pred: {p:.3f}" for r, p in zip(residuals, y_pred)],
            hovertemplate="Index: %{x}<br>Influence: %{y:.3f}<br>%{text}<extra></extra>"
        ))
        
        # Add threshold line (points above this might be influential)
        threshold = np.mean(influence_score) + 2 * np.std(influence_score)
        fig.add_hline(
            y=threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"High Influence Threshold ({threshold:.2f})"
        )
        
        fig.update_layout(
            title="Influential Points Analysis",
            xaxis_title='Sample Index',
            yaxis_title="Influence Score",
            height=400
        )
        
        return fig
    except Exception as e:
        print(f"Error creating influence plot: {e}")
        return None


@st.cache_data(show_spinner=False)
def create_prediction_intervals_plot(_model, _X_test, _y_test, _y_pred):
    """Create prediction intervals if model supports it."""
    try:
        # Assign to local variables (underscore prefix prevents hashing issues)
        model, X_test, y_test, y_pred = _model, _X_test, _y_test, _y_pred

        predictions = None
        
        # Check for different types of ensemble models
        if hasattr(model, 'estimators_') and hasattr(model.estimators_, '__len__'):
            # Traditional sklearn ensemble models (Random Forest, Extra Trees, sklearn Gradient Boosting)
            estimators = model.estimators_
            if len(estimators) > 1:
                # Limit the number of estimators for performance
                max_estimators = min(50, len(estimators))
                selected_estimators = estimators[:max_estimators]
                
                try:
                    # For different ensemble types, access estimators differently
                    if hasattr(selected_estimators[0], 'predict'):
                        # Direct estimator predictions (Random Forest, Extra Trees)
                        predictions = np.array([est.predict(X_test) for est in selected_estimators])
                    elif hasattr(model, 'staged_predict'):
                        # sklearn Gradient Boosting models
                        staged_preds = list(model.staged_predict(X_test))
                        if len(staged_preds) > max_estimators:
                            step = len(staged_preds) // max_estimators
                            staged_preds = staged_preds[::step]
                        predictions = np.array(staged_preds)
                    else:
                        return None
                except Exception as e:
                    print(f"Error accessing estimator predictions: {e}")
                    return None
        
        elif hasattr(model, 'get_booster'):
            # XGBoost models - use multiple predictions with different random states
            try:
                # For XGBoost, we can get prediction intervals by using different subsamples
                # or by training multiple models with different random seeds (simulated here)
                n_predictions = 20  # PERFORMANCE: Reduced from 50 to 20
                xgb_predictions = []
                
                # Try to get feature importance to add some variation
                if hasattr(model, 'feature_importances_'):
                    # Use feature dropout simulation for variation
                    feature_weights = model.feature_importances_
                    
                    # Create variations by slightly modifying the input
                    for i in range(n_predictions):
                        # Add small random noise based on feature importance
                        noise_scale = 0.01  # Very small noise
                        noise = np.random.normal(0, noise_scale, X_test.shape)
                        # Weight noise by feature importance (normalized)
                        if len(feature_weights) == X_test.shape[1]:
                            noise = noise * (feature_weights / np.max(feature_weights))
                        
                        X_modified = X_test + noise
                        pred_variant = model.predict(X_modified)
                        xgb_predictions.append(pred_variant)
                    
                    predictions = np.array(xgb_predictions)
                else:
                    # Fallback: create variations using bootstrap-like approach
                    n_samples = len(X_test)
                    for i in range(n_predictions):
                        # Random sample with replacement
                        idx = np.random.choice(n_samples, size=n_samples, replace=True)
                        X_bootstrap = X_test.iloc[idx] if hasattr(X_test, 'iloc') else X_test[idx]
                        pred_variant = model.predict(X_bootstrap)
                        
                        # Map back to original order
                        pred_full = np.zeros(n_samples)
                        for orig_idx, boot_idx in enumerate(idx):
                            pred_full[boot_idx] = pred_variant[orig_idx]
                        
                        xgb_predictions.append(pred_full)
                    
                    predictions = np.array(xgb_predictions)
                    
            except Exception as e:
                print(f"Error creating XGBoost prediction intervals: {e}")
                return None
        
        elif hasattr(model, 'booster_'):
            # LightGBM models - similar approach to XGBoost
            try:
                n_predictions = 20  # PERFORMANCE: Reduced from 50 to 20
                lgb_predictions = []
                
                # Create variations by adding small noise or using bootstrap sampling
                for i in range(n_predictions):
                    # Add small random noise
                    noise_scale = 0.01
                    noise = np.random.normal(0, noise_scale, X_test.shape)
                    X_modified = X_test + noise
                    pred_variant = model.predict(X_modified)
                    lgb_predictions.append(pred_variant)
                
                predictions = np.array(lgb_predictions)
                    
            except Exception as e:
                print(f"Error creating LightGBM prediction intervals: {e}")
                return None
        
        elif hasattr(model, 'staged_predict'):
            # Some gradient boosting models without direct estimators_ access
            try:
                staged_preds = list(model.staged_predict(X_test))
                max_stages = min(50, len(staged_preds))
                if len(staged_preds) > max_stages:
                    step = len(staged_preds) // max_stages
                    staged_preds = staged_preds[::step]
                predictions = np.array(staged_preds)
            except Exception as e:
                print(f"Error accessing staged predictions: {e}")
                return None
        
        else:
            # Check by model class name for other boosting models
            model_class_name = model.__class__.__name__.lower()
            boosting_models = ['catboost', 'gbm', 'gradient', 'adaboost']
            
            if any(boosting_name in model_class_name for boosting_name in boosting_models):
                try:
                    # Generic approach for other boosting models
                    n_predictions = 20  # PERFORMANCE: Reduced from 50 to 20
                    boost_predictions = []
                    
                    for i in range(n_predictions):
                        # Add small random noise to create variations
                        noise_scale = 0.01
                        noise = np.random.normal(0, noise_scale, X_test.shape)
                        X_modified = X_test + noise
                        pred_variant = model.predict(X_modified)
                        boost_predictions.append(pred_variant)
                    
                    predictions = np.array(boost_predictions)
                    
                except Exception as e:
                    print(f"Error creating boosting model prediction intervals: {e}")
                    return None
            else:
                return None
        
        if predictions is None or len(predictions) == 0:
            return None
        
        # Calculate prediction intervals
        lower_bound = np.percentile(predictions, 5, axis=0)
        upper_bound = np.percentile(predictions, 95, axis=0)
        
        # Sort by actual values for cleaner visualization
        if hasattr(y_test, 'values'):
            y_test_values = y_test.values
        else:
            y_test_values = y_test
            
        sort_idx = np.argsort(y_test_values)
        
        # Limit points for performance
        max_points = 200
        if len(sort_idx) > max_points:
            step = len(sort_idx) // max_points
            sort_idx = sort_idx[::step]
        
        fig = go.Figure()
        
        # Add prediction intervals
        fig.add_trace(go.Scatter(
            x=np.arange(len(sort_idx)),
            y=upper_bound[sort_idx],
            fill=None,
            mode='lines',
            line_color='rgba(0,100,80,0)',
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=np.arange(len(sort_idx)),
            y=lower_bound[sort_idx],
            fill='tonexty',
            mode='lines',
            line_color='rgba(0,100,80,0)',
            name='90% Prediction Interval',
            fillcolor='rgba(0,100,80,0.2)'
        ))
        
        # Add actual and predicted values
        y_test_sorted = y_test_values[sort_idx]
        fig.add_trace(go.Scatter(
            x=np.arange(len(sort_idx)),
            y=y_test_sorted,
            mode='markers',
            name='Actual',
            marker=dict(color='red', size=4)
        ))
        
        fig.add_trace(go.Scatter(
            x=np.arange(len(sort_idx)),
            y=y_pred[sort_idx],
            mode='markers',
            name='Predicted',
            marker=dict(color='blue', size=4)
        ))
        
        fig.update_layout(
            title='Predictions with Confidence Intervals',
            xaxis_title='Sample Index (sorted by actual value)',
            yaxis_title='Target Value',
            height=400
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating prediction intervals: {e}")
        return None


def can_provide_confidence_intervals(model):
    """Check if model can provide confidence intervals through ensemble methods."""
    # Traditional sklearn ensemble models
    if hasattr(model, 'estimators_') and hasattr(model.estimators_, '__len__'):
        return True
    
    # XGBoost models
    if hasattr(model, 'get_booster'):
        return True
    
    # LightGBM models
    if hasattr(model, 'booster_'):
        return True
    
    # Models with staged_predict (some gradient boosting implementations)
    if hasattr(model, 'staged_predict'):
        return True
    
    # Check by model class name for additional boosting models
    model_class_name = model.__class__.__name__.lower()
    boosting_models = ['xgb', 'lightgbm', 'catboost', 'gbm', 'gradient', 'adaboost']
    if any(boosting_name in model_class_name for boosting_name in boosting_models):
        return True
    
    return False


def highlight_high_influence(row, residuals):
    """Style function for highlighting high influence points in dataframes."""
    colors = []
    for col in row.index:
        if col == 'Influence_Score':
            colors.append('background-color: #ffcccc')  # Light red for high influence
        elif col == 'Residual':
            abs_residual = abs(float(row[col]))
            if abs_residual > 2 * np.std(residuals):
                colors.append('background-color: #fff2cc')  # Light yellow for high residual
            else:
                colors.append('')
        else:
            colors.append('')
    return colors


@st.cache_data(show_spinner=False)
def create_confusion_matrix(_y_test, _y_pred, _class_names, optimal_threshold=None, threshold_info=None):
    """Create confusion matrix visualization."""
    from sklearn.metrics import confusion_matrix

    # Assign to local variables (underscore prefix prevents hashing issues)
    y_test, y_pred, class_names = _y_test, _y_pred, _class_names

    cm = confusion_matrix(y_test, y_pred)

    # Create confusion matrix
    confusion_fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=class_names,
        y=class_names,
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 16},
        hoverongaps=False,
        colorscale='Blues',
        showscale=True
    ))

    # Update confusion matrix title based on threshold optimization
    cm_title = 'Confusion Matrix'
    if threshold_info and threshold_info.get("threshold_optimized", False):
        optimal_threshold = threshold_info.get("optimal_threshold", 0.5)
        is_binary = threshold_info.get("threshold_is_binary", True)
        if is_binary:
            cm_title = f'Confusion Matrix (Optimal Threshold: {optimal_threshold:.3f})'
        else:
            cm_title = f'Confusion Matrix (Optimal Confidence: {optimal_threshold:.3f})'

    confusion_fig.update_layout(
        title=cm_title,
        xaxis_title='Predicted',
        yaxis_title='Actual',
        xaxis=dict(tickmode='array', ticktext=class_names, tickvals=list(range(len(class_names)))),
        yaxis=dict(tickmode='array', ticktext=class_names, tickvals=list(range(len(class_names))))
    )

    return confusion_fig


@st.cache_data(show_spinner=False)
def create_roc_curve(_y_test, _y_prob_matrix, _class_names):
    """Create ROC curve visualization for binary and multiclass classification."""
    from sklearn.metrics import roc_curve, auc, roc_auc_score

    # Assign to local variables (underscore prefix prevents hashing issues)
    y_test, y_prob_matrix, class_names = _y_test, _y_prob_matrix, _class_names

    if len(class_names) == 2:
        # Binary classification
        y_prob = y_prob_matrix[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        roc_fig = go.Figure()
        roc_fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f'ROC (AUC = {roc_auc:.3f})'))
        roc_fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name='Random', line=dict(dash='dash')))
        roc_fig.update_layout(
            title='ROC Curve',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate'
        )
    else:
        # Multiclass classification - use one-vs-rest ROC
        from sklearn.preprocessing import LabelBinarizer

        # Create one-vs-rest ROC curves
        roc_fig = go.Figure()

        # Calculate macro-average ROC AUC
        try:
            macro_auc = roc_auc_score(y_test, y_prob_matrix, multi_class='ovr', average='macro')
        except:
            macro_auc = 0.5

        # Plot ROC curve for each class
        for i, class_name in enumerate(class_names):
            # Create binary targets for this class vs all others
            y_binary = (y_test == class_name).astype(int)
            y_prob_class = y_prob_matrix[:, i]

            try:
                fpr, tpr, _ = roc_curve(y_binary, y_prob_class)
                class_auc = auc(fpr, tpr)

                roc_fig.add_trace(go.Scatter(
                    x=fpr, y=tpr,
                    name=f'Class {class_name} (AUC = {class_auc:.3f})',
                    mode='lines'
                ))
            except:
                pass

        # Add random classifier line
        roc_fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name='Random', line=dict(dash='dash')))
        roc_fig.update_layout(
            title=f'ROC Curves (Macro-avg AUC = {macro_auc:.3f})',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate'
        )

    return roc_fig


@st.cache_data(show_spinner=False)
def create_classification_learning_curve(_model_instance, _X_train, _y_train):
    """Create learning curve for classification."""
    from sklearn.model_selection import learning_curve

    # Assign to local variables (underscore prefix prevents hashing issues)
    model_instance, X_train, y_train = _model_instance, _X_train, _y_train

    train_sizes, train_scores, val_scores = learning_curve(
        model_instance, X_train, y_train,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5, scoring='accuracy'
    )

    learning_fig = go.Figure()
    learning_fig.add_trace(go.Scatter(
        x=train_sizes,
        y=train_scores.mean(axis=1),
        name='Training Score'
    ))
    learning_fig.add_trace(go.Scatter(
        x=train_sizes,
        y=val_scores.mean(axis=1),
        name='Cross-validation Score'
    ))
    learning_fig.update_layout(
        title='Learning Curve',
        xaxis_title='Training Examples',
        yaxis_title='Score'
    )

    return learning_fig


@st.cache_data(show_spinner=False)
def create_actual_vs_predicted_plot(_y_test, _y_pred):
    """Create actual vs predicted values plot for regression."""

    # Assign to local variables (underscore prefix prevents hashing issues)
    y_test, y_pred = _y_test, _y_pred

    plot_df = pd.DataFrame({
        'Actual': y_test,
        'Predicted': y_pred
    })

    pred_fig = go.Figure()
    pred_fig.add_trace(go.Scatter(
        x=plot_df['Actual'],
        y=plot_df['Predicted'],
        mode='markers',
        name='Predictions',
        marker=dict(size=8, opacity=0.6)
    ))

    # Perfect prediction line
    min_val = min(plot_df['Actual'].min(), plot_df['Predicted'].min())
    max_val = max(plot_df['Actual'].max(), plot_df['Predicted'].max())
    line_range = [min_val, max_val]

    pred_fig.add_trace(go.Scatter(
        x=line_range,
        y=line_range,
        name='Perfect Prediction',
        line=dict(dash='dash', color='red')
    ))

    pred_fig.update_layout(
        title='Actual vs Predicted Values',
        xaxis_title='Actual Values',
        yaxis_title='Predicted Values',
        showlegend=True
    )

    return pred_fig


@st.cache_data(show_spinner=False)
def create_residuals_analysis_plot(_y_test, _y_pred):
    """Create comprehensive residuals analysis plot for regression."""
    from scipy.stats import probplot
    from plotly.subplots import make_subplots

    # Assign to local variables (underscore prefix prevents hashing issues)
    y_test, y_pred = _y_test, _y_pred

    plot_df = pd.DataFrame({
        'Actual': y_test,
        'Predicted': y_pred
    })

    # Ensure residuals are calculated as actual minus predicted
    plot_df['Residuals'] = plot_df['Actual'] - plot_df['Predicted']
    plot_df['Sqrt_Abs_Residuals'] = np.sqrt(np.abs(plot_df['Residuals']))

    # Create subplots for residual analysis
    residuals_fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Residuals vs Predicted',
            'Residual Distribution',
            'Normal Q-Q Plot',
            'Scale-Location Plot'
        )
    )

    # 1. Residuals vs Predicted
    residuals_fig.add_trace(
        go.Scatter(
            x=plot_df['Predicted'],
            y=plot_df['Residuals'],
            mode='markers',
            name='Residuals',
            marker=dict(size=8, opacity=0.6)
        ),
        row=1, col=1
    )

    # Add zero line
    residuals_fig.add_hline(
        y=0, line_dash="dash",
        line_color="red",
        row=1, col=1
    )

    # 2. Residual Distribution
    residuals_fig.add_trace(
        go.Histogram(
            x=plot_df['Residuals'],
            name='Residuals Dist',
            nbinsx=30
        ),
        row=1, col=2
    )

    # 3. Q-Q Plot
    residuals = plot_df['Residuals'].values

    # Standardize residuals for Q-Q plot
    standardized_residuals = (residuals - residuals.mean()) / residuals.std()

    # Generate Q-Q plot data using standardized residuals
    qq = probplot(standardized_residuals, dist='norm', fit=True)
    theoretical_q = qq[0][0]
    sample_q = qq[0][1]

    # Create Q-Q plot
    residuals_fig.add_trace(
        go.Scatter(
            x=theoretical_q,
            y=sample_q,
            mode='markers',
            name='Q-Q Plot',
            marker=dict(
                size=8,
                opacity=0.6,
                color='blue'
            )
        ),
        row=2, col=1
    )

    # Add reference line
    line_min = min(theoretical_q.min(), sample_q.min())
    line_max = max(theoretical_q.max(), sample_q.max())

    residuals_fig.add_trace(
        go.Scatter(
            x=[line_min, line_max],
            y=[line_min, line_max],
            mode='lines',
            name='Reference Line',
            line=dict(
                color='red',
                dash='dash'
            ),
            showlegend=False
        ),
        row=2, col=1
    )

    # Update axes labels and title
    residuals_fig.update_xaxes(
        title_text="Theoretical Quantiles (Standard Normal)",
        row=2, col=1
    )
    residuals_fig.update_yaxes(
        title_text="Standardized Sample Quantiles",
        row=2, col=1
    )

    # Ensure proper ranges for Q-Q plot
    plot_range = [-4, 4]  # Standard range for normal distribution

    residuals_fig.update_xaxes(
        range=plot_range,
        row=2, col=1
    )
    residuals_fig.update_yaxes(
        range=plot_range,
        row=2, col=1
    )

    # 4. Scale-Location Plot
    residuals_fig.add_trace(
        go.Scatter(
            x=plot_df['Predicted'],
            y=plot_df['Sqrt_Abs_Residuals'],
            mode='markers',
            name='Scale-Location',
            marker=dict(size=8, opacity=0.6)
        ),
        row=2, col=2
    )

    # Update layout
    residuals_fig.update_layout(
        height=800,
        title_text="Residual Analysis Plots",
        showlegend=False,
        template='plotly_white'
    )

    # Update individual subplot layouts
    for i in range(1, 3):
        for j in range(1, 3):
            residuals_fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='Gray',
                row=i, col=j
            )
            residuals_fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='Gray',
                row=i, col=j
            )

    return residuals_fig


@st.cache_data(show_spinner=False)
def create_regression_learning_curve(_model_instance, _X_train, _y_train):
    """Create learning curve for regression."""
    from sklearn.model_selection import learning_curve

    # Assign to local variables (underscore prefix prevents hashing issues)
    model_instance, X_train, y_train = _model_instance, _X_train, _y_train

    train_sizes, train_scores, val_scores = learning_curve(
        model_instance, X_train, y_train,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5, scoring='r2'
    )

    learning_fig = go.Figure()
    learning_fig.add_trace(go.Scatter(
        x=train_sizes,
        y=train_scores.mean(axis=1),
        name='Training Score',
        line=dict(color='darkblue')
    ))
    learning_fig.add_trace(go.Scatter(
        x=train_sizes,
        y=val_scores.mean(axis=1),
        name='Cross-validation Score',
        line=dict(color='lightblue')
    ))
    learning_fig.update_layout(
        title='Learning Curve',
        xaxis_title='Training Examples',
        yaxis_title='R² Score',
        yaxis=dict(range=[-1, 1])  # Set y-axis range for R² scores
    )

    return learning_fig
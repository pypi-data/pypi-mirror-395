"""
Model Explanation Core Utilities

This module contains the core functionality for generating comprehensive model explanations
using SHAP values and other interpretability techniques.

Extracted from Builder.py to improve code organization and reusability.
"""

import shap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from typing import Dict, Any
from sklearn.calibration import CalibratedClassifierCV
from .shap_computation_utils import create_shap_explainer


def explain_model(model_dict: Dict[str, Any],
                 X_train: pd.DataFrame,
                 X_test: pd.DataFrame,
                 problem_type: str = None) -> Dict[str, Any]:
    """
    Generate comprehensive model explanations using SHAP values.

    Args:
        model_dict: Dictionary containing model information
        X_train: Training features
        X_test: Test features
        problem_type: Type of ML problem

    Returns:
        Dict containing explanation results and visualizations
    """
    print("\n=== Starting Model Explanation ===")

    if model_dict is None or not hasattr(model_dict["model"], "predict"):
        print("Error: Model is not available or does not have predict method")
        return {
            "success": False,
            "message": "No trained model available"
        }

    try:
        # Use session state problem type if available, otherwise fallback to model
        if problem_type is None:
            if hasattr(st, 'session_state') and hasattr(st.session_state, 'problem_type'):
                problem_type = st.session_state.problem_type
            else:
                problem_type = model_dict.get("problem_type", "unknown")

        print(f"Problem type: {problem_type}")

        if problem_type == "unknown":
            print("Error: Unknown problem type")
            return {
                "success": False,
                "message": "Unable to determine problem type"
            }

        # Process data for SHAP analysis
        feature_names, X_train_processed, X_test_processed = _prepare_data_for_shap(X_train, X_test)

        # Create background dataset and samples for explanation
        background_data, samples_to_explain = _create_sample_datasets(X_train_processed, X_test_processed)

        # Create SHAP explainer
        model_instance = model_dict["model"]
        model_type = model_dict.get("type", "unknown")

        explainer = _create_explainer(model_instance, model_type, problem_type, background_data, feature_names)

        if explainer is None:
            return {
                "success": False,
                "message": "Failed to create SHAP explainer"
            }

        # Calculate SHAP values
        shap_values = _calculate_shap_values(explainer, samples_to_explain, problem_type)

        if shap_values is None:
            return {
                "success": False,
                "message": "Failed to calculate SHAP values"
            }

        # Create visualization and calculate feature importance
        shap_plot, feature_importance_df = _create_shap_visualization(
            shap_values, feature_names, problem_type
        )

        print("\n=== Model Explanation Completed Successfully ===")

        return {
            "success": True,
            "message": "Model explanation generated successfully",
            "shap_values": {
                "plot": shap_plot,
                "feature_importance": feature_importance_df.to_dict('records'),
                "problem_type": problem_type,
                "raw_shap_values": shap_values,  # Raw SHAP values for summary plot
                "feature_data": samples_to_explain,  # Feature data for summary plot
                "feature_names": feature_names  # Feature names for summary plot
            }
        }

    except Exception as e:
        print(f"\nError in explain_model: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Traceback:")
        traceback.print_exc()
        plt.close()  # Clean up any open figures
        return {
            "success": False,
            "message": f"Error explaining model: {str(e)}. Try with a simpler model or fewer samples."
        }


def _prepare_data_for_shap(X_train: pd.DataFrame, X_test: pd.DataFrame) -> tuple:
    """Prepare data for SHAP analysis by converting boolean columns and extracting feature names."""
    print("\nPreparing data for SHAP analysis...")
    feature_names = list(X_train.columns)

    # Convert boolean columns to int
    X_train_processed = X_train.copy()
    X_test_processed = X_test.copy()

    for col in X_train.select_dtypes(include=['bool']).columns:
        X_train_processed[col] = X_train_processed[col].astype(int)
        X_test_processed[col] = X_test_processed[col].astype(int)

    print(f"- Training data shape: {X_train_processed.shape}")
    print(f"- Test data shape: {X_test_processed.shape}")

    return feature_names, X_train_processed, X_test_processed


def _create_sample_datasets(X_train_processed: pd.DataFrame, X_test_processed: pd.DataFrame) -> tuple:
    """Create background dataset and samples for SHAP explanation."""
    # Create a small background dataset for the explainer
    n_background = min(50, len(X_train_processed))
    background_indices = np.random.choice(len(X_train_processed), n_background, replace=False)
    background_data = X_train_processed.iloc[background_indices].values
    print(f"- Created background dataset with {n_background} samples")

    # Create a sample for explanation
    n_explain = min(50, len(X_test_processed))
    explain_indices = np.random.choice(len(X_test_processed), n_explain, replace=False)
    samples_to_explain = X_test_processed.iloc[explain_indices].values
    print(f"- Selected {n_explain} samples for explanation")

    return background_data, samples_to_explain


def _create_explainer(model_instance, model_type: str, problem_type: str, background_data, feature_names: list):
    """Create SHAP explainer based on model type and problem type."""
    print("\nCreating SHAP explainer...")
    print(f"- Model type: {model_type}")

    # Check if model is calibrated and extract underlying model for TreeExplainer
    is_calibrated = isinstance(model_instance, CalibratedClassifierCV)

    if is_calibrated:
        print("- Detected calibrated model")
        # Extract the underlying model for TreeExplainer
        try:
            # Try new API first (sklearn >= 1.2)
            if hasattr(model_instance, 'estimator'):
                underlying_model = model_instance.estimator
                print("- Extracted underlying model using 'estimator' attribute")
            # Fall back to old API (sklearn < 1.2)
            elif hasattr(model_instance, 'base_estimator'):
                underlying_model = model_instance.base_estimator
                print("- Extracted underlying model using 'base_estimator' attribute")
            else:
                # If we can't extract, we'll use the calibrated model with KernelExplainer
                underlying_model = None
                print("- Could not extract underlying model, will use KernelExplainer")
        except:
            underlying_model = None
            print("- Error extracting underlying model, will use KernelExplainer")
    else:
        underlying_model = model_instance

    # Create a prediction function wrapper that doesn't allow attribute setting
    def prediction_wrapper(predict_fn):
        def wrapped(x):
            return predict_fn(x)
        return wrapped

    # Special handling for tree-based models
    if ('xgboost' in model_type.lower() or 'lightgbm' in model_type.lower() or 'hist_gradient_boosting' in model_type.lower() or 'catboost' in model_type.lower()) and underlying_model is not None:
        print("- Using TreeExplainer for tree-based model")
        if problem_type == "multiclass_classification":
            print("- Multiclass tree model detected")
        try:
            explainer = shap.TreeExplainer(underlying_model)
            print("- TreeExplainer created successfully with underlying model")
            return explainer
        except Exception as e:
            print(f"- TreeExplainer failed: {str(e)}. Falling back to KernelExplainer")
            # Fall back to KernelExplainer
            return _create_kernel_explainer(model_instance, problem_type, background_data, feature_names, prediction_wrapper)
    else:
        print("- Using KernelExplainer")
        return _create_kernel_explainer(model_instance, problem_type, background_data, feature_names, prediction_wrapper)


def _create_kernel_explainer(model_instance, problem_type: str, background_data, feature_names: list, prediction_wrapper):
    """Create KernelExplainer for non-tree models or when TreeExplainer fails."""
    if problem_type in ["binary_classification", "multiclass_classification", "classification"]:
        if hasattr(model_instance, "predict_proba"):
            print(f"- Using predict_proba for {problem_type}")
            if problem_type == "binary_classification":
                predict_fn = lambda x: model_instance.predict_proba(x)[:, 1]
            elif problem_type == "multiclass_classification":
                # For multiclass, use all probabilities but focus on max for importance
                predict_fn = lambda x: model_instance.predict_proba(x)
            else:  # fallback for legacy "classification"
                predict_fn = lambda x: model_instance.predict_proba(x)[:, 1]

            explainer = shap.KernelExplainer(
                prediction_wrapper(predict_fn),
                background_data,
                feature_names=feature_names
            )
        else:
            print("- Using predict for classification")
            explainer = shap.KernelExplainer(
                prediction_wrapper(model_instance.predict),
                background_data,
                feature_names=feature_names
            )
    else:  # regression
        print("- Using predict for regression")
        explainer = shap.KernelExplainer(
            prediction_wrapper(model_instance.predict),
            background_data,
            feature_names=feature_names
        )

    return explainer


def _calculate_shap_values(explainer, samples_to_explain, problem_type: str):
    """Calculate SHAP values and handle different output formats."""
    print("\nCalculating SHAP values...")
    shap_values = explainer.shap_values(samples_to_explain)
    print("- SHAP values calculated successfully")

    # Handle different shapes of SHAP values for classification vs regression
    if problem_type in ["binary_classification", "multiclass_classification", "classification"] and isinstance(shap_values, list):
        print(f"- Processing {problem_type} SHAP values")
        if problem_type == "binary_classification":
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
        elif problem_type == "multiclass_classification":
            # For multiclass, SHAP values are typically a list of arrays, one per class
            # Each array has shape (samples, features)
            print(f"- Multiclass SHAP values type: {type(shap_values)}")
            print(f"- Number of classes: {len(shap_values)}")
            if len(shap_values) > 0:
                print(f"- Shape of first class SHAP values: {shap_values[0].shape}")

            # Convert list of arrays to 3D array (samples, features, classes)
            shap_3d = np.stack(shap_values, axis=2)
            print(f"- Stacked SHAP shape: {shap_3d.shape}")

            # Take mean absolute value across classes to get (samples, features)
            shap_values = np.mean(np.abs(shap_3d), axis=2)
            print(f"- Final SHAP shape after aggregation: {shap_values.shape}")
        else:  # fallback for legacy "classification"
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]

    # Additional check for multiclass when not a list (some models return 3D arrays directly)
    elif problem_type == "multiclass_classification" and hasattr(shap_values, 'shape') and len(shap_values.shape) == 3:
        print(f"- Processing 3D multiclass SHAP values with shape: {shap_values.shape}")
        # Take mean absolute value across classes (axis=2) to get (samples, features)
        shap_values = np.mean(np.abs(shap_values), axis=2)
        print(f"- Final SHAP shape after aggregation: {shap_values.shape}")

    return shap_values


def _create_shap_visualization(shap_values, feature_names: list, problem_type: str) -> tuple:
    """Create SHAP visualization and calculate feature importance."""
    print("\nCreating SHAP plot...")
    # Close any existing plots to avoid interference
    plt.close('all')

    # Validate SHAP values shape before calculating importance
    print(f"- Final SHAP values shape before importance calculation: {shap_values.shape}")
    if len(shap_values.shape) != 2:
        print(f"- Warning: Expected 2D SHAP values, got {len(shap_values.shape)}D")
        # Try to reshape to 2D if possible
        if len(shap_values.shape) == 3:
            print("- Attempting to fix by taking mean across last dimension")
            shap_values = np.mean(np.abs(shap_values), axis=2)
            print(f"- New shape: {shap_values.shape}")
        elif len(shap_values.shape) == 1:
            print("- Error: Cannot compute feature importance from 1D SHAP values")
            return None, None

    # Calculate feature importance from SHAP values
    shap_importance = np.abs(shap_values).mean(0)
    print(f"- Feature importance shape: {shap_importance.shape}")
    print(f"- Number of features: {len(feature_names)}")

    # Validate that importance and feature names match
    if len(shap_importance) != len(feature_names):
        print(f"- Error: Mismatch between importance ({len(shap_importance)}) and features ({len(feature_names)})")
        return None, None

    # Create a DataFrame for better handling
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': shap_importance
    }).sort_values('Importance', ascending=True)  # Ascending for horizontal bar chart

    # Limit to top 20 features if there are more
    if len(importance_df) > 20:
        importance_df = importance_df.tail(20)

    # Create a simple bar chart that will definitely display
    plt.figure(figsize=(10, 8))

    # Use a nice color palette and add grid for readability
    bars = plt.barh(importance_df['Feature'], importance_df['Importance'],
                   color=plt.cm.viridis(np.linspace(0.1, 0.9, len(importance_df))))

    plt.xlabel('Feature Importance (mean |SHAP value|)')
    plt.ylabel('Feature')

    title = 'Feature Importance Based on SHAP Values'
    if problem_type in ["binary_classification", "multiclass_classification", "classification"]:
        if problem_type == "binary_classification":
            title += ' (Binary Classification)'
        elif problem_type == "multiclass_classification":
            title += ' (Multiclass Classification)'
        else:
            title += ' (Classification)'
    else:
        title += ' (Regression)'

    plt.title(title)
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Add value labels to the end of each bar
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + bar.get_width()*0.01,
                bar.get_y() + bar.get_height()/2,
                f'{bar.get_width():.3f}',
                va='center')

    plt.tight_layout()

    # Ensure figure is properly rendered
    shap_plot = plt.gcf()
    print("- SHAP plot created successfully")

    # Calculate feature importance for return value
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': shap_importance
    }).sort_values('Importance', ascending=False)

    return shap_plot, feature_importance_df


def get_model_explanation_summary(explanation_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a summary of model explanation results.

    Args:
        explanation_result: Result from explain_model function

    Returns:
        Dict containing summarized explanation information
    """
    if not explanation_result.get("success", False):
        return {
            "success": False,
            "message": "No valid explanation results to summarize"
        }

    shap_data = explanation_result.get("shap_values", {})
    feature_importance = shap_data.get("feature_importance", [])

    if not feature_importance:
        return {
            "success": False,
            "message": "No feature importance data available"
        }

    # Calculate summary statistics
    importance_values = [item["Importance"] for item in feature_importance]

    summary = {
        "success": True,
        "total_features": len(feature_importance),
        "top_features": feature_importance[:5],  # Top 5 most important
        "importance_stats": {
            "max": max(importance_values),
            "min": min(importance_values),
            "mean": np.mean(importance_values),
            "std": np.std(importance_values)
        },
        "problem_type": shap_data.get("problem_type", "unknown"),
        "concentration_ratio": importance_values[0] / sum(importance_values) if importance_values else 0
    }

    # Add interpretation
    if summary["concentration_ratio"] > 0.5:
        summary["interpretation"] = "Model heavily depends on a single feature"
    elif summary["concentration_ratio"] > 0.3:
        summary["interpretation"] = "Model shows moderate feature concentration"
    else:
        summary["interpretation"] = "Model uses features relatively evenly"

    return summary
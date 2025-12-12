"""
Individual Prediction Explanation Utilities

This module contains utilities for explaining individual predictions using SHAP and LIME,
providing detailed insights into feature contributions for specific instances.

Extracted from Builder.py to improve code organization and reusability.
"""

import shap
import matplotlib.pyplot as plt
import lime
import lime.lime_tabular
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import streamlit as st
import re
from typing import Dict, Any
from sklearn.calibration import CalibratedClassifierCV


def explain_prediction(model_dict: Dict[str, Any],
                      X_train: pd.DataFrame,
                      X_test: pd.DataFrame,
                      y_test: pd.Series,
                      row_index: int,
                      problem_type: str = None) -> Dict[str, Any]:
    """
    Generate explanation for a specific prediction using SHAP and LIME.

    Args:
        model_dict: Dictionary containing model information
        X_train: Training features
        X_test: Test features
        y_test: Test target values
        row_index: Index of the row to explain
        problem_type: Type of ML problem

    Returns:
        Dict containing detailed prediction explanation
    """
    try:
        if model_dict is None or X_test is None:
            return {
                "success": False,
                "message": "Model or test data not available"
            }

        # Get the row data
        row_data = X_test.iloc[[row_index]]
        actual_value = y_test.iloc[row_index]

        # Get problem type from session state if available
        if problem_type is None:
            if hasattr(st, 'session_state') and hasattr(st.session_state, 'problem_type'):
                problem_type = st.session_state.problem_type
            else:
                problem_type = model_dict.get("problem_type", "unknown")

        # Make prediction
        model_instance = model_dict["model"]
        prediction_results = _make_prediction(model_instance, model_dict, row_data, actual_value, problem_type)

        # Create SHAP explanation
        shap_explanation = _create_shap_explanation(
            model_dict, X_train, row_data, prediction_results, problem_type
        )

        # Create LIME explanation
        lime_explanation = _create_lime_explanation(
            model_instance, X_train, row_data, problem_type
        )

        return {
            "success": True,
            "individual_explanation": {
                "prediction": prediction_results,
                "force_plot": shap_explanation["force_plot"],
                "waterfall_plot": shap_explanation["waterfall_plot"],
                "lime_plot": lime_explanation["lime_plot"],
                "contributions": shap_explanation["contributions"],
                "lime_contributions": lime_explanation["contributions"],
                "base_value": shap_explanation["base_value"]
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error explaining prediction: {str(e)}"
        }


def _make_prediction(model_instance, model_dict: Dict, row_data: pd.DataFrame,
                    actual_value: float, problem_type: str) -> Dict[str, Any]:
    """Make prediction and format results based on problem type."""
    # Make prediction
    if hasattr(model_instance, "predict_proba"):
        prediction = model_instance.predict_proba(row_data)[0]
        if problem_type == "binary_classification":
            pred_value = prediction[1] if len(prediction) > 1 else prediction[0]
        elif problem_type == "multiclass_classification":
            pred_value = prediction  # Keep full probability array for multiclass
        else:  # fallback for legacy "classification"
            pred_value = prediction[1] if len(prediction) > 1 else prediction[0]
    else:
        pred_value = model_instance.predict(row_data)[0]

    # Prepare prediction results based on problem type
    if problem_type == "multiclass_classification":
        # For multiclass, provide comprehensive prediction info
        predicted_class = np.argmax(pred_value)
        max_probability = np.max(pred_value)
        prediction_results = {
            "predicted": float(max_probability),  # Max probability for compatibility
            "predicted_class": int(predicted_class),
            "class_probabilities": pred_value.tolist(),
            "actual": float(actual_value)
        }
    elif problem_type == "binary_classification":
        # For binary, pred_value is already the probability of positive class
        # Use optimal threshold if available
        if (model_dict.get("threshold_optimized", False) and
            model_dict.get("threshold_is_binary", True)):
            optimal_threshold = model_dict.get("optimal_threshold", 0.5)
            predicted_class = 1 if pred_value >= optimal_threshold else 0
        else:
            predicted_class = 1 if pred_value >= 0.5 else 0
        prediction_results = {
            "predicted": float(pred_value),
            "predicted_class": int(predicted_class),
            "actual": float(actual_value)
        }
    else:
        # For regression or legacy classification
        prediction_results = {
            "predicted": float(pred_value),
            "actual": float(actual_value)
        }

    return prediction_results


def _create_shap_explanation(model_dict: Dict, X_train: pd.DataFrame,
                           row_data: pd.DataFrame, prediction_results: Dict,
                           problem_type: str) -> Dict[str, Any]:
    """Create SHAP-based explanation for the prediction."""
    model_instance = model_dict["model"]
    model_type = model_dict.get("type", "unknown")

    # Create background data for the explainer
    n_background = min(100, len(X_train))
    background_indices = np.random.choice(len(X_train), n_background, replace=False)
    background_data = X_train.iloc[background_indices]

    # Create SHAP explainer
    explainer = _create_individual_shap_explainer(
        model_instance, model_type, problem_type, background_data, prediction_results
    )

    # Calculate SHAP values for this prediction
    shap_values = explainer.shap_values(row_data)

    # Handle different SHAP value formats
    if isinstance(shap_values, list):
        if problem_type == "binary_classification":
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
        elif problem_type == "multiclass_classification":
            # For multiclass, we already focused on the predicted class in the explainer
            shap_values = shap_values[0] if len(shap_values) > 0 else shap_values
        else:  # fallback for legacy "classification"
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]

    # Get the expected value based on model type and problem type
    base_value = _get_base_value(explainer, model_type, problem_type, prediction_results)

    # Create force plot with SHAP v0.20+ compatibility
    force_plot = _create_force_plot(base_value, shap_values, row_data)

    # Generate waterfall plot
    waterfall_plot = _create_waterfall_plot(base_value, shap_values, row_data)

    # Get feature contributions for SHAP
    feature_contributions = pd.DataFrame({
        'Feature': row_data.columns,
        'Value': row_data.iloc[0].values,
        'Impact': shap_values[0] if isinstance(shap_values, np.ndarray) else shap_values
    }).sort_values('Impact', key=abs, ascending=False)

    return {
        "force_plot": force_plot,
        "waterfall_plot": waterfall_plot,
        "contributions": feature_contributions.to_dict('records'),
        "base_value": float(base_value)
    }


def _create_individual_shap_explainer(model_instance, model_type: str, problem_type: str,
                                    background_data: pd.DataFrame, prediction_results: Dict):
    """Create SHAP explainer for individual prediction explanation."""
    # Check if model is calibrated and extract underlying model for TreeExplainer
    is_calibrated = isinstance(model_instance, CalibratedClassifierCV)

    if is_calibrated:
        print("- Detected calibrated model in explain_prediction")
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

    # Special handling for XGBoost models
    if ('xgboost' in model_type or 'lightgbm' in model_type) and underlying_model is not None:
        try:
            return shap.TreeExplainer(underlying_model)
        except Exception as e:
            print(f"- TreeExplainer failed: {str(e)}. Falling back to KernelExplainer")
            # Fall back to KernelExplainer with calibrated model
            return _create_kernel_explainer_individual(
                model_instance, problem_type, background_data, prediction_results
            )
    else:
        return _create_kernel_explainer_individual(
            model_instance, problem_type, background_data, prediction_results
        )


def _create_kernel_explainer_individual(model_instance, problem_type: str,
                                       background_data: pd.DataFrame, prediction_results: Dict):
    """Create KernelExplainer for individual predictions."""
    if problem_type in ["binary_classification", "multiclass_classification", "classification"] and hasattr(model_instance, "predict_proba"):
        if problem_type == "binary_classification":
            return shap.KernelExplainer(
                lambda x: model_instance.predict_proba(x)[:, 1],
                background_data
            )
        elif problem_type == "multiclass_classification":
            # For multiclass individual predictions, focus on predicted class
            predicted_class = prediction_results.get("predicted_class", 0)
            return shap.KernelExplainer(
                lambda x: model_instance.predict_proba(x)[:, predicted_class],
                background_data
            )
        else:  # fallback for legacy "classification"
            return shap.KernelExplainer(
                lambda x: model_instance.predict_proba(x)[:, 1],
                background_data
            )
    else:
        return shap.KernelExplainer(
            model_instance.predict,
            background_data
        )


def _get_base_value(explainer, model_type: str, problem_type: str, prediction_results: Dict) -> float:
    """Get the base value for SHAP explanation."""
    if 'xgboost' in model_type or 'lightgbm' in model_type:
        base_value = explainer.expected_value
        if isinstance(base_value, (list, np.ndarray)):
            if problem_type == "multiclass_classification":
                # For multiclass, use the expected value for the predicted class
                predicted_class = prediction_results.get("predicted_class", 0)
                base_value = base_value[predicted_class] if predicted_class < len(base_value) else base_value[0]
            elif problem_type == "binary_classification":
                base_value = base_value[1] if len(base_value) > 1 else base_value[0]
        # For scalar values (like XGBoost regression), use as-is
    else:
        if isinstance(explainer.expected_value, (list, np.ndarray)):
            if problem_type == "multiclass_classification":
                # For multiclass, use the expected value for the predicted class
                predicted_class = prediction_results.get("predicted_class", 0)
                base_value = explainer.expected_value[predicted_class] if predicted_class < len(explainer.expected_value) else explainer.expected_value[0]
            elif problem_type == "binary_classification":
                base_value = explainer.expected_value[1] if len(explainer.expected_value) > 1 else explainer.expected_value[0]
            else:
                base_value = explainer.expected_value[0] if len(explainer.expected_value) > 0 else 0.0
        else:
            base_value = explainer.expected_value

    return float(base_value)


def _create_force_plot(base_value: float, shap_values, row_data: pd.DataFrame):
    """Create SHAP force plot with version compatibility."""
    try:
        # Try new SHAP v0.20+ API first
        force_plot = shap.plots.force(
            base_value,
            shap_values[0] if isinstance(shap_values, np.ndarray) else shap_values,
            row_data.iloc[0],
            feature_names=row_data.columns.tolist(),
            matplotlib=True,
            show=False
        )
    except AttributeError:
        # Fallback to old API for older SHAP versions
        force_plot = shap.force_plot(
            base_value,
            shap_values[0] if isinstance(shap_values, np.ndarray) else shap_values,
            row_data.iloc[0],
            matplotlib=True,
            show=False
        )
    return force_plot


def _create_waterfall_plot(base_value: float, shap_values, row_data: pd.DataFrame):
    """Create SHAP waterfall plot."""
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(
        shap.Explanation(
            values=shap_values[0] if isinstance(shap_values, np.ndarray) else shap_values,
            base_values=float(base_value),
            data=row_data.iloc[0].values,
            feature_names=row_data.columns.tolist()
        ),
        max_display=10,  # Show top 10 features
        show=False
    )
    waterfall_plot = plt.gcf()
    plt.tight_layout()
    return waterfall_plot


def _create_lime_explanation(model_instance, X_train: pd.DataFrame,
                           row_data: pd.DataFrame, problem_type: str) -> Dict[str, Any]:
    """Create LIME-based explanation for the prediction."""
    # Create LIME explainer
    categorical_features = [i for i, col in enumerate(X_train.columns)
                          if not pd.api.types.is_numeric_dtype(X_train[col])]

    feature_names = list(X_train.columns)

    # Set class names based on problem type
    class_names = _get_class_names(model_instance, problem_type)

    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        X_train.values,
        feature_names=feature_names,
        class_names=class_names,
        categorical_features=categorical_features,
        mode="classification" if problem_type in ["binary_classification", "multiclass_classification", "classification"] else "regression"
    )

    # Get LIME explanation - use calibrated model for LIME
    if problem_type in ["binary_classification", "multiclass_classification", "classification"] and hasattr(model_instance, "predict_proba"):
        lime_exp = lime_explainer.explain_instance(
            row_data.iloc[0].values,
            model_instance.predict_proba,
            num_features=len(feature_names)
        )
    else:
        lime_exp = lime_explainer.explain_instance(
            row_data.iloc[0].values,
            model_instance.predict,
            num_features=len(feature_names)
        )

    # Process LIME contributions
    lime_contributions = _process_lime_contributions(lime_exp, feature_names, row_data)

    # Create LIME waterfall plot
    lime_plot = _create_lime_waterfall_plot(lime_contributions)

    return {
        "lime_plot": lime_plot,
        "contributions": lime_contributions.to_dict('records')
    }


def _get_class_names(model_instance, problem_type: str):
    """Get class names for LIME explainer."""
    if problem_type == "binary_classification":
        return ['Negative', 'Positive']
    elif problem_type == "multiclass_classification":
        # Get number of classes from model
        if hasattr(model_instance, "classes_"):
            n_classes = len(model_instance.classes_)
            return [f'Class {i}' for i in range(n_classes)]
        else:
            return None
    elif problem_type == "classification":  # legacy
        return ['Negative', 'Positive']
    else:
        return None


def _process_lime_contributions(lime_exp, feature_names: list, row_data: pd.DataFrame) -> pd.DataFrame:
    """Process LIME explanation results into structured format."""
    lime_contributions = []

    for feat, weight in lime_exp.as_list():
        try:
            # Parse the feature description
            feature_name = None
            feature_value = None

            # Pattern 1: "value1 < feature <= value2"
            match = re.search(r'[\d.-]+ < ([^\s<>≤≥=]+) <= [\d.-]+', feat)
            if match:
                feature_name = match.group(1)
                values = re.findall(r'[\d.-]+', feat)
                if len(values) >= 2:
                    feature_value = f"Range: {values[0]} to {values[1]}"

            # Pattern 2: "feature > value" or "feature <= value"
            if not feature_name:
                match = re.search(r'([^\s<>≤≥=]+)\s*[<>≤≥=]+\s*[\d.-]+', feat)
                if match:
                    feature_name = match.group(1)
                    value = re.search(r'[<>≤≥=]+\s*([\d.-]+)', feat)
                    if value:
                        feature_value = f"Value: {value.group(1)}"

            # If still no match, try numeric index or direct name
            if not feature_name:
                if str(feat).replace('.', '', 1).replace('-', '', 1).isdigit():
                    try:
                        idx = int(float(feat))
                        feature_name = feature_names[idx] if 0 <= idx < len(feature_names) else feat
                    except (ValueError, IndexError):
                        feature_name = feat
                else:
                    feature_name = next((name for name in feature_names if feat.startswith(name)), feat)

            # Clean up feature name and get value from data if needed
            feature_name = re.sub(r'[<>≤≥=]+', '', feature_name).strip()
            if not feature_value and feature_name in row_data.columns:
                feature_value = f"Actual: {row_data[feature_name].iloc[0]}"
            elif not feature_value:
                feature_value = "N/A"

            lime_contributions.append({
                'Feature': feature_name,
                'Value': feature_value,
                'Original_Description': feat,
                'Impact': weight
            })
        except Exception as e:
            print(f"Warning: Error processing LIME feature '{feat}': {str(e)}")
            lime_contributions.append({
                'Feature': str(feat),
                'Value': "Error",
                'Original_Description': f"Error processing feature: {str(e)}",
                'Impact': weight
            })

    lime_contributions_df = pd.DataFrame(lime_contributions)
    lime_contributions_df = lime_contributions_df.sort_values('Impact', key=abs, ascending=False)

    return lime_contributions_df


def _create_lime_waterfall_plot(lime_contributions_df: pd.DataFrame):
    """Create LIME waterfall plot using Plotly."""
    lime_waterfall = go.Figure(go.Waterfall(
        name="LIME",
        orientation="h",
        measure=["relative"] * len(lime_contributions_df),
        x=lime_contributions_df['Impact'].astype(float),
        y=lime_contributions_df['Feature'],
        text=lime_contributions_df['Value'],
        textposition="outside",
        connector={"mode": "spanning", "line": {"width": 1, "color": "rgb(63, 63, 63)", "dash": "solid"}},
        decreasing={"marker": {"color": "rgba(50, 171, 96, 0.7)"}},
        increasing={"marker": {"color": "rgba(219, 64, 82, 0.7)"}},
        hovertemplate="<b>%{y}</b><br>" +
                    "Impact: %{x:.4f}<br>" +
                    "Value: %{text}<br>" +
                    "<extra></extra>"
    ))

    lime_waterfall.update_layout(
        title="LIME Feature Contributions",
        showlegend=False,
        height=max(400, len(lime_contributions_df) * 25),
        margin=dict(t=50, b=50, l=50, r=50),
        yaxis=dict(
            title="Features",
            autorange="reversed"  # Put strongest features at the top
        ),
        xaxis=dict(title="Impact on Prediction")
    )

    return lime_waterfall


def compare_explanations(shap_contributions: list, lime_contributions: list) -> Dict[str, Any]:
    """
    Compare SHAP and LIME explanations to identify consensus and differences.

    Args:
        shap_contributions: List of SHAP feature contributions
        lime_contributions: List of LIME feature contributions

    Returns:
        Dict containing comparison analysis
    """
    # Convert to DataFrames for easier processing
    shap_df = pd.DataFrame(shap_contributions)
    lime_df = pd.DataFrame(lime_contributions)

    # Find common features
    shap_features = set(shap_df['Feature'])
    lime_features = set(lime_df['Feature'])
    common_features = shap_features.intersection(lime_features)

    if not common_features:
        return {
            "success": False,
            "message": "No common features found between SHAP and LIME explanations"
        }

    # Compare feature importance rankings
    shap_ranking = {row['Feature']: idx for idx, row in shap_df.iterrows()}
    lime_ranking = {row['Feature']: idx for idx, row in lime_df.iterrows()}

    ranking_correlation = []
    impact_agreement = []

    for feature in common_features:
        if feature in shap_ranking and feature in lime_ranking:
            # Check if both methods agree on impact direction
            shap_impact = next(row['Impact'] for row in shap_contributions if row['Feature'] == feature)
            lime_impact = next(row['Impact'] for row in lime_contributions if row['Feature'] == feature)

            impact_agreement.append({
                'feature': feature,
                'shap_impact': shap_impact,
                'lime_impact': lime_impact,
                'same_direction': (shap_impact > 0) == (lime_impact > 0)
            })

    agreement_rate = sum(1 for item in impact_agreement if item['same_direction']) / len(impact_agreement) if impact_agreement else 0

    return {
        "success": True,
        "common_features": len(common_features),
        "total_features": len(shap_features.union(lime_features)),
        "agreement_rate": agreement_rate,
        "impact_agreement": impact_agreement,
        "interpretation": "High agreement" if agreement_rate > 0.7 else "Moderate agreement" if agreement_rate > 0.5 else "Low agreement"
    }
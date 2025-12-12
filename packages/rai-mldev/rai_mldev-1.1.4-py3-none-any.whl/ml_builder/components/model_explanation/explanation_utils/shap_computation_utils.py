"""
SHAP Computation Utilities

This module contains utilities for SHAP explainer creation, value calculation,
and model class name handling.

Extracted from what_if_analysis.py to improve code organization and reusability.
"""

import numpy as np
import pandas as pd
import shap
import streamlit as st
from typing import Any, Optional, List
from Builder import Builder


def get_class_names_with_indices(model=None) -> Optional[List[str]]:
    """Get class names in the format 'Class_0 (ActualName)' for consistent display."""
    try:
        if model is None and hasattr(st.session_state, 'builder') and hasattr(st.session_state.builder, 'model'):
            model = st.session_state.builder.model.get("model") or st.session_state.builder.model.get("active_model")
        
        if model and hasattr(model, "classes_"):
            return [f"Class_{i} ({cls})" for i, cls in enumerate(model.classes_)]
        else:
            return None
    except Exception as e:
        st.logger.log_error("Class Names Error", {"error": str(e)}) if hasattr(st.session_state, 'logger') else None
        return None


@st.cache_data
def get_background_data(_builder: Builder, train_data_hash: str, n_background: int = 100) -> pd.DataFrame:
    """Cache and return background data for SHAP calculations."""
    n_background = min(n_background, len(_builder.X_train))
    background_indices = np.random.choice(len(_builder.X_train), n_background, replace=False)
    return _builder.X_train.iloc[background_indices]


def create_shap_explainer(model: Any, background_data: pd.DataFrame, problem_type: str, model_type: str = None) -> shap.KernelExplainer:
    """Create and return a SHAP explainer based on model type."""
    if model_type is None:
        model_type = st.session_state.builder.model.get("type", "unknown") if hasattr(st.session_state, 'builder') else "unknown"
    
    # Check if model is calibrated and extract underlying model for TreeExplainer
    from sklearn.calibration import CalibratedClassifierCV
    is_calibrated = isinstance(model, CalibratedClassifierCV)
    
    if is_calibrated:
        # Extract the underlying model for TreeExplainer
        try:
            # Try new API first (sklearn >= 1.2)
            if hasattr(model, 'estimator'):
                underlying_model = model.estimator
            # Fall back to old API (sklearn < 1.2)
            elif hasattr(model, 'base_estimator'):
                underlying_model = model.base_estimator
            else:
                # If we can't extract, we'll use the calibrated model with KernelExplainer
                underlying_model = None
        except Exception:
            underlying_model = None
    else:
        underlying_model = model
    
    # Special handling for XGBoost models
    if ('xgboost' in model_type or 'lightgbm' in model_type) and underlying_model is not None:
        try:
            return shap.TreeExplainer(underlying_model)
        except Exception as e:
            # Fall back to KernelExplainer with calibrated model
            if problem_type in ["binary_classification", "multiclass_classification", "classification"] and hasattr(model, "predict_proba"):
                if problem_type == "binary_classification":
                    return shap.KernelExplainer(
                        lambda x: model.predict_proba(x)[:, 1],
                        background_data
                    )
                elif problem_type == "multiclass_classification":
                    return shap.KernelExplainer(
                        model.predict_proba,
                        background_data
                    )
                else:  # fallback for legacy "classification"
                    return shap.KernelExplainer(
                        lambda x: model.predict_proba(x)[:, 1],
                        background_data
                    )
            else:
                return shap.KernelExplainer(model.predict, background_data)
    
    # For other models, use KernelExplainer
    if problem_type in ["binary_classification", "multiclass_classification", "classification"] and hasattr(model, "predict_proba"):
        # For binary classification, use probability of positive class
        if problem_type == "binary_classification":
            return shap.KernelExplainer(
                lambda x: model.predict_proba(x)[:, 1],
                background_data
            )
        # For multiclass classification, use all probabilities
        elif problem_type == "multiclass_classification":
            return shap.KernelExplainer(
                model.predict_proba,
                background_data
            )
        else:  # fallback for legacy "classification"
            return shap.KernelExplainer(
                lambda x: model.predict_proba(x)[:, 1],
                background_data
            )
    
    return shap.KernelExplainer(model.predict, background_data)


@st.cache_data
def calculate_shap_values(_explainer: shap.KernelExplainer, input_data: pd.DataFrame) -> np.ndarray:
    """Calculate and cache SHAP values."""
    shap_values = _explainer.shap_values(input_data)
    
    if isinstance(shap_values, list):
        # For multiclass, return all classes (will be processed later)
        # For binary, return positive class
        problem_type = st.session_state.get('problem_type', 'unknown')
        if problem_type == "multiclass_classification":
            # Return all classes as a 3D array: (n_samples, n_features, n_classes)
            result = np.stack(shap_values, axis=-1)
            return result
        else:
            # Binary classification - return positive class
            return shap_values[1] if len(shap_values) > 1 else shap_values[0]
    
    return shap_values
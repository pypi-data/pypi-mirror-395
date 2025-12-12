"""
Form Generation Utilities

This module contains utilities for generating interactive forms in the what-if analysis component.
Handles feature type detection, slider calculations, and complex form UI generation.

Extracted from what_if_analysis.py to improve code organization and reusability.
"""

import streamlit as st
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional
from functools import lru_cache
from Builder import Builder


@lru_cache(maxsize=128)
def calculate_slider_step(min_val: float, max_val: float) -> float:
    """
    Calculate an appropriate step size for a slider based on its range.
    Now cached for better performance.
    """
    value_range = float(max_val - min_val)
    
    if value_range == 0:
        return 0.01
        
    if value_range > 1000:
        return float(max(1.0, round(value_range / 100)))
    elif value_range > 100:
        return float(max(0.1, round(value_range / 100, 1)))
    elif value_range > 10:
        return float(max(0.01, round(value_range / 50, 2)))
    elif value_range > 1:
        return float(max(0.001, round(value_range / 50, 3)))
    else:
        return float(max(0.0001, round(value_range / 50, 4)))


def get_feature_type(column: pd.Series, num_unique: int) -> Tuple[str, bool, bool]:
    """Helper function to determine feature type and characteristics."""
    is_categorical = pd.api.types.is_categorical_dtype(column)
    is_numeric = pd.api.types.is_numeric_dtype(column)
    is_binned = '_binned' in column.name
    is_categorical_numeric = is_numeric and num_unique < 10
    
    feature_type = 'numerical'
    # Add is_binned to the conditions for categorical type
    if is_categorical or is_categorical_numeric or (not is_numeric and num_unique < 10) or is_binned:
        feature_type = 'categorical'
    elif column.dtype == bool:
        feature_type = 'boolean'
        
    return feature_type, is_categorical_numeric, is_binned


def process_original_data(builder: Builder, column: str, info: Dict[str, Any]) -> Dict[str, Any]:
    """Process original data for a column and update info dictionary."""
    if builder.data is None or column not in builder.data.columns:
        return info
        
    orig_column = column
    info['orig_column'] = orig_column
    
    orig_data = builder.data[orig_column]
    if pd.api.types.is_numeric_dtype(orig_data):
        info.update({
            'orig_min': float(orig_data.min()),
            'orig_max': float(orig_data.max()),
            'orig_mean': float(orig_data.mean()),
            'orig_std': float(orig_data.std())
        })
        
        # Store original unique values for potential categorical processing
        if orig_data.nunique() <= 10:
            orig_unique = sorted(orig_data.dropna().unique().tolist())
            info['orig_unique_values'] = orig_unique
            
            if pd.api.types.is_integer_dtype(orig_data):
                min_val = min(orig_unique)
                max_val = max(orig_unique)
                if max_val - min_val < 20:
                    info['orig_unique_values'] = list(range(int(min_val), int(max_val) + 1))
                    
    return info


def create_feature_info(builder: Builder) -> Dict[str, Dict[str, Any]]:
    """
    Create feature information dictionary using test data for structure.
    Optimized version with better data structure usage and reduced redundancy.
    """
    feature_info = {}
    X_test = builder.X_test
    
    # Pre-calculate column statistics once
    column_stats = {
        col: {
            'nunique': X_test[col].nunique(),
            'is_categorical': pd.api.types.is_categorical_dtype(X_test[col]),
            'is_numeric': pd.api.types.is_numeric_dtype(X_test[col])
        }
        for col in X_test.columns
    }
    
    # Process each column
    for column in X_test.columns:
        stats = column_stats[column]
        feature_type, is_categorical_numeric, is_binned = get_feature_type(
            X_test[column], 
            stats['nunique']
        )
        
        # Initialize info with common fields
        info = {
            'type': feature_type,
            'is_binned': is_binned,
            'min': None,  # Initialize min/max as None for all features
            'max': None,
            'mean': None,
            'std': None
        }
        
        # Add numerical statistics if applicable
        if stats['is_numeric']:
            info.update({
                'mean': float(X_test[column].mean()),
                'std': float(X_test[column].std()),
                'min': float(X_test[column].min()),
                'max': float(X_test[column].max())
            })
        
        # Handle categorical data
        if feature_type == 'categorical':
            if stats['is_categorical']:
                info['unique_values'] = X_test[column].cat.categories.tolist()
            else:
                info['unique_values'] = sorted(X_test[column].unique().tolist())
            
            if not stats['is_categorical'] and stats['is_numeric']:
                info['min'] = float(X_test[column].min())
                info['max'] = float(X_test[column].max())
        
        # Process original data if available
        if builder.data is not None:
            info = process_original_data(builder, column, info)
        
        feature_info[column] = info
    
    return feature_info


def _parse_calculated_field(feature_name: str) -> Optional[Dict[str, str]]:
    """
    Parse a feature name to identify if it's a calculated field and extract components.
    Returns None if not a calculated field, or a dict with operation and component features.
    """
    operations = {
        'ratio': ('_ratio_', '÷'),
        'sum': ('_sum_', '+'),
        'difference': ('_difference_', '-'),
        'product': ('_product_', '×'),
        'mean': ('_mean_', '▽')
    }
    
    for op_name, (op_pattern, symbol) in operations.items():
        if op_pattern in feature_name:
            parts = feature_name.split(op_pattern)
            if len(parts) == 2:
                return {
                    'operation': op_name,
                    'symbol': symbol,
                    'feature1': parts[0],
                    'feature2': parts[1]
                }
    return None


def _calculate_feature_value(operation: str, value1: float, value2: float) -> float:
    """Calculate the value for a calculated field based on the operation."""
    if operation == 'ratio':
        return value1 / value2 if value2 != 0 else 0
    elif operation == 'sum':
        return value1 + value2
    elif operation == 'difference':
        return value1 - value2
    elif operation == 'product':
        return value1 * value2
    elif operation == 'mean':
        return (value1 + value2) / 2
    return 0


def create_input_form(feature_info: Dict[str, Dict[str, Any]], initial_values: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Create an input form based on feature information.
    Returns a dictionary of input values.
    """
    input_values = {}
    
    st.markdown("""
    ### 📝 Input Feature Values
    Enter values for each feature below. The form is pre-populated with default values based on the test data.
    
    ℹ️ For numerical features, ranges shown are based on the original dataset where possible, 
    serving as a guide - you can enter values outside these ranges if needed.
    
    ⚠️ For categorical features, all original values are included. Values not seen in training 
    may produce less reliable predictions.
    """)
    
    # First, identify all calculated fields and their required original features
    calculated_fields = {}
    required_original_features = set()
    
    for feature in feature_info.keys():
        calc_info = _parse_calculated_field(feature)
        if calc_info:
            calculated_fields[feature] = calc_info
            required_original_features.add(calc_info['feature1'])
            required_original_features.add(calc_info['feature2'])
    
    # Add any missing original features from preprocessing data
    missing_features = required_original_features - set(feature_info.keys())
    if missing_features and hasattr(st.session_state, 'final_preprocessing_training_data'):
        preprocessing_data = st.session_state.final_preprocessing_training_data
        for feat in missing_features:
            if feat in preprocessing_data.columns:
                # Get basic stats for the feature
                feat_data = preprocessing_data[feat]
                is_binned = '_binned' in feat
                feature_info[feat] = {
                    'type': 'categorical' if not pd.api.types.is_numeric_dtype(feat_data) or is_binned else 'numerical',
                    'min': float(feat_data.min()) if pd.api.types.is_numeric_dtype(feat_data) else None,
                    'max': float(feat_data.max()) if pd.api.types.is_numeric_dtype(feat_data) else None,
                    'mean': float(feat_data.mean()) if pd.api.types.is_numeric_dtype(feat_data) else None,
                    'std': float(feat_data.std()) if pd.api.types.is_numeric_dtype(feat_data) else None,
                    'is_auxiliary': True,  # Mark as auxiliary feature
                    'is_binned': is_binned  # Mark if it's a binned feature
                }
                # For categorical or binned features, add unique values
                if not pd.api.types.is_numeric_dtype(feat_data) or is_binned:
                    feature_info[feat]['unique_values'] = sorted(feat_data.unique().tolist())
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    feature_count = len(feature_info)
    features_per_column = (feature_count + 1) // 2
    
    # Track values for calculated fields
    calculated_values = {}
    
    # First, render all non-calculated fields
    regular_features = [f for f in feature_info.keys() if f not in calculated_fields]
    for idx, feature in enumerate(regular_features):
        info = feature_info[feature]
        current_col = col1 if idx < features_per_column else col2
        
        with current_col:
            # Add visual distinction for auxiliary features
            if info.get('is_auxiliary'):
                st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <span style='color: #ff9800;'>⚠️</span> <b>{feature}</b> (Auxiliary Feature)
                    <br><small>This feature is only used for calculations and won't be passed to the model.</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Create help text with range information
            has_range = info.get('min') is not None and info.get('max') is not None
            if has_range:
                value_range = info['max'] - info['min']
                is_normalized = abs(info['min']) <= 5 and abs(info['max']) <= 5 and value_range <= 10
            else:
                value_range = None
                is_normalized = False
            
            has_orig_data = 'orig_min' in info
            
            # Create help text based on feature type and available information
            if info['type'] == 'numerical':
                if is_normalized and has_orig_data:
                    help_text = f"""
                    Type: {info['type']} (normalized/scaled)
                    Original range: [{info['orig_min']:.2f} to {info['orig_max']:.2f}]
                    Original mean: {info['orig_mean']:.2f}
                    Original std: {info['orig_std']:.2f}
                    Processed range: [{info['min']:.2f} to {info['max']:.2f}]
                    Processed mean: {info['mean']:.2f}
                    Note: This feature has been normalized/scaled from its original values.
                    """
                elif is_normalized:
                    help_text = f"""
                    Type: {info['type']} (likely normalized/scaled)
                    Range: [{info['min']:.2f} to {info['max']:.2f}]
                    Mean: {info['mean']:.2f}
                    Std: {info['std']:.2f}
                    Note: This feature appears to be normalized or scaled.
                    """
                elif has_orig_data:
                    help_text = f"""
                    Type: {info['type']}
                    Range: [{info['min']:.2f} to {info['max']:.2f}]
                    Mean: {info['mean']:.2f}
                    Std: {info['std']:.2f}
                    Original column: {info['orig_column']}
                    Original range: [{info['orig_min']:.2f} to {info['orig_max']:.2f}]
                    """
                else:
                    range_text = f"Range: [{info['min']:.2f} to {info['max']:.2f}]" if has_range else "Range: Not available"
                    mean_text = f"Mean: {info['mean']:.2f}" if info.get('mean') is not None else "Mean: Not available"
                    std_text = f"Std: {info['std']:.2f}" if info.get('std') is not None else "Std: Not available"
                    help_text = f"""
                    Type: {info['type']}
                    {range_text}
                    {mean_text}
                    {std_text}
                    """
            elif info['type'] == 'categorical':
                if 'test_unique_values' in info:
                    test_values_str = ", ".join(map(str, sorted(info['test_unique_values'])))
                    all_values_str = ", ".join(map(str, sorted(info['unique_values'])))
                    help_text = f"""
                    Type: {info['type']}
                    Values in test data: {test_values_str}
                    All possible values: {all_values_str}
                    Note: Values not in test data may produce less reliable predictions.
                    """
                else:
                    help_text = f"""
                    Type: {info['type']}
                    Unique values: {len(info['unique_values'])}
                    """
            else:
                help_text = f"""
                Type: {info['type']}
                """
            
            if info.get('unique_values') and info['type'] != 'categorical':
                help_text += f"\nUnique Values: {', '.join(map(str, info['unique_values']))}"
            
            # Create appropriate input field based on data type
            if info['type'] == 'categorical':
                # Handle categorical fields
                has_extra_categorical_values = False
                if 'test_unique_values' in info:
                    has_extra_categorical_values = True
                    test_values_set = set(info['test_unique_values'])
                
                default_index = 0
                if feature in initial_values:
                    initial_value = initial_values[feature]
                    initial_value_str = str(initial_value)
                    
                    # Special handling for binned features which might be numeric
                    if info.get('is_binned') and isinstance(initial_value, (int, float)):
                        # Try to find exact numeric match first
                        for i, val in enumerate(info['unique_values']):
                            try:
                                if float(val) == float(initial_value):
                                    default_index = i
                                    break
                            except (ValueError, TypeError):
                                continue
                    else:
                        # Standard string matching for non-binned categorical features
                        for i, val in enumerate(info['unique_values']):
                            if str(val) == initial_value_str:
                                default_index = i
                                break
                
                selected_value = st.selectbox(
                    f"{feature}",
                    options=info['unique_values'],
                    index=default_index,
                    help=help_text,
                    key=f"select_{feature}"
                )
                
                if has_extra_categorical_values and str(selected_value) not in map(str, test_values_set):
                    st.warning(f"Value '{selected_value}' was not present in the test data. Prediction may be less reliable.")
                
                input_values[feature] = selected_value
                
            elif info['type'] == 'boolean':
                # Handle boolean fields
                default_value = bool(info.get('mean', 0.5) > 0.5)
                if feature in initial_values:
                    if isinstance(initial_values[feature], bool):
                        default_value = initial_values[feature]
                    elif isinstance(initial_values[feature], (int, float)):
                        default_value = bool(initial_values[feature])
                    elif isinstance(initial_values[feature], str):
                        default_value = initial_values[feature].lower() in ['true', 't', 'yes', 'y', '1']
                
                input_values[feature] = st.checkbox(
                    f"{feature}",
                    value=default_value,
                    help=help_text
                )
            else:
                # Handle numerical fields
                default_value = initial_values.get(feature, info.get('mean', 0))
                
                if has_range:
                    step = calculate_slider_step(info['min'], info['max'])
                    range_info = f"Suggested range: [{info['min']:.4f} to {info['max']:.4f}]"
                    full_help = f"{help_text}\n\n{range_info}"
                    
                    input_values[feature] = st.number_input(
                        f"{feature}",
                        value=float(default_value),
                        step=step,
                        help=full_help,
                        key=f"input_{feature}"
                    )
                else:
                    input_values[feature] = st.number_input(
                        f"{feature}",
                        value=float(default_value),
                        help=help_text,
                        key=f"input_{feature}"
                    )
    
    # Now render calculated fields
    for idx, (feature, calc_info) in enumerate(calculated_fields.items()):
        info = feature_info[feature]
        current_col = col1 if (idx + len(regular_features)) < features_per_column else col2
        
        with current_col:
            # Calculate the value based on input values
            try:
                value1 = float(input_values[calc_info['feature1']])
                value2 = float(input_values[calc_info['feature2']])
                calculated_value = _calculate_feature_value(calc_info['operation'], value1, value2)
            except (KeyError, ValueError, TypeError):
                calculated_value = 0
            
            # Create tooltip with formula
            formula = f"{calc_info['feature1']} {calc_info['symbol']} {calc_info['feature2']}"
            
            # Display calculated field with formula tooltip
            st.markdown(f"""
            <div style='background-color: #e8f4f8; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <span title='{formula}'>🔢 <b>{feature}</b> (Calculated)</span><br>
                <span style='font-family: monospace;'>{calculated_value:.4f}</span>
                <br><small>Formula: {formula}</small>
            </div>
            """, unsafe_allow_html=True)
            
            input_values[feature] = calculated_value
    
    # Return a tuple containing all input values and a filtered dict without auxiliary features
    return {
        'all_values': input_values,
        'model_values': {k: v for k, v in input_values.items() if not feature_info.get(k, {}).get('is_auxiliary', False)}
    }
"""
Tracking utilities for feature selection operations.

This module contains functions for tracking feature selection activities
and maintaining selection history.
"""

import streamlit as st
from typing import List


def track_automated_feature_removal(removed_features: List[str],
                                   method_name: str = "Automated",
                                   addresses_low_importance: bool = False,
                                   addresses_correlation: bool = False) -> None:
    """
    Helper function to track automated feature removals from external components.

    Args:
        removed_features: List of features that were removed
        method_name: Name of the method used for removal
        addresses_low_importance: Whether this method addresses low importance features
        addresses_correlation: Whether this method addresses correlation issues
    """
    if 'feature_selection_tracking' in st.session_state:
        st.session_state.feature_selection_tracking['features_removed_automated'].extend(removed_features)
        if method_name not in st.session_state.feature_selection_tracking['removal_methods_used']:
            st.session_state.feature_selection_tracking['removal_methods_used'].append(method_name)
        if addresses_low_importance:
            st.session_state.feature_selection_tracking['low_importance_addressed'] = True
        if addresses_correlation:
            st.session_state.feature_selection_tracking['correlation_addressed'] = True
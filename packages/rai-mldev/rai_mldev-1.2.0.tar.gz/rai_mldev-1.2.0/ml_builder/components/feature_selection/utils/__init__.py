"""
Feature selection utilities package.

This package contains utility functions for feature selection operations.
"""
from .feature_utils import update_features
from .data_processing_utils import check_and_remove_duplicates, synchronize_data_splits, validate_data_consistency, clean_missing_values
from .correlation_utils import (
    build_correlation_groups,
    create_correlation_analysis_data,
    validate_correlation_group_selection,
    analyze_transitive_impact,
    calculate_weighted_correlation_score,
    UnionFind,
    CORRELATION_DETECTION_THRESHOLD,
    CORRELATION_STRONG_THRESHOLD,
    CORRELATION_VERY_STRONG_THRESHOLD
)
from .selection_strategies import get_available_selection_strategies, create_features_by_category, create_tiered_feature_analysis
from .visualization_utils import create_feature_importance_plot, create_correlation_network_plot, get_feature_importance_stats
from .tracking_utils import track_automated_feature_removal

__all__ = [
    'update_features',
    'check_and_remove_duplicates',
    'synchronize_data_splits',
    'validate_data_consistency',
    'clean_missing_values',
    'build_correlation_groups',
    'create_correlation_analysis_data',
    'validate_correlation_group_selection',
    'analyze_transitive_impact',
    'calculate_weighted_correlation_score',
    'UnionFind',
    'CORRELATION_DETECTION_THRESHOLD',
    'CORRELATION_STRONG_THRESHOLD',
    'CORRELATION_VERY_STRONG_THRESHOLD',
    'get_available_selection_strategies',
    'create_features_by_category',
    'create_tiered_feature_analysis',
    'create_feature_importance_plot',
    'create_correlation_network_plot',
    'get_feature_importance_stats',
    'track_automated_feature_removal'
]
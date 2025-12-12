"""
Model Evaluation Utilities

This module contains utility functions for model evaluation including
core evaluation metrics, visualization utilities, and model limitations analysis.
"""

# Re-export main utility functions for easier imports
from .eval_core_utils import (
    extract_model_predictions, calculate_classification_metrics,
    calculate_regression_metrics, get_classification_report,
    prepare_evaluation_data, prepare_residuals_data,
    calculate_residuals_stats
)
from .eval_visualization_utils import (
    create_confusion_matrix, create_roc_curve, create_classification_learning_curve,
    create_actual_vs_predicted_plot, create_residuals_analysis_plot,
    create_regression_learning_curve
)
from .model_limitations_utils import analyze_model_limitations

__all__ = [
    'extract_model_predictions',
    'calculate_classification_metrics',
    'calculate_regression_metrics',
    'get_classification_report',
    'prepare_evaluation_data',
    'prepare_residuals_data',
    'calculate_residuals_stats',
    'create_confusion_matrix',
    'create_roc_curve',
    'create_classification_learning_curve',
    'create_actual_vs_predicted_plot',
    'create_residuals_analysis_plot',
    'create_regression_learning_curve',
    'analyze_model_limitations'
]
"""
Model Explanation Utilities

This module contains utility functions for model explanation components including
SHAP computation, visualization, scenario management, form generation, and core explanation functionality.
"""

# Re-export main utility functions for easier imports
from .form_generation_utils import create_input_form, create_feature_info
from .shap_computation_utils import get_class_names_with_indices, get_background_data, create_shap_explainer, calculate_shap_values
from .shap_visualization_utils import create_force_plot, create_waterfall_chart, create_radar_chart, CustomJSONEncoder
from .scenario_management_utils import ScenarioManager, generate_comparison_report
from .protected_attributes_utils import get_protected_attributes, analyze_protected_attribute_distribution, check_fairness_requirements
from .model_explanation_core import explain_model, get_model_explanation_summary
from .individual_explanation_utils import explain_prediction, compare_explanations
from .ale_utils import generate_ale, generate_ale_for_multiple_features, analyze_ale_effects

__all__ = [
    'create_input_form',
    'create_feature_info',
    'get_class_names_with_indices',
    'get_background_data',
    'create_shap_explainer',
    'calculate_shap_values',
    'create_force_plot',
    'create_waterfall_chart',
    'create_radar_chart',
    'CustomJSONEncoder',
    'ScenarioManager',
    'generate_comparison_report',
    'get_protected_attributes',
    'analyze_protected_attribute_distribution',
    'check_fairness_requirements',
    'explain_model',
    'get_model_explanation_summary',
    'explain_prediction',
    'compare_explanations',
    'generate_ale',
    'generate_ale_for_multiple_features',
    'analyze_ale_effects'
]
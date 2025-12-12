"""ML Builder - Responsible ML Model Development Guide

A comprehensive Streamlit web application that provides a guided, 9-stage workflow 
for building, training, evaluating, and explaining machine learning models. The 
application emphasizes responsible AI practices with built-in bias detection, 
fairness analysis, and ethical considerations throughout the development pipeline.

Key Features:
- 9-stage guided workflow from data loading to model explanation
- Interactive visualizations and educational content
- Responsible AI integration with bias detection
- Model comparison and hyperparameter optimization
- Comprehensive model explanation with SHAP analysis
- Export capabilities for models and reproduction scripts

Usage:
    After installation, launch the application with:
    $ ml-builder
    
    Or programmatically import the main components:
    >>> from ml_builder import Builder, ModelStage
    >>> builder = Builder()
"""

__version__ = "1.0.0"
__author__ = "Richard Wheeler"
__email__ = "richard.wheeler@priosym.com"

# Import main classes for programmatic use
try:
    from .Builder import Builder
    from .content.stage_info import ModelStage
    
    __all__ = ["Builder", "ModelStage", "__version__", "__author__"]
    
except ImportError:
    # Handle cases where dependencies might not be installed
    __all__ = ["__version__", "__author__"]
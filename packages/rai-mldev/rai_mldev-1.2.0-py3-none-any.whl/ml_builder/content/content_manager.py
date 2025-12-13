"""
Content Manager for ML Builder.

Central class for accessing all text content including stage information,
explanations, and help text that was previously embedded in Builder.py.
"""

from typing import Dict, Any
import streamlit as st
from .stage_info import ModelStage, STAGE_INFO
from .explanations import CALCULATION_EXPLANATIONS
from .statistical_tests import get_statistical_explanation
from .parameter_explanations import (
    PARAMETER_EXPLANATIONS,
    CV_EXPLANATION,
    CV_VISUAL_EXAMPLE,
    SEARCH_EXPLANATION
)
from .model_selection_content import (
    MODEL_CHARACTERISTICS,
    MODEL_DETAILED_EXPLANATIONS,
    MODEL_COMPARISON_CHART,
    QUICK_SELECTION_GUIDE,
    PERFORMANCE_METRICS_EXPLANATIONS
)
from .preprocessing_explanations import (
    ADVANCED_AUTO_PREPROCESSING_EXPLANATION
)


class ContentManager:
    """Central manager for all text content in ML Builder."""

    def __init__(self):
        """Initialize the content manager."""
        self.stage_info = STAGE_INFO
        self.calculation_explanations = CALCULATION_EXPLANATIONS
        self.parameter_explanations = PARAMETER_EXPLANATIONS
        self.model_characteristics = MODEL_CHARACTERISTICS
        self.model_detailed_explanations = MODEL_DETAILED_EXPLANATIONS
        self.model_comparison_chart = MODEL_COMPARISON_CHART
        self.quick_selection_guide = QUICK_SELECTION_GUIDE
        self.performance_metrics_explanations = PERFORMANCE_METRICS_EXPLANATIONS
        self.advanced_auto_preprocessing_explanation = ADVANCED_AUTO_PREPROCESSING_EXPLANATION

    def get_stage_info(self, stage: ModelStage) -> Dict[str, Any]:
        """
        Get information about a specific stage including description and requirements.

        Args:
            stage: The ModelStage enum value

        Returns:
            Dictionary containing stage information or empty dict if not found
        """
        return self.stage_info.get(stage, {})

    def get_current_stage_info(self, current_stage: ModelStage) -> Dict[str, Any]:
        """
        Get information about the current stage (backwards compatibility method).

        Args:
            current_stage: The current ModelStage enum value

        Returns:
            Dictionary containing stage information or empty dict if not found
        """
        return self.get_stage_info(current_stage)

    def get_calculation_explanation(self, calculation_type: str) -> Dict[str, str]:
        """
        Get explanation for a specific calculation type.

        Args:
            calculation_type: Type of calculation to explain

        Returns:
            Dictionary with 'method' and 'interpretation' keys
        """
        return self.calculation_explanations.get(calculation_type, {
            "method": "Explanation not available",
            "interpretation": "Interpretation guide not available"
        })

    def get_statistical_explanation(self, test_type: str, values: Dict[str, float]) -> Dict[str, str]:
        """
        Get explanation for specific statistical test and its values.

        Args:
            test_type: Type of statistical test
            values: Dictionary of test results/values

        Returns:
            Dictionary with 'method' and 'interpretation' keys
        """
        return get_statistical_explanation(test_type, values)

    def get_all_stage_titles(self) -> Dict[str, str]:
        """
        Get all stage titles for navigation purposes.

        Returns:
            Dictionary mapping stage values to titles
        """
        return {
            stage.value: info.get("title", f"Stage {stage.value}")
            for stage, info in self.stage_info.items()
        }

    def get_stage_ethical_considerations(self, stage: ModelStage) -> list:
        """
        Get ethical considerations for a specific stage.

        Args:
            stage: The ModelStage enum value

        Returns:
            List of ethical considerations or empty list if not found
        """
        stage_data = self.get_stage_info(stage)
        return stage_data.get("ethical_considerations", [])

    def get_stage_requirements(self, stage: ModelStage) -> list:
        """
        Get requirements for a specific stage.

        Args:
            stage: The ModelStage enum value

        Returns:
            List of requirements or empty list if not found
        """
        stage_data = self.get_stage_info(stage)
        return stage_data.get("requirements", [])

    def search_content(self, search_term: str) -> Dict[str, list]:
        """
        Search for content across all text in the content manager.

        Args:
            search_term: Term to search for (case-insensitive)

        Returns:
            Dictionary with search results categorized by content type
        """
        search_term = search_term.lower()
        results = {
            "stages": [],
            "calculations": [],
            "statistical_tests": []
        }

        # Search stage information
        for stage, info in self.stage_info.items():
            # Extract text from requirements (handle both string and dict formats)
            requirements_text = ""
            for req in info.get("requirements", []):
                if isinstance(req, str):
                    requirements_text += req + " "
                elif isinstance(req, dict):
                    requirements_text += req.get("title", "") + " "
                    requirements_text += " ".join(req.get("items", [])) + " "

            # Extract text from ethical considerations (handle both string and dict formats)
            ethical_text = ""
            for eth in info.get("ethical_considerations", []):
                if isinstance(eth, str):
                    ethical_text += eth + " "
                elif isinstance(eth, dict):
                    ethical_text += eth.get("title", "") + " "
                    ethical_text += " ".join(eth.get("items", [])) + " "

            stage_text = (
                info.get("title", "").lower() + " " +
                info.get("description", "").lower() + " " +
                requirements_text.lower() + " " +
                ethical_text.lower()
            )
            if search_term in stage_text:
                results["stages"].append({
                    "stage": stage.value,
                    "title": info.get("title", ""),
                    "match_type": "stage_info"
                })

        # Search calculation explanations
        for calc_type, explanation in self.calculation_explanations.items():
            calc_text = (
                explanation.get("method", "").lower() + " " +
                explanation.get("interpretation", "").lower()
            )
            if search_term in calc_text:
                results["calculations"].append({
                    "type": calc_type,
                    "match_type": "calculation_explanation"
                })

        return results

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_parameter_explanations(_self, model_type: str) -> str:
        """
        Get parameter explanations for a specific model type with caching.

        Args:
            model_type: The type of model (e.g., 'random_forest', 'xgboost')

        Returns:
            String containing the parameter explanations for the model
        """
        return _self.parameter_explanations.get(
            model_type,
            "No parameter explanation available for this model type."
        )

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_cv_explanation(_self) -> str:
        """
        Get cross-validation explanation with caching.

        Returns:
            String containing cross-validation explanation
        """
        return CV_EXPLANATION

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_cv_visual_example(_self) -> str:
        """
        Get cross-validation visual example with caching.

        Returns:
            String containing cross-validation visual example
        """
        return CV_VISUAL_EXAMPLE

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_search_explanation(_self) -> str:
        """
        Get parameter search explanation with caching.

        Returns:
            String containing parameter search explanation
        """
        return SEARCH_EXPLANATION

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_advanced_auto_preprocessing_explanation(_self) -> str:
        """
        Get advanced auto preprocessing explanation with caching.

        Returns:
            String containing advanced auto preprocessing explanation
        """
        return _self.advanced_auto_preprocessing_explanation

    def get_model_characteristics(self, model_type: str) -> Dict[str, Any]:
        """
        Get characteristics for a specific model type.

        Args:
            model_type: The type of model (e.g., 'random_forest', 'xgboost')

        Returns:
            Dictionary containing model characteristics
        """
        return self.model_characteristics.get(model_type, {})

    def get_model_detailed_explanation(self, model_category: str) -> str:
        """
        Get detailed explanation for a model category.

        Args:
            model_category: The category of model (e.g., 'linear_models', 'random_forest')

        Returns:
            String containing detailed model explanation
        """
        return self.model_detailed_explanations.get(model_category, "No explanation available for this model category.")

    def get_model_comparison_chart(self) -> dict:
        """
        Get the model comparison chart.

        Returns:
            Dictionary containing the comparison chart data (for DataFrame conversion)
        """
        return self.model_comparison_chart

    def get_quick_selection_guide(self, model_category: str) -> str:
        """
        Get quick selection guide for a model category.

        Args:
            model_category: The category of model

        Returns:
            String containing selection guidance
        """
        return self.quick_selection_guide.get(model_category, "No selection guide available for this model category.")

    def get_performance_metrics_explanation(self, problem_type: str, metric: str) -> Dict[str, Any]:
        """
        Get explanation for a specific performance metric.

        Args:
            problem_type: Either 'classification' or 'regression'
            metric: The specific metric to explain

        Returns:
            Dictionary containing metric explanation
        """
        return self.performance_metrics_explanations.get(problem_type, {}).get(metric, {})
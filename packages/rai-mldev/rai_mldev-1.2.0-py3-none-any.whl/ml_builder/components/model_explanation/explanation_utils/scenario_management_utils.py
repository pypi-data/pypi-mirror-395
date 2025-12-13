"""
Scenario Management Utilities

This module contains utilities for managing what-if analysis scenarios,
including scenario storage, comparison, and report generation.

Extracted from what_if_analysis.py to improve code organization and reusability.
"""

import json
import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional
from components.model_explanation.explanation_utils.shap_visualization_utils import CustomJSONEncoder


class ScenarioManager:
    """Class to manage scenario data and calculations."""
    
    def __init__(self):
        self.scenarios = {}
        self.current_comparison = None
        
    def add_scenario(self, name: str, values: Dict[str, Any], prediction: float):
        """Add a new scenario to the manager."""
        self.scenarios[name] = {
            'values': dict(values),
            'prediction': float(prediction)
        }
        
    def get_scenario(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a scenario by name."""
        return self.scenarios.get(name)
        
    def compare_scenarios(self, scenario1: str, scenario2: str) -> Optional[Dict[str, Any]]:
        """Compare two scenarios and cache results."""
        if not (scenario1 in self.scenarios and scenario2 in self.scenarios):
            return None
            
        data1 = self.scenarios[scenario1]
        data2 = self.scenarios[scenario2]
        
        pred_diff = data2['prediction'] - data1['prediction']
        pred_diff_pct = (pred_diff / data1['prediction']) * 100 if data1['prediction'] != 0 else 0
        
        # Calculate differences efficiently using vectorized operations
        diff_features = []
        common_features = set(data1['values'].keys()) & set(data2['values'].keys())
        
        for feature in common_features:
            val1, val2 = data1['values'][feature], data2['values'][feature]
            if val1 != val2:
                diff_value = "N/A"
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    diff_value = f"{val2 - val1:.4f}"
                    
                diff_features.append({
                    'Feature': feature,
                    f'{scenario1}': val1,
                    f'{scenario2}': val2,
                    'Difference': diff_value
                })
        
        return {
            'scenario1': scenario1,
            'scenario2': scenario2,
            'data1': data1,
            'data2': data2,
            'pred_diff': pred_diff,
            'pred_diff_pct': pred_diff_pct,
            'diff_features': diff_features
        }

    def get_all_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Get all stored scenarios."""
        return self.scenarios.copy()

    def remove_scenario(self, name: str) -> bool:
        """Remove a scenario by name. Returns True if removed, False if not found."""
        if name in self.scenarios:
            del self.scenarios[name]
            return True
        return False

    def clear_all_scenarios(self):
        """Clear all stored scenarios."""
        self.scenarios.clear()
        self.current_comparison = None


@st.cache_data
def generate_comparison_report(scenario1: str, scenario2: str, data1: Dict[str, Any], 
                             data2: Dict[str, Any], feature_impacts: Dict[str, Any], 
                             shap_data: Optional[Dict[str, Any]] = None) -> str:
    """Generate and cache comparison report in JSON format."""
    # Safely get model information
    model_type = "unknown"
    problem_type = "unknown"
    
    if hasattr(st.session_state, 'builder') and st.session_state.builder:
        if hasattr(st.session_state.builder, 'model') and st.session_state.builder.model:
            model_type = st.session_state.builder.model.get("type", "unknown")
            problem_type = st.session_state.builder.model.get("problem_type", "unknown")
    
    # Fallback to session state problem_type
    if problem_type == "unknown":
        problem_type = getattr(st.session_state, 'problem_type', "unknown")
    
    report = {
        "metadata": {
            "report_type": "Scenario Comparison",
            "created_at": datetime.now().isoformat(),
            "model_type": model_type,
            "problem_type": problem_type,
            "feature_count": len(set(list(data1['values'].keys()) + list(data2['values'].keys())))
        },
        "comparison_summary": {
            "scenario1": {
                "name": scenario1,
                "prediction": float(data1['prediction']),
                "feature_count": len(data1['values'])
            },
            "scenario2": {
                "name": scenario2,
                "prediction": float(data2['prediction']),
                "feature_count": len(data2['values'])
            },
            "prediction_difference": {
                "absolute": float(data2['prediction'] - data1['prediction']),
                "percentage": float((data2['prediction'] - data1['prediction']) / data1['prediction'] * 100 if data1['prediction'] != 0 else 0)
            }
        },
        "scenarios": {
            scenario1: data1['values'],
            scenario2: data2['values']
        },
        "feature_impacts": feature_impacts
    }
    
    if shap_data:
        report["shap_analysis"] = shap_data
    
    return json.dumps(report, indent=2, cls=CustomJSONEncoder)
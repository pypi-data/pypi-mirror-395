"""
Feature Selection State Manager.

This module manages session state for the feature selection process,
including initialization, tracking, and state consistency.
"""

import streamlit as st
from typing import Dict, Any, Optional
from Builder import ModelStage


class FeatureSelectionStateManager:
    """Manages session state for feature selection operations."""

    def __init__(self, builder, logger=None):
        """
        Initialize the state manager.

        Args:
            builder: Builder instance containing the dataset
            logger: Optional logger instance for tracking
        """
        self.builder = builder
        self.logger = logger

    def initialize_session_state(self) -> None:
        """Initialize all session state variables for feature selection."""
        # Initialize feature history if not present
        if 'feature_history' not in st.session_state:
            st.session_state.feature_history = []

        # Initialize duplicate history if not present
        if 'duplicate_history' not in st.session_state:
            st.session_state.duplicate_history = []

        # Initialize the tracking function for automated feature removal
        from components.feature_selection.utils.tracking_utils import track_automated_feature_removal
        st.session_state.track_automated_feature_removal = track_automated_feature_removal

        # Initialize feature selection step
        if 'feature_selection_step' not in st.session_state:
            st.session_state.feature_selection_step = 1

        # Initialize automated selection state
        if 'auto_selection_active' not in st.session_state:
            st.session_state.auto_selection_active = False

        # Initialize Boruta-related states
        if 'boruta_result' not in st.session_state:
            st.session_state.boruta_result = None

        if 'boruta_success' not in st.session_state:
            st.session_state.boruta_success = None

        # Save original data state for reset functionality
        self._save_original_data_state()

        # Initialize feature selection tracking
        self._initialize_feature_tracking()

    def _save_original_data_state(self) -> None:
        """Save the original data state for later restoration."""
        if ('original_feature_data' not in st.session_state or
            st.session_state.original_feature_data.get('training_data') is None or
            st.session_state.original_feature_data.get('testing_data') is None):

            st.session_state.original_feature_data = {
                'training_data': self.builder.training_data.copy() if self.builder.training_data is not None else None,
                'testing_data': self.builder.testing_data.copy() if self.builder.testing_data is not None else None,
                'target_column': self.builder.target_column
            }

            # Log that we've saved the original state
            if self.logger:
                self.logger.log_user_action(
                    "Original Data State Saved",
                    {
                        "train_rows": len(self.builder.training_data) if self.builder.training_data is not None else 0,
                        "test_rows": len(self.builder.testing_data) if self.builder.testing_data is not None else 0,
                        "target_column": self.builder.target_column
                    }
                )

    def _initialize_feature_tracking(self) -> None:
        """Initialize feature selection tracking metrics."""
        if 'feature_selection_tracking' not in st.session_state:
            # Calculate initial feature count from original data
            initial_features = 0
            if (st.session_state.original_feature_data.get('training_data') is not None and
                self.builder.target_column):
                initial_features = len([
                    col for col in st.session_state.original_feature_data['training_data'].columns
                    if col != self.builder.target_column
                ])

            st.session_state.feature_selection_tracking = {
                'initial_features': initial_features,
                'features_removed_manual': [],
                'features_removed_automated': [],
                'duplicates_removed': False,
                'correlation_addressed': False,
                'low_importance_addressed': False,
                'removal_methods_used': []
            }

    def get_tracking_summary(self) -> Dict[str, Any]:
        """
        Get a summary of feature selection tracking.

        Returns:
            Dictionary with tracking summary
        """
        tracking = st.session_state.get('feature_selection_tracking', {})
        current_features = len(self.builder.X_train.columns) if self.builder.X_train is not None else 0

        return {
            "initial_features": tracking.get('initial_features', 0),
            "current_features": current_features,
            "manual_removals": len(tracking.get('features_removed_manual', [])),
            "automated_removals": len(tracking.get('features_removed_automated', [])),
            "total_removed": len(tracking.get('features_removed_manual', [])) + len(tracking.get('features_removed_automated', [])),
            "duplicates_removed": tracking.get('duplicates_removed', False),
            "correlation_addressed": tracking.get('correlation_addressed', False),
            "low_importance_addressed": tracking.get('low_importance_addressed', False),
            "methods_used": tracking.get('removal_methods_used', []),
            "reduction_percentage": self._calculate_reduction_percentage(tracking, current_features),
            "features_removed_manual": tracking.get('features_removed_manual', []),
            "features_removed_automated": tracking.get('features_removed_automated', [])
        }

    def _calculate_reduction_percentage(self, tracking: Dict[str, Any], current_features: int) -> float:
        """Calculate the percentage of features removed."""
        initial_features = tracking.get('initial_features', current_features)
        if initial_features > 0:
            removed = initial_features - current_features
            return (removed / initial_features) * 100
        return 0.0

    def reset_to_original_features(self) -> Dict[str, Any]:
        """
        Reset features to their original state.

        Returns:
            Dictionary with reset results
        """
        try:
            original_data = st.session_state.get('original_feature_data')
            if not original_data:
                return {
                    "success": False,
                    "message": "No original data state found"
                }

            # Validate original data
            if (original_data.get('training_data') is None or
                original_data.get('testing_data') is None or
                original_data.get('target_column') is None):
                return {
                    "success": False,
                    "message": "Original data state is incomplete"
                }

            # Check target column exists in datasets
            target_col = original_data['target_column']
            if (target_col not in original_data['training_data'].columns or
                target_col not in original_data['testing_data'].columns):
                return {
                    "success": False,
                    "message": f"Target column '{target_col}' not found in original data"
                }

            # Restore the data
            self.builder.training_data = original_data['training_data'].copy()
            self.builder.testing_data = original_data['testing_data'].copy()
            self.builder.target_column = original_data['target_column']

            # Reconstruct splits ensuring consistent lengths
            self.builder.X_train = self.builder.training_data.drop(columns=[target_col])
            self.builder.X_test = self.builder.testing_data.drop(columns=[target_col])
            self.builder.y_train = self.builder.training_data[target_col]
            self.builder.y_test = self.builder.testing_data[target_col]

            # Verify data consistency
            if (len(self.builder.X_train) != len(self.builder.y_train) or
                len(self.builder.X_test) != len(self.builder.y_test)):
                return {
                    "success": False,
                    "message": "Data consistency check failed after reset"
                }

            # Reset states
            self._reset_selection_states()

            # Log the reset action
            if self.logger:
                self.logger.log_user_action(
                    "Feature Selection Reset",
                    {
                        "restored_features": list(original_data['training_data'].columns),
                        "action": "reset_to_original",
                        "data_consistency": "verified",
                        "target_column": target_col
                    }
                )

            return {
                "success": True,
                "message": "Features reset to original state successfully",
                "restored_features": list(self.builder.X_train.columns)
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Reset failed: {str(e)}"
            }

    def _reset_selection_states(self) -> None:
        """Reset selection-related session states."""
        # Reset automated selection state
        if 'boruta_result' in st.session_state:
            del st.session_state.boruta_result
        if 'auto_selection_active' in st.session_state:
            st.session_state.auto_selection_active = False

        # Reset the step
        st.session_state.feature_selection_step = 1

        # Reset feature selection tracking
        if 'feature_selection_tracking' in st.session_state:
            del st.session_state.feature_selection_tracking

        # Reinitialize tracking with fresh state
        self._initialize_feature_tracking()

    def add_to_feature_history(self, step_info: Optional[str] = None) -> None:
        """
        Add current state to feature history for undo functionality.

        Args:
            step_info: Optional description of the step being saved
        """
        history_entry = {
            'X_train': self.builder.X_train.copy(),
            'X_test': self.builder.X_test.copy(),
            'y_train': self.builder.y_train.copy(),
            'y_test': self.builder.y_test.copy(),
            'step': st.session_state.get('feature_selection_step', 1),
            'step_info': step_info,
            'metrics': st.session_state.get('dedup_metrics', None)
        }
        st.session_state.feature_history.append(history_entry)

    def track_manual_feature_removal(self, removed_features: list, method: str) -> None:
        """
        Track manual feature removal.

        Args:
            removed_features: List of features that were removed
            method: Method used for removal
        """
        if 'feature_selection_tracking' in st.session_state:
            tracking = st.session_state.feature_selection_tracking
            tracking['features_removed_manual'].extend(removed_features)

            if method not in tracking['removal_methods_used']:
                tracking['removal_methods_used'].append(method)

            # Update specific improvement flags based on method
            if method == "Remove Low Importance":
                tracking['low_importance_addressed'] = True
            elif method == "Remove One from Correlated Groups":
                tracking['correlation_addressed'] = True

    def log_page_state(self, additional_context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log the current page state for debugging and analytics.

        Args:
            additional_context: Additional context to include in logging
        """
        if not self.logger:
            return

        base_context = {
            "stage": "FEATURE_SELECTION",
            "data_loaded": bool(st.session_state.get('data')),
            "target_selected": bool(st.session_state.get('target_column')),
            "preprocessing_completed": self.builder.stage_completion.get(
                ModelStage.DATA_PREPROCESSING, False
            ),
            "current_step": st.session_state.get('feature_selection_step', 1)
        }

        if additional_context:
            base_context.update(additional_context)

        self.logger.log_page_state("Feature_Selection", base_context)

    def get_current_step(self) -> int:
        """Get the current feature selection step."""
        return st.session_state.get('feature_selection_step', 1)

    def set_current_step(self, step: int) -> None:
        """Set the current feature selection step."""
        st.session_state.feature_selection_step = step

    def is_auto_selection_active(self) -> bool:
        """Check if automated selection is currently active."""
        return st.session_state.get('auto_selection_active', False)

    def set_auto_selection_active(self, active: bool) -> None:
        """Set the automated selection active state."""
        st.session_state.auto_selection_active = active

    def render_progress_indicator(self) -> None:
        """Render a progress indicator for the feature selection process."""
        current_step = self.get_current_step()
        total_steps = 3
        steps = ["Analysis", "Selection", "Review"]

        # Log progress state
        if self.logger:
            self.logger.log_page_state(
                "Feature_Selection_Progress",
                {
                    "current_step": current_step,
                    "steps_total": total_steps,
                    "steps": steps,
                    "completion_percentage": (current_step / total_steps) * 100
                }
            )
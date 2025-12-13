"""Shared utilities for hyperparameter tuning operations."""

from typing import Dict, Any, List, Optional
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class CVMetricsCalculator:
    """Utility class for calculating cross-validation metrics."""

    def calculate_cv_metrics(self, fold_scores: List[float], adjusted_score: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate cross-validation metrics from fold scores.

        Args:
            fold_scores: List of scores from each CV fold
            adjusted_score: Optional adjusted score value

        Returns:
            Dictionary containing CV metrics
        """
        metrics = {
            "mean_score": float(np.mean(fold_scores)),
            "std_score": float(np.std(fold_scores)),
            "min_score": float(min(fold_scores)),
            "max_score": float(max(fold_scores)),
            "score_range": float(max(fold_scores) - min(fold_scores)),
            "fold_scores": fold_scores
        }

        if adjusted_score is not None:
            metrics["adjusted_score"] = adjusted_score

        return metrics


class PlotGenerator:
    """Utility class for generating tuning-related plots."""

    def create_cv_distribution_plots(self, fold_scores: List[float], cv_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create cross-validation distribution plots.

        Args:
            fold_scores: List of scores from each CV fold
            cv_metrics: CV metrics dictionary

        Returns:
            Dictionary containing plotly figures
        """
        # Distribution plot
        fig_dist = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Score Distribution', 'Cross-validation Scores'),
            specs=[[{"type": "histogram"}, {"type": "box"}]],
            column_widths=[0.7, 0.3]
        )

        # Add histogram of scores using actual fold scores
        fig_dist.add_trace(
            go.Histogram(
                x=fold_scores,
                name='Score Distribution',
                nbinsx=10,
                showlegend=False
            ),
            row=1, col=1
        )

        # Add box plot using actual fold scores
        fig_dist.add_trace(
            go.Box(
                y=fold_scores,
                name='CV Scores',
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8,
                marker_color='rgb(107,174,214)',
                line_color='rgb(8,81,156)',
                showlegend=False
            ),
            row=1, col=2
        )

        # Add mean line to both plots using actual mean
        fig_dist.add_hline(
            y=cv_metrics["mean_score"],
            line_dash="dash",
            line_color="red",
            row=1, col=1
        )
        fig_dist.add_hline(
            y=cv_metrics["mean_score"],
            line_dash="dash",
            line_color="red",
            row=1, col=2
        )

        # Update layout
        fig_dist.update_layout(
            title='Cross-validation Analysis',
            height=500,
            width=1000,
            showlegend=False
        )

        # Create metrics table
        fig_metrics = go.Figure(go.Table(
            header=dict(
                values=['Metric', 'Value', 'Interpretation'],
                font=dict(size=12, color='white'),
                fill_color='rgb(8,81,156)',
                align='left'
            ),
            cells=dict(
                values=[
                    ['Mean Score', 'Standard Deviation', 'Minimum Score', 'Maximum Score', 'Score Range'],
                    [
                        f"{cv_metrics['mean_score']:.3f}",
                        f"{cv_metrics['std_score']:.3f}",
                        f"{cv_metrics['min_score']:.3f}",
                        f"{cv_metrics['max_score']:.3f}",
                        f"{cv_metrics['score_range']:.3f}"
                    ],
                    [
                        'Average performance across folds',
                        'Measure of model stability (lower is better)',
                        'Lowest performance in any fold',
                        'Highest performance in any fold',
                        'Range between best and worst fold'
                    ]
                ],
                align='left'
            )
        ))

        fig_metrics.update_layout(
            title='Cross-validation Metrics Explanation',
            height=300,
            width=1000
        )

        return {
            "distribution": fig_dist,
            "metrics": fig_metrics
        }


class StabilityAnalyzer:
    """Utility class for analyzing model stability."""

    def create_stability_analysis(self, cv_metrics: Dict[str, Any], fold_scores: List[float]) -> Dict[str, Any]:
        """
        Create stability analysis for Random Search results.

        Args:
            cv_metrics: CV metrics dictionary
            fold_scores: List of scores from each CV fold

        Returns:
            Dictionary containing stability analysis
        """
        # Determine stability level
        stability_level = self._determine_stability_level(cv_metrics["std_score"])

        # Create stability plots
        stability_plots = self._create_stability_plots(cv_metrics, fold_scores)

        # Create recommendations
        recommendations = self._get_stability_recommendations(stability_level)

        return {
            "level": stability_level,
            "score": 1 - cv_metrics["std_score"],
            "plots": stability_plots,
            "recommendations": recommendations
        }

    def create_optuna_stability_analysis(
        self,
        cv_results: np.ndarray,
        cv_mean: float,
        cv_std: float,
        stability_score: float
    ) -> Dict[str, Any]:
        """
        Create stability analysis for Optuna results.

        Args:
            cv_results: Array of CV results
            cv_mean: Mean CV score
            cv_std: Standard deviation of CV scores
            stability_score: Calculated stability score

        Returns:
            Dictionary containing stability analysis
        """
        # Determine stability level
        if stability_score > 0.95:
            stability_level = "High stability"
        elif stability_score > 0.9:
            stability_level = "Moderate stability"
        else:
            stability_level = "High variability"

        # Create stability plots for Optuna
        stability_plots = self._create_optuna_stability_plots(cv_results, cv_mean, cv_std, stability_score)

        # Create recommendations
        recommendations = []
        if stability_level != "High stability":
            recommendations = [
                "Consider using more training data",
                "Try different feature combinations",
                "Experiment with different model architectures",
            ]

        return {
            "level": stability_level,
            "score": stability_score,
            "plots": stability_plots,
            "recommendations": recommendations
        }

    def _determine_stability_level(self, std_score: float) -> str:
        """Determine stability level based on standard deviation."""
        if std_score > 0.1:
            return "High variability"
        elif std_score > 0.05:
            return "Moderate variability"
        else:
            return "Stable"

    def _create_stability_plots(self, cv_metrics: Dict[str, Any], fold_scores: List[float]) -> Dict[str, Any]:
        """Create stability visualization plots for Random Search."""
        # Create stability gauge chart
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=1 - cv_metrics["std_score"],
            title={'text': "Model Stability Score"},
            gauge={
                'axis': {'range': [0, 1]},
                'steps': [
                    {'range': [0, 0.9], 'color': "lightgray"},
                    {'range': [0.9, 0.95], 'color': "yellow"},
                    {'range': [0.95, 1], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0.9
                }
            }
        ))
        gauge_fig.update_layout(height=400)

        # Create performance variation chart
        variation_fig = go.Figure()

        # Add performance range area
        variation_fig.add_trace(go.Scatter(
            x=['Min', 'Mean', 'Max'],
            y=[cv_metrics['min_score'], cv_metrics['mean_score'], cv_metrics['max_score']],
            mode='lines+markers',
            name='Score Range',
            line=dict(color='rgb(31, 119, 180)'),
            marker=dict(size=10)
        ))

        # Add error bars
        variation_fig.add_trace(go.Scatter(
            x=['Mean'],
            y=[cv_metrics['mean_score']],
            error_y=dict(
                type='data',
                array=[cv_metrics['std_score']],
                visible=True
            ),
            mode='markers',
            name='Standard Deviation',
            marker=dict(size=12, color='red')
        ))

        variation_fig.update_layout(
            title='Performance Variation',
            yaxis_title='Score',
            showlegend=True,
            height=300
        )

        # Create fold comparison chart
        fold_fig = go.Figure(data=go.Bar(
            x=[f'Fold {i+1}' for i in range(len(fold_scores))],
            y=fold_scores,
            marker_color='lightblue'
        ))

        fold_fig.add_hline(
            y=cv_metrics['mean_score'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean Score: {cv_metrics['mean_score']:.3f}"
        )

        fold_fig.update_layout(
            title='Performance Across Folds',
            xaxis_title='Fold',
            yaxis_title='Score',
            showlegend=False,
            height=400
        )

        return {
            "gauge": gauge_fig,
            "variation": variation_fig,
            "fold_comparison": fold_fig
        }

    def _create_optuna_stability_plots(
        self,
        cv_results: np.ndarray,
        cv_mean: float,
        cv_std: float,
        stability_score: float
    ) -> Dict[str, Any]:
        """Create stability visualization plots for Optuna."""
        # Create gauge chart
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stability_score,
            title={'text': "Model Stability Score"},
            gauge={
                'axis': {'range': [0, 1]},
                'steps': [
                    {'range': [0, 0.9], 'color': "lightgray"},
                    {'range': [0.9, 0.95], 'color': "yellow"},
                    {'range': [0.95, 1], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': stability_score
                }
            }
        ))

        gauge_fig.update_layout(
            height=350,
            margin=dict(l=30, r=30, t=50, b=30)
        )

        # Create variation plot
        variation_fig = go.Figure()

        # Add min-mean-max line
        variation_fig.add_trace(go.Scatter(
            x=['Min', 'Mean', 'Max'],
            y=[cv_results.min(), cv_mean, cv_results.max()],
            mode='lines+markers',
            name='Score Range',
            marker=dict(size=10)
        ))

        # Add error bars using actual std
        variation_fig.add_trace(go.Scatter(
            x=['Mean'],
            y=[cv_mean],
            error_y=dict(
                type='data',
                array=[cv_std],
                visible=True
            ),
            mode='markers',
            name='Standard Deviation',
            marker=dict(size=12, color='red')
        ))

        variation_fig.update_layout(
            title='Performance Variation',
            yaxis_title='Score',
            showlegend=True,
            height=300
        )

        # Create fold comparison chart
        fold_fig = go.Figure(data=go.Bar(
            x=[f'Fold {i+1}' for i in range(len(cv_results))],
            y=cv_results,
            marker_color='lightblue'
        ))

        fold_fig.add_hline(
            y=cv_mean,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean Score: {cv_mean:.3f}"
        )

        fold_fig.update_layout(
            title='Performance Across Folds',
            xaxis_title='Fold',
            yaxis_title='Score',
            showlegend=False,
            height=400
        )

        return {
            "gauge": gauge_fig,
            "variation": variation_fig,
            "fold_comparison": fold_fig
        }

    def _get_stability_recommendations(self, stability_level: str) -> List[str]:
        """Get recommendations based on stability level."""
        if stability_level == "High variability":
            return [
                "Collect more training data to improve model stability",
                "Consider simplifying the model to reduce overfitting",
                "Review feature selection and engineering",
                "Check for data quality issues in problematic folds"
            ]
        elif stability_level == "Moderate variability":
            return [
                "Monitor model performance closely in production",
                "Consider periodic model retraining",
                "Review feature importance for potential improvements"
            ]
        else:
            return [
                "Model shows good stability across different data splits",
                "Continue monitoring performance in production",
                "Consider this configuration for deployment"
            ]
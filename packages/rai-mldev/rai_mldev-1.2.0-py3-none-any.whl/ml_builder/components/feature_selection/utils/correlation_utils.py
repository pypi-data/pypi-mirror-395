"""
Correlation analysis utilities for feature selection.

This module contains functions for analyzing feature correlations, building correlation groups,
and managing correlation-based feature selection strategies.
"""

import pandas as pd
import numpy as np
import math
from typing import List, Dict, Set, Tuple, Any

# Centralized correlation thresholds for consistency
CORRELATION_DETECTION_THRESHOLD = 0.7  # Threshold for identifying correlated pairs
CORRELATION_STRONG_THRESHOLD = 0.8     # Threshold for "strong" correlation
CORRELATION_VERY_STRONG_THRESHOLD = 0.9  # Threshold for "very strong" correlation


class UnionFind:
    """Union-Find data structure for efficiently merging correlation groups."""

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, item):
        """Find the root parent of an item with path compression."""
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0
            return item

        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]

    def union(self, item1, item2):
        """Union two items' sets by rank."""
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 == root2:
            return

        # Union by rank
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

    def get_groups(self) -> List[Set[str]]:
        """Get all groups as a list of sets."""
        groups_dict = {}
        for item in self.parent:
            root = self.find(item)
            if root not in groups_dict:
                groups_dict[root] = set()
            groups_dict[root].add(item)
        return list(groups_dict.values())


def build_correlation_groups(correlations: List[Dict[str, Any]]) -> List[Set[str]]:
    """
    Build correlation groups from a list of correlation pairs using Union-Find algorithm.

    This ensures all transitively connected features are grouped together correctly,
    even in complex correlation graphs.

    Args:
        correlations: List of correlation dictionaries with 'feature1', 'feature2', and 'correlation'

    Returns:
        List of sets, each containing features that are correlated with each other
    """
    if not correlations:
        return []

    # Use Union-Find for robust group merging
    uf = UnionFind()

    for corr in correlations:
        feat1, feat2 = corr['feature1'], corr['feature2']
        uf.union(feat1, feat2)

    return uf.get_groups()


def calculate_correlation_metrics(feature_corr_matrix: pd.DataFrame,
                                features: List[str]) -> Dict[str, float]:
    """
    Calculate correlation metrics for a list of features.

    Args:
        feature_corr_matrix: Correlation matrix for all features
        features: List of feature names to calculate metrics for

    Returns:
        Dictionary mapping feature names to their total correlation scores
    """
    total_correlations = {}
    for feature in features:
        if feature in feature_corr_matrix.columns:
            # Subtract 1 to exclude self-correlation
            total_correlations[feature] = feature_corr_matrix[feature].sum() - 1.0
        else:
            total_correlations[feature] = 0.0

    return total_correlations


def calculate_weighted_correlation_score(feature: str,
                                        group: Set[str],
                                        feature_corr_matrix: pd.DataFrame) -> float:
    """
    Calculate a weighted correlation score that considers correlation strength.

    Higher scores indicate features that are more redundant (higher correlations).

    Args:
        feature: The feature to score
        group: The correlation group containing the feature
        feature_corr_matrix: Correlation matrix for all features

    Returns:
        Weighted correlation score
    """
    weighted_score = 0.0

    for other_feat in group:
        if other_feat != feature:
            corr_value = abs(feature_corr_matrix.loc[feature, other_feat])

            # Weight correlations by strength: stronger correlations contribute more
            if corr_value >= CORRELATION_VERY_STRONG_THRESHOLD:
                weighted_score += corr_value * 3.0  # Very strong correlations weighted heavily
            elif corr_value >= CORRELATION_STRONG_THRESHOLD:
                weighted_score += corr_value * 2.0  # Strong correlations weighted moderately
            else:
                weighted_score += corr_value * 1.0  # Moderate correlations weighted normally

    return weighted_score


def get_correlation_recommendations(correlation_groups: List[Set[str]],
                                  feature_scores: pd.DataFrame,
                                  feature_corr_matrix: pd.DataFrame) -> List[str]:
    """
    Get recommendations for which features to remove from correlation groups.

    Uses weighted scoring that prioritizes removing features with:
    1. Higher weighted correlation scores (stronger redundancy)
    2. Lower feature importance (less predictive value)

    Args:
        correlation_groups: List of sets containing correlated features
        feature_scores: DataFrame with feature importance scores
        feature_corr_matrix: Correlation matrix for all features

    Returns:
        List of feature names recommended for removal
    """
    all_recommended_removals = []
    total_correlations = calculate_correlation_metrics(
        feature_corr_matrix,
        feature_corr_matrix.columns.tolist()
    )

    for group in correlation_groups:
        # Calculate metrics for each feature in group
        group_metrics = []
        for feat in group:
            feat_importance = feature_scores[
                feature_scores['feature'] == feat
            ]['importance'].values[0] if len(feature_scores[feature_scores['feature'] == feat]) > 0 else 0

            # Count correlations above strong threshold for this feature
            high_corr_count = sum(1 for other_feat in group
                                if other_feat != feat and
                                feature_corr_matrix.loc[feat, other_feat] > CORRELATION_STRONG_THRESHOLD)

            # Calculate weighted correlation score
            weighted_corr_score = calculate_weighted_correlation_score(
                feat, group, feature_corr_matrix
            )

            group_metrics.append({
                'feature': feat,
                'importance': feat_importance,
                'total_correlation': total_correlations.get(feat, 0),
                'weighted_correlation': weighted_corr_score,
                'high_corr_count': high_corr_count
            })

        # Calculate group averages for recommendations
        group_df = pd.DataFrame(group_metrics)
        avg_total_corr = group_df['total_correlation'].mean()
        avg_weighted_corr = group_df['weighted_correlation'].mean()
        avg_importance = group_df['importance'].mean()

        # Recommend features for removal based on enhanced criteria
        group_recommended = []
        for _, row in group_df.iterrows():
            # Primary criterion: High weighted correlation + Low importance
            if (row['weighted_correlation'] > avg_weighted_corr and
                row['importance'] < avg_importance):
                group_recommended.append(row['feature'])
            # Secondary criterion: Very high total correlation + Below average importance
            elif (row['total_correlation'] > avg_total_corr * 1.2 and
                  row['importance'] <= avg_importance):
                if row['feature'] not in group_recommended:
                    group_recommended.append(row['feature'])

        # If no clear recommendations, suggest the feature with highest weighted correlation
        if not group_recommended:
            highest_weighted_idx = group_df['weighted_correlation'].idxmax()
            highest_corr_feature = group_df.loc[highest_weighted_idx, 'feature']
            group_recommended = [highest_corr_feature]

        all_recommended_removals.extend(group_recommended)

    return all_recommended_removals


def create_correlation_analysis_data(correlation_groups: List[Set[str]],
                                   feature_scores: pd.DataFrame,
                                   feature_corr_matrix: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Create comprehensive analysis data for correlation groups.

    Args:
        correlation_groups: List of sets containing correlated features
        feature_scores: DataFrame with feature importance scores
        feature_corr_matrix: Correlation matrix for all features

    Returns:
        List of dictionaries containing analysis data for each feature
    """
    correlation_analysis_data = []
    all_recommended_removals = get_correlation_recommendations(
        correlation_groups, feature_scores, feature_corr_matrix
    )
    total_correlations = calculate_correlation_metrics(
        feature_corr_matrix,
        feature_corr_matrix.columns.tolist()
    )

    for group_idx, group in enumerate(correlation_groups):
        # Calculate metrics for each feature in group
        group_metrics = []
        for feat in group:
            feat_importance = feature_scores[
                feature_scores['feature'] == feat
            ]['importance'].values[0] if len(feature_scores[feature_scores['feature'] == feat]) > 0 else 0

            # Count correlations above strong threshold (using centralized constant)
            high_corr_count = sum(1 for other_feat in group
                                if other_feat != feat and
                                feature_corr_matrix.loc[feat, other_feat] > CORRELATION_STRONG_THRESHOLD)

            # Calculate weighted correlation score
            weighted_corr = calculate_weighted_correlation_score(
                feat, group, feature_corr_matrix
            )

            group_metrics.append({
                'feature': feat,
                'importance': feat_importance,
                'total_correlation': total_correlations.get(feat, 0),
                'weighted_correlation': weighted_corr,
                'high_corr_count': high_corr_count,
                'group': group_idx + 1
            })

        # Calculate group averages for recommendations
        group_df = pd.DataFrame(group_metrics)
        avg_total_corr = group_df['total_correlation'].mean()
        avg_weighted_corr = group_df['weighted_correlation'].mean()
        avg_importance = group_df['importance'].mean()

        # Add to comprehensive analysis
        for _, row in group_df.iterrows():
            is_recommended = row['feature'] in all_recommended_removals

            # Create reason based on enhanced analysis
            if is_recommended:
                if row['weighted_correlation'] > avg_weighted_corr and row['importance'] < avg_importance:
                    reason = f"High redundancy (weighted: {row['weighted_correlation']:.2f}) + Low importance ({row['importance']:.4f})"
                elif row['total_correlation'] > avg_total_corr and row['importance'] <= avg_importance:
                    reason = f"High correlation ({row['total_correlation']:.3f}) + Below-avg importance ({row['importance']:.4f})"
                else:
                    reason = f"Highest redundancy in group (weighted: {row['weighted_correlation']:.2f})"
                category = "🔴 Recommended"
            else:
                if row['importance'] > avg_importance:
                    reason = f"Higher importance ({row['importance']:.4f}) preserves predictive value"
                else:
                    reason = f"Lower redundancy (weighted: {row['weighted_correlation']:.2f})"
                category = "🟢 Keep"

            correlation_analysis_data.append({
                "Remove": is_recommended,  # Pre-check recommended features
                "Feature": row['feature'],
                "Group": f"Group {row['group']}",
                "Category": category,
                "Importance": f"{row['importance']:.4f}",
                "Total Correlation": f"{row['total_correlation']:.3f}",
                "High Corr Count": int(row['high_corr_count']),
                "Analysis": reason
            })

    return correlation_analysis_data


def create_correlation_display_data(correlation_groups: List[Set[str]],
                                  feature_corr_matrix: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Create correlation display data for visualization.

    Args:
        correlation_groups: List of sets containing correlated features
        feature_corr_matrix: Correlation matrix for all features

    Returns:
        List of dictionaries containing correlation display information
    """
    all_corr_display_data = []

    for group_idx, group in enumerate(correlation_groups):
        group_features = list(group)

        # Create correlation matrix for this group
        group_corr_matrix = feature_corr_matrix.loc[group_features, group_features]

        # Create a more readable correlation display
        corr_display_data = []
        for i, feat1 in enumerate(group_features):
            for j, feat2 in enumerate(group_features):
                if i < j:  # Only show upper triangle to avoid duplicates
                    corr_value = group_corr_matrix.loc[feat1, feat2]

                    # Add color coding using centralized thresholds
                    if corr_value >= CORRELATION_VERY_STRONG_THRESHOLD:
                        status = "🔴 Very Strong"
                    elif corr_value >= CORRELATION_STRONG_THRESHOLD:
                        status = "🟠 Strong"
                    elif corr_value >= CORRELATION_DETECTION_THRESHOLD:
                        status = "🟡 Moderate"
                    else:
                        status = "🟢 Weaker"

                    corr_display_data.append({
                        "Group": group_idx + 1,
                        "Feature Pair": f"{feat1} ↔ {feat2}",
                        "Correlation": f"{corr_value:.3f}",
                        "Strength": status
                    })

        all_corr_display_data.extend(corr_display_data)

    return all_corr_display_data


def create_network_positions(features: List[str]) -> Dict[str, Tuple[float, float]]:
    """
    Create positions for features in a circular network layout.

    Args:
        features: List of feature names

    Returns:
        Dictionary mapping feature names to (x, y) positions
    """
    n_features = len(features)
    radius = 1
    angle = 2 * math.pi / n_features if n_features > 0 else 0
    feature_positions = {}

    for i, feat in enumerate(features):
        feature_positions[feat] = (
            radius * math.cos(i * angle),
            radius * math.sin(i * angle)
        )

    return feature_positions


def analyze_transitive_impact(selected_features: List[str],
                             correlation_groups: List[Set[str]],
                             feature_corr_matrix: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze the transitive impact of removing selected features.

    Checks if removing features might affect correlations between remaining features
    or if any features act as "bridges" in correlation chains.

    Args:
        selected_features: List of features selected for removal
        correlation_groups: List of sets containing correlated features
        feature_corr_matrix: Correlation matrix for all features

    Returns:
        Dictionary containing transitive impact analysis
    """
    impact_analysis = {
        "has_bridge_features": False,
        "bridge_features": [],
        "affected_correlations": [],
        "warnings": []
    }

    # For each group, check if removing selected features breaks correlation chains
    for group_idx, group in enumerate(correlation_groups):
        group_features = list(group)
        selected_in_group = [f for f in selected_features if f in group]
        remaining_in_group = [f for f in group_features if f not in selected_features]

        if len(selected_in_group) > 0 and len(remaining_in_group) > 1:
            # Check if any selected feature is a "bridge" between remaining features
            for selected_feat in selected_in_group:
                # Find features that are strongly correlated through this selected feature
                for feat1 in remaining_in_group:
                    for feat2 in remaining_in_group:
                        if feat1 != feat2:
                            # Direct correlation between remaining features
                            direct_corr = abs(feature_corr_matrix.loc[feat1, feat2])

                            # Correlations through the selected feature
                            corr_through_selected = (
                                abs(feature_corr_matrix.loc[feat1, selected_feat]) *
                                abs(feature_corr_matrix.loc[selected_feat, feat2])
                            )

                            # If selected feature acts as a strong bridge (weak direct but strong transitive)
                            if (direct_corr < CORRELATION_DETECTION_THRESHOLD and
                                corr_through_selected > CORRELATION_STRONG_THRESHOLD):
                                impact_analysis["has_bridge_features"] = True
                                if selected_feat not in impact_analysis["bridge_features"]:
                                    impact_analysis["bridge_features"].append(selected_feat)

                                impact_analysis["affected_correlations"].append({
                                    "bridge": selected_feat,
                                    "feature1": feat1,
                                    "feature2": feat2,
                                    "direct_correlation": f"{direct_corr:.3f}",
                                    "transitive_strength": f"{corr_through_selected:.3f}",
                                    "group": f"Group {group_idx + 1}"
                                })

    # Generate warnings based on analysis
    if impact_analysis["has_bridge_features"]:
        impact_analysis["warnings"].append(
            f"⚠️ {len(impact_analysis['bridge_features'])} feature(s) act as correlation bridges. "
            f"Removing them may hide relationships between other features."
        )

    return impact_analysis


def validate_correlation_group_selection(correlation_groups: List[Set[str]],
                                       selected_features: List[str]) -> Dict[str, Any]:
    """
    Validate that each correlation group has at least one feature selected for removal.

    Args:
        correlation_groups: List of sets containing correlated features
        selected_features: List of features selected for removal

    Returns:
        Dictionary containing validation results
    """
    group_validation = {}
    groups_with_no_selection = []

    for group_idx, group in enumerate(correlation_groups):
        group_features = list(group)
        selected_in_group = [feat for feat in selected_features if feat in group_features]

        group_name = f"Group {group_idx + 1}"
        group_validation[group_name] = {
            "total_features": len(group_features),
            "selected_features": len(selected_in_group),
            "has_selection": len(selected_in_group) > 0,
            "selected_list": selected_in_group,
            "group_features": group_features
        }

        if len(selected_in_group) == 0:
            groups_with_no_selection.append(group_name)

    return {
        "group_validation": group_validation,
        "groups_with_no_selection": groups_with_no_selection,
        "all_groups_valid": len(groups_with_no_selection) == 0
    }
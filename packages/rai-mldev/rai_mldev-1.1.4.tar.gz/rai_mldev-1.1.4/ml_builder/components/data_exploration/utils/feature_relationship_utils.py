"""
Feature Relationship Analysis Utilities

This module contains utility functions for analyzing relationships between features and with target variables.
Extracted from Builder.get_feature_relationship_plots() and Builder.analyse_feature_target_relationship()
to improve code organization.
"""
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import chi2_contingency, f_oneway, pearsonr


def get_feature_relationship_plots(data: pd.DataFrame, feature1: str, feature2: str,
                                   grouping_feature: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate plots and statistical analysis for the relationship between any two features.

    This function analyzes the relationship between two features and generates appropriate
    visualizations and statistical tests based on their data types.

    Args:
        data: The pandas DataFrame containing the data
        feature1: Name of the first feature to analyze
        feature2: Name of the second feature to analyze
        grouping_feature: Optional feature to group data by for visualization

    Returns:
        Dictionary containing plots and statistical analysis results
    """
    try:
        # Get feature data
        feature1_data = data[feature1]
        feature2_data = data[feature2]

        # Early check for data types
        is_feature1_numeric = pd.api.types.is_numeric_dtype(feature1_data)
        is_feature2_numeric = pd.api.types.is_numeric_dtype(feature2_data)

        # Handle NaN and inf values
        feature1_data_clean = feature1_data.replace([np.inf, -np.inf], np.nan).dropna()
        feature2_data_clean = feature2_data.replace([np.inf, -np.inf], np.nan).dropna()

        # Get indices where both features are valid
        valid_indices = feature1_data_clean.index.intersection(feature2_data_clean.index)
        feature1_data_clean = feature1_data_clean[valid_indices]
        feature2_data_clean = feature2_data_clean[valid_indices]

        # If grouping feature provided, get that data too
        grouping_data_clean = None
        if grouping_feature is not None:
            grouping_data = data[grouping_feature]
            grouping_data_clean = grouping_data.replace([np.inf, -np.inf], np.nan).dropna()
            valid_indices = valid_indices.intersection(grouping_data_clean.index)

            # Refine all series to use common valid indices
            feature1_data_clean = feature1_data_clean[valid_indices]
            feature2_data_clean = feature2_data_clean[valid_indices]
            grouping_data_clean = grouping_data_clean[valid_indices]

        # Check if we have enough data after cleaning
        if len(feature1_data_clean) < 2:
            return {
                "stats": {
                    "error": "Insufficient valid data for analysis",
                    "reason": "Too many missing or invalid values"
                }
            }

        # Create DataFrame for plotting
        plot_df = pd.DataFrame({
            'feature1': feature1_data_clean,
            'feature2': feature2_data_clean
        })

        # Add grouping feature to plot data if available
        if grouping_feature is not None and grouping_data_clean is not None:
            plot_df["group"] = grouping_data_clean

        # Determine if feature2 should be treated as categorical
        feature2_unique_values = feature2_data_clean.nunique()
        is_feature2_categorical = not is_feature2_numeric or feature2_unique_values <= 10

        result = {}

        if is_feature1_numeric:
            if is_feature2_categorical:
                # Numerical feature vs Categorical feature
                # Density plot
                fig_density = px.histogram(
                    plot_df,
                    x='feature1',
                    color='feature2',
                    marginal='box',
                    title=f"Distribution of {feature1} by {feature2}",
                    labels={"feature1": feature1, "feature2": feature2}
                )
                result["density"] = fig_density

                # Violin plot
                fig_violin = px.violin(
                    plot_df,
                    x='feature2',
                    y='feature1',
                    box=True,
                    points="all",
                    title=f"Distribution of {feature1} by {feature2}",
                    labels={"feature1": feature1, "feature2": feature2}
                )
                result["violin"] = fig_violin

                # Box plot
                fig_box = px.box(
                    plot_df,
                    x='feature2',
                    y='feature1',
                    title=f"Distribution of {feature1} by {feature2}",
                    labels={"feature1": feature1, "feature2": feature2}
                )
                result["box"] = fig_box

                # ANOVA test
                try:
                    groups = [group for name, group in feature1_data_clean.groupby(feature2_data_clean)]
                    if len(groups) >= 2 and all(len(g) > 1 for g in groups):
                        f_stat, p_value = f_oneway(*groups)
                        result["stats"] = {
                            "test": "One-way ANOVA",
                            "statistic": float(f_stat),
                            "p_value": float(p_value)
                        }
                    else:
                        result["stats"] = {
                            "error": "Cannot perform statistical test",
                            "reason": "Insufficient data in some categories for statistical comparison"
                        }
                except Exception as e:
                    result["stats"] = {
                        "error": "Error performing statistical test",
                        "reason": str(e)
                    }
            else:
                # Numerical feature vs Numerical feature
                # Scatter plot
                fig_scatter = px.scatter(
                    plot_df,
                    x='feature1',
                    y='feature2',
                    trendline="ols",
                    title=f"{feature1} vs {feature2}",
                    labels={"feature1": feature1, "feature2": feature2}
                )
                result["scatter"] = fig_scatter

                # Hexbin plot
                fig_hexbin = px.density_heatmap(
                    plot_df,
                    x='feature1',
                    y='feature2',
                    title=f"Density of {feature1} vs {feature2}",
                    labels={"feature1": feature1, "feature2": feature2}
                )
                result["hexbin"] = fig_hexbin

                # Correlation analysis
                try:
                    correlation, p_value = pearsonr(feature1_data_clean, feature2_data_clean)
                    result["stats"] = {
                        "test": "Pearson Correlation",
                        "statistic": float(correlation),
                        "p_value": float(p_value)
                    }
                except Exception as e:
                    result["stats"] = {
                        "error": "Could not compute correlation",
                        "reason": str(e)
                    }
        else:
            if is_feature2_categorical:
                # Categorical feature vs Categorical feature
                # Create contingency table
                contingency = pd.crosstab(plot_df['feature1'], plot_df['feature2'])

                # Stacked bar chart
                fig_stacked = px.bar(
                    contingency,
                    barmode='stack',
                    title=f"Distribution of {feature2} by {feature1}",
                    labels={"index": feature1, "value": "Count", "variable": feature2}
                )
                result["stacked_bar"] = fig_stacked

                # Association heatmap
                fig_heatmap = px.imshow(
                    contingency,
                    title=f"Association between {feature1} and {feature2}",
                    labels={"x": feature2, "y": feature1},
                    aspect="auto"
                )
                result["heatmap"] = fig_heatmap

                # Chi-square test
                try:
                    chi2, p_value, dof, expected = chi2_contingency(contingency)
                    result["stats"] = {
                        "test": "Chi-square Test",
                        "chi2": float(chi2),
                        "p_value": float(p_value),
                        "dof": int(dof)
                    }
                except Exception as e:
                    result["stats"] = {
                        "error": "Error performing chi-square test",
                        "reason": str(e)
                    }
            else:
                # Categorical feature vs Numerical feature
                # Box plot
                fig_box = px.box(
                    plot_df,
                    x='feature1',
                    y='feature2',
                    title=f"Distribution of {feature2} by {feature1}",
                    labels={"feature1": feature1, "feature2": feature2}
                )
                result["box"] = fig_box

                # Violin plot
                fig_violin = px.violin(
                    plot_df,
                    x='feature1',
                    y='feature2',
                    box=True,
                    points="all",
                    title=f"Distribution of {feature2} by {feature1}",
                    labels={"feature1": feature1, "feature2": feature2}
                )
                result["violin"] = fig_violin

                # Bar plot with error bars
                agg_df = plot_df.groupby('feature1').agg({
                    'feature2': ['mean', 'sem']
                }).reset_index()
                agg_df.columns = ['feature1', 'mean', 'sem']

                fig_bar = px.bar(
                    agg_df,
                    x='feature1',
                    y='mean',
                    error_y='sem',
                    title=f"Mean {feature2} by {feature1}",
                    labels={"feature1": feature1, "mean": f"Mean {feature2}", "sem": "Standard Error"}
                )
                result["bar"] = fig_bar

                # ANOVA test
                try:
                    groups = [group for name, group in feature2_data_clean.groupby(feature1_data_clean)]
                    if len(groups) >= 2 and all(len(g) > 1 for g in groups):
                        f_stat, p_value = f_oneway(*groups)
                        result["stats"] = {
                            "test": "One-way ANOVA",
                            "statistic": float(f_stat),
                            "p_value": float(p_value)
                        }
                    else:
                        result["stats"] = {
                            "error": "Cannot perform statistical test",
                            "reason": "Insufficient data in some categories for statistical comparison"
                        }
                except Exception as e:
                    result["stats"] = {
                        "error": "Error performing statistical test",
                        "reason": str(e)
                    }

        return result

    except Exception as e:
        return {
            "stats": {
                "error": "Error analyzing relationship",
                "reason": str(e)
            }
        }


def analyze_feature_target_relationship(data: pd.DataFrame, feature: str, target: str,
                                        grouping_feature: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze relationship between a feature and target variable.

    This function generates comprehensive visualizations and statistical analysis for the
    relationship between a feature and target variable, with support for grouping.

    Args:
        data: The pandas DataFrame containing the data
        feature: Name of the feature to analyze
        target: Name of the target variable
        grouping_feature: Optional feature to group data by for visualization

    Returns:
        Dictionary containing analysis results and visualizations
    """
    try:
        # Get feature and target data
        feature_data = data[feature]
        target_data = data[target]

        # Early check for data types
        is_feature_numeric = pd.api.types.is_numeric_dtype(feature_data)
        is_target_numeric = pd.api.types.is_numeric_dtype(target_data)

        # Handle NaN and inf values
        feature_data_clean = feature_data.replace([np.inf, -np.inf], np.nan).dropna()
        target_data_clean = target_data.replace([np.inf, -np.inf], np.nan).dropna()

        # Get indices where both feature and target are valid
        valid_indices = feature_data_clean.index.intersection(target_data_clean.index)
        feature_data_clean = feature_data_clean[valid_indices]
        target_data_clean = target_data_clean[valid_indices]

        # If grouping feature provided, get that data too
        grouping_data_clean = None
        if grouping_feature is not None:
            grouping_data = data[grouping_feature]
            grouping_data_clean = grouping_data.replace([np.inf, -np.inf], np.nan).dropna()
            valid_indices = valid_indices.intersection(grouping_data_clean.index)

            # Refine all series to use common valid indices
            feature_data_clean = feature_data_clean[valid_indices]
            target_data_clean = target_data_clean[valid_indices]
            grouping_data_clean = grouping_data_clean[valid_indices]

        # Check if we have enough data after cleaning
        if len(feature_data_clean) < 2:
            return {
                "stats": {
                    "error": "Insufficient valid data for analysis",
                    "reason": "Too many missing or invalid values"
                }
            }

        # Create DataFrame for plotting
        plot_df = pd.DataFrame({
            'feature': feature_data_clean,
            'target': target_data_clean
        })

        # Add grouping feature to plot data if available
        if grouping_feature is not None and grouping_data_clean is not None:
            plot_df['group'] = grouping_data_clean

        # Determine if this is a classification problem
        target_unique_values = target_data_clean.nunique()
        is_classification = not is_target_numeric or target_unique_values <= 10

        result = {}

        if is_feature_numeric:
            if is_classification:
                # Numerical feature vs Categorical target (Classification)
                # Density plot
                if grouping_feature is not None:
                    # Use facet_row for grouping or color if number of groups is small
                    if len(plot_df['group'].unique()) <= 5:
                        fig_density = px.histogram(
                            plot_df,
                            x='feature',
                            color='target',
                            facet_row='group',
                            marginal='box',
                            title=f"Distribution of {feature} by {target}, grouped by {grouping_feature}",
                            labels={"feature": feature, "target": target, "group": grouping_feature}
                        )
                    else:
                        # For many groups, use color and animate between groups
                        fig_density = px.histogram(
                            plot_df,
                            x='feature',
                            color='target',
                            animation_frame='group',
                            marginal='box',
                            title=f"Distribution of {feature} by {target}, grouped by {grouping_feature}",
                            labels={"feature": feature, "target": target, "group": grouping_feature}
                        )
                else:
                    fig_density = px.histogram(
                        plot_df,
                        x='feature',
                        color='target',
                        marginal='box',
                        title=f"Distribution of {feature} by {target}",
                        labels={"feature": feature, "target": target}
                    )
                result["density"] = fig_density

                # Violin plot
                if grouping_feature is not None:
                    fig_violin = px.violin(
                        plot_df,
                        x='target',
                        y='feature',
                        color='group',
                        box=True,
                        points="all",
                        title=f"Distribution of {feature} by {target}, grouped by {grouping_feature}",
                        labels={"feature": feature, "target": target, "group": grouping_feature}
                    )
                else:
                    fig_violin = px.violin(
                        plot_df,
                        x='target',
                        y='feature',
                        box=True,
                        points="all",
                        title=f"Distribution of {feature} by {target}",
                        labels={"feature": feature, "target": target}
                    )
                result["violin"] = fig_violin

                # Box plot
                if grouping_feature is not None:
                    fig_box = px.box(
                        plot_df,
                        x='target',
                        y='feature',
                        color='group',
                        title=f"Distribution of {feature} by {target}, grouped by {grouping_feature}",
                        labels={"feature": feature, "target": target, "group": grouping_feature}
                    )
                else:
                    fig_box = px.box(
                        plot_df,
                        x='target',
                        y='feature',
                        title=f"Distribution of {feature} by {target}",
                        labels={"feature": feature, "target": target}
                    )
                result["box"] = fig_box

                # Statistical test (ANOVA)
                try:
                    groups = [group for name, group in feature_data_clean.groupby(target_data_clean)]
                    if len(groups) >= 2 and all(len(g) > 1 for g in groups):
                        f_stat, p_value = f_oneway(*groups)
                        result["stats"] = {
                            "test": "One-way ANOVA",
                            "statistic": float(f_stat),
                            "p_value": float(p_value)
                        }
                    else:
                        result["stats"] = {
                            "error": "Cannot perform statistical test",
                            "reason": "Insufficient data in some categories for statistical comparison"
                        }
                except Exception as e:
                    result["stats"] = {
                        "error": "Error performing statistical test",
                        "reason": str(e)
                    }
            else:
                # Numerical feature vs Numerical target (Regression)
                # Scatter plot
                if grouping_feature is not None:
                    fig_scatter = px.scatter(
                        plot_df,
                        x='feature',
                        y='target',
                        color='group',
                        trendline="ols",
                        title=f"{feature} vs {target}, grouped by {grouping_feature}",
                        labels={"feature": feature, "target": target, "group": grouping_feature}
                    )
                else:
                    fig_scatter = px.scatter(
                        plot_df,
                        x='feature',
                        y='target',
                        trendline="ols",
                        title=f"{feature} vs {target}",
                        labels={"feature": feature, "target": target}
                    )
                result["scatter"] = fig_scatter

                # Hexbin plot (Density heatmap)
                if grouping_feature is not None and len(plot_df['group'].unique()) <= 4:
                    # Use facet_col for small number of groups
                    fig_hexbin = px.density_heatmap(
                        plot_df,
                        x='feature',
                        y='target',
                        facet_col='group',
                        title=f"Density of {feature} vs {target}, grouped by {grouping_feature}",
                        labels={"feature": feature, "target": target, "group": grouping_feature}
                    )
                else:
                    fig_hexbin = px.density_heatmap(
                        plot_df,
                        x='feature',
                        y='target',
                        title=f"Density of {feature} vs {target}",
                        labels={"feature": feature, "target": target}
                    )
                result["hexbin"] = fig_hexbin

                # Correlation analysis
                try:
                    correlation, p_value = pearsonr(feature_data_clean, target_data_clean)
                    result["stats"] = {
                        "test": "Pearson Correlation",
                        "statistic": float(correlation),
                        "p_value": float(p_value)
                    }
                except Exception as e:
                    result["stats"] = {
                        "error": "Could not compute correlation",
                        "reason": str(e)
                    }
        else:
            if is_classification:
                # Categorical feature vs Categorical target (Classification)
                if grouping_feature is not None:
                    # For grouped data, create a grouped bar chart
                    grouped_contingency = pd.crosstab(
                        [plot_df['feature'], plot_df['group']],
                        plot_df['target']
                    ).reset_index()

                    # Reshape for grouped bar chart
                    grouped_contingency_melted = pd.melt(
                        grouped_contingency,
                        id_vars=['feature', 'group'],
                        var_name='target',
                        value_name='count'
                    )

                    # Stacked bar chart with grouping
                    fig_stacked = px.bar(
                        grouped_contingency_melted,
                        x='feature',
                        y='count',
                        color='target',
                        barmode='stack',
                        facet_col='group',
                        title=f"Distribution of {target} by {feature}, grouped by {grouping_feature}",
                        labels={"feature": feature, "count": "Count", "target": target, "group": grouping_feature}
                    )
                    result["stacked_bar"] = fig_stacked

                    # Add a sunburst chart for hierarchical visualization
                    fig_sunburst = px.sunburst(
                        plot_df,
                        path=['group', 'feature', 'target'],
                        title=f"Hierarchical view of {feature}, {target}, and {grouping_feature}"
                    )
                    result["sunburst"] = fig_sunburst
                else:
                    # Regular contingency table without grouping
                    contingency = pd.crosstab(plot_df['feature'], plot_df['target'])

                    # Stacked bar chart
                    fig_stacked = px.bar(
                        contingency,
                        barmode='stack',
                        title=f"Distribution of {target} by {feature}",
                        labels={"index": feature, "value": "Count", "variable": target}
                    )
                    result["stacked_bar"] = fig_stacked

                # Association heatmap
                if grouping_feature is None:
                    # Standard heatmap for non-grouped data
                    contingency = pd.crosstab(plot_df['feature'], plot_df['target'])
                    fig_heatmap = px.imshow(
                        contingency,
                        title=f"Association between {feature} and {target}",
                        labels={"x": target, "y": feature},
                        aspect="auto"
                    )
                    result["heatmap"] = fig_heatmap
                else:
                    # For grouped data, create separate heatmaps or an animated heatmap
                    if len(plot_df['group'].unique()) <= 4:
                        # Create separate heatmaps for each group
                        for group_val, group_df in plot_df.groupby('group'):
                            group_contingency = pd.crosstab(group_df['feature'], group_df['target'])
                            fig_group_heatmap = px.imshow(
                                group_contingency,
                                title=f"Association between {feature} and {target} (Group: {group_val})",
                                labels={"x": target, "y": feature},
                                aspect="auto"
                            )
                            result[f"heatmap_{group_val}"] = fig_group_heatmap

                # Chi-square test
                try:
                    # Basic chi-square test (not grouped)
                    contingency = pd.crosstab(plot_df['feature'], plot_df['target'])
                    chi2, p_value, dof, expected = chi2_contingency(contingency)
                    result["stats"] = {
                        "test": "Chi-square Test",
                        "chi2": float(chi2),
                        "p_value": float(p_value),
                        "dof": int(dof)
                    }
                except Exception as e:
                    result["stats"] = {
                        "error": "Error performing chi-square test",
                        "reason": str(e)
                    }
            else:
                # Categorical feature vs Numerical target (Regression)
                # Box plot
                if grouping_feature is not None:
                    fig_box = px.box(
                        plot_df,
                        x='feature',
                        y='target',
                        color='group',
                        title=f"Distribution of {target} by {feature}, grouped by {grouping_feature}",
                        labels={"feature": feature, "target": target, "group": grouping_feature}
                    )
                else:
                    fig_box = px.box(
                        plot_df,
                        x='feature',
                        y='target',
                        title=f"Distribution of {target} by {feature}",
                        labels={"feature": feature, "target": target}
                    )
                result["box"] = fig_box

                # Violin plot
                if grouping_feature is not None:
                    fig_violin = px.violin(
                        plot_df,
                        x='feature',
                        y='target',
                        color='group',
                        box=True,
                        points="all",
                        title=f"Distribution of {target} by {feature}, grouped by {grouping_feature}",
                        labels={"feature": feature, "target": target, "group": grouping_feature}
                    )
                else:
                    fig_violin = px.violin(
                        plot_df,
                        x='feature',
                        y='target',
                        box=True,
                        points="all",
                        title=f"Distribution of {target} by {feature}",
                        labels={"feature": feature, "target": target}
                    )
                result["violin"] = fig_violin

                # Bar plot with error bars
                if grouping_feature is not None:
                    # Grouped bar chart with error bars
                    agg_df = plot_df.groupby(['feature', 'group']).agg({
                        'target': ['mean', 'sem']
                    }).reset_index()
                    agg_df.columns = ['feature', 'group', 'mean', 'sem']

                    fig_bar = px.bar(
                        agg_df,
                        x='feature',
                        y='mean',
                        color='group',
                        error_y='sem',
                        barmode='group',
                        title=f"Mean {target} by {feature}, grouped by {grouping_feature}",
                        labels={"feature": feature, "mean": f"Mean {target}", "sem": "Standard Error",
                                "group": grouping_feature}
                    )
                else:
                    agg_df = plot_df.groupby('feature').agg({
                        'target': ['mean', 'sem']
                    }).reset_index()
                    agg_df.columns = ['feature', 'mean', 'sem']

                    fig_bar = px.bar(
                        agg_df,
                        x='feature',
                        y='mean',
                        error_y='sem',
                        title=f"Mean {target} by {feature}",
                        labels={"feature": feature, "mean": f"Mean {target}", "sem": "Standard Error"}
                    )
                result["bar"] = fig_bar

                # ANOVA test
                try:
                    groups = [group for name, group in target_data_clean.groupby(feature_data_clean)]
                    if len(groups) >= 2 and all(len(g) > 1 for g in groups):
                        f_stat, p_value = f_oneway(*groups)
                        result["stats"] = {
                            "test": "One-way ANOVA",
                            "statistic": float(f_stat),
                            "p_value": float(p_value)
                        }
                    else:
                        result["stats"] = {
                            "error": "Cannot perform statistical test",
                            "reason": "Insufficient data in some categories for statistical comparison"
                        }
                except Exception as e:
                    result["stats"] = {
                        "error": "Error performing statistical test",
                        "reason": str(e)
                    }

        return result

    except Exception as e:
        return {
            "stats": {
                "error": "Error analyzing relationship",
                "reason": str(e)
            }
        }
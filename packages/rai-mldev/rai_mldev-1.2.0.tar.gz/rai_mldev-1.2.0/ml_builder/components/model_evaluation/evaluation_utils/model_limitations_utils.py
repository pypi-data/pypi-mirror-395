"""
Model Limitations Analysis Utilities

This module contains utilities for analyzing model limitations, data quality issues,
and providing recommendations for model improvement.

Extracted from Builder.py to improve code organization and reusability.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any, List
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


def analyze_model_limitations(model_dict: Dict[str, Any],
                            X_train: pd.DataFrame,
                            y_train: pd.Series,
                            problem_type: str) -> Dict[str, Any]:
    """
    Analyze and identify potential limitations and considerations of the current model.

    Args:
        model_dict: Dictionary containing model information
        X_train: Training features
        y_train: Training target
        problem_type: Type of ML problem (classification/regression)

    Returns:
        Dict containing analysis results, limitations, warnings, and recommendations
    """
    try:
        print("\n=== Starting Model Limitations Analysis ===")

        # Check if required components are available
        if model_dict is None:
            print("Error: Model is None")
            return {
                "success": False,
                "message": "Model not available"
            }

        if X_train is None:
            print("Error: X_train is None")
            return {
                "success": False,
                "message": "Training data not available"
            }

        if y_train is None:
            print("Error: y_train is None")
            return {
                "success": False,
                "message": "Training labels not available"
            }

        print("Initial validation passed - required components are present")

        limitations = []
        warnings = []
        recommendations = []
        metrics = {}
        limitation_plots = {}
        data_quality = {}
        improvement_metrics = []

        # Get model characteristics
        model_type = model_dict.get("type", "unknown")
        model_instance = model_dict["model"]

        print(f"\nModel Details:")
        print(f"- Problem type: {problem_type}")
        print(f"- Model type: {model_type}")
        print(f"- Model instance type: {type(model_instance)}")

        # 1. Data Size Analysis
        try:
            limitations_data = _analyze_data_size(X_train, y_train, limitations, recommendations, metrics)
            limitations.extend(limitations_data["limitations"])
            recommendations.extend(limitations_data["recommendations"])
            metrics.update(limitations_data["metrics"])
        except Exception as e:
            print(f"Error in data size analysis: {str(e)}")

        # 2. Feature Correlation Analysis
        try:
            correlation_data = _analyze_feature_correlations(X_train, warnings, recommendations, metrics, limitation_plots)
            warnings.extend(correlation_data["warnings"])
            recommendations.extend(correlation_data["recommendations"])
            metrics.update(correlation_data["metrics"])
            limitation_plots.update(correlation_data["plots"])
        except Exception as e:
            print(f"Error in feature correlation analysis: {str(e)}")

        # 3. Class Distribution Analysis (for classification)
        try:
            if problem_type in ["classification", "binary_classification", "multiclass_classification"]:
                class_data = _analyze_class_distribution(y_train, warnings, recommendations, metrics, limitation_plots)
                warnings.extend(class_data["warnings"])
                recommendations.extend(class_data["recommendations"])
                metrics.update(class_data["metrics"])
                limitation_plots.update(class_data["plots"])
        except Exception as e:
            print(f"Error in class distribution analysis: {str(e)}")

        # 4. Feature Importance Analysis
        try:
            importance_data = _analyze_feature_importance(model_dict, X_train, y_train, problem_type, warnings, recommendations, limitation_plots)
            warnings.extend(importance_data["warnings"])
            recommendations.extend(importance_data["recommendations"])
            limitation_plots.update(importance_data["plots"])
        except Exception as e:
            print(f"Error in feature importance analysis: {str(e)}")

        # 5. Model Complexity Analysis
        try:
            complexity_data = _analyze_model_complexity(model_instance, X_train, warnings, recommendations)
            warnings.extend(complexity_data["warnings"])
            recommendations.extend(complexity_data["recommendations"])
        except Exception as e:
            print(f"Error in model complexity analysis: {str(e)}")

        # 6. Data Quality Analysis
        try:
            quality_data = _analyze_data_quality(X_train, warnings, recommendations, data_quality)
            warnings.extend(quality_data["warnings"])
            recommendations.extend(quality_data["recommendations"])
            data_quality.update(quality_data["data_quality"])
        except Exception as e:
            print(f"Error in data quality analysis: {str(e)}")

        print("\nAnalysis completed successfully")
        print(f"Generated {len(limitation_plots)} plots")
        print(f"Found {len(warnings)} warnings")
        print(f"Made {len(recommendations)} recommendations")

        return {
            "success": True,
            "limitations": limitations,
            "warnings": warnings,
            "recommendations": recommendations,
            "metrics": metrics,
            "limitation_plots": limitation_plots,
            "data_quality": data_quality,
            "improvement_metrics": improvement_metrics
        }

    except Exception as e:
        print("\n=== Error in analyze_model_limitations ===")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Error analyzing model limitations: {str(e)}"
        }


def _analyze_data_size(X_train: pd.DataFrame, y_train: pd.Series, limitations: List, recommendations: List, metrics: Dict) -> Dict:
    """Analyze data size and provide recommendations."""
    print("\nAnalyzing data size...")
    n_samples = len(X_train)
    n_features = X_train.shape[1]

    print(f"- Number of samples: {n_samples}")
    print(f"- Number of features: {n_features}")

    size_metrics = {
        "Sample Size": n_samples,
        "Feature Count": n_features
    }

    size_limitations = []
    size_recommendations = []

    if n_samples < 1000:
        size_limitations.append(
            f"Small dataset size ({n_samples} samples) may limit model generalisation. "
            f"Current size is {n_samples} samples with {n_features} features. "
            "Generally, more samples are needed for reliable model performance."
        )
        size_recommendations.append(
            f"Consider collecting more training data. Current size: {n_samples} samples. "
            "Recommended minimum: 1000 samples for basic modeling, "
            "more for complex problems or high-dimensional data."
        )

    return {
        "limitations": size_limitations,
        "recommendations": size_recommendations,
        "metrics": size_metrics
    }


def _analyze_feature_correlations(X_train: pd.DataFrame, warnings: List, recommendations: List, metrics: Dict, plots: Dict) -> Dict:
    """Analyze feature correlations and detect multicollinearity."""
    print("\nAnalyzing feature correlations...")
    numeric_features = X_train.select_dtypes(include=[np.number]).columns
    print(f"- Number of numeric features: {len(numeric_features)}")

    corr_warnings = []
    corr_recommendations = []
    corr_metrics = {}
    corr_plots = {}

    if len(numeric_features) > 1:
        # Correlation analysis
        corr_df = X_train[numeric_features].corr()
        print("- Correlation matrix calculated successfully")

        try:
            # Create correlation heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns,
                y=corr_df.columns,
                colorscale='RdBu',
                zmid=0,
                text=np.round(corr_df.values, 2),
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False,
            ))

            fig.update_layout(
                title='Feature Correlation Heatmap',
                xaxis_title="Features",
                yaxis_title="Features",
                width=600,
                height=600
            )

            corr_plots["correlation_heatmap"] = fig
            print("- Correlation heatmap created successfully")

            # Check for high correlations with more detailed analysis
            high_corr_mask = np.abs(corr_df.values) > 0.8
            np.fill_diagonal(high_corr_mask, False)
            if high_corr_mask.any():
                correlations = []
                rows, cols = np.where(high_corr_mask)
                for i, j in zip(rows, cols):
                    correlations.append({
                        'feature1': corr_df.columns[i],
                        'feature2': corr_df.columns[j],
                        'correlation': float(corr_df.values[i, j])
                    })

                # Add detailed warning and recommendation
                corr_details = "\n".join([
                    f"- {c['feature1']} & {c['feature2']} (correlation: {c['correlation']:.2f})"
                    for c in correlations
                ])
                corr_warnings.append(
                    f"High correlation detected between features:\n{corr_details}\n"
                    "High correlation can lead to multicollinearity issues and reduced model interpretability."
                )
                corr_recommendations.append(
                    "Consider feature reduction strategies for highly correlated pairs:\n"
                    f"{corr_details}\n"
                    "Options:\n"
                    "1. Keep the feature with higher importance score\n"
                    "2. Create a new combined feature"
                )
                corr_metrics["correlations"] = correlations
                print(f"- Found {len(correlations)} highly correlated feature pairs")
        except Exception as e:
            print(f"Error in correlation analysis: {str(e)}")

    return {
        "warnings": corr_warnings,
        "recommendations": corr_recommendations,
        "metrics": corr_metrics,
        "plots": corr_plots
    }


def _analyze_class_distribution(y_train: pd.Series, warnings: List, recommendations: List, metrics: Dict, plots: Dict) -> Dict:
    """Analyze class distribution for classification problems."""
    print("\nAnalyzing class distribution...")

    class_warnings = []
    class_recommendations = []
    class_metrics = {}
    class_plots = {}

    class_counts = pd.Series(y_train).value_counts()
    imbalance_ratio = class_counts.max() / class_counts.min()
    class_metrics["Class Imbalance Ratio"] = imbalance_ratio
    print(f"- Class imbalance ratio: {imbalance_ratio:.2f}")

    try:
        # Create class distribution plot
        fig = go.Figure(data=go.Bar(
            x=class_counts.index.astype(str),
            y=class_counts.values,
            text=class_counts.values,
            textposition='auto',
        ))

        fig.update_layout(
            title='Class Distribution',
            xaxis_title='Class',
            yaxis_title='Count',
            showlegend=False
        )

        class_plots["class_distribution"] = fig
        print("- Class distribution plot created successfully")

        if imbalance_ratio > 3:
            class_details = "\n".join([
                f"- Class {cls}: {count} samples ({count/len(y_train)*100:.1f}%)"
                for cls, count in class_counts.items()
            ])
            class_warnings.append(
                f"Class imbalance detected (ratio: {imbalance_ratio:.2f})\n"
                f"Class distribution:\n{class_details}"
            )
            class_recommendations.append(
                f"Address class imbalance (ratio: {imbalance_ratio:.2f}):\n"
                "1. Apply SMOTE or other resampling techniques\n"
                "2. Collect more data for minority classes\n"
                f"Current distribution:\n{class_details}"
            )
    except Exception as e:
        print(f"Error creating class distribution analysis: {str(e)}")

    return {
        "warnings": class_warnings,
        "recommendations": class_recommendations,
        "metrics": class_metrics,
        "plots": class_plots
    }


def _analyze_feature_importance(model_dict: Dict, X_train: pd.DataFrame, y_train: pd.Series,
                               problem_type: str, warnings: List, recommendations: List, plots: Dict) -> Dict:
    """Analyze feature importance and identify low-impact features."""
    print("\nAnalyzing feature importance...")

    importance_warnings = []
    importance_recommendations = []
    importance_plots = {}

    # Create processed copies of the data for feature importance
    X_train_processed = X_train.copy()
    y_train_processed = y_train.copy()

    # Process each column based on its content
    for col in X_train_processed.columns:
        column_data = X_train_processed[col]

        # Try to convert to numeric first
        try:
            numeric_data = pd.to_numeric(column_data, errors='raise')
            X_train_processed[col] = numeric_data
            continue
        except (ValueError, TypeError):
            pass

        # If not numeric, handle categorical data
        unique_values = column_data.nunique()
        if unique_values <= 10:  # Threshold for categorical
            X_train_processed[col] = pd.Categorical(column_data).codes
        else:
            # For high cardinality strings, use hash encoding
            X_train_processed[col] = pd.util.hash_array(column_data.fillna(''), num_items=100)

    # Get feature importance based on context
    if model_dict is None or "model" not in model_dict:
        # For feature selection, use random forest
        temp_model = (RandomForestClassifier if problem_type in ["classification", "binary_classification", "multiclass_classification"]
                      else RandomForestRegressor)(n_estimators=100, random_state=42)
        temp_model.fit(X_train_processed, y_train_processed)
        importance_scores = temp_model.feature_importances_
    else:
        # Use the trained model if available
        model_instance = model_dict["model"]
        if hasattr(model_instance, "feature_importances_"):
            # Special handling for LightGBM and XGBoost models
            model_type = str(type(model_instance)).lower()
            if 'lightgbm' in model_type:
                importance_scores = model_instance.booster_.feature_importance(importance_type='gain')
                # Normalize the scores
                importance_scores = importance_scores / np.sum(importance_scores) if np.sum(importance_scores) > 0 else importance_scores
            elif 'xgboost' in model_type:
                # Get feature importance using feature names
                importance_dict = model_instance.get_booster().get_score(importance_type='gain')
                # Map importance scores to features, default to 0 if not found
                importance_scores = np.array([importance_dict.get(feat, 0.0) for feat in X_train.columns])
                # Normalize the scores
                importance_scores = importance_scores / np.sum(importance_scores) if np.sum(importance_scores) > 0 else importance_scores
            else:
                importance_scores = model_instance.feature_importances_
        elif hasattr(model_instance, "coef_"):
            importance_scores = np.abs(model_instance.coef_[0] if len(model_instance.coef_.shape) > 1
                                    else model_instance.coef_)
        else:
            # Fallback to random forest if model doesn't provide importance
            temp_model = (RandomForestClassifier if problem_type in ["classification", "binary_classification", "multiclass_classification"]
                         else RandomForestRegressor)(n_estimators=100, random_state=42)
            temp_model.fit(X_train_processed, y_train_processed)
            importance_scores = temp_model.feature_importances_

    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': importance_scores
    }).sort_values('importance', ascending=False)

    print("- Feature importance calculated successfully")
    print(f"- Top 5 important features: {', '.join(feature_importance['feature'].head().tolist())}")

    # Create feature importance plot
    fig = go.Figure(data=go.Bar(
        x=feature_importance['feature'],
        y=feature_importance['importance'],
        text=np.round(feature_importance['importance'], 4),
        textposition='auto',
    ))

    fig.update_layout(
        title='Feature Importance',
        xaxis_title='Features',
        yaxis_title='Importance',
        showlegend=False
    )

    importance_plots["feature_importance"] = fig
    print("- Feature importance plot created successfully")

    # Identify low importance features
    threshold = 0.01
    low_importance_features = feature_importance[feature_importance['importance'] <= threshold]

    if not low_importance_features.empty:
        low_imp_details = "\n".join([
            f"- {row['feature']} (importance: {row['importance']:.4f})"
            for _, row in low_importance_features.iterrows()
        ])
        importance_warnings.append(
            f"Low importance features detected (threshold: {threshold:.4f}):\n"
            f"{low_imp_details}"
        )
        importance_recommendations.append(
            "Consider removing or combining low importance features:\n"
            f"{low_imp_details}\n"
            "Options:\n"
            "1. Remove features with very low importance\n"
            "2. Combine related low-importance features\n"
            "3. Investigate if these features have indirect importance"
        )
        print(f"- Found {len(low_importance_features)} low importance features")

    return {
        "warnings": importance_warnings,
        "recommendations": importance_recommendations,
        "plots": importance_plots
    }


def _analyze_model_complexity(model_instance, X_train: pd.DataFrame, warnings: List, recommendations: List) -> Dict:
    """Analyze model complexity and risk of overfitting."""
    print("\nAnalyzing model complexity...")

    complexity_warnings = []
    complexity_recommendations = []
    n_samples = len(X_train)

    if hasattr(model_instance, "n_features_in_"):
        feature_ratio = model_instance.n_features_in_ / n_samples
        print(f"- Feature to sample ratio: {feature_ratio:.3f}")
        if feature_ratio > 0.1:
            complexity_warnings.append(
                f"High feature-to-sample ratio: {feature_ratio:.2f}\n"
                f"Current: {model_instance.n_features_in_} features, {n_samples} samples\n"
                "This may lead to overfitting."
            )
            complexity_recommendations.append(
                "Reduce feature-to-sample ratio:\n"
                "1. Collect more training data\n"
                "2. Use feature selection methods\n"
                f"Target ratio should be < 0.1 (currently {feature_ratio:.2f})"
            )

    return {
        "warnings": complexity_warnings,
        "recommendations": complexity_recommendations
    }


def _analyze_data_quality(X_train: pd.DataFrame, warnings: List, recommendations: List, data_quality: Dict) -> Dict:
    """Analyze data quality metrics for each feature."""
    print("\nAnalyzing data quality...")

    quality_warnings = []
    quality_recommendations = []
    quality_metrics = {}

    for col in X_train.columns:
        try:
            missing_pct = X_train[col].isnull().mean() * 100
            unique_pct = (X_train[col].nunique() / len(X_train)) * 100

            # Calculate basic metrics
            try:
                # Check for expected data type
                expected_type = X_train[col].dtype
                type_consistency = sum(isinstance(x, type(X_train[col].iloc[0]))
                                    for x in X_train[col]) / len(X_train) * 100

                # Check for values within expected range
                if np.issubdtype(expected_type, np.number):
                    q1, q3 = X_train[col].quantile([0.25, 0.75])
                    iqr = q3 - q1
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    range_consistency = sum((X_train[col] >= lower_bound) &
                                         (X_train[col] <= upper_bound)) / len(X_train) * 100
                else:
                    range_consistency = 100  # For non-numeric columns

                consistency_score = (type_consistency + range_consistency) / 2
            except Exception:
                consistency_score = 0
                print(f"- Error calculating consistency score for {col}")

            # Calculate validity score
            try:
                if np.issubdtype(expected_type, np.number):
                    # Check for numeric validity
                    validity_score = sum(~np.isnan(X_train[col].astype(float))) / len(X_train) * 100
                else:
                    # For categorical/string columns, check for empty strings and whitespace
                    validity_score = sum(X_train[col].astype(str).str.strip() != '') / len(X_train) * 100
            except Exception:
                validity_score = 0
                print(f"- Error calculating validity score for {col}")

            # Calculate completeness score
            completeness_score = 100 - missing_pct

            # Calculate overall quality score with weighted components
            quality_score = (
                0.4 * completeness_score +  # Completeness is most important
                0.3 * consistency_score +   # Consistency is second
                0.3 * validity_score        # Validity is third
            )

            quality_metrics[col] = {
                "Quality Score": float(quality_score),
                "Completeness": float(completeness_score),
                "Consistency": float(consistency_score),
                "Validity": float(validity_score),
                "Missing Values (%)": float(missing_pct),
                "Unique Values (%)": float(unique_pct)
            }

            # Add warnings for low quality scores
            if quality_score < 70:
                quality_warnings.append(f"Low data quality score for feature '{col}' ({quality_score:.1f}%)")
                quality_recommendations.append(
                    f"Improve data quality for feature '{col}':\n"
                    f"- Completeness: {completeness_score:.1f}%\n"
                    f"- Consistency: {consistency_score:.1f}%\n"
                    f"- Validity: {validity_score:.1f}%"
                )
        except Exception as e:
            print(f"- Error analyzing quality for column {col}: {str(e)}")

    return {
        "warnings": quality_warnings,
        "recommendations": quality_recommendations,
        "data_quality": quality_metrics
    }
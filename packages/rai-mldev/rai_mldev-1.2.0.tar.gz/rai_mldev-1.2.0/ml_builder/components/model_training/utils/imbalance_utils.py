"""Pure utility functions for class imbalance analysis and handling."""

import pandas as pd
import numpy as np
from typing import Dict, Any
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler


def analyse_class_imbalance(X_train: pd.DataFrame, y_train: pd.Series) -> Dict[str, Any]:
    """
    Analyse class imbalance in the target variable and provide recommendations.

    Args:
        X_train: Training features DataFrame
        y_train: Training target Series

    Returns:
        Dict containing analysis results, metrics, and recommendations
    """
    if X_train is None or y_train is None:
        return {
            "success": False,
            "message": "No training data available"
        }

    try:
        # Calculate class distribution
        class_dist = pd.Series(y_train).value_counts()
        imbalance_ratio = float(class_dist.max() / class_dist.min())

        # Convert class distribution to native Python types
        class_dist_dict = {
            str(k): int(v) for k, v in class_dist.to_dict().items()
        }

        # Determine imbalance severity
        if imbalance_ratio > 10:
            severity = "Severe"
            recommendations = [
                "Consider using SMOTE or other advanced resampling techniques",
                "Evaluate model performance using metrics like F1-score or AUC-ROC",
                "Consider collecting more data for minority classes"
            ]
        elif imbalance_ratio > 3:
            severity = "Moderate"
            recommendations = [
                "Consider using random oversampling or undersampling",
                "Monitor model performance on minority classes",
                "Use stratified sampling in cross-validation"
            ]
        else:
            severity = "Mild or None"
            recommendations = [
                "Standard modeling approaches should work well",
                "Still monitor performance across all classes"
            ]

        return {
            "success": True,
            "metrics": {
                "class_distribution": class_dist_dict,
                "imbalance_ratio": imbalance_ratio,
                "severity": severity,
                "majority_class": {
                    "label": str(class_dist.index[0]),
                    "count": int(class_dist.max())
                },
                "minority_class": {
                    "label": str(class_dist.index[-1]),
                    "count": int(class_dist.min())
                }
            },
            "recommendations": recommendations
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error analyzing class imbalance: {str(e)}"
        }


def get_imbalance_recommendation(X_train: pd.DataFrame, y_train: pd.Series) -> Dict[str, Any]:
    """
    Analyse dataset characteristics to recommend the best resampling method.

    Args:
        X_train: Training features DataFrame
        y_train: Training target Series

    Returns:
        Dict containing recommended method and explanation
    """
    if X_train is None or y_train is None:
        return {
            "success": False,
            "message": "No training data available"
        }

    try:
        # Get basic dataset characteristics
        n_samples = len(X_train)
        n_features = len(X_train.columns)
        class_dist = pd.Series(y_train).value_counts()
        min_class_size = class_dist.min()
        imbalance_ratio = class_dist.max() / min_class_size

        # Calculate feature characteristics
        numerical_features = X_train.select_dtypes(include=[np.number]).columns
        categorical_features = X_train.select_dtypes(exclude=[np.number]).columns
        n_numerical = len(numerical_features)
        n_categorical = len(categorical_features)

        # Initialize recommendation variables
        recommended_method = None
        explanation = None
        considerations = []

        # Decision logic for recommendation
        if imbalance_ratio <= 3:
            recommended_method = "None (Original Data)"
            explanation = """
                Your dataset has only mild class imbalance. The imbalance ratio of {:.2f} is
                generally manageable without special techniques. The model should be able to
                learn from the original data effectively.
            """.format(imbalance_ratio)

        elif min_class_size < 6:
            recommended_method = "Random Oversampling"
            explanation = """
                Your minority class has very few samples ({} instances). In this case,
                SMOTE and ADASYN might not work well because they need at least 6 samples
                to generate synthetic examples. Random oversampling is safer as it just
                duplicates existing samples.
            """.format(min_class_size)

        elif n_categorical > n_numerical:
            recommended_method = "Random Oversampling"
            explanation = """
                Your dataset has more categorical features ({}) than numerical features ({}).
                SMOTE and ADASYN work better with numerical features because they create synthetic
                samples by interpolation. Random oversampling is more appropriate for
                categorical-heavy datasets.
            """.format(n_categorical, n_numerical)

        elif n_samples > 10000 and imbalance_ratio > 10:
            recommended_method = "Random Undersampling"
            explanation = """
                You have a large dataset ({:,} samples) with severe imbalance (ratio: {:.2f}).
                Random undersampling can help by:
                1. Reducing training time
                2. Balancing class distribution
                3. Avoiding memory issues with synthetic sampling
            """.format(n_samples, imbalance_ratio)

        else:
            recommended_method = "SMOTE"
            explanation = """
                Based on your dataset characteristics:
                - Moderate to high imbalance (ratio: {:.2f})
                - Sufficient samples in minority class ({} instances)
                - More numerical ({}) than categorical ({}) features

                SMOTE is recommended because it can create synthetic samples that help the
                model learn decision boundaries better than simple oversampling.
            """.format(imbalance_ratio, min_class_size, n_numerical, n_categorical)

        # Add method-specific considerations
        if recommended_method == "SMOTE":
            considerations = [
                "Ensure your features are properly scaled before applying SMOTE",
                "Consider removing outliers as they can affect synthetic sample generation",
                "Monitor for overfitting as synthetic samples might make the model too specific"
            ]
        elif recommended_method == "Random Undersampling":
            considerations = [
                "Check if important information is being lost from majority class",
                "Consider using multiple rounds of undersampling and averaging results",
                "Validate model on the original class distribution"
            ]
        elif recommended_method == "Random Oversampling":
            considerations = [
                "Watch for overfitting as samples are exactly duplicated",
                "Consider using class weights as an alternative",
                "Validate model performance on non-duplicated test data"
            ]

        return {
            "success": True,
            "recommended_method": recommended_method,
            "explanation": explanation.strip(),
            "considerations": considerations,
            "metrics": {
                "imbalance_ratio": float(imbalance_ratio),
                "min_class_size": int(min_class_size),
                "total_samples": int(n_samples),
                "numerical_features": int(n_numerical),
                "categorical_features": int(n_categorical)
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating recommendation: {str(e)}"
        }


def apply_resampling(X_train: pd.DataFrame, y_train: pd.Series, method: str) -> Dict[str, Any]:
    """
    Apply the specified resampling method to handle class imbalance.

    Args:
        X_train: Training features DataFrame
        y_train: Training target Series
        method: The resampling method to use ('oversampling', 'undersampling', or 'smote')

    Returns:
        Dict containing success status, resampled data, and resampling results
    """
    if X_train is None or y_train is None:
        return {
            "success": False,
            "message": "No training data available"
        }

    try:
        # Store original distribution
        original_dist = pd.Series(y_train).value_counts()

        # Apply resampling
        if method == "oversampling":
            resampler = RandomOverSampler(random_state=42)
        elif method == "undersampling":
            resampler = RandomUnderSampler(random_state=42)
        elif method == "smote":
            resampler = SMOTE(random_state=42)
        else:
            return {
                "success": False,
                "message": f"Unknown resampling method: {method}"
            }

        # Perform resampling
        X_resampled, y_resampled = resampler.fit_resample(X_train, y_train)

        # Calculate new distribution
        new_dist = pd.Series(y_resampled).value_counts()

        # Convert distributions to native Python types
        original_dist_dict = {str(k): int(v) for k, v in original_dist.to_dict().items()}
        new_dist_dict = {str(k): int(v) for k, v in new_dist.to_dict().items()}

        return {
            "success": True,
            "message": "Resampling applied successfully",
            "X_resampled": X_resampled,
            "y_resampled": y_resampled,
            "results": {
                "original_distribution": original_dist_dict,
                "new_distribution": new_dist_dict,
                "original_samples": int(len(y_train)),
                "new_samples": int(len(y_resampled)),
                "original_ratio": float(original_dist.max() / original_dist.min()),
                "new_ratio": float(new_dist.max() / new_dist.min())
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error applying resampling: {str(e)}"
        }
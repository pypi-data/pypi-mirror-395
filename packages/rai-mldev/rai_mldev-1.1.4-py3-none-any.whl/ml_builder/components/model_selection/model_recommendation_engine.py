"""
Model recommendation engine for ML Builder.

Contains sophisticated logic to recommend appropriate machine learning models
based on dataset characteristics, problem type, and other factors.
"""

import pandas as pd
from datetime import datetime
from .utils.nonlinearity_detection import detect_nonlinearity
from .utils.compatibility_utils import check_xgboost_compatibility


def get_dataset_characteristics(data, target_column):
    """
    Analyze dataset characteristics for model recommendation.

    Args:
        data: DataFrame containing the data
        target_column: Name of the target column

    Returns:
        dict: Dictionary containing dataset characteristics
    """
    n_samples = len(data)
    n_features = len(data.columns) - 1  # Excluding target variable

    characteristics = {
        "samples": n_samples,
        "features": n_features,
        "categorical_features": len(data.select_dtypes(include=['object']).columns),
        "numerical_features": len(data.select_dtypes(include=['float64', 'int64']).columns),
        "missing_values": data.isnull().sum().sum(),
        "data_types": data.dtypes.astype(str).to_dict(),
        "memory_usage": data.memory_usage(deep=True).sum(),
        "timestamp": str(datetime.now())
    }

    return characteristics


def analyze_target_skewness(data, target_column, problem_type):
    """
    Analyze target variable skewness for regression problems.

    Args:
        data: DataFrame containing the data
        target_column: Name of the target column
        problem_type: Type of ML problem

    Returns:
        tuple: (is_skewed, skewness_value)
    """
    if problem_type == "regression" and target_column:
        skewness = data[target_column].skew()
        is_skewed = abs(skewness) > 1.0  # Common threshold for significant skewness
        return is_skewed, skewness
    return False, 0.0


def determine_data_complexity(n_features):
    """
    Determine data complexity level based on number of features.

    Args:
        n_features: Number of features in the dataset

    Returns:
        str: Complexity level ('low', 'medium', 'high')
    """
    if n_features > 10:
        return "high"
    elif n_features > 5:
        return "medium"
    else:
        return "low"


def recommend_model_for_classification(data, target_column, problem_type, xgboost_compatible,
                                     n_samples, n_features, data_complexity, has_sufficient_data,
                                     categorical_features):
    """
    Recommend model for classification problems.

    Args:
        data: DataFrame containing the data
        target_column: Name of the target column
        problem_type: Type of classification problem
        xgboost_compatible: Whether XGBoost is compatible
        n_samples: Number of samples
        n_features: Number of features
        data_complexity: Data complexity level
        has_sufficient_data: Whether there's sufficient data for complex models
        categorical_features: Number of categorical features

    Returns:
        tuple: (recommended_model, recommendation_reasons)
    """
    recommendation_reason = []

    if n_samples < 1000:
        if n_features < 10:
            # Test for non-linearity
            is_nonlinear = detect_nonlinearity(data, target_column, problem_type)
            if is_nonlinear:
                if n_features < 5:  # For very simple non-linear problems with few features
                    recommended_model = "decision_tree"
                    recommendation_reason.append("Non-linear relationships detected with few features - Decision Tree provides good interpretability")
                else:
                    recommended_model = "random_forest"
                    recommendation_reason.append("Non-linear relationships detected - Random Forest handles non-linearity well")
            else:
                # For small datasets with linear relationships, prefer Naive Bayes for speed
                if n_samples < 500 and n_features < 5:
                    recommended_model = "naive_bayes"
                    recommendation_reason.append("Very small dataset with linear relationships - Naive Bayes provides extremely fast training and good probabilistic predictions")
                else:
                    recommended_model = "logistic_regression"
                    recommendation_reason.append("Linear relationships detected - simpler logistic regression model should be sufficient")
        else:
            # For small datasets with many features, random forest handles high dimensionality well
            recommended_model = "random_forest"
            recommendation_reason.append("Small dataset with many features - Random Forest handles high dimensionality well")
    else:
        if data_complexity == "high" and has_sufficient_data:
            if n_samples >= 50000 or (n_features > 1000 and n_samples >= 10000):
                # For very large datasets or high-dimensional data, LightGBM is optimal
                recommended_model = "lightgbm"
                recommendation_reason.append("Very large dataset or high-dimensional data - LightGBM provides excellent performance with lower memory usage and faster training")
            elif n_samples >= 10000:
                # For very large, complex datasets, XGBoost often performs best (if compatible)
                if xgboost_compatible:
                    recommended_model = "xgboost"
                    recommendation_reason.append("Large complex dataset - XGBoost typically provides best-in-class performance with excellent speed")
                else:
                    recommended_model = "lightgbm"
                    recommendation_reason.append("Large complex dataset - LightGBM provides excellent performance (XGBoost unavailable due to class labeling)")
            elif n_samples >= 5000:
                # For large, complex datasets with sufficient samples, consider CatBoost or MLP
                if n_samples >= 10000 and data_complexity == "high":
                    # For very large, very complex datasets, MLP can learn intricate patterns
                    recommended_model = "mlp"
                    recommendation_reason.append("Very large complex dataset with sufficient samples - MLP can learn intricate non-linear patterns effectively")
                else:
                    # CatBoost is preferred when robustness to overfitting is important
                    recommended_model = "catboost"
                    recommendation_reason.append("Large complex dataset - CatBoost provides state-of-the-art performance with superior overfitting resistance")
            else:
                # For moderately large complex datasets, histogram-based gradient boosting often performs best
                recommended_model = "hist_gradient_boosting"
                recommendation_reason.append("Moderately large complex dataset - Histogram-based Gradient Boosting provides excellent accuracy with faster training than standard Gradient Boosting")
        else:
            # For large datasets with moderate complexity, random forest is a good balance
            recommended_model = "random_forest"
            recommendation_reason.append("Large dataset with moderate complexity - Random Forest provides good balance of accuracy and training time")

    return recommended_model, recommendation_reason


def recommend_model_for_regression(data, target_column, problem_type, xgboost_compatible,
                                 n_samples, n_features, data_complexity, has_sufficient_data,
                                 target_skewed, skewness_value, categorical_features):
    """
    Recommend model for regression problems.

    Args:
        data: DataFrame containing the data
        target_column: Name of the target column
        problem_type: Type of regression problem
        xgboost_compatible: Whether XGBoost is compatible
        n_samples: Number of samples
        n_features: Number of features
        data_complexity: Data complexity level
        has_sufficient_data: Whether there's sufficient data for complex models
        target_skewed: Whether target variable is skewed
        skewness_value: Actual skewness value
        categorical_features: Number of categorical features

    Returns:
        tuple: (recommended_model, recommendation_reasons)
    """
    recommendation_reason = []

    if target_skewed:
        # For skewed targets, recommend XGBoost, LightGBM, or random forest
        if n_samples >= 50000 or (n_features > 1000 and n_samples >= 10000):
            recommended_model = "lightgbm"
            recommendation_reason.append("Large skewed dataset - LightGBM handles non-normal distributions well with excellent efficiency")
        elif n_samples >= 5000 or data_complexity == "high":
            if xgboost_compatible:
                recommended_model = "xgboost"
                recommendation_reason.append("Skewed target with large/complex dataset - XGBoost handles non-normal distributions exceptionally well")
            else:
                recommended_model = "lightgbm"
                recommendation_reason.append("Skewed target with large/complex dataset - LightGBM handles non-normal distributions well (XGBoost unavailable due to class labeling)")
        else:
            recommended_model = "random_forest"
            recommendation_reason.append("Skewed target - Random Forest is robust to non-normal distributions")
    else:
        if n_samples < 1000:
            if data_complexity == "low":
                # Test for non-linearity
                is_nonlinear = detect_nonlinearity(data, target_column, problem_type)
                if is_nonlinear:
                    if n_features < 5:  # For very simple non-linear problems with few features
                        recommended_model = "decision_tree"
                        recommendation_reason.append("Non-linear relationships detected with few features - Decision Tree provides good interpretability")
                    else:
                        recommended_model = "random_forest"
                        recommendation_reason.append("Non-linear relationships detected - Random Forest handles non-linearity well")
                else:
                    # For small datasets with linear relationships, prefer Ridge for regularization
                    if n_samples < 500 or n_features > n_samples * 0.5:
                        recommended_model = "ridge_regression"
                        recommendation_reason.append("Small dataset with linear relationships and/or many features - Ridge Regression provides regularization to prevent overfitting")
                    else:
                        recommended_model = "linear_regression"
                        recommendation_reason.append("Linear relationships detected - simpler linear regression model should be sufficient")
            else:
                # For small complex datasets, random forest handles non-linearity well
                recommended_model = "random_forest"
                recommendation_reason.append("Small complex dataset - Random Forest handles non-linear relationships well")
        else:
            if data_complexity == "high" and has_sufficient_data:
                if n_samples >= 50000 or (n_features > 1000 and n_samples >= 10000):
                    # For very large datasets or high-dimensional data, LightGBM is optimal
                    recommended_model = "lightgbm"
                    recommendation_reason.append("Very large dataset or high-dimensional data - LightGBM provides superior performance with lower memory usage")
                elif n_samples >= 10000:
                    # For very large, complex datasets, XGBoost often performs best (if compatible)
                    if xgboost_compatible:
                        recommended_model = "xgboost"
                        recommendation_reason.append("Large complex dataset - XGBoost provides superior performance with excellent speed")
                    else:
                        recommended_model = "lightgbm"
                        recommendation_reason.append("Large complex dataset - LightGBM provides superior performance (XGBoost unavailable due to class labeling)")
                elif n_samples >= 5000:
                    # For large, complex datasets with sufficient samples, consider CatBoost or MLP
                    if n_samples >= 10000 and data_complexity == "high":
                        # For very large, very complex datasets, MLP can learn intricate patterns
                        recommended_model = "mlp"
                        recommendation_reason.append("Very large complex dataset with sufficient samples - MLP can learn complex non-linear patterns")
                    else:
                        # CatBoost is preferred when robustness to overfitting is important
                        recommended_model = "catboost"
                        recommendation_reason.append("Large complex dataset - CatBoost provides state-of-the-art performance with superior overfitting resistance")
                else:
                    # For moderately large complex datasets, histogram-based gradient boosting often performs best
                    recommended_model = "hist_gradient_boosting"
                    recommendation_reason.append("Moderately large complex dataset - Histogram-based Gradient Boosting provides excellent accuracy with faster training than standard Gradient Boosting")
            else:
                # For large datasets with moderate complexity, random forest is a good balance
                recommended_model = "random_forest"
                recommendation_reason.append("Large dataset with moderate complexity - Random Forest provides good balance of accuracy and training time")

    return recommended_model, recommendation_reason


def add_contextual_recommendations(recommendation_reason, n_samples, n_features,
                                 categorical_features, missing_values, recommended_model):
    """
    Add contextual recommendations based on data characteristics.

    Args:
        recommendation_reason: List of current recommendation reasons
        n_samples: Number of samples
        n_features: Number of features
        categorical_features: Number of categorical features
        missing_values: Number of missing values
        recommended_model: Currently recommended model

    Returns:
        list: Updated recommendation reasons
    """
    # Check for potential computational constraints
    if n_samples * n_features > 1000000:  # Large computational load
        recommendation_reason.append("Note: Dataset is large - consider computational resources and training time")

    # Add warning for deep learning models if data might be insufficient
    if recommended_model == "mlp" and n_samples < 5000:
        recommendation_reason.append("Warning: While MLP is recommended, more training data would be beneficial for optimal performance")

    # Add note about CatBoost requiring Optuna
    if recommended_model == "catboost":
        recommendation_reason.append("⚠️ Note: CatBoost requires Optuna optimization (Random Search not supported)")

    # Suggest CatBoost as alternative for complex datasets when not already recommended
    if n_samples >= 5000 and n_features > 10 and recommended_model not in ["catboost"]:
        recommendation_reason.append("💡 Alternative suggestion: CatBoost offers superior overfitting resistance and state-of-the-art performance for complex datasets")

    # Suggest Naive Bayes as fast baseline for small datasets (classification only)
    if n_samples < 1000 and recommended_model not in ["naive_bayes", "logistic_regression", "linear_regression", "ridge_regression"]:
        recommendation_reason.append("💡 Alternative suggestion: Naive Bayes (classification) provides extremely fast baseline for comparison on small datasets")

    # Suggest Ridge Regression when Linear Regression is recommended and multicollinearity might be an issue
    if recommended_model == "linear_regression" and n_features > 5:
        recommendation_reason.append("💡 Alternative suggestion: Ridge Regression adds regularization to prevent overfitting, especially useful if features are correlated")

    return recommendation_reason


def get_model_recommendation(training_data, target_column, problem_type):
    """
    Get comprehensive model recommendation based on dataset characteristics.

    Args:
        training_data: DataFrame containing the training data
        target_column: Name of the target column
        problem_type: Type of ML problem

    Returns:
        dict: Dictionary containing recommendation details
    """
    # Get dataset characteristics
    characteristics = get_dataset_characteristics(training_data, target_column)
    n_samples = characteristics["samples"]
    n_features = characteristics["features"]
    categorical_features = characteristics["categorical_features"]
    missing_values = characteristics["missing_values"]

    # Determine data complexity and other factors
    data_complexity = determine_data_complexity(n_features)
    has_sufficient_data = n_samples >= 1000

    # Check XGBoost compatibility
    xgboost_compatible = check_xgboost_compatibility(training_data, target_column, problem_type)

    # Analyze target skewness for regression
    target_skewed, skewness_value = analyze_target_skewness(training_data, target_column, problem_type)

    # Get model recommendation based on problem type
    if problem_type in ["classification", "binary_classification", "multiclass_classification"]:
        recommended_model, recommendation_reason = recommend_model_for_classification(
            training_data, target_column, problem_type, xgboost_compatible,
            n_samples, n_features, data_complexity, has_sufficient_data,
            categorical_features
        )
    else:  # regression
        recommended_model, recommendation_reason = recommend_model_for_regression(
            training_data, target_column, problem_type, xgboost_compatible,
            n_samples, n_features, data_complexity, has_sufficient_data,
            target_skewed, skewness_value, categorical_features
        )

    # Add contextual recommendations
    recommendation_reason = add_contextual_recommendations(
        recommendation_reason, n_samples, n_features, categorical_features,
        missing_values, recommended_model
    )

    return {
        "recommended_model": recommended_model,
        "reasons": recommendation_reason,
        "problem_type": problem_type,
        "dataset_characteristics": characteristics,
        "xgboost_compatible": xgboost_compatible,
        "target_skewed": target_skewed,
        "skewness_value": skewness_value if target_skewed else None,
        "timestamp": str(datetime.now())
    }
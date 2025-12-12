"""
Model options and configurations for model selection.

Contains model definitions, options, and configurations used throughout
the model selection process.
"""


def get_model_options(problem_type, xgboost_compatible=True):
    """
    Get available model options based on problem type and compatibility.

    Args:
        problem_type: Type of ML problem
        xgboost_compatible: Whether XGBoost is compatible with the dataset

    Returns:
        dict: Dictionary mapping model keys to display names
    """
    # Handle both binary and multiclass classification
    if problem_type in ["classification", "binary_classification", "multiclass_classification"]:
        model_options = {
            "logistic_regression": "Logistic Regression",
            "naive_bayes": "Naive Bayes",
            "decision_tree": "Decision Tree",
            "random_forest": "Random Forest",
            "mlp": "Multilayer Perceptron",
            "hist_gradient_boosting": "Histogram-based Gradient Boosting",
            "catboost": "CatBoost",
            "lightgbm": "LightGBM"
        }

        # Add XGBoost only if it's compatible
        if xgboost_compatible:
            model_options["xgboost"] = "XGBoost"

    elif problem_type == "regression":
        model_options = {
            "linear_regression": "Linear Regression",
            "ridge_regression": "Ridge Regression",
            "decision_tree": "Decision Tree",
            "random_forest": "Random Forest",
            "mlp": "Multilayer Perceptron",
            "hist_gradient_boosting": "Histogram-based Gradient Boosting",
            "catboost": "CatBoost",
            "lightgbm": "LightGBM"
        }

        # Add XGBoost (always compatible for regression)
        if xgboost_compatible:
            model_options["xgboost"] = "XGBoost"
    else:
        model_options = {}

    return model_options


def get_problem_type_display(problem_type):
    """
    Get user-friendly display name for problem type.

    Args:
        problem_type: Internal problem type string

    Returns:
        str: User-friendly display name
    """
    problem_type_display = {
        "binary_classification": "Binary Classification",
        "multiclass_classification": "Multiclass Classification",
        "classification": "Classification",
        "regression": "Regression"
    }
    return problem_type_display.get(problem_type, problem_type)
"""
Model Selection Content for ML Builder.

Contains detailed model explanations, comparison charts, and selection guidance
that was previously embedded in the Model Selection page.
"""

# Model characteristics and descriptions
MODEL_CHARACTERISTICS = {
    "logistic_regression": {
        "description": "A linear model for classification that estimates probabilities using a logistic function.",
        "best_for": ["Binary classification", "Simple linear relationships", "Large datasets", "When interpretability is important"],
        "limitations": ["Cannot capture non-linear relationships", "May underperform with high-dimensional data", "Assumes linearly separable classes"],
        "complexity": "Low",
        "training_speed": "Very Fast",
        "prediction_speed": "Very Fast",
        "memory_usage": "Very Low",
        "interpretability": "High"
    },
    "naive_bayes": {
        "description": "A probabilistic classifier based on Bayes' theorem with strong (naive) independence assumptions between features. **Classification only - not available for regression.**",
        "best_for": ["Small to medium datasets", "Fast training and prediction", "Probabilistic predictions", "Text classification", "When feature independence assumption is reasonable"],
        "limitations": ["Classification only (no regression support)", "Assumes feature independence", "Can be outperformed by more complex models", "Not ideal for highly correlated features"],
        "complexity": "Low",
        "training_speed": "Very Fast",
        "prediction_speed": "Very Fast",
        "memory_usage": "Very Low",
        "interpretability": "High"
    },
    "linear_regression": {
        "description": "A linear approach to modeling the relationship between a dependent variable and independent variables.",
        "best_for": ["Simple linear relationships", "When interpretability is important", "Baseline modeling", "Small to medium datasets"],
        "limitations": ["Cannot capture non-linear relationships", "Sensitive to outliers", "Assumes independent features"],
        "complexity": "Low",
        "training_speed": "Very Fast",
        "prediction_speed": "Very Fast",
        "memory_usage": "Very Low",
        "interpretability": "High"
    },
    "ridge_regression": {
        "description": "Linear regression with L2 regularization that prevents overfitting by penalizing large coefficients. **Regression only - not available for classification.**",
        "best_for": ["Correlated features (multicollinearity)", "Preventing overfitting", "When feature selection isn't needed", "Datasets with more features than samples"],
        "limitations": ["Regression only (no classification support)", "Cannot capture non-linear relationships", "Keeps all features (doesn't eliminate any)", "May underperform with truly irrelevant features"],
        "complexity": "Low",
        "training_speed": "Very Fast",
        "prediction_speed": "Very Fast",
        "memory_usage": "Very Low",
        "interpretability": "High"
    },
    "decision_tree": {
        "description": "A decision tree is a flowchart-like structure that represents decisions and their possible consequences.",
        "best_for": ["Complex relationships", "High-dimensional data", "When feature importance is needed", "Handling missing values"],
        "limitations": ["Can overfit if not properly pruned", "Less interpretable than linear models", "Can be sensitive to outliers"],
        "complexity": "Low-Medium",
        "training_speed": "Fast",
        "prediction_speed": "Very Fast",
        "memory_usage": "Low",
        "interpretability": "High"
    },
    "random_forest": {
        "description": "An ensemble learning method that operates by constructing multiple decision trees.",
        "best_for": ["Complex relationships", "High-dimensional data", "When feature importance is needed", "Handling missing values"],
        "limitations": ["Less interpretable than linear models", "Can be computationally intensive", "May overfit with very small datasets"],
        "complexity": "Medium",
        "training_speed": "Medium",
        "prediction_speed": "Fast",
        "memory_usage": "Medium",
        "interpretability": "Medium"
    },
    "mlp": {
        "description": "A deep learning model that uses multiple layers of neurons to learn complex patterns in data.",
        "best_for": ["Complex non-linear relationships", "Large datasets", "High-dimensional data", "Pattern recognition"],
        "limitations": ["Requires careful hyperparameter tuning", "May need significant training data", "Less interpretable", "Computationally intensive"],
        "complexity": "High",
        "training_speed": "Slow",
        "prediction_speed": "Fast",
        "memory_usage": "Medium",
        "interpretability": "Low"
    },
    "xgboost": {
        "description": "An ensemble technique that builds models sequentially by learning from previous model errors.",
        "best_for": ["Complex relationships", "When highest accuracy is needed", "Feature interactions", "Various data types"],
        "limitations": ["Can overfit if not properly tuned", "Computationally intensive", "Less interpretable", "Sensitive to outliers"],
        "complexity": "Medium-High",
        "training_speed": "Fast",
        "prediction_speed": "Fast",
        "memory_usage": "Medium",
        "interpretability": "Medium-Low"
    },
    "lightgbm": {
        "description": "A fast, distributed, high-performance gradient boosting framework optimized for efficiency and speed.",
        "best_for": ["Large datasets", "High-dimensional data", "When training speed is critical", "Memory-constrained environments"],
        "limitations": ["May need careful parameter tuning", "Can be sensitive to overfitting with small datasets", "Less interpretable than simpler models"],
        "complexity": "Medium-High",
        "training_speed": "Very Fast",
        "prediction_speed": "Very Fast",
        "memory_usage": "Low",
        "interpretability": "Medium-Low"
    },
    "hist_gradient_boosting": {
        "description": "A modern sklearn gradient boosting implementation using histogram-based algorithms for faster training than traditional gradient boosting.",
        "best_for": ["Medium to large datasets", "When you want sklearn's gradient boosting but faster", "Native missing value handling", "When avoiding external dependencies"],
        "limitations": ["Newer implementation (less battle-tested than XGBoost/LightGBM)", "May need parameter tuning", "Less interpretable than simpler models"],
        "complexity": "Medium-High",
        "training_speed": "Fast",
        "prediction_speed": "Fast",
        "memory_usage": "Medium",
        "interpretability": "Medium-Low"
    },
    "catboost": {
        "description": "A state-of-the-art gradient boosting library with ordered boosting algorithm and superior overfitting resistance.",
        "best_for": ["Complex datasets requiring robustness", "When overfitting is a concern", "Competition-level performance", "Excellent out-of-box performance with minimal tuning"],
        "limitations": ["Requires Optuna optimization (Random Search not supported)", "Slightly slower training than LightGBM", "Larger model size"],
        "complexity": "Medium-High",
        "training_speed": "Fast",
        "prediction_speed": "Fast",
        "memory_usage": "Medium",
        "interpretability": "Medium-Low"
    }
}

# Detailed model explanations for expandable sections
MODEL_DETAILED_EXPLANATIONS = {
    "linear_models": """
        ### Linear/Logistic Regression

        #### Key Characteristics
        - **Complexity**: Low 🟢
        - **Training Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Prediction Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Memory Usage**: Very Low 💾
        - **Interpretability**: High 🎯🎯🎯🎯🎯

        #### Perfect For
        - 📈 Baseline modeling
        - 📊 Linear relationships
        - 👥 When interpretability is crucial
        - 📦 Small to large datasets

        ⚠️ **Limitations**
        - Cannot capture non-linear relationships
        - May underperform with high-dimensional data
        - Assumes independence between features
    """,
    "ridge_regression": """
        ### Ridge Regression

        **📌 Regression Only** - Not available for classification tasks

        #### Key Characteristics
        - **Complexity**: Low 🟢
        - **Training Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Prediction Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Memory Usage**: Very Low 💾
        - **Interpretability**: High 🎯🎯🎯🎯🎯

        #### Perfect For
        - 🔗 Correlated features (multicollinearity)
        - 🛡️ Preventing overfitting in linear models
        - 📊 More features than samples
        - 📈 Improving upon Linear Regression with regularization

        ⚠️ **Limitations**
        - **Regression only** (no classification support)
        - Cannot capture non-linear relationships
        - Keeps all features (doesn't perform feature selection)
        - May underperform if many features are truly irrelevant
    """,
    "naive_bayes": """
        ### Naive Bayes

        **📌 Classification Only** - Not available for regression tasks

        #### Key Characteristics
        - **Complexity**: Low 🟢
        - **Training Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Prediction Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Memory Usage**: Very Low 💾
        - **Interpretability**: High 🎯🎯🎯🎯

        #### Perfect For
        - 📊 Small to medium datasets
        - ⚡ When speed is critical (training AND prediction)
        - 📈 Probabilistic predictions needed
        - 🎯 Baseline model for comparison
        - 📝 Text classification tasks

        ⚠️ **Limitations**
        - **Classification only** (no regression support)
        - Assumes feature independence (rarely true in practice)
        - Can be outperformed by complex models
        - Sensitive to highly correlated features
    """,
    "decision_trees": """
        ### Decision Trees

        #### Key Characteristics
        - **Complexity**: Low-Medium 🟢🟡
        - **Training Speed**: Fast ⚡⚡⚡⚡
        - **Prediction Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Memory Usage**: Low 💾
        - **Interpretability**: High 🎯🎯🎯🎯

        #### Perfect For
        - 📋 Understanding decision rules
        - 🔢 Mixed data types
        - 🔄 Feature interactions
        - ❓ Handling missing values

        ⚠️ **Limitations**
        - Can overfit if not pruned
        - May be unstable
        - Lower accuracy than ensembles
    """,
    "random_forest": """
        ### Random Forest

        #### Key Characteristics
        - **Complexity**: Medium 🟡
        - **Training Speed**: Medium ⚡⚡⚡
        - **Prediction Speed**: Fast ⚡⚡⚡⚡
        - **Memory Usage**: Medium 💾💾
        - **Interpretability**: Medium 🎯🎯🎯

        #### Perfect For
        - 📊 Non-linear relationships
        - 📈 Feature importance analysis
        - 🎯 Robust performance
        - ❓ Missing values handling

        ⚠️ **Limitations**
        - Less interpretable than single trees
        - Higher memory requirements
        - Computationally intensive for large datasets
    """,
    "mlp": """
        ### Multilayer Perceptron (MLP)

        #### Key Characteristics
        - **Complexity**: High 🔴
        - **Training Speed**: Slow ⚡⚡
        - **Prediction Speed**: Fast ⚡⚡⚡⚡
        - **Memory Usage**: Medium 💾💾
        - **Interpretability**: Low 🎯

        #### Perfect For
        - 🔄 Complex non-linear relationships
        - 📊 Large datasets
        - 🎯 Pattern recognition
        - 🔗 Complex feature interactions

        ⚠️ **Limitations**
        - Requires careful tuning
        - Needs significant training data
        - Black box model
        - Computationally intensive
    """,
    "xgboost": """
        ### XGBoost

        #### Key Characteristics
        - **Complexity**: Medium-High 🟡🔴
        - **Training Speed**: Fast ⚡⚡⚡⚡
        - **Prediction Speed**: Fast ⚡⚡⚡⚡
        - **Memory Usage**: Medium 💾💾
        - **Interpretability**: Medium-Low 🎯🎯

        #### Perfect For
        - 🏆 State-of-the-art performance
        - 📊 Large datasets
        - 🚀 Production environments
        - 📋 Structured data

        ⚠️ **Limitations**
        - Many hyperparameters
        - Can overfit on noisy data
        - Requires careful tuning
    """,
    "lightgbm": """
        ### LightGBM

        #### Key Characteristics
        - **Complexity**: Medium-High 🟡🔴
        - **Training Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Prediction Speed**: Very Fast ⚡⚡⚡⚡⚡
        - **Memory Usage**: Low 💾
        - **Interpretability**: Medium-Low 🎯🎯

        #### Perfect For
        - 📊 Very large datasets
        - ⚡ Speed-critical applications
        - 💾 Memory-constrained environments
        - 🚀 Production deployment

        ⚠️ **Limitations**
        - Careful tuning needed
        - Can overfit on small datasets
        - Not ideal for small datasets
    """,
    "hist_gradient_boosting": """
        ### Histogram-based Gradient Boosting

        #### Key Characteristics
        - **Complexity**: Medium-High 🟡🔴
        - **Training Speed**: Fast ⚡⚡⚡⚡
        - **Prediction Speed**: Fast ⚡⚡⚡⚡
        - **Memory Usage**: Medium 💾💾
        - **Interpretability**: Medium-Low 🎯🎯

        #### Perfect For
        - 📊 Medium to large datasets
        - 🔧 Pure sklearn workflows (no external deps)
        - ❓ Native missing value handling
        - ⚡ Faster than standard Gradient Boosting

        ⚠️ **Limitations**
        - Newer than XGBoost/LightGBM
        - Still needs parameter tuning
        - Less documentation than competitors
    """,
    "catboost": """
        ### CatBoost

        #### Key Characteristics
        - **Complexity**: Medium-High 🟡🔴
        - **Training Speed**: Fast ⚡⚡⚡⚡
        - **Prediction Speed**: Fast ⚡⚡⚡⚡
        - **Memory Usage**: Medium 💾💾
        - **Interpretability**: Medium-Low 🎯🎯

        #### Perfect For
        - 🎯 Competition-level accuracy
        - 🛡️ Superior overfitting resistance
        - 📊 Complex datasets with many features
        - 🚀 Excellent out-of-box performance with minimal tuning
        - 🏆 When you want state-of-the-art results

        ⚠️ **Limitations**
        - **Requires Optuna optimization** (Random Search not supported)
        - Slightly slower training than LightGBM for very large datasets
        - Larger model files than other boosting methods
    """
}

# Model comparison chart data
# This will be converted to a DataFrame for better display
MODEL_COMPARISON_CHART = {
    "Aspect": [
        "Training Speed",
        "Prediction Speed",
        "Memory Usage",
        "Interpretability",
        "Handling Non-linearity",
        "Feature Interactions",
        "Handling Missing Values",
        "Categorical Features",
        "Robustness to Overfitting"
    ],
    "Linear Models": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐", "⭐⭐⭐⭐⭐", "⭐", "⭐", "⭐", "⭐⭐", "⭐⭐⭐"],
    "Ridge Regression": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐", "⭐⭐⭐⭐⭐", "⭐", "⭐", "⭐", "⭐⭐", "⭐⭐⭐⭐"],
    "Naive Bayes": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐", "⭐⭐⭐⭐", "⭐⭐", "⭐", "⭐", "⭐⭐", "⭐⭐⭐"],
    "Decision Trees": ["⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐"],
    "Random Forest": ["⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐"],
    "MLP": ["⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐", "⭐", "⭐⭐"],
    "Histogram Gradient Boosting": ["⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐"],
    "XGBoost": ["⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐"],
    "LightGBM": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐"],
    "CatBoost": ["⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
}

# Quick selection guide
QUICK_SELECTION_GUIDE = {
    "linear_models": """
        #### Choose Linear Models when:
        - 📊 You need a simple, interpretable baseline
        - 📈 Relationships are mostly linear
        - 💻 You have limited computational resources
        - ⚡ You need very fast predictions
    """,
    "ridge_regression": """
        #### Choose Ridge Regression when:
        - 🔗 Features are correlated (multicollinearity present)
        - 🛡️ Linear Regression is overfitting
        - 📊 More features than samples
        - ⚡ You need fast training with regularization
        - 📈 Regression only (not for classification)
    """,
    "naive_bayes": """
        #### Choose Naive Bayes when:
        - ⚡ Speed is critical (fastest training AND prediction)
        - 📊 Small to medium dataset
        - 📈 Probabilistic predictions needed
        - 🎯 Fast baseline model for comparison
        - 📝 Classification only (not for regression)
    """,
    "decision_trees": """
        #### Choose Decision Trees when:
        - 👥 You need to explain decisions to stakeholders
        - 📋 You want explicit decision rules
        - 🔢 You have mixed feature types
        - 📦 Your dataset is small and simple
    """,
    "random_forest": """
        #### Choose Random Forest when:
        - 🎯 You want reliable out-of-box performance
        - 📊 You need feature importance analysis
        - ❓ You have missing values
        - 🛡️ You want to avoid overfitting
    """,
    "mlp": """
        #### Choose MLP when:
        - 🧠 You have complex patterns
        - 📊 You have a large dataset
        - 💪 You have computational resources
        - 🎯 Interpretability isn't crucial
    """,
    "xgboost": """
        #### Choose XGBoost when:
        - 🏆 You need state-of-the-art performance
        - 📈 You have a large but not enormous dataset
        - ⚙️ You can tune hyperparameters
        - 🚀 You need production-ready solution
    """,
    "lightgbm": """
        #### Choose LightGBM when:
        - 📦 You have a very large dataset
        - ⚡ Training speed is critical
        - 💾 Memory usage is a concern
        - 🚀 You need production performance
    """,
    "hist_gradient_boosting": """
        #### Choose Histogram-based Gradient Boosting when:
        - 🔧 You want to stay within sklearn ecosystem
        - ⚡ You need faster training than standard Gradient Boosting
        - ❓ You have missing values (native support)
        - 📊 You have medium to large datasets
    """,
    "catboost": """
        #### Choose CatBoost when:
        - 🎯 You want competition-level, state-of-the-art accuracy
        - 🛡️ Overfitting resistance is critical
        - 📊 You have complex datasets with many features
        - 🚀 You want excellent results with minimal hyperparameter tuning
        - 🏆 Maximum model performance is the priority
        - ⚠️ **Note**: Requires Optuna optimization (Random Search not supported)
    """
}

# Performance metrics explanations for classification and regression
PERFORMANCE_METRICS_EXPLANATIONS = {
    "classification": {
        "accuracy": {
            "what_is": "Accuracy measures the **overall correctness** of predictions across all classes.",
            "formula": "`(Correct Predictions) / (Total Predictions)`",
            "range": "0 to 1 (or 0% to 100%)",
            "interpretation": {
                "1.0": "Perfect predictions",
                "0.5": "Random guessing (for balanced binary classification)",
                "0.0": "All predictions wrong"
            },
            "best_used_when": ["Balanced datasets", "All classes equally important", "Simple interpretation needed"],
            "avoid_when": ["Imbalanced datasets", "Cost of errors varies by class"],
            "warning": "**⚠️ Accuracy Paradox:** In imbalanced datasets, a model can achieve high accuracy by simply predicting the majority class!"
        },
        "precision": {
            "what_is": "Precision answers: **'Of all the positive predictions I made, how many were actually correct?'**",
            "formula": "`True Positives / (True Positives + False Positives)`",
            "range": "0 to 1 (or 0% to 100%)",
            "interpretation": {
                "high": "Few false alarms",
                "low": "Many false alarms"
            },
            "prioritize_when": ["False positives are costly", "You want to minimize false alarms", "Conservative predictions needed"],
            "examples": ["🚨 Spam detection", "💊 Medical diagnosis", "🔒 Fraud detection"]
        },
        "recall": {
            "what_is": "Recall answers: **'Of all the actual positive cases, how many did I correctly identify?'**",
            "formula": "`True Positives / (True Positives + False Negatives)`",
            "range": "0 to 1 (or 0% to 100%)",
            "interpretation": {
                "high": "Few missed cases",
                "low": "Many missed cases"
            },
            "prioritize_when": ["False negatives are costly", "You can't afford to miss cases", "Comprehensive detection needed"],
            "examples": ["🏥 Cancer screening", "🔥 Fire detection", "💳 Fraud monitoring"]
        },
        "f1_score": {
            "what_is": "F1-Score is the **harmonic mean** of precision and recall, providing a single metric that balances both.",
            "formula": "`2 × (Precision × Recall) / (Precision + Recall)`",
            "range": "0 to 1 (or 0% to 100%)",
            "interpretation": {
                "1.0": "Perfect precision and recall",
                "0.0": "Either precision or recall is zero"
            },
            "best_used_when": ["You need one overall metric", "Both precision and recall matter", "Comparing multiple models", "Imbalanced datasets"],
            "why_harmonic_mean": "The harmonic mean penalizes extreme values more than arithmetic mean - both precision AND recall must be high for a high F1-score"
        }
    },
    "regression": {
        "r2_score": {
            "what_is": "R² measures **how much of the target variable's variance** your model explains.",
            "formula": "`1 - (Sum of Squared Residuals) / (Total Sum of Squares)`",
            "range": "-∞ to 1",
            "interpretation": {
                "1.0": "Perfect predictions (explains 100% of variance)",
                "0.0": "Model performs no better than predicting the mean",
                "negative": "Model performs worse than predicting the mean"
            },
            "guidelines": {
                "excellent": "> 0.8",
                "good": "0.6-0.8",
                "moderate": "0.4-0.6",
                "poor": "< 0.4"
            }
        },
        "mae": {
            "what_is": "MAE measures the **average absolute difference** between predictions and actual values.",
            "formula": "`Average of |Predicted - Actual|`",
            "range": "0 to ∞",
            "units": "Same units as your target variable",
            "advantages": ["Easy to interpret", "Same units as target", "Not sensitive to outliers", "Treats all errors equally"],
            "best_used_when": ["You want simple interpretation", "All errors are equally bad"]
        },
        "mse": {
            "what_is": "MSE measures the **average of squared differences** between predictions and actual values.",
            "formula": "`Average of (Predicted - Actual)²`",
            "range": "0 to ∞",
            "units": "Units are squared (e.g., dollars²)",
            "characteristics": ["Penalizes large errors heavily", "Units are squared", "Sensitive to outliers", "Smooth for optimization"],
            "best_used_when": ["Large errors are much worse", "Training models (smooth gradient)"]
        },
        "rmse": {
            "what_is": "RMSE is the **square root of MSE**, bringing the metric back to original units.",
            "formula": "`√(Average of (Predicted - Actual)²)`",
            "range": "0 to ∞",
            "units": "Same units as your target variable",
            "benefits": ["Same units as target (like MAE)", "Penalizes large errors (like MSE)", "Easy to interpret", "Most commonly used"],
            "comparison": {
                "rmse_approx_mae": "Errors are consistent in size",
                "rmse_much_greater_mae": "You have some large errors (outliers)",
                "rmse_equals_mae": "All errors are exactly the same size (rare!)"
            }
        }
    }
}
"""
Automated Data Preprocessing Component

This module provides a fully automated preprocessing pipeline that replicates 100%
of the functionality from the manual data preprocessing page. It automatically applies
all recommendations and outputs all required data for the downstream pipeline.

Key Features:
- Complete replication of manual preprocessing functionality
- Automatic application of all recommendations
- Full KNN imputation support for missing values
- Optimal binning with optbinning library
- All outlier detection methods (IQR, Extended IQR, Isolation Forest)
- Complete feature creation with filtering pipeline
- Categorical encoding with mapping storage
- Data type optimization with synchronization
- Compatible output with all downstream stages

Usage:
    from utils.automated_preprocessing import AutomatedPreprocessingComponent

    auto_prep = AutomatedPreprocessingComponent(
        builder=st.session_state.builder,
        logger=st.session_state.logger,
        auto_select_top_features=10
    )

    result = auto_prep.run()
    if result['success']:
        # All preprocessing complete, ready for feature selection
        print(f"Success! {result['summary']}")
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import traceback
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Import existing preprocessing components
from components.data_preprocessing.train_test_split import TrainTestSplitComponent
from components.data_preprocessing.missing_values_analysis import MissingValuesAnalysis
from components.data_preprocessing.feature_binning import FeatureBinningComponent
from components.data_preprocessing.outlier_detection import OutlierDetectionComponent
from components.data_preprocessing.feature_creation import FeatureCreationComponent
from components.data_preprocessing.categorical_encoding import CategoricalEncodingComponent
from components.data_preprocessing.data_types_optimization import DataTypesOptimisationComponent

# Import utility functions for direct access
from components.data_preprocessing.utils.binning_utils import (
    suggest_binning_strategies,
    apply_binning
)
from components.data_preprocessing.utils.outlier_detection_utils import (
    suggest_outlier_strategies,
    handle_outliers
)

# Import Builder for ModelStage
from Builder import ModelStage


def _format_bin_range(bin_range: Any) -> str:
    """
    Format a bin range tuple into a clean, readable string.

    Handles:
    - Numerical ranges with infinity (e.g., (-inf, 10.5) -> "(-∞, 10.50]")
    - Numpy types (np.float64, np.inf) -> clean Python types
    - Tuple/list ranges with two values

    Args:
        bin_range: A tuple/list of (lower, upper) bounds or other value

    Returns:
        Formatted string representation of the bin range
    """
    if isinstance(bin_range, (list, tuple)) and len(bin_range) == 2:
        lower, upper = bin_range

        # Convert numpy values to Python types and handle infinity
        try:
            if np.isinf(lower) and float(lower) < 0:
                lower_str = '-∞'
            else:
                lower_str = f'{float(lower):.2f}'
        except (ValueError, TypeError):
            lower_str = str(lower)

        try:
            if np.isinf(upper) and float(upper) > 0:
                upper_str = '∞'
            else:
                upper_str = f'{float(upper):.2f}'
        except (ValueError, TypeError):
            upper_str = str(upper)

        return f'({lower_str}, {upper_str}]'

    return str(bin_range)


class AutomatedPreprocessingComponent:
    """
    Automated preprocessing component that replicates 100% of manual preprocessing
    functionality, automatically applying all recommendations.

    This component uses the actual utility functions from the preprocessing components
    to ensure complete fidelity with the manual process, including:
    - Full KNN imputation for missing values
    - Optimal binning with optbinning library
    - All outlier detection methods
    - Complete feature creation pipeline
    - Proper encoding mapping storage

    Attributes:
        builder: Builder instance containing data and model state
        logger: MLLogger instance for tracking operations
        auto_select_top_features: Number of engineered features to auto-select (default 10)
        show_analysis: Whether to display analysis summaries (default True)
        skip_feature_creation: Skip feature creation step (default False)
        preprocessing_summary: Dictionary containing preprocessing results

    Example:
        >>> auto_prep = AutomatedPreprocessingComponent(builder, logger)
        >>> result = auto_prep.run()
        >>> if result['success']:
        >>>     # Ready for feature selection
        >>>     st.switch_page("pages/4_Feature_Selection.py")
    """

    def __init__(
        self,
        builder,
        logger,
        auto_select_top_features: int = 10,
        show_analysis: bool = True,
        skip_feature_creation: bool = False
    ):
        """
        Initialize the automated preprocessing component.

        Args:
            builder: Builder instance with data loaded and target column set
            logger: MLLogger instance for tracking operations
            auto_select_top_features: Number of top engineered features to select (default 10)
            show_analysis: Whether to show analysis summaries (default True)
            skip_feature_creation: Skip feature creation step (default False)
        """
        self.builder = builder
        self.logger = logger
        self.auto_select_top_features = auto_select_top_features
        self.show_analysis = show_analysis
        self.skip_feature_creation = skip_feature_creation

        # Initialize preprocessing summary
        self.preprocessing_summary = {
            'steps_completed': [],
            'steps_failed': [],
            'start_time': None,
            'end_time': None,
            'initial_shape': None,
            'final_shape': None,
            'transformations_applied': [],
            'bin_ranges': {},  # Store binning information
            'encoding_mappings': {},  # Store encoding mappings
            'outlier_strategies': {}  # Store outlier handling strategies
        }

        # Validate initial state
        self._validate_initial_state()

    def _validate_initial_state(self):
        """Validate that required data and configuration exist."""
        if self.builder.data is None:
            raise ValueError("Builder data is None. Please load data before preprocessing.")

        if self.builder.target_column is None:
            raise ValueError("Target column is not set. Please set target column before preprocessing.")

        # Store initial shape for reporting
        self.preprocessing_summary['initial_shape'] = self.builder.data.shape

        self.logger.log_user_action(
            "Automated Preprocessing - Initialization",
            {
                "initial_shape": self.builder.data.shape,
                "target_column": self.builder.target_column,
                "auto_select_top_features": self.auto_select_top_features,
                "skip_feature_creation": self.skip_feature_creation
            }
        )

    def run(self) -> Dict[str, Any]:
        """
        Run the complete automated preprocessing pipeline.

        This method executes all preprocessing steps in sequence:
        1. Initial duplicate removal (before train-test split)
        2. Train-test split
        3. Missing values handling (median/mode/drop)
        4. Feature binning (with optbinning)
        5. Outlier handling (all 4 methods)
        6. Categorical encoding (with mapping storage)
        7. Feature creation (optional, with full filtering)
        8. Data types optimization (with synchronization)
        9. Final duplicate removal (after all preprocessing)

        Returns:
            Dict containing:
                - success (bool): Whether preprocessing completed successfully
                - summary (str): Human-readable summary of results
                - details (Dict): Detailed results from each step
                - errors (List): Any errors encountered during processing

        Example:
            >>> result = auto_prep.run()
            >>> if result['success']:
            >>>     st.success(result['summary'])
        """
        self.preprocessing_summary['start_time'] = datetime.now()

        self.logger.log_stage_transition(
            "DATA_LOADING",
            "AUTOMATED_PREPROCESSING_START"
        )

        # Only show header if showing step-by-step analysis
        if self.show_analysis:
            st.write("## 🤖 Automated Data Preprocessing")
            st.write("Running automated preprocessing pipeline with full fidelity to manual process...")

        try:
            # Step 1: Initial duplicate detection and removal (BEFORE train-test split)
            # This prevents duplicates from being split across train/test sets
            self._step_1_duplicate_removal_initial()

            # Step 2: Train-test split
            self._step_2_train_test_split()

            # Step 3: Missing values handling (with KNN)
            self._step_3_missing_values()

            # Step 4: Feature binning (with optbinning)
            self._step_4_feature_binning()

            # Step 5: Outlier handling (all methods)
            self._step_5_outlier_handling()

            # Step 6: Categorical encoding (with mapping storage)
            self._step_7_categorical_encoding()

            # Step 7: Feature creation (optional, with full filtering)
            if not self.skip_feature_creation:
                self._step_6_feature_creation()
            else:
                if self.show_analysis:
                    st.info("ℹ️ Feature creation step skipped per configuration.")

            # Step 8: Data types optimization (with synchronization)
            self._step_8_data_types_optimization()

            # Step 9: Final duplicate detection and removal (AFTER all preprocessing)
            # This catches any duplicates created during feature engineering
            self._step_9_duplicate_removal_final()

            # Step 10: Final validation - ensure train/test data consistency
            self._validate_final_data()

            # Finalize preprocessing
            self.preprocessing_summary['end_time'] = datetime.now()
            self.preprocessing_summary['final_shape'] = (
                self.builder.training_data.shape if self.builder.training_data is not None
                else None
            )

            # Mark preprocessing stage as complete
            self.builder.stage_completion[ModelStage.DATA_PREPROCESSING] = True

            # CRITICAL: Store final preprocessing data in session state
            # This is required for What-If Analysis to find auxiliary features
            # (e.g., original features that were binned and are needed for calculated fields)
            st.session_state.final_preprocessing_training_data = self.builder.training_data.copy()

            self.logger.log_stage_transition(
                "AUTOMATED_PREPROCESSING_END",
                "FEATURE_SELECTION"
            )

            # Generate summary (always needed for return value)
            summary = self._generate_summary()

            # Don't show summary here - it will be shown in the dashboard
            # Only show if explicitly in step-by-step mode
            if self.show_analysis:
                st.success("✅ Automated preprocessing completed successfully!")

            return {
                'success': True,
                'summary': summary,
                'details': self.preprocessing_summary,
                'errors': self.preprocessing_summary['steps_failed']
            }

        except Exception as e:
            error_msg = f"Automated preprocessing failed: {str(e)}"
            self.logger.log_error(
                "Automated Preprocessing Failed",
                {
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "steps_completed": self.preprocessing_summary['steps_completed'],
                    "steps_failed": self.preprocessing_summary['steps_failed']
                }
            )

            if self.show_analysis:
                st.error(f"❌ {error_msg}")
                with st.expander("View Error Details"):
                    st.code(traceback.format_exc())

            return {
                'success': False,
                'summary': error_msg,
                'details': self.preprocessing_summary,
                'errors': [str(e)]
            }

    def run_with_report(self) -> Dict[str, Any]:
        """
        Run preprocessing and generate a detailed report.

        Returns:
            Dict containing:
                - success (bool): Whether preprocessing completed successfully
                - summary (str): Human-readable summary
                - report (str): Detailed markdown report
                - details (Dict): Detailed results from each step

        Example:
            >>> result = auto_prep.run_with_report()
            >>> st.markdown(result['report'])
        """
        result = self.run()
        result['report'] = self._generate_detailed_report()
        return result

    def _step_1_duplicate_removal_initial(self):
        """
        Step 1: Initial Duplicate Detection and Removal (BEFORE train-test split)

        Detects and removes duplicates from the original dataset BEFORE splitting
        to prevent duplicates from appearing in both train and test sets.

        Checks for:
        1. Exact duplicates (all features + target identical)
        2. Partial duplicates (all features identical but different target values)

        Partial duplicates are problematic as they create ambiguous training examples
        where the same input leads to different outputs.
        """
        step_name = "Initial Duplicate Removal"

        try:
            if self.show_analysis:
                st.write(f"### Step 1: {step_name}")

            initial_shape = self.builder.data.shape

            # Check for exact duplicates (all columns including target)
            exact_duplicates = self.builder.data.duplicated(keep='first').sum()

            # Check for partial duplicates (same features, different target)
            feature_cols = [col for col in self.builder.data.columns if col != self.builder.target_column]
            partial_duplicates_mask = self.builder.data.duplicated(subset=feature_cols, keep=False)

            # Count partial duplicates (where features match but targets differ)
            partial_duplicate_groups = self.builder.data[partial_duplicates_mask].groupby(feature_cols)[self.builder.target_column].nunique()
            partial_duplicates = (partial_duplicate_groups > 1).sum()

            if exact_duplicates == 0 and partial_duplicates == 0:
                if self.show_analysis:
                    st.info("ℹ️ No duplicates found - skipping this step.")

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {
                        'exact_duplicates': 0,
                        'partial_duplicates': 0,
                        'action': 'skipped'
                    }
                })
                return

            # Remove exact duplicates (keep first occurrence)
            if exact_duplicates > 0:
                self.builder.data = self.builder.data.drop_duplicates(keep='first')

            # Remove partial duplicates (keep first occurrence of each feature combination)
            if partial_duplicates > 0:
                # For partial duplicates, keep the first occurrence
                self.builder.data = self.builder.data.drop_duplicates(subset=feature_cols, keep='first')

            final_shape = self.builder.data.shape
            rows_removed = initial_shape[0] - final_shape[0]

            self.preprocessing_summary['steps_completed'].append({
                'step': step_name,
                'details': {
                    'initial_shape': initial_shape,
                    'exact_duplicates_found': int(exact_duplicates),
                    'partial_duplicate_groups_found': int(partial_duplicates),
                    'rows_removed': int(rows_removed),
                    'final_shape': final_shape
                }
            })

            if self.show_analysis:
                st.success(f"✅ {step_name} complete")
                if exact_duplicates > 0:
                    st.write(f"- **Exact duplicates found:** {exact_duplicates} rows with identical values across all columns")
                    st.write(f"  - Action: Removed duplicates, keeping first occurrence")
                if partial_duplicates > 0:
                    st.write(f"- **Partial duplicate groups found:** {partial_duplicates} groups where features match but target differs")
                    st.write(f"  - Action: Removed ambiguous rows, keeping first occurrence of each feature combination")
                st.write(f"- **Total rows removed:** {rows_removed}")
                st.write(f"- **Shape change:** {initial_shape} → {final_shape}")

            self.logger.log_calculation(
                f"Automated Preprocessing - {step_name}",
                {
                    "exact_duplicates_removed": int(exact_duplicates),
                    "partial_duplicate_groups": int(partial_duplicates),
                    "rows_removed": int(rows_removed)
                }
            )

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _step_2_train_test_split(self):
        """
        Step 2: Train-Test Split

        Automatically splits data into training and testing sets using
        optimal ratios based on problem type and dataset size.
        """
        step_name = "Train-Test Split"

        try:
            if self.show_analysis:
                st.write(f"### Step 2: {step_name}")

            # Get features and target (same as TrainTestSplitComponent)
            X = self.builder.data.drop(columns=[self.builder.target_column])
            y = self.builder.data[self.builder.target_column]

            # Calculate adaptive test size (same logic as TrainTestSplitComponent.calculate_test_size)
            total_samples = len(X)
            min_test_samples = 100

            if total_samples < 1000:
                test_size = max(min_test_samples / total_samples, 0.20)
            elif total_samples < 10000:
                reduction = (total_samples - 1000) / 9000
                test_size = 0.20 - (0.05 * reduction)
            elif total_samples < 100000:
                reduction = (total_samples - 10000) / 90000
                test_size = 0.15 - (0.05 * reduction)
            else:
                test_size = min(0.10, 10000 / total_samples)

            # Ensure test size is between 0.05 and 0.20
            test_size = min(max(test_size, 0.05), 0.20)

            # Determine stratification (same as TrainTestSplitComponent)
            is_binary_classification = getattr(st.session_state, 'is_binary', False)
            is_multiclass_classification = getattr(st.session_state, 'is_multiclass', False)
            is_classification = is_binary_classification or is_multiclass_classification

            # Perform split using sklearn directly (same as TrainTestSplitComponent)
            if is_classification:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, stratify=y, random_state=42
                )
                split_method = "stratified"
            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )
                split_method = "random"

            # Create combined datasets
            training_data = pd.concat([X_train, y_train], axis=1)
            testing_data = pd.concat([X_test, y_test], axis=1)

            # Reset index
            training_data = training_data.reset_index(drop=True)
            testing_data = testing_data.reset_index(drop=True)

            # Store in builder
            self.builder.training_data = training_data
            self.builder.testing_data = testing_data
            self.builder.X_train = X_train
            self.builder.X_test = X_test
            self.builder.y_train = y_train
            self.builder.y_test = y_test

            # Update feature names
            self.builder.feature_names = list(X_train.columns)

            self.preprocessing_summary['steps_completed'].append({
                'step': step_name,
                'details': {
                    'test_size': test_size,
                    'training_shape': training_data.shape,
                    'testing_shape': testing_data.shape,
                    'stratified': split_method == "stratified",
                    'split_method': split_method
                }
            })

            if self.show_analysis:
                st.success(f"✅ {step_name} complete")
                st.write(f"- **Training set:** {training_data.shape[0]} rows, {training_data.shape[1]} columns")
                st.write(f"- **Testing set:** {testing_data.shape[0]} rows, {testing_data.shape[1]} columns")
                st.write(f"- **Split method:** {split_method.title()}")
                st.write(f"- **Test size:** {test_size:.1%} ({testing_data.shape[0]} samples)")
                st.write(f"- **Random state:** 42 (reproducible split)")

            self.logger.log_calculation(
                f"Automated Preprocessing - {step_name}",
                {
                    "test_size": test_size,
                    "split_method": split_method,
                    "training_shape": list(training_data.shape),
                    "testing_shape": list(testing_data.shape),
                    "stratified": split_method == "stratified"
                }
            )

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _step_3_missing_values(self):
        """
        Step 2: Missing Values Handling

        Automatically analyzes missing value patterns and applies optimal
        imputation strategies. Matches MissingValuesAnalysis component logic exactly.

        Strategies (matching manual component recommendations):
        - Drop column: For >50% missing
        - Drop rows: For <5% missing
        - KNN imputation: For numeric columns with correlations OR categorical with multiple features
        - Median imputation: For numeric columns (fallback)
        - Mode imputation: For categorical columns (fallback)

        Test data: Always drops rows with missing values (no imputation)
        """
        step_name = "Missing Values Handling"

        try:
            if self.show_analysis:
                st.write(f"### Step 2: {step_name}")

            # Check for missing values
            missing_count = self.builder.training_data.isnull().sum().sum()

            if missing_count == 0:
                if self.show_analysis:
                    st.info("ℹ️ No missing values found - skipping this step.")

                # Set completion flag even though no handling was needed
                st.session_state.missing_values_complete = True

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {'missing_count': 0, 'action': 'skipped'}
                })
                return

            # Get columns with missing values
            missing_cols = self.builder.training_data.columns[
                self.builder.training_data.isnull().any()
            ].tolist()

            # Automatically determine handling strategy for each column
            # Using SAME logic as MissingValuesAnalysis.render_missing_values_analysis()
            strategy_dict = {}
            training_data = self.builder.training_data

            for col in missing_cols:
                missing_pct = (training_data[col].isnull().sum() / len(training_data)) * 100
                is_numeric = pd.api.types.is_numeric_dtype(training_data[col])

                # Decision logic EXACTLY matching manual component (lines 277-315)
                if missing_pct > 50:
                    strategy_dict[col] = 'drop_column'
                elif missing_pct < 5:
                    strategy_dict[col] = 'drop_rows'
                elif is_numeric:
                    # Check for correlations with other numeric columns
                    numeric_cols = training_data.select_dtypes(include=['int64', 'float64']).columns
                    if len(numeric_cols) > 1:
                        strategy_dict[col] = 'knn'
                    else:
                        strategy_dict[col] = 'median'
                else:
                    # For categorical columns, check if KNN might be appropriate
                    categorical_cols = training_data.select_dtypes(include=['object', 'category']).columns
                    numeric_cols = training_data.select_dtypes(include=['int64', 'float64']).columns
                    # If we have multiple categorical columns or both numeric and categorical data,
                    # KNN might be a better choice than mode
                    if len(categorical_cols) > 1 or len(numeric_cols) > 0:
                        strategy_dict[col] = 'knn'
                    else:
                        strategy_dict[col] = 'mode'

            # Apply strategies directly to data (same as MissingValuesAnalysis._apply_missing_value_strategies)
            columns_processed = []

            for col, strategy in strategy_dict.items():
                if strategy == "drop_rows":
                    # Drop rows with missing values in both datasets
                    self.builder.training_data = self.builder.training_data.dropna(subset=[col])
                    self.builder.testing_data = self.builder.testing_data.dropna(subset=[col])
                    columns_processed.append(col)

                elif strategy == "drop_column":
                    # Drop entire column from both datasets
                    self.builder.training_data = self.builder.training_data.drop(columns=[col])
                    self.builder.testing_data = self.builder.testing_data.drop(columns=[col])
                    columns_processed.append(col)

                elif strategy == "mean":
                    # Calculate mean from training data only
                    mean_value = self.builder.training_data[col].mean()
                    # Apply to training data
                    self.builder.training_data[col] = self.builder.training_data[col].fillna(mean_value)
                    # For testing data, drop rows with missing values
                    self.builder.testing_data = self.builder.testing_data.dropna(subset=[col])
                    columns_processed.append(col)

                elif strategy == "median":
                    # Calculate median from training data only
                    median_value = self.builder.training_data[col].median()
                    # Apply to training data
                    self.builder.training_data[col] = self.builder.training_data[col].fillna(median_value)
                    # For testing data, drop rows with missing values
                    self.builder.testing_data = self.builder.testing_data.dropna(subset=[col])
                    columns_processed.append(col)

                elif strategy == "mode":
                    # Calculate mode from training data only
                    mode_value = self.builder.training_data[col].mode()[0]
                    # Apply to training data
                    self.builder.training_data[col] = self.builder.training_data[col].fillna(mode_value)
                    # For testing data, drop rows with missing values
                    self.builder.testing_data = self.builder.testing_data.dropna(subset=[col])
                    columns_processed.append(col)

                elif strategy == "knn":
                    # Apply KNN imputation to training data, drop rows in test data
                    self._apply_knn_imputation_automated(col)
                    columns_processed.append(col)

            # Reset indices after dropping rows
            self.builder.training_data = self.builder.training_data.reset_index(drop=True)
            self.builder.testing_data = self.builder.testing_data.reset_index(drop=True)

            # Update X_train, X_test, y_train, y_test after modifications
            self.builder.X_train = self.builder.training_data.drop(columns=[self.builder.target_column])
            self.builder.X_test = self.builder.testing_data.drop(columns=[self.builder.target_column])
            self.builder.y_train = self.builder.training_data[self.builder.target_column]
            self.builder.y_test = self.builder.testing_data[self.builder.target_column]

            # Update feature names
            self.builder.feature_names = list(self.builder.X_train.columns)

            # Mark missing values as complete
            st.session_state.missing_values_complete = True

            self.preprocessing_summary['steps_completed'].append({
                'step': step_name,
                'details': {
                    'columns_processed': len(columns_processed),
                    'strategies_applied': strategy_dict,
                    'remaining_missing': int(self.builder.training_data.isnull().sum().sum()),
                    'processed_columns': columns_processed
                }
            })

            if self.show_analysis:
                st.success(f"✅ {step_name} complete")
                st.write(f"- **Columns processed:** {len(columns_processed)}")

                # Show detailed strategy breakdown
                strategy_counts = {}
                for strategy in strategy_dict.values():
                    strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

                st.write(f"- **Strategies applied:**")
                for strategy, count in strategy_counts.items():
                    strategy_name_map = {
                        'drop_column': 'Drop Column (>50% missing)',
                        'drop_rows': 'Drop Rows (<5% missing)',
                        'knn': 'KNN Imputation',
                        'median': 'Median Imputation',
                        'mode': 'Mode Imputation',
                        'mean': 'Mean Imputation'
                    }
                    st.write(f"  - {strategy_name_map.get(strategy, strategy)}: {count} column(s)")

                # Show specific columns and their strategies
                with st.expander("View detailed column-wise strategies"):
                    for col, strategy in strategy_dict.items():
                        st.write(f"  - **{col}:** {strategy_name_map.get(strategy, strategy)}")

                st.write(f"- **Remaining missing values:** {self.builder.training_data.isnull().sum().sum()}")
                st.write(f"- **Final training shape:** {self.builder.training_data.shape}")
                st.write(f"- **Final testing shape:** {self.builder.testing_data.shape}")

            self.logger.log_calculation(
                f"Automated Preprocessing - {step_name}",
                {
                    "columns_processed": len(columns_processed),
                    "strategies_applied": strategy_dict,
                    "remaining_missing": int(self.builder.training_data.isnull().sum().sum())
                }
            )

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _step_4_feature_binning(self):
        """
        Step 3: Feature Binning

        Automatically applies optimal binning using the optbinning library with
        complete analysis including:
        - Non-linear relationship detection (Pearson vs Spearman correlation)
        - U-shaped relationship detection (quadratic regression)
        - Skewness analysis
        - Optimal bin calculation with proper parameters

        Uses the real binning_utils functions for complete fidelity.
        """
        step_name = "Feature Binning"

        try:
            if self.show_analysis:
                st.write(f"### Step 3: {step_name}")

            # Get REAL binning suggestions using the actual utility function
            # This includes all the sophisticated analysis from the manual component
            suggestions_result = suggest_binning_strategies(
                self.builder.training_data,
                self.builder.target_column
            )

            if not suggestions_result['success']:
                if self.show_analysis:
                    st.warning(f"Could not generate binning suggestions: {suggestions_result.get('message', 'Unknown error')}")
                return

            suggestions = suggestions_result['suggestions']

            # Count how many features need binning
            features_needing_binning = sum(
                1 for sug in suggestions.values()
                if sug.get('needs_binning', False)
            )

            if features_needing_binning == 0:
                if self.show_analysis:
                    st.info("ℹ️ No features require binning based on analysis.")

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {
                        'features_analyzed': len(suggestions),
                        'features_binned': 0,
                        'action': 'skipped'
                    }
                })
                return

            # Build strategy dict - automatically apply binning where recommended
            strategy_dict = {}

            for col, suggestion in suggestions.items():
                if suggestion.get('needs_binning', False):
                    # Apply the recommended strategy (usually "Optimal")
                    strategy_dict[col] = {
                        'strategy': suggestion['strategy'],
                        'n_bins': suggestion.get('n_bins', None)
                    }
                else:
                    strategy_dict[col] = {'strategy': 'None'}

            # Apply binning using REAL utility function with optbinning library
            result = apply_binning(
                self.builder.training_data,
                self.builder.testing_data,
                strategy_dict,
                self.builder.target_column
            )

            if result['success']:
                # Update builder with binned data
                self.builder.training_data = result['training_data']
                self.builder.testing_data = result['testing_data']

                # CRITICAL: Convert binned features from category to int for XGBoost compatibility
                # XGBoost requires int, float, bool or category with enable_categorical=True
                # Converting to int is the simplest solution
                modified_columns = result.get('modified_columns', [])
                for col in modified_columns:
                    if col in self.builder.training_data.columns:
                        # Check if column is categorical (binned features are typically categorical)
                        if pd.api.types.is_categorical_dtype(self.builder.training_data[col]):
                            # Convert category codes to int (0, 1, 2, ...)
                            self.builder.training_data[col] = self.builder.training_data[col].cat.codes.astype('int64')

                    if col in self.builder.testing_data.columns:
                        if pd.api.types.is_categorical_dtype(self.builder.testing_data[col]):
                            self.builder.testing_data[col] = self.builder.testing_data[col].cat.codes.astype('int64')

                # Store bin_ranges for downstream use (e.g., model explanation)
                bin_ranges = result.get('bin_ranges', {})
                self.preprocessing_summary['bin_ranges'] = bin_ranges

                # CRITICAL: Store binning information in session state (matching manual feature binning)
                # This is required for later stages to access bin information
                if not hasattr(st.session_state, 'binning_info'):
                    st.session_state.binning_info = {}

                # For each binned column, store its original name and bin ranges
                for orig_col, binned_col in zip(result.get("dropped_columns", []), result.get("modified_columns", [])):
                    if binned_col in bin_ranges:
                        st.session_state.binning_info[binned_col] = {
                            "original_feature": orig_col,
                            "bin_ranges": bin_ranges[binned_col],
                            "is_categorical": orig_col in self.builder.training_data.select_dtypes(include=['object', 'category']).columns
                        }

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {
                        'features_analyzed': len(suggestions),
                        'features_binned': len(modified_columns),
                        'modified_columns': modified_columns,
                        'bin_ranges': bin_ranges,
                        'dropped_columns': result.get('dropped_columns', [])
                    }
                })

                if self.show_analysis:
                    st.success(f"✅ {step_name} complete")
                    st.write(f"- **Features analyzed:** {len(suggestions)}")
                    st.write(f"- **Features binned:** {len(modified_columns)}")

                    if modified_columns:
                        st.write(f"- **Binned features:**")
                        for col in modified_columns:
                            # Get the strategy used
                            original_col = col.replace('_binned', '')
                            if original_col in strategy_dict:
                                strategy = strategy_dict[original_col]['strategy']
                                n_bins = strategy_dict[original_col].get('n_bins', 'Auto')
                                st.write(f"  - **{col}** (from {original_col}): {strategy} binning, {n_bins} bins")

                        # Show bin ranges in expander
                        if bin_ranges:
                            with st.expander("View bin ranges for each feature"):
                                for col, ranges in bin_ranges.items():
                                    st.write(f"**{col}:**")
                                    if isinstance(ranges, list):
                                        # Numerical binning - format as clean ranges
                                        for i, bin_range in enumerate(ranges):
                                            formatted_range = _format_bin_range(bin_range)
                                            st.write(f"  - Bin {i}: {formatted_range}")
                                    elif isinstance(ranges, dict):
                                        # Categorical binning - show category mappings
                                        for bin_id, categories in ranges.items():
                                            cat_str = ', '.join(map(str, categories))
                                            st.write(f"  - {bin_id}: {cat_str}")
                                    else:
                                        st.write(f"  - {ranges}")

                self.logger.log_calculation(
                    f"Automated Preprocessing - {step_name}",
                    {
                        "features_binned": len(modified_columns),
                        "modified_columns": modified_columns,
                        "bin_ranges": bin_ranges
                    }
                )
            else:
                raise Exception(result.get('message', 'Unknown error during binning'))

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _step_5_outlier_handling(self):
        """
        Step 4: Outlier Detection and Handling

        Automatically detects and handles outliers using multiple methods:
        - IQR method (1.5*IQR) for standard outliers
        - Extended IQR method (3*IQR) for extreme outliers (Tukey's far outliers)
        - Isolation Forest for skewed data with sufficient samples
        - Intelligent recommendations based on outlier percentage and skewness

        Strategies applied:
        - Remove: Delete rows with outliers (1.5*IQR)
        - Remove Extreme: Delete only extreme outliers (3*IQR)
        - Cap: Limit values to threshold (Winsorization)
        - Isolation Forest: ML-based outlier detection

        IMPORTANT: Binned features are excluded from outlier analysis since they
        have already been transformed into discrete bins.

        Uses the real outlier_detection_utils functions for complete fidelity.
        """
        step_name = "Outlier Handling"

        try:
            if self.show_analysis:
                st.write(f"### Step 4: {step_name}")

            # Get REAL outlier suggestions using the actual utility function
            # This includes intelligent recommendations based on data characteristics
            suggestions_result = suggest_outlier_strategies(
                self.builder.training_data,
                self.builder.target_column
            )

            if not suggestions_result['success']:
                if self.show_analysis:
                    st.warning(f"Could not generate outlier suggestions: {suggestions_result.get('message', 'Unknown error')}")
                return

            suggestions = suggestions_result['suggestions']

            # CRITICAL: Exclude binned features from outlier analysis
            # Binned features have already been transformed and should not be analyzed for outliers
            binned_features = [col for col in suggestions.keys() if col.endswith('_binned')]
            suggestions = {col: sug for col, sug in suggestions.items() if col not in binned_features}

            if binned_features and self.show_analysis:
                st.info(f"ℹ️ Excluded {len(binned_features)} binned feature(s) from outlier analysis: {', '.join(binned_features)}")

            # Count features that need outlier handling
            features_needing_handling = sum(
                1 for sug in suggestions.values()
                if sug.get('strategy') != 'None'
            )

            if features_needing_handling == 0:
                if self.show_analysis:
                    st.info("ℹ️ No outlier handling needed based on analysis.")

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {
                        'features_analyzed': len(suggestions),
                        'features_handled': 0,
                        'action': 'skipped'
                    }
                })
                return

            # Apply recommended strategies automatically
            outliers_handled = []
            total_outliers_removed = 0

            for col, suggestion in suggestions.items():
                strategy = suggestion['strategy']

                if strategy == 'None':
                    continue

                # Handle outliers in training data using REAL utility function
                # Supports: 'Remove', 'Remove Extreme', 'Cap', 'Isolation Forest'
                result = handle_outliers(
                    self.builder.training_data,
                    col,
                    strategy
                )

                if result['success'] and result.get('modified', False):
                    self.builder.training_data = result['data']
                    outlier_count = result.get('outlier_count', 0)
                    total_outliers_removed += outlier_count

                    # No outlier handling applied to test data (per user requirement)
                    # Only training data is processed for outliers

                    outliers_handled.append({
                        'feature': col,
                        'strategy': strategy,
                        'outliers_count': outlier_count
                    })

            # Store outlier strategies for reference
            self.preprocessing_summary['outlier_strategies'] = {
                oh['feature']: oh['strategy'] for oh in outliers_handled
            }

            self.preprocessing_summary['steps_completed'].append({
                'step': step_name,
                'details': {
                    'features_analyzed': len(suggestions),
                    'features_handled': len(outliers_handled),
                    'total_outliers_processed': total_outliers_removed,
                    'outliers_handled': outliers_handled
                }
            })

            if self.show_analysis:
                st.success(f"✅ {step_name} complete")
                st.write(f"- **Features analyzed:** {len(suggestions)}")
                st.write(f"- **Features with outlier handling:** {len(outliers_handled)}")
                st.write(f"- **Total outliers processed:** {total_outliers_removed}")

                if outliers_handled:
                    st.write(f"- **Outlier handling details:**")
                    for oh_info in outliers_handled:
                        feature = oh_info['feature']
                        strategy = oh_info['strategy']
                        count = oh_info['outliers_count']

                        strategy_desc_map = {
                            'Remove': 'IQR method (1.5×IQR)',
                            'Remove Extreme': 'Extended IQR method (3×IQR, Tukey\'s far outliers)',
                            'Cap': 'Winsorization (cap to threshold)',
                            'Isolation Forest': 'ML-based detection'
                        }
                        strategy_desc = strategy_desc_map.get(strategy, strategy)
                        st.write(f"  - **{feature}:** {strategy_desc} - {count} outlier(s)")

                    with st.expander("View outlier detection rationale"):
                        for col, suggestion in suggestions.items():
                            if suggestion['strategy'] != 'None':
                                st.write(f"**{col}:**")
                                st.write(f"  - Strategy: {suggestion['strategy']}")
                                if 'reason' in suggestion:
                                    st.write(f"  - Reason: {suggestion['reason']}")

            self.logger.log_calculation(
                f"Automated Preprocessing - {step_name}",
                {
                    "features_handled": len(outliers_handled),
                    "outliers_details": outliers_handled
                }
            )

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _step_6_feature_creation(self):
        """
        Step 5: Feature Creation

        Automatically generates and selects engineered features using the complete
        filtering pipeline:
        - Generates combinations using 5 operations (ratio, sum, difference, product, mean)
        - Removes features with >5% null values
        - Calculates correlation matrix for all features
        - Removes multicollinear features (correlation > 0.8)
        - Removes features with similar distributions (Kolmogorov-Smirnov test)
        - Analyzes target relationships using mutual information
        - Applies RMS correlation penalty
        - Final correlation group analysis with network graphs

        Uses the real FeatureCreationComponent methods with caching.

        CRITICAL: This step runs AFTER outlier handling, which may have modified
        the training data size (removed rows). We need to ensure the component
        uses the current data, not cached references.
        """
        step_name = "Feature Creation"

        try:
            if self.show_analysis:
                st.write(f"### Step 5: {step_name}")

            # CRITICAL: Update X_train and y_train to reflect current data state
            # Previous steps (outlier handling, missing values) may have removed rows
            self.builder.X_train = self.builder.training_data.drop(columns=[self.builder.target_column])
            self.builder.X_test = self.builder.testing_data.drop(columns=[self.builder.target_column])
            self.builder.y_train = self.builder.training_data[self.builder.target_column]
            self.builder.y_test = self.builder.testing_data[self.builder.target_column]

            # CRITICAL: Clear any cached feature creation data from session state
            # This prevents size mismatches when previous steps modified row counts
            try:
                if 'feature_creation_generated_features' in st.session_state:
                    del st.session_state['feature_creation_generated_features']
            except (AttributeError, KeyError):
                pass

            try:
                if 'feature_creation_selected_features' in st.session_state:
                    del st.session_state['feature_creation_selected_features']
            except (AttributeError, KeyError):
                pass

            # Initialize feature creation component with refreshed data
            fc_component = FeatureCreationComponent(
                self.builder,
                self.logger,
                self.builder.training_data,
                self.builder.testing_data,
                self.builder.target_column
            )

            # Get numeric features
            numeric_features = fc_component._get_numeric_features()

            if len(numeric_features) < 2:
                if self.show_analysis:
                    st.info("ℹ️ Insufficient numeric features (< 2) - skipping feature creation.")

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {'numeric_features': len(numeric_features), 'action': 'skipped'}
                })
                return

            # Generate feature combinations using CACHED function
            # This uses cached generation for performance
            fc_component._generate_feature_combinations(numeric_features)

            # Analyze generated features using CACHED function with COMPLETE filtering
            # This includes all the sophisticated filtering from the manual component
            top_features = fc_component._analyse_generated_features()

            # Select top N features automatically
            features_to_add = top_features[:min(self.auto_select_top_features, len(top_features))]

            # Inform user if limiting selection
            if len(top_features) > self.auto_select_top_features:
                if self.show_analysis:
                    st.info(f"ℹ️ {len(top_features)} features passed filtering, selecting top {self.auto_select_top_features} based on target correlation")

            if len(features_to_add) == 0:
                if self.show_analysis:
                    st.info("ℹ️ No suitable engineered features found after filtering.")

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {
                        'features_generated': len(st.session_state.feature_creation_generated_features),
                        'features_added': 0,
                        'action': 'no_features_selected'
                    }
                })
                return

            # Apply selected features to both training and testing data
            st.session_state.feature_creation_selected_features = features_to_add
            successful_features = []
            failed_features = []  # Track features that failed to be added

            for feat_name in features_to_add:
                feat_info = None  # Initialize to avoid reference errors
                try:
                    feat_info = st.session_state.feature_creation_generated_features[feat_name]
                    operation = feat_info['operation_func']
                    feat1 = feat_info['feature1']
                    feat2 = feat_info['feature2']

                    # Add to training data
                    self.builder.training_data[feat_name] = feat_info['values']

                    # Calculate and add to testing data
                    feat1_values = self.builder.testing_data[feat1]
                    feat2_values = self.builder.testing_data[feat2]

                    # Handle binned features that might be categorical
                    from pandas.api.types import is_categorical_dtype
                    if '_binned' in feat1 and is_categorical_dtype(feat1_values):
                        feat1_values = pd.to_numeric(feat1_values.astype(str), errors='coerce')
                    if '_binned' in feat2 and is_categorical_dtype(feat2_values):
                        feat2_values = pd.to_numeric(feat2_values.astype(str), errors='coerce')

                    # Apply operation
                    feat_values = operation(feat1_values, feat2_values)
                    feat_values = pd.Series(feat_values).replace([np.inf, -np.inf], np.nan).fillna(0)

                    self.builder.testing_data[feat_name] = feat_values
                    successful_features.append(feat_name)

                except Exception as feature_error:
                    # Log and track the failure with details
                    error_msg = str(feature_error)
                    self.logger.log_error(
                        f"Failed to add feature {feat_name}",
                        {"error": error_msg, "traceback": traceback.format_exc()}
                    )

                    # Track failed feature with error information
                    failed_info = {
                        'feature': feat_name,
                        'error': error_msg
                    }

                    # Add component feature info if available
                    if feat_info is not None:
                        failed_info.update({
                            'feature1': feat_info.get('feature1', 'Unknown'),
                            'feature2': feat_info.get('feature2', 'Unknown'),
                            'operation': feat_info.get('operation', 'Unknown')
                        })

                    failed_features.append(failed_info)
                    continue

            self.preprocessing_summary['steps_completed'].append({
                'step': step_name,
                'details': {
                    'features_generated': len(st.session_state.feature_creation_generated_features),
                    'features_analyzed': len(top_features),
                    'features_selected': len(features_to_add),
                    'features_added': len(successful_features),
                    'features_failed': len(failed_features),
                    'added_features_list': successful_features,
                    'failed_features_list': failed_features
                }
            })

            if self.show_analysis:
                st.success(f"✅ {step_name} complete")
                st.write(f"- **Feature combinations generated:** {len(st.session_state.feature_creation_generated_features)}")
                st.write(f"- **Features after filtering pipeline:** {len(top_features)}")
                st.write(f"- **Features selected for addition:** {len(features_to_add)}")
                st.write(f"- **Engineered features successfully added:** {len(successful_features)}")

                # Show warning if some features failed
                if len(features_to_add) > len(successful_features):
                    st.warning(f"⚠️ {len(features_to_add) - len(successful_features)} feature(s) failed to be added")

                if successful_features:
                    st.write(f"- **Top engineered features:**")
                    for i, feat in enumerate(successful_features[:5], 1):
                        feat_info = st.session_state.feature_creation_generated_features[feat]
                        operation = feat_info['operation']
                        st.write(f"  {i}. **{feat}** ({operation} of {feat_info['feature1']} and {feat_info['feature2']})")

                    if len(successful_features) > 5:
                        st.write(f"  ... and {len(successful_features) - 5} more")

                    with st.expander("View all engineered features"):
                        for feat in successful_features:
                            feat_info = st.session_state.feature_creation_generated_features[feat]
                            st.write(f"- **{feat}:** {feat_info['operation']} of {feat_info['feature1']} and {feat_info['feature2']}")

                # Show failed features with detailed error information
                if failed_features:
                    with st.expander("⚠️ View failed features and error details"):
                        st.write(f"**{len(failed_features)} feature(s) could not be added:**")
                        st.write("")
                        for fail_info in failed_features:
                            st.write(f"**{fail_info['feature']}**")
                            st.write(f"  - **Error:** {fail_info['error']}")

                            # Show component features if available
                            if 'operation' in fail_info and fail_info['operation'] != 'Unknown':
                                st.write(f"  - **Operation:** {fail_info['operation']}")
                                st.write(f"  - **Requires:** {fail_info['feature1']} and {fail_info['feature2']}")

                            st.write("")  # Blank line for readability

                st.write(f"- **Filtering stages applied:**")
                st.write(f"  - Null value filter (>5% nulls removed)")
                st.write(f"  - Multicollinearity filter (correlation > 0.8)")
                st.write(f"  - Distribution similarity filter (KS test)")
                st.write(f"  - Target relationship analysis (mutual information)")
                st.write(f"  - RMS correlation penalty")

            self.logger.log_calculation(
                f"Automated Preprocessing - {step_name}",
                {
                    "features_generated": len(st.session_state.feature_creation_generated_features),
                    "features_analyzed": len(top_features),
                    "features_selected": len(features_to_add),
                    "features_added": len(successful_features),
                    "features_failed": len(failed_features),
                    "added_features_list": successful_features,
                    "failed_features_count": len(failed_features)
                }
            )

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _step_7_categorical_encoding(self):
        """
        Step 6: Categorical Encoding

        Automatically encodes categorical variables using optimal strategies
        based on cardinality and target relationships. Stores encoding mappings
        in both session state and Builder for downstream use.

        Encoding strategies:
        - Label Encoding: For low cardinality or ordered categories
        - One-Hot Encoding: For low cardinality unordered categories
        - Target Encoding: For high cardinality with target relationship

        CRITICAL: Properly stores encoding_mappings in session state for
        model evaluation and explanation stages.

        IMPORTANT: Binned features are EXCLUDED from encoding to prevent
        double transformation.
        """
        step_name = "Categorical Encoding"

        try:
            if self.show_analysis:
                st.write(f"### Step 6: {step_name}")

            # Get categorical columns
            categorical_cols = self.builder.training_data.select_dtypes(
                include=['object', 'category']
            ).columns.tolist()

            # CRITICAL: Exclude binned features from encoding
            # Binned features are already transformed and should not be encoded again
            binned_features = [col for col in categorical_cols if col.endswith('_binned')]
            categorical_cols = [col for col in categorical_cols if col not in binned_features]

            if len(categorical_cols) == 0:
                if self.show_analysis:
                    if binned_features:
                        st.info(f"ℹ️ No categorical variables found that need encoding (excluding {len(binned_features)} binned features) - skipping this step.")
                    else:
                        st.info("ℹ️ No categorical variables found - skipping this step.")

                # Mark encoding as complete even though no encoding was needed
                st.session_state.categorical_encoding_complete = True

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {
                        'categorical_columns': 0,
                        'binned_features_excluded': len(binned_features),
                        'action': 'skipped'
                    }
                })
                return

            # Get encoding suggestions from Builder
            suggestions = self.builder.suggest_encoding_strategies(data=self.builder.training_data)

            if not suggestions["success"]:
                raise Exception("Failed to generate encoding suggestions")

            handling_dict = {}

            for col in categorical_cols:
                if col not in suggestions["suggestions"]:
                    continue

                suggestion = suggestions["suggestions"][col]

                # Use the suggested strategy
                strategy_mapping = {
                    "label": "label",
                    "onehot": "onehot",
                    "target": "target",
                    "drop": "drop_column"
                }
                method = strategy_mapping.get(suggestion['strategy'], 'label')
                handling_dict[col] = {"method": method}

            # Apply encoding to training data using Builder's real method
            result = self.builder.handle_categorical_data(
                handling_dict,
                data=self.builder.training_data,
                is_training=True
            )

            # Apply to testing data
            if result["success"] and self.builder.testing_data is not None:
                test_result = self.builder.handle_categorical_data(
                    handling_dict,
                    data=self.builder.testing_data,
                    is_training=False
                )

            if result["success"]:
                # CRITICAL: Store encoding mappings in session state
                # This is required for downstream stages (evaluation, explanation)
                if result.get('encoding_mappings'):
                    if 'encoding_mappings' not in st.session_state:
                        st.session_state.encoding_mappings = {}

                    # Merge new mappings with existing ones
                    st.session_state.encoding_mappings.update(result['encoding_mappings'])

                    # Also store in Builder for consistency
                    self.builder.encoding_mappings = st.session_state.encoding_mappings

                    # Store in summary for reporting
                    self.preprocessing_summary['encoding_mappings'] = st.session_state.encoding_mappings

                # Mark encoding as complete
                st.session_state.categorical_encoding_complete = True

                modified_columns = result.get('modified_columns', [])

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {
                        'columns_encoded': len(handling_dict),
                        'encoding_methods': handling_dict,
                        'modified_columns': modified_columns,
                        'mappings_stored': len(self.preprocessing_summary['encoding_mappings'])
                    }
                })

                if self.show_analysis:
                    st.success(f"✅ {step_name} complete")
                    st.write(f"- **Categorical columns encoded:** {len(handling_dict)}")
                    st.write(f"- **Encoding mappings stored:** {len(self.preprocessing_summary['encoding_mappings'])}")

                    if handling_dict:
                        # Count encoding methods
                        method_counts = {}
                        for col_info in handling_dict.values():
                            method = col_info['method']
                            method_counts[method] = method_counts.get(method, 0) + 1

                        st.write(f"- **Encoding methods applied:**")
                        method_name_map = {
                            'label': 'Label Encoding (ordinal)',
                            'onehot': 'One-Hot Encoding',
                            'target': 'Target Encoding (mean encoding)',
                            'drop_column': 'Drop Column'
                        }
                        for method, count in method_counts.items():
                            st.write(f"  - {method_name_map.get(method, method)}: {count} column(s)")

                        # Show specific columns and their methods
                        with st.expander("View detailed encoding strategies"):
                            for col, col_info in handling_dict.items():
                                method = col_info['method']
                                st.write(f"  - **{col}:** {method_name_map.get(method, method)}")

                                # Show cardinality info from suggestions if available
                                if col in suggestions['suggestions']:
                                    cardinality = suggestions['suggestions'][col].get('cardinality', 'N/A')
                                    st.write(f"    - Unique values: {cardinality}")

                self.logger.log_calculation(
                    f"Automated Preprocessing - {step_name}",
                    {
                        "columns_encoded": len(handling_dict),
                        "encoding_methods": handling_dict,
                        "mappings_count": len(self.preprocessing_summary['encoding_mappings'])
                    }
                )
            else:
                raise Exception(result.get('message', 'Unknown error during encoding'))

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _step_8_data_types_optimization(self):
        """
        Step 7: Data Types Optimization

        Automatically optimizes data types for memory efficiency and ensures
        synchronization between training and testing datasets.

        Optimizations:
        - Binary features (0/1) → int8
        - Integer features → Downcast to int16/int32 if possible
        - Float features → Downcast to float32 if possible
        - Low cardinality objects → category type

        CRITICAL: Synchronizes data types between train and test datasets
        to prevent type mismatch errors during model training.
        """
        step_name = "Data Types Optimization"

        try:
            if self.show_analysis:
                st.write(f"### Step 7: {step_name}")

            # Initialize data types optimization component
            dtype_component = DataTypesOptimisationComponent(self.builder, self.logger)

            # CRITICAL: Synchronize data types first
            # This ensures testing data types match training data
            dtype_component._synchronize_data_types()

            # Get optimization suggestions
            suggestions, optimized_types = dtype_component._get_optimisation_suggestions(
                self.builder.training_data
            )

            # Calculate initial memory
            train_memory_before = self.builder.training_data.memory_usage().sum() / 1024 / 1024
            test_memory_before = self.builder.testing_data.memory_usage().sum() / 1024 / 1024

            # Apply optimizations
            successful_conversions = []

            for col, new_type in optimized_types.items():
                if new_type != str(self.builder.training_data[col].dtype):
                    try:
                        old_type = str(self.builder.training_data[col].dtype)

                        # Apply to training data
                        if new_type == 'datetime':
                            self.builder.training_data[col] = pd.to_datetime(self.builder.training_data[col])
                        elif new_type == 'int8' and self.builder.training_data[col].dtype == 'object':
                            # Convert string '0'/'1' to integers first
                            self.builder.training_data[col] = self.builder.training_data[col].map(
                                {'0': 0, '1': 1}
                            ).astype('int8')
                        else:
                            self.builder.training_data[col] = self.builder.training_data[col].astype(new_type)

                        # Apply to testing data
                        if col in self.builder.testing_data.columns:
                            if new_type == 'datetime':
                                self.builder.testing_data[col] = pd.to_datetime(self.builder.testing_data[col])
                            elif new_type == 'int8' and self.builder.testing_data[col].dtype == 'object':
                                self.builder.testing_data[col] = self.builder.testing_data[col].map(
                                    {'0': 0, '1': 1}
                                ).astype('int8')
                            else:
                                self.builder.testing_data[col] = self.builder.testing_data[col].astype(new_type)

                        successful_conversions.append((col, old_type, new_type))

                    except Exception as conversion_error:
                        # Log but don't fail entire step
                        self.logger.log_error(
                            f"Failed to convert {col}",
                            {"error": str(conversion_error), "target_type": new_type}
                        )
                        continue

            # Calculate final memory
            train_memory_after = self.builder.training_data.memory_usage().sum() / 1024 / 1024
            test_memory_after = self.builder.testing_data.memory_usage().sum() / 1024 / 1024
            memory_saved = (train_memory_before + test_memory_before) - (train_memory_after + test_memory_after)

            self.preprocessing_summary['steps_completed'].append({
                'step': step_name,
                'details': {
                    'conversions_applied': len(successful_conversions),
                    'memory_before_mb': train_memory_before + test_memory_before,
                    'memory_after_mb': train_memory_after + test_memory_after,
                    'memory_saved_mb': memory_saved,
                    'memory_reduction_pct': (memory_saved / (train_memory_before + test_memory_before)) * 100
                }
            })

            if self.show_analysis:
                st.success(f"✅ {step_name} complete")
                st.write(f"- **Type conversions applied:** {len(successful_conversions)}")
                st.write(f"- **Memory saved:** {memory_saved:.2f} MB ({(memory_saved / (train_memory_before + test_memory_before) * 100):.1f}%)")
                st.write(f"- **Memory before:** {train_memory_before + test_memory_before:.2f} MB")
                st.write(f"- **Memory after:** {train_memory_after + test_memory_after:.2f} MB")

                if successful_conversions:
                    # Group conversions by type
                    conversion_groups = {}
                    for col, old_type, new_type in successful_conversions:
                        key = f"{old_type} → {new_type}"
                        if key not in conversion_groups:
                            conversion_groups[key] = []
                        conversion_groups[key].append(col)

                    st.write(f"- **Type conversions by category:**")
                    for conversion_type, cols in conversion_groups.items():
                        st.write(f"  - {conversion_type}: {len(cols)} column(s)")

                    with st.expander("View detailed type conversions"):
                        for col, old_type, new_type in successful_conversions:
                            st.write(f"  - **{col}:** {old_type} → {new_type}")

            self.logger.log_calculation(
                f"Automated Preprocessing - {step_name}",
                {
                    "conversions_applied": len(successful_conversions),
                    "memory_saved_mb": memory_saved
                }
            )

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _step_9_duplicate_removal_final(self):
        """
        Step 9: Final Duplicate Detection and Removal (AFTER all preprocessing)

        Detects and removes duplicates from the preprocessed training and testing
        datasets. This catches any duplicates that may have been created during
        feature engineering (e.g., binning, encoding, feature creation).

        Checks for:
        1. Exact duplicates (all features + target identical)
        2. Partial duplicates (all features identical but different target values)

        Applied separately to training and testing datasets to maintain data separation.
        """
        step_name = "Final Duplicate Removal"

        try:
            if self.show_analysis:
                st.write(f"### Step 9: {step_name}")

            # Process training data
            train_initial_shape = self.builder.training_data.shape

            # Check for exact duplicates in training data
            train_exact_duplicates = self.builder.training_data.duplicated(keep='first').sum()

            # Check for partial duplicates in training data
            feature_cols = [col for col in self.builder.training_data.columns if col != self.builder.target_column]
            train_partial_duplicates_mask = self.builder.training_data.duplicated(subset=feature_cols, keep=False)

            # Count partial duplicates (where features match but targets differ)
            train_partial_duplicate_groups = self.builder.training_data[train_partial_duplicates_mask].groupby(feature_cols)[self.builder.target_column].nunique()
            train_partial_duplicates = (train_partial_duplicate_groups > 1).sum()

            # Remove duplicates from training data
            train_rows_removed = 0
            if train_exact_duplicates > 0 or train_partial_duplicates > 0:
                # Remove exact duplicates
                if train_exact_duplicates > 0:
                    self.builder.training_data = self.builder.training_data.drop_duplicates(keep='first')

                # Remove partial duplicates
                if train_partial_duplicates > 0:
                    self.builder.training_data = self.builder.training_data.drop_duplicates(subset=feature_cols, keep='first')

                train_rows_removed = train_initial_shape[0] - self.builder.training_data.shape[0]

                # Update X_train and y_train after removal
                self.builder.X_train = self.builder.training_data.drop(columns=[self.builder.target_column])
                self.builder.y_train = self.builder.training_data[self.builder.target_column]

            # Process testing data
            test_initial_shape = self.builder.testing_data.shape

            # Check for exact duplicates in testing data
            test_exact_duplicates = self.builder.testing_data.duplicated(keep='first').sum()

            # Check for partial duplicates in testing data
            test_partial_duplicates_mask = self.builder.testing_data.duplicated(subset=feature_cols, keep=False)

            # Count partial duplicates
            test_partial_duplicate_groups = self.builder.testing_data[test_partial_duplicates_mask].groupby(feature_cols)[self.builder.target_column].nunique()
            test_partial_duplicates = (test_partial_duplicate_groups > 1).sum()

            # Remove duplicates from testing data
            test_rows_removed = 0
            if test_exact_duplicates > 0 or test_partial_duplicates > 0:
                # Remove exact duplicates
                if test_exact_duplicates > 0:
                    self.builder.testing_data = self.builder.testing_data.drop_duplicates(keep='first')

                # Remove partial duplicates
                if test_partial_duplicates > 0:
                    self.builder.testing_data = self.builder.testing_data.drop_duplicates(subset=feature_cols, keep='first')

                test_rows_removed = test_initial_shape[0] - self.builder.testing_data.shape[0]

                # Update X_test and y_test after removal
                self.builder.X_test = self.builder.testing_data.drop(columns=[self.builder.target_column])
                self.builder.y_test = self.builder.testing_data[self.builder.target_column]

            total_exact_duplicates = int(train_exact_duplicates + test_exact_duplicates)
            total_partial_duplicates = int(train_partial_duplicates + test_partial_duplicates)
            total_rows_removed = int(train_rows_removed + test_rows_removed)

            if total_rows_removed == 0:
                if self.show_analysis:
                    st.info("ℹ️ No duplicates found after preprocessing - skipping this step.")

                self.preprocessing_summary['steps_completed'].append({
                    'step': step_name,
                    'details': {
                        'train_exact_duplicates': 0,
                        'train_partial_duplicates': 0,
                        'test_exact_duplicates': 0,
                        'test_partial_duplicates': 0,
                        'total_rows_removed': 0,
                        'action': 'skipped'
                    }
                })
                return

            self.preprocessing_summary['steps_completed'].append({
                'step': step_name,
                'details': {
                    'train_initial_shape': train_initial_shape,
                    'train_exact_duplicates': int(train_exact_duplicates),
                    'train_partial_duplicates': int(train_partial_duplicates),
                    'train_rows_removed': train_rows_removed,
                    'train_final_shape': self.builder.training_data.shape,
                    'test_initial_shape': test_initial_shape,
                    'test_exact_duplicates': int(test_exact_duplicates),
                    'test_partial_duplicates': int(test_partial_duplicates),
                    'test_rows_removed': test_rows_removed,
                    'test_final_shape': self.builder.testing_data.shape,
                    'total_exact_duplicates': total_exact_duplicates,
                    'total_partial_duplicates': total_partial_duplicates,
                    'total_rows_removed': total_rows_removed
                }
            })

            if self.show_analysis:
                st.success(f"✅ {step_name} complete")
                st.write(f"**Training Data:**")
                if train_exact_duplicates > 0:
                    st.write(f"- **Exact duplicates found:** {train_exact_duplicates} rows")
                    st.write(f"  - Action: Removed duplicates, keeping first occurrence")
                if train_partial_duplicates > 0:
                    st.write(f"- **Partial duplicate groups found:** {train_partial_duplicates} groups")
                    st.write(f"  - Action: Removed ambiguous rows")
                if train_rows_removed > 0:
                    st.write(f"- **Rows removed:** {train_rows_removed}")
                else:
                    st.write(f"- No duplicates found")

                st.write(f"**Testing Data:**")
                if test_exact_duplicates > 0:
                    st.write(f"- **Exact duplicates found:** {test_exact_duplicates} rows")
                    st.write(f"  - Action: Removed duplicates, keeping first occurrence")
                if test_partial_duplicates > 0:
                    st.write(f"- **Partial duplicate groups found:** {test_partial_duplicates} groups")
                    st.write(f"  - Action: Removed ambiguous rows")
                if test_rows_removed > 0:
                    st.write(f"- **Rows removed:** {test_rows_removed}")
                else:
                    st.write(f"- No duplicates found")

                st.write(f"**Total rows removed: {total_rows_removed}**")
                st.write(f"- Final training shape: {self.builder.training_data.shape}")
                st.write(f"- Final testing shape: {self.builder.testing_data.shape}")

            self.logger.log_calculation(
                f"Automated Preprocessing - {step_name}",
                {
                    "train_exact_duplicates": int(train_exact_duplicates),
                    "train_partial_duplicates": int(train_partial_duplicates),
                    "train_rows_removed": train_rows_removed,
                    "test_exact_duplicates": int(test_exact_duplicates),
                    "test_partial_duplicates": int(test_partial_duplicates),
                    "test_rows_removed": test_rows_removed,
                    "total_rows_removed": total_rows_removed
                }
            )

        except Exception as e:
            self._handle_step_error(step_name, e)

    def _validate_final_data(self):
        """
        Final validation step to ensure train/test data consistency.

        Checks:
        1. Both train and test datasets exist
        2. Same columns in both datasets (excluding target)
        3. Same data types for matching columns
        4. No NaN values in either dataset
        5. X_train, X_test, y_train, y_test are properly set
        """
        step_name = "Final Data Validation"

        try:
            if self.show_analysis:
                st.write(f"### Step 10: {step_name}")

            validation_issues = []

            # Check 1: Both datasets exist
            if self.builder.training_data is None:
                validation_issues.append("Training data is None")
            if self.builder.testing_data is None:
                validation_issues.append("Testing data is None")

            if validation_issues:
                raise ValueError(f"Missing datasets: {', '.join(validation_issues)}")

            # Check 2: Column consistency
            train_cols = set(self.builder.training_data.columns)
            test_cols = set(self.builder.testing_data.columns)

            if train_cols != test_cols:
                missing_in_test = train_cols - test_cols
                missing_in_train = test_cols - train_cols
                if missing_in_test:
                    validation_issues.append(f"Columns in training but not testing: {missing_in_test}")
                if missing_in_train:
                    validation_issues.append(f"Columns in testing but not training: {missing_in_train}")

            # Check 3: Data type consistency (excluding target column)
            feature_cols = [col for col in train_cols if col != self.builder.target_column]
            dtype_mismatches = []

            for col in feature_cols:
                train_dtype = self.builder.training_data[col].dtype
                test_dtype = self.builder.testing_data[col].dtype
                if train_dtype != test_dtype:
                    dtype_mismatches.append(f"{col}: train={train_dtype}, test={test_dtype}")

            if dtype_mismatches:
                validation_issues.append(f"Data type mismatches: {dtype_mismatches}")

            # Check 4: No NaN values
            train_nans = self.builder.training_data.isna().sum().sum()
            test_nans = self.builder.testing_data.isna().sum().sum()

            if train_nans > 0:
                validation_issues.append(f"Training data has {train_nans} NaN values")
            if test_nans > 0:
                validation_issues.append(f"Testing data has {test_nans} NaN values")

            # Check 5: X_train, X_test, y_train, y_test are set
            if self.builder.X_train is None:
                validation_issues.append("X_train is None")
            if self.builder.X_test is None:
                validation_issues.append("X_test is None")
            if self.builder.y_train is None:
                validation_issues.append("y_train is None")
            if self.builder.y_test is None:
                validation_issues.append("y_test is None")

            if validation_issues:
                raise ValueError(f"Validation failed:\n" + "\n".join(f"  - {issue}" for issue in validation_issues))

            # CRITICAL: Update X_train, X_test, y_train, y_test to reflect final preprocessing state
            # This ensures the dataset overview and all downstream stages use the correct preprocessed data
            # with all transformations applied (binning, feature creation, encoding, data type optimization)
            self.builder.X_train = self.builder.training_data.drop(columns=[self.builder.target_column])
            self.builder.X_test = self.builder.testing_data.drop(columns=[self.builder.target_column])
            self.builder.y_train = self.builder.training_data[self.builder.target_column]
            self.builder.y_test = self.builder.testing_data[self.builder.target_column]

            # Update feature names to match final X_train columns
            self.builder.feature_names = list(self.builder.X_train.columns)

            # All checks passed
            validation_summary = {
                'train_shape': self.builder.training_data.shape,
                'test_shape': self.builder.testing_data.shape,
                'num_features': len(feature_cols),
                'train_nans': int(train_nans),
                'test_nans': int(test_nans),
                'columns_match': True,
                'dtypes_match': True
            }

            self.preprocessing_summary['steps_completed'].append({
                'step': step_name,
                'details': validation_summary
            })

            if self.show_analysis:
                st.success(f"✅ {step_name} complete")
                st.write(f"- **Training shape:** {validation_summary['train_shape']}")
                st.write(f"- **Testing shape:** {validation_summary['test_shape']}")
                st.write(f"- **Number of features:** {validation_summary['num_features']}")
                st.write(f"- **Dataset consistency checks:**")
                st.write(f"  - Columns match: ✓")
                st.write(f"  - Data types match: ✓")
                st.write(f"  - No NaN values: ✓")
                st.write(f"  - X_train/X_test/y_train/y_test: ✓")
                st.write(f"  - Feature names synchronized: ✓")

            self.logger.log_calculation(
                f"Automated Preprocessing - {step_name}",
                validation_summary
            )

        except Exception as e:
            self._handle_step_error(step_name, e)
            # Re-raise to stop the pipeline since validation failed
            raise

    def _apply_knn_imputation_automated(self, column: str):
        """
        Apply KNN imputation to a specific column in training data.
        For testing data, drop rows with missing values.

        This method replicates the exact logic from MissingValuesAnalysis._apply_knn_imputation
        (lines 708-804 in missing_values_analysis.py)

        Args:
            column: The column to apply KNN imputation to
        """
        train_data_for_impute = self.builder.training_data.copy()

        # Only proceed if we have enough data for KNN
        if len(train_data_for_impute) <= 5:  # Not enough samples for KNN
            self._apply_fallback_strategy_automated(column)
            return

        # Identify column types
        numeric_cols = train_data_for_impute.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = train_data_for_impute.select_dtypes(include=['object', 'category']).columns.tolist()

        # Prepare preprocessing for both types of data
        transformers = []

        # Only add numeric preprocessing if we have numeric columns
        if numeric_cols:
            # Just pass numeric columns through without scaling to preserve original values
            transformers.append(('num', 'passthrough', numeric_cols))

        # Only add categorical preprocessing if we have categorical columns
        if categorical_cols:
            # Use OrdinalEncoder for categorical data to preserve distances
            categorical_transformer = Pipeline(steps=[
                ('ordinal', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
            ])
            transformers.append(('cat', categorical_transformer, categorical_cols))

        # Create and apply the column transformer
        if not transformers:  # No transformers to apply
            self._apply_fallback_strategy_automated(column)
            return

        try:
            preprocessor = ColumnTransformer(
                transformers=transformers,
                remainder='passthrough'
            )

            # Fit and transform the data
            train_processed = preprocessor.fit_transform(train_data_for_impute)

            # Apply KNN imputation
            imputer = KNNImputer(n_neighbors=min(5, len(train_data_for_impute)-1))
            imputed_data = imputer.fit_transform(train_processed)

            # If we're imputing the selected column
            if column in numeric_cols:
                # Find the position of the column in the processed data
                col_pos = numeric_cols.index(column)
                # Replace the column with imputed values in training data
                self.builder.training_data[column] = imputed_data[:, col_pos]
            elif column in categorical_cols:
                # Find the position of the column
                col_pos = len(numeric_cols) + categorical_cols.index(column)

                # Get the encoder for this categorical column
                encoder = preprocessor.transformers_[1][1].named_steps['ordinal']

                # Get the imputed values and inverse transform them
                imputed_cat_values = imputed_data[:, col_pos].reshape(-1, 1)

                # Round the values to nearest integer (since ordinal encoding produces integers)
                imputed_cat_values = np.round(imputed_cat_values).astype(int)

                # Convert back to original categories
                original_categories = encoder.inverse_transform(imputed_cat_values)

                # Replace the column
                self.builder.training_data[column] = original_categories.flatten()

            # For test data, drop rows with missing values
            if column in self.builder.testing_data.columns:
                self.builder.testing_data = self.builder.testing_data.dropna(subset=[column])

        except Exception as e:
            # Log the exception for debugging
            self.logger.log_error(
                "KNN Imputation Error (Automated)",
                {
                    "error": str(e),
                    "column": column,
                    "fallback": "Using median/mode imputation instead"
                }
            )
            self._apply_fallback_strategy_automated(column)

    def _apply_fallback_strategy_automated(self, column: str):
        """
        Apply a fallback strategy when KNN imputation fails.
        Training data: median/mode imputation
        Testing data: drop rows

        Args:
            column: The column to apply the fallback strategy to
        """
        if pd.api.types.is_numeric_dtype(self.builder.training_data[column]):
            median_value = self.builder.training_data[column].median()
            self.builder.training_data[column] = self.builder.training_data[column].fillna(median_value)
        else:
            mode_value = self.builder.training_data[column].mode()[0]
            self.builder.training_data[column] = self.builder.training_data[column].fillna(mode_value)

        # For test data, always drop rows
        self.builder.testing_data = self.builder.testing_data.dropna(subset=[column])

    def _handle_step_error(self, step_name: str, error: Exception):
        """
        Handle errors that occur during a preprocessing step.

        Args:
            step_name: Name of the step that failed
            error: Exception that was raised
        """
        error_details = {
            'step': step_name,
            'error': str(error),
            'traceback': traceback.format_exc()
        }

        self.preprocessing_summary['steps_failed'].append(error_details)

        self.logger.log_error(
            f"Automated Preprocessing - {step_name} Failed",
            error_details
        )

        if self.show_analysis:
            st.warning(f"⚠️ {step_name} failed: {str(error)}")
            with st.expander("View Error Details"):
                st.code(traceback.format_exc())
            st.info("Continuing with remaining steps...")

    def _generate_summary(self) -> str:
        """
        Generate a human-readable summary of preprocessing results.

        Returns:
            Formatted summary string
        """
        duration = (
            self.preprocessing_summary['end_time'] - self.preprocessing_summary['start_time']
        ).total_seconds()

        summary = f"""
### Preprocessing Summary

**Duration:** {duration:.1f} seconds

**Steps Completed:** {len(self.preprocessing_summary['steps_completed'])} / {len(self.preprocessing_summary['steps_completed']) + len(self.preprocessing_summary['steps_failed'])}

**Dataset Shape:**
- Initial: {self.preprocessing_summary['initial_shape']}
- Final (Training): {self.preprocessing_summary['final_shape']}

**Key Outputs:**
- Encoding mappings stored: {len(self.preprocessing_summary.get('encoding_mappings', {}))}
- Bin ranges stored: {len(self.preprocessing_summary.get('bin_ranges', {}))}
- Outlier strategies applied: {len(self.preprocessing_summary.get('outlier_strategies', {}))}

**Steps:**
"""

        for step in self.preprocessing_summary['steps_completed']:
            summary += f"\n✅ {step['step']}"

        for step in self.preprocessing_summary['steps_failed']:
            summary += f"\n❌ {step['step']} (failed)"

        return summary

    def _generate_detailed_report(self) -> str:
        """
        Generate a detailed markdown report of all preprocessing operations.

        Returns:
            Detailed markdown report
        """
        report = "# Automated Preprocessing Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += "## Summary\n\n"
        report += self._generate_summary()
        report += "\n\n## Detailed Results\n\n"

        for step in self.preprocessing_summary['steps_completed']:
            report += f"### {step['step']}\n\n"
            report += "**Details:**\n\n"
            for key, value in step['details'].items():
                if isinstance(value, (list, dict)) and len(str(value)) > 100:
                    report += f"- **{key}:** {len(value)} items\n"
                else:
                    report += f"- **{key}:** {value}\n"
            report += "\n"

        if self.preprocessing_summary['steps_failed']:
            report += "## Failed Steps\n\n"
            for step in self.preprocessing_summary['steps_failed']:
                report += f"### {step['step']}\n\n"
                report += f"**Error:** {step['error']}\n\n"

        return report

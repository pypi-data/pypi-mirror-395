"""
Preprocessing explanations and documentation for Advanced Auto Preprocessing.

This module contains all explanatory text for the advanced automated preprocessing
feature, including the 10-step pipeline and optional feature selection.
"""

ADVANCED_AUTO_PREPROCESSING_EXPLANATION = """
### What is Advanced Auto Preprocessing?

Advanced auto preprocessing provides a comprehensive 10-step pipeline that prepares
your dataset for Feature Selection and Model Development using state-of-the-art techniques.

### The 10 Preprocessing Steps:

1. **Initial Duplicate Removal** (Before Split)
   - Removes exact duplicates (all features + target identical)
   - Removes partial duplicates (same features, different targets)
   - Prevents duplicates from being split across train/test sets

2. **Train-Test Split**
   - Intelligent split sizing based on dataset size
   - Stratification for classification problems
   - Ensures proper data separation

3. **Missing Values Handling**
   - **Training data**: KNN imputation (k=5) with fallback to median/mode
   - **Testing data**: Drops rows with missing values (no imputation)
   - Supports both numeric and categorical features
   - Prevents data leakage

4. **Feature Binning**
   - Uses optimal binning (optbinning library)
   - Detects non-linear and U-shaped relationships
   - Training statistics applied to test data
   - Preserves ordinal nature of bins

5. **Outlier Handling**
   - **Training data only**: Multiple strategies (Remove, Remove Extreme, Cap, Isolation Forest)
   - **Testing data**: No outlier handling (preserves real-world distribution)
   - Intelligent recommendations based on data characteristics

6. **Categorical Encoding**
   - Low cardinality (<10): One-hot encoding
   - High cardinality (>=10): Target encoding
   - Binned features: Label encoding (preserves order)
   - Stores encoding mappings for downstream use

7. **Feature Creation**
   - Generates combinations using 5 operations (ratio, sum, difference, product, mean)
   - Complete 7-step filtering process:
     1. Null value filtering (>5%)
     2. Correlation matrix calculation
     3. Multicollinearity removal (>0.8)
     4. Similar distribution removal (KS test)
     5. Target relationship analysis (mutual information)
     6. RMS correlation scoring
     7. Iterative correlation group analysis
   - Automatically selects top N features (default 10)
   
8. **Data Types Optimization**
   - Binary features -> int8
   - Integer features -> Downcast to int16/int32
   - Float features -> Downcast to float32
   - Low cardinality objects -> category type
   - Synchronizes train/test data types

9. **Final Duplicate Removal** (After Preprocessing)
   - Catches duplicates created during feature engineering
   - Applied separately to train and test datasets
   - Ensures clean data for model training

10. **Final Data Validation**
    - Verifies train/test column consistency
    - Checks data type matching
    - Confirms zero NaN values
    - Validates X/y splits
    - Ensures downstream compatibility

### Optional: Automated Feature Selection

When enabled, an additional automated feature selection pipeline runs after preprocessing:

**Feature Selection Steps:**
1. **Feature Importance Analysis** - Calculates importance scores and identifies issues
2. **Low Importance Removal** - Removes features below threshold (≤ 0.01)
3. **Correlation Removal** - Iteratively removes correlated features (> 0.7) one per group
4. **Protected Attributes Review** - Identifies sensitive features (not removed automatically)
5. **Data Synchronization** - Ensures data consistency
6. **Boruta Selection** (Optional) - Advanced feature selection using Boruta algorithm
7. **Duplicate Removal** - Removes duplicates after feature changes
8. **Final Validation** - Validates final feature set

**Configuration Options:**
- **Include Automated Feature Selection**: Enable/disable feature selection
- **Enable Boruta Algorithm**: Use Boruta for advanced selection (requires minimum features)
- **Boruta Threshold**: Minimum features needed to trigger Boruta (default: 10)

**Boruta Strategy**: Uses "Confirmed Only" approach - removes tentative and rejected features,
keeping only features confirmed as important by the algorithm.

### Benefits:
- 🚀 **Comprehensive**: Complete 10-step preprocessing pipeline with optional feature selection
- 🧠 **Intelligent**: Advanced techniques including KNN imputation, optimal binning, and Boruta algorithm
- 🎯 **Accurate**: Proper train/test separation with no data leakage
- ⚡ **Automated**: From raw data to model-ready features with minimal configuration
- 📊 **Transparent**: Detailed step-by-step analysis and comprehensive reporting
- ✅ **Validated**: Multiple validation checkpoints ensure data integrity
- 🔍 **Explainable**: Clear reasoning for all feature removals and transformations
- 🛡️ **Responsible**: Identifies protected attributes and prevents bias introduction

### When to Use:
- ✅ **Production pipelines**: When you need a reliable, battle-tested preprocessing workflow
- ✅ **Advanced preprocessing**: When KNN imputation, optimal binning, and feature engineering are beneficial
- ✅ **Feature selection**: When you want to automatically reduce dimensionality and remove redundant features
- ✅ **Large datasets**: When you have enough data for proper train/test splits and advanced techniques
- ✅ **Time constraints**: When you need fast, automated preprocessing without manual intervention
- ✅ **Best practices**: When you want to ensure proper data handling and avoid common pitfalls

### When NOT to Use:
- ❌ **Small datasets** (< 100 rows): Advanced techniques may not work well with limited data
- ❌ **Simple problems**: When basic preprocessing is sufficient for your use case
- ❌ **Custom requirements**: When you need fine-grained control over each preprocessing step
- ❌ **Domain-specific preprocessing**: When your data requires specialized domain knowledge

> 💡 **Note**: This advanced pipeline is sophisticated and provides production-ready results,
>  but may take longer to run on large datasets. The automated feature selection
> is optional and can be disabled if you prefer to handle feature selection manually.
"""

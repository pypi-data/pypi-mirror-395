import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from utils.dataset_overview import DatasetOverviewComponent
from utils.logging.logger import MLLogger

class TrainTestSplitComponent:
    def __init__(self, builder):
        self.builder = builder
        self.logger = MLLogger()

    def calculate_test_size(self,total_samples):
        """
        Calculate optimal test size based on dataset size following common ML practices.
        
        Args:
            total_samples (int): Total number of samples in dataset
            
        Returns:
            float: Optimal test size as a proportion (between 0 and 1)
        """
        min_test_samples = 100  # Increased from 50 to ensure better statistical significance
        
        if total_samples < 1000:
            # For small datasets (<1000 samples)
            # Use 20% but ensure at least 100 samples if possible
            test_size = max(min_test_samples / total_samples, 0.20)
            
        elif total_samples < 10000:
            # For medium datasets (1000-10000 samples)
            # Gradually decrease from 20% to 15%
            reduction = (total_samples - 1000) / 9000  # Scales from 0 to 1
            test_size = 0.20 - (0.05 * reduction)  # Reduces from 0.20 to 0.15
            
        elif total_samples < 100000:
            # For large datasets (10000-100000 samples)
            # Gradually decrease from 15% to 10%
            reduction = (total_samples - 10000) / 90000  # Scales from 0 to 1
            test_size = 0.15 - (0.05 * reduction)  # Reduces from 0.15 to 0.10
            
        else:
            # For very large datasets (>100000 samples)
            # Use 10% but ensure test set doesn't become unnecessarily large
            test_size = min(0.10, 10000 / total_samples)
        
        # Ensure test size is between 0.05 and 0.20
        return min(max(test_size, 0.05), 0.20)

    def render_train_test_split(self):
        """
        Renders the train test split section.
        """
        st.write("### Train Test Split")
        st.write("""
            Split your data into training data and testing data.
            - Training set: Used to train the model on patterns and relationships
            - Testing set: Used to evaluate how well the model generalizes to new data
            
            To prevent data leakage the training and testing sets are kept separate.
            This helps prevent overfitting and provides a more realistic assessment of model performance.
            
            The split ratio is automatically optimized based on your dataset size.
                 
            For the rest of the data preprocessing you will be working with the training data.
            The only changes made to the testing data will be to match the format of the training data:
            - Rows with missing values will be removed from the testing data.
            - Features that are binned in the training data will be updated in the testing data by mapping the ranges for each bin.
            - No changes to the testing data will be made when handling outliers, changes will only be applied to the training data
            - When categorical encoding the test data will be one hot encoded as with the training data, for features that have been label or target encoded the mappings from the training data will be applied to the test data
            - Changes in datatypes will be applied to both the training and test data
            """)
        
        # Add explanation about the optimized splitting and recommendations for custom settings
        with st.expander("ℹ️ Understanding Train-Test Split Options", expanded=False):
            st.markdown("""
            ### How Optimized Splitting Works
            
            The automatic split ratio is dynamically calculated based on your dataset size to optimize the balance between having enough test data for reliable evaluation and maximizing training data for better model learning.
            
            #### Calculation Logic:
            
            - For small datasets (< 1,000 samples):
              - Uses 20% test split
              - Ensures at least 100 samples in test set where possible
              - Formula: `test_size = max(100 / total_samples, 0.20)`
            
            - For medium datasets (1,000-10,000 samples):
              - Gradually reduces from 20% to 15% test split
              - Reduction scales with dataset size
            
            - For large datasets (10,000-100,000 samples):
              - Gradually reduces from 15% to 10% test split
              - Reduction scales with dataset size
            
            - For very large datasets (> 100,000 samples):
              - Uses 10% test split
              - Caps test set size to prevent it becoming unnecessarily large
              - Formula: `test_size = min(0.10, 10000 / total_samples)`
            
            The final test size is always kept between 5% and 20% of the total dataset.
            
            #### Automatic Splitting Benefits:
            
            - Small datasets maintain adequate test samples while maximizing training data
            - Medium datasets use a balanced approach (15-20% test split)
            - Large datasets use a smaller percentage for testing (10-15%)
            - Very large datasets optimize for efficiency (≤10%)
            - Always maintains sufficient test samples for statistical significance
            
            ### Custom Split Recommendations
            
            When to consider using a custom split percentage:
            
            | Dataset Size | Recommended Test % | Considerations |
            |--------------|-------------------|----------------|
            | < 1,000 samples | 20-25% | Higher % ensures adequate test samples, but may limit training data |
            | 1,000-10,000 samples | 15-20% | Traditional split ratio works well in this range |
            | 10,000-100,000 samples | 10-15% | Can use smaller test % to maximize training data |
            | > 100,000 samples | 5-10% | Very large datasets can use minimal test % |
            
            **Special Considerations:**
            
            - Imbalanced Classes: For highly imbalanced datasets, prefer the automatic splitting which uses stratification to maintain class proportions
            - Rare Events: If you have rare events, ensure your test split is large enough to include sufficient examples of these events
            
            The automatic optimisation is designed to make these decisions for you, but custom splitting gives you control when you have specific requirements.
            """)
        
        # Create options for custom or automatic split
        split_option = st.radio(
            "Choose split method:",
            ["Automatic (Optimized)", "Custom"],
            index=0
        )
        
        # Custom test size slider if selected
        custom_test_size = None
        if split_option == "Custom":
            custom_test_size = st.slider(
                "Test set percentage", 
                min_value=10, 
                max_value=40, 
                value=20, 
                step=5,
                format="%d%%",
                help="Select the percentage of data to use for testing"
            ) / 100
        
        # Apply Train Test Split
        if self.builder.X_train is None or \
            self.builder.X_test is None or \
            len(self.builder.data) != (
                len(self.builder.X_train) + len(self.builder.X_test)
            ) or \
            (split_option == "Custom" and custom_test_size is not None):  # Added condition for custom split
            
            # Get features and target
            X = self.builder.data.drop(columns=[self.builder.target_column])
            y = self.builder.data[self.builder.target_column]
            
            # Calculate adaptive test size based on dataset size or use custom value
            total_samples = len(X)
            min_test_samples = 50
            
            if split_option == "Custom" and custom_test_size is not None:
                test_size = custom_test_size
                split_method_description = "custom"
            else:
                total_samples = len(X)
                test_size = self.calculate_test_size(total_samples)
                split_method_description = "automatic"
            # Log the split calculation
            st.session_state.logger.log_calculation(
                "Train Test Split Calculation",
                {
                    "total_samples": total_samples,
                    "test_size": test_size,
                    "split_method": split_method_description,
                    "estimated_test_samples": int(total_samples * test_size),
                    "estimated_train_samples": int(total_samples * (1 - test_size)),
                    "test_percentage": f"{test_size * 100:.1f}%"
                }
            )
            
            # Determine if it's a classification or regression problem using session state
            is_binary_classification = getattr(st.session_state, 'is_binary', False)
            is_multiclass_classification = getattr(st.session_state, 'is_multiclass', False)
            is_classification = is_binary_classification or is_multiclass_classification
            
            if is_classification:
                # Perform train/test split with appropriate method
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, stratify=y, random_state=42
                )
                split_method = "stratified"
            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )
                split_method = "random"
            
            training_data = pd.concat([X_train, y_train], axis=1)
            testing_data = pd.concat([X_test, y_test], axis=1)

            #Reset index
            training_data = training_data.reset_index(drop=True)
            testing_data = testing_data.reset_index(drop=True)

            self.builder.training_data = training_data
            self.builder.testing_data = testing_data
            
            # Store in builder for later use
            self.builder.X_train = X_train
            self.builder.X_test = X_test
            self.builder.y_train = y_train
            self.builder.y_test = y_test
            
            # Log the split results with enhanced information
            problem_type = getattr(st.session_state, 'problem_type', 'unknown')
            st.session_state.logger.log_calculation(
                "Train/Test Split Results",
                {
                    "split_method": split_method,
                    "split_type": split_method_description,
                    "problem_type": problem_type,
                    "train_size": len(X_train),
                    "test_size": len(X_test),
                    "train_class_distribution": y_train.value_counts().to_dict() if is_classification else "regression",
                    "test_class_distribution": y_test.value_counts().to_dict() if is_classification else "regression",
                    "total_features": len(X_train.columns)
                }
            )

            st.session_state.logger.log_journey_point(
                stage="DATA_PREPROCESSING",
                decision_type="TRAIN_TEST_SPLIT",
                description="Train/Test split completed",
                details={'Split Method': split_method, 
                         'Split Type': split_method_description,
                         'Problem Type': problem_type,
                         'Train Shape': self.builder.training_data.shape, 
                         'Test Shape': self.builder.testing_data.shape, 
                         'Train Class Distribution': y_train.value_counts().to_dict() if is_classification else "regression", 
                         'Test Class Distribution': y_test.value_counts().to_dict() if is_classification else "regression", 
                         },
                parent_id=None
            )

            # Show success confirmation and split information
            st.success(f"✅ Data successfully split into training and testing sets using {split_method_description} split!")
            
            # Display split information in an expander
            with st.expander("📊 View split information", expanded=True):
                # Create columns for split metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Training set size", f"{len(X_train)} samples", 
                              f"{len(X_train)/total_samples:.1%} of data")
                
                with col2:
                    st.metric("Testing set size", f"{len(X_test)} samples", 
                              f"{len(X_test)/total_samples:.1%} of data")
                
                st.markdown(f"**Split method:** {'Stratified' if split_method == 'stratified' else 'Random'}")
                st.markdown(f"**Problem type:** {problem_type}")
                st.markdown(f"**Test percentage:** {test_size*100:.1f}%")
                st.markdown(f"**Number of features:** {len(X_train.columns)}")
                
                # Display class balance information for classification problems
                if is_classification:
                    st.markdown("### Class Distribution")
                    
                    # For binary classification, show class balance
                    if is_binary_classification:
                        # Get class labels
                        classes = y.unique()
                        
                        # Create a DataFrame for the class distribution
                        class_dist = pd.DataFrame({
                            'Class': classes,
                            'Training set': [y_train.value_counts().get(cls, 0) for cls in classes],
                            'Testing set': [y_test.value_counts().get(cls, 0) for cls in classes]
                        })
                        
                        # Calculate percentages
                        class_dist['Training %'] = class_dist['Training set'] / len(y_train) * 100
                        class_dist['Testing %'] = class_dist['Testing set'] / len(y_test) * 100
                        
                        # Display the distribution table
                        st.table(class_dist)
                        
                        # Provide interpretation
                        max_diff = max(abs(class_dist['Training %'] - class_dist['Testing %']))
                        if max_diff < 5:
                            st.success("✅ Class balance is well-maintained between training and testing sets.")
                        elif max_diff < 10:
                            st.info("ℹ️ Minor differences in class distribution between training and testing sets.")
                        else:
                            st.warning("⚠️ Notable differences in class distribution between sets. This might affect model evaluation.")
                    # For multi-class classification
                    elif is_multiclass_classification:
                        # Get class labels
                        classes = y.unique()
                        
                        # Create a DataFrame for the class distribution
                        class_dist = pd.DataFrame({
                            'Class': classes,
                            'Training set': [y_train.value_counts().get(cls, 0) for cls in classes],
                            'Testing set': [y_test.value_counts().get(cls, 0) for cls in classes]
                        })
                        
                        # Calculate percentages
                        class_dist['Training %'] = class_dist['Training set'] / len(y_train) * 100
                        class_dist['Testing %'] = class_dist['Testing set'] / len(y_test) * 100
                        
                        # Display the distribution table
                        st.dataframe(class_dist)
                        
                        # Provide interpretation
                        max_diff = max(abs(class_dist['Training %'] - class_dist['Testing %']))
                        if max_diff < 5:
                            st.success("✅ Class balance is well-maintained between training and testing sets.")
                        elif max_diff < 10:
                            st.info("ℹ️ Minor differences in class distribution between training and testing sets.")
                        else:
                            st.warning("⚠️ Notable differences in class distribution between sets. This might affect model evaluation.") 
                        
            st.subheader("Training Data Overview")
            # Use the DatasetOverviewComponent to display dataset overview
            dataset_overview = DatasetOverviewComponent(st.session_state.builder.training_data, st.session_state.logger)
            dataset_overview.display_overview()            # Display the class distribution for the training and testing sets

            # Store original training data for Final Data Review comparison (temporary until next stage)
            if 'tts_original_data' not in st.session_state:
                st.session_state.tts_original_data = st.session_state.builder.training_data.copy()
                
            # Also store metadata for additional context
            if 'tts_split_metadata' not in st.session_state:
                st.session_state.tts_split_metadata = {
                    'split_time': pd.Timestamp.now(),
                    'training_shape': st.session_state.builder.training_data.shape,
                    'testing_shape': st.session_state.builder.testing_data.shape,
                    'test_size': test_size,
                    'split_method': split_method
                }

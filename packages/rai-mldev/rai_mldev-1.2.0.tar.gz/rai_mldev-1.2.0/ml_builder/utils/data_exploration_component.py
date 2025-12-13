import streamlit as st
from components.data_exploration.feature_relationships import FeatureRelationshipsComponent
from components.data_exploration.feature_analysis import show_feature_analysis, get_visualisation_info
from components.data_exploration.target_feature_analysis import analyse_feature_relationships, display_target_distribution
from utils.dataset_overview import DatasetOverviewComponent
import pandas as pd
from typing import Optional

class DataExplorationComponent:
    """
    A component for data exploration that provides different types of analysis through a popover interface.
    
    This component allows users to explore:
    - Feature-Target Relationships
    - Feature Analysis
    - Feature Associations
    - Correlation Groups Analysis
    - Feature Relationships
    
    Example usage:
    ```python
    # Using builder's data
    data_explorer = DataExplorationComponent(builder, logger)
    data_explorer.render()
    
    # Using custom dataframe
    custom_df = pd.DataFrame(...)
    data_explorer = DataExplorationComponent(builder, logger, data=custom_df)
    data_explorer.render()
    ```
    """
    
    def __init__(self, builder, logger, data: Optional[pd.DataFrame] = None, target_column: Optional[str] = None):
        """
        Initialize the DataExplorationComponent.
        
        Args:
            builder: The Builder instance containing data and model building methods
            logger: The Logger instance for tracking actions and errors
            data: Optional pandas DataFrame to use instead of builder's data
            target_column: Optional target column name to use instead of builder's target column
        """
        self.builder = builder
        self.logger = logger
        self.data = data if data is not None else self.builder.data
        self.target_column = target_column if target_column is not None else self.builder.target_column

    def render(self):
        """
        Render the data exploration interface with a popover containing different analysis options.
        """
        #with st.popover("Data Exploration", icon=":material/info:"):
            
        # Use the DatasetOverviewComponent to display dataset overview
        dataset_overview = DatasetOverviewComponent(self.data, self.logger,keyidentifier="data_exploration")
        dataset_overview.display_overview()

        # Create pills for different types of analysis
        selected_section = st.pills(
            "Choose Analysis Section",
            ["Feature-Target Relationships",
            "Feature Analysis",
            "Correlation/Association Analysis",
            "Feature Relationships"],
            key="analysis_section",
            default="Feature-Target Relationships"
        )
        
        # Feature Relationships Component initialization
        feature_relationships = FeatureRelationshipsComponent(
            self.builder, 
            self.logger, 
            self.data, 
            self.target_column
        )
        
        # Display the selected analysis section
        if selected_section == "Feature-Target Relationships":
            display_target_distribution(self.data, self.target_column)
            analyse_feature_relationships(self.data, self.target_column)
        elif selected_section == "Feature Analysis":
            get_visualisation_info()
            show_feature_analysis(self.data, self.target_column)
        elif selected_section == "Correlation/Association Analysis":
            summary = feature_relationships.display_feature_associations_analysis()
        
            feature_relationships.display_correlation_group_analysis(summary)
        
        elif selected_section == "Feature Relationships":
            feature_relationships.display_detailed_feature_relationship_analysis() 
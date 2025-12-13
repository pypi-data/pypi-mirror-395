import streamlit as st
import pandas as pd

def render_model_limitations(builder, limitations_result, importance_df=None):
    """Render the model limitations and recommendations section."""
    st.header("Model Limitations & Recommendations")
    
    # Add debugging information
    with st.expander("🔍 Debug Information", expanded=False):
        model_instance = builder.model["model"]
        st.write(f"Model type: {type(model_instance).__name__}")
        st.write(f"Has feature_importances_: {hasattr(model_instance, 'feature_importances_')}")
        st.write(f"Has coef_: {hasattr(model_instance, 'coef_')}")
        if hasattr(model_instance, "coef_"):
            st.write(f"Coefficients shape: {model_instance.coef_.shape}")
    
    if limitations_result["success"]:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("⚠️ Limitations")
            for limitation in limitations_result.get("limitations", []):
                st.warning(limitation)
            
            st.subheader("🚨 Warnings")
            for warning in limitations_result.get("warnings", []):
                # Check if this is a low importance feature warning
                if "low importance" in warning.lower():
                    try:
                        # Use same threshold as analyse_model_limitations (0.01)
                        low_importance_threshold = 0.01
                        low_importance_features = importance_df[importance_df['importance'] < low_importance_threshold]['feature'].tolist()
                        
                        if low_importance_features:
                            st.error(
                                f"{warning}\n\n"
                                "**Low importance features:**\n" + 
                                "\n".join([f"- {feature} (importance: {importance_df[importance_df['feature'] == feature]['importance'].iloc[0]:.4f})" 
                                         for feature in low_importance_features])
                            )
                    except Exception as e:
                        st.error(f"Error processing low importance features: {str(e)}")
                # Add handling for correlation warnings
                elif "correlation" in warning.lower():
                    if "correlations" in limitations_result:
                        st.error(
                            f"{warning}\n\n"
                            "**Highly correlated feature pairs:**\n" +
                            "\n".join([f"- {corr['feature1']} & {corr['feature2']} (correlation: {corr['correlation']:.2f})"
                                     for corr in limitations_result["correlations"]])
                        )
                else:
                    st.error(warning)
        
        with col2:
            st.subheader("💡 Recommendations")
            recommendations_list = []
            for recommendation in limitations_result.get("recommendations", []):
                st.info(recommendation)
                recommendations_list.append(recommendation)
                
                # Add specific recommendations for low importance features
                if "feature selection" in recommendation.lower() and importance_df is not None:
                    try:
                        # Use same threshold as analyse_model_limitations (0.01)
                        low_importance_threshold = 0.01
                        low_importance_features = importance_df[importance_df['importance'] < low_importance_threshold]['feature'].tolist()
                        if low_importance_features:
                            st.info(
                                "**Consider removing or combining these low importance features:**\n" +
                                "\n".join([f"- {feature} (importance: {importance_df[importance_df['feature'] == feature]['importance'].iloc[0]:.4f})" 
                                         for feature in low_importance_features])
                            )
                    except Exception as e:
                        st.error(f"Error processing feature recommendations: {str(e)}")
            
            # Create Journey point for all recommendations (outside the loop)
            if recommendations_list:
                st.session_state.logger.log_journey_point(
                    stage="MODEL_EXPLANATION",
                    decision_type="MODEL_LIMITATIONS_RECOMMENDATIONS",
                    description="Model Limitations Analysis and Recommendations",
                    details={
                        "Limitations": limitations_result.get("limitations", []),
                        "Warnings": limitations_result.get("warnings", [])
                    },
                    parent_id=None
                )
    else:
        st.error(f"Failed to analyse model limitations: {limitations_result.get('message', 'Unknown error')}")
        if 'message' in limitations_result:
            st.write("Error details:", limitations_result['message'])
        st.session_state.logger.log_error(
            "Limitations Analysis Failed",
            {"error": limitations_result.get("message", "Unknown error")}
        ) 
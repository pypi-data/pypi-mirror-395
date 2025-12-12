"""
Report Generator Utility

This module provides comprehensive report generation functionality for scenario comparisons
in the ML Builder application. Supports multiple output formats including PDF, Text, and JSON.
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional
from io import BytesIO

# Optional PDF support
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling numpy and special types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bool):
            return str(obj)
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


class ScenarioComparisonReportGenerator:
    """
    Generates comprehensive comparison reports between two scenarios in multiple formats.
    
    Supported formats:
    - PDF: Professional formatted report with tables and styling
    - Text: Human-readable plain text format
    - JSON: Machine-readable structured data format
    """
    
    def __init__(self):
        self.pdf_available = PDF_AVAILABLE
    
    def create_comprehensive_report_data(
        self, 
        scenario1: str, 
        scenario2: str, 
        data1: Dict[str, Any], 
        data2: Dict[str, Any], 
        pred_diff: float, 
        pred_diff_pct: float,
        diff_features: List[Dict[str, Any]], 
        all_feature_impacts: Dict[str, Any],
        model_type: str = "unknown",
        problem_type: str = "unknown",
        shap_values1: Optional[Any] = None, 
        shap_values2: Optional[Any] = None,
        shap_diff: Optional[Any] = None,
        model_feature_importances: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Create a comprehensive report data structure from all analysis results."""
        
        # Build the complete report structure
        report = {
            "metadata": {
                "report_type": "Scenario Comparison",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model_type": model_type,
                "problem_type": problem_type,
                "feature_count": len(set(list(data1['values'].keys()) + list(data2['values'].keys())))
            },
            "comparison_summary": {
                "scenario1": {
                    "name": scenario1,
                    "prediction": float(data1['prediction']),
                    "feature_count": len(data1['values'])
                },
                "scenario2": {
                    "name": scenario2,
                    "prediction": float(data2['prediction']),
                    "feature_count": len(data2['values'])
                },
                "prediction_difference": {
                    "absolute": float(pred_diff),
                    "percentage": float(pred_diff_pct)
                },
                "different_features": {
                    "count": len(diff_features),
                    "with_impact_analysis": len(all_feature_impacts)
                }
            },
            "scenarios": {
                scenario1: data1['values'],
                scenario2: data2['values']
            },
            "feature_differences": {}
        }
        
        # Add comprehensive feature differences
        all_features = set(list(data1['values'].keys()) + list(data2['values'].keys()))
        for feature in all_features:
            feature_diff = {
                "scenario1_value": data1['values'].get(feature, "Missing"),
                "scenario2_value": data2['values'].get(feature, "Missing"),
            }
            
            # Add numeric difference if applicable
            if (feature in data1['values'] and feature in data2['values'] and
                isinstance(data1['values'][feature], (int, float)) and 
                isinstance(data2['values'][feature], (int, float))):
                
                numeric_diff = float(data2['values'][feature]) - float(data1['values'][feature])
                feature_diff["difference"] = numeric_diff
                
                # Add percentage change if possible
                if float(data1['values'][feature]) != 0:
                    pct_change = (numeric_diff / float(data1['values'][feature])) * 100
                    feature_diff["percentage_change"] = float(pct_change)
            else:
                feature_diff["difference"] = "N/A"
            
            # Add individual feature impact if available
            if feature in all_feature_impacts:
                impact_data = all_feature_impacts[feature].copy()
                # Ensure JSON serializable
                if "same_direction" in impact_data:
                    impact_data["same_direction"] = str(impact_data["same_direction"])
                feature_diff["isolated_impact"] = impact_data
            
            # Add SHAP values if available
            if shap_diff is not None and shap_values1 is not None and shap_values2 is not None:
                try:
                    feature_list = list(data1['values'].keys())
                    if feature in feature_list:
                        feature_index = feature_list.index(feature)
                        if feature_index < len(shap_diff):
                            feature_diff["shap"] = {
                                "scenario1": float(shap_values1[0][feature_index]),
                                "scenario2": float(shap_values2[0][feature_index]),
                                "difference": float(shap_diff[feature_index])
                            }
                except (ValueError, IndexError, TypeError):
                    pass  # Skip SHAP data if there's an issue
            
            report["feature_differences"][feature] = feature_diff
        
        # Add model information if available
        if model_feature_importances:
            report["model_info"] = {
                "feature_importances": model_feature_importances
            }
        
        return report
    
    def generate_text_report(self, report_data: Dict[str, Any]) -> str:
        """Convert the report data dictionary into a well-formatted text report."""
        
        lines = []
        
        # Header
        lines.extend([
            "="*80,
            "SCENARIO COMPARISON REPORT",
            "="*80,
            "",
        ])
        
        # Metadata
        metadata = report_data.get("metadata", {})
        lines.extend([
            "REPORT INFORMATION",
            "-" * 20,
            f"Generated: {metadata.get('created_at', 'Unknown')}",
            f"Report Type: {metadata.get('report_type', 'Unknown')}",
            f"Model Type: {metadata.get('model_type', 'Unknown')}",
            f"Problem Type: {metadata.get('problem_type', 'Unknown')}",
            f"Features Analyzed: {metadata.get('feature_count', 'Unknown')}",
            "",
        ])
        
        # Comparison Summary
        summary = report_data.get("comparison_summary", {})
        scenario1_data = summary.get("scenario1", {})
        scenario2_data = summary.get("scenario2", {})
        diff_data = summary.get("prediction_difference", {})
        
        lines.extend([
            "PREDICTION COMPARISON SUMMARY",
            "-" * 30,
            f"Scenario 1: {scenario1_data.get('name', 'Unknown')}",
            f"  • Prediction: {scenario1_data.get('prediction', 0):.4f}",
            f"  • Features: {scenario1_data.get('feature_count', 0)}",
            "",
            f"Scenario 2: {scenario2_data.get('name', 'Unknown')}",
            f"  • Prediction: {scenario2_data.get('prediction', 0):.4f}",
            f"  • Features: {scenario2_data.get('feature_count', 0)}",
            "",
            f"Prediction Difference:",
            f"  • Absolute: {diff_data.get('absolute', 0):+.4f}",
            f"  • Percentage: {diff_data.get('percentage', 0):+.2f}%",
            "",
        ])
        
        # Feature Differences
        feature_diffs = report_data.get("feature_differences", {})
        if feature_diffs:
            lines.extend([
                "DETAILED FEATURE ANALYSIS",
                "-" * 25,
                "",
            ])
            
            # Group features by whether they have impacts or not
            features_with_impact = []
            features_without_impact = []
            
            for feature, data in feature_diffs.items():
                if 'isolated_impact' in data:
                    features_with_impact.append((feature, data))
                else:
                    features_without_impact.append((feature, data))
            
            # Sort features with impact by importance
            if features_with_impact:
                features_with_impact.sort(key=lambda x: abs(x[1]['isolated_impact'].get('feature_impact', 0)), reverse=True)
                
                lines.extend([
                    "Features with Isolated Impact Analysis:",
                    "",
                ])
                
                for feature, data in features_with_impact:
                    val1 = data.get('scenario1_value', 'N/A')
                    val2 = data.get('scenario2_value', 'N/A')
                    diff = data.get('difference', 'N/A')
                    
                    impact_data = data.get('isolated_impact', {})
                    feature_impact = impact_data.get('feature_impact', 0)
                    impact_direction = impact_data.get('impact_direction', 'unknown')
                    importance_score = impact_data.get('importance_score', 0)
                    
                    lines.extend([
                        f"📊 {feature}",
                        f"   Values: {val1} → {val2} (Δ: {diff})",
                        f"   Impact: {feature_impact:+.4f} ({impact_direction})",
                        f"   Importance: {importance_score:.1f}%",
                        "",
                    ])
            
            # Features without impact analysis
            if features_without_impact:
                lines.extend([
                    "Other Changed Features:",
                    "",
                ])
                
                for feature, data in features_without_impact:
                    val1 = data.get('scenario1_value', 'N/A')
                    val2 = data.get('scenario2_value', 'N/A')
                    diff = data.get('difference', 'N/A')
                    
                    lines.extend([
                        f"• {feature}: {val1} → {val2} (Δ: {diff})",
                    ])
                
                lines.append("")
        
        # Model Information
        model_info = report_data.get("model_info", {})
        if model_info and 'feature_importances' in model_info:
            lines.extend([
                "MODEL FEATURE IMPORTANCES",
                "-" * 25,
                "",
            ])
            
            # Sort by importance
            importances = model_info['feature_importances']
            sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)
            
            for feature, importance in sorted_features[:10]:  # Top 10
                lines.append(f"• {feature}: {importance:.4f}")
            
            lines.append("")
        
        # Footer
        lines.extend([
            "",
            "="*80,
            "END OF REPORT",
            "="*80,
        ])
        
        return "\n".join(lines)
    
    def generate_json_report(self, report_data: Dict[str, Any]) -> str:
        """Generate a JSON report from the report data."""
        return json.dumps(report_data, indent=2, cls=CustomJSONEncoder)
    
    def generate_report(
        self, 
        format_type: str,
        scenario1: str, 
        scenario2: str, 
        data1: Dict[str, Any], 
        data2: Dict[str, Any], 
        pred_diff: float, 
        pred_diff_pct: float,
        diff_features: List[Dict[str, Any]], 
        all_feature_impacts: Dict[str, Any],
        model_type: str = "unknown",
        problem_type: str = "unknown",
        shap_values1: Optional[Any] = None, 
        shap_values2: Optional[Any] = None,
        shap_diff: Optional[Any] = None,
        model_feature_importances: Optional[Dict[str, float]] = None
    ) -> tuple[str, str, Any]:
        """
        Generate a complete report in the specified format.
        
        Returns:
            tuple: (filename, mime_type, file_data)
        """
        
        # STEP 1: Always create the comprehensive JSON data first (single source of truth)
        json_report_data = self.create_comprehensive_report_data(
            scenario1, scenario2, data1, data2, pred_diff, pred_diff_pct,
            diff_features, all_feature_impacts, model_type, problem_type,
            shap_values1, shap_values2, shap_diff, model_feature_importances
        )
        
        base_filename = f"comparison_{scenario1}_vs_{scenario2}"
        
        # STEP 2: Generate the requested format from the JSON data
        if format_type.lower().startswith("pdf"):
            if not self.pdf_available:
                raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
            
            pdf_buffer = self.generate_pdf_from_json(json_report_data)
            return f"{base_filename}.pdf", "application/pdf", pdf_buffer.getvalue()
            
        elif format_type.lower().startswith("text"):
            text_report = self.generate_text_report(json_report_data)
            return f"{base_filename}.txt", "text/plain", text_report
            
        elif format_type.lower().startswith("json"):
            json_report = self.generate_json_report(json_report_data)
            return f"{base_filename}.json", "application/json", json_report
            
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
    
    def generate_pdf_from_json(self, json_data: Dict[str, Any]) -> BytesIO:
        """Generate PDF report from JSON data structure - improved and comprehensive approach."""
        
        if not self.pdf_available:
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=0.75*inch, rightMargin=0.75*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading1']
        subheading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Create custom styles
        small_style = ParagraphStyle(
            'Small',
            parent=normal_style,
            fontSize=8,
            spaceAfter=6,
        )
        
        # Build story (content)
        story = []
        
        # Title
        story.append(Paragraph("Scenario Comparison Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Metadata section
        metadata = json_data.get("metadata", {})
        story.append(Paragraph("Report Information", heading_style))
        
        info_data = [
            ["Generated:", metadata.get('created_at', 'Unknown')],
            ["Report Type:", metadata.get('report_type', 'Scenario Comparison')],
            ["Model Type:", metadata.get('model_type', 'Unknown')],
            ["Problem Type:", metadata.get('problem_type', 'Unknown')],
            ["Features Analyzed:", str(metadata.get('feature_count', 'Unknown'))],
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Comparison Summary section
        story.append(Paragraph("Prediction Comparison Summary", heading_style))
        
        summary = json_data.get("comparison_summary", {})
        scenario1_data = summary.get("scenario1", {})
        scenario2_data = summary.get("scenario2", {})
        diff_data = summary.get("prediction_difference", {})
        
        # Create comparison table
        comparison_data = [
            ["Metric", scenario1_data.get('name', 'Scenario 1'), scenario2_data.get('name', 'Scenario 2'), "Difference"],
            ["Prediction Value", 
             f"{scenario1_data.get('prediction', 0):.4f}", 
             f"{scenario2_data.get('prediction', 0):.4f}", 
             f"{diff_data.get('absolute', 0):+.4f}"],
            ["Feature Count", 
             str(scenario1_data.get('feature_count', 0)), 
             str(scenario2_data.get('feature_count', 0)), 
             ""],
            ["Percentage Change", "", "", f"{diff_data.get('percentage', 0):+.2f}%"],
        ]
        
        comparison_table = Table(comparison_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.3*inch])
        comparison_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(comparison_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Feature Analysis section
        feature_diffs = json_data.get("feature_differences", {})
        if feature_diffs:
            story.append(Paragraph("Detailed Feature Analysis", heading_style))
            
            # Separate features into those with and without isolated impact analysis
            features_with_impact = []
            features_with_changes = []
            
            for feature_name, feature_data in feature_diffs.items():
                val1 = feature_data.get('scenario1_value', 'N/A')
                val2 = feature_data.get('scenario2_value', 'N/A')
                diff = feature_data.get('difference', 'N/A')
                
                # Skip if no meaningful change
                if val1 == val2 and diff in ['N/A', 0, '0']:
                    continue
                
                # Check if feature has isolated impact analysis
                isolated_impact = feature_data.get('isolated_impact', {})
                if isolated_impact and 'feature_impact' in isolated_impact:
                    features_with_impact.append((feature_name, feature_data, isolated_impact))
                elif val1 != val2:  # Only include if values actually changed
                    features_with_changes.append((feature_name, feature_data))
            
            # Section 1: Features with Impact Analysis
            if features_with_impact:
                story.append(Paragraph("Features with Isolated Impact Analysis", subheading_style))
                story.append(Paragraph("These features have been analyzed to show their individual impact on the prediction difference.", small_style))
                
                # Sort by absolute impact
                features_with_impact.sort(key=lambda x: abs(x[2].get('feature_impact', 0)), reverse=True)
                
                impact_table_data = [
                    ["Feature", "Value Change", "Prediction Impact", "Direction", "Importance"]
                ]
                
                for feature_name, feature_data, impact_data in features_with_impact:
                    val1 = feature_data.get('scenario1_value', 'N/A')
                    val2 = feature_data.get('scenario2_value', 'N/A')
                    
                    # Format value change
                    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                        diff_val = val2 - val1
                        value_change = f"{val1:.3f} → {val2:.3f} ({diff_val:+.3f})"
                    else:
                        value_change = f"{str(val1)[:8]} → {str(val2)[:8]}"
                    
                    # Get impact data
                    feature_impact = impact_data.get('feature_impact', 0)
                    importance_score = impact_data.get('importance_score', 0)
                    same_direction = impact_data.get('same_direction', True)
                    
                    direction = "Supporting ✓" if same_direction else "Opposing ✗"
                    
                    impact_table_data.append([
                        str(feature_name)[:15],
                        value_change[:20],
                        f"{feature_impact:+.4f}",
                        direction,
                        f"{importance_score:.1f}%"
                    ])
                
                impact_table = Table(impact_table_data, colWidths=[1.3*inch, 1.8*inch, 1*inch, 1*inch, 0.7*inch])
                impact_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                
                story.append(impact_table)
                story.append(Spacer(1, 0.2*inch))
            
            # Section 2: Other Changed Features
            if features_with_changes:
                story.append(Paragraph("Other Changed Features", subheading_style))
                story.append(Paragraph("These features changed between scenarios but do not have isolated impact analysis.", small_style))
                
                change_table_data = [
                    ["Feature", "Scenario 1 Value", "Scenario 2 Value", "Difference"]
                ]
                
                for feature_name, feature_data in features_with_changes:
                    val1 = feature_data.get('scenario1_value', 'N/A')
                    val2 = feature_data.get('scenario2_value', 'N/A')
                    diff = feature_data.get('difference', 'N/A')
                    
                    # Format values for display
                    val1_str = f"{val1:.4f}" if isinstance(val1, (int, float)) else str(val1)[:10]
                    val2_str = f"{val2:.4f}" if isinstance(val2, (int, float)) else str(val2)[:10]
                    diff_str = f"{diff:+.4f}" if isinstance(diff, (int, float)) else str(diff)[:10]
                    
                    change_table_data.append([
                        str(feature_name)[:15],
                        val1_str,
                        val2_str,
                        diff_str
                    ])
                
                change_table = Table(change_table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.3*inch])
                change_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                
                story.append(change_table)
                story.append(Spacer(1, 0.2*inch))
            
            # Add summary if no features found
            if not features_with_impact and not features_with_changes:
                story.append(Paragraph("No significant feature differences found between the scenarios.", normal_style))
                story.append(Spacer(1, 0.2*inch))
        
        # SHAP Analysis section (if available)
        shap_features = []
        for feature_name, feature_data in feature_diffs.items():
            if 'shap' in feature_data:
                shap_features.append((feature_name, feature_data['shap']))
        
        if shap_features:
            story.append(Paragraph("SHAP Value Analysis", subheading_style))
            story.append(Paragraph("SHAP values show how each feature contributes to the model's prediction.", small_style))
            
            # Sort by absolute SHAP difference
            shap_features.sort(key=lambda x: abs(x[1].get('difference', 0)), reverse=True)
            
            shap_table_data = [
                ["Feature", "Scenario 1 SHAP", "Scenario 2 SHAP", "SHAP Difference"]
            ]
            
            for feature_name, shap_data in shap_features[:15]:  # Top 15 features
                shap1 = shap_data.get('scenario1', 0)
                shap2 = shap_data.get('scenario2', 0)
                shap_diff = shap_data.get('difference', 0)
                
                shap_table_data.append([
                    str(feature_name)[:15],
                    f"{shap1:+.4f}",
                    f"{shap2:+.4f}",
                    f"{shap_diff:+.4f}"
                ])
            
            shap_table = Table(shap_table_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
            shap_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            story.append(shap_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Model Feature Importances section
        model_info = json_data.get("model_info", {})
        if model_info and 'feature_importances' in model_info:
            story.append(Paragraph("Model Feature Importances", subheading_style))
            story.append(Paragraph("Overall feature importance scores from the trained model (top 15 features).", small_style))
            
            importances = model_info['feature_importances']
            sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:15]
            
            importance_data = [["Feature", "Importance Score"]]
            for feature, importance in sorted_features:
                importance_data.append([
                    str(feature)[:20],
                    f"{importance:.4f}"
                ])
            
            importance_table = Table(importance_data, colWidths=[3*inch, 1.5*inch])
            importance_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            story.append(importance_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Summary and Insights section
        story.append(Paragraph("Summary", heading_style))
        
        summary_text = f"""
        This report compares two scenarios: '{scenario1_data.get('name', 'Scenario 1')}' and '{scenario2_data.get('name', 'Scenario 2')}'. 
        The prediction difference is {diff_data.get('absolute', 0):+.4f} ({diff_data.get('percentage', 0):+.2f}%).
        
        """
        
        if features_with_impact:
            summary_text += f"• {len(features_with_impact)} features have detailed impact analysis\n"
        if features_with_changes:
            summary_text += f"• {len(features_with_changes)} additional features show value changes\n"
        if shap_features:
            summary_text += f"• SHAP analysis available for {len(shap_features)} features\n"
        
        summary_text += f"\nGenerated on {metadata.get('created_at', 'Unknown')} using {metadata.get('model_type', 'Unknown')} model."
        
        story.append(Paragraph(summary_text, normal_style))
        
        # Build PDF
        try:
            doc.build(story)
        except Exception as e:
            # If there's an error building the PDF, create a simple error report
            error_story = [
                Paragraph("PDF Generation Error", title_style),
                Paragraph(f"An error occurred while generating the detailed report: {str(e)}", normal_style),
                Paragraph("Basic Information:", heading_style),
                Paragraph(f"Scenarios: {scenario1_data.get('name', 'Unknown')} vs {scenario2_data.get('name', 'Unknown')}", normal_style),
                Paragraph(f"Prediction Difference: {diff_data.get('absolute', 0):+.4f}", normal_style),
            ]
            doc.build(error_story)
        
        # Reset buffer position
        buffer.seek(0)
        return buffer


# Convenience function for easy importing
def create_scenario_comparison_report(
    format_type: str,
    scenario1: str, 
    scenario2: str, 
    data1: Dict[str, Any], 
    data2: Dict[str, Any], 
    pred_diff: float, 
    pred_diff_pct: float,
    diff_features: List[Dict[str, Any]], 
    all_feature_impacts: Dict[str, Any],
    model_type: str = "unknown",
    problem_type: str = "unknown",
    shap_values1: Optional[Any] = None, 
    shap_values2: Optional[Any] = None,
    shap_diff: Optional[Any] = None,
    model_feature_importances: Optional[Dict[str, float]] = None
) -> tuple[str, str, Any]:
    """
    Convenience function to generate a scenario comparison report.
    
    Returns:
        tuple: (filename, mime_type, file_data)
    """
    generator = ScenarioComparisonReportGenerator()
    return generator.generate_report(
        format_type, scenario1, scenario2, data1, data2, pred_diff, pred_diff_pct,
        diff_features, all_feature_impacts, model_type, problem_type,
        shap_values1, shap_values2, shap_diff, model_feature_importances
    ) 
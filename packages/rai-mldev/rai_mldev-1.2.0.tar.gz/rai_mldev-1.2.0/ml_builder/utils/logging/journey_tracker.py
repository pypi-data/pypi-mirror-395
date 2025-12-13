from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import numpy as np

@dataclass
class JourneyPoint:
    timestamp: datetime
    stage: str
    decision_type: str  # e.g., 'MODEL_SELECTION', 'PREPROCESSING', 'EVALUATION'
    description: str
    details: Dict[str, Any]
    parent_id: Optional[str] = None
    branch_number: int = 0  # 0 = main path, 1+ = branch numbers
    
class MLJourneyTracker:
    def __init__(self):
        self.journey_points = []
        self.graph = nx.DiGraph()
        self.last_node_id = None  # Track the last created node
        self.stage_to_latest_node = {}  # Map stage to the most recent node ID for that stage
        self.current_branch_number = 0  # Track the current branch number (0 = main path)
        
        # Define stage order for hierarchical layout
        self.stage_order = [
            'DATA_LOADING',
            'DATA_EXPLORATION', 
            'DATA_PREPROCESSING',
            'FEATURE_SELECTION',
            'MODEL_SELECTION',
            'MODEL_TRAINING',
            'MODEL_EVALUATION',
            'MODEL_EXPLANATION'
        ]
        
    def _is_duplicate(self, point: JourneyPoint) -> bool:
        """Check if a point is a duplicate within recent points."""
        if not self.journey_points:
            return False
            
        # Check last few points for duplicates
        check_range = min(5, len(self.journey_points))
        for i in range(len(self.journey_points) - check_range, len(self.journey_points)):
            existing_point = self.journey_points[i]
            
            # Check if this is identical to an existing point
            if (existing_point.stage == point.stage and 
                existing_point.decision_type == point.decision_type and 
                existing_point.description == point.description and
                existing_point.details == point.details):
                return True
                    
        return False
    
    def _find_parent_for_stage(self, target_stage: str) -> Optional[str]:
        """Find the optimal parent node for the target stage.
        
        For branching: find the most recent node from the latest stage that 
        comes at or before the target stage in progression.
        For linear progression: use the last node.
        """
        if not self.journey_points:
            return None
            
        try:
            target_stage_idx = self.stage_order.index(target_stage)
        except ValueError:
            # Unknown stage - use last node
            return self.last_node_id
        
        # Find the most recent node from a stage at or before the target stage
        for i in range(len(self.journey_points) - 1, -1, -1):
            point = self.journey_points[i]
            point_stage = point.stage
            
            try:
                point_stage_idx = self.stage_order.index(point_stage)
                
                # If this point's stage comes at or before the target stage, it's a valid parent
                if point_stage_idx <= target_stage_idx:
                    return str(i)
                        
            except ValueError:
                # Unknown stage - skip
                continue
        
        # Fallback to the last node if nothing suitable found
        return self.last_node_id
    
    def _is_going_backwards(self, target_stage: str) -> bool:
        """Simple check: are we going backwards in stage order?
        
        Args:
            target_stage: The stage we're considering adding a decision to
            
        Returns:
            bool: True if this represents going backwards in stage order
        """
        if not self.journey_points:
            return False  # First decision is never backwards
            
        # Get the stage of the last decision
        last_point = self.journey_points[-1]
        last_stage = last_point.stage
        
        # If we're continuing in the same stage, it's not going backwards
        if target_stage == last_stage:
            return False
            
        # Check stage order positions
        try:
            target_idx = self.stage_order.index(target_stage)
            last_idx = self.stage_order.index(last_stage)
            
            # If target stage comes before the last stage, we're going backwards
            return target_idx < last_idx
            
        except ValueError:
            # Unknown stages - assume not going backwards
            return False
    
    def add_decision(self, stage: str, decision_type: str, description: str, 
                    details: Dict[str, Any], parent_id: Optional[str] = None) -> Optional[str]:
        """Add a new decision point with simple branching logic.
        
        Simple branching rule: 
        - If the stage comes before the last stage in stage order, increment branch number
        - Keep that branch number until another backwards navigation happens
        
        Args:
            stage: The ML development stage (e.g., 'MODEL_SELECTION')
            decision_type: The type of decision made
            description: Human-readable description of the decision
            details: Technical details about the decision
            parent_id: Explicit parent node ID (if None, will be auto-determined)
            
        Returns:
            Optional[str]: The ID of the newly added node, or None if duplicate
        """
        # Simple branching logic: check if we're going backwards in stage order
        is_going_backwards = self._is_going_backwards(stage)
        
        # If going backwards, increment branch number
        if is_going_backwards:
            self.current_branch_number += 1
        
        # Determine parent
        if parent_id is None:
            parent_id = self._find_parent_for_stage(stage)

        point = JourneyPoint(
            timestamp=datetime.now(),
            stage=stage,
            decision_type=decision_type,
            description=description,
            details=details,
            parent_id=parent_id,
            branch_number=self.current_branch_number
        )
        
        # Check for duplicates
        if self._is_duplicate(point):
            return None
            
        self.journey_points.append(point)
        node_id = self._update_graph(point)
        
        # Update tracking variables
        self.last_node_id = node_id
        self.stage_to_latest_node[stage] = node_id
        
        return node_id
        
    def _update_graph(self, point: JourneyPoint) -> str:
        """Update the network graph with new point.
        
        Returns:
            str: The ID of the newly added node
        """
        node_id = f"{len(self.journey_points) - 1}"  # Subtract 1 since we already appended
        self.graph.add_node(
            node_id,
            timestamp=point.timestamp,
            stage=point.stage,
            decision_type=point.decision_type,
            description=point.description,
            details=point.details,
            branch_number=point.branch_number
        )
        
        if point.parent_id:
            self.graph.add_edge(point.parent_id, node_id)
            
        return node_id
    
    def _create_hierarchical_layout(self) -> Dict[str, Tuple[float, float]]:
        """Create a hierarchical layout that groups nodes by stages with clear separation and handles branching."""
        if not self.graph.nodes:
            return {}
        
        # Group nodes by stage
        stage_nodes = {stage: [] for stage in self.stage_order}
        for node_id, node_data in self.graph.nodes(data=True):
            stage = node_data.get('stage', 'UNKNOWN')
            if stage in stage_nodes:
                stage_nodes[stage].append(node_id)
            else:
                # Handle unknown stages
                if 'UNKNOWN' not in stage_nodes:
                    stage_nodes['UNKNOWN'] = []
                stage_nodes['UNKNOWN'].append(node_id)
        
        # Create positions with stage separation and branch handling
        pos = {}
        stage_width = 2.0  # Width allocated per stage
        
        for i, stage in enumerate(self.stage_order):
            nodes_in_stage = stage_nodes.get(stage, [])
            if not nodes_in_stage:
                continue
                
            # Calculate x position for this stage (left to right progression)
            stage_x = i * stage_width
            
            # Sort nodes by timestamp to maintain chronological order within stage
            nodes_with_timestamps = []
            for node_id in nodes_in_stage:
                timestamp = self.graph.nodes[node_id].get('timestamp', datetime.now())
                nodes_with_timestamps.append((node_id, timestamp))
            
            # Sort by timestamp
            nodes_with_timestamps.sort(key=lambda x: x[1])
            sorted_node_ids = [node_id for node_id, _ in nodes_with_timestamps]
            
            # Detect branches within this stage
            # A branch occurs when a node has a parent from an earlier stage (not the immediate previous node)
            branches = self._detect_branches_in_stage(sorted_node_ids, stage)
            
            # Arrange nodes within the stage with branch separation
            num_nodes = len(sorted_node_ids)
            if num_nodes == 1:
                # Single node centered
                pos[sorted_node_ids[0]] = (stage_x, 0)
            else:
                # Multiple nodes: distribute them considering branches
                self._position_nodes_with_branches(pos, sorted_node_ids, branches, stage_x)
        
        return pos
    
    def _detect_branches_in_stage(self, node_ids: List[str], stage: str) -> Dict[str, int]:
        """Detect which nodes in a stage represent branches using the new simple logic.
        
        Args:
            node_ids: List of node IDs in chronological order for this stage
            stage: The stage name
            
        Returns:
            Dict mapping node_id to branch_level (0 = main path, 1+ = branch levels)
        """
        branches = {}
        
        for node_id in node_ids:
            # Get the branch number from the graph node data
            node_data = self.graph.nodes[node_id]
            branch_number = node_data.get('branch_number', 0)
            branches[node_id] = branch_number
                    
        return branches
    
    def _position_nodes_with_branches(self, pos: Dict[str, Tuple[float, float]], 
                                    node_ids: List[str], branches: Dict[str, int], stage_x: float):
        """Position nodes within a stage using simple branch number grouping.
        
        Args:
            pos: Position dictionary to update
            node_ids: List of node IDs to position
            branches: Branch level mapping from _detect_branches_in_stage
            stage_x: X coordinate for this stage
        """
        if not node_ids:
            return
            
        # Group nodes by branch number
        branch_groups = {}
        for node_id in node_ids:
            branch_num = branches.get(node_id, 0)
            if branch_num not in branch_groups:
                branch_groups[branch_num] = []
            branch_groups[branch_num].append(node_id)
        
        # Calculate total vertical space needed
        total_groups = len(branch_groups)
        
        # Improved spacing calculation
        base_spacing = 3.0  # Base spacing between groups
        node_spacing = 0.8  # Spacing between nodes within a group
        
        # Calculate starting Y position
        if total_groups == 1:
            start_y = 0
        else:
            # Center the groups around Y=0
            total_height = (total_groups - 1) * base_spacing
            start_y = total_height / 2
        
        current_y = start_y
        
        # Sort branch groups by branch number (main path first)
        sorted_branch_nums = sorted(branch_groups.keys())
        
        for branch_num in sorted_branch_nums:
            nodes_in_group = branch_groups[branch_num]
            
            if len(nodes_in_group) == 1:
                # Single node in group
                pos[nodes_in_group[0]] = (stage_x, current_y)
            else:
                # Multiple nodes in group - spread them vertically
                for i, node_id in enumerate(nodes_in_group):
                    if len(nodes_in_group) == 1:
                        y_offset = 0
                    else:
                        # Distribute nodes within the group
                        group_span = (len(nodes_in_group) - 1) * node_spacing
                        y_offset = (i / (len(nodes_in_group) - 1) - 0.5) * group_span
                    pos[node_id] = (stage_x, current_y + y_offset)
            
            current_y -= base_spacing
    
    def get_journey_story(self) -> List[Dict[str, Any]]:
        """Generate a chronological story of the ML development journey with simple branch awareness."""
        story_points = []
        
        # Sort journey points by timestamp
        sorted_points = sorted(self.journey_points, key=lambda x: x.timestamp)
        
        # Track stage visits properly - only count when transitioning between stages
        stage_visit_count = {}
        last_stage = None
        
        for i, point in enumerate(sorted_points):
            stage = point.stage
            
            # Only increment visit count when transitioning to a different stage
            if stage != last_stage:
                stage_visit_count[stage] = stage_visit_count.get(stage, 0) + 1
                last_stage = stage
            
            # Determine if this is a branch using the simple branch number
            is_branch = point.branch_number > 0
            
            # Create branch indicator based on simple logic
            branch_indicator = ""
            if is_branch:
                if stage_visit_count[stage] > 1:
                    branch_indicator = f" (Visit #{stage_visit_count[stage]}, Branch {point.branch_number})"
                else:
                    branch_indicator = f" (Branch {point.branch_number})"
            
            story_point = {
                'step_number': i + 1,
                'timestamp': point.timestamp,
                'stage': point.stage.replace('_', ' ').title(),
                'decision_type': point.decision_type.replace('_', ' ').title() + branch_indicator,
                'description': point.description,
                'details': point.details,
                'stage_color': self._get_stage_color(point.stage),
                'is_branch': is_branch,
                'visit_number': stage_visit_count[stage],
                'branch_number': point.branch_number
            }
            story_points.append(story_point)
            
        return story_points
    
    def _get_stage_color(self, stage: str) -> str:
        """Get color for a given stage."""
        stage_colors = {
            'DATA_LOADING': '#e5e5e5',
            'DATA_EXPLORATION': '#dfa7a7',
            'DATA_PREPROCESSING': '#ed195a',
            'FEATURE_SELECTION': '#123e61',
            'MODEL_SELECTION': '#0c2230',
            'MODEL_TRAINING': '#78b659',
            'MODEL_EVALUATION': '#cca459',
            'MODEL_EXPLANATION': '#e19300',
        }
        return stage_colors.get(stage, '#455789')
        
    def generate_visualization(self, include_annotations: bool = False) -> go.Figure:
        """Generate an interactive visualization using plotly with improved stage separation and branch visualization.
        
        Args:
            include_annotations: Whether to include static text annotations (for exports)
        """
        if not self.graph.nodes:
            # Return empty figure if no nodes
            return go.Figure(layout=go.Layout(
                title='ML Development Journey Map (No data yet)',
                showlegend=False
            ))
            
        # Use hierarchical layout for better stage separation
        pos = self._create_hierarchical_layout()
        
        # Create stage background shapes
        stage_shapes = self._create_stage_backgrounds(pos)
        
        # Create different edge traces for main path vs branches
        main_edge_x, main_edge_y = [], []
        branch_edge_x, branch_edge_y = [], []
        
        for edge in self.graph.edges():
            source_node, target_node = edge[0], edge[1]
            x0, y0 = pos[source_node]
            x1, y1 = pos[target_node]
            
            # Determine if this is a branch edge using branch numbers
            source_branch = self.graph.nodes[source_node].get('branch_number', 0)
            target_branch = self.graph.nodes[target_node].get('branch_number', 0)
            is_branch = source_branch > 0 or target_branch > 0
            
            if is_branch:
                branch_edge_x.extend([x0, x1, None])
                branch_edge_y.extend([y0, y1, None])
            else:
                main_edge_x.extend([x0, x1, None])
                main_edge_y.extend([y0, y1, None])
        
        # Create main path edges (solid lines)
        main_edge_trace = go.Scatter(
            x=main_edge_x, y=main_edge_y,
            line=dict(width=3, color='#2E86AB'),
            hoverinfo='none',
            mode='lines',
            name='Main Path'
        )
        
        # Create branch edges (dashed lines)
        branch_edge_trace = go.Scatter(
            x=branch_edge_x, y=branch_edge_y,
            line=dict(width=2, color='#F24236', dash='dash'),
            hoverinfo='none',
            mode='lines',
            name='Branch Path'
        )
        
        # Create nodes with enhanced interactivity and branch indicators
        main_node_x, main_node_y = [], []
        branch_node_x, branch_node_y = [], []
        main_node_text, branch_node_text = [], []
        main_node_labels, branch_node_labels = [], []
        main_node_color, branch_node_color = [], []
        main_node_ids, branch_node_ids = [], []
        static_annotations = [] if include_annotations else []
        
        for node in self.graph.nodes():
            x, y = pos[node]
            
            # Get node data with default values if missing
            node_data = self.graph.nodes[node]
            stage = node_data.get('stage', 'UNKNOWN')
            decision_type = node_data.get('decision_type', 'UNKNOWN')
            description = node_data.get('description', 'No description available')
            details = node_data.get('details', {})
            timestamp = node_data.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
            
            # Determine if this is a branch node using the branch number
            branch_number = node_data.get('branch_number', 0)
            is_branch_node = branch_number > 0
            
            # Create detailed hover text with branch indicator
            if is_branch_node:
                branch_indicator = f" (Branch {branch_number})"
            else:
                branch_indicator = " (Main Path)"
            
            # Format details for hover display
            formatted_details = ""
            if details:
                detail_parts = []
                for key, value in details.items():
                    formatted_value = _format_detail_value_for_hover(value)
                    detail_parts.append(f"{key.replace('_', ' ').title()}: {formatted_value}")
                formatted_details = "<br>".join(detail_parts)
            else:
                formatted_details = "No technical details"
            
            hover_text = (
                f"<b>Stage:</b> {stage.replace('_', ' ').title()}<br>"
                f"<b>Action:</b> {decision_type.replace('_', ' ').title()}{branch_indicator}<br>"
                f"<b>Description:</b> {description}<br>"
                f"<b>Details:</b><br>{formatted_details}<br>"
                f"<b>Time:</b> {timestamp}<br>"
                f"<i>Click for full story details</i>"
            )
            
            # Create minimal node label
            action = decision_type.replace('_', ' ').title()
            if is_branch_node:
                action += " ↗"  # Add branch indicator to label
            
            # Create static annotation for exports
            if include_annotations:
                static_text = (
                    f"{action}<br>"
                    f"Stage: {stage.replace('_', ' ').title()}<br>"
                    f"Description: {description}<br>"
                    f"Time: {timestamp}"
                )
                static_annotations.append(
                    dict(
                        x=x,
                        y=y - 0.2,
                        text=static_text,
                        showarrow=False,
                        font=dict(size=8, color='#666'),
                        align='center',
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor='#ccc',
                        borderwidth=1
                    )
                )
            
            # Separate nodes by type
            if is_branch_node:
                branch_node_x.append(x)
                branch_node_y.append(y)
                branch_node_text.append(hover_text)
                branch_node_labels.append(action)
                branch_node_color.append(self._get_stage_color(stage))
                branch_node_ids.append(node)
            else:
                main_node_x.append(x)
                main_node_y.append(y)
                main_node_text.append(hover_text)
                main_node_labels.append(action)
                main_node_color.append(self._get_stage_color(stage))
                main_node_ids.append(node)
        
        # Create main path nodes (circles)
        main_node_trace = go.Scatter(
            x=main_node_x, y=main_node_y,
            mode='markers+text',
            hoverinfo='text',
            hovertext=main_node_text,
            text=main_node_labels,
            textposition="bottom center",
            textfont=dict(size=10, color='#333'),
            marker=dict(
                color=main_node_color,
                size=25,
                line_width=3,
                line=dict(color='white'),
                symbol='circle'
            ),
            customdata=main_node_ids,
            name="Main Path Steps"
        )
        
        # Create branch nodes (diamonds)
        branch_node_trace = go.Scatter(
            x=branch_node_x, y=branch_node_y,
            mode='markers+text',
            hoverinfo='text',
            hovertext=branch_node_text,
            text=branch_node_labels,
            textposition="bottom center",
            textfont=dict(size=9, color='#333'),
            marker=dict(
                color=branch_node_color,
                size=22,
                line_width=2,
                line=dict(color='#F24236'),
                symbol='diamond'
            ),
            customdata=branch_node_ids,
            name="Branch Steps"
        )
        
        # Create stage labels
        stage_annotations = self._create_stage_labels(pos)
        
        # Combine all annotations
        all_annotations = stage_annotations + static_annotations
        
        # Prepare traces
        traces = [main_edge_trace]
        if branch_edge_x:  # Only add branch edges if they exist
            traces.append(branch_edge_trace)
        traces.append(main_node_trace)
        if branch_node_x:  # Only add branch nodes if they exist
            traces.append(branch_node_trace)
        
        # Calculate dynamic dimensions based on content
        dynamic_layout = self._calculate_dynamic_layout(pos)
        
        # Create figure with enhanced layout
        fig = go.Figure(
            data=traces,
            layout=go.Layout(
                title=dict(
                    text='ML Development Journey Map with Branching',
                    #x=0.5,
                    #y=0.95,
                    font=dict(size=20)
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hovermode='closest',
                margin=dict(b=60, l=60, r=60, t=100),  # Increased margins for better spacing
                width=dynamic_layout['width'],
                height=dynamic_layout['height'],
                xaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False,
                    range=dynamic_layout['x_range']
                ),
                yaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False,
                    range=dynamic_layout['y_range']
                ),
                plot_bgcolor='#fafafa',
                shapes=stage_shapes,
                annotations=all_annotations,
                dragmode='pan'  # Enable panning for large journey maps
            )
        )
        
        return fig
    
    def _calculate_dynamic_layout(self, pos: Dict[str, Tuple[float, float]]) -> Dict[str, any]:
        """Calculate dynamic layout dimensions based on the content spread.
        
        Returns:
            Dict with width, height, x_range, and y_range for the plot
        """
        if not pos:
            return {
                'width': 800,
                'height': 600,
                'x_range': [-0.5, len(self.stage_order) * 2],
                'y_range': [-3, 3]
            }
        
        # Get all positions
        x_coords = [x for x, y in pos.values()]
        y_coords = [y for x, y in pos.values()]
        
        # Calculate ranges with padding
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Add padding around the content
        x_padding = 1.0
        y_padding = 2.0  # Extra padding for stage labels and node text
        
        x_range = [x_min - x_padding, x_max + x_padding]
        y_range = [y_min - y_padding, y_max + y_padding]
        
        # Calculate dimensions based on content spread
        x_span = x_range[1] - x_range[0]
        y_span = y_range[1] - y_range[0]
        
        # Base dimensions
        base_width = 1000
        base_height = 600
        
        # Scale width based on number of stages
        num_stages = len([stage for stage in self.stage_order 
                         if any(self.graph.nodes[node].get('stage') == stage for node in self.graph.nodes())])
        width = max(base_width, num_stages * 180 + 200)  # 180px per stage + margins
        
        # Scale height based on vertical spread and number of branch groups
        # Calculate the maximum number of groups in any stage for height scaling
        stage_node_groups = self._group_nodes_by_stage_and_branches(pos)
        max_groups_in_stage = max(len(groups) for groups in stage_node_groups.values()) if stage_node_groups else 1
        
        # Also calculate max nodes within any single group for finer spacing control
        max_nodes_in_group = 1
        for groups in stage_node_groups.values():
            for group_positions in groups.values():
                max_nodes_in_group = max(max_nodes_in_group, len(group_positions))
        
        # Height scales with both y-span and complexity
        height_for_spread = max(400, y_span * 100 + 250)  # Increased from 80 to 100px per unit + more margin
        height_for_complexity = max(400, max_groups_in_stage * 150 + 250)  # Increased from 120 to 150px per group
        height_for_density = max(400, max_nodes_in_group * 80 + 200)  # Additional scaling for dense groups
        height = max(base_height, height_for_spread, height_for_complexity, height_for_density)
        
        # Ensure reasonable limits
        width = min(width, 2000)  # Max width
        height = min(height, 1200)  # Max height
        
        return {
            'width': width,
            'height': height,
            'x_range': x_range,
            'y_range': y_range
        }
    
    def _create_stage_backgrounds(self, pos: Dict[str, Tuple[float, float]]) -> List[Dict]:
        """Create background shapes to visually separate stages with enhanced branch grouping.
        
        This method now creates separate background boxes for different branch groups
        within each stage, making it much clearer when there are multiple branches.
        """
        if not pos:
            return []
            
        shapes = []
        stage_width = 2.0
        
        # Group nodes by stage and then by branch groups
        stage_node_groups = self._group_nodes_by_stage_and_branches(pos)
        
        # Create background shapes for each group
        for stage_idx, groups in stage_node_groups.items():
            if not groups:
                continue
                
            # Create separate background for each group within the stage
            for group_idx, (group_type, node_positions) in enumerate(groups.items()):
                if not node_positions:
                    continue
                    
                x_coords = [pos[0] for pos in node_positions]
                y_coords = [pos[1] for pos in node_positions]
                
                # Calculate bounding box with padding
                padding_x = 0.6
                padding_y_top = 0.5
                padding_y_bottom = 0.8  # More space for labels
                
                min_x, max_x = min(x_coords) - padding_x, max(x_coords) + padding_x
                min_y, max_y = min(y_coords) - padding_y_bottom, max(y_coords) + padding_y_top
                
                # Ensure minimum dimensions
                num_nodes = len(node_positions)
                if num_nodes > 1:
                    min_height = num_nodes * 0.6 + 1.0
                    current_height = max_y - min_y
                    if current_height < min_height:
                        center_y = (min_y + max_y) / 2
                        min_y = center_y - min_height / 2
                        max_y = center_y + min_height / 2
                else:
                    if max_y - min_y < 1.4:
                        center_y = (min_y + max_y) / 2
                        min_y = center_y - 0.7
                        max_y = center_y + 0.7
                
                # Choose styling based on group type
                if group_type == 'main_path':
                    # Main path: solid border, light background
                    fill_color = 'rgba(46, 134, 171, 0.08)'  # Light blue
                    border_color = 'rgba(46, 134, 171, 0.3)'
                    border_width = 2
                    border_dash = None
                elif group_type.startswith('branch_'):
                    # Branch groups: different colors and dashed borders
                    branch_colors = [
                        'rgba(242, 66, 54, 0.08)',   # Light red
                        'rgba(255, 165, 0, 0.08)',   # Light orange  
                        'rgba(138, 43, 226, 0.08)',  # Light purple
                        'rgba(34, 139, 34, 0.08)',   # Light green
                        'rgba(255, 20, 147, 0.08)',  # Light pink
                    ]
                    border_colors = [
                        'rgba(242, 66, 54, 0.4)',
                        'rgba(255, 165, 0, 0.4)',
                        'rgba(138, 43, 226, 0.4)',
                        'rgba(34, 139, 34, 0.4)',
                        'rgba(255, 20, 147, 0.4)',
                    ]
                    
                    # Extract actual branch number from group_type (e.g., 'branch_1' -> 1)
                    branch_number = int(group_type.split('_')[1]) if '_' in group_type else 1
                    color_idx = (branch_number - 1) % len(branch_colors)  # Convert to 0-based index
                    
                    fill_color = branch_colors[color_idx]
                    border_color = border_colors[color_idx]
                    border_width = 2
                    border_dash = 'dot'
                else:
                    # Fallback styling
                    fill_color = 'rgba(240,240,240,0.3)'
                    border_color = 'rgba(200,200,200,0.5)'
                    border_width = 1
                    border_dash = None
                
                # Create the background shape
                shape = {
                    'type': 'rect',
                    'x0': min_x,
                    'y0': min_y,
                    'x1': max_x,
                    'y1': max_y,
                    'fillcolor': fill_color,
                    'line': {
                        'color': border_color, 
                        'width': border_width
                    },
                    'layer': 'below'
                }
                
                if border_dash:
                    shape['line']['dash'] = border_dash
                
                shapes.append(shape)
                
                # Add group labels for branches
                if group_type.startswith('branch_') and len(groups) > 1:
                    # Only add labels when there are multiple groups in the stage
                    branch_number = int(group_type.split('_')[1]) if '_' in group_type else 1
                    shapes.append({
                        'type': 'rect',
                        'x0': min_x,
                        'y0': max_y - 0.3,
                        'x1': min_x + 1.0,
                        'y1': max_y,
                        'fillcolor': border_color.replace('0.4', '0.7'),
                        'line': {'width': 0},
                        'layer': 'above'
                    })
            
        return shapes
    
    def _group_nodes_by_stage_and_branches(self, pos: Dict[str, Tuple[float, float]]) -> Dict[int, Dict[str, List[Tuple[float, float]]]]:
        """Group nodes by stage and then by branch numbers.
        
        Returns:
            Dict mapping stage_idx to dict of group_type -> list of positions
            group_type can be 'main_path', 'branch_1', 'branch_2', etc.
        """
        stage_width = 2.0
        stage_groups = {}
        
        # First, group nodes by stage
        stage_nodes = {}
        for node_id, (x, y) in pos.items():
            stage_x = round(x / stage_width)
            if stage_x not in stage_nodes:
                stage_nodes[stage_x] = []
            stage_nodes[stage_x].append(node_id)
        
        # For each stage, group nodes by their branch numbers
        for stage_idx, node_ids in stage_nodes.items():
            if not node_ids:
                continue
                
            groups = {}
            
            # Group nodes by branch number
            branch_groups = {}
            for node_id in node_ids:
                branch_number = self.graph.nodes[node_id].get('branch_number', 0)
                if branch_number not in branch_groups:
                    branch_groups[branch_number] = []
                branch_groups[branch_number].append(node_id)
            
            # Convert to the expected format
            for branch_number, node_list in branch_groups.items():
                if branch_number == 0:
                    groups['main_path'] = [pos[nid] for nid in node_list]
                else:
                    groups[f'branch_{branch_number}'] = [pos[nid] for nid in node_list]
            
            stage_groups[stage_idx] = groups
            
        return stage_groups
    
    def _create_stage_labels(self, pos: Dict[str, Tuple[float, float]]) -> List[Dict]:
        """Create stage labels for the visualization with enhanced branch group indicators."""
        if not pos:
            return []
            
        annotations = []
        stage_width = 2.0
        
        # Get the grouped structure to determine if we need branch indicators
        stage_node_groups = self._group_nodes_by_stage_and_branches(pos)
        
        # Find which stages have nodes
        stages_with_nodes = set()
        for node_id in pos.keys():
            node_data = self.graph.nodes[node_id]
            stage = node_data.get('stage', 'UNKNOWN')
            stages_with_nodes.add(stage)
        
        # Create labels for stages that have nodes
        for i, stage in enumerate(self.stage_order):
            if stage in stages_with_nodes:
                stage_x = i * stage_width
                
                # Check if this stage has multiple groups (indicating branches)
                groups = stage_node_groups.get(i, {})
                has_branches = len([k for k in groups.keys() if k.startswith('branch_')]) > 0
                has_multiple_groups = len(groups) > 1
                
                # Create main stage label
                stage_label = f"<b>{stage.replace('_', ' ').title()}</b>"
                
                # Add branch indicator if there are branches
                if has_branches:
                    num_branches = len([k for k in groups.keys() if k.startswith('branch_')])
                    if has_multiple_groups:
                        stage_label += f"<br><span style='font-size: 10px; color: #666;'>🔀 {num_branches} branch{'es' if num_branches > 1 else ''}</span>"
                
                annotations.append({
                    'x': stage_x,
                    'y': -6,  # Position below the nodes
                    'text': stage_label,
                    'showarrow': False,
                    'font': {'size': 12, 'color': '#333'},
                    'align': 'center'
                })
                
                # Add group type indicators for stages with multiple groups
                if has_multiple_groups and len(groups) > 1:
                    # Find the y-positions to place group labels
                    group_y_positions = {}
                    for group_type, node_positions in groups.items():
                        if node_positions:
                            avg_y = sum(pos[1] for pos in node_positions) / len(node_positions)
                            group_y_positions[group_type] = avg_y
                    
                    # Sort groups by their y-position to place labels consistently
                    sorted_groups = sorted(group_y_positions.items(), key=lambda x: x[1], reverse=True)
                    
                    for group_type, avg_y in sorted_groups:
                        if group_type == 'main_path':
                            label_text = "📍 Main"
                            label_color = '#2E86AB'
                        elif group_type.startswith('branch_'):
                            # Extract the actual branch number (e.g., 'branch_1' -> 1)
                            branch_number = int(group_type.split('_')[1]) if '_' in group_type else 0
                            label_text = f"🔀 Branch {branch_number}"
                            # Use the same colors as the background, indexed by actual branch number
                            branch_colors = ['#F24236', '#FFA500', '#8A2BE2', '#228B22', '#FF1493']
                            label_color = branch_colors[(branch_number - 1) % len(branch_colors)]
                        else:
                            continue
                        
                        annotations.append({
                            'x': stage_x + 0.8,  # Offset to the right
                            'y': avg_y + 0.3,    # Position near the group
                            'text': f"<span style='font-size: 9px; color: {label_color}; font-weight: bold;'>{label_text}</span>",
                            'showarrow': False,
                            'font': {'size': 9, 'color': label_color},
                            'align': 'left',
                            'bgcolor': 'rgba(255,255,255,0.8)',
                            'bordercolor': label_color,
                            'borderwidth': 1,
                            'borderpad': 2
                        })
                
        return annotations
    
    def _is_branch_edge(self, source_node: str, target_node: str) -> bool:
        """Determine if an edge represents a branch connection using branch numbers.
        
        Args:
            source_node: Source node ID
            target_node: Target node ID
            
        Returns:
            bool: True if this is a branch edge
        """
        # An edge is a branch if either node has a branch number > 0
        source_branch = self.graph.nodes[source_node].get('branch_number', 0)
        target_branch = self.graph.nodes[target_node].get('branch_number', 0)
        return source_branch > 0 or target_branch > 0
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get debug information about the current journey tracker state."""
        return {
            "total_journey_points": len(self.journey_points),
            "current_branch_number": self.current_branch_number,
            "graph_nodes": list(self.graph.nodes()),
            "graph_edges": list(self.graph.edges()),
            "last_node_id": self.last_node_id,
            "stage_to_latest_node": self.stage_to_latest_node,
            "stage_order": self.stage_order,
            "last_stage": self.journey_points[-1].stage if self.journey_points else None,
            "stage_visit_counts": {
                stage: sum(1 for point in self.journey_points if point.stage == stage)
                for stage in set(point.stage for point in self.journey_points)
            } if self.journey_points else {},
            "journey_points_summary": [
                {
                    "index": i,
                    "stage": point.stage,
                    "decision_type": point.decision_type,
                    "description": point.description,
                    "parent_id": point.parent_id,
                    "branch_number": point.branch_number,
                    "is_branch": point.branch_number > 0,
                    "timestamp": point.timestamp.isoformat()
                }
                for i, point in enumerate(self.journey_points)
            ]
        }

def _format_detail_value_for_hover(value):
    """Format detail values for hover text display (more compact than story display)."""
    if value is None:
        return "None"
    
    # Handle numpy values
    if hasattr(value, 'item'):  # numpy scalar
        value = value.item()
    
    # Handle lists
    if isinstance(value, list):
        if not value:
            return "[]"
        
        # Check if it's a list of dictionaries (like feature importances or fairness results)
        if all(isinstance(item, dict) for item in value):
            if len(value) <= 3:
                formatted_items = []
                for item in value:
                    item_parts = []
                    for k, v in item.items():
                        if hasattr(v, 'item'):  # numpy scalar
                            v = v.item()
                        if isinstance(v, float):
                            v = f"{v:.3f}"
                        # Convert key to string before calling replace
                        key_str = str(k).replace('_', ' ').title() if isinstance(k, str) else str(k)
                        item_parts.append(f"{key_str}: {v}")
                    formatted_items.append(" | ".join(item_parts))
                return "<br>".join(formatted_items)
            else:
                # Show first 2 items + count
                formatted_items = []
                for item in value[:2]:
                    item_parts = []
                    for k, v in item.items():
                        if hasattr(v, 'item'):  # numpy scalar
                            v = v.item()
                        if isinstance(v, float):
                            v = f"{v:.3f}"
                        # Convert key to string before calling replace
                        key_str = str(k).replace('_', ' ').title() if isinstance(k, str) else str(k)
                        item_parts.append(f"{key_str}: {v}")
                    formatted_items.append(" | ".join(item_parts))
                return "<br>".join(formatted_items) + f"<br>... (+{len(value)-2} more)"
        
        # Handle list of simple values
        formatted_list = []
        for item in value:
            if hasattr(item, 'item'):  # numpy scalar
                item = item.item()
            if isinstance(item, float):
                item = f"{item:.3f}"
            formatted_list.append(str(item))
        
        if len(formatted_list) <= 3:
            return ", ".join(formatted_list)
        else:
            return ", ".join(formatted_list[:3]) + f" ... (+{len(formatted_list)-3} more)"
    
    # Handle dictionaries
    if isinstance(value, dict):
        if not value:
            return "{}"
        
        formatted_dict = []
        for k, v in value.items():
            if hasattr(v, 'item'):  # numpy scalar
                v = v.item()
            if isinstance(v, float):
                v = f"{v:.3f}"
            elif isinstance(v, bool):
                v = "Yes" if v else "No"
            # Convert key to string before calling replace
            key_str = str(k).replace('_', ' ').title() if isinstance(k, str) else str(k)
            formatted_dict.append(f"{key_str}: {v}")
        
        return " | ".join(formatted_dict)
    
    # Handle floats
    if isinstance(value, float):
        if abs(value) < 0.001 or abs(value) > 1000:
            return f"{value:.2e}"
        else:
            return f"{value:.3f}"
    
    # Handle booleans
    if isinstance(value, bool):
        return "Yes" if value else "No"
    
    # Handle strings and other types
    str_value = str(value)
    if len(str_value) > 100:
        return str_value[:97] + "..."
    return str_value

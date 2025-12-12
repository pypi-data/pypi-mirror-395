import streamlit as st
from datetime import datetime
import json
import re


def render_log_viewer():
    """Render a log viewer component."""

    # Add help section above the logs expander
    with st.expander("📋 Session Logs", expanded=False):
        if 'logger' in st.session_state:
            # Get all log lines from memory
            raw_logs = st.session_state.logger.get_session_logs()
            
            # Add filters and download button
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                log_types = ["All", "USER ACTION", "CALCULATION", "RECOMMENDATION", "ERROR", "MODEL METRICS", "STAGE TRANSITION"]
                log_type = st.multiselect(
                    "Filter by type",
                    log_types,
                    default=["All"],
                    key="log_viewer_type_filter"
                )
                
                # If no types are selected, default to "All"
                if not log_type:
                    log_type = ["All"]
                # If "All" is selected along with other options, keep only "All"
                elif "All" in log_type and len(log_type) > 1:
                    log_type = ["All"]
            
            with col2:
                time_range = st.slider(
                    "Time range (minutes ago)",
                    0, 20, (0, 5)
                )
            
            with col3:
                # Create download button for full logs
                if raw_logs:
                    log_content = "\n".join(raw_logs)
                    st.download_button(
                        label="📥 Download Logs",
                        data=log_content,
                        file_name=f"ml_builder_session_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        help="Download the complete session logs"
                    )
            
            # Filter and display logs
            current_time = datetime.now()
            filtered_logs = []
            seen_logs = set()  # Track unique log messages
            
            # Process logs
            i = 0
            while i < len(raw_logs):
                try:
                    log = raw_logs[i]
                    if isinstance(log, str):
                        log = log.strip()
                    
                    # Check if this is a valid log entry (should start with timestamp)
                    if not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', log):
                        i += 1
                        continue
                    
                    # Parse log entry
                    timestamp_str = log.split('|')[0].strip()
                    log_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    minutes_ago = (current_time - log_timestamp).total_seconds() / 60
                    
                    # Apply filters
                    time_filter = time_range[0] <= minutes_ago <= time_range[1]
                    type_filter = "All" in log_type or any(type_filter in log for type_filter in log_type)
                    
                    if time_filter and type_filter:
                        # Split the log entry only by the first two pipe characters
                        parts = log.split('|', 2)
                        if len(parts) == 3:
                            timestamp = parts[0].strip()
                            log_type_str = parts[1].strip()
                            message = parts[2].strip()
                            
                            # Look ahead for potential JSON content
                            json_content = []
                            next_idx = i + 1
                            while next_idx < len(raw_logs):
                                next_line = raw_logs[next_idx]
                                if isinstance(next_line, str):
                                    next_line = next_line.strip()
                                if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', next_line):
                                    break
                                if next_line:
                                    json_content.append(next_line)
                                next_idx += 1
                            
                            # Update loop counter to skip processed JSON lines
                            i = next_idx - 1
                            
                            # Try to parse JSON if present
                            if json_content:
                                try:
                                    json_str = ' '.join(json_content)
                                    json_obj = json.loads(json_str)
                                    formatted_log = f"{timestamp} | {log_type_str}\n    {message}\n{json.dumps(json_obj, indent=4)}"
                                except json.JSONDecodeError:
                                    # If JSON parsing fails, include the content as is
                                    formatted_log = f"{timestamp} | {log_type_str}\n    {message}\n    " + '\n    '.join(json_content)
                            else:
                                formatted_log = f"{timestamp} | {log_type_str}\n    {message}"
                            
                            # Create a key for deduplication (using message content and a 2-second window)
                            dedup_key = f"{log_type_str}|{message}|{int(log_timestamp.timestamp()) // 2}"
                            
                            # Only add if we haven't seen this message recently
                            if dedup_key not in seen_logs:
                                seen_logs.add(dedup_key)
                                filtered_logs.append(formatted_log)
                except Exception:
                    pass
                i += 1
            
            # Display filtered logs with improved formatting
            if filtered_logs:
                # Use columns to maximize width
                col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
                with col2:
                    st.text_area(
                        "Log Messages",
                        value='\n'.join(filtered_logs),
                        height=400,
                        help="Scroll to view all log messages"
                    )
            else:
                st.info("No logs match the current filters")

    with st.expander("ℹ️ Log Viewer Help", expanded=False):
        st.markdown("""
        ### Log Viewer Help
        
        The log viewer helps you track and analyse the ML model development process. Here's how to use it:
        
        #### Filtering Options
        - **Log Type Filter**: Choose which types of logs to display
            - `All`: Show all log types
            - `USER ACTION`: User interactions and decisions
            - `CALCULATION`: Data processing and computations
            - `RECOMMENDATION`: System suggestions
            - `ERROR`: Error messages and warnings
            - `MODEL METRICS`: Model performance measurements
            - `STAGE TRANSITION`: Movement between development stages
        
        - **Time Range**: Filter logs by how recently they occurred
            - Adjust the slider to show logs from the last X minutes
            - Default shows logs from the last 5 minutes
        
        #### Log Format
        Each log entry contains:
        ```
        TIMESTAMP | LOG_TYPE
            Message content
            {
                "json_data": "If present, shown in formatted structure"
            }
        ```
        
        #### Tips
        - Use the text area's scroll functionality to view all logs
        - Select multiple log types to see different categories
        - Adjust the time range to find specific events
        - JSON data is automatically formatted for better readability
        """)
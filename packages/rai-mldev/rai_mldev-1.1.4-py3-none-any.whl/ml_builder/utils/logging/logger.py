import logging
from datetime import datetime
import json
from typing import Any, Dict, Optional
import streamlit as st
import numpy as np
import pandas as pd
import re

from utils.logging.journey_tracker import MLJourneyTracker

class MLLogger:
    """Custom logger for ML model development process."""
    
    def __init__(self):
        """Initialize the logger with memory storage and stream handlers."""
        # Create a memory buffer for logs
        self.log_buffer = []
        
        # Create a new session ID
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Configure logger
        self.logger = logging.getLogger(f"MLLogger_{self.session_id}")
        self.logger.setLevel(logging.DEBUG)
        
        # Add last message tracking with timestamp
        self._last_message = None
        self._last_timestamp = None
        self._duplicate_threshold = 5  # Increased from 1 to 5 seconds
        
        # Add message cache for deduplication
        self._message_cache = {}
        self._cache_size = 1000  # Maximum number of cached messages
        
        # Add state tracking for page-level deduplication
        self._page_state = {}
        self._page_state_ttl = 5  # seconds before allowing same page state to be logged again
        
        # Add similarity threshold for fuzzy matching
        self._similarity_threshold = 0.85
        
        # Add message normalization patterns
        self._normalization_patterns = [
            (r'\b\d+\.\d+\b', 'NUMBER'),  # Float numbers
            (r'\b\d+\b', 'NUMBER'),        # Integer numbers
            (r'\b[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}\b', 'UUID'),  # UUIDs
            (r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}', 'TIMESTAMP'),    # Timestamps
            (r'0x[0-9a-fA-F]+', 'HEX'),   # Hex numbers
        ]
        
        # Add message type categorization
        self._message_categories = {
            'calculation': ['CALCULATION', 'METRICS', 'ANALYSIS'],
            'state': ['STATE', 'STATUS', 'PROGRESS'],
            'action': ['ACTION', 'TRANSITION', 'EVENT']
        }
        
        # Category-specific thresholds (in seconds)
        self._category_thresholds = {
            'calculation': 10,
            'state': 5,
            'action': 2,
            'default': self._duplicate_threshold
        }
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            # Custom handler for memory logging
            self.memory_handler = self.MemoryHandler()
            self.memory_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            self.memory_handler.setFormatter(file_formatter)
            self.logger.addHandler(self.memory_handler)
            
            # Stream handler for console output
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
            stream_handler.setFormatter(stream_formatter)
            self.logger.addHandler(stream_handler)

    def _normalize_message(self, message: str) -> str:
        """Normalize message by replacing variable parts with constants."""
        normalized = message.lower()
        for pattern, replacement in self._normalization_patterns:
            normalized = re.sub(pattern, replacement, normalized)
        return normalized
        
    def _get_message_category(self, message: str) -> str:
        """Determine message category based on content."""
        message_upper = message.upper()
        for category, keywords in self._message_categories.items():
            if any(keyword in message_upper for keyword in keywords):
                return category
        return 'default'
        
    def _should_log_message(self, level: str, message: str) -> bool:
        """Enhanced duplicate detection with message normalization and categorization."""
        current_time = datetime.now()
        
        # Normalize message for comparison
        normalized_message = self._normalize_message(message)
        cache_key = f"{level}:{normalized_message}"
        
        # Get message category and its threshold
        category = self._get_message_category(message)
        threshold = self._category_thresholds.get(category, self._duplicate_threshold)
        
        # Check exact duplicates first
        if cache_key in self._message_cache:
            last_time = self._message_cache[cache_key]
            time_diff = (current_time - last_time).total_seconds()
            
            if time_diff < threshold:
                return False
        
        # Check for similar messages in the same category
        for cached_key, cached_time in list(self._message_cache.items()):
            if cached_key.startswith(f"{level}:"):
                cached_msg = cached_key.split(':', 1)[1]
                if self._are_messages_similar(normalized_message, cached_msg):
                    time_diff = (current_time - cached_time).total_seconds()
                    if time_diff < threshold * 1.5:  # Use slightly higher threshold for similar messages
                        return False
        
        # Update cache
        self._message_cache[cache_key] = current_time
        
        # Clean old entries from cache
        self._clean_message_cache()
        
        return True
    
    def _are_messages_similar(self, msg1: str, msg2: str) -> bool:
        """Check if two messages are similar using basic similarity metrics."""
        # Simple word overlap ratio
        words1 = set(msg1.split())
        words2 = set(msg2.split())
        
        if not words1 or not words2:
            return False
            
        overlap = len(words1.intersection(words2))
        similarity = overlap / max(len(words1), len(words2))
        
        return similarity >= self._similarity_threshold
    
    def _clean_message_cache(self):
        """Clean old entries from message cache."""
        current_time = datetime.now()
        max_age = max(self._category_thresholds.values()) * 2
        
        # Remove entries older than max_age
        self._message_cache = {
            k: v for k, v in self._message_cache.items()
            if (current_time - v).total_seconds() <= max_age
        }
        
        # If cache is still too large, remove oldest entries
        if len(self._message_cache) > self._cache_size:
            sorted_cache = sorted(self._message_cache.items(), key=lambda x: x[1])
            self._message_cache = dict(sorted_cache[len(sorted_cache)//2:])

    def _get_base_message(self, message: str) -> str:
        """Extract core message content ignoring variable parts."""
        # Remove timestamps
        message = ' '.join([part for part in message.split() if not self._is_timestamp(part)])
        
        # Remove specific numbers and IDs
        message = re.sub(r'\d+\.\d+', 'NUM', message)
        message = re.sub(r'\b\d+\b', 'NUM', message)
        
        return message.strip()
    
    def _is_timestamp(self, text: str) -> bool:
        """Check if text part looks like a timestamp."""
        timestamp_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # Date
            r'\d{2}:\d{2}:\d{2}',  # Time
            r'\d{4}\d{2}\d{2}_\d{6}'  # Compact timestamp
        ]
        return any(re.match(pattern, text) for pattern in timestamp_patterns)
    
    def convert_to_serializable(self, obj):
        """Convert numpy and pandas types to JSON serializable types."""
        if isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        if isinstance(obj, (np.float64, np.float32, np.float16)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        if isinstance(obj, np.dtype):
            return str(obj)
        # Add handling for Plotly figures
        if str(type(obj).__module__).startswith('plotly'):
            return "[Plotly Figure Object]"
        if hasattr(obj, 'dtype'):
            if isinstance(obj.dtype, np.dtype):
                return str(obj.dtype)
            return str(obj)
        return obj

    def convert_dict_or_list(self, obj):
        """Recursively convert dictionary and list contents to serializable types."""
        if isinstance(obj, dict):
            return {k: self.convert_dict_or_list(self.convert_to_serializable(v)) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_dict_or_list(self.convert_to_serializable(item)) for item in obj]
        return self.convert_to_serializable(obj)

    def _format_message(self, message: Any) -> str:
        """Format message for logging."""
        if isinstance(message, (dict, list)):
            message = self.convert_dict_or_list(message)
            return json.dumps(message, indent=2)
        
        return str(self.convert_to_serializable(message))
    
    def _log_message(self, level: str, message: str):
        """Internal method to handle message logging with duplicate checking."""
        if not self._should_log_message(level, message):
            return
            
        if level == 'INFO':
            self.logger.info(message)
        elif level == 'DEBUG':
            self.logger.debug(message)
        elif level == 'ERROR':
            self.logger.error(message)

    def log_user_action(self, action: str, details: Optional[Dict] = None):
        """Log user interactions."""
        message = f"USER ACTION | {action}"
        if details:
            message += f" | {self._format_message(details)}"
        self._log_message('INFO', message)
    
    def log_calculation(self, calculation_type: str, details: Optional[Dict] = None):
        """Log calculations and their results."""
        message = f"CALCULATION | {calculation_type}"
        if details:
            message += f" | {self._format_message(details)}"
        self._log_message('DEBUG', message)
    
    def log_recommendation(self, recommendation: str, context: Optional[Dict] = None):
        """Log system recommendations."""
        message = f"RECOMMENDATION | {recommendation}"
        if context:
            message += f" | Context: {self._format_message(context)}"
        self._log_message('INFO', message)
    
    def log_error(self, error: str, details: Optional[Dict] = None):
        """Log errors and exceptions."""
        message = f"ERROR | {error}"
        if details:
            message += f" | {self._format_message(details)}"
        self._log_message('ERROR', message)
    
    def log_model_metrics(self, metrics: Dict):
        """Log model performance metrics."""
        message = f"MODEL METRICS | {self._format_message(metrics)}"
        self._log_message('INFO', message)
    
    def log_stage_transition(self, from_stage: str, to_stage: str, metrics: Optional[Dict] = None):
        """Log transitions between stages."""
        message = f"STAGE TRANSITION | From: {from_stage} | To: {to_stage}"
        if metrics:
            message += f" | Metrics: {self._format_message(metrics)}"
        self._log_message('INFO', message)
    
    def log_page_state(self, page_name: str, state_data: Dict):
        """Log page state changes with deduplication."""
        current_time = datetime.now()
        
        # Convert state_data to serializable format first
        converted_state_data = self.convert_dict_or_list(state_data)
        state_key = f"{page_name}:{json.dumps(converted_state_data, sort_keys=True)}"
        
        if state_key in self._page_state:
            last_time = self._page_state[state_key]
            if (current_time - last_time).total_seconds() < self._page_state_ttl:
                return
        
        self._page_state[state_key] = current_time
        self._log_message('DEBUG', f"PAGE STATE | {page_name} | {self._format_message(state_data)}")
    
    def get_session_logs(self) -> list:
        """Retrieve logs for current session."""
        for handler in self.logger.handlers:
            if isinstance(handler, self.MemoryHandler):
                return handler.get_logs()
        return []

    def flush_logs(self):
        """Flush the buffered logs, removing duplicates."""
        for handler in self.logger.handlers:
            if isinstance(handler, self.MemoryHandler):
                handler.flush()

    def log_journey_point(self, stage: str, decision_type: str, description: str, 
                         details: Dict[str, Any], parent_id: Optional[str] = None) -> Optional[str]:
        """Log a significant journey point that should appear in the visualization.
        
        Returns:
            Optional[str]: The ID of the newly added journey point, or None if it was a duplicate
        """
        # Ensure we have a journey tracker but don't recreate if it exists
        if 'journey_tracker' not in st.session_state:
            st.session_state.journey_tracker = MLJourneyTracker()
        
        # Get reference to the existing tracker to avoid recreating it
        tracker = st.session_state.journey_tracker
        
        node_id = tracker.add_decision(
            stage=stage,
            decision_type=decision_type,
            description=description,
            details=details,
            parent_id=parent_id
        )
        
        if node_id is not None:
            # Only log to regular logger if this wasn't a duplicate
            self.log_user_action(
                f"JOURNEY_POINT: {decision_type}",
                {"stage": stage, "description": description, "details": details}
            )
        else:
            # Log that we skipped a duplicate point
            self.log_calculation(
                "Duplicate Journey Point Skipped",
                {
                    "stage": stage,
                    "decision_type": decision_type,
                    "description": description,
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        return node_id

    class MemoryHandler(logging.Handler):
        """Custom handler that stores logs in memory."""
        def __init__(self):
            super().__init__()
            self.log_buffer = []
            self._last_flush = datetime.now()
            self._flush_interval = 1  # Minimum seconds between flushes
            
        def emit(self, record):
            """Override emit to store in memory buffer."""
            msg = self.format(record)
            self.log_buffer.append(msg)
            
            # Auto-flush if enough time has passed
            current_time = datetime.now()
            if (current_time - self._last_flush).total_seconds() >= self._flush_interval:
                self.flush()
                self._last_flush = current_time
            
        def flush(self):
            """Override flush to deduplicate logs in memory."""
            if not self.log_buffer:
                return
                
            # Remove duplicates while preserving order
            seen = set()
            unique_logs = []
            for msg in self.log_buffer:
                if msg not in seen:
                    seen.add(msg)
                    unique_logs.append(msg)
            
            # Update buffer with unique logs
            self.log_buffer = unique_logs
        
        def get_logs(self) -> list:
            """Get all logs from memory."""
            return self.log_buffer.copy() 
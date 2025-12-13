"""
Unified Logging System for Browser-AI Interface Server
Replaces the previous dual logging system with a clean, configurable solution
"""

import os
import sys
import json
import time
import threading
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum

class LogLevel(Enum):
    """Logging levels in order of priority"""
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40

class UnifiedLogger:
    """
    Unified logging system with:
    - Single log file with timestamps
    - Multi-level support (ERROR/WARN/INFO/DEBUG)
    - Config file controlled
    - System health monitoring
    - Smart deduplication
    - Console error output
    """
    
    def __init__(self, server_dir: str, config_file: str = "logging.json"):
        self.server_dir = Path(server_dir)
        self.config_file = self.server_dir / config_file
        self.config = self._load_config()
        
        # Set up log file
        self.log_file = self.server_dir / self.config["file"]
        self._initialize_log_file()
        
        # Deduplication tracking
        self.last_message = None
        self.duplicate_count = 0
        self.max_duplicates = self.config.get("max_duplicates", 3)
        
        # System health tracking
        self.health_stats = {
            "observer_events_total": 0,  # Running totals (never reset)
            "actor_commands_total": 0,
            "errors_count_total": 0,
            "warnings_count_total": 0,
            "observer_events_period": 0,  # Period counts (reset each summary)
            "actor_commands_period": 0,
            "errors_count_period": 0,
            "warnings_count_period": 0,
            "unique_sessions": set(),  # Track unique session IDs
            "last_summary": time.time(),
            "last_activity": time.time()  # Track when any events occurred
        }
        
        # Thread lock for thread-safe logging
        self._lock = threading.Lock()
        
        # Start background timer for adaptive summaries
        self._timer_thread = None
        self._stop_timer = threading.Event()
        self._start_summary_timer()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load logging configuration from JSON file"""
        default_config = {
            "level": "INFO",
            "file": "server.log",
            "summary_interval": 30,
            "console_errors": True,
            "deduplication": True,
            "max_duplicates": 3,
            "timestamp_format": "%Y-%m-%d %H:%M:%S.%f"
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    return {**default_config, **config}
            else:
                # Create default config file
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            print(f"Error loading logging config: {e}, using defaults")
            return default_config
    
    def _initialize_log_file(self):
        """Initialize log file with startup marker"""
        try:
            startup_time = datetime.now().strftime(self.config["timestamp_format"])[:-3]
            startup_message = f"=== SERVER STARTUP {startup_time} ==="
            
            # Append to existing log file (cumulative logging)
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write('\n' + startup_message)
                
        except Exception as e:
            print(f"Error initializing log file: {e}")
    
    def _format_timestamp(self) -> str:
        """Generate formatted timestamp"""
        return datetime.now().strftime(self.config["timestamp_format"])[:-3]
    
    def _normalize_message(self, message: str) -> str:
        """Normalize message for deduplication by removing dynamic content"""
        import re
        
        # Remove timestamps
        message = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', '[TIMESTAMP]', message)
        
        # Remove session IDs and UUIDs  
        message = re.sub(r'\b[a-zA-Z0-9_]{20,}\b', '[ID]', message)
        
        # Remove numbers in "Consumed X events, Y total processed"
        message = re.sub(r'Consumed \d+ events, \d+ total processed', 'Consumed [N] events, [N] total processed', message)
        
        # Heavily normalize operational messages for aggressive deduplication
        message = re.sub(r'Retrieved \d+ recent events', 'Retrieved events', message)
        message = re.sub(r'Retrieved \d+ pending commands', 'Retrieved commands', message)
        message = re.sub(r'Session Events Recent.*Retrieved \d+ recent events', 'Session polling', message)
        message = re.sub(r'Session Commands.*Retrieved \d+ pending commands', 'Command polling', message)
        
        # Remove other counts (but preserve important non-numeric patterns)
        message = re.sub(r'\b\d+\b', '[NUM]', message)
        
        return message.strip()
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged based on current log level"""
        current_level = LogLevel[self.config["level"]]
        return level.value >= current_level.value
    
    
    def _write_to_file(self, formatted_message: str):
        """Write message to log file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_message + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def _output_to_console(self, level: LogLevel, message: str):
        """Output message to console based on level and config"""
        if level in [LogLevel.ERROR, LogLevel.WARN] and self.config["console_errors"]:
            # Format for console (no timestamp for cleaner output)
            level_prefix = f"[{level.name}]" if level in [LogLevel.ERROR, LogLevel.WARN] else ""
            console_message = f"{level_prefix} {message}".strip()
            print(console_message)
    
    def _handle_deduplication(self, normalized_message: str, level: LogLevel, original_message: str) -> bool:
        """Handle message deduplication. Returns True if message should be skipped"""
        if not self.config["deduplication"]:
            return False
            
        with self._lock:
            if normalized_message == self.last_message:
                self.duplicate_count += 1
                
                # For first few duplicates, still log them
                if self.duplicate_count < self.max_duplicates:
                    return False
                    
                # Beyond threshold, skip logging but track
                return True
            else:
                # New message - log duplicate summary if needed
                if self.duplicate_count >= self.max_duplicates:
                    timestamp = self._format_timestamp()
                    summary = f"[{timestamp}] [System] ... {self.duplicate_count} similar messages suppressed"
                    self._write_to_file(summary)
                    
                # Reset tracking
                self.last_message = normalized_message
                self.duplicate_count = 0
                return False
    
    def count_observer_event(self):
        """Explicitly count observer events"""
        self.health_stats["observer_events_total"] += 1
        self.health_stats["observer_events_period"] += 1
        self.health_stats["last_activity"] = time.time()
    
    def count_actor_command(self):
        """Explicitly count actor commands"""
        self.health_stats["actor_commands_total"] += 1
        self.health_stats["actor_commands_period"] += 1
        self.health_stats["last_activity"] = time.time()
    
    def count_session(self, session_id: str):
        """Explicitly count unique sessions"""
        self.health_stats["unique_sessions"].add(session_id)
    
    def count_error(self):
        """Explicitly count errors"""
        self.health_stats["errors_count_total"] += 1
        self.health_stats["errors_count_period"] += 1
    
    def count_warning(self):
        """Explicitly count warnings"""
        self.health_stats["warnings_count_total"] += 1
        self.health_stats["warnings_count_period"] += 1
    
    def _update_health_stats(self, message: str):
        """Update system health statistics for ERROR/WARN level messages only"""
        import re
        message_lower = message.lower()
        
        # Only auto-count errors and warnings from log messages
        # Observer/Actor/Session counts should be done via explicit method calls
        if "error" in message_lower:
            self.count_error()
        elif "warning" in message_lower or "warn" in message_lower:
            self.count_warning()
    
    def _start_summary_timer(self):
        """Start background timer thread for adaptive summaries"""
        def timer_loop():
            while not self._stop_timer.is_set():
                try:
                    # Check every 10 seconds for adaptive timing
                    if self._stop_timer.wait(10):
                        break
                    self._check_summary()
                except Exception:
                    # Silently ignore timer errors to avoid breaking logging
                    pass
        
        self._timer_thread = threading.Thread(target=timer_loop, daemon=True, name="LogSummaryTimer")
        self._timer_thread.start()
    
    def _stop_summary_timer(self):
        """Stop the background timer thread"""
        if self._stop_timer:
            self._stop_timer.set()
        if self._timer_thread and self._timer_thread.is_alive():
            self._timer_thread.join(timeout=1)
    
    def _check_summary(self):
        """
        Adaptive summary timing (called by background timer):
        - If events stop for 30s, print current summary
        - Then continue periodic summaries every 120s
        """
        current_time = time.time()
        time_since_last_summary = current_time - self.health_stats["last_summary"]
        time_since_last_activity = current_time - self.health_stats["last_activity"]
        
        # Regular periodic summary (120s) - takes priority
        if time_since_last_summary >= 120:
            self._generate_health_summary()
            self.health_stats["last_summary"] = current_time
        # Quick summary after activity stops (30s idle) - only if not recently summarized
        elif time_since_last_activity >= 30 and time_since_last_summary >= 30:
            self._generate_health_summary()
            self.health_stats["last_summary"] = current_time
    
    def _generate_health_summary(self):
        """Generate single-line operational health summary for INFO level"""
        if not self._should_log(LogLevel.INFO):
            return
            
        # Create single-line status summary
        status_message = (
            f"Status: Observer backlog: 0, Actor backlog: 0, Sessions: {len(self.health_stats['unique_sessions'])}, "
            f"Totals: Observer {self.health_stats['observer_events_total']}/Actor {self.health_stats['actor_commands_total']}, "
            f"Errors: {self.health_stats['errors_count_total']}, Warnings: {self.health_stats['warnings_count_total']}"
        )
        
        # Log status message directly with emphasis (bypass deduplication and summary checks)
        summary_timestamp = self._format_timestamp()
        formatted_message = f"[{summary_timestamp}] [INFO] === {status_message} ==="
        self._write_to_file(formatted_message)
        
        # Stream to MongoDB (fire-and-forget)
        _stream_to_mongodb(status_message, "INFO")
        
        # Reset period counters after summary (totals remain)
        self.health_stats["observer_events_period"] = 0
        self.health_stats["actor_commands_period"] = 0
        self.health_stats["errors_count_period"] = 0
        self.health_stats["warnings_count_period"] = 0
    
    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        """
        Main logging method
        
        Args:
            message: Message to log
            level: Logging level (DEBUG, INFO, WARN, ERROR)
        """
        # Timestamp the message immediately when issued
        event_timestamp = self._format_timestamp()
        
        # Check if we should log this level
        if not self._should_log(level):
            return
        
        # Update health statistics for ERROR/WARN only
        self._update_health_stats(message)
        
        # Note: Summaries now handled by background timer thread
        
        # Normalize message for deduplication
        normalized_message = self._normalize_message(message)
        
        # Handle deduplication
        if self._handle_deduplication(normalized_message, level, message):
            return  # Skip this duplicate message
        
        # Format message with event timestamp and level
        level_prefix = f"[{level.name}]"
        
        # Determine source context from message
        if "[" in message and "]" in message:
            # Message already has context
            formatted_message = f"[{event_timestamp}] {level_prefix} {message}".strip()
        else:
            # Add generic context
            formatted_message = f"[{event_timestamp}] {level_prefix} [Server] {message}".strip()
        
        # Clean up double spaces
        formatted_message = " ".join(formatted_message.split())
        
        # Write to file
        self._write_to_file(formatted_message)
        
        # Output to console if appropriate
        self._output_to_console(level, message)
        
        # Stream to MongoDB (fire-and-forget)
        _stream_to_mongodb(message, level.name)

# Global logger instance
_logger: Optional[UnifiedLogger] = None

def _stream_to_mongodb(message: str, level: str, session_id: Optional[str] = None):
    """Helper to stream log events to MongoDB ServerStreamer"""
    try:
        # Import here to avoid circular imports
        from ..streaming.server_streamer import get_server_streamer
        
        # Use asyncio.create_task for fire-and-forget async call
        async def _stream_log():
            try:
                server_streamer = await get_server_streamer()
                if server_streamer:
                    await server_streamer.stream_log_event(level, message, session_id)
            except Exception:
                pass  # Silently ignore streaming errors to not break logging
        
        # Only create task if we're in an async context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(_stream_log())
        except RuntimeError:
            # No event loop running, skip streaming
            pass
    except Exception:
        # Silently ignore all streaming errors to not break logging
        pass

def initialize_logger(server_dir: str, is_detached: bool = False):
    """Initialize the global logger instance"""
    global _logger
    _logger = UnifiedLogger(server_dir)

def log(message: str, skip_console: bool = False):
    """
    Global logging function - maintains compatibility with existing code
    
    Args:
        message: Message to log
        skip_console: Ignored (kept for backward compatibility)
    """
    if _logger is None:
        # Fallback if logger not initialized
        print(message)
        return
    
    # Default to INFO level for backward compatibility
    _logger.log(message, LogLevel.INFO)

def log_debug(message: str):
    """Log DEBUG level message"""
    if _logger:
        _logger.log(message, LogLevel.DEBUG)

def log_info(message: str):
    """Log INFO level message"""
    if _logger:
        _logger.log(message, LogLevel.INFO)

def log_warn(message: str):
    """Log WARN level message"""
    if _logger:
        _logger.log(message, LogLevel.WARN)

def log_error(message: str):
    """Log ERROR level message"""
    if _logger:
        _logger.log(message, LogLevel.ERROR)

def get_log_file() -> Optional[Path]:
    """Get the current log file path"""
    return _logger.log_file if _logger else None

def count_observer_event():
    """Count an observer event"""
    if _logger:
        _logger.count_observer_event()

def count_actor_command():
    """Count an actor command"""
    if _logger:
        _logger.count_actor_command()

def count_session(session_id: str):
    """Count a unique session"""
    if _logger:
        _logger.count_session(session_id)

def reload_config():
    """Reload logging configuration from file"""
    if _logger:
        _logger.config = _logger._load_config()
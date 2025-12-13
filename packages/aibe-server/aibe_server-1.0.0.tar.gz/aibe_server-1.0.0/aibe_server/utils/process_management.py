"""
Process management utilities
Direct port from Node.js server.cjs process management functionality
Handles PID files, existing server detection, and graceful shutdown
"""

import os
import sys
import signal
import time
import psutil
from pathlib import Path
from typing import Optional

from .logging import log


class ProcessManager:
    """
    Process lifecycle management
    Exact port of Node.js process management functionality
    """
    
    def __init__(self, server_dir: str, is_detached: bool = False):
        self.server_dir = Path(server_dir)
        self.is_detached = is_detached
        self.pid_file = self.server_dir / 'server.pid'
        self.start_time = time.time()
        
    def check_existing_server(self):
        """Check for existing server and shut it down if needed"""
        if not self.pid_file.exists():
            log("checkExistingServer: No existing server PID file found")
            return
            
        try:
            pid_str = self.pid_file.read_text().strip()
            log(f"checkExistingServer: Found existing server PID file with PID: {pid_str}")
            
            # Attempt to terminate the existing server process
            try:
                pid = int(pid_str)
                
                # Check if process exists and is not this process
                current_pid = os.getpid()
                if pid == current_pid:
                    log(f"checkExistingServer: PID file contains current process PID ({pid}), ignoring")
                    return
                elif psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    log(f"checkExistingServer: Terminating existing server process PID: {pid}")
                    
                    # Send SIGTERM to allow graceful shutdown
                    process.terminate()
                    
                    # Wait a moment for the server to shut down
                    log("checkExistingServer: Waiting for existing server to shut down...")
                    try:
                        process.wait(timeout=3)  # Wait up to 3 seconds
                    except psutil.TimeoutExpired:
                        log("checkExistingServer: Process didn't terminate gracefully, forcing kill")
                        process.kill()
                    except psutil.NoSuchProcess:
                        log("checkExistingServer: Process already terminated")
                else:
                    log(f"checkExistingServer: Process {pid} no longer exists")
                
                # Remove the PID file if it still exists
                if self.pid_file.exists():
                    self.pid_file.unlink()
                    log("checkExistingServer: Removed existing PID file")
                    
            except (ValueError, psutil.NoSuchProcess, psutil.AccessDenied) as kill_error:
                log(f"checkExistingServer: Error terminating existing server: {kill_error}")
                
                # If we couldn't terminate the process, it might not exist anymore
                # Remove the stale PID file
                if self.pid_file.exists():
                    self.pid_file.unlink()
                    log("checkExistingServer: Removed stale PID file")
                    
        except Exception as read_error:
            log(f"checkExistingServer: Error reading PID file: {read_error}")
            
            # Remove the invalid PID file
            try:
                self.pid_file.unlink()
                log("checkExistingServer: Removed invalid PID file")
            except Exception as unlink_error:
                log(f"checkExistingServer: Error removing invalid PID file: {unlink_error}")
    
    def save_pid(self):
        """Write PID to file for easier management, but only when in detached mode"""
        if self.is_detached:
            try:
                self.pid_file.write_text(str(os.getpid()))
                log(f"savePID: Saved PID {os.getpid()} to server.pid file")
            except Exception as error:
                print(f"savePID: Error writing PID file: {error}")
                log(f"savePID: Error writing PID file: {error}", True)
        else:
            # In debug mode, make sure to remove any existing PID file to avoid confusion
            if self.pid_file.exists():
                try:
                    self.pid_file.unlink()
                    log("savePID: Removed existing PID file in debug mode")
                except Exception as error:
                    print(f"savePID: Error removing existing PID file: {error}")
                    log(f"savePID: Error removing existing PID file: {error}", True)
    
    def clean_shutdown(self, signal_name: str):
        """Helper function for clean shutdown"""
        log("cleanShutdown: === SERVER SHUTDOWN INITIATED ===")
        log(f"cleanShutdown: Shutdown signal: {signal_name}")
        log(f"cleanShutdown: PID: {os.getpid()}")
        uptime = time.time() - self.start_time
        log(f"cleanShutdown: Uptime: {uptime:.2f} seconds")
        
        # Always ensure shutdown is logged to file
        try:
            timestamp = time.time()
            message = f"{timestamp} - Shutting down server via {signal_name} after {uptime:.2f}s uptime"
            # This will be handled by the logging system
            log(message, skip_console=True)
        except Exception as error:
            # Last attempt, if this fails, we can't do much more
            print(f"cleanShutdown: Failed to write shutdown log: {error}")
        
        # Remove PID file if it exists
        if self.pid_file.exists():
            try:
                self.pid_file.unlink()
                log("cleanShutdown: Removed PID file")
            except Exception as error:
                log(f"cleanShutdown: Error removing PID file: {error}")
        
        # Exit with code 0 for normal shutdown
        sys.exit(0)


def setup_signal_handlers(process_manager: ProcessManager):
    """Setup signal handlers for graceful shutdown"""
    
    def signal_handler(signum, frame):
        signal_name = signal.Signals(signum).name
        log(f"process.on.{signal_name}: === EXCEPTION ===")
        process_manager.clean_shutdown(signal_name)
    
    # Handle process signals to ensure clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # SIGHUP is not available on Windows
    if hasattr(signal, 'SIGHUP'):
        signal.signal(signal.SIGHUP, signal_handler)
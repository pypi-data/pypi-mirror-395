#!/usr/bin/env python3
"""
Unified Server Management for AI Browser Extension
Cross-platform server management with proper space detection
"""

import sys
import os
import platform
import subprocess
import time
import requests
import json
from pathlib import Path
from datetime import datetime

# Server configuration
SERVER_PORT = 3001
SERVER_URL = f"http://localhost:{SERVER_PORT}"
STATUS_ENDPOINT = f"{SERVER_URL}/status"

def get_my_platform():
    """Get the platform this script is running on"""
    return platform.system()

def get_server_status():
    """
    Status detection primitive: HTTP call to /status endpoint
    Returns: JSON dict if server up, None if server down
    """
    try:
        response = requests.get(STATUS_ENDPOINT, timeout=100)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def start_server():
    """Start server in my OS space"""
    my_platform = get_my_platform()
    
    # Check if server already running
    status = get_server_status()
    if status:
        server_platform = status.get('platform', 'Unknown')
        print(f"Server already running on {server_platform} (PID: {status.get('pid')})")
        if server_platform != my_platform:
            print(f"You're on {my_platform} but server is on {server_platform}")
            print(f"Use {server_platform} commands to manage this server")
        return False
    
    # Start server (OS-agnostic)
    try:        
        print("Starting AI Browser Extension Server...")
        
        # Start detached process without waiting
        if platform.system() == "Windows":
            # Windows: Use CREATE_NEW_PROCESS_GROUP for background execution
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            # Unix: Standard detachment  
            creation_flags = 0
            
        # Temporarily show output to debug startup issue
        process = subprocess.Popen([
            "python", "-m", "aibe_server.main", "--detached"
        ], cwd=Path(__file__).parent.parent, 
           creationflags=creation_flags)
        
        # Give server time to start
        time.sleep(5)
        
        # Check if server started successfully
        status = get_server_status()
        if status:
            print(f"+ Server started successfully on {my_platform}")
            print(f"   PID: {status.get('pid')}")
            print(f"   URL: {SERVER_URL}")
            if status.get('extensionPath'):
                print(f"   Extension files: {status.get('extensionPath')}")
            return True
        else:
            print("! Server start failed - not responding")
            return False
            
    except Exception as e:
        print(f"! Server start failed: {e}")
        return False

def stop_server():
    """Stop server in my OS space"""
    my_platform = get_my_platform()
    
    # Check server status first
    status = get_server_status()
    if not status:
        print("Server is not running")
        return True
        
    server_platform = status.get('platform', 'Unknown')
    server_pid = status.get('pid')
    
    # Check if server is in different space
    if server_platform != my_platform:
        print(f"Server running on {server_platform} (PID: {server_pid})")
        print(f"You're on {my_platform} - can't stop server in different space")
        print(f"Use {server_platform} commands to stop this server")
        return False
    
    # Stop server in my space
    try:
        print(f"Stopping server (PID: {server_pid})...")
        
        if my_platform == "Windows":
            # Windows: taskkill with force flag
            result = subprocess.run(['taskkill', '/F', '/PID', str(server_pid)], 
                                  capture_output=True, text=True)
        else:
            # Linux/WSL: kill
            result = subprocess.run(['kill', str(server_pid)], 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            # Verify server is down
            time.sleep(1)
            if not get_server_status():
                print("+ Server stopped successfully")
                return True
            else:
                print("! Server stop command succeeded but server still responding")
                return False
        else:
            print(f"! Server stop failed: {result.stderr}")
            print("Server may still be running - check permissions?")
            return False
            
    except Exception as e:
        print(f"! Server stop failed: {e}")
        return False

def restart_server():
    """Restart server: stop if running, then start"""
    print("Restarting AI Browser Extension Server...")
    
    # Stop if running (handles space checking)
    stop_server()
    
    # Always try to start
    time.sleep(1)
    return start_server()

def status_command():
    """Status command: format and display server status"""
    my_platform = get_my_platform()
    
    print("AI Browser Extension Server Status")
    print("=" * 40)
    
    status = get_server_status()
    if not status:
        print("! Server is not running")
        print()
        print("Commands:")
        print(f"  python server_manager.py start    - Start server")
        print(f"  python server_manager.py stop     - Stop server") 
        print(f"  python server_manager.py restart  - Restart server")
        return
    
    server_platform = status.get('platform', 'Unknown')
    
    # Cross-space warning
    if server_platform != my_platform:
        print(f"! CROSS-SPACE DETECTION:")
        print(f"   Server running on: {server_platform}")
        print(f"   You are on: {my_platform}")
        print(f"   Use {server_platform} commands to manage this server")
        print()
    
    # Server info
    print(f"+ Server running on {server_platform}")
    print(f"   PID: {status.get('pid')}")
    print(f"   URL: {SERVER_URL}")
    print(f"   Mode: {status.get('mode')}")
    print(f"   Uptime: {status.get('uptime', 0):.1f} seconds")
    print(f"   Started: {status.get('startTime', 'Unknown')}")
    if status.get('extensionPath'):
        print(f"   Extension files: {status.get('extensionPath')}")
    
    # Session info
    if status.get('sessionBased'):
        print(f"   Active sessions: {1 if status.get('sessionId') != 'fallback_session' else 0}")
        print(f"   Events: {status.get('eventCount', 0)}")
        print(f"   Pending commands: {status.get('pendingActorCommands', 0)}")
    
    print()
    print("Commands:")
    if server_platform == my_platform:
        print(f"  python server_manager.py stop     - Stop server")
        print(f"  python server_manager.py restart  - Restart server")
    else:
        print(f"  (Use {server_platform} commands to control this server)")

def show_help():
    """Show help message"""
    print("AI Browser Extension Interface Server")
    print("=====================================")
    print()
    print("USAGE:")
    print("  aibe-server <command>")
    print()
    print("COMMANDS:")
    print("  start     Start the server in background")
    print("  stop      Stop the running server") 
    print("  restart   Restart the server")
    print("  status    Show server status and information")
    print("  help      Show this help message")
    print()
    print("EXAMPLES:")
    print("  aibe-server start    # Start server in background")
    print("  aibe-server status   # Check if server is running")
    print("  aibe-server stop     # Stop the server")
    print()
    print("The server will be available at: http://localhost:3001")
    print("Extension files are included in the package for Chrome installation.")

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        if len(sys.argv) == 1:
            show_help()
        else:
            print("Usage: aibe-server {start|stop|restart|status|help}")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command in ["help", "--help", "-h"]:
        show_help()
        sys.exit(0)
    elif command == "start":
        success = start_server()
        sys.exit(0 if success else 1)
    elif command == "stop":
        success = stop_server()
        sys.exit(0 if success else 1)
    elif command == "restart":
        success = restart_server()
        sys.exit(0 if success else 1)
    elif command == "status":
        status_command()
        sys.exit(0)
    else:
        print(f"Unknown command: {command}")
        print()
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
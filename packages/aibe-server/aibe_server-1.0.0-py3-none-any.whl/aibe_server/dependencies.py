import uuid
from datetime import datetime
from typing import Dict, Any
from fastapi import Request, HTTPException
from .session_manager import SessionManager

# Global singleton instance
session_manager = SessionManager()

# Configuration constants
PORT = 3001
MAX_UNPROCESSED_EVENTS = 50
MAX_PROCESSED_EVENTS = 1000
MAX_COMMANDS_PER_SESSION = 100

def validate_session_dependency(session_id: str, request: Request):
    """Dependency for session validation"""
    result = session_manager.validate_session(session_id)
    if result["error"]:
        raise HTTPException(
            status_code=404,
            detail={
                "error": result["error"]["message"],
                "availableSessions": result["error"]["availableSessions"]
            }
        )
    return result

def generate_unique_id() -> str:
    """Generate unique ID for commands"""
    return 'cmd_' + str(uuid.uuid4()).replace('-', '')[:12] + '_' + str(int(datetime.now().timestamp() * 1000))

def enrich_command(command: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich command with metadata (exact match with Node.js)"""
    return {
        **command,
        "id": generate_unique_id(),
        "timestamp": datetime.now().isoformat(),
        "queuedAt": datetime.now().isoformat(),
        "status": "queued"
    }

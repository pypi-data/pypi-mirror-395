"""
Session middleware for extracting and managing sessions
Direct port from Node.js session middleware functionality
"""

from fastapi import Request, HTTPException
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from ..session_manager import SessionManager
from ..utils.logging import log


# Configuration constants - exact match with Node.js
MAX_UNPROCESSED_EVENTS = 50
MAX_PROCESSED_EVENTS = 1000
MAX_COMMANDS_PER_SESSION = 100


def generate_fallback_id() -> str:
    """Generate fallback session ID"""
    return 'fallback_' + str(uuid.uuid4()).replace('-', '')[:9]


def setup_session_middleware(session_manager: SessionManager):
    """
    Setup session middleware factory
    Returns middleware function configured with SessionManager
    """

    async def session_middleware(request: Request, call_next):
        """
        Session middleware using sessionStorage tabID approach
        Direct port from Node.js session middleware with improvements
        """
        # Get tabID from X-Tab-ID header (sent by extension)
        tab_id = request.headers.get('x-tab-id')

        if tab_id:
            # Use tabID as session identifier
            request.state.session_id = tab_id

            # Get or create session from SessionManager
            session = session_manager.get_or_create_session(tab_id)
            request.state.session = session
        else:
            # Only generate fallback for API endpoints that require sessions
            # This prevents creating unnecessary sessions for static resources
            path = request.url.path
            
            # Skip session creation for static resources
            if path.endswith(('.js', '.css', '.svg', '.ico')) or '/static/' in path:
                # For static resources, just use a placeholder
                request.state.session_id = 'static'
                request.state.session = {'sessionId': 'static'}
            else:
                # Fallback for API requests without tabID
                fallback_id = generate_fallback_id()
                request.state.session_id = fallback_id
                request.state.session = {
                    'sessionId': fallback_id,
                    'actorCommands': [],
                    'created': datetime.now().isoformat()
                }
                
                # Don't store fallback sessions - they're temporary for API calls only

        # Ensure session has all required arrays (for non-static requests)
        if request.state.session_id != 'static':
            session = request.state.session
            if 'unprocessedEvents' not in session:
                session['unprocessedEvents'] = []
            if 'processedEvents' not in session:
                session['processedEvents'] = []
            if 'retrievedActorCommands' not in session:
                session['retrievedActorCommands'] = []
            if 'actorCommands' not in session:
                session['actorCommands'] = []

        # Continue with request
        response = await call_next(request)
        return response

    return session_middleware


def get_session_from_request(request: Request) -> Dict[str, Any]:
    """Extract session from request state"""
    return getattr(request.state, 'session', {})


def get_session_id_from_request(request: Request) -> str:
    """Extract session ID from request state"""
    return getattr(request.state, 'session_id', 'unknown')


# Helper functions for session operations (direct ports from Node.js)

def add_event_to_session(session: Dict[str, Any], event: Dict[str, Any]) -> None:
    """Add event to session with FIFO queue management"""
    session['unprocessedEvents'].append(event)

    if len(session['unprocessedEvents']) > MAX_UNPROCESSED_EVENTS:
        # Move oldest event to processed queue
        oldest_event = session['unprocessedEvents'].pop(0)
        session['processedEvents'].append(oldest_event)

        # Maintain processed events limit
        if len(session['processedEvents']) > MAX_PROCESSED_EVENTS:
            session['processedEvents'].pop(0)


def clear_all_events(session: Dict[str, Any]) -> None:
    """Clear all events from session"""
    all_events = session['processedEvents'] + session['unprocessedEvents']
    session['unprocessedEvents'] = []
    session['processedEvents'] = []


def add_actor_command(session: Dict[str, Any], enriched_command: Dict[str, Any]) -> None:
    """Add actor command to session with queue management"""
    session['actorCommands'].append(enriched_command)

    # Maintain command queue limit
    if len(session['actorCommands']) > MAX_COMMANDS_PER_SESSION:
        dropped = session['actorCommands'].pop(0)
        log(f"add_actor_command: Dropped oldest command due to queue limit: {dropped.get('id', 'unknown')}")


def get_pending_actor_commands(session: Dict[str, Any]) -> list:
    """Get all pending actor commands and clear the queue"""
    pending = session['actorCommands'].copy()
    session['actorCommands'].clear()
    
    # Add to retrieved commands history
    if 'retrievedActorCommands' not in session:
        session['retrievedActorCommands'] = []
    
    session['retrievedActorCommands'].extend(pending)
    
    # Maintain retrieved commands limit
    MAX_RETRIEVED_COMMANDS = 100
    if len(session['retrievedActorCommands']) > MAX_RETRIEVED_COMMANDS:
        excess = len(session['retrievedActorCommands']) - MAX_RETRIEVED_COMMANDS
        session['retrievedActorCommands'] = session['retrievedActorCommands'][excess:]
    
    return pending


def get_session_status(session: Dict[str, Any]) -> Dict[str, Any]:
    """Get session status information"""
    return {
        'exists': True,
        'eventCount': len(session.get('unprocessedEvents', [])) + len(session.get('processedEvents', [])),
        'unprocessedEventCount': len(session.get('unprocessedEvents', [])),
        'processedEventCount': len(session.get('processedEvents', [])),
        'actorCommandCount': len(session.get('retrievedActorCommands', [])),
        'pendingCommandCount': len(session.get('actorCommands', [])),
        'retrievedCommandCount': len(session.get('retrievedActorCommands', [])),
        'oldestCommand': session['actorCommands'][0] if session.get('actorCommands') else None
    }
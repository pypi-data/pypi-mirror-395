from datetime import datetime
from typing import Dict, Any, List
from fastapi import APIRouter, Request, HTTPException, Query

from ..dependencies import (
    session_manager, validate_session_dependency, 
    MAX_PROCESSED_EVENTS
)
from ..models.sessions import (
    TabIdentity, SessionInitResponse, SessionStatus
)
from ..models.events import EventResponse
from ..middleware.session_middleware import (
    get_session_id_from_request, add_event_to_session, get_session_status
)
from ..utils.logging import (
    log, log_debug, log_error, count_observer_event, count_session
)
from ..streaming.server_streamer import get_server_streamer

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.put("/init", response_model=SessionInitResponse)
async def sessions_init(tab_identity: TabIdentity, request: Request):
    """Initialize new session"""
    try:
        if not tab_identity.tabId or not tab_identity.url:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Missing required fields: tabId and url are required",
                    "received": tab_identity.dict()
                }
            )
        
        log_debug(f"Session Init: Registering session {tab_identity.tabId} - {tab_identity.url}")
        
        # Create session data structure in session_store
        session_manager.get_or_create_session(tab_identity.tabId)
        
        # Register session metadata in active_sessions registry
        session_manager.register_session(tab_identity.tabId, {
            "tabId": tab_identity.tabId,
            "url": tab_identity.url,
            "title": tab_identity.title or "Untitled",
            "windowId": tab_identity.windowId,
            "index": tab_identity.index,
            "capabilities": ["observer", "actor"]
        })
        
        return SessionInitResponse(
            success=True,
            sessionId=tab_identity.tabId,
            message=f"Session {tab_identity.tabId} registered successfully"
        )
        
    except HTTPException:
        raise
    except Exception as error:
        log_error(f"Session Init: Error registering session: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.get("")
async def sessions_list():
    """List all active sessions"""
    try:
        sessions = []
        for session_id, session in session_manager.sessions.items():
            sessions.append({
                "sessionId": session_id,
                "tabId": session.get("tabId", session_id),
                "url": session.get("url", "unknown"),
                "title": session.get("title", "Unknown"),
                "created": session.get("created"),
                "lastActivity": session.get("lastActivity"),
                "capabilities": ["observer", "actor"]
            })
        return sessions
    except Exception as error:
        log_error(f"ERROR in sessions endpoint: {error}")
        return []


@router.post("/close")
async def sessions_close(request: Request):
    """Close session when tab is closed"""
    try:
        session_id = get_session_id_from_request(request)
        
        if session_manager.has_session(session_id):
            log(f"Explicit close request for session {session_id}")
            session_manager.close_session(session_id)
            return {"success": True, "message": f"Session {session_id} closed"}
        else:
            return {"success": False, "message": f"Session {session_id} not found"}
    except Exception as error:
        log(f"Error closing session: {error}")
        return {"success": False, "error": str(error)}


@router.post("/{session_id}/heartbeat")
async def sessions_heartbeat(session_id: str, request: Request):
    """Update session activity timestamp"""
    try:
        if session_manager.has_session(session_id):
            session_manager.update_session_activity(session_id)
            log(f"Heartbeat received for session {session_id}", True)  # Log but skip console
            return {"success": True}
        return {"success": False, "error": "Session not found"}
    except Exception as error:
        log(f"Error processing heartbeat for {session_id}: {error}")
        return {"success": False, "error": str(error)}


@router.post("/{session_id}/events", response_model=EventResponse)
async def sessions_events_post(session_id: str, event_data: Dict[str, Any], request: Request):
    """Submit new browser event to specific session"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    
    try:
        if not event_data or not isinstance(event_data, dict):
            raise HTTPException(status_code=400, detail={"error": "Invalid event data"})
        
        # Convert timestamp from milliseconds to datetime object for proper BSON Date storage
        if 'timestamp' in event_data:
            timestamp_val = event_data['timestamp']
            if isinstance(timestamp_val, (int, float)):
                # Convert milliseconds to datetime object
                event_data['timestamp'] = datetime.fromtimestamp(timestamp_val / 1000)
            elif isinstance(timestamp_val, str):
                # Handle legacy ISO string timestamps for backward compatibility
                try:
                    event_data['timestamp'] = datetime.fromisoformat(timestamp_val.replace('Z', '+00:00'))
                except ValueError:
                    # If parsing fails, use current time
                    event_data['timestamp'] = datetime.now()
        else:
            # Add timestamp if not present
            event_data["timestamp"] = datetime.now()
        
        # Reduced verbosity - only log important events or errors, not routine processing
        if event_data.get('type') not in ['log', 'screen_status', 'heartbeat']:
            # Only log non-routine event types
            log_debug(f"Session Event [{session_id}]: Processing event type={event_data.get('type')}")
        
        # Add event to session
        add_event_to_session(session, event_data)
        
        # Count Observer event for statistics
        count_observer_event()
        count_session(session_id)
        
        # Stream Observer event for debugging
        try:
            server_streamer = await get_server_streamer()
            if server_streamer:
                await server_streamer.stream_observer_event(session_id, event_data)
        except Exception as stream_error:
            log_debug(f"Observer streaming error: {stream_error}")

        # Process event through session's Story Assembly pipeline  
        story_result = {'success': False, 'story_updated': False}
        try:
            log_debug(f"Processing event for session {session_id}, type: {event_data.get('type')}, session keys: {list(session.keys())}")
            story_assembler = session.get("story_assembler")
            if story_assembler:
                log_debug(f"Found story assembler for session {session_id}")
                log_debug(f"Processing event type: {event_data.get('type', 'unknown')}")
                story = await story_assembler.process_event(session_id, event_data)
                story_result = {
                    'success': True, 
                    'story_updated': story is not None
                }
                log_debug(f"Story processing result for {session_id}: {story_result}")
                
                # Stream Story event for debugging (if story was updated)
                if story:
                    try:
                        server_streamer = await get_server_streamer()
                        if server_streamer:
                            # Convert story to dict for streaming
                            story_data = story.model_dump()
                            await server_streamer.stream_story_event(session_id, story_data)
                    except Exception as stream_error:
                        log_debug(f"Story streaming error: {stream_error}")
            else:
                log_debug(f"No story assembler found for session {session_id}")
        except Exception as story_error:
            log_error(f"Story processing exception: {story_error}")
            import traceback
            log_error(f"Story processing traceback: {traceback.format_exc()}")
        
        # Update session activity
        session_manager.update_session_activity(session_id)
        
        return EventResponse(
            success=True,
            sessionId=session_id,
            message="Event processed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as error:
        log_error(f"Session Event Post [{session_id}]: Error posting event: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.get("/{session_id}/events/recent")
async def sessions_events_recent(session_id: str, request: Request, limit: int = Query(50)):
    """Get recent events for session"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    
    try:
        # Get recent events from both processed and unprocessed
        all_events = session.get("processedEvents", []) + session.get("unprocessedEvents", [])
        events = all_events[-limit:] if limit > 0 else all_events
        
        log_debug(f"Session Events Recent [{session_id}]: Retrieved {len(events)} recent events")
        return events  # Return array directly for Node.js TestingFramework compatibility
        
    except Exception as error:
        log(f"Session Events Recent [{session_id}]: Error retrieving events: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.get("/{session_id}/events/consume")
async def sessions_events_consume(session_id: str, request: Request):
    """Consume unprocessed events for session (FIFO Queue)"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    
    try:
        # Get events to consume
        events_to_consume = session.get("unprocessedEvents", []).copy()
        
        # Move unprocessed to processed
        session.setdefault("processedEvents", []).extend(session.get("unprocessedEvents", []))
        session["unprocessedEvents"] = []
        
        # Maintain processed events limit
        if len(session["processedEvents"]) > MAX_PROCESSED_EVENTS:
            excess = len(session["processedEvents"]) - MAX_PROCESSED_EVENTS
            session["processedEvents"] = session["processedEvents"][excess:]
        
        # Update session activity
        session_manager.update_session_activity(session_id)
        
        log_debug(f"Session Events Consume [{session_id}]: Consumed {len(events_to_consume)} events, {len(session['processedEvents'])} total processed")
        return events_to_consume  # Return array directly for Node.js TestingFramework compatibility
        
    except Exception as error:
        log_error(f"Session Events Consume [{session_id}]: Error consuming events: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.get("/{session_id}/events/unprocessed")
async def sessions_events_unprocessed(session_id: str, request: Request):
    """View unprocessed events for session"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    
    try:
        unprocessed_events = session.get("unprocessedEvents", [])
        log(f"Session Events Unprocessed [{session_id}]: Viewing {len(unprocessed_events)} unprocessed events")
        return unprocessed_events  # Return array directly for Node.js TestingFramework compatibility
        
    except Exception as error:
        log(f"Session Events Unprocessed [{session_id}]: Error viewing unprocessed events: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.get("/{session_id}/events/processed")
async def sessions_events_processed(session_id: str, request: Request, limit: int = Query(50)):
    """View processed events for session"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    
    try:
        processed_events = session.get("processedEvents", [])
        recent_processed = processed_events[-limit:] if limit > 0 else processed_events
        
        log(f"Session Events Processed [{session_id}]: Viewing {len(recent_processed)} processed events")
        return recent_processed  # Return array directly for Node.js TestingFramework compatibility
        
    except Exception as error:
        log(f"Session Events Processed [{session_id}]: Error viewing processed events: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.get("/{session_id}/status", response_model=SessionStatus)
async def sessions_status(session_id: str, request: Request):
    """Get status for specific session"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    session_info = session_data["sessionInfo"]
    
    try:
        status = get_session_status(session)
        status["sessionId"] = session_id
        status["created"] = session.get("created")
        
        # Add session registry info to status (matching Node.js behavior)
        if session_info:
            status["registryInfo"] = {
                "tabId": session_info.get("tabId"),
                "url": session_info.get("url"),
                "title": session_info.get("title"),
                "windowId": session_info.get("windowId"),  
                "index": session_info.get("index"),
                "lastActivity": session_info.get("lastActivity"),
                "capabilities": session_info.get("capabilities", [])
            }
        
        log_debug(f"Session Status [{session_id}]: Status retrieved")
        return status
        
    except Exception as error:
        log(f"Session Status [{session_id}]: Error retrieving status: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})

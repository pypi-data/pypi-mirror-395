from typing import Dict, Any, List
from fastapi import APIRouter, Request, HTTPException, Query

from ..models.events import BrowserEvent, EventResponse
from ..middleware.session_middleware import (
    get_session_from_request, get_session_id_from_request,
    add_event_to_session, clear_all_events
)
from ..utils.logging import log, log_debug

router = APIRouter(tags=["legacy"])

# ========================================================================
# LEGACY ENDPOINTS (Non-session based for backward compatibility)
# ========================================================================

@router.post("/event", response_model=EventResponse)
async def event_post(event: BrowserEvent, request: Request):
    """Submit new browser event (legacy endpoint)"""
    session = get_session_from_request(request)
    session_id = get_session_id_from_request(request)
    
    try:
        event_data = event.dict()
        log(f"app.post/event [{session_id}]: Processing event: type={event_data.get('type')}")
        
        add_event_to_session(session, event_data)
        
        log(f"app.post/event [{session_id}]: Event processed successfully: type={event_data.get('type')}")
        return EventResponse(success=True, sessionId=session_id)
        
    except Exception as error:
        log(f"app.post/event [{session_id}]: Error processing event: {error}")
        raise HTTPException(status_code=400, detail={"error": str(error)})


@router.post("/events/clear")
async def events_clear(request: Request):
    """Clear all stored events (legacy endpoint)"""
    session = get_session_from_request(request)
    session_id = get_session_id_from_request(request)
    
    try:
        log(f"app.post/events/clear [{session_id}]: Clearing all events")
        clear_all_events(session)
        log(f"app.post/events/clear [{session_id}]: Events cleared successfully")
        return {"success": True, "sessionId": session_id}
        
    except Exception as error:
        log(f"app.post/events/clear [{session_id}]: Error clearing events: {error}")
        raise HTTPException(status_code=400, detail={"error": str(error)})


@router.get("/events/recent")
async def events_recent(request: Request, limit: int = Query(50)):
    """Get recent events (legacy endpoint)"""
    session = get_session_from_request(request)
    session_id = get_session_id_from_request(request)
    
    try:
        all_events = session.get("processedEvents", []) + session.get("unprocessedEvents", [])
        events = all_events[-limit:] if limit > 0 else all_events
        
        log_debug(f"app.get/events/recent [{session_id}]: Retrieving {len(events)} recent events")
        return events  # Return array directly for Node.js TestingFramework compatibility
        
    except Exception as error:
        log(f"app.get/events/recent [{session_id}]: Error retrieving events: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.get("/events/unbroadcast")
async def events_unbroadcast(request: Request):
    """Get unbroadcast events (legacy endpoint for compatibility)"""
    session_id = get_session_id_from_request(request)
    log(f"app.get/events/unbroadcast [{session_id}]: Retrieving unbroadcast events data (legacy endpoint)")
    return []  # Legacy endpoint - return empty array for compatibility

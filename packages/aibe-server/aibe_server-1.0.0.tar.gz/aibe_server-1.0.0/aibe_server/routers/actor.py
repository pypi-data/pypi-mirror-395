from typing import Dict, Any, List
from fastapi import APIRouter, Request, HTTPException, Query

from ..dependencies import (
    session_manager, validate_session_dependency, enrich_command,
    MAX_COMMANDS_PER_SESSION
)
from ..middleware.session_middleware import (
    add_actor_command, get_pending_actor_commands,
    get_session_from_request, get_session_id_from_request
)
from ..utils.logging import (
    log, log_debug, log_error, count_actor_command
)
from ..streaming.server_streamer import get_server_streamer

router = APIRouter(tags=["actor"])

# ========================================================================
# SESSION-BASED ACTOR ENDPOINTS
# ========================================================================

@router.post("/sessions/{session_id}/actor/send")
async def sessions_actor_send(session_id: str, request: Request):
    """Send Actor command to session"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    
    try:
        # Get raw JSON body to handle both single commands and arrays (matching Node.js)
        input_data = await request.json()
        
        # Handle both single commands and arrays
        if isinstance(input_data, list):
            commands_data = input_data
        else:
            commands_data = [input_data]
        
        log_debug(f"Session Actor [{session_id}]: Queueing {len(commands_data)} commands")
        
        # Validate and enrich commands
        results = []
        for command_data in commands_data:
            if not command_data.get("type"):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "All commands must have a type field",
                        "invalidCommand": command_data
                    }
                )
            
            enriched_command = enrich_command(command_data)
            add_actor_command(session, enriched_command)
            
            # Count Actor command for statistics
            count_actor_command()
            
            log_debug(f"Session Actor [{session_id}]: Queued command {enriched_command['id']} of type {enriched_command['type']}")
            
            results.append({
                "commandId": enriched_command["id"],
                "type": enriched_command["type"],
                "status": "queued"
            })
        
        # Update session activity
        session_manager.update_session_activity(session_id)
        
        return {
            "success": True,
            "sessionId": session_id,
            "commandsQueued": len(results),
            "commands": results,
            "message": f"{len(results)} command(s) queued for session {session_id}"
        }
        
    except HTTPException:
        raise
    except Exception as error:
        log_error(f"Session Actor [{session_id}]: Error queueing commands: {error}")
        raise HTTPException(status_code=400, detail={"error": str(error)})


@router.get("/sessions/{session_id}/actor/commands")
async def sessions_actor_commands(session_id: str, request: Request):
    """Poll Actor commands for session"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    
    try:
        # Get pending commands and clear queue
        commands = get_pending_actor_commands(session)
        
        # Stream Actor events for debugging (when commands are consumed)
        if commands:
            try:
                server_streamer = await get_server_streamer()
                if server_streamer:
                    for command in commands:
                        await server_streamer.stream_actor_event(session_id, command)
            except Exception as stream_error:
                log_debug(f"Actor streaming error: {stream_error}")
        
        # Only log when there are commands to report - reduces chattiness
        if commands:
            log_debug(f"Session Commands [{session_id}]: Retrieved {len(commands)} pending commands")
        
        # Update session activity
        session_manager.update_session_activity(session_id)
        
        # Return just the commands array directly to match JS server behavior
        # This is what the extension expects (not an object with a commands property)
        return commands
        
    except Exception as error:
        log(f"Session Commands [{session_id}]: Error retrieving commands: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.get("/sessions/{session_id}/actor/retrieved")
async def sessions_actor_retrieved(session_id: str, request: Request, limit: int = Query(50)):
    """View retrieved Actor commands from specific session"""
    session_data = validate_session_dependency(session_id, request)
    session = session_data["session"]
    
    try:
        retrieved_commands = session.get("retrievedActorCommands", [])
        recent_retrieved = retrieved_commands[-limit:] if limit > 0 else retrieved_commands
        
        session_manager.update_session_activity(session_id)
        
        log_debug(f"Session Actor Retrieved [{session_id}]: Viewing {len(recent_retrieved)} recent retrieved commands (limit: {limit})")
        return {"commands": recent_retrieved, "total": len(recent_retrieved), "sessionId": session_id}
        
    except Exception as error:
        log(f"Session Actor Retrieved [{session_id}]: Error viewing retrieved commands: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


# ========================================================================
# LEGACY ACTOR ENDPOINTS
# ========================================================================

@router.get("/actor/commands")
async def actor_commands(request: Request):
    """Poll for pending Actor commands (legacy endpoint)"""
    session = get_session_from_request(request)
    session_id = get_session_id_from_request(request)
    
    try:
        commands = get_pending_actor_commands(session)
        
        # Only log when commands are actually delivered (reduces polling noise)
        if commands:
            log(f"Actor Commands [{session_id}]: Delivered {len(commands)} commands to browser")
        
        # Return just the commands array directly to match JS server behavior
        # This is what the extension expects (not an object with a commands property)
        log(f"Actor Commands [{session_id}]: Returning commands array directly for extension compatibility")
        return commands
        
    except Exception as error:
        log(f"Actor Commands [{session_id}]: Error retrieving commands: {error}")
        raise HTTPException(status_code=500, detail={"error": str(error)})


@router.post("/actor/send")
async def actor_send(request: Request):
    """Queue new Actor command(s) for browser execution"""
    session = get_session_from_request(request)
    session_id = get_session_id_from_request(request)
    
    try:
        # Get raw JSON body to handle both single commands and arrays (matching Node.js)
        input_data = await request.json()
        
        # Handle both single commands and arrays
        if isinstance(input_data, list):
            commands_data = input_data
        else:
            commands_data = [input_data]
        
        log(f"Actor Send [{session_id}]: Queueing {len(commands_data)} commands")
        
        # Validate and enrich commands
        results = []
        for command_data in commands_data:
            if not command_data.get("type"):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "All commands must have a type field",
                        "invalidCommand": command_data
                    }
                )
            
            enriched_command = enrich_command(command_data)
            add_actor_command(session, enriched_command)
            
            log(f"Actor Send [{session_id}]: Queued command {enriched_command['id']} of type {enriched_command['type']}")
            
            results.append({
                "commandId": enriched_command["id"],
                "type": enriched_command["type"],
                "status": "queued"
            })
        
        return {
            "success": True,
            "commandsQueued": len(results),
            "commands": results,
            "message": f"{len(results)} command(s) queued for browser execution"
        }
        
    except HTTPException:
        raise
    except Exception as error:
        log(f"Actor Send [{session_id}]: Error queueing commands: {error}")
        raise HTTPException(status_code=400, detail={"error": str(error)})


@router.get("/actor/test")
async def actor_test(request: Request):
    """Send test command to verify Actor channel functionality"""
    # This was incomplete in main.py, implementing basic test command
    session = get_session_from_request(request)
    session_id = get_session_id_from_request(request)
    
    test_command = {
        "type": "log",
        "message": "Test command from server"
    }
    
    enriched_command = enrich_command(test_command)
    add_actor_command(session, enriched_command)
    
    return {
        "success": True, 
        "message": "Test command queued",
        "command": enriched_command
    }

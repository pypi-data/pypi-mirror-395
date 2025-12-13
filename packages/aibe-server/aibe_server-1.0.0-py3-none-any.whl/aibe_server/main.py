"""
FastAPI Browser-AI Interface Server
Direct port from Node.js server.cjs with exact functional parity
Maintains all 25+ endpoints with identical behavior
"""

import os
import sys
import asyncio
import uuid
import uvicorn
import json
import time
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Local imports
from .dependencies import session_manager, PORT, MAX_COMMANDS_PER_SESSION
from .config_manager import get_config_manager, get_auth_config
from .routers import sessions, actor, legacy
from .middleware.session_middleware import (
    setup_session_middleware, get_session_from_request, get_session_id_from_request,
    get_session_status
)
from .utils.logging import initialize_logger, log, log_debug, log_info, log_warn, log_error
from .utils.process_management import ProcessManager, setup_signal_handlers
from .streaming.server_streamer import get_server_streamer, shutdown_server_streamer, reload_server_streamer

# Path helper functions
def get_tests_dir():
    return Path(__file__).parent / "tests"

def get_extension_dir():
    return Path(__file__).parent / "extension"

def serve_package_file(subdir: str, filename: str, media_type: str):
    try:
        file_path = Path(__file__).parent / subdir / filename
        if file_path.exists():
            return FileResponse(str(file_path), media_type=media_type)
        else:
            parent_dir = file_path.parent
            if parent_dir.exists():
                files = [f.name for f in parent_dir.iterdir()]
                error_msg = f"File {filename} not found in {parent_dir}. Available: {files}"
            else:
                error_msg = f"Directory {parent_dir} does not exist"
            log(f"File serve error: {error_msg}")
            raise HTTPException(status_code=404, detail=error_msg)
    except Exception as e:
        log(f"Error serving {subdir}/{filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def parse_args():
    args = sys.argv[1:]
    return {
        'debug': '--debug' in args,
        'detached': '--detached' in args
    }

# Global variables
app_config = parse_args()
server_dir = Path(__file__).parent.parent
process_manager = ProcessManager(str(server_dir), app_config['detached'])

# Initialize logging
initialize_logger(str(server_dir), app_config['detached'])

log("main.py: === NEW SERVER SESSION STARTED ===", True)
log(f"main.py: Mode: {'DEBUG' if app_config['debug'] else 'NORMAL'}", True)

process_manager.check_existing_server()
process_manager.save_pid()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        asyncio.create_task(cleanup_task())
        log("Session cleanup background task started")
        server_streamer = await get_server_streamer()
        if server_streamer and server_streamer.is_connected():
            log(f"ServerStreamer initialized: {server_streamer.get_collection_name()}")
    except Exception as error:
        log_error(f"ServerStreamer startup error: {error}")
    yield
    try:
        await shutdown_server_streamer()
        log("ServerStreamer shutdown complete")
    except Exception as error:
        log_error(f"ServerStreamer shutdown error: {error}")

app = FastAPI(
    title="Browser-AI Interface Server",
    description="HTTP server for browser automation and AI interaction",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
session_middleware = setup_session_middleware(session_manager)
app.middleware("http")(session_middleware)

# Register Routers
app.include_router(sessions.router)
app.include_router(actor.router)
app.include_router(legacy.router)

async def cleanup_task():
    while True:
        try:
            await asyncio.sleep(300)
            expired_count = session_manager.cleanup_expired_sessions(max_age_ms=30 * 60 * 1000)
            if expired_count > 0:
                log(f"Cleaned up {expired_count} expired sessions")
        except Exception as e:
            log(f"Error in cleanup task: {e}")

@app.get("/status")
async def status(request: Request):
    """Server status and statistics"""
    session = get_session_from_request(request)
    session_id = get_session_id_from_request(request)
    
    if session:
        session_status = get_session_status(session)
        status_data = {
            "version": "1.0.0",
            "uptime": time.time() - process_manager.start_time,
            "sessionId": session_id,
            "sessionBased": True,
            "eventCount": session_status["eventCount"],
            "unprocessedEventCount": session_status["unprocessedEventCount"],
            "processedEventCount": session_status["processedEventCount"],
            "clientCount": 0,
            "lastEventSent": -1,
            "unbroadcastCount": session_status["unprocessedEventCount"],
            "pendingActorCommands": session_status["pendingCommandCount"],
            "maxCommandCapacity": MAX_COMMANDS_PER_SESSION,
            "oldestPendingCommand": session_status["oldestCommand"],
            "mode": "DEBUG" if app_config['debug'] else "NORMAL",
            "detached": app_config['detached'],
            "pid": os.getpid(),
            "nodeVersion": sys.version,
            "startTime": datetime.fromtimestamp(process_manager.start_time).isoformat(),
            "platform": platform.system(),
            "extensionPath": str(get_extension_dir().absolute())
        }
    else:
        status_data = {
            "version": "1.0.0",
            "uptime": time.time() - process_manager.start_time,
            "sessionBased": False,
            "note": "Session-based architecture active - status shown is server-wide only",
            "mode": "DEBUG" if app_config['debug'] else "NORMAL",
            "detached": app_config['detached'],
            "pid": os.getpid(),
            "nodeVersion": sys.version,
            "startTime": datetime.fromtimestamp(process_manager.start_time).isoformat(),
            "platform": platform.system(),
            "extensionPath": str(get_extension_dir().absolute())
        }
    return status_data

@app.get("/api/status")
async def api_status(request: Request):
    """API-style status endpoint"""
    return await status(request)


# ========================================================================
# STATIC FILE ENDPOINTS
# ========================================================================

@app.get("/favicon.svg")
async def favicon():
    """Server favicon"""
    favicon_path = server_dir / "aibe_server" / "static" / "favicon.svg"
    if favicon_path.exists():
        return FileResponse(
            str(favicon_path),
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=3600"}
        )
    raise HTTPException(status_code=404, detail="Favicon not found")


@app.get("/TestingFramework.js")
async def testing_framework_js():
    """Testing framework JavaScript library"""
    return serve_package_file("tests/framework", "TestingFramework.js", "application/javascript")


@app.get("/GenericElementTest.js")
async def generic_element_test_js():
    """Generic element testing library"""
    return serve_package_file("tests/framework", "GenericElementTest.js", "application/javascript")


@app.get("/DataDrivenTestRunner.js")
async def data_driven_test_runner_js():
    """Data-driven test runner library"""
    return serve_package_file("tests/framework", "DataDrivenTestRunner.js", "application/javascript")


# ========================================================================
# CHROME EXTENSION FILE ENDPOINTS
# ========================================================================

@app.get("/extension/manifest.json")
async def extension_manifest():
    """Chrome extension manifest file"""
    manifest_path = get_extension_dir() / "manifest.json"
    if manifest_path.exists():
        return FileResponse(
            str(manifest_path),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=manifest.json"}
        )
    raise HTTPException(status_code=404, detail="Extension manifest not found")


@app.get("/extension/content.js")
async def extension_content_js():
    """Chrome extension content script"""
    content_path = get_extension_dir() / "content.js"
    if content_path.exists():
        return FileResponse(
            str(content_path),
            media_type="application/javascript",
            headers={"Content-Disposition": "attachment; filename=content.js"}
        )
    raise HTTPException(status_code=404, detail="Extension content.js not found")


@app.get("/extension/background.js")
async def extension_background_js():
    """Chrome extension background script"""
    background_path = get_extension_dir() / "background.js"
    if background_path.exists():
        return FileResponse(
            str(background_path),
            media_type="application/javascript",
            headers={"Content-Disposition": "attachment; filename=background.js"}
        )
    raise HTTPException(status_code=404, detail="Extension background.js not found")


@app.get("/extension/popup.js")
async def extension_popup_js():
    """Chrome extension popup script"""
    popup_js_path = get_extension_dir() / "popup.js"
    if popup_js_path.exists():
        return FileResponse(
            str(popup_js_path),
            media_type="application/javascript",
            headers={"Content-Disposition": "attachment; filename=popup.js"}
        )
    raise HTTPException(status_code=404, detail="Extension popup.js not found")


@app.get("/extension/popup.html")
async def extension_popup_html():
    """Chrome extension popup HTML"""
    popup_html_path = get_extension_dir() / "popup.html"
    if popup_html_path.exists():
        return FileResponse(
            str(popup_html_path),
            media_type="text/html",
            headers={"Content-Disposition": "attachment; filename=popup.html"}
        )
    raise HTTPException(status_code=404, detail="Extension popup.html not found")


@app.get("/extension/install")
async def extension_install_guide():
    """Chrome extension installation guide"""
    extension_path = get_extension_dir().absolute()
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AIBE Chrome Extension Installation</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        .download-links {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .download-links a {{ display: inline-block; margin: 10px 15px 10px 0; padding: 8px 16px; 
                           background: #007cba; color: white; text-decoration: none; border-radius: 4px; }}
        .download-links a:hover {{ background: #005a87; }}
        ol {{ line-height: 1.6; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>🤖 AIBE Chrome Extension Installation</h1>
    
    <h2>Step 1: Locate Extension Files</h2>
    <p><strong>Extension files are located at:</strong></p>
    <code style="display: block; background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 4px;">{extension_path}</code>
    
    <p>You can either use the files directly from this location, or download them individually:</p>
    <div class="download-links">
        <a href="/extension/manifest.json">manifest.json</a>
        <a href="/extension/content.js">content.js</a>
        <a href="/extension/background.js">background.js</a>
        <a href="/extension/popup.js">popup.js</a>
        <a href="/extension/popup.html">popup.html</a>
    </div>
    
    <h2>Step 2: Create Extension Directory</h2>
    <ol>
        <li>Create a new folder on your computer (e.g., <code>aibe-extension</code>)</li>
        <li>Download all 5 files above into this folder</li>
        <li>Make sure all files are in the same directory</li>
    </ol>
    
    <h2>Step 3: Install in Chrome</h2>
    <ol>
        <li>Open Chrome and go to <code>chrome://extensions/</code></li>
        <li>Enable "Developer mode" (toggle in top right corner)</li>
        <li>Click "Load unpacked"</li>
        <li>Navigate to and select the extension directory shown above, OR select your downloaded files folder</li>
        <li>The AIBE extension should appear in your extensions list</li>
    </ol>
    
    <h2>Step 4: Verify Installation</h2>
    <p>The extension will automatically connect to this server at <code>localhost:3001</code>. 
    Check the <a href="/status">server status</a> to see connected sessions.</p>
    
    <h2>Troubleshooting</h2>
    <ul>
        <li>Make sure the AIBE server is running on port 3001</li>
        <li>Check that all 5 extension files are in the same directory</li>
        <li>Ensure "Developer mode" is enabled in Chrome extensions</li>
        <li>If the extension doesn't load, check Chrome's extension error messages</li>
    </ul>
    
    <p><a href="/">← Back to Server Home</a></p>
</body>
</html>"""
    return HTMLResponse(content=html_content)


# ========================================================================
# HTML TEST INTERFACE ENDPOINTS
# ========================================================================

@app.get("/test-inputs", response_class=HTMLResponse)
async def test_inputs():
    """Input fields test page"""
    html_path = get_tests_dir() / "pages" / "test-inputs.html"
    if html_path.exists():
        return FileResponse(str(html_path), media_type="text/html")
    raise HTTPException(status_code=404, detail="test-inputs.html not found")


@app.get("/test-controls", response_class=HTMLResponse) 
async def test_controls():
    """Comprehensive controls test page"""
    html_path = get_tests_dir() / "pages" / "test-controls.html"
    if html_path.exists():
        return FileResponse(str(html_path), media_type="text/html")
    raise HTTPException(status_code=404, detail="test-controls.html not found")


@app.get("/test-runner", response_class=HTMLResponse)
async def test_runner():
    """Web-based test runner interface"""
    html_path = get_tests_dir() / "web-runner.html"
    if html_path.exists():
        return FileResponse(str(html_path), media_type="text/html")
    raise HTTPException(status_code=404, detail="web-runner.html not found")


@app.get("/framework/TestingFramework.js")
async def framework_testing_framework_js():
    """Testing framework JavaScript library (framework path)"""
    js_path = get_tests_dir() / "framework" / "TestingFramework.js"
    if js_path.exists():
        return FileResponse(
            str(js_path),
            media_type="application/javascript",
            headers={"Cache-Control": "public, max-age=3600"}
        )
    raise HTTPException(status_code=404, detail="TestingFramework.js not found")


@app.get("/framework/DataDrivenTestRunner.js")
async def framework_data_driven_test_runner_js():
    """Data driven test runner JavaScript library (framework path)"""
    js_path = get_tests_dir() / "framework" / "DataDrivenTestRunner.js"
    if js_path.exists():
        return FileResponse(
            str(js_path),
            media_type="application/javascript",
            headers={"Cache-Control": "public, max-age=3600"}
        )
    raise HTTPException(status_code=404, detail="DataDrivenTestRunner.js not found")


@app.get("/framework/GenericElementTest.js")
async def framework_generic_element_test_js():
    """Generic element testing library (framework path)"""
    js_path = get_tests_dir() / "framework" / "GenericElementTest.js"
    if js_path.exists():
        return FileResponse(
            str(js_path),
            media_type="application/javascript",
            headers={"Cache-Control": "public, max-age=3600"}
        )
    raise HTTPException(status_code=404, detail="GenericElementTest.js not found")


@app.get("/test-suites-config")
async def test_suites_config():
    """Test suites configuration data - loaded from JSON file"""
    try:
        # Load complete test suite data from JSON file (proper data/code separation)
        json_path = get_tests_dir() / "test-suites.json"
        
        if not json_path.exists():
            log(f"Test Suites Config: JSON file not found at {json_path}")
            raise HTTPException(status_code=404, detail="Test suites configuration file not found")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            test_suites_data = json.load(f)
        
        # Validate that we have the expected structure
        if "TEST_SUITES" not in test_suites_data:
            log("Test Suites Config: Invalid JSON structure - missing TEST_SUITES key")
            raise HTTPException(status_code=500, detail="Invalid test suites configuration format")
        
        suites_count = len(test_suites_data["TEST_SUITES"])
        log(f"Test Suites Config: Serving {suites_count} test suites from JSON file")
        
        return test_suites_data
        
    except FileNotFoundError:
        log("Test Suites Config: Test suites JSON file not found")
        raise HTTPException(status_code=404, detail="Test suites configuration file not found")
    except json.JSONDecodeError as e:
        log(f"Test Suites Config: Invalid JSON format: {e}")
        raise HTTPException(status_code=500, detail="Invalid JSON format in test suites configuration")
    except Exception as error:
        log(f"Test Suites Config: Error loading test suites: {error}")
        raise HTTPException(status_code=500, detail="Failed to load test suites configuration")


@app.get("/test-streaming-config")
async def test_streaming_config():
    """Test streaming configuration - non-authenticated for browser test runners"""
    try:
        config_manager = get_config_manager()
        config = config_manager.get_config()
        
        return {
            "test_streaming": config.test_streaming.model_dump(),
            "database": {
                "connection_string": config.database.connection_string,
                "database_name": config.database.database_name,
                "connection_timeout": config.database.connection_timeout,
                "max_pool_size": config.database.max_pool_size
            },
            "server": {
                "log_level": config.server.log_level
            }
        }
    except Exception as error:
        log(f"Test Streaming Config: Error loading config: {error}")
        raise HTTPException(status_code=500, detail="Failed to load test streaming configuration")


@app.get("/server-streaming-config")
async def server_streaming_config():
    """Server streaming configuration - for monitoring server streaming status"""
    try:
        config_manager = get_config_manager()
        config = config_manager.get_config()
        
        return {
            "server_streaming": config.server_streaming.model_dump(),
            "database": {
                "connection_string": config.database.connection_string,
                "database_name": config.database.database_name,
                "connection_timeout": config.database.connection_timeout,
                "max_pool_size": config.database.max_pool_size
            },
            "server": {
                "log_level": config.server.log_level
            }
        }
    except Exception as error:
        log(f"Server Streaming Config: Error loading config: {error}")
        raise HTTPException(status_code=500, detail="Failed to load server streaming configuration")


@app.post("/test-streaming/flush")
async def test_streaming_flush(request: Request):
    """Flush test streaming events to MongoDB - for browser test runners"""
    try:
        data = await request.json()
        collection_name = data.get('collection')
        database_name = data.get('database')
        events = data.get('events', [])
        
        if not collection_name or not database_name or not events:
            raise HTTPException(status_code=400, detail="Missing collection, database, or events")
        
        # Get MongoDB connection from config
        config_manager = get_config_manager()
        config = config_manager.get_config()
        
        # Import MongoDB client here to avoid import issues if not installed
        from pymongo import MongoClient
        
        # Connect to MongoDB
        client = MongoClient(config.database.connection_string)
        db = client[database_name]
        collection = db[collection_name]
        
        # Insert events
        if events:
            result = collection.insert_many(events)
            inserted_count = len(result.inserted_ids)
        else:
            inserted_count = 0
        
        client.close()
        
        return {
            "success": True,
            "inserted": inserted_count,
            "collection": collection_name,
            "database": database_name
        }
        
    except Exception as error:
        log(f"Test Streaming Flush: Error: {error}")
        raise HTTPException(status_code=500, detail=f"Failed to flush streaming events: {str(error)}")


@app.get("/test-result", response_class=HTMLResponse)
async def test_result(action: str = Query("unknown")):
    """Test result endpoint for button/link click testing"""
    timestamp = datetime.now().isoformat()
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Result - {{action}}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
        .result {{ background: #e8f5e8; border: 2px solid #4caf50; border-radius: 8px; padding: 20px; }}
        .action {{ font-size: 24px; font-weight: bold; color: #2e7d32; }}
        .timestamp {{ color: #666; font-size: 14px; }}
        .back-link {{ margin-top: 20px; }}
        .back-link a {{ color: #1976d2; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="result">
        <div class="action">✅ Test Action: {{action}}</div>
        <div class="timestamp">Timestamp: {{timestamp}}</div>
        <p>This page confirms that the button/link click was successfully detected and processed.</p>
        <div class="back-link">
            <a href="/test-controls">← Back to Test Controls</a>
        </div>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


@app.get("/sessions/explorer", response_class=HTMLResponse)
async def sessions_explorer():
    """Interactive session exploration interface"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sessions Explorer - Browser-AI Interface</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 1000px; 
            margin: 20px auto; 
            padding: 20px; 
            line-height: 1.6; 
        }
        .header {
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%);
            border: 2px solid #4caf50;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .controls {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #007cba;
        }
        .session-selector {
            margin-bottom: 15px;
        }
        select {
            padding: 8px 12px;
            font-size: 14px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
            min-width: 300px;
        }
        button {
            background-color: #007cba;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 2px;
            font-size: 14px;
        }
        button:hover {
            background-color: #005a87;
        }
        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        .action-buttons {
            margin-top: 10px;
        }
        .results {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            min-height: 200px;
        }
        .results h3 {
            margin-top: 0;
            color: #333;
        }
        .json-data {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 10px;
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
            overflow-x: auto;
            max-height: 400px;
            overflow-y: auto;
        }
        .error {
            color: #dc3545;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        }
        .success {
            color: #155724;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        }
        .loading {
            color: #007cba;
            font-style: italic;
        }
        a {
            color: #007cba;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔗 Sessions Explorer</h1>
        <p><strong>Interactive Browser Session Management</strong></p>
        <p>Explore and manage active browser sessions, view events, send Actor commands, and monitor session state.</p>
        <p><a href="/">← Back to Server Home</a></p>
    </div>

    <div class="controls">
        <div class="session-selector">
            <label for="sessionSelect"><strong>Select Session:</strong></label><br>
            <select id="sessionSelect">
                <option value="">Loading sessions...</option>
            </select>
            <button onclick="refreshSessions()">🔄 Refresh Sessions</button>
        </div>
        
        <div class="action-buttons">
            <strong>Session Actions:</strong><br>
            <button onclick="viewRecentEvents()" disabled id="btn-recent">📡 Recent Events</button>
            <button onclick="viewUnprocessedEvents()" disabled id="btn-unprocessed">📥 Unprocessed Events</button>
            <button onclick="viewProcessedEvents()" disabled id="btn-processed">📤 Processed Events</button>
            <button onclick="consumeEvents()" disabled id="btn-consume">🍽️ Consume Events</button>
            <button onclick="viewActorCommands()" disabled id="btn-actor-commands">🎯 Pending Actor Commands</button>
            <button onclick="viewActorRetrieved()" disabled id="btn-actor-retrieved">📜 Retrieved Actor Commands</button>
            <button onclick="viewActorSummary()" disabled id="btn-actor-summary">📊 Actor Command Status</button>
            <button onclick="viewSessionStatus()" disabled id="btn-status">📋 Session Status</button>
        </div>
    </div>

    <div class="results" id="results">
        <h3>Results</h3>
        <p>Select a session and choose an action to explore session data.</p>
    </div>

    <script>
        let currentSessionId = null;
        
        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            refreshSessions();
            
            // Set up session selector change handler
            document.getElementById('sessionSelect').addEventListener('change', function() {
                currentSessionId = this.value;
                updateButtonStates();
                clearResults();
            });
        });
        
        function updateButtonStates() {
            const hasSession = currentSessionId && currentSessionId !== '';
            const buttons = ['btn-recent', 'btn-unprocessed', 'btn-processed', 'btn-consume', 'btn-actor-commands', 'btn-actor-retrieved', 'btn-actor-summary', 'btn-status'];
            buttons.forEach(id => {
                const btn = document.getElementById(id);
                if (btn) btn.disabled = !hasSession;
            });
        }
        
        function clearResults() {
            document.getElementById('results').innerHTML = '<h3>Results</h3><p>Select a session and choose an action to explore session data.</p>';
        }
        
        function showLoading(message = 'Loading...') {
            document.getElementById('results').innerHTML = `<h3>Results</h3><p class="loading">${message}</p>`;
        }
        
        function showError(message) {
            document.getElementById('results').innerHTML = `<h3>Results</h3><div class="error">❌ Error: ${message}</div>`;
        }
        
        function showSuccess(title, data) {
            let content = `<h3>${title}</h3>`;
            if (typeof data === 'object') {
                content += `<div class="json-data">${JSON.stringify(data, null, 2)}</div>`;
            } else {
                content += `<div class="success">${data}</div>`;
            }
            document.getElementById('results').innerHTML = content;
        }
        
        async function refreshSessions() {
            showLoading('Refreshing sessions...');
            try {
                const response = await fetch('/sessions');
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                const sessionsResponse = await response.json();
                const sessions = sessionsResponse.sessions || sessionsResponse; // Handle both response formats
                
                const select = document.getElementById('sessionSelect'); 
                select.innerHTML = '<option value="">-- Select a session --</option>';
                
                if (!sessions || sessions.length === 0) {
                    select.innerHTML += '<option value="" disabled>No active sessions found</option>';
                    showError('No active browser sessions found. Make sure the Chrome extension is loaded and browse to localhost:3001 in a tab.');
                } else {
                    sessions.forEach(session => {
                        const option = document.createElement('option');
                        option.value = session.sessionId || session.tabId;
                        // Handle different possible session data structures
                        const url = session.tabInfo?.url || session.url || 'Unknown URL';
                        const sessionId = session.sessionId || session.tabId;
                        option.textContent = `${sessionId} (${url})`;
                        select.appendChild(option);
                    });
                    showSuccess('Sessions Loaded', `Found ${sessions.length} active session(s). Select one to explore.`);
                }
                
                currentSessionId = null;
                updateButtonStates();
                
            } catch (error) {
                showError(`Failed to load sessions: ${error.message}`);
                console.error('Session refresh error:', error);
            }
        }
        
        async function makeSessionRequest(endpoint, action) {
            if (!currentSessionId) {
                showError('No session selected');
                return;
            }
            
            showLoading(`${action}...`);
            try {
                const url = `/sessions/${currentSessionId}${endpoint}`;
                const response = await fetch(url);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                showSuccess(action, data);
                
            } catch (error) {
                showError(`${action} failed: ${error.message}`);
                console.error(`${action} error:`, error);
            }
        }
        
        function viewRecentEvents() {
            makeSessionRequest('/events/recent', 'Recent Events (All)');
        }
        
        function viewUnprocessedEvents() {
            makeSessionRequest('/events/unprocessed', 'Unprocessed Events');
        }
        
        function viewProcessedEvents() {
            makeSessionRequest('/events/processed', 'Processed Events (All)');
        }
        
        function consumeEvents() {
            makeSessionRequest('/events/consume', 'Consume Events (FIFO)');
        }
        
        function viewActorCommands() {
            makeSessionRequest('/actor/commands', 'Pending Actor Commands');
        }
        
        function viewActorRetrieved() {
            makeSessionRequest('/actor/retrieved', 'Retrieved Actor Commands');
        }
        
        function viewActorSummary() {
            if (!currentSessionId) {
                showError('No session selected');
                return;
            }
            
            showLoading('Loading Actor command status...');
            
            // Fetch both pending and retrieved commands to create a summary
            Promise.all([
                fetch(`/sessions/${currentSessionId}/actor/commands`),
                fetch(`/sessions/${currentSessionId}/actor/retrieved`)
            ])
            .then(responses => {
                if (!responses[0].ok || !responses[1].ok) {
                    throw new Error('Failed to retrieve Actor command data');
                }
                return Promise.all(responses.map(r => r.json()));
            })
            .then(([pendingData, retrievedData]) => {
                // For pending commands, we get a direct array from our endpoint now
                const pendingCommands = Array.isArray(pendingData) ? pendingData : [];
                
                // For retrieved commands, we get an object with a commands property
                const retrievedCommands = retrievedData.commands || [];
                
                // Create a summary object
                const summary = {
                    pending: {
                        count: pendingCommands.length,
                        commands: pendingCommands.map(cmd => ({
                            id: cmd.id,
                            type: cmd.type,
                            timestamp: cmd.timestamp
                        }))
                    },
                    retrieved: {
                        count: retrievedCommands.length,
                        recentCommands: retrievedCommands.slice(-5).map(cmd => ({
                            id: cmd.id,
                            type: cmd.type,
                            timestamp: cmd.timestamp
                        }))
                    },
                    sessionId: currentSessionId,
                    status: pendingCommands.length > 0 ? 'Active' : 'Idle'
                };
                
                showSuccess('Actor Command Status Summary', summary);
            })
            .catch(error => {
                showError(`Failed to create Actor command summary: ${error.message}`);
                console.error('Actor summary error:', error);
            });
        }
        
        function viewSessionStatus() {
            makeSessionRequest('/status', 'Session Status');
        }
    </script>

</body>
</html>"""
    return HTMLResponse(content=html_content)


# ========================================================================
# CONFIGURATION MANAGEMENT ENDPOINTS
# ========================================================================

# Configuration authentication

def verify_localhost(request: Request):
    """Verify request is from localhost"""
    client_host = request.client.host
    if client_host not in ['127.0.0.1', '::1', 'localhost']:
        raise HTTPException(status_code=403, detail="Configuration access restricted to localhost")
    return True

def verify_config_auth(request: Request):
    """Verify configuration password via Basic Authentication"""
    import base64
    
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(
            status_code=401,
            detail="Configuration access requires authentication",
            headers={"WWW-Authenticate": "Basic realm=\"Configuration\""}
        )
    
    try:
        # Decode Basic auth credentials
        encoded_credentials = auth_header[6:]  # Remove "Basic " prefix
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        
        # Verify credentials
        auth_config = get_auth_config()
        if username != "admin" or password != auth_config.config_password:
            raise HTTPException(
                status_code=401,
                detail="Invalid configuration credentials",
                headers={"WWW-Authenticate": "Basic realm=\"Configuration\""}
            )
        
        return True
        
    except (ValueError, UnicodeDecodeError) as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication format",
            headers={"WWW-Authenticate": "Basic realm=\"Configuration\""}
        )


@app.get("/config", response_class=HTMLResponse)
async def config_page(request: Request):
    """Configuration management page (localhost only)"""
    # Verify access restrictions
    verify_localhost(request)
    verify_config_auth(request)
    
    config_manager = get_config_manager()
    current_config = config_manager.get_config()
    config_file_path = config_manager.get_config_file_path()
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔧 AIBE Server Configuration</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .config-section {{
            margin-bottom: 30px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .section-header {{
            background: #f7fafc;
            padding: 15px 20px;
            font-weight: bold;
            color: #2d3748;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .section-content {{
            padding: 20px;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #4a5568;
        }}
        
        .form-group input, .form-group select {{
            width: 100%;
            padding: 10px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
        }}
        
        .form-group input:focus, .form-group select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .checkbox-group {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .checkbox-group input[type="checkbox"] {{
            width: auto;
        }}
        
        .actions {{
            display: flex;
            gap: 15px;
            justify-content: center;
            padding: 30px;
            border-top: 1px solid #e2e8f0;
            background: #f7fafc;
        }}
        
        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #5a6fd8;
        }}
        
        .btn-secondary {{
            background: #e2e8f0;
            color: #4a5568;
        }}
        
        .btn-secondary:hover {{
            background: #cbd5e0;
        }}
        
        .file-info {{
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #0369a1;
        }}
        
        .error {{
            color: #e53e3e;
            margin-top: 5px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 AIBE Server Configuration</h1>
            <p>Manage your Browser-AI Interface Server settings</p>
        </div>
        
        <div class="content">
            <div class="file-info">
                <strong>Configuration File:</strong> {config_file_path}
            </div>
            
            <form id="configForm">
                <div class="config-section">
                    <div class="section-header">Database Settings</div>
                    <div class="section-content">
                        <div class="form-group">
                            <label for="db_connection">Connection String</label>
                            <input type="text" id="db_connection" name="database.connection_string" 
                                   value="{current_config.database.connection_string}" 
                                   placeholder="mongodb://localhost:27017/AIBE">
                        </div>
                        <div class="form-group">
                            <label for="db_name">Database Name</label>
                            <input type="text" id="db_name" name="database.database_name" 
                                   value="{current_config.database.database_name}" 
                                   placeholder="AIBE">
                        </div>
                        <div class="form-group">
                            <label for="db_collection">Collection Name</label>
                            <input type="text" id="db_collection" name="database.collection_name" 
                                   value="{current_config.database.collection_name}" 
                                   placeholder="Stories">
                        </div>
                        <div class="form-group">
                            <label for="db_timeout">Connection Timeout (seconds)</label>
                            <input type="number" id="db_timeout" name="database.connection_timeout" 
                                   value="{current_config.database.connection_timeout}" min="5" max="300">
                        </div>
                        <div class="form-group">
                            <label for="db_pool">Max Pool Size</label>
                            <input type="number" id="db_pool" name="database.max_pool_size" 
                                   value="{current_config.database.max_pool_size}" min="1" max="1000">
                        </div>
                    </div>
                </div>
                
                <div class="config-section">
                    <div class="section-header">Server Settings</div>
                    <div class="section-content">
                        <div class="form-group">
                            <label for="server_host">Host</label>
                            <input type="text" id="server_host" name="server.host" 
                                   value="{current_config.server.host}" 
                                   placeholder="localhost">
                        </div>
                        <div class="form-group checkbox-group">
                            <input type="checkbox" id="server_debug" name="server.debug" 
                                   {"checked" if current_config.server.debug else ""}>
                            <label for="server_debug">Debug Mode</label>
                        </div>
                        <div class="form-group">
                            <label for="server_log_level">Log Level</label>
                            <select id="server_log_level" name="server.log_level">
                                <option value="DEBUG" {"selected" if current_config.server.log_level == "DEBUG" else ""}>DEBUG</option>
                                <option value="INFO" {"selected" if current_config.server.log_level == "INFO" else ""}>INFO</option>
                                <option value="WARNING" {"selected" if current_config.server.log_level == "WARNING" else ""}>WARNING</option>
                                <option value="ERROR" {"selected" if current_config.server.log_level == "ERROR" else ""}>ERROR</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="config-section">
                    <div class="section-header">Test Streaming</div>
                    <div class="section-content">
                        <div class="form-group checkbox-group">
                            <input type="checkbox" id="streaming_enabled" name="test_streaming.enabled" 
                                   {"checked" if current_config.test_streaming.enabled else ""}>
                            <label for="streaming_enabled">Enable Test Streaming to MongoDB</label>
                        </div>
                        <div class="form-group">
                            <label for="streaming_database">Test Database</label>
                            <input type="text" id="streaming_database" name="test_streaming.database" 
                                   value="{current_config.test_streaming.database}" 
                                   placeholder="test_streams">
                        </div>
                        <div class="form-group">
                            <label for="streaming_prefix">Collection Prefix</label>
                            <input type="text" id="streaming_prefix" name="test_streaming.collection_prefix" 
                                   value="{current_config.test_streaming.collection_prefix}" 
                                   placeholder="test_">
                        </div>
                        <div class="form-group">
                            <label for="streaming_cleanup">Cleanup After (days)</label>
                            <input type="number" id="streaming_cleanup" name="test_streaming.cleanup_after_days" 
                                   value="{current_config.test_streaming.cleanup_after_days}" min="1" max="365">
                        </div>
                    </div>
                </div>
                
                <div class="config-section">
                    <div class="section-header">Server Streaming</div>
                    <div class="section-content">
                        <div class="form-group checkbox-group">
                            <input type="checkbox" id="server_streaming_enabled" name="server_streaming.enabled" 
                                   {"checked" if current_config.server_streaming.enabled else ""}>
                            <label for="server_streaming_enabled">Enable Server Streaming to MongoDB</label>
                        </div>
                        <div class="form-group">
                            <label for="server_streaming_database">Server Database</label>
                            <input type="text" id="server_streaming_database" name="server_streaming.database" 
                                   value="{current_config.server_streaming.database}" 
                                   placeholder="server_streams">
                        </div>
                        <div class="form-group">
                            <label for="server_streaming_prefix">Collection Prefix</label>
                            <input type="text" id="server_streaming_prefix" name="server_streaming.collection_prefix" 
                                   value="{current_config.server_streaming.collection_prefix}" 
                                   placeholder="server_">
                        </div>
                        <div class="form-group">
                            <label for="server_streaming_cleanup">Cleanup After (days)</label>
                            <input type="number" id="server_streaming_cleanup" name="server_streaming.cleanup_after_days" 
                                   value="{current_config.server_streaming.cleanup_after_days}" min="1" max="365">
                        </div>
                        <div class="form-group checkbox-group">
                            <input type="checkbox" id="stream_observer" name="server_streaming.stream_observer" 
                                   {"checked" if current_config.server_streaming.stream_observer else ""}>
                            <label for="stream_observer">Stream Observer Events (browser to server)</label>
                        </div>
                        <div class="form-group checkbox-group">
                            <input type="checkbox" id="stream_actor" name="server_streaming.stream_actor" 
                                   {"checked" if current_config.server_streaming.stream_actor else ""}>
                            <label for="stream_actor">Stream Actor Events (server to browser)</label>
                        </div>
                        <div class="form-group checkbox-group">
                            <input type="checkbox" id="stream_story" name="server_streaming.stream_story" 
                                   {"checked" if current_config.server_streaming.stream_story else ""}>
                            <label for="stream_story">Stream Story Assembly Events</label>
                        </div>
                        <div class="form-group checkbox-group">
                            <input type="checkbox" id="stream_log" name="server_streaming.stream_log" 
                                   {"checked" if current_config.server_streaming.stream_log else ""}>
                            <label for="stream_log">Stream Log Events</label>
                        </div>
                    </div>
                </div>
                
                <div class="config-section">
                    <div class="section-header">Authentication</div>
                    <div class="section-content">
                        <div class="form-group">
                            <label for="config_password">Configuration Password</label>
                            <input type="password" id="config_password" name="auth.config_password" 
                                   value="{current_config.auth.config_password}">
                        </div>
                    </div>
                </div>
            </form>
        </div>
        
        <div class="actions">
            <button type="button" class="btn btn-primary" onclick="saveConfig()">💾 Save Configuration</button>
            <button type="button" class="btn btn-secondary" onclick="cancelChanges()">❌ Cancel</button>
            <button type="button" class="btn btn-secondary" onclick="testConnection()">🔍 Test Connection</button>
        </div>
    </div>

    <script>
        let originalFormData = new FormData(document.getElementById('configForm'));
        
        function saveConfig() {{
            const formData = new FormData(document.getElementById('configForm'));
            const config = {{}};
            
            // Convert FormData to nested object
            for (const [key, value] of formData.entries()) {{
                const keys = key.split('.');
                let current = config;
                for (let i = 0; i < keys.length - 1; i++) {{
                    if (!current[keys[i]]) current[keys[i]] = {{}};
                    current = current[keys[i]];
                }}
                
                // Handle different data types
                const finalKey = keys[keys.length - 1];
                if (value === 'on') {{
                    current[finalKey] = true;
                }} else if (value === 'false' || value === '') {{
                    current[finalKey] = false;
                }} else if (!isNaN(value) && value !== '') {{
                    current[finalKey] = parseInt(value);
                }} else {{
                    current[finalKey] = value;
                }}
            }}
            
            // Handle unchecked checkboxes
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => {{
                if (!cb.checked) {{
                    const keys = cb.name.split('.');
                    let current = config;
                    for (let i = 0; i < keys.length - 1; i++) {{
                        if (!current[keys[i]]) current[keys[i]] = {{}};
                        current = current[keys[i]];
                    }}
                    current[keys[keys.length - 1]] = false;
                }}
            }});
            
            fetch('/api/config', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + btoa('admin:{current_config.auth.config_password}')
                }},
                body: JSON.stringify(config)
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    alert('Configuration saved successfully!');
                    originalFormData = new FormData(document.getElementById('configForm'));
                }} else {{
                    alert('Error saving configuration: ' + (data.error || 'Unknown error'));
                }}
            }})
            .catch(error => {{
                alert('Error saving configuration: ' + error.message);
            }});
        }}
        
        function cancelChanges() {{
            if (confirm('Are you sure you want to cancel all changes?')) {{
                location.reload();
            }}
        }}
        
        function testConnection() {{
            const connectionString = document.getElementById('db_connection').value;
            
            fetch('/api/config/validate', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + btoa('admin:{current_config.auth.config_password}')
                }},
                body: JSON.stringify({{ database: {{ connection_string: connectionString }} }})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.valid) {{
                    alert('Connection string is valid!');
                }} else {{
                    alert('Connection validation failed: ' + data.errors.join(', '));
                }}
            }})
            .catch(error => {{
                alert('Error testing connection: ' + error.message);
            }});
        }}
    </script>
</body>
</html>"""
    
    return HTMLResponse(content=html_content)

@app.get("/api/config")
async def get_config_api(request: Request):
    """Get current configuration (API)"""
    verify_localhost(request)
    verify_config_auth(request)
    
    try:
        config_manager = get_config_manager()
        config = config_manager.get_config()
        return {
            "success": True,
            "config": config.model_dump(),
            "config_file": config_manager.get_config_file_path()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

@app.post("/api/config")
async def update_config_api(request: Request):
    """Update configuration (API)"""
    verify_localhost(request)
    verify_config_auth(request)
    
    try:
        config_data = await request.json()
        config_manager = get_config_manager()
        
        # Validate configuration
        is_valid, errors = config_manager.validate_config(config_data)
        if not is_valid:
            return {"success": False, "errors": errors}
        
        # Create backup before updating
        config_manager.backup_config()
        
        # Update configuration
        new_config = config_manager.update_config(config_data)
        
        # Reload server streaming configuration if it was changed
        try:
            await reload_server_streamer()
            log("Server streaming configuration reloaded successfully")
        except Exception as reload_error:
            log_error(f"Error reloading server streaming configuration: {reload_error}")
            # Don't fail the config save if reload fails, just log the error
        
        return {
            "success": True,
            "message": "Configuration updated successfully",
            "config": new_config.model_dump()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/config/validate")
async def validate_config_api(request: Request):
    """Validate configuration without saving"""
    verify_localhost(request)
    verify_config_auth(request)
    
    try:
        config_data = await request.json()
        config_manager = get_config_manager()
        
        is_valid, errors = config_manager.validate_config(config_data)
        return {
            "valid": is_valid,
            "errors": errors
        }
    except Exception as e:
        return {"valid": False, "errors": [str(e)]}

# ========================================================================
# ROOT ENDPOINT - Server documentation
# ========================================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Server help page and documentation"""
    try:
        # Get server status for display
        status_response = await status(request)
        
        # Generate endpoint listing organized by categories (matching Node.js)
        endpoints_html = """
        <h3>📡 Observer Channel (Browser → Server)</h3>
        <div class="endpoint-line"><span class="method">POST</span> <code>/event</code> - Submit new browser event</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/sessions/:sessionId/events/recent</code> - Recent events for specific session</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/events/unbroadcast"><code>/events/unbroadcast</code></a> - Unbroadcast events (legacy)</div>
        <div class="endpoint-line"><span class="method">POST</span> <code>/events/clear</code> - Clear all stored events</div>

        <h3>🎯 Actor Channel (Server → Browser)</h3>
        <div class="endpoint-line"><span class="method">GET</span> <code>/actor/commands</code> - Poll for pending Actor commands</div>
        <div class="endpoint-line"><span class="method">POST</span> <code>/actor/send</code> - Queue new Actor command</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/actor/test"><code>/actor/test</code></a> - Test Actor channel functionality</div>

        <h3>📊 Server Status & Control</h3>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/status"><code>/status</code></a> - Server status and statistics</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/api/status"><code>/api/status</code></a> - Server status (API format)</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/"><code>/</code></a> - Server help page and documentation</div>

        <h3>🧪 Development & Testing</h3>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/test-inputs"><code>/test-inputs</code></a> - Input fields test page</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/test-controls"><code>/test-controls</code></a> - Comprehensive controls test page</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/test-runner"><code>/test-runner</code></a> - Web-based test runner interface</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/test-suites-config"><code>/test-suites-config</code></a> - Test suites configuration data</div>

        <h3>🔗 Session Management</h3>
        <div class="endpoint-line"><span class="method">PUT</span> <code>/sessions/init</code> - Initialize new session</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/sessions"><code>/sessions</code></a> - List all active sessions (JSON)</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/sessions/explorer"><code>/sessions/explorer</code></a> - Interactive session exploration</div>
        <div class="endpoint-line"><span class="method">POST</span> <code>/sessions/:sessionId/events</code> - Submit event to specific session</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/sessions/:sessionId/events/recent</code> - Recent events for session</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/sessions/:sessionId/events/consume</code> - Consume unprocessed events (FIFO)</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/sessions/:sessionId/events/unprocessed</code> - View unprocessed events</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/sessions/:sessionId/events/processed</code> - View processed events</div>
        <div class="endpoint-line"><span class="method">POST</span> <code>/sessions/:sessionId/actor/send</code> - Send Actor command to session</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/sessions/:sessionId/actor/commands</code> - Poll Actor commands for session</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/sessions/:sessionId/actor/retrieved</code> - View retrieved Actor commands</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/sessions/:sessionId/status</code> - Status for specific session</div>

        <h3>🔧 Configuration Management</h3>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/config"><code>/config</code></a> - Web-based configuration interface (localhost only, password protected)</div>
        <div class="endpoint-line"><span class="method">GET</span> <code>/api/config</code> - Get current configuration (API)</div>
        <div class="endpoint-line"><span class="method">POST</span> <code>/api/config</code> - Update configuration (API)</div>
        <div class="endpoint-line"><span class="method">POST</span> <code>/api/config/validate</code> - Validate configuration without saving</div>

        <h3>📄 Static Resources</h3>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/favicon.svg"><code>/favicon.svg</code></a> - Server favicon</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/TestingFramework.js"><code>/TestingFramework.js</code></a> - TestingFramework.js library</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/GenericElementTest.js"><code>/GenericElementTest.js</code></a> - GenericElementTest.js library</div>
        <div class="endpoint-line"><span class="method">GET</span> <a href="/DataDrivenTestRunner.js"><code>/DataDrivenTestRunner.js</code></a> - DataDrivenTestRunner.js library</div>
        """
        
        # Extract status information for display
        uptime = int(status_response.get("uptime", 0))
        event_count = status_response.get("eventCount", 0)
        pending_commands = status_response.get("pendingActorCommands", 0)
        mode = status_response.get("mode", "NORMAL")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Browser-AI Interface Server</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            max-width: 900px; 
            margin: 20px auto; 
            padding: 20px; 
            line-height: 1.4; 
        }}
        .status {{ 
            background-color: #e8f5e8; 
            padding: 15px; 
            border-radius: 5px; 
            margin-bottom: 25px; 
            border-left: 4px solid #4caf50;
        }}
        .endpoint-line {{ 
            padding: 4px 0; 
            font-family: monospace;
            font-size: 14px;
        }}
        .method {{ 
            font-weight: bold; 
            color: #007cba; 
            width: 50px;
            display: inline-block;
        }}
        code {{ 
            background-color: #f0f0f0; 
            padding: 2px 4px; 
            border-radius: 3px; 
        }}
        a {{ 
            color: #007cba; 
            text-decoration: none; 
        }}
        a:hover {{ 
            text-decoration: underline; 
        }}
        h3 {{
            color: #333;
            margin-top: 25px;
            margin-bottom: 10px;
        }}
        .quick-links {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #007cba;
        }}
    </style>
</head>
<body>
    <h1>🤖 Browser-AI Interface Server</h1>
    
    <div class="status">
        <strong>Status:</strong> Running ✅ | 
        <strong>Version:</strong> 0.9.0a1 | 
        <strong>Uptime:</strong> {uptime}s | 
        <strong>Events:</strong> {event_count} | 
        <strong>Pending Commands:</strong> {pending_commands} | 
        <strong>Mode:</strong> {mode} |
        <strong>Python Implementation:</strong> Full Node.js Parity
    </div>
    
    <div class="quick-links">
        <strong>🚀 Quick Links:</strong>
        <a href="/sessions/explorer">Sessions Explorer</a> | 
        <a href="/test-runner">Unified Test Runner</a>
    </div>

    <h2>📋 API Endpoints</h2>
{endpoints_html}
    
    <h2>💡 Quick Start</h2>
    <ul>
        <li>Install the Chrome extension</li>
        <li>Use <strong><a href="/sessions/explorer">Sessions Explorer</a></strong> to interact with browser sessions</li>
        <li>Use the <a href="/test-runner">unified test runner</a> for automated validation</li>
        <li>Monitor events via <a href="/sessions/explorer">Sessions Explorer</a> for session-specific data</li>
    </ul>

</body>
</html>"""
        
        return HTMLResponse(content=html_content)
        
    except Exception as error:
        log(f"Root endpoint error: {error}")
        # Fallback simple version if status fails
        simple_html = """
<!DOCTYPE html>
<html>
<head><title>Browser-AI Interface Server</title></head>
<body>
    <h1>🤖 Browser-AI Interface Server</h1>
    <p><strong>Status:</strong> Running (Python Implementation)</p>
    <p><a href="/status">View Status</a> | <a href="/sessions/explorer">Sessions Explorer</a> | <a href="/test-runner">Test Runner</a></p>
</body>
</html>"""
        return HTMLResponse(content=simple_html)


# ========================================================================
# MONGODB COLLECTIONS API  
# ========================================================================

@app.get("/api/collections")
async def list_collections():
    """List MongoDB collections for test streaming collection naming"""
    try:
        # Connect directly to MongoDB without creating unnecessary collections
        from motor.motor_asyncio import AsyncIOMotorClient
        
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client["test_streams"]
        
        # Get collection names from the database
        collections = await db.list_collection_names()
        
        client.close()
        
        return {"collections": collections}
        
    except Exception as error:
        log_error(f"Failed to list collections: {error}")
        return {"collections": [], "error": str(error)}


# ========================================================================
# APPLICATION LIFECYCLE
# ========================================================================

def run_server():
    """Run the server with uvicorn"""
    log(f"Starting server on port {PORT}")
    
    # Set up signal handlers now that we're ready to start the server
    setup_signal_handlers(process_manager)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=PORT,
        log_level="warning",  # Suppress uvicorn request logging
        access_log=False      # Disable access logging completely
    )


if __name__ == "__main__":
    run_server()
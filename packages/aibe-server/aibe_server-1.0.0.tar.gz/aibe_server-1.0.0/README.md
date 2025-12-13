# AIBE Server - AI Browser Extension Interface

**AI Browser Extension Interface Server** enables AI systems to observe and control web browsers through a standardized HTTP API. The system synchronizes your physical browser with a virtual browser, allowing AI to see exactly what you see and act exactly like a human user.

**Core Philosophy: "What the user can see and what they can do"** - The system captures only what's visible and interactive to humans, creating a natural interface for AI systems to understand and navigate web applications without complex DOM parsing or brittle selectors.

**Why use AIBE?** Instead of teaching AI systems to reverse-engineer web pages, AIBE lets them work with the same interface humans use. This makes AI browser automation more reliable, intuitive, and adaptable to any web application.

This is the server component that works with the AIBE Chrome extension to implement the Generic User Framework for AI-browser interaction.

*Learn more about the research and development behind this project at [AI & Me](https://paulhanchett.com).*

## Installation

### PyPI Installation (Recommended)

For most users, install from PyPI with a virtual environment:

```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install from PyPI
pip install aibe-server
```

**Why use a virtual environment?** Virtual environments isolate your project dependencies, preventing conflicts with other Python packages on your system. The `.venv` directory name is a Python standard that most editors and tools recognize automatically.

### Development Installation

For developers who want to modify the source code:

> **Note:** The source repository is private. For collaborator access, please contact paul@paulhanchett.com with details about your intended contribution.

```bash
# Clone the repository (requires access)
git clone <repository-url>
cd ai-browser-extension/server

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies and package in editable mode
pip install -e .
```

This installs the package in "editable mode" - changes to the source code take effect immediately without reinstalling.

## Quick Start

### 1. Start the Server

**If you installed from PyPI:**
```bash
# Make sure your virtual environment is activated
# Then start the server:
aibe-server start

# Check server status:
aibe-server status

# Stop server when done:
aibe-server stop
```

**If you're using the development installation:**
The server includes a unified management system with additional controls:

*Windows:*
```cmd
.\server.bat start     # Start server
.\server.bat stop      # Stop server  
.\server.bat restart   # Restart server
.\server.bat status    # Show server status
```

*Linux/WSL/macOS:*
```bash
./server start         # Start server
./server stop          # Stop server
./server restart       # Restart server  
./server status        # Show server status
```

**Management features (development install only):**
- Auto-detects and activates virtual environment
- Cross-platform process management
- Proper detached server processes
- Rich status reporting with platform detection
- Handles cross-space detection (Windows vs WSL)

The server will start on `http://localhost:3001`

## Command-Line Interface

The AIBE server provides a complete CLI for server management:

### Available Commands

```bash
aibe-server start     # Start server in background
aibe-server stop      # Stop the running server  
aibe-server restart   # Restart the server
aibe-server status    # Show server status and information
aibe-server help      # Show this help message
```

### Command Details

**Start Server:**
```bash
aibe-server start
```
Starts the server in background mode on port 3001. Shows PID, installation path, and connection URL when successful.

**Check Status:**
```bash
aibe-server status  
```
Displays comprehensive server information including:
- Server running status (running/not running)
- Installation path and PID
- Server uptime and platform
- Active sessions and event counts
- Available commands for current platform

**Stop Server:**
```bash
aibe-server stop
```
Gracefully shuts down the running server. Works across platforms (Windows/Linux/WSL) with proper process management.

**Restart Server:**
```bash
aibe-server restart
```
Stops the current server instance and starts a new one. Useful during development or after configuration changes.

**Get Help:**
```bash
aibe-server help
# or
aibe-server --help
# or  
aibe-server -h
```
Shows complete command reference with examples and usage information.

### 2. Install Chrome Extension

#### Option A: Download from Server (Recommended for PyPI installs)
1. Check server status to see installation location:
   ```bash
   aibe-server status
   ```
2. Visit `http://localhost:3001/extension/install` in your browser
3. Follow the installation guide to download all extension files
4. Load the extension in Chrome Developer Mode

#### Option B: Use Local Files (If you have the full repository)
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `server/extension` directory (containing `manifest.json`)
5. The extension should appear in your extensions list

The extension will automatically connect to the server on `localhost:3001`.

### 3. Verify Connection

Visit `http://localhost:3001/status` to see server status and connected sessions.

### 4. Run Tests (Optional)

The server includes comprehensive test suites to validate functionality:

**Web-based test runner:**
- Visit `http://localhost:3001/test-runner` in your browser
- Runs 48 automated tests covering all major functionality
- Interactive interface with real-time results

**Command-line test runner:**
```bash
# From server directory
node tests/console-runner.js
```

Both test runners validate:
- Event capture and processing
- Session management
- Form controls (inputs, dropdowns, checkboxes, radio buttons)
- Dynamic content handling
- Browser interaction capabilities

## Key Features

- **Observer Channel**: Captures user interactions and screen states
- **Actor Channel**: Foundation for AI systems to interact with the browser
- **Session Management**: Isolates browser tabs with unique session IDs
- **Event Processing**: Real-time event capture and queuing  
- **Testing Framework**: Built-in test suites for validation
- **Virtual Environment**: Isolated Python installation to avoid conflicts

## API Endpoints

### Status & Health
- `GET /status` - Server status and session information
- `GET /health` - Simple health check

### Event Capture (Observer)
- `POST /events` - Submit browser events
- `GET /events/{session_id}` - Get events for session
- `GET /events/{session_id}/latest` - Get latest events

### Browser Control (Actor)
- `POST /commands/{session_id}` - Send commands to browser
- `GET /commands/{session_id}` - Get pending commands
- `DELETE /commands/{session_id}/{command_id}` - Remove command

### Session Management
- `GET /sessions` - List all sessions
- `POST /sessions` - Create new session
- `GET /sessions/{session_id}` - Get session details

## Configuration

The server can be configured via environment variables:

```bash
AIBE_PORT=3001          # Server port (default: 3001)
AIBE_DEBUG=true         # Enable debug logging
AIBE_LOG_LEVEL=info     # Logging level
```

## Architecture

AIBE implements a dual-channel architecture:

1. **Observer Channel**: Browser → Server (events, screen state)
2. **Actor Channel**: Server → Browser (commands, actions)

This enables AI systems to both learn from human interactions and take autonomous actions.

## Generic User Framework

AIBE is designed to support the Generic User Framework (GUA), where:

- **Task Domain AI**: Focuses on business logic and goals
- **Browser Interaction AI**: Handles web navigation mechanics
- **AIBE Server**: Provides the technical bridge between AI and browser

## Testing

The server includes comprehensive test suites:

```bash
# Run validation tests
python validate_core.py

# Start test runner web interface
# Visit http://localhost:3001/test-runner
```

## Development

### Project Structure

```
server/
├── aibe_server/          # Main package
│   ├── main.py          # FastAPI application
│   ├── session_manager.py
│   ├── models/          # Pydantic models
│   ├── middleware/      # Custom middleware
│   ├── utils/           # Utilities
│   ├── static/          # Web assets
│   └── templates/       # HTML templates
├── server.py            # Entry point
├── install.py           # Automatic installer
├── pyproject.toml       # Package configuration
└── requirements.txt     # Dependencies
```

### Running from Source

```bash
# Using the installer (recommended)
python install.py

# Or manually
pip install -r requirements.txt
python server.py
```

## Virtual Environment Benefits

The automatic installation creates an isolated Python environment that:

- Prevents conflicts with system Python packages
- Works on systems where users can't install global packages
- Ensures consistent dependency versions
- Makes uninstallation clean (just delete `~/.aibe-server/`)

## Research Context

AIBE is part of ongoing research into:

- **Persistent Cognitive Architectures** for AI systems
- **Human-AI Collaboration** patterns and methodologies  
- **Generic User Framework** for universal web interaction
- **Memory Agent** concepts for continuous learning

## License

MIT License - See LICENSE file for details.

## Support

- **Documentation**: https://paulhanchett.com/aibe/manual
- **Research Papers**: https://paulhanchett.com/research

## Citation

If you use AIBE in research, please cite:

```bibtex
@software{hanchett2025aibe,
  title={AI Browser Extension Interface: Enabling AI Systems to Navigate Web Interfaces},
  author={Hanchett, Paul},
  year={2025},
  url={https://paulhanchett.com/aibe}
}
```
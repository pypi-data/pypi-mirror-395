const aiHostName = 'com.browser.ai.interface';
const nativeHostName = aiHostName; // Use the AI host name for consistency
const recentEvents = [];
const MAX_EVENTS = 50;


// Function to log messages
function log(message) {
    //
    // --> We're not going to be allowed to write to a file from here.
    //     The suggestion is to send log messages to the native host
    //     and have it write to a file. AT the moment, that isn't working
    //     in the way it should. So we'll just write to the console.
    //
    const timestamp = Date.now();
    console.log(message);
}

// Create a simple in-memory event store
class EventStore {
    constructor() {
        this.events = [];
    }

    addEvent(event) {
        this.events.unshift(event);
        if (this.events.length > MAX_EVENTS) {
            this.events.pop();
        }
    }

    getRecentEvents(limit = 50) {
        return this.events.slice(0, limit);
    }

    clearEvents() {
        this.events = [];
    }

    getStatus() {
        return {
            version: chrome.runtime.getManifest().version,
            uptime: performance.now() / 1000, // Convert to seconds
            eventCount: this.events.length
        };
    }
}

const eventStore = new EventStore();

// Map to track persistent tab IDs by Chrome tabId
let tabIdMap = {};

// Listen for tab close events
chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
    // Check if we have a persistent tab ID for this tab
    const persistentTabId = tabIdMap[tabId];
    if (persistentTabId) {
        log(`Tab closed: ${tabId}, sending cleanup for persistent ID: ${persistentTabId}`);
        
        // Send close notification to server
        fetch('http://localhost:3001/sessions/close', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-tab-id': persistentTabId
            },
            // Use keepalive to ensure the request completes during browser shutdown
            keepalive: true
        }).catch(error => {
            // Silent fail - tab is already closing
            log(`Error sending tab close notification: ${error}`);
        });
        
        // Clean up the mapping
        delete tabIdMap[tabId];
    }
});

// Handle messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // Register tab ID mapping from content script
    if (message.type === 'registerTabId' && sender.tab && message.tabId) {
        tabIdMap[sender.tab.id] = message.tabId;
        log(`Registered tab mapping: ${sender.tab.id} -> ${message.tabId}`);
        sendResponse({success: true});
    }
});

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'EVENT') {
        eventStore.addEvent(message.data);
        sendResponse({success: true});
    } else if (message.type === 'GET_RECENT_EVENTS') {
        sendResponse(eventStore.getRecentEvents(message.limit));
    } else if (message.type === 'GET_STATUS') {
        sendResponse(eventStore.getStatus());
    } else if (message.type === 'CLEAR_EVENTS') {
        eventStore.clearEvents();
        sendResponse({success: true});
    }
    return true; // Keep the message channel open for async responses
});

// Flag to track if server is running
let serverIsEnabled = false;

//
// Returns port object of running Native Host. If host is not running, starts it.
//
// Native host connection
let _nativePort = null;
let _connectionInProgress = false;

function getNativePort() {
    if (_nativePort) {
        return _nativePort;
    } else {
        try {
            // Connect to native messaging host
            console.log(`Attempting to connect to native host: ${nativeHostName}`);
            _nativePort = chrome.runtime.connectNative(nativeHostName);

            // Validate connection was successful
            if (!_nativePort) {
                console.error('Failed to create native port connection');
                return null;
            }

            // Handle disconnection events
            _nativePort.onDisconnect.addListener(() => {
            // Clear connection flag when disconnected
            _connectionInProgress = false;
            // Check for lastError when disconnected
            if (chrome.runtime.lastError) {
                // Log as a warning instead of an error to reduce alarm
                console.warn('getNativePort: Native host disconnected with message:', chrome.runtime.lastError.message);
                // todo: "Error when communicating with the native messaging host"

                // Don't attempt to reconnect immediately if this was due to an extension disable/enable cycle
                // The onEnabled handler will take care of reconnecting with appropriate delay
                const isExtensionCycleError =
                    chrome.runtime.lastError.message.includes('host not found') ||
                    chrome.runtime.lastError.message.includes('disconnected');

                if (isExtensionCycleError) {
                    console.log('getNativePort: Disconnection appears to be part of extension cycle, not attempting immediate reconnect');
                    disconnectNativePort();
                    serverIsEnabled = false;
                    return;
                }
            } else {
                console.log('getNativePort: Disconnected from native host');
            }

            // Housekeeping, server is down!
            disconnectNativePort();
            serverIsEnabled = false;
        });

        } catch (error) {
            console.error('Error connecting to native host:', error);
            _nativePort = null;
            _connectionInProgress = false;  // Clear connection flag
            serverIsEnabled = false;
            return null;
        }
    }
    return _nativePort;
}

function disconnectNativePort() {
    if (_nativePort) {
        _nativePort.disconnect();
        _nativePort = null;
        _connectionInProgress = false;  // Clear connection flag
    }
}

function enableServer() {
    if (serverIsEnabled) {
        console.log('enableServer: Server is already ENABLED');
    } else {
        console.log('enableServer: Server is DISABLED, sending START message');
        try {
            getNativePort().postMessage({ type: 'START' });

            // Send a test message to verify communication
            setTimeout(() => {
                if (getNativePort()) {
                    console.log('enableServer: Sending TEST message to native host');
                    getNativePort().postMessage({ type: 'TEST', message: 'Hello from extension' });
                }
            }, 1000); // Wait 1 second from START before sending test message
        } catch (error) {
            console.error('enableServer: Error sending message(s) to native host:', error);
            // Reset connection if we can't communicate with the native host
            _nativePort = null;
            _connectionInProgress = false;  // Clear connection flag
            serverIsEnabled = false;
            // Try to reconnect after a delay
            setTimeout(() => {
                console.log('enableServer: Retrying to connect to native host & enable server...');
                getNativePort();
                enableServer();
            }, 2000);
        }
    }
    return serverIsEnabled;
}

// Function to connect to native host
function connectToNativeHost() {
    // Prevent multiple simultaneous connection attempts
    if (_connectionInProgress) {
        console.log('connectToNativeHost: Connection already in progress, skipping...');
        return;
    }
    if (_nativePort) {
        console.log('connectToNativeHost: Already connected to native host, skipping...');
        return;
    }
    
    _connectionInProgress = true;
    console.log('connectToNativeHost: Attempting to connect to native host...');
    
    try {
        getNativePort();
        console.log('connectToNativeHost: Successfully connected to native host');

        getNativePort().onMessage.addListener((message) => {
            console.log('connectToNativeHost: Received message from native host:', message);
            if (message.type === 'SERVER_STARTED') {
                console.log('connectToNativeHost: Server ENABLED on port:', message.port);
                serverIsEnabled = true;
            } else if (message.type === 'SERVER_STOPPED') {
                console.log('connectToNativeHost: Server is DISABLED');
                serverIsEnabled = false;
            } else if (message.type === 'ECHO') {
                console.log('connectToNativeHost: Received echo from native host:', message.original);
            }
        });

        console.log('connectToNativeHost: Start the server...');
        enableServer();
        
        _connectionInProgress = false;  // Clear flag on success
    } catch (error) {
        console.error('connectToNativeHost: Error during connection:', error);
        _connectionInProgress = false;  // Clear flag on error
        throw error;
    }
}

// Function to disconnect from native host
function disconnectFromNativeHost(keepConnection = false) {
    if (getNativePort()) {
        try {
            // Send STOP message to stop the server
            console.log('disconnectFromNativeHost: Sending DISABLE message to native host');
            // getNativePort().postMessage({type: 'STOP'});
            getNativePort().disconnect();
            serverIsEnabled = false;

        } catch (error) {
            console.warn('disconnectFromNativeHost: Error during disconnection from native host:', error);
        }
    }
}

// Initialize when extension is installed
chrome.runtime.onInstalled.addListener(() => {
    console.log('chrome.management.onEnabled.addListener: Browser-AI Interface onInstalled event triggered');
    // TEMPORARILY DISABLED: connectToNativeHost() - Python server already running
    // connectToNativeHost();
});

// Handle extension enable/disable
chrome.management.onEnabled.addListener((extension) => {
    console.log('chrome.management.onEnabled.addListener: Browser-AI Interface onEnabled event triggered');
    console.log('chrome.management.onEnabled.addListener: Launching connectToNativeHost()');
    // TEMPORARILY DISABLED: connectToNativeHost() - Python server already running
    // connectToNativeHost();
});

console.log("bottom of file");

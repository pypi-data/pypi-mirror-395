/**
 * Content Script - Main Entry Point
 * 
 * AI Browser Extension - Content Script
 * 
 * This is the main entry point for the browser extension content script.
 * It imports and initializes all modular components.
 */

// Import all modules
import './modules/config.js';
import { CURRENT_TAB_SESSIONID, initializeSessionManager } from './modules/session-manager.js';
import { log } from './modules/utils.js';
import { initializeEventListeners } from './modules/events.js';
import { initializeActorChannel } from './modules/actor.js';
import { getCurrentScreen } from './modules/screen-capture.js';
import { sendEvent } from './modules/events.js';

//=================================================================================
// INITIALIZATION
//=================================================================================

// Handle uncaught exceptions
window.addEventListener('error', (event) => {
    log(`window.addEventListener.error: === UNCAUGHT EXCEPTION ===\n\t${event.error.message}\n${event.error.stack}`);
});

/**
 * Initialize all extension components in correct order
 */
async function initializeExtension() {
    try {
        console.log('AI Browser Extension: Initializing...');

        // 1. Initialize session manager (tab ID, heartbeat, settings)
        initializeSessionManager();
        console.log('✓ Session manager initialized');

        // 2. Initialize event listeners (Observer channel)
        initializeEventListeners();
        console.log('✓ Event listeners initialized');

        // 3. Initialize Actor channel (command polling)
        initializeActorChannel();
        console.log('✓ Actor channel initialized');

        // 4. Send initial screen status
        const initialScreen = getCurrentScreen();
        sendEvent('screen_status', initialScreen);
        console.log('✓ Initial screen status sent');

        console.log(`AI Browser Extension: Initialized successfully for tab ${CURRENT_TAB_SESSIONID}`);

    } catch (error) {
        console.error('AI Browser Extension: Initialization failed:', error);
        log(`Extension initialization error: ${error.message}\n${error.stack}`);
    }
}

// Start initialization when script loads
initializeExtension();

// Debug: Verify extension loaded
log('CONTENT SCRIPT VERSION 2025-11-26-MODULAR LOADED');
console.log('🚀 AI Browser Extension: Content script loaded (modular version)');

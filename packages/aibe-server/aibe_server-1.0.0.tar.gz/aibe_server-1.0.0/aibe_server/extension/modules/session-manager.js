/**
 * Session Manager Module
 * Handles tab session ID generation, heartbeat, and settings management
 */

import { EXTENSION_CONFIG, CONFIG } from './config.js';

// Tab Session ID using sessionStorage for proper tab isolation - enhanced for persistence
export let CURRENT_TAB_SESSIONID = sessionStorage.getItem('tabSessionId');
if (!CURRENT_TAB_SESSIONID) {
    CURRENT_TAB_SESSIONID = 'tab_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    sessionStorage.setItem('tabSessionId', CURRENT_TAB_SESSIONID);
    console.log('Generated new tab ID:', CURRENT_TAB_SESSIONID);
} else {
    console.log('Using existing tab ID:', CURRENT_TAB_SESSIONID);
}

/**
 * Register the tab ID with the background script for tab close handling
 */
export function registerTabIdWithBackground() {
    chrome.runtime.sendMessage({
        type: 'registerTabId',
        tabId: CURRENT_TAB_SESSIONID
    }, (response) => {
        if (response && response.success) {
            console.log('Tab ID registered with background script');
        }
    });
}

/**
 * Send heartbeats to keep the session alive
 */
export function startHeartbeat() {
    const HEARTBEAT_INTERVAL = 60000; // 60 seconds

    setInterval(() => {
        // Only send heartbeats when tab is visible
        if (document.visibilityState === 'visible') {
            console.log('Sending heartbeat for tab:', CURRENT_TAB_SESSIONID);

            fetch(`${CONFIG.serverUrl}/sessions/${CURRENT_TAB_SESSIONID}/heartbeat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-tab-id': CURRENT_TAB_SESSIONID
                }
            }).catch(err => {
                console.log('Heartbeat failed:', err);
            });
        }
    }, HEARTBEAT_INTERVAL);
}

/**
 * Load settings from storage
 */
export async function loadExtensionSettings() {
    try {
        const result = await chrome.storage.local.get(['showPasswordValues']);
        EXTENSION_CONFIG.showPasswordValues = result.showPasswordValues || false;
    } catch (error) {
        console.error('Error loading extension settings:', error);
    }
}

/**
 * Initialize session management
 */
export function initializeSessionManager() {
    // Register tab ID immediately
    registerTabIdWithBackground();

    // Start heartbeat when page is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startHeartbeat);
    } else {
        startHeartbeat();
    }

    // Listen for setting changes from popup
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === 'settingChanged' && message.setting === 'showPasswordValues') {
            EXTENSION_CONFIG.showPasswordValues = message.value;
            console.log('Password visibility setting changed:', message.value);
        }
    });

    // Load settings on startup
    loadExtensionSettings();
}

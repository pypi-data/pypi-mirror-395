/**
 * Events Module
 * Event capture, handlers, queuing, and transmission
 */

import { EXTENSION_CONFIG, CONFIG, STABLE_SCREEN_DELAY } from './config.js';
import { CURRENT_TAB_SESSIONID } from './session-manager.js';
import { extractBestLabel, getEventModifiers, isInteractiveElement, log } from './utils.js';
import { returnElementProperties, getCurrentScreen, updatePreviousScreen } from './screen-capture.js';

// Event queue system for race-safe sending and centralized change detection
let eventQueue = [];
let sendingInProgress = false;
let changeDetectionTimer = null;

// Keyboard accumulation system
let inProcessKeyboard = null;

/**
 * Flush pending keyboard events
 */
export function flushPendingKeyboard() {
    if (inProcessKeyboard) {
        // Capture final text value at flush time for accuracy using stored targetId
        const targetElement = document.getElementById(inProcessKeyboard.targetId) ||
            document.querySelector(`[id="${inProcessKeyboard.targetId}"]`) ||
            document.activeElement; // Fallback to active element

        if (targetElement) {
            let finalValue = targetElement.value || '';

            // Handle password masking - omit value entirely when masking enabled
            if (targetElement.type === 'password' && !EXTENSION_CONFIG.showPasswordValues) {
                // Don't include value field at all for masked passwords
                // (value property will be undefined/missing)
            } else {
                // Update unified dictionary format: display_name -> actual_value per Event-Refactoring.json
                inProcessKeyboard.target.value = { text: finalValue }; // Simplified to text field only
            }
        }

        // Remove targetId before sending (internal use only)
        const eventToSend = { ...inProcessKeyboard };
        delete eventToSend.targetId;

        sendEvent('keyboard', eventToSend);
        inProcessKeyboard = null;
    }
}

/**
 * Main function to send event to server
 */
export async function sendEvent(kind, data) {
    // Build event with standardized field ordering per Event-Refactoring.json
    //Order: primary fields → target → metadata (timestamp, source)
    const orderedEvent = {
        type: kind,
        // Primary event details first
        ...(data.event && { event: data.event }),
        ...(data.url && { url: data.url }),
        ...(data.button !== undefined && { button: data.button }),
        ...(data.buttons !== undefined && { buttons: data.buttons }),
        ...(data.key && { key: data.key }),
        ...(data.code && { code: data.code }),
        ...(data.x !== undefined && { x: data.x }),
        ...(data.y !== undefined && { y: data.y }),

        // All other data fields (including target, visible_elements, etc.)
        ...Object.fromEntries(
            Object.entries(data).filter(([key]) =>
                !['event', 'url', 'button', 'buttons', 'key', 'code', 'x', 'y'].includes(key)
            )
        ),
    };

    if (window.actorExecuting) {
        orderedEvent.source = 'actor';
        window.actorExecuting = false;  // Reset actor flag after event attribution.
    }

    // Queue the ordered event
    eventQueue.push(orderedEvent);

    // Schedule screen change detection for all events EXCEPT screen_status
    if (kind !== 'screen_status') {
        scheduleChangeDetection();
    }

    // Process the queue
    processSendQueue();
}

/**
 * Schedule delayed screen change detection (cancels previous if pending)
 */
export function scheduleChangeDetection() {
    if (changeDetectionTimer) {
        clearTimeout(changeDetectionTimer);
    }
    changeDetectionTimer = setTimeout(() => {
        // Flush any pending keyboard input before capturing screen state
        flushPendingKeyboard();

        const screen = getCurrentScreen();
        sendEvent('screen_status', screen);
        updatePreviousScreen(screen);
        changeDetectionTimer = null;
    }, STABLE_SCREEN_DELAY);
}

/**
 * Process the event queue serially to prevent race conditions
 */
function processSendQueue() {
    if (sendingInProgress || eventQueue.length === 0) {
        return; // Already sending or nothing to send
    }

    sendingInProgress = true;

    while (eventQueue.length > 0) {
        const event = eventQueue.shift(); // Atomic pop from front
        actuallySendEvent(event);
    }

    sendingInProgress = false;
}

/**
 * Helper function to clean event data for sending (remove internal fields)
 */
function cleanEventForSending(event_) {
    // Deep clone the event and remove node fields and position bloat recursively
    const cleanEvent = JSON.parse(JSON.stringify(event_, (key, value) => {
        // Filter out node fields and other internal properties
        if (key === 'node') {
            return undefined;
        }
        // Remove position bloat from visible_elements per Event-Refactoring.json
        if (['top', 'left', 'bottom', 'right'].includes(key)) {
            return undefined;
        }
        return value;
    }));

    // Additional cleanup for visible_elements arrays
    if (cleanEvent.visible_elements && Array.isArray(cleanEvent.visible_elements)) {
        cleanEvent.visible_elements = cleanEvent.visible_elements.map(element => {
            const cleanElement = { ...element };
            // Remove position coordinates - Observer doesn't need precise positioning
            delete cleanElement.top;
            delete cleanElement.left;
            delete cleanElement.bottom;
            delete cleanElement.right;

            // Remove redundant destination_hint if identical to href
            if (cleanElement.destination_hint === cleanElement.href) {
                delete cleanElement.destination_hint;
            }

            // Remove tagName when control_type supersedes it (except for UNKNOWN)
            if (cleanElement.control_type && cleanElement.control_type !== 'UNKNOWN') {
                delete cleanElement.tagName;
            }

            // Handle showPasswordValues properly - only include for password controls per Event-Refactoring.json
            if (cleanElement.control_type === 'INPUT_PASSWORD') {
                cleanElement.showPasswordValues = EXTENSION_CONFIG.showPasswordValues;
            } else {
                delete cleanElement.showPasswordValues;
            }

            return cleanElement;
        });
    }

    return cleanEvent;
}

/**
 * The actual HTTP sending logic (extracted from original sendEvent)
 */
async function actuallySendEvent(event_) {
    // Clean the event data before sending
    const cleanEvent = cleanEventForSending(event_);

    // Try to send to server first
    try {
        console.log(`actuallySendEvent session:${CURRENT_TAB_SESSIONID} event:${event_.type} data:${JSON.stringify(cleanEvent)}`);
        const response = await fetch(`${CONFIG.serverUrl}/sessions/${CURRENT_TAB_SESSIONID}/events`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Tab-ID': CURRENT_TAB_SESSIONID
            },
            body: JSON.stringify(cleanEvent)
        });

        if (!response.ok) {
            throw new Error(`sendEvent: Server responded with status: ${response.status}`);
        }
    } catch (error) {
        log(`sendEvent: Failed to send event ${event_.type} to server, trying fallback: ${error.message} \n ${error.stack}`);
    }
}

/**
 * Build structured target for dropdown (SELECT) elements
 */
function buildDropdownTarget(node, event, target, context) {
    const selectedOptions = Array.from(node.selectedOptions);

    // Build unified dictionary: display_name -> actual_value
    const valueDict = {};
    selectedOptions.forEach(option => {
        valueDict[option.text] = option.value;
    });

    const result = {
        label: node.labels?.[0]?.textContent?.trim() ||
            extractBestLabel(target.label) ||
            node.name ||
            node.getAttribute('aria-label') ||
            `select#${node.id || 'unlabeled'}`,
        value: valueDict,
        event_state: {
            modifiers: getEventModifiers(event)
        }
    };

    if (context === 'mouse') {
        const clickedOption = event.target.tagName === 'OPTION' ? event.target.text : null;
        result.event_state.clicked_option = clickedOption;
    }

    return result;
}

/**
 * Build structured target for radio button elements
 */
function buildRadioTarget(node, event, target) {
    const radioLabel = node.labels?.[0]?.textContent?.trim() ||
        extractBestLabel(target.label) ||
        node.value ||
        `radio[${node.name || 'unnamed'}]`;

    // Build unified dictionary: display_name -> actual_value
    const valueDict = {};
    valueDict[radioLabel] = node.value;

    return {
        label: radioLabel,
        value: valueDict,
        event_state: {
            modifiers: getEventModifiers(event)
        }
    };
}

/**
 * Build structured target for checkbox elements
 */
function buildCheckboxTarget(node, event) {
    const checkboxLabel = node.labels?.[0]?.textContent?.trim() ||
        node.name ||
        node.getAttribute('aria-label') ||
        `checkbox#${node.id || 'unlabeled'}`;

    // Build unified dictionary: display_name -> actual_value
    const valueDict = {};
    valueDict[checkboxLabel] = node.checked;

    return {
        label: checkboxLabel,
        value: valueDict,
        event_state: {
            modifiers: getEventModifiers(event)
        }
    };
}

/**
 * Build structured target for text input and textarea elements
 */
function buildTextInputTarget(node, event, target) {
    const inputLabel = node.labels?.[0]?.textContent?.trim() ||
        extractBestLabel(target.label) ||
        node.placeholder ||
        node.name ||
        node.getAttribute('aria-label') ||
        `${node.type || 'input'}#${node.id || 'unlabeled'}`;

    // Handle password masking - omit value entirely when masking enabled
    let fieldValue = node.value || '';
    const valueDict = {};

    if (node.type === 'password' && !EXTENSION_CONFIG.showPasswordValues) {
        // Don't include value at all for masked passwords
        // (valueDict remains empty)
    } else {
        // Use standardized text field format per Event-Refactoring.json
        valueDict.text = fieldValue;
    }

    return {
        label: inputLabel,
        value: valueDict,
        event_state: {
            modifiers: getEventModifiers(event)
        }
    };
}

/**
 * Build structured target for option elements (fallback)
 */
function buildOptionTarget(node, event) {
    const selectElement = node.closest('select');
    const selectLabel = selectElement?.labels?.[0]?.textContent?.trim() || 'Dropdown';

    // Build unified dictionary: display_name -> actual_value
    const valueDict = {};
    valueDict[node.text] = node.value;

    return {
        label: selectLabel,
        value: valueDict,
        event_state: {
            modifiers: getEventModifiers(event)
        }
    };
}

/**
 * Unified function to build structured targets for any control type
 */
function buildStructuredTarget(node, event, target, context) {
    try {
        // Dropdowns (SELECT elements)
        if (node.tagName === 'SELECT' && node.selectedOptions.length > 0) {
            return buildDropdownTarget(node, event, target, context);
        }

        // Radio buttons
        if (node.type === 'radio' && node.name) {
            return buildRadioTarget(node, event, target);
        }

        // Checkboxes
        if (node.type === 'checkbox') {
            return buildCheckboxTarget(node, event);
        }

        // Text inputs and textareas
        if (node.tagName === 'INPUT' || node.tagName === 'TEXTAREA') {
            return buildTextInputTarget(node, event, target);
        }

        // Option elements (fallback)
        if (node.tagName === 'OPTION') {
            return buildOptionTarget(node, event);
        }

        // Anchor / link elements: treat href as the value of the control
        if (node.tagName === 'A' || node.href) {
            const linkLabel = target.label ||
                node.textContent?.trim() ||
                node.getAttribute('aria-label') ||
                node.title ||
                node.href ||
                'link';

            const valueDict = {};
            if (node.href) {
                valueDict[linkLabel] = node.href;
            }

            return {
                label: linkLabel,
                value: valueDict,
                event_state: {
                    modifiers: getEventModifiers(event)
                }
            };
        }

        // Unknown control safety net - generate basic event for any unrecognized interactive element
        if (node.tagName && (node.onclick || node.href || node.type || isInteractiveElement(node))) {
            log(`Unknown control type detected: ${node.tagName}[type="${node.type}"] - generating basic event`);
            return {
                label: target.label || node.textContent?.trim() || node.tagName || 'Unknown Control',
                control_type: 'UNKNOWN',
                tagName: node.tagName, // Keep tagName for unknown controls to help with debugging
                ...(node.type && { type: node.type }),
                ...(node.href && { href: node.href }),
                value: {} // Empty value object for unknown controls
            };
        }

        return null; // No structured target for this element type
    } catch (error) {
        // Safety net for any errors in target building
        log(`Error building structured target for ${node?.tagName}: ${error.message}`);
        return {
            label: 'Error Building Target',
            control_type: 'UNKNOWN',
            error: error.message,
            value: {}
        };
    }
}

/**
 * Helper function to create fallback target structure when buildStructuredTarget fails
 */
function createFallbackTarget(target, event) {
    // Always return a minimal, human-facing target: label (+ empty value dict)
    if (target?.label) {
        const labelText = extractBestLabel(target.label) ||
            target.label ||
            event?.target?.textContent?.trim() ||
            event?.target?.placeholder ||
            event?.target?.getAttribute('aria-label') ||
            `${event?.target?.tagName?.toLowerCase() || 'element'}[${event?.target?.type || 'unknown'}]`;

        return {
            label: labelText,
            value: {}
        };
    }

    // If target is null/undefined, create basic fallback from event only
    if (!target && event?.target) {
        return {
            label: event.target.textContent?.trim().substring(0, 50) ||
                event.target.placeholder ||
                `${event.target.tagName?.toLowerCase() || 'element'}#${event.target.id || 'unlabeled'}`,
            value: {}
        };
    }

    // Last resort: derive something minimal from whatever we were given
    if (target && typeof target === 'object') {
        const labelText = target.label ||
            event?.target?.textContent?.trim() ||
            `${event?.target?.tagName?.toLowerCase() || 'element'}[${event?.target?.type || 'unknown'}]`;
        return {
            label: labelText,
            value: {}
        };
    }

    return {
        label: 'unknown',
        value: {}
    };
}

/**
 * Helper function to get keyboard event properties
 */
function returnKeyboardEventProperties(event) {
    const target = returnElementProperties(event.target);

    // Build structured target using shared function
    let structuredTarget = null;

    if (event.target) {
        const node = event.target;

        // Check if this is a control key interaction we want to capture
        const isControlKeyInteraction =
            (node.tagName === 'SELECT' && (event.key === 'Enter' || event.key === ' ')) ||
            (node.type === 'radio' && (event.key.startsWith('Arrow') || event.key === ' ')) ||
            (node.type === 'checkbox' && event.key === ' ') ||
            (node.tagName === 'INPUT' || node.tagName === 'TEXTAREA');

        if (isControlKeyInteraction) {
            structuredTarget = buildStructuredTarget(node, event, target, 'keyboard');

            // Log when we fall back to generic label due to poor labeling
            if (structuredTarget && !target.label && node.id) {
                sendEvent('log', {
                    message: `Using generic label for ${node.tagName.toLowerCase()} (keyboard) - poor UI labeling detected`,
                    element_id: node.id,
                    element_tag: node.tagName,
                    element_type: node.type,
                    key_pressed: event.key,
                    page_url: window.location.href
                });
            }
        }
    }

    // Normalize target to minimal { label, value } structure
    let minimalTarget = null;
    if (structuredTarget) {
        const labelText = structuredTarget.label ||
            (target && extractBestLabel(target.label)) ||
            event.target?.textContent?.trim() ||
            event.target?.placeholder ||
            `${event.target?.tagName?.toLowerCase() || 'element'}[${event.target?.type || 'unknown'}]`;

        const valueDict = structuredTarget.value &&
            typeof structuredTarget.value === 'object'
            ? structuredTarget.value
            : {};

        minimalTarget = {
            label: labelText,
            value: valueDict
        };
    }

    return {
        tagName: event.tagName,
        target: minimalTarget || createFallbackTarget(target, event),
        key: event.key,
        code: event.code,
    };
}

/**
 * Resolve the actual target element for mouse events
 */
function resolveEventTarget(event) {
    let targetElement = event.target;

    // Handle OPTION -> SELECT mapping
    if (event.target && event.target.tagName === 'OPTION') {
        targetElement = event.target.closest('select');
    }

    return targetElement;
}

/**
 * Find matching element in current screen data
 */
function findMatchingScreenElement(targetElement) {
    const currentScreen = getCurrentScreen();
    return currentScreen.visible_elements.find(element =>
        element.node === targetElement
    ) || null;
}

/**
 * Build mouse event properties for matching screen elements
 */
function buildMatchingEventProperties(event, matchingElement, targetElement) {
    log(`Mouse click: Found matching element with label \"${matchingElement.label}\" for ${targetElement.tagName}[id=\"${targetElement.id}\"]`);

    // Build structured target to capture final value/state where applicable (checkbox, radio, select, link, etc.)
    const structuredTarget = buildStructuredTarget(targetElement, event, { label: matchingElement.label }, 'mouse');

    const labelText = (structuredTarget && structuredTarget.label) ||
        matchingElement.label ||
        targetElement.textContent?.trim() ||
        targetElement.getAttribute('aria-label') ||
        targetElement.placeholder ||
        targetElement.tagName ||
        'Unknown Control';

    const valueDict = structuredTarget && structuredTarget.value && typeof structuredTarget.value === 'object'
        ? structuredTarget.value
        : {};

    const target = {
        label: labelText,
        value: valueDict
    };

    return {
        event: event.type,
        target,
        button: event.button || 0,
        buttons: event.buttons || 0,
    };
}

/**
 * Build fallback mouse event properties for non-matching elements
 */
function buildFallbackEventProperties(event, targetElement) {
    log(`Mouse click: No matching element found for ${targetElement.tagName}[id=\"${targetElement.id}\"] - element not in visible list`);

    const fallbackLabel = targetElement.textContent?.trim() ||
        targetElement.getAttribute('aria-label') ||
        targetElement.placeholder ||
        targetElement.tagName;

    const structuredTarget = buildStructuredTarget(targetElement, event, { label: fallbackLabel }, 'mouse');

    const labelText = (structuredTarget && structuredTarget.label) || fallbackLabel || 'Unknown Control';

    const valueDict = structuredTarget && structuredTarget.value && typeof structuredTarget.value === 'object'
        ? structuredTarget.value
        : {};

    return {
        event: event.type,
        target: {
            label: labelText,
            value: valueDict
        },
        button: event.button || 0,
        buttons: event.buttons || 0,
    };
}

/**
 * Build minimal error fallback event properties
 */
function buildErrorEventProperties(event, targetElement) {
    return {
        event: 'click',
        target: {
            label: 'unknown',
            value: {}
        },
        y: event.clientY || 0,
        x: event.clientX || 0,
        button: event.button || 0,
        buttons: event.buttons || 0,
    };
}

/**
 * Get mouse event properties with target resolution and screen matching
 */
export function getMouseEventProperties(event) {
    try {
        const targetElement = resolveEventTarget(event);
        const matchingElement = findMatchingScreenElement(targetElement);

        if (matchingElement) {
            return buildMatchingEventProperties(event, matchingElement, targetElement);
        } else {
            return buildFallbackEventProperties(event, targetElement);
        }

    } catch (error) {
        console.error('Error in getMouseEventProperties:', error);
        return buildErrorEventProperties(event, event.target);
    }
}

/**
 * Initialize event listeners
 */
export function initializeEventListeners() {
    // Window load event
    window.addEventListener('load', (event) => {
        flushPendingKeyboard();

        // Register this tab as a session
        registerSession();

        sendEvent('event', {
            event: 'load',
            url: window.location.href,
        });
    });

    // Click listener
    try {
        document.addEventListener('click', (event) => {
            // Debug: check if this is a synthetic event
            if (event.clientX === 100 && event.clientY === 100) {
                return; // Skip synthetic test clicks
            }

            // Process click immediately - no double-click delay
            // Flush any pending keyboard input before processing click
            flushPendingKeyboard();

            // Use queueMicrotask to read control state AFTER DOM updates complete
            queueMicrotask(() => {
                try {
                    const mouseProps = getMouseEventProperties(event);

                    sendEvent('mouse', {
                        event: 'click',
                        ...mouseProps,
                    });
                    log(`Mouse click processed: ${event.target.tagName}`);
                } catch (error) {
                    log(`Mouse click error: ${error.message}\n${error.stack}`);

                    // Send basic event without complex properties as fallback
                    sendEvent('mouse', {
                        event: 'click',
                        target: {
                            label: event.target.textContent?.trim().substring(0, 50) || event.target.tagName || 'unknown'
                        },
                        button: event.button,
                        error: error.message
                    });
                }
            });
        });
    } catch (error) {
        log(`Error attaching click listener: ${error.message}`);
        sendEvent('log', { message: `Error attaching click listener: ${error.message}` });
    }

    // Unified keyboard handler with accumulation
    document.addEventListener('keydown', (event) => {
        const currentTarget = event.target;
        const isTextInput = currentTarget.tagName === 'INPUT' &&
            (currentTarget.type === 'text' || currentTarget.type === 'email' ||
                currentTarget.type === 'search' || currentTarget.type === 'url' ||
                currentTarget.type === 'tel' || currentTarget.type === 'password') ||
            currentTarget.tagName === 'TEXTAREA';

        // Control keys - but EXCLUDE space for text inputs (space is part of typing)
        const isControlKey = event.key === 'Enter' ||
            (!isTextInput && event.key === ' ') ||
            (event.key && event.key.startsWith('Arrow')) ||
            event.key === 'Tab';

        // Exclude modifier keys from accumulation (they don't produce text)
        const isModifierKey = event.key === 'Shift' || event.key === 'Control' ||
            event.key === 'Alt' || event.key === 'Meta';

        // Control keys get sent immediately (navigation, form controls)
        if (isControlKey && isInteractiveElement(currentTarget)) {
            // Flush any pending text input first
            flushPendingKeyboard();

            // Send control key immediately using queueMicrotask for DOM updates
            queueMicrotask(() => {
                sendEvent('keyboard', {
                    event: 'control_key',
                    ...returnKeyboardEventProperties(event),
                });
            });
        }
        // Text input keys get accumulated (but skip modifier keys) 
        else if (isTextInput && !isModifierKey) {
            const currentTargetInfo = returnElementProperties(currentTarget);

            // If target changed or first keystroke, start new accumulated event
            if (!inProcessKeyboard || inProcessKeyboard.targetId !== (currentTargetInfo.id || currentTarget.id)) {
                flushPendingKeyboard(); // Send any previous accumulated event

                inProcessKeyboard = {
                    event: 'text_input',
                    targetId: currentTargetInfo.id || currentTarget.id || '', // Store ID for comparison
                    target: {
                        label: currentTarget.labels?.[0]?.textContent?.trim() ||
                            extractBestLabel(currentTargetInfo.label) ||
                            currentTarget.placeholder ||
                            currentTarget.name ||
                            currentTarget.getAttribute('aria-label') ||
                            `${currentTarget.type || 'input'}#${currentTarget.id || 'unlabeled'}`,
                        value: {} // Will be set to unified dictionary format at flush time
                    }
                };
            }
        }
    });

    // Blur event handler for keyboard accumulation management
    document.addEventListener('blur', (event) => {
        if (inProcessKeyboard) {
            flushPendingKeyboard();
        }
    }, true);

    // Submit handler
    document.addEventListener('submit', (event) => {
        flushPendingKeyboard();

        sendEvent('button', {
            event: 'submit',
            isSubmit: true,
            ...event,
        });
    });

    // Flush keyboard input before page unload
    window.addEventListener('beforeunload', (event) => {
        flushPendingKeyboard();
    });

    // Also flush on page hide (for back/forward navigation)
    window.addEventListener('pagehide', (event) => {
        flushPendingKeyboard();
    });
}

/**
 * Function to register session with tab identity
 */
async function registerSession() {
    try {
        const tabIdentity = {
            tabId: CURRENT_TAB_SESSIONID,
            url: window.location.href,
            title: document.title,
            windowId: null,
            index: null
        };

        const response = await fetch(`${CONFIG.serverUrl}/sessions/init`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-Tab-ID': CURRENT_TAB_SESSIONID
            },
            body: JSON.stringify(tabIdentity)
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Session registered successfully:', result.sessionId);
        } else {
            console.log('Failed to register session:', response.status);
        }
    } catch (error) {
        console.log('Error registering session (server likely offline):', error.message);
    }
}

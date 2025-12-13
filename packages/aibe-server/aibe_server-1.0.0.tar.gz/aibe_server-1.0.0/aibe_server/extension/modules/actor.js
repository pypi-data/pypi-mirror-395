/**
 * Actor Module
 * Actor channel for command execution - commands flowing FROM server TO browser
 */

import { CONFIG } from './config.js';
import { CURRENT_TAB_SESSIONID } from './session-manager.js';
import { log } from './utils.js';
import { getCurrentScreen } from './screen-capture.js';
import { sendEvent, scheduleChangeDetection, flushPendingKeyboard } from './events.js';

// Actor Channel State Management
let isExecutingActorCommand = false;
let inProcessKeyboard = null; // Shared with events module

/**
 * Check if it's safe to execute Actor commands
 * Prevents interference with ongoing Observer activities
 */
function isSafeToExecuteActor() {
    // Don't interrupt ongoing keyboard accumulation
    if (inProcessKeyboard) {
        return false;
    }

    // Don't overlap Actor commands
    if (isExecutingActorCommand) {
        return false;
    }

    return true;
}

/**
 * Poll server for Actor commands and execute them when safe
 * Runs continuously in background, non-blocking
 */
async function pollForActorCommands() {
    while (true) {
        try {
            // Poll server for pending commands
            const pollUrl = `${CONFIG.serverUrl}/sessions/${CURRENT_TAB_SESSIONID}/actor/commands`;
            const response = await fetch(pollUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Tab-ID': CURRENT_TAB_SESSIONID
                }
            });

            if (response.ok) {
                const commands = await response.json();

                if (commands.length > 0) {
                    // Process each command when safe
                    for (const command of commands) {
                        console.log(`🎯 POLLING DEBUG: Processing command: ${command.type} with data:`, command);
                        await processActorCommandWhenSafe(command);
                    }
                }
            } else {
                // Log HTTP error responses for debugging
                console.warn(`Actor Channel: Poll failed with status ${response.status}`);
            }
        } catch (error) {
            // Server not available or network error - continue polling
            // Don't log every polling error to avoid spam
            if (error.message && !error.message.includes('fetch')) {
                console.warn('Actor polling error:', error.message);
            }
        }

        // Non-blocking delay before next poll
        await new Promise(resolve => setTimeout(resolve, 100)); // Poll every 100ms
    }
}

/**
 * Process Actor command when it's safe to do so
 * Waits for safe execution window, then executes and echoes to Observer
 */
async function processActorCommandWhenSafe(command) {
    // Wait for safe execution window (with timeout)
    const maxWaitTime = 5000; // 5 second timeout
    const startTime = Date.now();

    console.log(`Actor Channel: Waiting for safe execution of command ${command.id}`);
    while (!isSafeToExecuteActor() && (Date.now() - startTime) < maxWaitTime) {
        await new Promise(resolve => setTimeout(resolve, 50)); // Check every 50ms
    }

    if (!isSafeToExecuteActor()) {
        log(`Actor Channel: Timeout waiting for safe execution of command ${command.id}`);
        return;
    }

    isExecutingActorCommand = true;

    try {
        try { log(`Actor Channel: Executing command ${command.id}: ${command.type}`); } catch (e) { }
        console.log(`Actor Channel: Executing command ${command.id}: ${command.type}`);
        await executeActorCommand(command);

        // Natural Observer events will detect DOM changes with proper source attribution

    } catch (error) {
        try { log(`Actor Channel: Error executing command ${command.id}: ${error.message}`); } catch (e) { }
    } finally {
        isExecutingActorCommand = false;
    }
}

/**
 * Find DOM element matching command target specification
 * Uses Observer's current screen data for reliable label-based matching with ID validation
 */
function findTargetElement(targetSpec) {
    if (!targetSpec || !targetSpec.label) {
        throw new Error('Actor: Target specification missing or invalid');
    }

    // Handle both old format {control, control_id} and new format (direct string)
    let control, control_id;
    if (typeof targetSpec.label === 'object' && targetSpec.label.control) {
        // Old format: {control: "text", control_id: "id"}
        control = targetSpec.label.control;
        control_id = targetSpec.label.control_id;
    } else {
        // New format: direct label string with id separate
        control = targetSpec.label;
        control_id = targetSpec.id;
    }

    // Primary strategy: Search current screen's visible_elements by label
    const currentScreen = getCurrentScreen();

    // Use exact matching only - same strategy as TestingFramework
    const screenElement = currentScreen.visible_elements.find(element => {
        return element.label && element.label.toLowerCase() === control.toLowerCase();
    });

    if (!screenElement) {
        // Log available labels to help with debugging
        const availableLabels = currentScreen.visible_elements
            .map(el => el.label || 'unlabeled')
            .slice(0, 10);
        log(`Actor: No element found with exact label "${control}". Available labels: ${availableLabels.join(', ')}`);
        throw new Error(`Actor: No element found with label "${control}" in current screen`);
    }

    // Check for multiple matches and warn (but still use first match for consistency)
    const allMatches = currentScreen.visible_elements.filter(element => {
        return element.label && element.label.toLowerCase() === control.toLowerCase();
    });

    if (allMatches.length > 1) {
        log(`Actor: WARNING - Multiple elements (${allMatches.length}) found with label "${control}". Using first match. Consider improving label uniqueness.`);
    }

    let foundElement = screenElement.node;
    let matchMethod = 'exact_label_match';

    // Cross-validation: Double-check ID matches if provided
    if (control_id && foundElement && foundElement.id !== control_id) {
        log(`Actor: WARNING - Label-based match found but ID mismatch. Expected: "${control_id}", Found: "${foundElement.id}"`);
        log(`Actor: This might indicate screen changes or labeling inconsistencies`);
    }

    // Log successful match for debugging
    if (foundElement) {
        log(`Actor: Found target element via ${matchMethod} - ${foundElement.tagName}[id="${foundElement.id}"] with label "${screenElement.label}"`);
    } else {
        log(`Actor: WARNING - screenElement.node is null for label "${screenElement.label}". This indicates an architectural issue.`);
    }

    return {
        element: foundElement,
        screenElement: screenElement,  // Include the full screen element data
        matchMethod: matchMethod,
        validated: !control_id || (foundElement && foundElement.id === control_id)
    };
}

/**
 * Set value on different control types before triggering events
 * Handles the complexity of different HTML control value setting
 */
function setElementValue(element, newValue, controlType) {
    const tagName = element.tagName.toLowerCase();
    const inputType = element.type?.toLowerCase();

    try {
        switch (tagName) {
            case 'input':
                if (inputType === 'checkbox' || inputType === 'radio') {
                    // For checkboxes/radio: newValue should be boolean or 'checked'/'unchecked'
                    const shouldCheck = newValue === true || newValue === 'checked' || newValue === 'true';
                    element.checked = shouldCheck;
                    try { log(`Actor: Set ${inputType} to ${shouldCheck ? 'checked' : 'unchecked'}`); } catch (e) { }
                } else {
                    // Text inputs, password, email, etc.
                    if (newValue === undefined || newValue === null) {
                        element.value = '';  // Explicitly clear if no value provided
                    } else {
                        element.value = newValue;  // Use exactly what was provided
                    }
                    try { log(`Actor: Set input value to "${element.value}"`); } catch (e) { }
                }
                break;

            case 'select':
                // Dropdown: find option by text or value
                const options = Array.from(element.options);
                let targetOption = null;

                // Try to match by value first, then by text
                targetOption = options.find(opt => opt.value === newValue) ||
                    options.find(opt => opt.text === newValue);

                if (targetOption) {
                    element.selectedIndex = targetOption.index;
                    try { log(`Actor: Set select to option "${targetOption.text}" (value: "${targetOption.value}")`); } catch (e) { }
                } else {
                    throw new Error(`Actor: Could not find option "${newValue}" in dropdown`);
                }
                break;

            case 'textarea':
                if (newValue === undefined || newValue === null) {
                    element.value = '';  // Explicitly clear if no value provided
                } else {
                    element.value = newValue;  // Use exactly what was provided
                }
                try { log(`Actor: Set textarea value to "${element.value}"`); } catch (e) { }
                break;

            default:
                // For buttons, links, etc. - no value to set
                try { log(`Actor: No value to set for ${tagName} element`); } catch (e) { }
        }

        return true;
    } catch (error) {
        try { log(`Actor: Error setting value on ${tagName}: ${error.message}`); } catch (e) { }
        throw error;
    }
}

/**
 * Execute the actual Actor command
 * Handles different command types with proper source tagging and native browser methods
 */
async function executeActorCommand(command) {
    console.log(`🚀 EXECUTE ENTRY: executeActorCommand called with command type: "${command.type}"`);
    log(`Actor Channel: Executing ${command.type} command`);

    // Set global flag to mark subsequent Observer events as Actor-generated
    window.actorExecuting = true;
    console.log(`🚀 ACTOR FLAG SET: ${command.type} - actorExecuting=true`);
    try { log(`Actor Channel: Setting actorExecuting flag for command: ${command.type}`); } catch (e) { }

    try {
        console.log(`🔍 EXECUTE DEBUG: About to switch on command type: "${command.type}"`);
        switch (command.type) {
            case 'screen_status':
                // Quietly ignore screen_status commands - browser generates its own reports
                log(`Actor Channel: Ignoring screen_status command (browser will generate own reports)`);
                break;

            case 'test_actor_channel':
                // Test command - just log and echo back
                log(`Actor Channel: Test command received: ${command.data.message}`);
                break;

            case 'mouse':
                try {
                    const target = findTargetElement(command.target);
                    log(`Actor Channel: Clicking element ${target.element.tagName}[id="${target.element.id}"]`);

                    // For state-changing controls, set values from dictionary
                    if (command.target?.value && typeof command.target.value === 'object') {
                        const element = target.element;
                        const tagName = element.tagName.toLowerCase();

                        if (tagName === 'select') {
                            // Handle dropdown selections - set selected options
                            const targetValues = Object.values(command.target.value);
                            Array.from(element.options).forEach(option => {
                                option.selected = targetValues.includes(option.value);
                            });
                            element.dispatchEvent(new Event('change', { bubbles: true }));
                        } else if (element.type === 'checkbox' || element.type === 'radio') {
                            // Handle checkbox/radio - set checked state
                            const values = Object.values(command.target.value);
                            element.checked = values.includes(true);
                            element.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                    }

                    // Use native browser click method for authentic events
                    target.element.click();

                } catch (error) {
                    log(`Actor Channel: Mouse click failed: ${error.message}`);
                }
                break;

            case 'keyboard':
                try {
                    console.log(`🔍 KEYBOARD DEBUG: Processing keyboard command with data:`, command.data);
                    console.log(`🔍 KEYBOARD DEBUG: Target specification:`, command.target);
                    const target = findTargetElement(command.target);
                    console.log(`🔍 KEYBOARD DEBUG: Found target element:`, target.element.tagName, target.element.type, target.element.id);

                    const valueObj = command.target?.value;
                    if (!valueObj || typeof valueObj !== 'object') {
                        throw new Error(`Invalid keyboard command: target.value must be an object, got: ${JSON.stringify(valueObj)}`);
                    }

                    // Set the value using native methods (actorExecuting flag already set by executeActorCommand)
                    target.element.focus();  // Focus first for proper event sequence
                    console.log(`🔍 KEYBOARD DEBUG: Before setting value, current value: "${target.element.value}"`);

                    let newValue = '';

                    // Handle different element types specially, using the same value shapes as Observer
                    if (target.element.tagName === 'SELECT') {
                        const selectedInternalValues = Object.values(valueObj);
                        if (target.element.multiple) {
                            // Multi-select: select all values present in dictionary values
                            Array.from(target.element.options).forEach(option => {
                                option.selected = selectedInternalValues.includes(option.value);
                            });
                            newValue = selectedInternalValues.join(',');
                            console.log(`🔍 KEYBOARD DEBUG: Multi-select set to values: [${selectedInternalValues.join(', ')}]`);
                        } else {
                            // Single select: use first value in dictionary
                            const chosen = selectedInternalValues[0] ?? '';
                            target.element.value = chosen;
                            Array.from(target.element.options).forEach(option => {
                                option.selected = (option.value === chosen);
                            });
                            newValue = chosen;
                            console.log(`🔍 KEYBOARD DEBUG: Single select set to value: "${chosen}"`);
                        }
                    } else if (target.element.type === 'checkbox' || target.element.type === 'radio') {
                        // Checkboxes and radio buttons: expect a boolean somewhere in the dictionary values
                        const boolVal = Object.values(valueObj).find(v => typeof v === 'boolean');
                        const shouldCheck = !!boolVal;
                        target.element.checked = shouldCheck;
                        newValue = shouldCheck ? 'true' : 'false';
                        console.log(`🔍 KEYBOARD DEBUG: ${target.element.type} set to checked: ${shouldCheck}`);
                    } else {
                        // Text-like controls: expect { text: "..." }
                        if (!Object.prototype.hasOwnProperty.call(valueObj, 'text')) {
                            throw new Error(`Invalid keyboard command format for text control: expected { text: "..." }, got: ${JSON.stringify(valueObj)}`);
                        }
                        newValue = valueObj.text;
                        target.element.value = newValue;
                        console.log(`🔍 KEYBOARD DEBUG: After setting value, current value: "${target.element.value}"`);
                    }

                    // Trigger native events for form validation and handlers
                    target.element.dispatchEvent(new Event('input', { bubbles: true }));
                    target.element.dispatchEvent(new Event('change', { bubbles: true }));

                    log(`Actor Channel: Set value "${newValue}" in ${target.element.tagName}[id="${target.element.id}"]`);

                    // Build a human-friendly value object for Observer echo
                    let echoValue;
                    const labelForEcho = (target.screenElement && target.screenElement.label) ||
                        (target.element.labels && target.element.labels[0] && target.element.labels[0].textContent && target.element.labels[0].textContent.trim()) ||
                        target.element.getAttribute('aria-label') ||
                        target.element.placeholder ||
                        target.element.name ||
                        `${target.element.type || target.element.tagName.toLowerCase()}#${target.element.id || 'unlabeled'}`;

                    if (target.element.tagName === 'SELECT') {
                        // Use dictionary mapping display text -> value for selected options
                        const selectedOpts = Array.from(target.element.selectedOptions || []);
                        const dict = {};
                        selectedOpts.forEach(opt => {
                            dict[opt.text] = opt.value;
                        });
                        echoValue = dict;
                    } else if (target.element.type === 'checkbox' || target.element.type === 'radio') {
                        const dict = {};
                        dict[labelForEcho] = target.element.checked;
                        echoValue = dict;
                    } else {
                        // Text-like controls: use unified { text } format
                        echoValue = { text: newValue };
                    }

                    // Echo Actor keyboard input on Observer channel for causal pairing
                    sendEvent('keyboard', {
                        event: 'text_input',
                        target: {
                            label: labelForEcho,
                            ...(echoValue && Object.keys(echoValue).length ? { value: echoValue } : {})
                        }
                    });

                    // Explicitly trigger screen change detection for Actor commands
                    scheduleChangeDetection();

                } catch (error) {
                    log(`Actor Channel: Keyboard input failed: ${error.message}`);
                }
                break;

            case 'set_value':
                try {
                    const target = findTargetElement(command.target);
                    const newValue = command.data?.value;

                    // Set the value and trigger change event
                    setElementValue(target.element, newValue);
                    target.element.dispatchEvent(new Event('change', { bubbles: true }));

                    log(`Actor Channel: Set value "${newValue}" on ${target.element.tagName}[id="${target.element.id}"]`);

                } catch (error) {
                    log(`Actor Channel: Set value failed: ${error.message}`);
                }
                break;

            case 'load':
                try {
                    const targetUrl = command.target?.url;
                    if (!targetUrl) {
                        throw new Error('Load command requires target.url');
                    }

                    log(`Actor Channel: Navigating to URL: ${targetUrl}`);

                    // Use native browser navigation for authentic page load
                    window.location.href = targetUrl;

                    // Note: No explicit success logging here as page will reload
                    // Success will be evident from subsequent screen_status events

                } catch (error) {
                    log(`Actor Channel: Load navigation failed: ${error.message}`);
                }
                break;

            default:
                // Log unrecognized commands - may report these in future
                console.log(`🔍 EXECUTE DEBUG: UNRECOGNIZED command type: "${command.type}"`);
                try { log(`Actor Channel: Unrecognized command type: ${command.type}`); } catch (e) { }
        }
    } finally {
        // Flag clearing now handled at event attribution time for tighter timing
        log(`Actor Channel: Command execution complete`);
    }
}

/**
 * Initialize Actor channel polling when content script loads
 * Runs in background, non-blocking
 */
export function initializeActorChannel() {
    log('Actor Channel: Initializing Actor command polling');

    // Start polling in background (don't await - let it run continuously)
    pollForActorCommands().catch(error => {
        log(`Actor Channel: Polling loop crashed: ${error.message}`);
    });
}

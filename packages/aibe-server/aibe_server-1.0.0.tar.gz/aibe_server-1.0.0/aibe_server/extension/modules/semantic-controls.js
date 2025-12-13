/**
 * Semantic Controls Module
 * Semantic control definitions and detection for the Generic User Framework
 * 
 * Philosophy: Instead of making AI systems understand the complexity of HTML/CSS/DOM,
 * we present a simplified semantic view of "what a human would see" - buttons, inputs,
 * dropdowns, etc. This enables AI to browse the web using human-like mental models
 * rather than low-level DOM manipulation.
 */

import { EXTENSION_CONFIG } from './config.js';

//=================================================================================
// SEMANTIC CONTROL DEFINITIONS - User-visible control abstractions
//=================================================================================

/**
 * SEMANTIC_CONTROL_DEFINITIONS - Generic User Framework Implementation
 * 
 * This defines the semantic abstraction layer that translates complex DOM structures
 * into human-meaningful control types that AI systems can understand and interact with.
 * 
 * Each definition maps DOM patterns to semantic control types, allowing one abstraction
 * to handle many different HTML implementations of the same user interaction concept.
 */
export const SEMANTIC_CONTROL_DEFINITIONS = [
    {
        id: 'INPUT_TEXT',
        visible_state: ['label', 'value', 'placeholder', 'is_focused', 'is_disabled'],
        actions: ['type', 'clear', 'focus', 'blur'],
        detection_rules: [
            { tagName: 'input', type: 'text' },
            { tagName: 'input', type: 'email' },
            { tagName: 'input', type: 'url' },
            { tagName: 'input', type: 'search' },
            { tagName: 'input', type: 'tel' }
        ]
    },
    {
        id: 'INPUT_PASSWORD',
        visible_state: ['label', 'is_masked', 'is_focused', 'is_disabled'],
        actions: ['type', 'clear', 'focus', 'blur', 'toggle_visibility'],
        detection_rules: [
            { tagName: 'input', type: 'password' }
        ]
    },
    {
        id: 'INPUT_DROPDOWN',
        visible_state: ['label', 'current_value', 'available_options', 'is_open', 'is_disabled'],
        actions: ['open', 'close', 'select_option', 'focus'],
        detection_rules: [
            { tagName: 'select' },
            { role: 'combobox' },
            { role: 'listbox' }
        ]
    },
    {
        id: 'INPUT_CHECKBOX',
        visible_state: ['label', 'is_checked', 'is_disabled'],
        actions: ['toggle', 'check', 'uncheck'],
        detection_rules: [
            { tagName: 'input', type: 'checkbox' }
        ]
    },
    {
        id: 'INPUT_RADIO',
        visible_state: ['label', 'is_selected', 'is_disabled', 'group_name'],
        actions: ['select'],
        detection_rules: [
            { tagName: 'input', type: 'radio' }
        ]
    },
    {
        id: 'INPUT_TEXTAREA',
        visible_state: ['label', 'value', 'placeholder', 'is_focused', 'is_disabled'],
        actions: ['type', 'clear', 'focus', 'blur'],
        detection_rules: [
            { tagName: 'textarea' }
        ]
    },
    {
        id: 'BUTTON_ACTION',
        visible_state: ['label', 'is_disabled', 'is_focused'],
        actions: ['click'],
        detection_rules: [
            { tagName: 'button', type: 'button' },
            { tagName: 'input', type: 'button' },
            { role: 'button' }
        ]
    },
    {
        id: 'BUTTON_SUBMIT',
        visible_state: ['label', 'is_disabled', 'is_focused'],
        actions: ['click', 'submit'],
        detection_rules: [
            { tagName: 'button', type: 'submit' },
            { tagName: 'input', type: 'submit' }
        ]
    },
    {
        id: 'LINK',
        visible_state: ['label', 'destination_hint'],
        actions: ['click', 'open_new_tab'],
        detection_rules: [
            { tagName: 'a', hasHref: true }
        ]
    }
];

/**
 * Detects the semantic control type(s) for a given DOM element
 * @param {Element} element - The DOM element to analyze
 * @returns {Array<number>} Array of indexes into SEMANTIC_CONTROL_DEFINITIONS that match
 */
export function detectSemanticControlType(element) {
    const elementProps = {
        tagName: element.tagName.toLowerCase(),
        type: element.type?.toLowerCase(),
        role: element.getAttribute('role'),
        hasHref: !!element.href
    };

    // Return array of matching control definition indexes
    return SEMANTIC_CONTROL_DEFINITIONS
        .map((def, index) => ({ def, index }))
        .filter(({ def }) =>
            def.detection_rules.some(rule =>
                Object.entries(rule).every(([key, value]) =>
                    elementProps[key] === value
                )
            )
        )
        .map(({ index }) => index);
}

/**
 * Gets the semantic control definition by index
 * @param {number} index - Index into SEMANTIC_CONTROL_DEFINITIONS
 * @returns {Object|null} Control definition or null if invalid index
 */
export function getSemanticControlDefinition(index) {
    return SEMANTIC_CONTROL_DEFINITIONS[index] || null;
}

/**
 * Add dropdown-specific state to semantic element
 * @param {Object} element - Element object to modify
 * @param {HTMLElement} node - The select element
 */
export function addDropdownSemanticState(element, node) {
    const options = Array.from(node.options || []);
    const selectedOptions = Array.from(node.selectedOptions || []);

    // Handle both single and multi-select properly
    const isMultiSelect = node.multiple || node.type === 'select-multiple';

    if (selectedOptions.length === 0) {
        element.current_selection = '(none selected)';
        element.current_value = isMultiSelect ? [] : null;
    } else if (selectedOptions.length === 1) {
        element.current_selection = selectedOptions[0].text;
        element.current_value = isMultiSelect ? [selectedOptions[0].value] : selectedOptions[0].value;
    } else {
        // Multi-select: show arrays
        element.current_selection = selectedOptions.map(opt => opt.text);
        element.current_value = selectedOptions.map(opt => opt.value);
    }

    element.clickable_options = options
        .filter(opt => opt.value !== '') // Skip placeholder options
        .map(opt => `"${opt.text}" → ${opt.value}`);
    element.is_open = node.matches(':focus') && node.size > 1; // Approximate open state
    element.is_disabled = node.disabled || false;
}

/**
 * Add password-specific state to semantic element
 * @param {Object} element - Element object to modify
 * @param {HTMLElement} node - The password input element
 */
export function addPasswordSemanticState(element, node) {
    element.is_focused = document.activeElement === node;
    element.is_disabled = node.disabled || false;

    // Handle password value based on showPasswordValues setting
    if (EXTENSION_CONFIG.showPasswordValues) {
        // Include actual password value when setting is enabled
        element.value = node.value || '';
        element.is_masked = false;
    } else {
        // Omit value entirely when masking is enabled (no value field at all)
        element.is_masked = true;
        // Note: deliberately NOT setting element.value for security
    }
}

/**
 * Add link-specific state to semantic element
 * @param {Object} element - Element object to modify
 * @param {HTMLElement} node - The link element
 */
export function addLinkSemanticState(element, node) {
    element.destination_hint = node.href || null;
}

/**
 * Add generic interactive element state to semantic element
 * @param {Object} element - Element object to modify
 * @param {HTMLElement} node - The interactive element
 */
export function addGenericSemanticState(element, node) {
    element.value = 'value' in node ? node.value : null;
    element.placeholder = node.placeholder || null;
    element.is_focused = document.activeElement === node;
    element.is_disabled = node.disabled || false;

    // Capture checkbox/radio specific properties
    if (node.type === 'checkbox' || node.type === 'radio') {
        element.checked = node.checked;
    }

    // Capture select-specific properties
    if (node.tagName === 'SELECT') {
        element.selectedOptions = Array.from(node.selectedOptions || []);
        element.multiple = node.multiple;
        element.selectedIndex = node.selectedIndex;
    }
}

/**
 * Build semantic element with proper priority ordering
 * @param {HTMLElement} node - The DOM element
 * @param {Object} semanticDef - Semantic definition object
 * @param {Object} positionData - Element position data
 * @param {string} existingLabel - Pre-existing label if any
 * @returns {Object} - Semantic element object
 */
export function buildSemanticElement(node, semanticDef, positionData, existingLabel = null) {
    // Master Creator - ALL field assignments in priority order
    // JavaScript object property order is determined by assignment order!
    const element = {};

    // Priority 1: Label (most important for AI)
    element.label = existingLabel;

    // Priority 2: Control type (semantic classification)
    element.control_type = semanticDef.id;

    // Priority 3: Basic element identification
    element.tagName = node.tagName?.toLowerCase();
    element.type = node.type?.toLowerCase();

    // Priority 4: User-visible state (semantic-specific)
    switch (semanticDef.id) {
        case 'INPUT_DROPDOWN':
            addDropdownSemanticState(element, node);
            break;
        case 'INPUT_PASSWORD':
            addPasswordSemanticState(element, node);
            break;
        case 'LINK':
            addLinkSemanticState(element, node);
            break;
        default:
            addGenericSemanticState(element, node);
            break;
    }

    // Priority 5: Special attributes (only if relevant)
    if (node.href) {
        element.href = node.href;
    }

    // Priority 6: Position data (for targeting)
    element.top = positionData.top;
    element.left = positionData.left;
    element.bottom = positionData.bottom;
    element.right = positionData.right;

    // Priority 7: Node reference (always last, for internal use)
    element.node = node;

    return element;
}

/**
 * Utility Module
 * Shared utility functions used across multiple modules
 */

/**
 * Function to log messages to remote server log
 * Currently disabled to reduce event noise
 */
export async function log(message) {
    // Disabled debug logging to reduce event noise
    // console.log(message);
}

/**
 * Copies specified attributes for semantic control abstraction.
 * Filters out internal DOM properties while preserving user-visible state,
 * creating a clean interface between raw DOM elements and semantic representations.
 */
export function copyAttributes(source, target, attr_list) {
    attr_list.forEach(attr => {
        if (source[attr] !== undefined) {
            target[attr] = source[attr];
        }
    })
    return target;
}

/**
 * Extract the best label from a label dictionary or return string as-is
 * Priority: Parent_Label, Left_Label, control, text, or first available key
 */
export function extractBestLabel(label) {
    if (typeof label === 'string') {
        return label;
    }

    if (typeof label === 'object' && label !== null) {
        // Priority order for label extraction
        const priorities = ['Parent_Label', 'Left_Label', 'control', 'text'];

        for (const key of priorities) {
            if (label[key] && typeof label[key] === 'string') {
                return label[key];
            }
        }

        // Fallback: return first string value found
        for (const [key, value] of Object.entries(label)) {
            if (typeof value === 'string' && value.trim() !== '') {
                return value;
            }
        }

        // Last resort: stringify the object
        return JSON.stringify(label);
    }

    return String(label);
}

/**
 * Helper function to get element position for sorting
 */
export function returnElementPosition(element) {
    if (typeof element.getBoundingClientRect === 'function') {
        const rect = element.getBoundingClientRect();
        return {
            top: rect.top + window.scrollY,
            left: rect.left + window.scrollX,
            bottom: rect.bottom + window.scrollY,
            right: rect.right + window.scrollX,
        };
    }
    if (typeof element?.node?.getBoundingClientRect === 'function') {
        const rect = element.node.getBoundingClientRect();
        return {
            top: rect.top + window.scrollY,
            left: rect.left + window.scrollX,
            bottom: rect.bottom + window.scrollY,
            right: rect.right + window.scrollX,
        };
    }
    // Actually, this should never happen
    return {
        top: -1,
        left: -1,
        bottom: -1,
        right: -1,
    }
}

/**
 * Check if element is a text element (heading, paragraph, list item)
 */
export function isTextElement(element) {
    const node = typeof element.node === 'undefined' ? element : element.node;
    // --> If it's editable, is it really just text?
    if (node && node.getAttribute && node.getAttribute('contenteditable') === 'true') {
        return false;
    }
    return ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li'].includes(node.tagName.toLowerCase());
}

/**
 * Check if element is interactive (can be clicked, typed into, etc.)
 */
export function isInteractiveElement(element) {
    const node = typeof element.node === 'undefined' ? element : element.node;
    // Check tag name first
    if (typeof node.tagName === 'undefined') {
        return false;
    }
    if (['a', 'button', 'input', 'select', 'textarea', 'details', 'summary', 'dialog'].includes(node.tagName.toLowerCase())) {
        return true;
    }

    // Check for contenteditable attribute if element is provided
    if (node && node.getAttribute && node.getAttribute('contenteditable') === 'true') {
        return true;
    }

    // Check for ARIA roles that make elements interactive
    if (node && node.getAttribute) {
        const role = node.getAttribute('role');
        if (['button', 'combobox', 'listbox'].includes(role)) {
            return true;
        }
    }

    return false;
}

/**
 * Get base event modifiers from event object
 * @param {Event} event - The DOM event
 * @returns {Object} - Modifier keys state
 */
export function getEventModifiers(event) {
    return {
        ctrl: event.ctrlKey,
        shift: event.shiftKey,
        alt: event.altKey,
        meta: event.metaKey
    };
}

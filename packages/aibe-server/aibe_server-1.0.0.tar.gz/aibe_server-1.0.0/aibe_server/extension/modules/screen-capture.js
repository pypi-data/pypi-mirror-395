/**
 * Screen Capture Module
 * Manages screen state capture, element collection, and screen change detection
 */

import { isTextElement, isInteractiveElement, returnElementPosition, log } from './utils.js';
import { detectSemanticControlType, getSemanticControlDefinition, buildSemanticElement } from './semantic-controls.js';
import { addLabel } from './labeling.js';
import { EXTENSION_CONFIG } from './config.js';

// Previous screen state for comparison
export let previousScreen = null;

/**
 * Helper function to get element properties with semantic control detection
 */
export function returnElementProperties(element) {
    // Note: Element may be a DOM node, or a dictionary with a node entry.
    //       Also, the proper label might not have been found yet!
    const node = typeof element.node === 'undefined' ? element : element.node;
    const positionData = returnElementPosition(element);

    // Check if element exists on previous screen to preserve label
    let existingLabel = null;
    if (previousScreen) {
        previousScreen.visible_elements.forEach((screenElement) => {
            if (screenElement.node && screenElement.node.id === node.id) {
                existingLabel = screenElement.label;
            }
        });
    }

    // Try semantic control detection for interactive elements
    if (isInteractiveElement(node)) {
        const semanticIndexes = detectSemanticControlType(node);

        if (semanticIndexes.length > 1) {
            // Multiple matches - this is an error condition that should be visible
            const matchedTypes = semanticIndexes.map(i => getSemanticControlDefinition(i).id);
            console.warn(`Multiple semantic control matches for ${node.tagName}[type="${node.type}"][id="${node.id}"]: ${matchedTypes.join(', ')} - using first match`);
        }

        if (semanticIndexes.length > 0) {
            // Use first matching semantic control type
            const semanticDef = getSemanticControlDefinition(semanticIndexes[0]);
            return buildSemanticElement(node, semanticDef, positionData, existingLabel);
        }
    }

    // Fallback for non-interactive elements (text content, etc.)
    const elem = {
        label: existingLabel,
        tagName: node.tagName?.toLowerCase(),
        textContent: null,
        top: positionData.top,
        left: positionData.left,
        bottom: positionData.bottom,
        right: positionData.right,
        has_focus: document.activeElement === node,
        node: node
    };

    // Add href only if the element actually has one
    if (node.href) {
        elem.href = node.href;
    }

    // Add text content for non-interactive elements
    if (!isInteractiveElement(node)) {
        elem.textContent = node?.textContent?.trim();
    }

    // Add href for links that weren't caught by semantic detection
    if (node?.href) {
        elem.href = node.href;
    }

    return elem;
}

/**
 * Collect all visible elements from the DOM
 */
export function collectAllVisibleElements() {
    const elements = [];
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
        {
            acceptNode: function (node) {
                // Skip hidden elements and their children
                if (node.nodeType === Node.ELEMENT_NODE) {
                    const style = window.getComputedStyle(node);
                    if (style.display === 'none' || style.visibility === 'hidden') {
                        return NodeFilter.FILTER_REJECT;
                    }
                }
                if (typeof node.tagName === 'undefined') {
                    return NodeFilter.FILTER_REJECT;
                }
                // Skip empty/whitespace text nodes
                if (node.nodeType === Node.TEXT_NODE && (!node.nodeValue || /^[\s\r\n\t]*$/.test(node.nodeValue))) {
                    return NodeFilter.FILTER_REJECT;
                }
                return NodeFilter.FILTER_ACCEPT;
            }
        }
    );

    // Collect all visible nodes
    const allNodes = [];
    while (walker.nextNode()) {
        let node = walker.currentNode;
        if (walker.currentNode.nodeType === Node.TEXT_NODE) {
            node = walker.currentNode.parentElement;
            if (isTextElement(node)) {
                allNodes.push(walker.currentNode);
            }
        } else {
            if (isInteractiveElement(node)) {
                allNodes.push(walker.currentNode);
            }
        }
    }

    // Process nodes to extract minimal required information
    return allNodes.map((node) => {
        const isText = node.nodeType === Node.TEXT_NODE;
        const element = isText ? node.parentElement : node;

        let result = {
            ...(isText ? {} : { label: '' }),
            tagName: element.tagName?.toLowerCase(),
            ...(isInteractiveElement(element) && element.tagName?.toLowerCase() === 'a' ? { href: '' } : {}),
            ...(isInteractiveElement(element) && element.tagName?.toLowerCase() !== 'a' ? { type: '' } : {}),
            ...(isText ? { textContent: '' } : {}),
            ...returnElementPosition(element),
        };

        if (isText && isTextElement(result)) {
            result.textContent = node.textContent.trim();
        }

        // Only add interactive properties for interactive elements
        if (!isText && isInteractiveElement(node)) {
            result = returnElementProperties(element);
        }

        result.node = node;

        return result;
    }).sort((a, b) => a.top - b.top || a.left - b.left);
}

/**
 * Get current screen status with all visible elements
 */
export function getCurrentScreen() {
    const screen = {
        type: 'screen_status',
        url: window.location.href,
        focus_label: null,
        visible_elements: collectAllVisibleElements(),
    };

    // Add labels to interactive elements
    screen.visible_elements.map((element) => {
        if (isInteractiveElement(element)) {
            addLabel(element, screen.visible_elements);
            if (element.has_focus && element.label) {
                screen.focus_label = element.label;
            }
        }
    });

    return screen;
}

/**
 * Update previous screen reference (called after sending screen_status)
 * @param {Object} screen - The screen object to store
 */
export function updatePreviousScreen(screen) {
    previousScreen = screen;
}

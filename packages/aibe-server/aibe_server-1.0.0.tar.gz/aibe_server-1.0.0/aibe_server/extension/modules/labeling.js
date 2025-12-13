/**
 * Labeling Module
 * Element labeling logic - finds and assigns labels to elements
 */

import { isTextElement } from './utils.js';
import { extractBestLabel } from './utils.js';

/**
 * Find the label associated with an element
 * @param {Object} element - Element with node property
 * @param {Array} elements - List of all visible elements
 */
export function addLabel(element, elements) {
    // todo: Search for label to the left of the input element
    // todo: Search for the label above the input element
    let labels = element?.labels ? element.labels : {};

    // Handle all button types properly
    if (element.tagName.toLowerCase() === 'button') {
        element.label = element.node.textContent.trim();
    } else if (element.tagName.toLowerCase() === 'input' && element.node.type === 'button') {
        // Input buttons use value attribute, not textContent
        element.label = element.node.value || '';
    } else if (element.node.getAttribute && element.node.getAttribute('role') === 'button') {
        // ARIA buttons use textContent
        element.label = element.node.textContent.trim();
    }

    // if anchor, use text!
    if (element.tagName.toLowerCase() === 'a') {
        element.label = element.node.textContent.trim();
        if (element.label === '') {
            let text = '';
            element.node.childNodes.forEach(node => {
                text += node.alt || node.textContent;
            })
            if (text !== '') {
                element.label = text.trim();
            }
        }
    }

    // Check for explicit label association
    if (!element.label && element.node.id) {
        const label = document.querySelector(`label[for="${element.node.id}"]`);
        if (label) {
            element.label = label.textContent.trim();
        }
    }

    // Check for implicit label association (label wrapping the element)
    if (!element.label && typeof element.node.closest === 'function') {
        const parentLabel = element.node.closest('label');
        if (parentLabel) {
            labels.Parent_Label = parentLabel.textContent.trim();
        }
    }

    // Note: Search for a Label to the left of the element. If the label has been determined
    //       above, use that because it's more likely to be correct...
    if (!element.label) {
        let prev = null;
        // search for element to the left and not below the element
        for (const el of elements) {
            const el_midpoint = (el.top + el.bottom) / 2;
            if (el_midpoint > element.top && el_midpoint > element.bottom
                && el.right < element.left) {
                // found an item to the left of the element
            } else {
                // is this the element we're searching for a label for?
                if (el === element) {
                    // If we found the element, stop searching
                    if (prev && isTextElement(prev)) {
                        // if the element to the left is textual, assume it's a label
                        labels.Left_Label = prev.textContent.trim();
                    }
                }
                break;
            }
        }
    }

    if (!element.label && Object.keys(labels).length > 0) {
        element.label = extractBestLabel(labels);
    }
}

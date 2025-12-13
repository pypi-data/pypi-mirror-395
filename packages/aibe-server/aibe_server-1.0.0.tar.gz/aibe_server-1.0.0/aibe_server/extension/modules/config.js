/**
 * Configuration Module
 * Central configuration constants and settings for the extension
 */

// Extension configuration settings (loaded from chrome.storage)
export const EXTENSION_CONFIG = {
    showPasswordValues: false  // Will be loaded from chrome.storage.local
};

// Server configuration
export const CONFIG = {
    changeDetectionDelay: 500, // ms NOT USED!
    serverUrl: 'http://localhost:3001'
};

// Timing constants
export const STABLE_SCREEN_DELAY = 300; // mS
export const STABLE_SCREEN_MAX_WAIT = 2000; // mS
export const DOUBLE_CLICK_THRESHOLD = 250; //mS

// Attribute lists for different element types
export const INPUT_ATTRIBUTES = ['value', 'type', 'name', 'id', 'placeholder', /* 'disabled', */ 'readonly',
    'required', 'maxlength', 'minlength', 'pattern', 'autocomplete',
    'autofocus', 'checked', 'multiple', 'size', 'disabled', 'readonly',
    'minlength', 'required', 'maxlength', 'minlength', 'pattern',
    'autocomplete', 'autofocus', 'checked', 'multiple', 'size',
    'has_focus', 'validity state', 'aria-label', 'aria-required',
    'aria-invalid', 'aria-describedby', 'label text', /* 'form', */ 'position',
    'dimensions', 'visibility'];

// ## For Specific Input Types
// 19. **min/max** - For number and date inputs
// 20. **step** - For number inputs
// 21. **accept** - For file inputs (file types accepted)
// 22. **list** - ID of a datalist element providing suggestions

export const SELECT_ATTRIBUTES = ['name', 'id', /* 'disabled', */ 'readonly', 'required', 'multiple', 'size',
    'has_focus', 'validity state', 'aria-label', 'aria-required',
    'aria-invalid', 'aria-describedby', 'label text', /* 'form', */
    'value', 'position', 'dimensions', 'visibility', 'options',
    'selectedIndex', 'selectedOptions',
    'value', 'text', 'selected'];

// Button attributes explanation:
// formaction: Specifies where to send form data (overrides form's action attribute)
// formenctype: Specifies how form data should be encoded before sending to server (for type="submit")
//              Values: application/x-www-form-urlencoded (default), multipart/form-data, text/plain
// formmethod: Specifies HTTP method for sending form data (GET/POST, overrides form's method)
// formnovalidate: Specifies that form shouldn't be validated when submitted (boolean attribute)
//              Useful for "Save Draft" or "Cancel" buttons to bypass validation
// formtarget: Specifies where to display response after form submission (overrides form's target)
export const BUTTON_ATTRIBUTES = ['name', 'id', 'type', /*'disabled', */ /* 'form',*/ 'autofocus',
    'formaction', 'formenctype', 'formmethod', 'formnovalidate',
    'formtarget', 'value', 'has_focus', 'aria-label', 'aria-required',
    'aria-invalid', 'aria-describedby', 'label text', 'position',
    'dimensions', 'visibility'];

export const TEXTAREA_ATTRIBUTES = ['name', 'id', 'placeholder', /* 'disabled', */ 'readonly', 'required',
    'maxlength', 'minlength', 'rows', 'cols', 'wrap', /* 'form', */
    'autofocus', 'has_focus', 'validity state', 'aria-label',
    'aria-required', 'aria-invalid', 'aria-describedby', 'label text',
    'value', 'position', 'dimensions', 'visibility'];

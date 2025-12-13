(() => {
  // modules/config.js
  var EXTENSION_CONFIG = {
    showPasswordValues: false
    // Will be loaded from chrome.storage.local
  };
  var CONFIG = {
    changeDetectionDelay: 500,
    // ms NOT USED!
    serverUrl: "http://localhost:3001"
  };
  var STABLE_SCREEN_DELAY = 300;

  // modules/session-manager.js
  var CURRENT_TAB_SESSIONID = sessionStorage.getItem("tabSessionId");
  if (!CURRENT_TAB_SESSIONID) {
    CURRENT_TAB_SESSIONID = "tab_" + Math.random().toString(36).substr(2, 9) + "_" + Date.now();
    sessionStorage.setItem("tabSessionId", CURRENT_TAB_SESSIONID);
    console.log("Generated new tab ID:", CURRENT_TAB_SESSIONID);
  } else {
    console.log("Using existing tab ID:", CURRENT_TAB_SESSIONID);
  }
  function registerTabIdWithBackground() {
    chrome.runtime.sendMessage({
      type: "registerTabId",
      tabId: CURRENT_TAB_SESSIONID
    }, (response) => {
      if (response && response.success) {
        console.log("Tab ID registered with background script");
      }
    });
  }
  function startHeartbeat() {
    const HEARTBEAT_INTERVAL = 6e4;
    setInterval(() => {
      if (document.visibilityState === "visible") {
        console.log("Sending heartbeat for tab:", CURRENT_TAB_SESSIONID);
        fetch(`${CONFIG.serverUrl}/sessions/${CURRENT_TAB_SESSIONID}/heartbeat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-tab-id": CURRENT_TAB_SESSIONID
          }
        }).catch((err) => {
          console.log("Heartbeat failed:", err);
        });
      }
    }, HEARTBEAT_INTERVAL);
  }
  async function loadExtensionSettings() {
    try {
      const result = await chrome.storage.local.get(["showPasswordValues"]);
      EXTENSION_CONFIG.showPasswordValues = result.showPasswordValues || false;
    } catch (error) {
      console.error("Error loading extension settings:", error);
    }
  }
  function initializeSessionManager() {
    registerTabIdWithBackground();
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", startHeartbeat);
    } else {
      startHeartbeat();
    }
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (message.type === "settingChanged" && message.setting === "showPasswordValues") {
        EXTENSION_CONFIG.showPasswordValues = message.value;
        console.log("Password visibility setting changed:", message.value);
      }
    });
    loadExtensionSettings();
  }

  // modules/utils.js
  async function log(message) {
  }
  function extractBestLabel(label) {
    if (typeof label === "string") {
      return label;
    }
    if (typeof label === "object" && label !== null) {
      const priorities = ["Parent_Label", "Left_Label", "control", "text"];
      for (const key of priorities) {
        if (label[key] && typeof label[key] === "string") {
          return label[key];
        }
      }
      for (const [key, value] of Object.entries(label)) {
        if (typeof value === "string" && value.trim() !== "") {
          return value;
        }
      }
      return JSON.stringify(label);
    }
    return String(label);
  }
  function returnElementPosition(element) {
    if (typeof element.getBoundingClientRect === "function") {
      const rect = element.getBoundingClientRect();
      return {
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX,
        bottom: rect.bottom + window.scrollY,
        right: rect.right + window.scrollX
      };
    }
    if (typeof element?.node?.getBoundingClientRect === "function") {
      const rect = element.node.getBoundingClientRect();
      return {
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX,
        bottom: rect.bottom + window.scrollY,
        right: rect.right + window.scrollX
      };
    }
    return {
      top: -1,
      left: -1,
      bottom: -1,
      right: -1
    };
  }
  function isTextElement(element) {
    const node = typeof element.node === "undefined" ? element : element.node;
    if (node && node.getAttribute && node.getAttribute("contenteditable") === "true") {
      return false;
    }
    return ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"].includes(node.tagName.toLowerCase());
  }
  function isInteractiveElement(element) {
    const node = typeof element.node === "undefined" ? element : element.node;
    if (typeof node.tagName === "undefined") {
      return false;
    }
    if (["a", "button", "input", "select", "textarea", "details", "summary", "dialog"].includes(node.tagName.toLowerCase())) {
      return true;
    }
    if (node && node.getAttribute && node.getAttribute("contenteditable") === "true") {
      return true;
    }
    if (node && node.getAttribute) {
      const role = node.getAttribute("role");
      if (["button", "combobox", "listbox"].includes(role)) {
        return true;
      }
    }
    return false;
  }
  function getEventModifiers(event) {
    return {
      ctrl: event.ctrlKey,
      shift: event.shiftKey,
      alt: event.altKey,
      meta: event.metaKey
    };
  }

  // modules/semantic-controls.js
  var SEMANTIC_CONTROL_DEFINITIONS = [
    {
      id: "INPUT_TEXT",
      visible_state: ["label", "value", "placeholder", "is_focused", "is_disabled"],
      actions: ["type", "clear", "focus", "blur"],
      detection_rules: [
        { tagName: "input", type: "text" },
        { tagName: "input", type: "email" },
        { tagName: "input", type: "url" },
        { tagName: "input", type: "search" },
        { tagName: "input", type: "tel" }
      ]
    },
    {
      id: "INPUT_PASSWORD",
      visible_state: ["label", "is_masked", "is_focused", "is_disabled"],
      actions: ["type", "clear", "focus", "blur", "toggle_visibility"],
      detection_rules: [
        { tagName: "input", type: "password" }
      ]
    },
    {
      id: "INPUT_DROPDOWN",
      visible_state: ["label", "current_value", "available_options", "is_open", "is_disabled"],
      actions: ["open", "close", "select_option", "focus"],
      detection_rules: [
        { tagName: "select" },
        { role: "combobox" },
        { role: "listbox" }
      ]
    },
    {
      id: "INPUT_CHECKBOX",
      visible_state: ["label", "is_checked", "is_disabled"],
      actions: ["toggle", "check", "uncheck"],
      detection_rules: [
        { tagName: "input", type: "checkbox" }
      ]
    },
    {
      id: "INPUT_RADIO",
      visible_state: ["label", "is_selected", "is_disabled", "group_name"],
      actions: ["select"],
      detection_rules: [
        { tagName: "input", type: "radio" }
      ]
    },
    {
      id: "INPUT_TEXTAREA",
      visible_state: ["label", "value", "placeholder", "is_focused", "is_disabled"],
      actions: ["type", "clear", "focus", "blur"],
      detection_rules: [
        { tagName: "textarea" }
      ]
    },
    {
      id: "BUTTON_ACTION",
      visible_state: ["label", "is_disabled", "is_focused"],
      actions: ["click"],
      detection_rules: [
        { tagName: "button", type: "button" },
        { tagName: "input", type: "button" },
        { role: "button" }
      ]
    },
    {
      id: "BUTTON_SUBMIT",
      visible_state: ["label", "is_disabled", "is_focused"],
      actions: ["click", "submit"],
      detection_rules: [
        { tagName: "button", type: "submit" },
        { tagName: "input", type: "submit" }
      ]
    },
    {
      id: "LINK",
      visible_state: ["label", "destination_hint"],
      actions: ["click", "open_new_tab"],
      detection_rules: [
        { tagName: "a", hasHref: true }
      ]
    }
  ];
  function detectSemanticControlType(element) {
    const elementProps = {
      tagName: element.tagName.toLowerCase(),
      type: element.type?.toLowerCase(),
      role: element.getAttribute("role"),
      hasHref: !!element.href
    };
    return SEMANTIC_CONTROL_DEFINITIONS.map((def, index) => ({ def, index })).filter(
      ({ def }) => def.detection_rules.some(
        (rule) => Object.entries(rule).every(
          ([key, value]) => elementProps[key] === value
        )
      )
    ).map(({ index }) => index);
  }
  function getSemanticControlDefinition(index) {
    return SEMANTIC_CONTROL_DEFINITIONS[index] || null;
  }
  function addDropdownSemanticState(element, node) {
    const options = Array.from(node.options || []);
    const selectedOptions = Array.from(node.selectedOptions || []);
    const isMultiSelect = node.multiple || node.type === "select-multiple";
    if (selectedOptions.length === 0) {
      element.current_selection = "(none selected)";
      element.current_value = isMultiSelect ? [] : null;
    } else if (selectedOptions.length === 1) {
      element.current_selection = selectedOptions[0].text;
      element.current_value = isMultiSelect ? [selectedOptions[0].value] : selectedOptions[0].value;
    } else {
      element.current_selection = selectedOptions.map((opt) => opt.text);
      element.current_value = selectedOptions.map((opt) => opt.value);
    }
    element.clickable_options = options.filter((opt) => opt.value !== "").map((opt) => `"${opt.text}" \u2192 ${opt.value}`);
    element.is_open = node.matches(":focus") && node.size > 1;
    element.is_disabled = node.disabled || false;
  }
  function addPasswordSemanticState(element, node) {
    element.is_focused = document.activeElement === node;
    element.is_disabled = node.disabled || false;
    if (EXTENSION_CONFIG.showPasswordValues) {
      element.value = node.value || "";
      element.is_masked = false;
    } else {
      element.is_masked = true;
    }
  }
  function addLinkSemanticState(element, node) {
    element.destination_hint = node.href || null;
  }
  function addGenericSemanticState(element, node) {
    element.value = "value" in node ? node.value : null;
    element.placeholder = node.placeholder || null;
    element.is_focused = document.activeElement === node;
    element.is_disabled = node.disabled || false;
    if (node.type === "checkbox" || node.type === "radio") {
      element.checked = node.checked;
    }
    if (node.tagName === "SELECT") {
      element.selectedOptions = Array.from(node.selectedOptions || []);
      element.multiple = node.multiple;
      element.selectedIndex = node.selectedIndex;
    }
  }
  function buildSemanticElement(node, semanticDef, positionData, existingLabel = null) {
    const element = {};
    element.label = existingLabel;
    element.control_type = semanticDef.id;
    element.tagName = node.tagName?.toLowerCase();
    element.type = node.type?.toLowerCase();
    switch (semanticDef.id) {
      case "INPUT_DROPDOWN":
        addDropdownSemanticState(element, node);
        break;
      case "INPUT_PASSWORD":
        addPasswordSemanticState(element, node);
        break;
      case "LINK":
        addLinkSemanticState(element, node);
        break;
      default:
        addGenericSemanticState(element, node);
        break;
    }
    if (node.href) {
      element.href = node.href;
    }
    element.top = positionData.top;
    element.left = positionData.left;
    element.bottom = positionData.bottom;
    element.right = positionData.right;
    element.node = node;
    return element;
  }

  // modules/labeling.js
  function addLabel(element, elements) {
    let labels = element?.labels ? element.labels : {};
    if (element.tagName.toLowerCase() === "button") {
      element.label = element.node.textContent.trim();
    } else if (element.tagName.toLowerCase() === "input" && element.node.type === "button") {
      element.label = element.node.value || "";
    } else if (element.node.getAttribute && element.node.getAttribute("role") === "button") {
      element.label = element.node.textContent.trim();
    }
    if (element.tagName.toLowerCase() === "a") {
      element.label = element.node.textContent.trim();
      if (element.label === "") {
        let text = "";
        element.node.childNodes.forEach((node) => {
          text += node.alt || node.textContent;
        });
        if (text !== "") {
          element.label = text.trim();
        }
      }
    }
    if (!element.label && element.node.id) {
      const label = document.querySelector(`label[for="${element.node.id}"]`);
      if (label) {
        element.label = label.textContent.trim();
      }
    }
    if (!element.label && typeof element.node.closest === "function") {
      const parentLabel = element.node.closest("label");
      if (parentLabel) {
        labels.Parent_Label = parentLabel.textContent.trim();
      }
    }
    if (!element.label) {
      let prev = null;
      for (const el of elements) {
        const el_midpoint = (el.top + el.bottom) / 2;
        if (el_midpoint > element.top && el_midpoint > element.bottom && el.right < element.left) {
        } else {
          if (el === element) {
            if (prev && isTextElement(prev)) {
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

  // modules/screen-capture.js
  var previousScreen = null;
  function returnElementProperties(element) {
    const node = typeof element.node === "undefined" ? element : element.node;
    const positionData = returnElementPosition(element);
    let existingLabel = null;
    if (previousScreen) {
      previousScreen.visible_elements.forEach((screenElement) => {
        if (screenElement.node && screenElement.node.id === node.id) {
          existingLabel = screenElement.label;
        }
      });
    }
    if (isInteractiveElement(node)) {
      const semanticIndexes = detectSemanticControlType(node);
      if (semanticIndexes.length > 1) {
        const matchedTypes = semanticIndexes.map((i) => getSemanticControlDefinition(i).id);
        console.warn(`Multiple semantic control matches for ${node.tagName}[type="${node.type}"][id="${node.id}"]: ${matchedTypes.join(", ")} - using first match`);
      }
      if (semanticIndexes.length > 0) {
        const semanticDef = getSemanticControlDefinition(semanticIndexes[0]);
        return buildSemanticElement(node, semanticDef, positionData, existingLabel);
      }
    }
    const elem = {
      label: existingLabel,
      tagName: node.tagName?.toLowerCase(),
      textContent: null,
      top: positionData.top,
      left: positionData.left,
      bottom: positionData.bottom,
      right: positionData.right,
      has_focus: document.activeElement === node,
      node
    };
    if (node.href) {
      elem.href = node.href;
    }
    if (!isInteractiveElement(node)) {
      elem.textContent = node?.textContent?.trim();
    }
    if (node?.href) {
      elem.href = node.href;
    }
    return elem;
  }
  function collectAllVisibleElements() {
    const elements = [];
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
      {
        acceptNode: function(node) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const style = window.getComputedStyle(node);
            if (style.display === "none" || style.visibility === "hidden") {
              return NodeFilter.FILTER_REJECT;
            }
          }
          if (typeof node.tagName === "undefined") {
            return NodeFilter.FILTER_REJECT;
          }
          if (node.nodeType === Node.TEXT_NODE && (!node.nodeValue || /^[\s\r\n\t]*$/.test(node.nodeValue))) {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );
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
    return allNodes.map((node) => {
      const isText = node.nodeType === Node.TEXT_NODE;
      const element = isText ? node.parentElement : node;
      let result = {
        ...isText ? {} : { label: "" },
        tagName: element.tagName?.toLowerCase(),
        ...isInteractiveElement(element) && element.tagName?.toLowerCase() === "a" ? { href: "" } : {},
        ...isInteractiveElement(element) && element.tagName?.toLowerCase() !== "a" ? { type: "" } : {},
        ...isText ? { textContent: "" } : {},
        ...returnElementPosition(element)
      };
      if (isText && isTextElement(result)) {
        result.textContent = node.textContent.trim();
      }
      if (!isText && isInteractiveElement(node)) {
        result = returnElementProperties(element);
      }
      result.node = node;
      return result;
    }).sort((a, b) => a.top - b.top || a.left - b.left);
  }
  function getCurrentScreen() {
    const screen = {
      type: "screen_status",
      url: window.location.href,
      focus_label: null,
      visible_elements: collectAllVisibleElements()
    };
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
  function updatePreviousScreen(screen) {
    previousScreen = screen;
  }

  // modules/events.js
  var eventQueue = [];
  var sendingInProgress = false;
  var changeDetectionTimer = null;
  var inProcessKeyboard = null;
  function flushPendingKeyboard() {
    if (inProcessKeyboard) {
      const targetElement = document.getElementById(inProcessKeyboard.targetId) || document.querySelector(`[id="${inProcessKeyboard.targetId}"]`) || document.activeElement;
      if (targetElement) {
        let finalValue = targetElement.value || "";
        if (targetElement.type === "password" && !EXTENSION_CONFIG.showPasswordValues) {
        } else {
          inProcessKeyboard.target.value = { text: finalValue };
        }
      }
      const eventToSend = { ...inProcessKeyboard };
      delete eventToSend.targetId;
      sendEvent("keyboard", eventToSend);
      inProcessKeyboard = null;
    }
  }
  async function sendEvent(kind, data) {
    const orderedEvent = {
      type: kind,
      // Primary event details first
      ...data.event && { event: data.event },
      ...data.url && { url: data.url },
      ...data.button !== void 0 && { button: data.button },
      ...data.buttons !== void 0 && { buttons: data.buttons },
      ...data.key && { key: data.key },
      ...data.code && { code: data.code },
      ...data.x !== void 0 && { x: data.x },
      ...data.y !== void 0 && { y: data.y },
      // All other data fields (including target, visible_elements, etc.)
      ...Object.fromEntries(
        Object.entries(data).filter(
          ([key]) => !["event", "url", "button", "buttons", "key", "code", "x", "y"].includes(key)
        )
      )
    };
    if (window.actorExecuting) {
      orderedEvent.source = "actor";
      window.actorExecuting = false;
    }
    eventQueue.push(orderedEvent);
    if (kind !== "screen_status") {
      scheduleChangeDetection();
    }
    processSendQueue();
  }
  function scheduleChangeDetection() {
    if (changeDetectionTimer) {
      clearTimeout(changeDetectionTimer);
    }
    changeDetectionTimer = setTimeout(() => {
      flushPendingKeyboard();
      const screen = getCurrentScreen();
      sendEvent("screen_status", screen);
      updatePreviousScreen(screen);
      changeDetectionTimer = null;
    }, STABLE_SCREEN_DELAY);
  }
  function processSendQueue() {
    if (sendingInProgress || eventQueue.length === 0) {
      return;
    }
    sendingInProgress = true;
    while (eventQueue.length > 0) {
      const event = eventQueue.shift();
      actuallySendEvent(event);
    }
    sendingInProgress = false;
  }
  function cleanEventForSending(event_) {
    const cleanEvent = JSON.parse(JSON.stringify(event_, (key, value) => {
      if (key === "node") {
        return void 0;
      }
      if (["top", "left", "bottom", "right"].includes(key)) {
        return void 0;
      }
      return value;
    }));
    if (cleanEvent.visible_elements && Array.isArray(cleanEvent.visible_elements)) {
      cleanEvent.visible_elements = cleanEvent.visible_elements.map((element) => {
        const cleanElement = { ...element };
        delete cleanElement.top;
        delete cleanElement.left;
        delete cleanElement.bottom;
        delete cleanElement.right;
        if (cleanElement.destination_hint === cleanElement.href) {
          delete cleanElement.destination_hint;
        }
        if (cleanElement.control_type && cleanElement.control_type !== "UNKNOWN") {
          delete cleanElement.tagName;
        }
        if (cleanElement.control_type === "INPUT_PASSWORD") {
          cleanElement.showPasswordValues = EXTENSION_CONFIG.showPasswordValues;
        } else {
          delete cleanElement.showPasswordValues;
        }
        return cleanElement;
      });
    }
    return cleanEvent;
  }
  async function actuallySendEvent(event_) {
    const cleanEvent = cleanEventForSending(event_);
    try {
      console.log(`actuallySendEvent session:${CURRENT_TAB_SESSIONID} event:${event_.type} data:${JSON.stringify(cleanEvent)}`);
      const response = await fetch(`${CONFIG.serverUrl}/sessions/${CURRENT_TAB_SESSIONID}/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Tab-ID": CURRENT_TAB_SESSIONID
        },
        body: JSON.stringify(cleanEvent)
      });
      if (!response.ok) {
        throw new Error(`sendEvent: Server responded with status: ${response.status}`);
      }
    } catch (error) {
      log(`sendEvent: Failed to send event ${event_.type} to server, trying fallback: ${error.message} 
 ${error.stack}`);
    }
  }
  function buildDropdownTarget(node, event, target, context) {
    const selectedOptions = Array.from(node.selectedOptions);
    const valueDict = {};
    selectedOptions.forEach((option) => {
      valueDict[option.text] = option.value;
    });
    const result = {
      label: node.labels?.[0]?.textContent?.trim() || extractBestLabel(target.label) || node.name || node.getAttribute("aria-label") || `select#${node.id || "unlabeled"}`,
      value: valueDict,
      event_state: {
        modifiers: getEventModifiers(event)
      }
    };
    if (context === "mouse") {
      const clickedOption = event.target.tagName === "OPTION" ? event.target.text : null;
      result.event_state.clicked_option = clickedOption;
    }
    return result;
  }
  function buildRadioTarget(node, event, target) {
    const radioLabel = node.labels?.[0]?.textContent?.trim() || extractBestLabel(target.label) || node.value || `radio[${node.name || "unnamed"}]`;
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
  function buildCheckboxTarget(node, event) {
    const checkboxLabel = node.labels?.[0]?.textContent?.trim() || node.name || node.getAttribute("aria-label") || `checkbox#${node.id || "unlabeled"}`;
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
  function buildTextInputTarget(node, event, target) {
    const inputLabel = node.labels?.[0]?.textContent?.trim() || extractBestLabel(target.label) || node.placeholder || node.name || node.getAttribute("aria-label") || `${node.type || "input"}#${node.id || "unlabeled"}`;
    let fieldValue = node.value || "";
    const valueDict = {};
    if (node.type === "password" && !EXTENSION_CONFIG.showPasswordValues) {
    } else {
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
  function buildOptionTarget(node, event) {
    const selectElement = node.closest("select");
    const selectLabel = selectElement?.labels?.[0]?.textContent?.trim() || "Dropdown";
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
  function buildStructuredTarget(node, event, target, context) {
    try {
      if (node.tagName === "SELECT" && node.selectedOptions.length > 0) {
        return buildDropdownTarget(node, event, target, context);
      }
      if (node.type === "radio" && node.name) {
        return buildRadioTarget(node, event, target);
      }
      if (node.type === "checkbox") {
        return buildCheckboxTarget(node, event);
      }
      if (node.tagName === "INPUT" || node.tagName === "TEXTAREA") {
        return buildTextInputTarget(node, event, target);
      }
      if (node.tagName === "OPTION") {
        return buildOptionTarget(node, event);
      }
      if (node.tagName === "A" || node.href) {
        const linkLabel = target.label || node.textContent?.trim() || node.getAttribute("aria-label") || node.title || node.href || "link";
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
      if (node.tagName && (node.onclick || node.href || node.type || isInteractiveElement(node))) {
        log(`Unknown control type detected: ${node.tagName}[type="${node.type}"] - generating basic event`);
        return {
          label: target.label || node.textContent?.trim() || node.tagName || "Unknown Control",
          control_type: "UNKNOWN",
          tagName: node.tagName,
          // Keep tagName for unknown controls to help with debugging
          ...node.type && { type: node.type },
          ...node.href && { href: node.href },
          value: {}
          // Empty value object for unknown controls
        };
      }
      return null;
    } catch (error) {
      log(`Error building structured target for ${node?.tagName}: ${error.message}`);
      return {
        label: "Error Building Target",
        control_type: "UNKNOWN",
        error: error.message,
        value: {}
      };
    }
  }
  function createFallbackTarget(target, event) {
    if (target?.label) {
      const labelText = extractBestLabel(target.label) || target.label || event?.target?.textContent?.trim() || event?.target?.placeholder || event?.target?.getAttribute("aria-label") || `${event?.target?.tagName?.toLowerCase() || "element"}[${event?.target?.type || "unknown"}]`;
      return {
        label: labelText,
        value: {}
      };
    }
    if (!target && event?.target) {
      return {
        label: event.target.textContent?.trim().substring(0, 50) || event.target.placeholder || `${event.target.tagName?.toLowerCase() || "element"}#${event.target.id || "unlabeled"}`,
        value: {}
      };
    }
    if (target && typeof target === "object") {
      const labelText = target.label || event?.target?.textContent?.trim() || `${event?.target?.tagName?.toLowerCase() || "element"}[${event?.target?.type || "unknown"}]`;
      return {
        label: labelText,
        value: {}
      };
    }
    return {
      label: "unknown",
      value: {}
    };
  }
  function returnKeyboardEventProperties(event) {
    const target = returnElementProperties(event.target);
    let structuredTarget = null;
    if (event.target) {
      const node = event.target;
      const isControlKeyInteraction = node.tagName === "SELECT" && (event.key === "Enter" || event.key === " ") || node.type === "radio" && (event.key.startsWith("Arrow") || event.key === " ") || node.type === "checkbox" && event.key === " " || (node.tagName === "INPUT" || node.tagName === "TEXTAREA");
      if (isControlKeyInteraction) {
        structuredTarget = buildStructuredTarget(node, event, target, "keyboard");
        if (structuredTarget && !target.label && node.id) {
          sendEvent("log", {
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
    let minimalTarget = null;
    if (structuredTarget) {
      const labelText = structuredTarget.label || target && extractBestLabel(target.label) || event.target?.textContent?.trim() || event.target?.placeholder || `${event.target?.tagName?.toLowerCase() || "element"}[${event.target?.type || "unknown"}]`;
      const valueDict = structuredTarget.value && typeof structuredTarget.value === "object" ? structuredTarget.value : {};
      minimalTarget = {
        label: labelText,
        value: valueDict
      };
    }
    return {
      tagName: event.tagName,
      target: minimalTarget || createFallbackTarget(target, event),
      key: event.key,
      code: event.code
    };
  }
  function resolveEventTarget(event) {
    let targetElement = event.target;
    if (event.target && event.target.tagName === "OPTION") {
      targetElement = event.target.closest("select");
    }
    return targetElement;
  }
  function findMatchingScreenElement(targetElement) {
    const currentScreen = getCurrentScreen();
    return currentScreen.visible_elements.find(
      (element) => element.node === targetElement
    ) || null;
  }
  function buildMatchingEventProperties(event, matchingElement, targetElement) {
    log(`Mouse click: Found matching element with label "${matchingElement.label}" for ${targetElement.tagName}[id="${targetElement.id}"]`);
    const structuredTarget = buildStructuredTarget(targetElement, event, { label: matchingElement.label }, "mouse");
    const labelText = structuredTarget && structuredTarget.label || matchingElement.label || targetElement.textContent?.trim() || targetElement.getAttribute("aria-label") || targetElement.placeholder || targetElement.tagName || "Unknown Control";
    const valueDict = structuredTarget && structuredTarget.value && typeof structuredTarget.value === "object" ? structuredTarget.value : {};
    const target = {
      label: labelText,
      value: valueDict
    };
    return {
      event: event.type,
      target,
      button: event.button || 0,
      buttons: event.buttons || 0
    };
  }
  function buildFallbackEventProperties(event, targetElement) {
    log(`Mouse click: No matching element found for ${targetElement.tagName}[id="${targetElement.id}"] - element not in visible list`);
    const fallbackLabel = targetElement.textContent?.trim() || targetElement.getAttribute("aria-label") || targetElement.placeholder || targetElement.tagName;
    const structuredTarget = buildStructuredTarget(targetElement, event, { label: fallbackLabel }, "mouse");
    const labelText = structuredTarget && structuredTarget.label || fallbackLabel || "Unknown Control";
    const valueDict = structuredTarget && structuredTarget.value && typeof structuredTarget.value === "object" ? structuredTarget.value : {};
    return {
      event: event.type,
      target: {
        label: labelText,
        value: valueDict
      },
      button: event.button || 0,
      buttons: event.buttons || 0
    };
  }
  function buildErrorEventProperties(event, targetElement) {
    return {
      event: "click",
      target: {
        label: "unknown",
        value: {}
      },
      y: event.clientY || 0,
      x: event.clientX || 0,
      button: event.button || 0,
      buttons: event.buttons || 0
    };
  }
  function getMouseEventProperties(event) {
    try {
      const targetElement = resolveEventTarget(event);
      const matchingElement = findMatchingScreenElement(targetElement);
      if (matchingElement) {
        return buildMatchingEventProperties(event, matchingElement, targetElement);
      } else {
        return buildFallbackEventProperties(event, targetElement);
      }
    } catch (error) {
      console.error("Error in getMouseEventProperties:", error);
      return buildErrorEventProperties(event, event.target);
    }
  }
  function initializeEventListeners() {
    window.addEventListener("load", (event) => {
      flushPendingKeyboard();
      registerSession();
      sendEvent("event", {
        event: "load",
        url: window.location.href
      });
    });
    try {
      document.addEventListener("click", (event) => {
        if (event.clientX === 100 && event.clientY === 100) {
          return;
        }
        flushPendingKeyboard();
        queueMicrotask(() => {
          try {
            const mouseProps = getMouseEventProperties(event);
            sendEvent("mouse", {
              event: "click",
              ...mouseProps
            });
            log(`Mouse click processed: ${event.target.tagName}`);
          } catch (error) {
            log(`Mouse click error: ${error.message}
${error.stack}`);
            sendEvent("mouse", {
              event: "click",
              target: {
                label: event.target.textContent?.trim().substring(0, 50) || event.target.tagName || "unknown"
              },
              button: event.button,
              error: error.message
            });
          }
        });
      });
    } catch (error) {
      log(`Error attaching click listener: ${error.message}`);
      sendEvent("log", { message: `Error attaching click listener: ${error.message}` });
    }
    document.addEventListener("keydown", (event) => {
      const currentTarget = event.target;
      const isTextInput = currentTarget.tagName === "INPUT" && (currentTarget.type === "text" || currentTarget.type === "email" || currentTarget.type === "search" || currentTarget.type === "url" || currentTarget.type === "tel" || currentTarget.type === "password") || currentTarget.tagName === "TEXTAREA";
      const isControlKey = event.key === "Enter" || !isTextInput && event.key === " " || event.key && event.key.startsWith("Arrow") || event.key === "Tab";
      const isModifierKey = event.key === "Shift" || event.key === "Control" || event.key === "Alt" || event.key === "Meta";
      if (isControlKey && isInteractiveElement(currentTarget)) {
        flushPendingKeyboard();
        queueMicrotask(() => {
          sendEvent("keyboard", {
            event: "control_key",
            ...returnKeyboardEventProperties(event)
          });
        });
      } else if (isTextInput && !isModifierKey) {
        const currentTargetInfo = returnElementProperties(currentTarget);
        if (!inProcessKeyboard || inProcessKeyboard.targetId !== (currentTargetInfo.id || currentTarget.id)) {
          flushPendingKeyboard();
          inProcessKeyboard = {
            event: "text_input",
            targetId: currentTargetInfo.id || currentTarget.id || "",
            // Store ID for comparison
            target: {
              label: currentTarget.labels?.[0]?.textContent?.trim() || extractBestLabel(currentTargetInfo.label) || currentTarget.placeholder || currentTarget.name || currentTarget.getAttribute("aria-label") || `${currentTarget.type || "input"}#${currentTarget.id || "unlabeled"}`,
              value: {}
              // Will be set to unified dictionary format at flush time
            }
          };
        }
      }
    });
    document.addEventListener("blur", (event) => {
      if (inProcessKeyboard) {
        flushPendingKeyboard();
      }
    }, true);
    document.addEventListener("submit", (event) => {
      flushPendingKeyboard();
      sendEvent("button", {
        event: "submit",
        isSubmit: true,
        ...event
      });
    });
    window.addEventListener("beforeunload", (event) => {
      flushPendingKeyboard();
    });
    window.addEventListener("pagehide", (event) => {
      flushPendingKeyboard();
    });
  }
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
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-Tab-ID": CURRENT_TAB_SESSIONID
        },
        body: JSON.stringify(tabIdentity)
      });
      if (response.ok) {
        const result = await response.json();
        console.log("Session registered successfully:", result.sessionId);
      } else {
        console.log("Failed to register session:", response.status);
      }
    } catch (error) {
      console.log("Error registering session (server likely offline):", error.message);
    }
  }

  // modules/actor.js
  var isExecutingActorCommand = false;
  var inProcessKeyboard2 = null;
  function isSafeToExecuteActor() {
    if (inProcessKeyboard2) {
      return false;
    }
    if (isExecutingActorCommand) {
      return false;
    }
    return true;
  }
  async function pollForActorCommands() {
    while (true) {
      try {
        const pollUrl = `${CONFIG.serverUrl}/sessions/${CURRENT_TAB_SESSIONID}/actor/commands`;
        const response = await fetch(pollUrl, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-Tab-ID": CURRENT_TAB_SESSIONID
          }
        });
        if (response.ok) {
          const commands = await response.json();
          if (commands.length > 0) {
            for (const command of commands) {
              console.log(`\u{1F3AF} POLLING DEBUG: Processing command: ${command.type} with data:`, command);
              await processActorCommandWhenSafe(command);
            }
          }
        } else {
          console.warn(`Actor Channel: Poll failed with status ${response.status}`);
        }
      } catch (error) {
        if (error.message && !error.message.includes("fetch")) {
          console.warn("Actor polling error:", error.message);
        }
      }
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }
  async function processActorCommandWhenSafe(command) {
    const maxWaitTime = 5e3;
    const startTime = Date.now();
    console.log(`Actor Channel: Waiting for safe execution of command ${command.id}`);
    while (!isSafeToExecuteActor() && Date.now() - startTime < maxWaitTime) {
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
    if (!isSafeToExecuteActor()) {
      log(`Actor Channel: Timeout waiting for safe execution of command ${command.id}`);
      return;
    }
    isExecutingActorCommand = true;
    try {
      try {
        log(`Actor Channel: Executing command ${command.id}: ${command.type}`);
      } catch (e) {
      }
      console.log(`Actor Channel: Executing command ${command.id}: ${command.type}`);
      await executeActorCommand(command);
    } catch (error) {
      try {
        log(`Actor Channel: Error executing command ${command.id}: ${error.message}`);
      } catch (e) {
      }
    } finally {
      isExecutingActorCommand = false;
    }
  }
  function findTargetElement(targetSpec) {
    if (!targetSpec || !targetSpec.label) {
      throw new Error("Actor: Target specification missing or invalid");
    }
    let control, control_id;
    if (typeof targetSpec.label === "object" && targetSpec.label.control) {
      control = targetSpec.label.control;
      control_id = targetSpec.label.control_id;
    } else {
      control = targetSpec.label;
      control_id = targetSpec.id;
    }
    const currentScreen = getCurrentScreen();
    const screenElement = currentScreen.visible_elements.find((element) => {
      return element.label && element.label.toLowerCase() === control.toLowerCase();
    });
    if (!screenElement) {
      const availableLabels = currentScreen.visible_elements.map((el) => el.label || "unlabeled").slice(0, 10);
      log(`Actor: No element found with exact label "${control}". Available labels: ${availableLabels.join(", ")}`);
      throw new Error(`Actor: No element found with label "${control}" in current screen`);
    }
    const allMatches = currentScreen.visible_elements.filter((element) => {
      return element.label && element.label.toLowerCase() === control.toLowerCase();
    });
    if (allMatches.length > 1) {
      log(`Actor: WARNING - Multiple elements (${allMatches.length}) found with label "${control}". Using first match. Consider improving label uniqueness.`);
    }
    let foundElement = screenElement.node;
    let matchMethod = "exact_label_match";
    if (control_id && foundElement && foundElement.id !== control_id) {
      log(`Actor: WARNING - Label-based match found but ID mismatch. Expected: "${control_id}", Found: "${foundElement.id}"`);
      log(`Actor: This might indicate screen changes or labeling inconsistencies`);
    }
    if (foundElement) {
      log(`Actor: Found target element via ${matchMethod} - ${foundElement.tagName}[id="${foundElement.id}"] with label "${screenElement.label}"`);
    } else {
      log(`Actor: WARNING - screenElement.node is null for label "${screenElement.label}". This indicates an architectural issue.`);
    }
    return {
      element: foundElement,
      screenElement,
      // Include the full screen element data
      matchMethod,
      validated: !control_id || foundElement && foundElement.id === control_id
    };
  }
  function setElementValue(element, newValue, controlType) {
    const tagName = element.tagName.toLowerCase();
    const inputType = element.type?.toLowerCase();
    try {
      switch (tagName) {
        case "input":
          if (inputType === "checkbox" || inputType === "radio") {
            const shouldCheck = newValue === true || newValue === "checked" || newValue === "true";
            element.checked = shouldCheck;
            try {
              log(`Actor: Set ${inputType} to ${shouldCheck ? "checked" : "unchecked"}`);
            } catch (e) {
            }
          } else {
            if (newValue === void 0 || newValue === null) {
              element.value = "";
            } else {
              element.value = newValue;
            }
            try {
              log(`Actor: Set input value to "${element.value}"`);
            } catch (e) {
            }
          }
          break;
        case "select":
          const options = Array.from(element.options);
          let targetOption = null;
          targetOption = options.find((opt) => opt.value === newValue) || options.find((opt) => opt.text === newValue);
          if (targetOption) {
            element.selectedIndex = targetOption.index;
            try {
              log(`Actor: Set select to option "${targetOption.text}" (value: "${targetOption.value}")`);
            } catch (e) {
            }
          } else {
            throw new Error(`Actor: Could not find option "${newValue}" in dropdown`);
          }
          break;
        case "textarea":
          if (newValue === void 0 || newValue === null) {
            element.value = "";
          } else {
            element.value = newValue;
          }
          try {
            log(`Actor: Set textarea value to "${element.value}"`);
          } catch (e) {
          }
          break;
        default:
          try {
            log(`Actor: No value to set for ${tagName} element`);
          } catch (e) {
          }
      }
      return true;
    } catch (error) {
      try {
        log(`Actor: Error setting value on ${tagName}: ${error.message}`);
      } catch (e) {
      }
      throw error;
    }
  }
  async function executeActorCommand(command) {
    console.log(`\u{1F680} EXECUTE ENTRY: executeActorCommand called with command type: "${command.type}"`);
    log(`Actor Channel: Executing ${command.type} command`);
    window.actorExecuting = true;
    console.log(`\u{1F680} ACTOR FLAG SET: ${command.type} - actorExecuting=true`);
    try {
      log(`Actor Channel: Setting actorExecuting flag for command: ${command.type}`);
    } catch (e) {
    }
    try {
      console.log(`\u{1F50D} EXECUTE DEBUG: About to switch on command type: "${command.type}"`);
      switch (command.type) {
        case "screen_status":
          log(`Actor Channel: Ignoring screen_status command (browser will generate own reports)`);
          break;
        case "test_actor_channel":
          log(`Actor Channel: Test command received: ${command.data.message}`);
          break;
        case "mouse":
          try {
            const target = findTargetElement(command.target);
            log(`Actor Channel: Clicking element ${target.element.tagName}[id="${target.element.id}"]`);
            if (command.target?.value && typeof command.target.value === "object") {
              const element = target.element;
              const tagName = element.tagName.toLowerCase();
              if (tagName === "select") {
                const targetValues = Object.values(command.target.value);
                Array.from(element.options).forEach((option) => {
                  option.selected = targetValues.includes(option.value);
                });
                element.dispatchEvent(new Event("change", { bubbles: true }));
              } else if (element.type === "checkbox" || element.type === "radio") {
                const values = Object.values(command.target.value);
                element.checked = values.includes(true);
                element.dispatchEvent(new Event("change", { bubbles: true }));
              }
            }
            target.element.click();
          } catch (error) {
            log(`Actor Channel: Mouse click failed: ${error.message}`);
          }
          break;
        case "keyboard":
          try {
            console.log(`\u{1F50D} KEYBOARD DEBUG: Processing keyboard command with data:`, command.data);
            console.log(`\u{1F50D} KEYBOARD DEBUG: Target specification:`, command.target);
            const target = findTargetElement(command.target);
            console.log(`\u{1F50D} KEYBOARD DEBUG: Found target element:`, target.element.tagName, target.element.type, target.element.id);
            const valueObj = command.target?.value;
            if (!valueObj || typeof valueObj !== "object") {
              throw new Error(`Invalid keyboard command: target.value must be an object, got: ${JSON.stringify(valueObj)}`);
            }
            target.element.focus();
            console.log(`\u{1F50D} KEYBOARD DEBUG: Before setting value, current value: "${target.element.value}"`);
            let newValue = "";
            if (target.element.tagName === "SELECT") {
              const selectedInternalValues = Object.values(valueObj);
              if (target.element.multiple) {
                Array.from(target.element.options).forEach((option) => {
                  option.selected = selectedInternalValues.includes(option.value);
                });
                newValue = selectedInternalValues.join(",");
                console.log(`\u{1F50D} KEYBOARD DEBUG: Multi-select set to values: [${selectedInternalValues.join(", ")}]`);
              } else {
                const chosen = selectedInternalValues[0] ?? "";
                target.element.value = chosen;
                Array.from(target.element.options).forEach((option) => {
                  option.selected = option.value === chosen;
                });
                newValue = chosen;
                console.log(`\u{1F50D} KEYBOARD DEBUG: Single select set to value: "${chosen}"`);
              }
            } else if (target.element.type === "checkbox" || target.element.type === "radio") {
              const boolVal = Object.values(valueObj).find((v) => typeof v === "boolean");
              const shouldCheck = !!boolVal;
              target.element.checked = shouldCheck;
              newValue = shouldCheck ? "true" : "false";
              console.log(`\u{1F50D} KEYBOARD DEBUG: ${target.element.type} set to checked: ${shouldCheck}`);
            } else {
              if (!Object.prototype.hasOwnProperty.call(valueObj, "text")) {
                throw new Error(`Invalid keyboard command format for text control: expected { text: "..." }, got: ${JSON.stringify(valueObj)}`);
              }
              newValue = valueObj.text;
              target.element.value = newValue;
              console.log(`\u{1F50D} KEYBOARD DEBUG: After setting value, current value: "${target.element.value}"`);
            }
            target.element.dispatchEvent(new Event("input", { bubbles: true }));
            target.element.dispatchEvent(new Event("change", { bubbles: true }));
            log(`Actor Channel: Set value "${newValue}" in ${target.element.tagName}[id="${target.element.id}"]`);
            let echoValue;
            const labelForEcho = target.screenElement && target.screenElement.label || target.element.labels && target.element.labels[0] && target.element.labels[0].textContent && target.element.labels[0].textContent.trim() || target.element.getAttribute("aria-label") || target.element.placeholder || target.element.name || `${target.element.type || target.element.tagName.toLowerCase()}#${target.element.id || "unlabeled"}`;
            if (target.element.tagName === "SELECT") {
              const selectedOpts = Array.from(target.element.selectedOptions || []);
              const dict = {};
              selectedOpts.forEach((opt) => {
                dict[opt.text] = opt.value;
              });
              echoValue = dict;
            } else if (target.element.type === "checkbox" || target.element.type === "radio") {
              const dict = {};
              dict[labelForEcho] = target.element.checked;
              echoValue = dict;
            } else {
              echoValue = { text: newValue };
            }
            sendEvent("keyboard", {
              event: "text_input",
              target: {
                label: labelForEcho,
                ...echoValue && Object.keys(echoValue).length ? { value: echoValue } : {}
              }
            });
            scheduleChangeDetection();
          } catch (error) {
            log(`Actor Channel: Keyboard input failed: ${error.message}`);
          }
          break;
        case "set_value":
          try {
            const target = findTargetElement(command.target);
            const newValue = command.data?.value;
            setElementValue(target.element, newValue);
            target.element.dispatchEvent(new Event("change", { bubbles: true }));
            log(`Actor Channel: Set value "${newValue}" on ${target.element.tagName}[id="${target.element.id}"]`);
          } catch (error) {
            log(`Actor Channel: Set value failed: ${error.message}`);
          }
          break;
        case "load":
          try {
            const targetUrl = command.target?.url;
            if (!targetUrl) {
              throw new Error("Load command requires target.url");
            }
            log(`Actor Channel: Navigating to URL: ${targetUrl}`);
            window.location.href = targetUrl;
          } catch (error) {
            log(`Actor Channel: Load navigation failed: ${error.message}`);
          }
          break;
        default:
          console.log(`\u{1F50D} EXECUTE DEBUG: UNRECOGNIZED command type: "${command.type}"`);
          try {
            log(`Actor Channel: Unrecognized command type: ${command.type}`);
          } catch (e) {
          }
      }
    } finally {
      log(`Actor Channel: Command execution complete`);
    }
  }
  function initializeActorChannel() {
    log("Actor Channel: Initializing Actor command polling");
    pollForActorCommands().catch((error) => {
      log(`Actor Channel: Polling loop crashed: ${error.message}`);
    });
  }

  // content.entry.js
  window.addEventListener("error", (event) => {
    log(`window.addEventListener.error: === UNCAUGHT EXCEPTION ===
	${event.error.message}
${event.error.stack}`);
  });
  async function initializeExtension() {
    try {
      console.log("AI Browser Extension: Initializing...");
      initializeSessionManager();
      console.log("\u2713 Session manager initialized");
      initializeEventListeners();
      console.log("\u2713 Event listeners initialized");
      initializeActorChannel();
      console.log("\u2713 Actor channel initialized");
      const initialScreen = getCurrentScreen();
      sendEvent("screen_status", initialScreen);
      console.log("\u2713 Initial screen status sent");
      console.log(`AI Browser Extension: Initialized successfully for tab ${CURRENT_TAB_SESSIONID}`);
    } catch (error) {
      console.error("AI Browser Extension: Initialization failed:", error);
      log(`Extension initialization error: ${error.message}
${error.stack}`);
    }
  }
  initializeExtension();
  log("CONTENT SCRIPT VERSION 2025-11-26-MODULAR LOADED");
  console.log("\u{1F680} AI Browser Extension: Content script loaded (modular version)");
})();

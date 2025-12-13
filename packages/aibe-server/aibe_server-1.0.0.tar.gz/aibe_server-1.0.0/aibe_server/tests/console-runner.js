/**
 * Data-Driven Element Tests - Pure configuration approach
 * 
 * Demonstrates how element tests can be defined as pure data
 * and executed generically without procedural code.
 * 
 * PREREQUISITES:
 * 1. AIBE server needs to be running (start via server.bat)
 * 2. Chrome browser needs to be open to a localhost:3001 page (e.g., http://localhost:3001/status)
 * 
 * USAGE:
 * cd server/aibe_server/tests
 * node console-runner.js
 * 
 * NOTE:
 * - Results are streamed to console
 * - Takes a couple of minutes, let it run to completion!
 */

// Test configuration - pure data, no code
const TEST_SUITES = {
    "basic_inputs": {
        description: "Basic form input testing",
        setup: {
            url: "http://localhost:3001/test-inputs",
            delay: 100
        },
        tests: [
            { element: "Username", setValue: "data_driven_user", expect: "data_driven_user", description: "Username field basic input" },
            { element: "Email Address", setValue: "user@test.com", expect: "user@test.com", description: "Email field validation" },
            // Passwords return null when they are masked
            { element: "Password", setValue: "secure123", expect: null, description: "Password masking behavior" },
        ]
    },

    "form_states": {
        description: "Form state management testing",
        setup: {
            url: "http://localhost:3001/test-inputs",
            delay: 100
        },
        tests: [
            { element: "Username", setValue: "initial_value", expect: "initial_value", description: "Set initial username" },
            { element: "Username", setValue: "updated_value", expect: "updated_value", description: "Update existing username" },
            { element: "Username", setValue: "", expect: "", description: "Clear username field" }
        ]
    },

    "edge_cases": {
        description: "Edge case and error handling",
        setup: {
            url: "http://localhost:3001/test-inputs",
            delay: 100
        },
        tests: [
            { element: "Username", setValue: "   spaces   ", expect: "   spaces   ", description: "Whitespace handling" },
            { element: "NonExistentField", setValue: "test", expect: "test", description: "Missing element error handling", expectError: true },
            { element: "Username", setValue: "special!@#$%^&*()chars", expect: "special!@#$%^&*()chars", description: "Special character handling" }
        ]
    },

    // ========================================================================
    // COMPREHENSIVE CONTROL TESTS - test-controls.html
    // ========================================================================

    "dropdown_controls": {
        description: "Dropdown and select control testing",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "country", setValue: "us", expect: "us", description: "Single select dropdown - select US" },
            { element: "country", setValue: "ca", expect: "ca", description: "Single select dropdown - change to Canada" },
            { element: "country", setValue: "", expect: "", description: "Single select dropdown - clear selection" },
            { element: "Skills (Multi-select)", setValue: ["js", "py"], expect: ["js", "py"], description: "Multi-select dropdown - select multiple" },
            { element: "Skills (Multi-select)", setValue: ["java"], expect: ["java"], description: "Multi-select dropdown - change selection" },
            { element: "Skills (Multi-select)", setValue: [], expect: [], description: "Multi-select dropdown - clear all" }
        ]
    },

    "checkbox_controls": {
        description: "Checkbox control testing",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "I accept the terms and conditions", setValue: true, expect: true, description: "Check terms checkbox" },
            { element: "I accept the terms and conditions", setValue: false, expect: false, description: "Uncheck terms checkbox" },
            { element: "Subscribe to newsletter", setValue: false, expect: false, description: "Uncheck pre-checked newsletter" },
            { element: "Subscribe to newsletter", setValue: true, expect: true, description: "Check newsletter again" },
            { element: "Enable notifications", setValue: true, expect: true, description: "Check notifications" }
        ]
    },

    "radio_controls": {
        description: "Radio button control testing",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "Credit Card", setValue: true, expect: true, description: "Select Credit Card payment" },
            { element: "Debit Card", setValue: true, expect: true, description: "Select Debit Card payment" },
            { element: "Bank Transfer", setValue: true, expect: true, description: "Select Bank Transfer payment" },
            { element: "Small", setValue: true, expect: true, description: "Select Small size" },
            { element: "Large", setValue: true, expect: true, description: "Select Large size" }
        ]
    },

    "textarea_controls": {
        description: "Textarea control testing",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "Comments", setValue: "This is a test comment.", expect: "This is a test comment.", description: "Set textarea content" },
            { element: "Comments", setValue: "Updated comment with\nmultiple lines.", expect: "Updated comment with\nmultiple lines.", description: "Multi-line textarea content" },
            { element: "Comments", setValue: "", expect: "", description: "Clear textarea content" },
            { element: "Description", setValue: "Replacing existing content", expect: "Replacing existing content", description: "Replace pre-filled textarea" }
        ]
    },

    "input_variations": {
        description: "Additional input type variations",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "Username", setValue: "test_user_123", expect: "test_user_123", description: "Text input on test-controls page" },
            { element: "Email Address", setValue: "comprehensive@test.com", expect: "comprehensive@test.com", description: "Email input validation" },
            { element: "Website URL", setValue: "https://example.com", expect: "https://example.com", description: "URL input validation" },
            { element: "Search", setValue: "search query", expect: "search query", description: "Search input functionality" }
        ]
    },

    "password_controls": {
        description: "Password input testing",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "Password", setValue: "test123", expect: null, description: "Basic password input (masked)" },
            { element: "Password with Toggle", setValue: "secret456", expect: null, description: "Password with show/hide toggle (masked)" }
        ]
    },

    "button_controls": {
        description: "Button action and submit testing",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "Save Draft", setValue: null, expect: null, description: "Action button click", action: "click" },
            { element: "Cancel", setValue: null, expect: null, description: "Cancel button click", action: "click" },
            { element: "Delete", setValue: null, expect: null, description: "Delete action button", action: "click" },
            { element: "Input Button", setValue: null, expect: null, description: "Input type button", action: "click" },
            { element: "Custom ARIA Button", setValue: null, expect: null, description: "ARIA role button", action: "click" }
        ]
    },

    "link_controls": {
        description: "Link navigation testing",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "Internal Link", setValue: null, expect: null, description: "Internal page link", action: "click" },
            { element: "External Link", setValue: null, expect: null, description: "External website link", action: "click" },
            { element: "Email Link", setValue: null, expect: null, description: "Mailto link", action: "click" },
            { element: "Phone Link", setValue: null, expect: null, description: "Tel link", action: "click" },
            { element: "JavaScript Link", setValue: null, expect: null, description: "JavaScript action link", action: "click" }
        ]
    },

    "nested_form_controls": {
        description: "Nested and complex form elements",
        setup: {
            url: "http://localhost:3001/test-controls",
            delay: 500
        },
        tests: [
            { element: "Full Name", setValue: "Test User", expect: "Test User", description: "Nested fieldset text input" },
            { element: "Country", setValue: "ca", expect: "ca", description: "Nested fieldset dropdown" },
            { element: "Shipping address same as billing", setValue: true, expect: true, description: "Nested fieldset checkbox" }
        ]
    }
};

// ========================================================================
// CONSOLE RUNNER - Main execution for command line
// ========================================================================

const TestingFramework = require('./framework/TestingFramework.js');
const DataDrivenTestRunner = require('./framework/DataDrivenTestRunner.js');

/**
 * Parse command line arguments
 */
function parseArgs() {
    const args = process.argv.slice(2);
    const options = {
        logLevel: 'INFO' // Default to INFO level
    };

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg.startsWith('--log-level=')) {
            options.logLevel = arg.split('=')[1].toUpperCase();
        } else if (arg === '--log-level' && i + 1 < args.length) {
            options.logLevel = args[i + 1].toUpperCase();
            i++; // Skip next argument
        } else if (arg === '--help' || arg === '-h') {
            console.log('🤖 Data-Driven Test Suite Runner');
            console.log('🔗 Comprehensive testing for AI Browser Extension\n');
            console.log('Usage: node data-driven-tests.js [options]\n');
            console.log('Options:');
            console.log('  --log-level=LEVEL    Set logging level (ERROR, WARN, INFO, DEBUG)');
            console.log('                       Default: INFO');
            console.log('  --help, -h           Show this help message\n');
            console.log('Log Levels:');
            console.log('  ERROR    Only show errors and test failures');
            console.log('  WARN     Show warnings and above');
            console.log('  INFO     Show normal operations (default)');
            console.log('  DEBUG    Show verbose debugging information');
            process.exit(0);
        }
    }

    // Validate log level
    const validLevels = ['ERROR', 'WARN', 'INFO', 'DEBUG'];
    if (!validLevels.includes(options.logLevel)) {
        console.error(`❌ Invalid log level: ${options.logLevel}`);
        console.error(`Valid levels: ${validLevels.join(', ')}`);
        process.exit(1);
    }

    return options;
}

async function loadTestSuitesFromServer() {
    const response = await fetch('http://localhost:3001/test-suites-config');
    if (!response.ok) {
        throw new Error(`Failed to load test suites from server: HTTP ${response.status}`);
    }
    const data = await response.json();
    return data.TEST_SUITES;
}

async function main() {
    const options = parseArgs();

    const framework = new TestingFramework('http://localhost:3001');

    // Console runner log level priority: command line args override config file
    // (Framework constructor already loaded config log level)
    if (options.logLevel !== 'INFO') {
        // Command line specified a different level, use it
        framework.setLogLevel(options.logLevel);
        console.log(`Using command line log level: ${options.logLevel}`);
    } else {
        console.log(`Using config file log level: ${framework.getLogLevelName()}`);
    }

    // Use framework's built-in filtering instead of overriding it
    // framework.setLogger((msg, level) => console.log(`[Framework] ${msg}`));

    const runner = new DataDrivenTestRunner(framework);

    try {
        console.log('Loading test configurations from server...');
        const testSuites = await loadTestSuitesFromServer();
        console.log(`✅ Loaded ${Object.keys(testSuites).length} test suites from server`);

        await framework.validateInfrastructure();
        await framework.selectSession('localhost:3001');

        const results = await runner.runAllSuites(testSuites);

        return results;

    } catch (error) {
        console.error('❌ Data-driven test execution failed:', error.message);
        throw error;
    } finally {
        // TestStreamer will be automatically closed when framework is destroyed
    }
}

// Run if called directly
if (require.main === module) {
    // Check for help flag first
    if (process.argv.includes('--help') || process.argv.includes('-h')) {
        parseArgs(); // This will show help and exit
    }

    const options = parseArgs();
    console.log('🤖 Data-Driven Test Suite Runner');
    console.log('🔗 Comprehensive testing for AI Browser Extension');
    console.log(`📊 Log Level: ${options.logLevel}\n`);

    main()
        .then(results => {
            console.log(`\n🎉 Testing completed: ${results.passed}/${results.total} tests passed`);
            process.exit(results.failed > 0 ? 1 : 0);
        })
        .catch(error => {
            console.error('\n💥 Testing failed:', error.message);
            process.exit(1);
        });
}

// Export for use as module  
module.exports = { TEST_SUITES };

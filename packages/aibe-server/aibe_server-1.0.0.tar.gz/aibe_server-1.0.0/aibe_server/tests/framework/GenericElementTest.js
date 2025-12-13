/**
 * GenericElementTest.js - Data-driven element testing system
 * 
 * Inspired by generic-testing.js but simplified for immediate use.
 * Uses the specification-based get_element/set_element methods.
 */

// Environment detection - only declare if not already defined
if (typeof isNodeJS === 'undefined') {
    var isNodeJS = (typeof module !== 'undefined' && module.exports);
}

class GenericElementTest {
    constructor(framework, progressCallback = null) {
        this.framework = framework;
        this.results = [];
        this.progressCallback = progressCallback;
    }

    /**
     * Run a single element test
     * @param {Object} testCase - {element, setValue, expect, description, action}
     * @param {string} originalUrl - The URL to return to if navigation occurs
     * @returns {Object} Test result
     */
    async runTest(testCase, originalUrl = null) {
        const { element, setValue, expect, description, expectError, action } = testCase;
        const testId = `${element}_${Date.now()}`;
        
        try {
            // Handle different action types
            if (action === 'click') {
                // Store current URL before clicking
                const currentUrl = await this.framework.getCurrentUrl();
                
                // For click actions, use mouse click instead of setting values
                await this.framework.click_element(element);
                
                // Verify the click worked by checking if we navigated
                const newUrl = await this.framework.getCurrentUrl();
                const navigated = newUrl !== currentUrl;
                
                let actual = navigated ? `Navigated to: ${newUrl}` : `Stayed on: ${newUrl}`;
                let passed = true; // Assume success - both navigation and staying can be valid
                
                // For buttons/links that should navigate, verify we went somewhere
                if (['Save Draft', 'Internal Link', 'External Link', 'Email Link', 'Phone Link'].includes(element)) {
                    passed = navigated;
                    if (!passed) {
                        actual = `Expected navigation but stayed on: ${newUrl}`;
                    }
                }
                
                const result = {
                    id: testId,
                    description: description || `Click ${element}`,
                    element,
                    action: 'click',
                    setValue: null,
                    expect,
                    actual,
                    passed,
                    error: null
                };
                
                this.results.push(result);
                return result;
            } else {
                // Default behavior: set and get values
                await this.framework.set_element(element, setValue);
                
                // Get the actual value back
                const actual = await this.framework.get_element(element);
                
                // If we expected an error but didn't get one, that's a failure
                if (expectError) {
                const result = {
                    id: testId,
                    description: description || `Test ${element}`,
                    element,
                    setValue,
                    expect,
                    actual,
                    passed: false,
                    error: `Expected error but operation succeeded with result: ${JSON.stringify(actual)}`
                };
                
                this.results.push(result);
                return result;
            }
            
            // Compare results (deep equality for arrays)
            const passed = this.deepEqual(actual, expect);
            
            const result = {
                id: testId,
                description: description || `Test ${element}`,
                element,
                setValue,
                expect,
                actual,
                passed,
                error: null
            };
            
                this.results.push(result);
                return result;
            }
            
        } catch (error) {
            // If we expected an error and got one, that's a pass
            if (expectError) {
                const result = {
                    id: testId,
                    description: description || `Test ${element}`,
                    element,
                    setValue,
                    expect: 'Error (as expected)',
                    actual: `Error: ${error.message}`,
                    passed: true,
                    error: null
                };
                
                this.results.push(result);
                return result;
            }
            
            // Unexpected error
            const result = {
                id: testId,
                description: description || `Test ${element}`,
                element,
                setValue,
                expect,
                actual: null,
                passed: false,
                error: error.message
            };
            
            this.results.push(result);
            return result;
        }
    }

    /**
     * Run multiple element tests
     * @param {Array} testCases - Array of test case objects
     * @param {string} originalUrl - The URL to return to after navigation clicks
     * @returns {Object} Summary results
     */
    async runTests(testCases, originalUrl = null) {
        if (this.framework.shouldLog && this.framework.shouldLog('info')) {
            console.log(`🧪 Running ${testCases.length} generic element tests...`);
        }
        if (this.framework.shouldLog && this.framework.shouldLog('debug')) {
            console.log(`🔍 Debug: originalUrl parameter = ${originalUrl}`);
        }
        
        // Notify progress callback if provided
        if (this.progressCallback) {
            this.progressCallback({
                type: 'tests_start',
                totalTests: testCases.length,
                originalUrl
            });
        }
        
        // Get current URL if not provided
        if (!originalUrl) {
            try {
                originalUrl = await this.framework.getCurrentUrl();
                if (this.framework.shouldLog && this.framework.shouldLog('debug')) {
                    console.log(`🔍 Debug: Got current URL = ${originalUrl}`);
                }
            } catch (error) {
                if (this.framework.shouldLog && this.framework.shouldLog('warn')) {
                    console.log(`⚠️ Warning: Could not get current URL: ${error.message}`);
                }
            }
        }
        
        const results = [];
        for (let i = 0; i < testCases.length; i++) {
            const testCase = testCases[i];
            
            // Notify progress callback about test start
            if (this.progressCallback) {
                this.progressCallback({
                    type: 'test_start',
                    testIndex: i,
                    testCase,
                    description: testCase.description || testCase.element
                });
            }
            
            // Every test should ensure it's on the correct page first
            if (this.framework.shouldLog && this.framework.shouldLog('debug')) {
                console.log(`🔍 Debug: originalUrl = ${originalUrl}`);
            }
            if (originalUrl) {
                if (this.framework.shouldLog && this.framework.shouldLog('debug')) {
                    console.log(`🔄 Ensuring correct page for test: ${testCase.description || testCase.element}`);
                }
                try {
                    // FIRST: Process all pending Observer events to know current state
                    await this.framework.processObserverQueue();
                    await this.framework.updateCurrentScreen();
                    
                    // THEN: Navigate if needed (navigate_load checks current URL vs target)
                    await this.framework.navigate_load(originalUrl);
                    await this.framework.navigate_confirm(originalUrl);
                    
                    // FINALLY: Process all Observer events from navigation to know new state
                    await this.framework.processObserverQueue();
                    await this.framework.updateCurrentScreen();
                    
                    // Brief delay for stability
                    await new Promise(resolve => setTimeout(resolve, 500));
                } catch (navError) {
                    if (this.framework.shouldLog && this.framework.shouldLog('warn')) {
                        console.log(`⚠️ Warning: Failed to navigate for test isolation: ${navError.message}`);
                    }
                }
            } else {
                if (this.framework.shouldLog && this.framework.shouldLog('warn')) {
                    console.log(`⚠️ Warning: No originalUrl provided - cannot ensure correct page`);
                }
            }
            
            const result = await this.runTest(testCase, originalUrl);
            results.push(result);
            
            // Notify progress callback about test result
            if (this.progressCallback) {
                this.progressCallback({
                    type: 'test_result',
                    testIndex: i,
                    result
                });
            }
            
            // Log each test result
            const status = result.passed ? '✅ PASS' : '❌ FAIL';
            console.log(`  ${status}: ${result.description}`);
            if (!result.passed) {
                if (result.error) {
                    console.log(`    Error: ${result.error}`);
                } else {
                    console.log(`    Expected: ${JSON.stringify(result.expect)}`);
                    console.log(`    Actual: ${JSON.stringify(result.actual)}`);
                }
            }
        }
        
        const summary = {
            total: results.length,
            passed: results.filter(r => r.passed).length,
            failed: results.filter(r => !r.passed).length,
            results
        };
        
        console.log(`📊 Test Summary: ${summary.passed}/${summary.total} passed`);
        
        // Notify progress callback about completion
        if (this.progressCallback) {
            this.progressCallback({
                type: 'tests_complete',
                summary
            });
        }
        
        return summary;
    }

    /**
     * Deep equality comparison for test results
     */
    deepEqual(a, b) {
        if (a === b) return true;
        if (a == null || b == null) return false;
        if (Array.isArray(a) && Array.isArray(b)) {
            if (a.length !== b.length) return false;
            for (let i = 0; i < a.length; i++) {
                if (a[i] !== b[i]) return false;
            }
            return true;
        }
        return false;
    }

    /**
     * Get detailed results for analysis
     */
    getResults() {
        return {
            summary: {
                total: this.results.length,
                passed: this.results.filter(r => r.passed).length,
                failed: this.results.filter(r => !r.passed).length
            },
            details: this.results
        };
    }

    /**
     * Clear previous results
     */
    reset() {
        this.results = [];
    }
}

// Environment-specific export
if (isNodeJS) {
    // Node.js environment - use module.exports
    module.exports = GenericElementTest;
} else {
    // Browser environment - attach to window
    window.GenericElementTest = GenericElementTest;
}
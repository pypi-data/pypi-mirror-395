/**
 * DataDrivenTestRunner.js - Generic test suite runner for data-driven tests
 * 
 * Executes pure test data configurations using the TestingFramework.
 * Completely separated from test data for maximum reusability.
 */

// Environment detection - only declare if not already defined
if (typeof isNodeJS === 'undefined') {
    var isNodeJS = (typeof module !== 'undefined' && module.exports);
}

// Environment-specific setup
if (isNodeJS) {
    // Node.js environment - use require() only if not already defined
    if (typeof GenericElementTest === 'undefined') {
        // Use eval to prevent browser from parsing this line
        eval('var GenericElementTest = require("./GenericElementTest.js");');
    }
}
// Browser environment - GenericElementTest is already global from script tag

class DataDrivenTestRunner {
    constructor(framework, progressCallback = null) {
        this.framework = framework;
        this.progressCallback = progressCallback;
    }
    
    async runSuite(suiteName, suiteConfig) {
        this.framework.logger(`📦 Running test suite: ${suiteName}`, 'info');
        this.framework.logger(`   ${suiteConfig.description}`, 'info');
        
        // Notify progress callback about suite start
        if (this.progressCallback) {
            this.progressCallback({
                type: 'suite_start',
                suiteName,
                description: suiteConfig.description
            });
        }
        
        // Setup - proper navigation with confirmation
        if (suiteConfig.setup) {
            await this.framework.navigate_load(suiteConfig.setup.url);
            await this.framework.navigate_confirm(suiteConfig.setup.url);
            if (suiteConfig.setup.delay) {
                await new Promise(resolve => setTimeout(resolve, suiteConfig.setup.delay));
            }
        }
        
        // Run tests with progress callback wrapper
        const suiteProgressCallback = this.progressCallback ? (data) => {
            // Add suiteName to all progress events
            this.progressCallback({
                ...data,
                suiteName
            });
        } : null;
        
        const elementTest = new GenericElementTest(this.framework, suiteProgressCallback);
        
        // Pass the setup URL as originalUrl for proper test isolation in click tests
        const originalUrl = suiteConfig.setup ? suiteConfig.setup.url : null;
        const results = await elementTest.runTests(suiteConfig.tests, originalUrl);
        
        const suiteResult = {
            suiteName,
            description: suiteConfig.description,
            ...results
        };
        
        // Notify progress callback about suite completion
        if (this.progressCallback) {
            this.progressCallback({
                type: 'suite_complete',
                suiteName,
                ...results
            });
        }
        
        return suiteResult;
    }
    
    async runAllSuites(testSuites) {
        this.framework.logger('🏃 Running all data-driven test suites...', 'info');
        
        const allResults = [];
        for (const [suiteName, suiteConfig] of Object.entries(testSuites)) {
            try {
                const suiteResult = await this.runSuite(suiteName, suiteConfig);
                allResults.push(suiteResult);
            } catch (error) {
                this.framework.logger(`💥 Suite ${suiteName} failed: ${error.message}`, 'error');
                allResults.push({
                    suiteName,
                    error: error.message,
                    total: 0,
                    passed: 0,
                    failed: 1
                });
            }
        }
        
        // Overall summary
        const totalTests = allResults.reduce((sum, r) => sum + (r.total || 0), 0);
        const totalPassed = allResults.reduce((sum, r) => sum + (r.passed || 0), 0);
        const totalFailed = allResults.reduce((sum, r) => sum + (r.failed || 0), 0);
        
        this.framework.logger('🎯 Overall Results:', 'info');
        this.framework.logger(`   Suites: ${allResults.length}`, 'info');
        this.framework.logger(`   Tests: ${totalPassed}/${totalTests} passed`, 'info');
        this.framework.logger(`   Failed: ${totalFailed}`, 'info');
        
        const overallResults = {
            suites: allResults.length,
            total: totalTests,
            passed: totalPassed,
            failed: totalFailed,
            results: allResults,
            success: totalFailed === 0
        };
        
        // Notify progress callback about overall completion
        if (this.progressCallback) {
            this.progressCallback({
                type: 'all_complete',
                ...overallResults
            });
        }
        
        return overallResults;
    }
}

// Environment-specific export
if (isNodeJS) {
    // Node.js environment - use module.exports
    module.exports = DataDrivenTestRunner;
} else {
    // Browser environment - attach to window
    window.DataDrivenTestRunner = DataDrivenTestRunner;
}
"""
UCUP Pytest Plugin

Automatically displays UCUP benefits when running tests with pytest.
This plugin hooks into pytest's lifecycle to show developers how UCUP
is helping them with their testing efforts.
"""

import time
import pytest
from typing import Optional

try:
    from .metrics import get_global_tracker, BenefitsDisplay, record_build_metrics
except ImportError:
    # Fallback for when running from different contexts
    from ucup.metrics import get_global_tracker, BenefitsDisplay, record_build_metrics


class UCUPPytestPlugin:
    """Pytest plugin to display UCUP benefits"""
    
    def __init__(self):
        self.start_time: Optional[float] = None
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0
        self.tracker = get_global_tracker()
    
    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionstart(self, session):
        """Called at the start of test session"""
        self.start_time = time.time()
        
        # Show initial benefits message
        print("\n")
        print("═" * 80)
        print("  🚀 UCUP-Enhanced Test Suite")
        print("  Your tests are powered by intelligent uncertainty quantification!")
        print("═" * 80)
    
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item, nextitem):
        """Called for each test item"""
        self.test_count += 1
        yield
    
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Called after each test phase"""
        outcome = yield
        report = outcome.get_result()
        
        if report.when == "call":
            if report.passed:
                self.passed_count += 1
            elif report.failed:
                self.failed_count += 1
    
    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        """Called at the end of test session"""
        if self.start_time:
            duration = time.time() - self.start_time
            
            # Record metrics
            self.tracker.record_test_run(
                tests_run=self.test_count,
                tests_passed=self.passed_count,
                tests_failed=self.failed_count,
                duration=duration
            )
            
            # Also record as build metrics for comprehensive tracking
            record_build_metrics(
                duration=duration,
                tests_run=self.test_count,
                tests_passed=self.passed_count,
                tests_failed=self.failed_count,
                errors_detected=self.failed_count,
                warnings_detected=0,
                uncertainty_checks=self.test_count,  # Each test uses UCUP
                validation_runs=self.test_count
            )
    
    @pytest.hookimpl(trylast=True)
    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        """Add UCUP benefits summary to test output"""
        duration = time.time() - self.start_time if self.start_time else 0
        
        # Show comprehensive benefits display
        BenefitsDisplay.show_test_benefits(
            self.tracker,
            current_tests=self.test_count,
            current_duration=duration
        )
        
        # Add extra motivational message based on test results
        if self.failed_count == 0 and self.test_count > 0:
            print("\n✨ All tests passed! UCUP helped ensure your AI agents are reliable.\n")
        elif self.test_count > 0:
            print("\n🔍 UCUP helped identify issues early in development.\n")


# This is required for pytest to discover the plugin
def pytest_configure(config):
    """Register the UCUP plugin with pytest"""
    if not config.option.collectonly:
        plugin = UCUPPytestPlugin()
        config.pluginmanager.register(plugin, "ucup_plugin")


# Make functions available at module level
__all__ = ['UCUPPytestPlugin', 'pytest_configure']

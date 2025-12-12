"""Output formatting for wobble framework.

This module provides enhanced output formatting with colors, timing information,
and multiple output formats (standard, verbose, JSON, minimal).
"""

import json
import sys
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from .decorators import get_test_metadata

try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback if colorama is not available
    COLORS_AVAILABLE = False
    
    class _DummyColor:
        def __getattr__(self, name):
            return ""
    
    Fore = Back = Style = _DummyColor()


class OutputFormatter:
    """Enhanced output formatter for wobble test results."""
    
    def __init__(self, 
                 format_type: str = "standard",
                 use_color: bool = True,
                 verbosity: int = 0,
                 quiet: bool = False):
        """Initialize the output formatter.
        
        Args:
            format_type: Output format ('standard', 'verbose', 'json', 'minimal')
            use_color: Whether to use colored output
            verbosity: Verbosity level (0-2)
            quiet: Whether to suppress most output
        """
        self.format_type = format_type
        self.use_color = use_color and COLORS_AVAILABLE
        self.verbosity = verbosity
        self.quiet = quiet
        
        # Status icons - use Unicode symbols with ASCII fallback for encoding issues
        try:
            # Test if Unicode symbols can be encoded
            test_symbols = '✓✗💥⊝ℹ'
            test_symbols.encode(sys.stdout.encoding or 'utf-8')
            self.icons = {
                'pass': '✓',
                'fail': '✗',
                'error': '💥',
                'skip': '⊝',
                'info': 'ℹ'
            }
        except (UnicodeEncodeError, LookupError):
            # Fallback to ASCII if Unicode symbols can't be encoded
            self.icons = {
                'pass': 'PASS',
                'fail': 'FAIL',
                'error': 'ERROR',
                'skip': 'SKIP',
                'info': 'INFO'
            }
        
        # Colors
        self.colors = {
            'pass': Fore.GREEN if self.use_color else '',
            'fail': Fore.RED if self.use_color else '',
            'error': Fore.YELLOW if self.use_color else '',
            'skip': Fore.CYAN if self.use_color else '',
            'info': Fore.BLUE if self.use_color else '',
            'reset': Style.RESET_ALL if self.use_color else ''
        }
    
    def print_test_run_header(self, test_count: int) -> None:
        """Print header for test run.
        
        Args:
            test_count: Number of tests to be run
        """
        if self.quiet:
            return
        
        if self.format_type == 'json':
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{self.colors['info']}{'='*60}{self.colors['reset']}")
        print(f"{self.colors['info']}Wobble Test Runner - {timestamp}{self.colors['reset']}")
        print(f"{self.colors['info']}Running {test_count} test(s){self.colors['reset']}")
        print(f"{self.colors['info']}{'='*60}{self.colors['reset']}\n")
    
    def print_test_start(self, test_case) -> None:
        """Print test start information.

        Args:
            test_case: unittest.TestCase instance
        """
        if self.quiet:
            return

        if self.format_type == 'json':
            return

        test_name = self._get_test_name(test_case)
        # Always show test start for debugging hanging tests
        # Use different format based on verbosity
        if self.verbosity >= 2:
            print(f"  Starting: {test_name}")
        elif self.verbosity >= 1:
            print(f"Starting {test_name}...", end=" ", flush=True)
        else:
            # Even at verbosity 0, show minimal progress for hanging test detection
            print(".", end="", flush=True)
    
    def print_test_success(self, test_case, duration: float) -> None:
        """Print successful test result.
        
        Args:
            test_case: unittest.TestCase instance
            duration: Test execution time in seconds
        """
        if self.quiet:
            return
        
        if self.format_type == 'json':
            return
        
        test_name = self._get_test_name(test_case)
        duration_str = f"({duration:.3f}s)" if self.verbosity > 0 else ""
        decorator_str = self._get_wobble_decorators(test_case)

        if self.format_type == 'minimal':
            print(".", end="", flush=True)
        else:
            icon = self.icons['pass']
            color = self.colors['pass']
            reset = self.colors['reset']
            print(f"{color}{icon} {test_name} {duration_str}{decorator_str}{reset}")
    
    def print_test_failure(self, test_case, err_info: Tuple, duration: float) -> None:
        """Print failed test result.
        
        Args:
            test_case: unittest.TestCase instance
            err_info: Error information tuple (type, value, traceback)
            duration: Test execution time in seconds
        """
        if self.quiet:
            return
        
        if self.format_type == 'json':
            return
        
        test_name = self._get_test_name(test_case)
        duration_str = f"({duration:.3f}s)" if self.verbosity > 0 else ""
        decorator_str = self._get_wobble_decorators(test_case)

        if self.format_type == 'minimal':
            print("F", end="", flush=True)
        else:
            icon = self.icons['fail']
            color = self.colors['fail']
            reset = self.colors['reset']
            print(f"{color}{icon} {test_name} {duration_str}{decorator_str}{reset}")

            if self.verbosity > 0:
                print(f"    {color}Failure: {err_info[1]}{reset}")
    
    def print_test_error(self, test_case, err_info: Tuple, duration: float) -> None:
        """Print test error result.
        
        Args:
            test_case: unittest.TestCase instance
            err_info: Error information tuple (type, value, traceback)
            duration: Test execution time in seconds
        """
        if self.quiet:
            return
        
        if self.format_type == 'json':
            return
        
        test_name = self._get_test_name(test_case)
        duration_str = f"({duration:.3f}s)" if self.verbosity > 0 else ""
        decorator_str = self._get_wobble_decorators(test_case)

        if self.format_type == 'minimal':
            print("E", end="", flush=True)
        else:
            icon = self.icons['error']
            color = self.colors['error']
            reset = self.colors['reset']
            print(f"{color}{icon} {test_name} {duration_str}{decorator_str}{reset}")

            if self.verbosity > 0:
                print(f"    {color}Error: {err_info[1]}{reset}")
    
    def print_test_skip(self, test_case, reason: str, duration: float) -> None:
        """Print skipped test result.
        
        Args:
            test_case: unittest.TestCase instance
            reason: Skip reason
            duration: Test execution time in seconds
        """
        if self.quiet:
            return
        
        if self.format_type == 'json':
            return
        
        test_name = self._get_test_name(test_case)
        duration_str = f"({duration:.3f}s)" if self.verbosity > 0 else ""
        decorator_str = self._get_wobble_decorators(test_case)

        if self.format_type == 'minimal':
            print("S", end="", flush=True)
        else:
            icon = self.icons['skip']
            color = self.colors['skip']
            reset = self.colors['reset']
            print(f"{color}{icon} {test_name} {duration_str}{decorator_str}{reset}")

            if self.verbosity > 0:
                print(f"    {color}Skipped: {reason}{reset}")
    
    def print_test_results(self, results: Dict[str, Any]) -> None:
        """Print final test results summary.
        
        Args:
            results: Test results dictionary
        """
        if self.format_type == 'json':
            self._print_json_results(results)
            return
        
        if self.format_type == 'minimal':
            print()  # New line after dots
        
        if self.quiet and results.get('failures', 0) == 0 and results.get('errors', 0) == 0:
            return
        
        print(f"\n{self.colors['info']}{'='*60}{self.colors['reset']}")
        print(f"{self.colors['info']}Test Results Summary{self.colors['reset']}")
        print(f"{self.colors['info']}{'='*60}{self.colors['reset']}")
        
        # Basic statistics
        tests_run = results.get('tests_run', 0)
        failures = results.get('failures', 0)
        errors = results.get('errors', 0)
        skipped = results.get('skipped', 0)
        success_rate = results.get('success_rate', 0.0)
        total_time = results.get('total_time', 0.0)
        
        print(f"Tests run: {tests_run}")
        print(f"Failures: {failures}")
        print(f"Errors: {errors}")
        print(f"Skipped: {skipped}")
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Total time: {total_time:.3f}s")
        
        # Overall result
        if failures == 0 and errors == 0:
            color = self.colors['pass']
            status = "PASSED"
        else:
            color = self.colors['fail']
            status = "FAILED"
        
        print(f"\n{color}Overall result: {status}{self.colors['reset']}")
    
    def print_discovery_summary(self, discovered_tests: Dict[str, List]) -> None:
        """Print test discovery summary.
        
        Args:
            discovered_tests: Dictionary of categorized discovered tests
        """
        if self.quiet:
            return
        
        if self.format_type == 'json':
            summary = {category: len(tests) for category, tests in discovered_tests.items()}
            print(json.dumps(summary, indent=2))
            return
        
        print(f"\n{self.colors['info']}Test Discovery Summary{self.colors['reset']}")
        print(f"{self.colors['info']}{'='*40}{self.colors['reset']}")
        
        total_tests = sum(len(tests) for tests in discovered_tests.values())
        print(f"Total tests discovered: {total_tests}")
        
        for category, tests in discovered_tests.items():
            if tests:
                print(f"  {category.capitalize()}: {len(tests)}")
    
    def print_test_categories(self, discovered_tests: Dict[str, List]) -> None:
        """Print available test categories.
        
        Args:
            discovered_tests: Dictionary of categorized discovered tests
        """
        if self.quiet:
            return
        
        categories = [cat for cat, tests in discovered_tests.items() if tests]
        
        if self.format_type == 'json':
            print(json.dumps(categories))
            return
        
        print("Available test categories:")
        for category in categories:
            count = len(discovered_tests[category])
            print(f"  {category} ({count} tests)")
    
    def print_info(self, message: str) -> None:
        """Print informational message.
        
        Args:
            message: Message to print
        """
        if self.quiet or self.format_type == 'json':
            return
        
        icon = self.icons['info']
        color = self.colors['info']
        reset = self.colors['reset']
        print(f"{color}{icon} {message}{reset}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message.
        
        Args:
            message: Warning message to print
        """
        if self.format_type == 'json':
            return
        
        color = self.colors['error']
        reset = self.colors['reset']
        print(f"{color}Warning: {message}{reset}", file=sys.stderr)
    
    def print_error(self, message: str) -> None:
        """Print error message.
        
        Args:
            message: Error message to print
        """
        if self.format_type == 'json':
            return
        
        color = self.colors['fail']
        reset = self.colors['reset']
        print(f"{color}Error: {message}{reset}", file=sys.stderr)
    
    def _print_json_results(self, results: Dict[str, Any]) -> None:
        """Print results in JSON format.
        
        Args:
            results: Test results dictionary
        """
        # Convert results to JSON-serializable format
        json_results = {
            'timestamp': datetime.now().isoformat(),
            'tests_run': results.get('tests_run', 0),
            'failures': results.get('failures', 0),
            'errors': results.get('errors', 0),
            'skipped': results.get('skipped', 0),
            'success_rate': results.get('success_rate', 0.0),
            'total_time': results.get('total_time', 0.0)
        }
        
        print(json.dumps(json_results, indent=2))
    
    def _get_test_name(self, test_case) -> str:
        """Get a readable name for a test case.

        Args:
            test_case: unittest.TestCase instance

        Returns:
            Human-readable test name
        """
        if hasattr(test_case, '_testMethodName'):
            class_name = test_case.__class__.__name__
            method_name = test_case._testMethodName
            return f"{class_name}.{method_name}"

        return str(test_case)

    def _get_wobble_decorators(self, test_case) -> str:
        """Get Wobble decorator information for a test case.

        Args:
            test_case: unittest.TestCase instance

        Returns:
            Formatted decorator string or empty string
        """
        if not hasattr(test_case, '_testMethodName'):
            return ""

        try:
            test_method = getattr(test_case, test_case._testMethodName)
            metadata = get_test_metadata(test_method)

            decorators = []
            if metadata.get('regression'):
                decorators.append('@regression_test')
            if metadata.get('integration'):
                decorators.append('@integration_test')
            if metadata.get('development'):
                decorators.append('@development_test')
            if metadata.get('slow'):
                decorators.append('@slow_test')
            if metadata.get('skip_ci'):
                decorators.append('@skip_ci')

            if decorators:
                return f" [{', '.join(decorators)}]"

        except (AttributeError, TypeError):
            pass

        return ""

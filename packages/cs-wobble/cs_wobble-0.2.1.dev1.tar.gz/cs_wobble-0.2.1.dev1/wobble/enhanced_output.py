"""Enhanced output system integrating Observer + Strategy patterns.

This module provides the EnhancedOutputFormatter that integrates
the new observer architecture with the existing OutputFormatter
interface for backward compatibility.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import time

from .output_architecture import (
    OutputEventPublisher, TestEvent, ConsoleOutputObserver, FileOutputObserver,
    StandardOutputStrategy, VerboseOutputStrategy, JSONOutputStrategy
)
from .data_structures import TestResult, TestStatus, ErrorInfo, TestRunSummary


class EnhancedOutputFormatter:
    """Enhanced output formatter using Observer + Strategy patterns.
    
    This class provides backward compatibility with the existing OutputFormatter
    interface while leveraging the new observer architecture for parallel
    output processing and extensibility.
    """
    
    def __init__(self, 
                 format_type: str = "standard",
                 use_color: bool = True,
                 verbosity: int = 0,
                 quiet: bool = False,
                 file_outputs: Optional[List[Dict[str, Any]]] = None):
        """Initialize the enhanced output formatter.
        
        Args:
            format_type: Console output format ('standard', 'verbose', 'json', 'minimal')
            use_color: Whether to use colored console output
            verbosity: Console verbosity level (0-2)
            quiet: Whether to suppress console output except errors
            file_outputs: List of file output configurations
        """
        self.format_type = format_type
        self.use_color = use_color
        self.verbosity = verbosity
        self.quiet = quiet
        self.file_outputs = file_outputs or []
        
        # Initialize observer system
        self.publisher = OutputEventPublisher()
        
        # Track test run state
        self.test_results: List[TestResult] = []
        self.run_start_time: Optional[datetime] = None
        self.run_command: Optional[str] = None
        self.run_ended: bool = False  # Guard against duplicate end_test_run calls
        
        # Setup observers
        self._setup_console_observer()
        self._setup_file_observers()
    
    def _setup_console_observer(self) -> None:
        """Setup console output observer based on format type."""
        if self.format_type == 'verbose':
            strategy = VerboseOutputStrategy()
        elif self.format_type == 'json':
            strategy = JSONOutputStrategy()
        else:  # standard, minimal
            strategy = StandardOutputStrategy()
        
        console_observer = ConsoleOutputObserver(
            strategy=strategy,
            use_color=self.use_color,
            quiet=self.quiet
        )
        
        self.publisher.add_observer(console_observer)
    
    def _setup_file_observers(self) -> None:
        """Setup file output observers based on configuration."""
        for file_config in self.file_outputs:
            # Determine strategy based on format
            if file_config['format'] == 'json':
                strategy = JSONOutputStrategy()
            elif file_config.get('verbosity', 1) >= 2:
                strategy = VerboseOutputStrategy()
            else:
                strategy = StandardOutputStrategy()
            
            file_observer = FileOutputObserver(
                file_path=file_config['filename'],
                strategy=strategy,
                verbosity=file_config.get('verbosity', 1),
                threaded=True,
                append_mode=file_config.get('append', False)
            )
            
            self.publisher.add_observer(file_observer)
    
    def start_test_run(self, command: str, test_count: int) -> None:
        """Start a test run and notify observers.
        
        Args:
            command: The command that started the test run
            test_count: Number of tests to be run
        """
        self.run_start_time = datetime.now()
        self.run_command = command
        self.test_results.clear()
        
        # Notify observers of run start
        event = TestEvent(
            event_type='run_start',
            metadata={
                'command': command,
                'start_time': self.run_start_time,
                'test_count': test_count
            }
        )
        
        self.publisher.notify_all(event)
    
    def notify_test_start(self, test_case) -> None:
        """Notify observers that a test is starting.
        
        Args:
            test_case: unittest.TestCase instance
        """
        test_name = self._get_test_name(test_case)
        
        event = TestEvent(
            event_type='test_start',
            metadata={
                'test_name': test_name,
                'test_class': test_case.__class__.__name__
            }
        )
        
        self.publisher.notify_all(event)
    
    def notify_test_end(self, test_result: TestResult) -> None:
        """Notify observers that a test has ended.
        
        Args:
            test_result: The completed test result
        """
        self.test_results.append(test_result)
        
        event = TestEvent(
            event_type='test_end',
            test_result=test_result
        )
        
        self.publisher.notify_all(event)
    
    def end_test_run(self, exit_code: int = 0) -> None:
        """End the test run and notify observers with summary.

        Args:
            exit_code: The exit code for the test run
        """
        if not self.run_start_time or self.run_ended:
            return

        # Mark run as ended to prevent duplicate calls
        self.run_ended = True
        
        end_time = datetime.now()
        duration = (end_time - self.run_start_time).total_seconds()
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.status == TestStatus.PASS)
        failed = sum(1 for r in self.test_results if r.status == TestStatus.FAIL)
        errors = sum(1 for r in self.test_results if r.status == TestStatus.ERROR)
        skipped = sum(1 for r in self.test_results if r.status == TestStatus.SKIP)
        
        # Create run summary
        summary = TestRunSummary(
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            errors=errors,
            skipped=skipped,
            duration=duration,
            start_time=self.run_start_time,
            end_time=end_time,
            command=self.run_command or "unknown",
            exit_code=exit_code
        )
        
        # Notify observers of run end
        event = TestEvent(
            event_type='run_end',
            run_summary=summary
        )
        
        self.publisher.notify_all(event)
    
    def close(self) -> None:
        """Close the output formatter and clean up resources."""
        self.publisher.close_all()
    
    # Backward compatibility methods for existing OutputFormatter interface
    
    def print_test_run_header(self, test_count: int) -> None:
        """Print header for test run (backward compatibility).
        
        Args:
            test_count: Number of tests to be run
        """
        if not self.run_command:
            self.run_command = "wobble"  # Default command
        
        self.start_test_run(self.run_command, test_count)
    
    def print_test_success(self, test_case, duration: float) -> None:
        """Print successful test result (backward compatibility).
        
        Args:
            test_case: unittest.TestCase instance
            duration: Test execution time in seconds
        """
        test_result = self._create_test_result(test_case, TestStatus.PASS, duration)
        self.notify_test_end(test_result)
    
    def print_test_failure(self, test_case, err_info, duration: float) -> None:
        """Print failed test result (backward compatibility).
        
        Args:
            test_case: unittest.TestCase instance
            err_info: Error information tuple (type, value, traceback)
            duration: Test execution time in seconds
        """
        error_info = self._create_error_info(err_info)
        test_result = self._create_test_result(test_case, TestStatus.FAIL, duration, error_info)
        self.notify_test_end(test_result)
    
    def print_test_error(self, test_case, err_info, duration: float) -> None:
        """Print test error result (backward compatibility).
        
        Args:
            test_case: unittest.TestCase instance
            err_info: Error information tuple (type, value, traceback)
            duration: Test execution time in seconds
        """
        error_info = self._create_error_info(err_info)
        test_result = self._create_test_result(test_case, TestStatus.ERROR, duration, error_info)
        self.notify_test_end(test_result)
    
    def print_test_skip(self, test_case, reason: str, duration: float = 0.0) -> None:
        """Print skipped test result (backward compatibility).
        
        Args:
            test_case: unittest.TestCase instance
            reason: Reason for skipping
            duration: Test execution time in seconds
        """
        test_result = self._create_test_result(test_case, TestStatus.SKIP, duration)
        test_result.metadata['skip_reason'] = reason
        self.notify_test_end(test_result)
    
    def print_test_results(self, results: Dict[str, Any]) -> None:
        """Print final test results (backward compatibility).
        
        Args:
            results: Test results dictionary
        """
        exit_code = 1 if (results.get('failures', 0) > 0 or results.get('errors', 0) > 0) else 0
        self.end_test_run(exit_code)
    
    def print_info(self, message: str) -> None:
        """Print informational message (backward compatibility).
        
        Args:
            message: Message to print
        """
        if not self.quiet:
            print(f"Info: {message}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message (backward compatibility).
        
        Args:
            message: Warning message to print
        """
        print(f"Warning: {message}")
    
    def print_error(self, message: str) -> None:
        """Print error message (backward compatibility).
        
        Args:
            message: Error message to print
        """
        print(f"Error: {message}")
    
    def print_discovery_summary(self, discovered_tests: Dict[str, Any]) -> None:
        """Print test discovery summary and write to files.

        Args:
            discovered_tests: Dictionary of discovered tests
        """
        total_tests = sum(len(tests) for tests in discovered_tests.values())

        # Console output (backward compatibility)
        print(f"Discovered {total_tests} test(s) across {len(discovered_tests)} categories")

        if self.verbosity > 0:
            for category, tests in discovered_tests.items():
                print(f"  {category}: {len(tests)} test(s)")

        # File output via Observer pattern
        if self.file_outputs:
            # Create discovery event for file output
            event = TestEvent(
                event_type='discovery_complete',
                metadata={
                    'discovered_tests': discovered_tests,
                    'total_tests': total_tests,
                    'categories': len(discovered_tests),
                    'timestamp': datetime.now()
                }
            )

            self.publisher.notify_all(event)
    
    def print_test_categories(self, discovered_tests: Dict[str, Any]) -> None:
        """Print available test categories (backward compatibility).
        
        Args:
            discovered_tests: Dictionary of discovered tests
        """
        print("Available test categories:")
        for category, tests in discovered_tests.items():
            print(f"  {category}: {len(tests)} test(s)")
    
    # Helper methods
    
    def _get_test_name(self, test_case) -> str:
        """Get the full test name from a test case.

        Args:
            test_case: unittest.TestCase instance or _ErrorHolder

        Returns:
            Full test name in format 'ClassName.test_method'
        """
        class_name = test_case.__class__.__name__
        if self._is_error_holder(test_case):
            # Create enhanced error message for _ErrorHolder
            enhanced_info = self._parse_error_holder_description(test_case.description)
            method_name = enhanced_info['enhanced_message']
        else:
            method_name = test_case._testMethodName
        return f"{class_name}.{method_name}"
    
    def _create_test_result(self, test_case, status: TestStatus, duration: float, 
                          error_info: Optional[ErrorInfo] = None) -> TestResult:
        """Create a TestResult from a test case.
        
        Args:
            test_case: unittest.TestCase instance
            status: Test status
            duration: Test execution time
            error_info: Optional error information
            
        Returns:
            TestResult instance
        """
        if self._is_error_holder(test_case):
            # Create enhanced error message for _ErrorHolder
            enhanced_info = self._parse_error_holder_description(test_case.description)
            test_name = enhanced_info['enhanced_message']
        else:
            test_name = test_case._testMethodName

        return TestResult(
            name=test_name,
            classname=test_case.__class__.__name__,
            status=status,
            duration=duration,
            timestamp=datetime.now(),
            metadata=getattr(test_case, '_wobble_metadata', {}),
            error_info=error_info
        )
    
    def _create_error_info(self, err_info) -> ErrorInfo:
        """Create ErrorInfo from error tuple.
        
        Args:
            err_info: Error information tuple (type, value, traceback)
            
        Returns:
            ErrorInfo instance
        """
        import traceback
        
        exc_type, exc_value, exc_traceback = err_info
        
        return ErrorInfo(
            type=exc_type.__name__,
            message=str(exc_value),
            traceback=''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        )
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def _is_error_holder(self, test_case) -> bool:
        """Check if test case is an _ErrorHolder representing import/loading failure.

        Args:
            test_case: The test case object to check

        Returns:
            True if this is an _ErrorHolder, False otherwise
        """
        return test_case.__class__.__name__ == '_ErrorHolder'

    def _parse_error_holder_description(self, description: str) -> dict:
        """Parse _ErrorHolder description to extract meaningful information.

        Args:
            description: The error description from _ErrorHolder

        Returns:
            Dictionary with parsed information
        """
        import re

        # Initialize result
        result = {
            'original_description': description,
            'error_type': 'import_error',
            'test_class': None,
            'test_module': None,
            'file_path': None,
            'method_name': None,
            'enhanced_message': description
        }

        # Parse patterns like "setUpClass (test_hatch_installer.TestHatchInstaller)"
        setup_pattern = r'(setUpClass|setUp|tearDown|tearDownClass)\s*\(([^.]+)\.([^)]+)\)'
        match = re.match(setup_pattern, description)

        if match:
            method_name, module_name, class_name = match.groups()
            result.update({
                'method_name': method_name,
                'test_module': module_name,
                'test_class': class_name,
                'file_path': f"{module_name}.py",
                'enhanced_message': f"{method_name} failed in {class_name} ({module_name}.py)"
            })
        else:
            # Try to extract class and module from other patterns
            # Pattern like "module.ClassName"
            class_pattern = r'([^.]+)\.([^.]+)$'
            match = re.search(class_pattern, description)
            if match:
                module_name, class_name = match.groups()
                result.update({
                    'test_module': module_name,
                    'test_class': class_name,
                    'file_path': f"{module_name}.py",
                    'enhanced_message': f"Import failed for {class_name} in {module_name}.py"
                })

        return result

    def print_discovery_output(self, discovery_output: str, verbosity: int = 1, discovery_data: dict = None) -> None:
        """Print discovery output to both console and file outputs.

        Args:
            discovery_output: Formatted discovery output string for console
            verbosity: Discovery verbosity level (1-3)
            discovery_data: Structured discovery data for JSON formatting
        """
        # Print to console (unless quiet)
        if not self.quiet:
            print(discovery_output)

        # Send to file observers if configured
        if self.file_outputs:
            # Create discovery event for file output with structured data
            discovery_event = TestEvent(
                event_type='discovery_summary',
                metadata={
                    'discovery_output': discovery_output,  # Text format fallback
                    'discovery_data': discovery_data,      # Structured data for JSON
                    'verbosity': verbosity,
                    'timestamp': datetime.now(),
                    'command_info': {
                        'type': 'discovery',
                        'verbosity_level': verbosity
                    }
                }
            )

            # Notify all observers
            self.publisher.notify_all(discovery_event)

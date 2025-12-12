"""Output architecture using Observer + Strategy patterns.

This module implements a scalable output system that supports
parallel processing of multiple output destinations using the
Observer pattern for event distribution and Strategy pattern
for format-specific output handling.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
import threading
import time
import sys
from datetime import datetime

from .data_structures import TestResult, TestRunSummary
from .file_io import ThreadedFileWriter


@dataclass
class TestEvent:
    """Event representing a test-related occurrence.
    
    Attributes:
        event_type: Type of event ('test_start', 'test_end', 'run_start', 'run_end')
        test_result: Test result data (for test events)
        run_summary: Test run summary (for run events)
        metadata: Additional event metadata
        timestamp: When the event occurred
    """
    event_type: str
    test_result: Optional[TestResult] = None
    run_summary: Optional[TestRunSummary] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class OutputStrategy(ABC):
    """Abstract base class for output formatting strategies."""
    
    @abstractmethod
    def format_test_result(self, test_result: TestResult, verbosity: int = 1) -> str:
        """Format a test result for output.
        
        Args:
            test_result: The test result to format
            verbosity: Output verbosity level
            
        Returns:
            Formatted string representation
        """
        pass
    
    @abstractmethod
    def format_run_summary(self, summary: TestRunSummary) -> str:
        """Format a test run summary for output.
        
        Args:
            summary: The test run summary to format
            
        Returns:
            Formatted string representation
        """
        pass
    
    @abstractmethod
    def format_header(self, command: str, start_time: datetime) -> str:
        """Format a header for the output.

        Args:
            command: The command that started the test run
            start_time: When the test run started

        Returns:
            Formatted header string
        """
        pass

    @abstractmethod
    def format_discovery_results(self, discovery_metadata: Dict[str, Any]) -> str:
        """Format discovery results for output.

        Args:
            discovery_metadata: Discovery results metadata

        Returns:
            Formatted discovery results string
        """
        pass

    @abstractmethod
    def format_discovery_summary(self, discovery_data: Dict[str, Any], verbosity: int = 1) -> str:
        """Format discovery summary for output.

        Args:
            discovery_data: Structured discovery data
            verbosity: Discovery verbosity level

        Returns:
            Formatted discovery summary string
        """
        pass


class StandardOutputStrategy(OutputStrategy):
    """Standard text output formatting strategy."""
    
    def format_test_result(self, test_result: TestResult, verbosity: int = 1) -> str:
        """Format test result in standard text format."""
        status_symbol = {
            'PASS': '✓',
            'FAIL': '✗',
            'ERROR': '💥',
            'SKIP': '⊝'
        }.get(test_result.status.value, '?')
        
        result = f"{status_symbol} {test_result.classname}.{test_result.name}"
        
        if verbosity >= 1:
            result += f" ({test_result.duration:.3f}s)"
        
        if verbosity >= 2 and test_result.error_info:
            result += f"\n    Error: {test_result.error_info.type}: {test_result.error_info.message}"
        
        return result
    
    def format_run_summary(self, summary: TestRunSummary) -> str:
        """Format test run summary in standard text format."""
        lines = [
            "=== Test Run Summary ===",
            f"Total: {summary.total_tests}",
            f"Passed: {summary.passed}",
            f"Failed: {summary.failed}",
            f"Errors: {summary.errors}",
            f"Skipped: {summary.skipped}",
            f"Success Rate: {summary.success_rate:.1f}%",
            f"Duration: {summary.duration:.3f}s"
        ]
        return '\n'.join(lines)
    
    def format_header(self, command: str, start_time: datetime) -> str:
        """Format header in standard text format."""
        return f"Running: {command}\nStarted: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"

    def format_discovery_results(self, discovery_metadata: Dict[str, Any]) -> str:
        """Format discovery results in standard text format."""
        lines = [
            "=== Test Discovery Results ===",
            f"Total tests: {discovery_metadata.get('total_tests', 0)}",
            f"Categories: {discovery_metadata.get('categories', 0)}",
            ""
        ]

        discovered_tests = discovery_metadata.get('discovered_tests', {})
        for category, tests in discovered_tests.items():
            lines.append(f"{category}: {len(tests)} test(s)")

        return '\n'.join(lines)

    def format_discovery_summary(self, discovery_data: Dict[str, Any], verbosity: int = 1) -> str:
        """Format discovery summary in standard text format."""
        summary = discovery_data.get('discovery_summary', {})
        total_tests = summary.get('total_tests', 0)
        categories = summary.get('categories', {})

        lines = []
        lines.append(f"Total tests discovered: {total_tests}")

        # Add category counts
        for category in ['regression', 'integration', 'development', 'slow', 'skip_ci', 'uncategorized']:
            count = categories.get(category, 0)
            if count > 0:
                lines.append(f"{category.title()}: {count}")

        # Level 2: Add uncategorized test details
        if verbosity >= 2 and 'uncategorized_tests' in summary:
            lines.append("\nUncategorized tests:")
            for test in summary['uncategorized_tests']:
                lines.append(f"  {test['name']} ({test.get('file', 'unknown')})")

        # Level 3: Add all test details
        if verbosity >= 3 and 'tests_by_category' in summary:
            tests_by_category = summary['tests_by_category']
            for category in ['regression', 'integration', 'development', 'slow', 'skip_ci']:
                if category in tests_by_category and tests_by_category[category]:
                    lines.append(f"\n{category.title()} tests:")
                    for test in tests_by_category[category]:
                        decorators = test.get('decorators', [])
                        decorator_str = f" [{', '.join(decorators)}]" if decorators else ""
                        lines.append(f"  {test['name']} ({test.get('file', 'unknown')}){decorator_str}")

        return '\n'.join(lines)


class VerboseOutputStrategy(OutputStrategy):
    """Verbose text output formatting strategy."""
    
    def format_test_result(self, test_result: TestResult, verbosity: int = 2) -> str:
        """Format test result in verbose text format."""
        lines = [f"Test: {test_result.classname}.{test_result.name}"]
        lines.append(f"Status: {test_result.status.value}")
        lines.append(f"Duration: {test_result.duration:.6f}s")
        lines.append(f"Timestamp: {test_result.timestamp.isoformat()}")
        
        if test_result.metadata:
            lines.append(f"Metadata: {test_result.metadata}")
        
        if test_result.error_info:
            lines.append(f"Error Type: {test_result.error_info.type}")
            lines.append(f"Error Message: {test_result.error_info.message}")
            if verbosity >= 3:
                lines.append("Traceback:")
                lines.extend(f"  {line}" for line in test_result.error_info.traceback.split('\n')[:10])
        
        return '\n'.join(lines) + '\n'
    
    def format_run_summary(self, summary: TestRunSummary) -> str:
        """Format test run summary in verbose text format."""
        lines = [
            "=== Detailed Test Run Summary ===",
            f"Command: {summary.command}",
            f"Start Time: {summary.start_time.isoformat()}",
            f"End Time: {summary.end_time.isoformat()}",
            f"Total Duration: {summary.duration:.6f}s",
            "",
            "Test Counts:",
            f"  Total: {summary.total_tests}",
            f"  Passed: {summary.passed}",
            f"  Failed: {summary.failed}",
            f"  Errors: {summary.errors}",
            f"  Skipped: {summary.skipped}",
            "",
            f"Success Rate: {summary.success_rate:.2f}%",
            f"Exit Code: {summary.exit_code}"
        ]
        return '\n'.join(lines)
    
    def format_header(self, command: str, start_time: datetime) -> str:
        """Format header in verbose text format."""
        lines = [
            "=" * 60,
            "WOBBLE TEST EXECUTION",
            "=" * 60,
            f"Command: {command}",
            f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Process ID: {threading.get_ident()}",
            "=" * 60,
            ""
        ]
        return '\n'.join(lines)

    def format_discovery_results(self, discovery_metadata: Dict[str, Any]) -> str:
        """Format discovery results in verbose text format."""
        lines = [
            "=" * 60,
            "WOBBLE TEST DISCOVERY RESULTS",
            "=" * 60,
            f"Timestamp: {discovery_metadata.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total tests discovered: {discovery_metadata.get('total_tests', 0)}",
            f"Test categories found: {discovery_metadata.get('categories', 0)}",
            "=" * 60,
            ""
        ]

        discovered_tests = discovery_metadata.get('discovered_tests', {})
        for category, tests in discovered_tests.items():
            lines.append(f"Category: {category} ({len(tests)} tests)")
            lines.append("-" * 40)
            for test in tests:
                test_name = test.get('name', 'unknown')
                test_class = test.get('class', 'unknown')
                lines.append(f"  • {test_class}.{test_name}")
            lines.append("")

        return '\n'.join(lines)

    def format_discovery_summary(self, discovery_data: Dict[str, Any], verbosity: int = 1) -> str:
        """Format discovery summary in verbose text format."""
        summary = discovery_data.get('discovery_summary', {})
        total_tests = summary.get('total_tests', 0)
        categories = summary.get('categories', {})
        timestamp = summary.get('timestamp', datetime.now().isoformat())

        lines = [
            "=" * 60,
            "WOBBLE TEST DISCOVERY SUMMARY",
            "=" * 60,
            f"Timestamp: {timestamp}",
            f"Total tests discovered: {total_tests}",
            "=" * 60,
            ""
        ]

        # Add category counts
        for category in ['regression', 'integration', 'development', 'slow', 'skip_ci', 'uncategorized']:
            count = categories.get(category, 0)
            if count > 0:
                lines.append(f"{category.title()}: {count}")

        # Level 2: Add uncategorized test details
        if verbosity >= 2 and 'uncategorized_tests' in summary:
            lines.append("\n" + "=" * 40)
            lines.append("UNCATEGORIZED TESTS")
            lines.append("=" * 40)
            for test in summary['uncategorized_tests']:
                lines.append(f"  • {test['name']} ({test.get('file', 'unknown')})")

        # Level 3: Add all test details
        if verbosity >= 3 and 'tests_by_category' in summary:
            tests_by_category = summary['tests_by_category']
            for category in ['regression', 'integration', 'development', 'slow', 'skip_ci']:
                if category in tests_by_category and tests_by_category[category]:
                    lines.append(f"\n" + "=" * 40)
                    lines.append(f"{category.upper()} TESTS")
                    lines.append("=" * 40)
                    for test in tests_by_category[category]:
                        decorators = test.get('decorators', [])
                        decorator_str = f" [{', '.join(decorators)}]" if decorators else ""
                        lines.append(f"  • {test['name']} ({test.get('file', 'unknown')}){decorator_str}")

        lines.append("\n" + "=" * 60)
        return '\n'.join(lines)


class JSONOutputStrategy(OutputStrategy):
    """JSON output formatting strategy."""
    
    def format_test_result(self, test_result: TestResult, verbosity: int = 1) -> str:
        """Format test result in JSON format."""
        import json
        return json.dumps(test_result.to_dict(verbosity), indent=2)
    
    def format_run_summary(self, summary: TestRunSummary) -> str:
        """Format test run summary in JSON format."""
        import json
        return json.dumps(summary.to_dict(), indent=2)
    
    def format_header(self, command: str, start_time: datetime) -> str:
        """Format header in JSON format."""
        import json
        header_data = {
            "run_info": {
                "command": command,
                "start_time": start_time.isoformat(),
                "format": "json"
            }
        }
        return json.dumps(header_data, indent=2)

    def format_discovery_results(self, discovery_metadata: Dict[str, Any]) -> str:
        """Format discovery results in JSON format."""
        import json
        discovery_data = {
            "discovery_results": {
                "timestamp": discovery_metadata.get('timestamp', datetime.now()).isoformat(),
                "total_tests": discovery_metadata.get('total_tests', 0),
                "categories": discovery_metadata.get('categories', 0),
                "discovered_tests": discovery_metadata.get('discovered_tests', {})
            }
        }
        return json.dumps(discovery_data, indent=2)

    def format_discovery_summary(self, discovery_data: Dict[str, Any], verbosity: int = 1) -> str:
        """Format discovery summary in JSON format."""
        import json
        # Return the discovery data directly as JSON (it's already in the correct format)
        return json.dumps(discovery_data, indent=2)


class OutputObserver(ABC):
    """Abstract base class for output observers."""
    
    @abstractmethod
    def notify(self, event: TestEvent) -> None:
        """Handle a test event notification.
        
        Args:
            event: The test event to handle
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the observer and clean up resources."""
        pass


class ConsoleOutputObserver(OutputObserver):
    """Observer that outputs to console/stdout."""
    
    def __init__(self, strategy: OutputStrategy, use_color: bool = True, quiet: bool = False):
        """Initialize console output observer.
        
        Args:
            strategy: Output formatting strategy
            use_color: Whether to use colored output
            quiet: Whether to suppress non-error output
        """
        self.strategy = strategy
        self.use_color = use_color
        self.quiet = quiet
        self.lock = threading.Lock()
    
    def notify(self, event: TestEvent) -> None:
        """Handle test event by printing to console."""
        if self.quiet and event.event_type not in ['run_end']:
            return

        with self.lock:
            if event.event_type == 'run_start':
                if event.metadata.get('command') and event.metadata.get('start_time'):
                    header = self.strategy.format_header(
                        event.metadata['command'],
                        event.metadata['start_time']
                    )
                    print(header)

            elif event.event_type == 'test_start':
                # Always show test start for debugging hanging tests
                test_name = event.metadata.get('test_name', 'Unknown')
                test_class = event.metadata.get('test_class', 'Unknown')
                full_name = f"{test_class}.{test_name}"
                print(f"Starting {full_name}...", end=" ", flush=True)

            elif event.event_type == 'test_end' and event.test_result:
                result_text = self.strategy.format_test_result(event.test_result)
                if self.use_color:
                    result_text = self._colorize_output(result_text, event.test_result.status.value)
                print(result_text)

            elif event.event_type == 'run_end' and event.run_summary:
                summary_text = self.strategy.format_run_summary(event.run_summary)
                print(summary_text)
    
    def _colorize_output(self, text: str, status: str) -> str:
        """Add color codes to output text based on status."""
        color_codes = {
            'PASS': '\033[92m',  # Green
            'FAIL': '\033[91m',  # Red
            'ERROR': '\033[91m', # Red
            'SKIP': '\033[93m'   # Yellow
        }
        reset_code = '\033[0m'
        
        color = color_codes.get(status, '')
        if color:
            return f"{color}{text}{reset_code}"
        return text
    
    def close(self) -> None:
        """Close console observer (no cleanup needed)."""
        pass


class FileOutputObserver(OutputObserver):
    """Observer that outputs to files using ThreadedFileWriter."""
    
    def __init__(self, file_path: str, strategy: OutputStrategy, 
                 verbosity: int = 1, threaded: bool = True, append_mode: bool = False):
        """Initialize file output observer.
        
        Args:
            file_path: Path to output file
            strategy: Output formatting strategy
            verbosity: Output verbosity level
            threaded: Whether to use threaded file writing
            append_mode: Whether to append to existing file
        """
        self.file_path = file_path
        self.strategy = strategy
        self.verbosity = verbosity
        self.threaded = threaded
        self.append_mode = append_mode
        
        # Determine format from strategy
        if isinstance(strategy, JSONOutputStrategy):
            format_type = 'json'
        else:
            format_type = 'txt'
        
        if threaded:
            self.writer = ThreadedFileWriter(
                file_path=file_path,
                format_type=format_type,
                verbosity=verbosity,
                append_mode=append_mode
            )
        else:
            # Direct file writing for testing
            self.file_handle = open(file_path, 'a' if append_mode else 'w', encoding='utf-8')
            self.writer = None
    
    def notify(self, event: TestEvent) -> None:
        """Handle test event by writing to file."""
        if event.event_type == 'run_start':
            if event.metadata.get('command') and event.metadata.get('start_time'):
                if self.writer:
                    self.writer.write_header(
                        event.metadata['command'],
                        event.metadata['start_time'].isoformat()
                    )
                else:
                    header = self.strategy.format_header(
                        event.metadata['command'],
                        event.metadata['start_time']
                    )
                    self.file_handle.write(header + '\n')
        
        elif event.event_type == 'test_end' and event.test_result:
            if self.writer:
                self.writer.write_test_result(event.test_result)
            else:
                result_text = self.strategy.format_test_result(event.test_result, self.verbosity)
                self.file_handle.write(result_text + '\n')
        
        elif event.event_type == 'run_end' and event.run_summary:
            if self.writer:
                self.writer.write_summary(event.run_summary)
            else:
                summary_text = self.strategy.format_run_summary(event.run_summary)
                self.file_handle.write(summary_text + '\n')

        elif event.event_type == 'discovery_complete':
            # Handle discovery results for file output
            if event.metadata.get('discovered_tests'):
                if self.writer:
                    # Use ThreadedFileWriter for discovery output
                    self.writer.write_discovery_results(event.metadata)
                else:
                    # Direct file writing for discovery output
                    discovery_text = self.strategy.format_discovery_results(event.metadata)
                    self.file_handle.write(discovery_text + '\n')
                    self.file_handle.flush()

        elif event.event_type == 'discovery_summary':
            # Handle discovery summary output (new enhanced discovery feature)
            discovery_data = event.metadata.get('discovery_data')
            discovery_output = event.metadata.get('discovery_output', '')

            if discovery_data:
                # Use strategy to format structured discovery data (supports JSON)
                formatted_output = self.strategy.format_discovery_summary(discovery_data, event.metadata.get('verbosity', 1))
                if self.writer:
                    # Use ThreadedFileWriter for discovery output
                    self.writer.write_text(formatted_output)
                else:
                    # Direct file writing for discovery output
                    self.file_handle.write(formatted_output + '\n')
                    self.file_handle.flush()
            elif discovery_output:
                # Fallback to plain text output
                if self.writer:
                    # Use ThreadedFileWriter for discovery output
                    self.writer.write_text(discovery_output)
                else:
                    # Direct file writing for discovery output
                    self.file_handle.write(discovery_output + '\n')
                    self.file_handle.flush()
    
    def close(self) -> None:
        """Close file observer and clean up resources."""
        if self.writer:
            self.writer.close()
        elif hasattr(self, 'file_handle'):
            self.file_handle.close()


class OutputEventPublisher:
    """Central event publisher for the output system."""
    
    def __init__(self):
        """Initialize the event publisher."""
        self.observers: List[OutputObserver] = []
        self.lock = threading.Lock()
        self.event_count = 0
    
    def add_observer(self, observer: OutputObserver) -> None:
        """Add an observer to receive event notifications.
        
        Args:
            observer: The observer to add
        """
        with self.lock:
            self.observers.append(observer)
    
    def remove_observer(self, observer: OutputObserver) -> None:
        """Remove an observer from event notifications.
        
        Args:
            observer: The observer to remove
        """
        with self.lock:
            if observer in self.observers:
                self.observers.remove(observer)
    
    def notify_all(self, event: TestEvent) -> None:
        """Notify all observers of an event.
        
        Args:
            event: The event to broadcast
        """
        with self.lock:
            observers_snapshot = self.observers.copy()
            self.event_count += 1
        
        if len(observers_snapshot) > 1:
            self._notify_parallel(observers_snapshot, event)
        else:
            self._notify_sequential(observers_snapshot, event)
    
    def _notify_parallel(self, observers: List[OutputObserver], event: TestEvent) -> None:
        """Notify observers in parallel using threads.
        
        Args:
            observers: List of observers to notify
            event: The event to send
        """
        threads = []
        for observer in observers:
            thread = threading.Thread(
                target=self._safe_notify,
                args=(observer, event),
                name=f"Notify-{type(observer).__name__}"
            )
            thread.start()
            threads.append(thread)
        
        # Wait for all notifications to complete
        for thread in threads:
            thread.join()
    
    def _notify_sequential(self, observers: List[OutputObserver], event: TestEvent) -> None:
        """Notify observers sequentially.
        
        Args:
            observers: List of observers to notify
            event: The event to send
        """
        for observer in observers:
            self._safe_notify(observer, event)
    
    def _safe_notify(self, observer: OutputObserver, event: TestEvent) -> None:
        """Safely notify an observer, catching and logging exceptions.
        
        Args:
            observer: The observer to notify
            event: The event to send
        """
        try:
            observer.notify(event)
        except Exception as e:
            # Log error but don't let it stop other observers
            print(f"Error in observer {type(observer).__name__}: {e}", file=sys.stderr)
    
    def close_all(self) -> None:
        """Close all observers and clean up resources."""
        with self.lock:
            for observer in self.observers:
                try:
                    observer.close()
                except Exception as e:
                    print(f"Error closing observer {type(observer).__name__}: {e}",
                          file=sys.stderr)
            self.observers.clear()
    
    def get_observer_count(self) -> int:
        """Get the number of registered observers.
        
        Returns:
            Number of observers
        """
        with self.lock:
            return len(self.observers)
    
    def get_event_count(self) -> int:
        """Get the total number of events published.
        
        Returns:
            Number of events published
        """
        return self.event_count

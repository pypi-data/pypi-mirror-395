"""Tests for wobble output architecture.

This module tests the Observer + Strategy pattern implementation,
parallel notification system, and output formatting strategies.
"""

import unittest
import tempfile
import threading
import time
import json
import io
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the parent directory to the path for imports during testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from wobble.output_architecture import (
    TestEvent, OutputStrategy, StandardOutputStrategy, VerboseOutputStrategy,
    JSONOutputStrategy, OutputObserver, ConsoleOutputObserver, FileOutputObserver,
    OutputEventPublisher
)
from wobble.data_structures import TestResult, TestStatus, ErrorInfo, TestRunSummary


class TestTestEvent(unittest.TestCase):
    """Test TestEvent dataclass."""
    
    def test_test_event_creation(self):
        """Test TestEvent creation with different event types."""
        # Test with test result
        timestamp = datetime(2024, 1, 15, 14, 30, 25)
        test_result = TestResult(
            name="test_example",
            classname="TestClass",
            status=TestStatus.PASS,
            duration=0.1,
            timestamp=timestamp
        )
        
        event = TestEvent(
            event_type='test_end',
            test_result=test_result,
            metadata={'category': 'unit'}
        )
        
        self.assertEqual(event.event_type, 'test_end')
        self.assertEqual(event.test_result, test_result)
        self.assertIsNone(event.run_summary)
        self.assertEqual(event.metadata['category'], 'unit')
        self.assertIsInstance(event.timestamp, float)


class TestOutputStrategies(unittest.TestCase):
    """Test output formatting strategies."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.timestamp = datetime(2024, 1, 15, 14, 30, 25)
        self.test_result = TestResult(
            name="test_example",
            classname="TestClass",
            status=TestStatus.PASS,
            duration=0.123,
            timestamp=self.timestamp
        )
        
        self.failed_result = TestResult(
            name="test_failure",
            classname="TestClass",
            status=TestStatus.FAIL,
            duration=0.456,
            timestamp=self.timestamp,
            error_info=ErrorInfo(
                type="AssertionError",
                message="Expected 5, got 3",
                traceback="Traceback (most recent call last)..."
            )
        )
        
        self.summary = TestRunSummary(
            total_tests=2,
            passed=1,
            failed=1,
            errors=0,
            skipped=0,
            duration=0.579,
            start_time=self.timestamp,
            end_time=self.timestamp,
            command="wobble tests/"
        )
    
    def test_standard_output_strategy(self):
        """Test StandardOutputStrategy formatting."""
        strategy = StandardOutputStrategy()
        
        # Test passing result
        result_text = strategy.format_test_result(self.test_result)
        self.assertIn("✓", result_text)
        self.assertIn("TestClass.test_example", result_text)
        self.assertIn("0.123s", result_text)
        
        # Test failing result with verbosity
        result_text = strategy.format_test_result(self.failed_result, verbosity=2)
        self.assertIn("✗", result_text)
        self.assertIn("Error:", result_text)
        self.assertIn("AssertionError", result_text)
        
        # Test summary
        summary_text = strategy.format_run_summary(self.summary)
        self.assertIn("=== Test Run Summary ===", summary_text)
        self.assertIn("Total: 2", summary_text)
        self.assertIn("Passed: 1", summary_text)
        self.assertIn("Failed: 1", summary_text)
        
        # Test header
        header_text = strategy.format_header("wobble tests/", self.timestamp)
        self.assertIn("Running: wobble tests/", header_text)
        self.assertIn("2024-01-15 14:30:25", header_text)
    
    def test_verbose_output_strategy(self):
        """Test VerboseOutputStrategy formatting."""
        strategy = VerboseOutputStrategy()
        
        # Test result formatting
        result_text = strategy.format_test_result(self.test_result)
        self.assertIn("Test: TestClass.test_example", result_text)
        self.assertIn("Status: PASS", result_text)
        self.assertIn("Duration: 0.123000s", result_text)
        self.assertIn("Timestamp:", result_text)
        
        # Test failed result with traceback
        result_text = strategy.format_test_result(self.failed_result, verbosity=3)
        self.assertIn("Error Type: AssertionError", result_text)
        self.assertIn("Traceback:", result_text)
        
        # Test summary
        summary_text = strategy.format_run_summary(self.summary)
        self.assertIn("=== Detailed Test Run Summary ===", summary_text)
        self.assertIn("Command: wobble tests/", summary_text)
        self.assertIn("Success Rate: 50.00%", summary_text)
        
        # Test header
        header_text = strategy.format_header("wobble tests/", self.timestamp)
        self.assertIn("WOBBLE TEST EXECUTION", header_text)
        self.assertIn("Command: wobble tests/", header_text)
    
    def test_json_output_strategy(self):
        """Test JSONOutputStrategy formatting."""
        strategy = JSONOutputStrategy()
        
        # Test result formatting
        result_text = strategy.format_test_result(self.test_result)
        result_data = json.loads(result_text)
        self.assertEqual(result_data['name'], 'test_example')
        self.assertEqual(result_data['status'], 'PASS')
        self.assertEqual(result_data['duration'], 0.123)
        
        # Test summary formatting
        summary_text = strategy.format_run_summary(self.summary)
        summary_data = json.loads(summary_text)
        self.assertEqual(summary_data['summary']['total_tests'], 2)
        self.assertEqual(summary_data['summary']['passed'], 1)
        
        # Test header formatting
        header_text = strategy.format_header("wobble tests/", self.timestamp)
        header_data = json.loads(header_text)
        self.assertEqual(header_data['run_info']['command'], 'wobble tests/')


class TestConsoleOutputObserver(unittest.TestCase):
    """Test ConsoleOutputObserver functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.strategy = StandardOutputStrategy()
        self.timestamp = datetime(2024, 1, 15, 14, 30, 25)
        self.test_result = TestResult(
            name="test_example",
            classname="TestClass",
            status=TestStatus.PASS,
            duration=0.123,
            timestamp=self.timestamp
        )
    
    def test_console_observer_creation(self):
        """Test ConsoleOutputObserver initialization."""
        observer = ConsoleOutputObserver(self.strategy, use_color=True, quiet=False)
        
        self.assertEqual(observer.strategy, self.strategy)
        self.assertTrue(observer.use_color)
        self.assertFalse(observer.quiet)
        # Check that lock is a lock object (type varies by Python version)
        self.assertTrue(hasattr(observer.lock, 'acquire'))
        self.assertTrue(hasattr(observer.lock, 'release'))
    
    @patch('builtins.print')
    def test_console_observer_test_event(self, mock_print):
        """Test console observer handling test events."""
        observer = ConsoleOutputObserver(self.strategy, use_color=False)
        
        event = TestEvent(
            event_type='test_end',
            test_result=self.test_result
        )
        
        observer.notify(event)
        
        # Verify print was called
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("test_example", call_args)
        self.assertIn("✓", call_args)
    
    @patch('builtins.print')
    def test_console_observer_quiet_mode(self, mock_print):
        """Test console observer in quiet mode."""
        observer = ConsoleOutputObserver(self.strategy, quiet=True)
        
        # Test event should be suppressed in quiet mode
        event = TestEvent(
            event_type='test_end',
            test_result=self.test_result
        )
        
        observer.notify(event)
        mock_print.assert_not_called()
        
        # Run end event should still be printed
        summary = TestRunSummary(
            total_tests=1, passed=1, failed=0, errors=0, skipped=0,
            duration=0.123, start_time=self.timestamp, end_time=self.timestamp,
            command="wobble tests/"
        )
        
        run_end_event = TestEvent(
            event_type='run_end',
            run_summary=summary
        )
        
        observer.notify(run_end_event)
        mock_print.assert_called_once()
    
    def test_console_observer_colorization(self):
        """Test console output colorization."""
        observer = ConsoleOutputObserver(self.strategy, use_color=True)
        
        # Test different status colors
        pass_text = observer._colorize_output("PASS", "PASS")
        self.assertIn('\033[92m', pass_text)  # Green
        self.assertIn('\033[0m', pass_text)   # Reset
        
        fail_text = observer._colorize_output("FAIL", "FAIL")
        self.assertIn('\033[91m', fail_text)  # Red
        
        skip_text = observer._colorize_output("SKIP", "SKIP")
        self.assertIn('\033[93m', skip_text)  # Yellow


class TestFileOutputObserver(unittest.TestCase):
    """Test FileOutputObserver functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test_output.txt'
        self.strategy = StandardOutputStrategy()
        self.timestamp = datetime(2024, 1, 15, 14, 30, 25)
        self.test_result = TestResult(
            name="test_example",
            classname="TestClass",
            status=TestStatus.PASS,
            duration=0.123,
            timestamp=self.timestamp
        )
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_file_observer_creation(self):
        """Test FileOutputObserver initialization."""
        observer = FileOutputObserver(
            file_path=str(self.test_file),
            strategy=self.strategy,
            verbosity=2,
            threaded=False
        )
        
        self.assertEqual(observer.file_path, str(self.test_file))
        self.assertEqual(observer.strategy, self.strategy)
        self.assertEqual(observer.verbosity, 2)
        self.assertFalse(observer.threaded)
        
        observer.close()
    
    def test_file_observer_non_threaded_output(self):
        """Test file observer with non-threaded output."""
        observer = FileOutputObserver(
            file_path=str(self.test_file),
            strategy=self.strategy,
            threaded=False
        )
        
        # Send test event
        event = TestEvent(
            event_type='test_end',
            test_result=self.test_result
        )
        
        observer.notify(event)
        observer.close()
        
        # Verify file content
        content = self.test_file.read_text(encoding='utf-8')
        self.assertIn("test_example", content)
        self.assertIn("✓", content)
    
    def test_file_observer_json_strategy(self):
        """Test file observer with JSON strategy."""
        json_file = Path(self.temp_dir) / 'test_output.json'
        json_strategy = JSONOutputStrategy()
        
        observer = FileOutputObserver(
            file_path=str(json_file),
            strategy=json_strategy,
            threaded=False
        )
        
        # Send test event
        event = TestEvent(
            event_type='test_end',
            test_result=self.test_result
        )
        
        observer.notify(event)
        observer.close()
        
        # Verify JSON content
        content = json_file.read_text()
        self.assertIn('"name": "test_example"', content)
        self.assertIn('"status": "PASS"', content)


class TestOutputEventPublisher(unittest.TestCase):
    """Test OutputEventPublisher functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.publisher = OutputEventPublisher()
        self.timestamp = datetime(2024, 1, 15, 14, 30, 25)
        self.test_result = TestResult(
            name="test_example",
            classname="TestClass",
            status=TestStatus.PASS,
            duration=0.123,
            timestamp=self.timestamp
        )
    
    def test_publisher_creation(self):
        """Test OutputEventPublisher initialization."""
        self.assertEqual(len(self.publisher.observers), 0)
        self.assertEqual(self.publisher.event_count, 0)
        # Check that lock is a lock object (type varies by Python version)
        self.assertTrue(hasattr(self.publisher.lock, 'acquire'))
        self.assertTrue(hasattr(self.publisher.lock, 'release'))
    
    def test_add_remove_observers(self):
        """Test adding and removing observers."""
        strategy = StandardOutputStrategy()
        observer1 = ConsoleOutputObserver(strategy)
        observer2 = ConsoleOutputObserver(strategy)
        
        # Add observers
        self.publisher.add_observer(observer1)
        self.publisher.add_observer(observer2)
        
        self.assertEqual(self.publisher.get_observer_count(), 2)
        
        # Remove observer
        self.publisher.remove_observer(observer1)
        self.assertEqual(self.publisher.get_observer_count(), 1)
        
        # Remove non-existent observer (should not error)
        self.publisher.remove_observer(observer1)
        self.assertEqual(self.publisher.get_observer_count(), 1)
    
    def test_sequential_notification(self):
        """Test sequential notification with single observer."""
        mock_observer = MagicMock()
        self.publisher.add_observer(mock_observer)
        
        event = TestEvent(
            event_type='test_end',
            test_result=self.test_result
        )
        
        self.publisher.notify_all(event)
        
        # Verify observer was notified
        mock_observer.notify.assert_called_once_with(event)
        self.assertEqual(self.publisher.get_event_count(), 1)
    
    def test_parallel_notification(self):
        """Test parallel notification with multiple observers."""
        notification_times = []
        
        class TimingObserver:
            def __init__(self, delay):
                self.delay = delay
            
            def notify(self, event):
                time.sleep(self.delay)
                notification_times.append(time.time())
            
            def close(self):
                pass
        
        # Add observers with delays
        observer1 = TimingObserver(0.1)  # 100ms delay
        observer2 = TimingObserver(0.1)  # 100ms delay
        
        self.publisher.add_observer(observer1)
        self.publisher.add_observer(observer2)
        
        event = TestEvent(
            event_type='test_end',
            test_result=self.test_result
        )
        
        # Measure notification time
        start_time = time.time()
        self.publisher.notify_all(event)
        end_time = time.time()
        
        # Parallel execution should take ~100ms, not ~200ms
        total_time = end_time - start_time
        self.assertLess(total_time, 0.15, 
                       f"Parallel notification took {total_time:.3f}s, expected <0.15s")
        
        # Verify both observers were notified
        self.assertEqual(len(notification_times), 2)
    
    def test_error_handling_in_notification(self):
        """Test error handling when observer raises exception."""
        class ErrorObserver:
            def notify(self, event):
                raise ValueError("Test error")
            
            def close(self):
                pass
        
        mock_observer = MagicMock()
        error_observer = ErrorObserver()
        
        self.publisher.add_observer(mock_observer)
        self.publisher.add_observer(error_observer)
        
        event = TestEvent(
            event_type='test_end',
            test_result=self.test_result
        )
        
        # Should not raise exception, but should still notify good observer
        with patch('sys.stderr'):  # Suppress error output
            self.publisher.notify_all(event)
        
        # Good observer should still be called
        mock_observer.notify.assert_called_once_with(event)
    
    def test_close_all_observers(self):
        """Test closing all observers."""
        mock_observer1 = MagicMock()
        mock_observer2 = MagicMock()
        
        self.publisher.add_observer(mock_observer1)
        self.publisher.add_observer(mock_observer2)
        
        self.publisher.close_all()
        
        # Verify all observers were closed
        mock_observer1.close.assert_called_once()
        mock_observer2.close.assert_called_once()
        
        # Verify observers list is cleared
        self.assertEqual(self.publisher.get_observer_count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)

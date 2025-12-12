"""Tests for wobble data structures.

This module tests the dataclass-based data structures used for
test results, error information, and JSON serialization.
"""

import unittest
import json
from datetime import datetime
from pathlib import Path
import sys

# Add the parent directory to the path for imports during testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from wobble.data_structures import (
    TestStatus, ErrorInfo, TestResult, TestRunSummary,
    TestResultEncoder, serialize_test_results, format_test_results_text
)
from tests.test_data_utils import (
    get_test_result_template, get_timing_config, get_command_template
)


class TestTestStatus(unittest.TestCase):
    """Test TestStatus enumeration."""
    
    def test_status_values(self):
        """Test that status enum has correct values."""
        self.assertEqual(TestStatus.PASS.value, "PASS")
        self.assertEqual(TestStatus.FAIL.value, "FAIL")
        self.assertEqual(TestStatus.ERROR.value, "ERROR")
        self.assertEqual(TestStatus.SKIP.value, "SKIP")


class TestErrorInfo(unittest.TestCase):
    """Test ErrorInfo dataclass."""
    
    def test_error_info_creation(self):
        """Test basic ErrorInfo creation."""
        # Get error info template from centralized test data
        error_template = get_test_result_template('with_error_info')['error_info']

        error = ErrorInfo(
            type=error_template['type'],
            message=error_template['message'],
            traceback=error_template['traceback']
        )

        self.assertEqual(error.type, error_template['type'])
        self.assertEqual(error.message, error_template['message'])
        self.assertEqual(error.traceback, error_template['traceback'])
        self.assertIsNone(error.file_path)
        self.assertIsNone(error.line_number)
    
    def test_error_info_with_location(self):
        """Test ErrorInfo with file path and line number."""
        error = ErrorInfo(
            type="ValueError",
            message="Invalid input",
            traceback="Traceback...",
            file_path="/path/to/test.py",
            line_number=42
        )
        
        self.assertEqual(error.file_path, "/path/to/test.py")
        self.assertEqual(error.line_number, 42)
    
    def test_error_info_validation(self):
        """Test ErrorInfo validation in __post_init__."""
        # Test empty type
        with self.assertRaises(ValueError) as context:
            ErrorInfo(type="", message="test", traceback="trace")
        self.assertIn("Error type cannot be empty", str(context.exception))
        
        # Test empty message
        with self.assertRaises(ValueError) as context:
            ErrorInfo(type="TestError", message="", traceback="trace")
        self.assertIn("Error message cannot be empty", str(context.exception))
    
    def test_error_info_to_dict(self):
        """Test ErrorInfo to_dict method."""
        error = ErrorInfo(
            type="AssertionError",
            message="Test failed",
            traceback="Full traceback...",
            file_path="/test.py",
            line_number=10
        )
        
        result = error.to_dict()
        expected = {
            'type': 'AssertionError',
            'message': 'Test failed',
            'traceback': 'Full traceback...',
            'file_path': '/test.py',
            'line_number': 10
        }
        
        self.assertEqual(result, expected)
    
    def test_error_info_to_dict_minimal(self):
        """Test ErrorInfo to_dict with minimal data."""
        error = ErrorInfo(
            type="Error",
            message="Message",
            traceback="Trace"
        )
        
        result = error.to_dict()
        expected = {
            'type': 'Error',
            'message': 'Message',
            'traceback': 'Trace'
        }
        
        self.assertEqual(result, expected)


class TestTestResult(unittest.TestCase):
    """Test TestResult dataclass."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Get standard timestamp from centralized test data
        timestamp_str = get_timing_config('standard_timestamp')
        self.timestamp = datetime.fromisoformat(timestamp_str)

        # Get error info template from centralized test data
        error_template = get_test_result_template('with_error_info')['error_info']
        self.error_info = ErrorInfo(
            type=error_template['type'],
            message=error_template['message'],
            traceback=error_template['traceback']
        )
    
    def test_test_result_creation(self):
        """Test basic TestResult creation."""
        # Get test result template from centralized test data
        template = get_test_result_template('test_example')

        result = TestResult(
            name=template['name'],
            classname=template['classname'],
            status=TestStatus.PASS,
            duration=template['duration'],
            timestamp=self.timestamp
        )

        self.assertEqual(result.name, template['name'])
        self.assertEqual(result.classname, template['classname'])
        self.assertEqual(result.status, TestStatus.PASS)
        self.assertEqual(result.duration, template['duration'])
        self.assertEqual(result.timestamp, self.timestamp)
        self.assertEqual(result.metadata, {})
        self.assertIsNone(result.error_info)
        self.assertIsNone(result.captured_output)
    
    def test_test_result_with_error(self):
        """Test TestResult with error information."""
        result = TestResult(
            name="test_failure",
            classname="TestClass",
            status=TestStatus.FAIL,
            duration=0.456,
            timestamp=self.timestamp,
            metadata={"category": "regression"},
            error_info=self.error_info
        )
        
        self.assertEqual(result.status, TestStatus.FAIL)
        self.assertEqual(result.metadata["category"], "regression")
        self.assertEqual(result.error_info, self.error_info)
    
    def test_test_result_validation(self):
        """Test TestResult validation in __post_init__."""
        # Test negative duration
        with self.assertRaises(ValueError) as context:
            TestResult(
                name="test",
                classname="TestClass",
                status=TestStatus.PASS,
                duration=-1.0,
                timestamp=self.timestamp
            )
        self.assertIn("Duration cannot be negative", str(context.exception))
        
        # Test empty name
        with self.assertRaises(ValueError) as context:
            TestResult(
                name="",
                classname="TestClass",
                status=TestStatus.PASS,
                duration=1.0,
                timestamp=self.timestamp
            )
        self.assertIn("Test name cannot be empty", str(context.exception))
        
        # Test empty classname
        with self.assertRaises(ValueError) as context:
            TestResult(
                name="test",
                classname="",
                status=TestStatus.PASS,
                duration=1.0,
                timestamp=self.timestamp
            )
        self.assertIn("Test class name cannot be empty", str(context.exception))
    
    def test_test_result_to_dict_level_1(self):
        """Test TestResult to_dict with verbosity level 1 (Standard)."""
        result = TestResult(
            name="test_example",
            classname="TestClass",
            status=TestStatus.PASS,
            duration=0.123456,
            timestamp=self.timestamp,
            metadata={"category": "unit"},
            error_info=self.error_info  # Should not be included at level 1
        )
        
        result_dict = result.to_dict(verbosity=1)
        
        expected = {
            'name': 'test_example',
            'classname': 'TestClass',
            'status': 'PASS',
            'duration': 0.123456,
            'timestamp': self.timestamp.isoformat(),
            'metadata': {'category': 'unit'}
        }
        
        self.assertEqual(result_dict, expected)
        self.assertNotIn('error_info', result_dict)
        self.assertNotIn('environment', result_dict)
    
    def test_test_result_to_dict_level_2(self):
        """Test TestResult to_dict with verbosity level 2 (Detailed)."""
        result = TestResult(
            name="test_failure",
            classname="TestClass",
            status=TestStatus.FAIL,
            duration=0.123,
            timestamp=self.timestamp,
            error_info=self.error_info
        )
        
        result_dict = result.to_dict(verbosity=2)
        
        self.assertIn('error_info', result_dict)
        self.assertIn('full_name', result_dict)
        self.assertEqual(result_dict['full_name'], 'TestClass.test_failure')
        self.assertEqual(result_dict['error_info']['type'], 'AssertionError')
        self.assertNotIn('environment', result_dict)
    
    def test_test_result_to_dict_level_3(self):
        """Test TestResult to_dict with verbosity level 3 (Complete)."""
        result = TestResult(
            name="test_complete",
            classname="TestClass",
            status=TestStatus.PASS,
            duration=0.123,
            timestamp=self.timestamp,
            captured_output={'stdout': 'output', 'stderr': 'error'}
        )
        
        result_dict = result.to_dict(verbosity=3)
        
        self.assertIn('environment', result_dict)
        self.assertIn('captured_output', result_dict)
        self.assertIn('python_version', result_dict['environment'])
        self.assertIn('platform', result_dict['environment'])
        self.assertEqual(result_dict['captured_output']['stdout'], 'output')


class TestTestRunSummary(unittest.TestCase):
    """Test TestRunSummary dataclass."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.start_time = datetime(2024, 1, 15, 14, 30, 0)
        self.end_time = datetime(2024, 1, 15, 14, 30, 5)
    
    def test_test_run_summary_creation(self):
        """Test basic TestRunSummary creation."""
        summary = TestRunSummary(
            total_tests=10,
            passed=8,
            failed=1,
            errors=0,
            skipped=1,
            duration=5.0,
            start_time=self.start_time,
            end_time=self.end_time,
            command="wobble tests/"
        )
        
        self.assertEqual(summary.total_tests, 10)
        self.assertEqual(summary.passed, 8)
        self.assertEqual(summary.failed, 1)
        self.assertEqual(summary.errors, 0)
        self.assertEqual(summary.skipped, 1)
        self.assertEqual(summary.duration, 5.0)
        self.assertEqual(summary.command, "wobble tests/")
        self.assertEqual(summary.exit_code, 0)
    
    def test_test_run_summary_validation(self):
        """Test TestRunSummary validation in __post_init__."""
        # Test negative total tests
        with self.assertRaises(ValueError):
            TestRunSummary(
                total_tests=-1, passed=0, failed=0, errors=0, skipped=0,
                duration=1.0, start_time=self.start_time, end_time=self.end_time,
                command="test"
            )
        
        # Test counts don't sum to total
        with self.assertRaises(ValueError):
            TestRunSummary(
                total_tests=10, passed=5, failed=2, errors=1, skipped=1,  # Sum = 9, not 10
                duration=1.0, start_time=self.start_time, end_time=self.end_time,
                command="test"
            )
        
        # Test end time before start time
        with self.assertRaises(ValueError):
            TestRunSummary(
                total_tests=1, passed=1, failed=0, errors=0, skipped=0,
                duration=1.0, start_time=self.end_time, end_time=self.start_time,
                command="test"
            )
    
    def test_success_rate_calculation(self):
        """Test success rate property calculation."""
        summary = TestRunSummary(
            total_tests=10, passed=8, failed=1, errors=0, skipped=1,
            duration=1.0, start_time=self.start_time, end_time=self.end_time,
            command="test"
        )
        
        self.assertEqual(summary.success_rate, 80.0)
        
        # Test with zero tests
        summary_empty = TestRunSummary(
            total_tests=0, passed=0, failed=0, errors=0, skipped=0,
            duration=0.0, start_time=self.start_time, end_time=self.start_time,
            command="test"
        )
        
        self.assertEqual(summary_empty.success_rate, 100.0)
    
    def test_test_run_summary_to_dict(self):
        """Test TestRunSummary to_dict method."""
        summary = TestRunSummary(
            total_tests=5, passed=4, failed=1, errors=0, skipped=0,
            duration=2.5, start_time=self.start_time, end_time=self.end_time,
            command="wobble --verbose", exit_code=1
        )
        
        result = summary.to_dict()
        
        self.assertEqual(result['summary']['total_tests'], 5)
        self.assertEqual(result['summary']['passed'], 4)
        self.assertEqual(result['summary']['failed'], 1)
        self.assertEqual(result['summary']['success_rate'], 80.0)
        self.assertEqual(result['timing']['duration'], 2.5)
        self.assertEqual(result['execution']['command'], "wobble --verbose")
        self.assertEqual(result['execution']['exit_code'], 1)


class TestSerialization(unittest.TestCase):
    """Test serialization functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.timestamp = datetime(2024, 1, 15, 14, 30, 25)
        self.test_results = [
            TestResult(
                name="test_pass",
                classname="TestClass",
                status=TestStatus.PASS,
                duration=0.1,
                timestamp=self.timestamp
            ),
            TestResult(
                name="test_fail",
                classname="TestClass",
                status=TestStatus.FAIL,
                duration=0.2,
                timestamp=self.timestamp,
                error_info=ErrorInfo(
                    type="AssertionError",
                    message="Test failed",
                    traceback="Traceback..."
                )
            )
        ]
        
        self.summary = TestRunSummary(
            total_tests=2, passed=1, failed=1, errors=0, skipped=0,
            duration=0.3, start_time=self.timestamp, end_time=self.timestamp,
            command="wobble tests/"
        )
    
    def test_serialize_test_results_json(self):
        """Test JSON serialization of test results."""
        json_str = serialize_test_results(self.test_results, self.summary, verbosity=1)
        
        # Parse back to verify structure
        data = json.loads(json_str)
        
        self.assertIn('run_info', data)
        self.assertIn('test_results', data)
        self.assertEqual(len(data['test_results']), 2)
        self.assertEqual(data['test_results'][0]['name'], 'test_pass')
        self.assertEqual(data['test_results'][1]['name'], 'test_fail')
    
    def test_format_test_results_text(self):
        """Test text formatting of test results."""
        text = format_test_results_text(self.test_results, self.summary, verbosity=1)
        
        self.assertIn("=== Wobble Test Run Results ===", text)
        self.assertIn("wobble tests/", text)
        self.assertIn("test_pass", text)
        self.assertIn("test_fail", text)
        self.assertIn("=== Summary ===", text)
        self.assertIn("Total: 2", text)
        self.assertIn("Passed: 1", text)
        self.assertIn("Failed: 1", text)


if __name__ == '__main__':
    unittest.main(verbosity=2)

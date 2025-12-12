"""Tests for core integration of file output system.

This module tests the integration between WobbleTestResult, TestRunner,
and the enhanced output system with file output capabilities.
"""

import unittest
import tempfile
import time
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import sys

# Add the parent directory to the path for imports during testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from wobble.runner import WobbleTestResult, TestRunner
from wobble.enhanced_output import EnhancedOutputFormatter
from wobble.output import OutputFormatter
from wobble.data_structures import TestResult, TestStatus, ErrorInfo


# Helper function to create mock test instances
def create_mock_test(class_name: str, method_name: str, metadata: dict = None):
    """Create a mock test case instance for testing purposes."""

    class MockTestForIntegration(unittest.TestCase):
        """Mock test case for testing."""

        def __init__(self):
            super().__init__(methodName='runTest')
            self.__class__.__name__ = class_name
            self._testMethodName = method_name
            self._wobble_metadata = metadata or {}

        def runTest(self):
            """Default test method."""
            pass

    return MockTestForIntegration()


class TestWobbleTestResultIntegration(unittest.TestCase):
    """Test WobbleTestResult integration with enhanced output."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test_output.txt'
        
        # Create file output configuration
        self.file_config = {
            'filename': str(self.test_file),
            'format': 'txt',
            'verbosity': 1,
            'append': False
        }
        
        # Create enhanced output formatter
        self.enhanced_formatter = EnhancedOutputFormatter(
            format_type='standard',
            use_color=False,
            quiet=True,  # Suppress console output for testing
            file_outputs=[self.file_config]
        )
        
        # Create standard output formatter for comparison
        self.standard_formatter = OutputFormatter(
            format_type='standard',
            use_color=False,
            quiet=True
        )
    
    def tearDown(self):
        """Clean up test environment."""
        self.enhanced_formatter.close()
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_wobble_test_result_enhanced_mode_detection(self):
        """Test that WobbleTestResult correctly detects enhanced mode."""
        # Test with enhanced formatter
        enhanced_result = WobbleTestResult(self.enhanced_formatter)
        self.assertTrue(enhanced_result.enhanced_mode)
        
        # Test with standard formatter
        standard_result = WobbleTestResult(self.standard_formatter)
        self.assertFalse(standard_result.enhanced_mode)
    
    def test_test_success_integration(self):
        """Test successful test integration with enhanced output."""
        result = WobbleTestResult(self.enhanced_formatter)
        test_case = create_mock_test("TestClass", "test_success")
        
        # Simulate test execution
        result.startTest(test_case)
        time.sleep(0.01)  # Small delay to ensure duration > 0
        result.addSuccess(test_case)
        result.stopTest(test_case)
        
        # Verify test was recorded in enhanced formatter
        self.assertEqual(len(self.enhanced_formatter.test_results), 1)
        test_result = self.enhanced_formatter.test_results[0]
        
        self.assertEqual(test_result.name, "test_success")
        self.assertEqual(test_result.classname, "TestClass")
        self.assertEqual(test_result.status, TestStatus.PASS)
        self.assertGreater(test_result.duration, 0)
    
    def test_test_failure_integration(self):
        """Test failed test integration with enhanced output."""
        result = WobbleTestResult(self.enhanced_formatter)
        test_case = create_mock_test("TestClass", "test_failure")
        
        # Create error info
        try:
            raise AssertionError("Test assertion failed")
        except AssertionError:
            import sys
            err_info = sys.exc_info()
        
        # Simulate test execution
        result.startTest(test_case)
        time.sleep(0.01)
        result.addFailure(test_case, err_info)
        result.stopTest(test_case)
        
        # Verify test was recorded with error info
        self.assertEqual(len(self.enhanced_formatter.test_results), 1)
        test_result = self.enhanced_formatter.test_results[0]
        
        self.assertEqual(test_result.status, TestStatus.FAIL)
        self.assertIsNotNone(test_result.error_info)
        self.assertEqual(test_result.error_info.type, "AssertionError")
        self.assertIn("Test assertion failed", test_result.error_info.message)
    
    def test_test_error_integration(self):
        """Test test error integration with enhanced output."""
        result = WobbleTestResult(self.enhanced_formatter)
        test_case = create_mock_test("TestClass", "test_error")
        
        # Create error info
        try:
            raise ValueError("Test value error")
        except ValueError:
            import sys
            err_info = sys.exc_info()
        
        # Simulate test execution
        result.startTest(test_case)
        time.sleep(0.01)
        result.addError(test_case, err_info)
        result.stopTest(test_case)
        
        # Verify test was recorded with error info
        self.assertEqual(len(self.enhanced_formatter.test_results), 1)
        test_result = self.enhanced_formatter.test_results[0]
        
        self.assertEqual(test_result.status, TestStatus.ERROR)
        self.assertIsNotNone(test_result.error_info)
        self.assertEqual(test_result.error_info.type, "ValueError")
        self.assertIn("Test value error", test_result.error_info.message)
    
    def test_test_skip_integration(self):
        """Test skipped test integration with enhanced output."""
        result = WobbleTestResult(self.enhanced_formatter)
        test_case = create_mock_test("TestClass", "test_skip")
        
        # Simulate test execution
        result.startTest(test_case)
        result.addSkip(test_case, "Test skipped for testing")
        result.stopTest(test_case)
        
        # Verify test was recorded with skip reason
        self.assertEqual(len(self.enhanced_formatter.test_results), 1)
        test_result = self.enhanced_formatter.test_results[0]
        
        self.assertEqual(test_result.status, TestStatus.SKIP)
        self.assertEqual(test_result.metadata['skip_reason'], "Test skipped for testing")
    
    def test_metadata_extraction(self):
        """Test metadata extraction from test cases."""
        result = WobbleTestResult(self.enhanced_formatter)
        test_case = create_mock_test(
            "TestClass",
            "test_with_metadata",
            metadata={'category': 'integration', 'priority': 'high'}
        )
        
        # Simulate test execution
        result.startTest(test_case)
        result.addSuccess(test_case)
        result.stopTest(test_case)
        
        # Verify metadata was captured
        test_result = self.enhanced_formatter.test_results[0]
        self.assertEqual(test_result.metadata['category'], 'integration')
        self.assertEqual(test_result.metadata['priority'], 'high')


class TestTestRunnerIntegration(unittest.TestCase):
    """Test TestRunner integration with enhanced output."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test_output.json'
        
        # Create file output configuration
        self.file_config = {
            'filename': str(self.test_file),
            'format': 'json',
            'verbosity': 2,
            'append': False
        }
        
        # Create enhanced output formatter
        self.enhanced_formatter = EnhancedOutputFormatter(
            format_type='standard',
            use_color=False,
            quiet=True,
            file_outputs=[self.file_config]
        )
    
    def tearDown(self):
        """Clean up test environment."""
        self.enhanced_formatter.close()
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_test_runner_enhanced_mode_detection(self):
        """Test that TestRunner correctly detects enhanced mode."""
        runner = TestRunner(self.enhanced_formatter)
        self.assertTrue(runner.enhanced_mode)
        
        standard_formatter = OutputFormatter(format_type='standard')
        standard_runner = TestRunner(standard_formatter)
        self.assertFalse(standard_runner.enhanced_mode)
    
    def test_run_tests_with_enhanced_output(self):
        """Test running tests with enhanced output system."""
        runner = TestRunner(self.enhanced_formatter)
        
        # Create test infos
        test_infos = [
            {'test_case': create_mock_test("TestClass", "test_pass")},
            {'test_case': create_mock_test("TestClass", "test_fail")}
        ]
        
        # Mock the test execution to control results
        with patch.object(unittest.TestSuite, 'run') as mock_run:
            def mock_test_run(result):
                # Simulate test execution
                for test_info in test_infos:
                    test_case = test_info['test_case']
                    result.startTest(test_case)
                    
                    if test_case._testMethodName == "test_pass":
                        result.addSuccess(test_case)
                    else:
                        try:
                            raise AssertionError("Mock failure")
                        except AssertionError:
                            import sys
                            result.addFailure(test_case, sys.exc_info())
                    
                    result.stopTest(test_case)
                
                result.testsRun = len(test_infos)
            
            mock_run.side_effect = mock_test_run
            
            # Run tests
            results = runner.run_tests(test_infos)
        
        # Verify results
        self.assertEqual(results['tests_run'], 2)
        self.assertEqual(results['failures'], 1)
        self.assertEqual(results['errors'], 0)
        
        # Verify enhanced formatter captured results
        self.assertEqual(len(self.enhanced_formatter.test_results), 2)
        
        # Verify file output was created
        self.assertTrue(self.test_file.exists())

        # Close formatter to finalize file output
        self.enhanced_formatter.close()

        # Verify JSON content
        content = self.test_file.read_text()
        data = json.loads(content)
        
        self.assertIn('run_info', data)
        self.assertIn('test_results', data)
        self.assertEqual(len(data['test_results']), 2)
    
    def test_command_reconstruction_integration(self):
        """Test command reconstruction in test runner."""
        runner = TestRunner(self.enhanced_formatter)
        
        # Mock sys.argv to simulate command line
        with patch('sys.argv', ['wobble', 'tests/', '--verbose', '2']):
            test_infos = [{'test_case': create_mock_test("TestClass", "test_example")}]
            
            with patch.object(unittest.TestSuite, 'run') as mock_run:
                def mock_test_run(result):
                    test_case = test_infos[0]['test_case']
                    result.startTest(test_case)
                    result.addSuccess(test_case)
                    result.stopTest(test_case)
                    result.testsRun = 1
                
                mock_run.side_effect = mock_test_run
                
                # Run tests
                results = runner.run_tests(test_infos)
        
        # Verify command was captured in run summary
        self.assertIsNotNone(self.enhanced_formatter.run_command)
    
    def test_empty_test_list_handling(self):
        """Test handling of empty test list."""
        runner = TestRunner(self.enhanced_formatter)
        
        results = runner.run_tests([])
        
        # Verify empty results
        self.assertEqual(results['tests_run'], 0)
        self.assertEqual(results['failures'], 0)
        self.assertEqual(results['errors'], 0)
        self.assertEqual(results['success_rate'], 100.0)


class TestCLIIntegration(unittest.TestCase):
    """Test CLI integration with enhanced output system."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'cli_test_output.txt'
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('wobble.cli.TestDiscoveryEngine')
    @patch('wobble.cli.TestRunner')
    def test_cli_enhanced_formatter_selection(self, mock_runner_class, mock_discovery_class):
        """Test that CLI selects enhanced formatter when file outputs are configured."""
        from wobble.cli import main
        
        # Mock discovery and runner
        mock_discovery = MagicMock()
        mock_discovery.discover_tests.return_value = {'test': []}
        mock_discovery.filter_tests.return_value = [{'test_case': create_mock_test("Test", "test")}]
        mock_discovery_class.return_value = mock_discovery
        
        mock_runner = MagicMock()
        mock_runner.run_tests.return_value = {
            'tests_run': 1, 'failures': 0, 'errors': 0, 'skipped': 0,
            'success_rate': 100.0, 'total_time': 0.1
        }
        mock_runner_class.return_value = mock_runner
        
        # Test with file output arguments
        test_args = [
            'wobble', 'tests/',
            '--log-file', str(self.test_file),
            '--log-file-format', 'txt'
        ]
        
        with patch('sys.argv', test_args):
            exit_code = main()
        
        # Verify enhanced formatter was used
        self.assertEqual(exit_code, 0)
        mock_runner_class.assert_called_once()
        
        # Get the formatter passed to TestRunner
        formatter_arg = mock_runner_class.call_args[0][0]
        self.assertEqual(type(formatter_arg).__name__, 'EnhancedOutputFormatter')


if __name__ == '__main__':
    unittest.main(verbosity=2)

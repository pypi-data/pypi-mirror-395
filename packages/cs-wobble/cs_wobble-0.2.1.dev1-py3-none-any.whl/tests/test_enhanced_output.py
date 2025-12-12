"""Tests for enhanced output formatter.

This module tests the EnhancedOutputFormatter that integrates
the observer architecture with backward compatibility.
"""

import unittest
import tempfile
import time
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import sys

# Add the parent directory to the path for imports during testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from wobble.enhanced_output import EnhancedOutputFormatter
from wobble.data_structures import TestResult, TestStatus, ErrorInfo


class MockTest:
    """Mock test case for testing."""

    def __init__(self, class_name: str, method_name: str, metadata: dict = None):
        self.__class__.__name__ = class_name
        self._testMethodName = method_name
        self._wobble_metadata = metadata or {}


class TestEnhancedOutputFormatter(unittest.TestCase):
    """Test EnhancedOutputFormatter functionality."""
    
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
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_enhanced_formatter_creation(self):
        """Test EnhancedOutputFormatter initialization."""
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            use_color=True,
            verbosity=1,
            quiet=False,
            file_outputs=[self.file_config]
        )
        
        self.assertEqual(formatter.format_type, 'standard')
        self.assertTrue(formatter.use_color)
        self.assertEqual(formatter.verbosity, 1)
        self.assertFalse(formatter.quiet)
        self.assertEqual(len(formatter.file_outputs), 1)
        
        # Should have console + file observers
        self.assertEqual(formatter.publisher.get_observer_count(), 2)
        
        formatter.close()
    
    def test_console_only_output(self):
        """Test formatter with console output only."""
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            use_color=False,
            quiet=False
        )
        
        # Should have only console observer
        self.assertEqual(formatter.publisher.get_observer_count(), 1)
        
        formatter.close()
    
    def test_multiple_file_outputs(self):
        """Test formatter with multiple file outputs."""
        json_file = Path(self.temp_dir) / 'test_output.json'
        
        file_configs = [
            {
                'filename': str(self.test_file),
                'format': 'txt',
                'verbosity': 1
            },
            {
                'filename': str(json_file),
                'format': 'json',
                'verbosity': 2
            }
        ]
        
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            file_outputs=file_configs
        )
        
        # Should have console + 2 file observers
        self.assertEqual(formatter.publisher.get_observer_count(), 3)
        
        formatter.close()
    
    @patch('builtins.print')
    def test_test_run_lifecycle(self, mock_print):
        """Test complete test run lifecycle."""
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            use_color=False,
            file_outputs=[self.file_config]
        )
        
        # Start test run
        formatter.start_test_run("wobble tests/", 2)
        
        # Create mock test cases
        test_case_1 = MockTest("TestClass", "test_pass")
        test_case_2 = MockTest("TestClass", "test_fail")
        
        # Simulate test execution
        formatter.notify_test_start(test_case_1)
        formatter.print_test_success(test_case_1, 0.123)
        
        formatter.notify_test_start(test_case_2)
        err_info = (ValueError, ValueError("Test error"), None)
        formatter.print_test_failure(test_case_2, err_info, 0.456)
        
        # End test run
        formatter.end_test_run(exit_code=1)
        
        # Verify test results were collected
        self.assertEqual(len(formatter.test_results), 2)
        self.assertEqual(formatter.test_results[0].status, TestStatus.PASS)
        self.assertEqual(formatter.test_results[1].status, TestStatus.FAIL)
        
        formatter.close()
        
        # Verify file output was created
        self.assertTrue(self.test_file.exists())
        content = self.test_file.read_text()
        self.assertIn("test_pass", content)
        self.assertIn("test_fail", content)
    
    def test_backward_compatibility_methods(self):
        """Test backward compatibility with existing OutputFormatter interface."""
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            use_color=False,
            quiet=True  # Suppress console output for testing
        )
        
        # Test header method
        formatter.print_test_run_header(5)
        self.assertIsNotNone(formatter.run_start_time)
        
        # Test info/warning/error methods
        formatter.print_info("Test info")
        formatter.print_warning("Test warning")
        formatter.print_error("Test error")
        
        # Test discovery methods
        discovered_tests = {
            'regression': ['test1', 'test2'],
            'integration': ['test3']
        }
        formatter.print_discovery_summary(discovered_tests)
        formatter.print_test_categories(discovered_tests)
        
        formatter.close()
    
    def test_different_output_strategies(self):
        """Test different output strategies based on format type."""
        # Test verbose strategy
        verbose_formatter = EnhancedOutputFormatter(format_type='verbose')
        self.assertEqual(verbose_formatter.publisher.get_observer_count(), 1)
        verbose_formatter.close()
        
        # Test JSON strategy
        json_formatter = EnhancedOutputFormatter(format_type='json')
        self.assertEqual(json_formatter.publisher.get_observer_count(), 1)
        json_formatter.close()
        
        # Test minimal strategy (uses standard)
        minimal_formatter = EnhancedOutputFormatter(format_type='minimal')
        self.assertEqual(minimal_formatter.publisher.get_observer_count(), 1)
        minimal_formatter.close()
    
    def test_file_output_with_different_formats(self):
        """Test file output with different formats and verbosity levels."""
        json_file = Path(self.temp_dir) / 'test_output.json'
        
        file_configs = [
            {
                'filename': str(self.test_file),
                'format': 'txt',
                'verbosity': 2  # Should use verbose strategy
            },
            {
                'filename': str(json_file),
                'format': 'json',
                'verbosity': 1
            }
        ]
        
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            quiet=True,  # Suppress console output
            file_outputs=file_configs
        )
        
        # Run a simple test
        formatter.start_test_run("wobble tests/", 1)
        
        test_case = MockTest("TestClass", "test_example")
        formatter.print_test_success(test_case, 0.123)
        
        formatter.end_test_run()
        formatter.close()
        
        # Verify both files were created
        self.assertTrue(self.test_file.exists())
        self.assertTrue(json_file.exists())
        
        # Verify content formats
        txt_content = self.test_file.read_text()
        self.assertIn("test_example", txt_content)
        
        json_content = json_file.read_text()
        self.assertIn('"name": "test_example"', json_content)
    
    def test_error_handling_in_test_results(self):
        """Test error handling and error info creation."""
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            quiet=True
        )
        
        formatter.start_test_run("wobble tests/", 1)
        
        test_case = MockTest("TestClass", "test_error")
        
        # Create error info
        try:
            raise ValueError("Test error message")
        except ValueError:
            import sys
            err_info = sys.exc_info()
            formatter.print_test_error(test_case, err_info, 0.123)
        
        formatter.end_test_run()
        
        # Verify error was captured
        self.assertEqual(len(formatter.test_results), 1)
        result = formatter.test_results[0]
        self.assertEqual(result.status, TestStatus.ERROR)
        self.assertIsNotNone(result.error_info)
        self.assertEqual(result.error_info.type, "ValueError")
        self.assertIn("Test error message", result.error_info.message)
        
        formatter.close()
    
    def test_skip_handling(self):
        """Test handling of skipped tests."""
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            quiet=True
        )
        
        formatter.start_test_run("wobble tests/", 1)
        
        test_case = MockTest("TestClass", "test_skip")
        formatter.print_test_skip(test_case, "Test skipped for testing", 0.0)
        
        formatter.end_test_run()
        
        # Verify skip was captured
        self.assertEqual(len(formatter.test_results), 1)
        result = formatter.test_results[0]
        self.assertEqual(result.status, TestStatus.SKIP)
        self.assertEqual(result.metadata['skip_reason'], "Test skipped for testing")
        
        formatter.close()
    
    def test_context_manager(self):
        """Test context manager functionality."""
        with EnhancedOutputFormatter(format_type='standard') as formatter:
            formatter.start_test_run("wobble tests/", 1)
            
            test_case = MockTest("TestClass", "test_context")
            formatter.print_test_success(test_case, 0.123)
            
            formatter.end_test_run()
        
        # Formatter should be closed automatically
        self.assertEqual(formatter.publisher.get_observer_count(), 0)
    
    def test_test_metadata_handling(self):
        """Test handling of test metadata from decorators."""
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            quiet=True
        )
        
        formatter.start_test_run("wobble tests/", 1)
        
        # Test case with metadata
        test_case = MockTest(
            "TestClass",
            "test_with_metadata",
            metadata={'category': 'regression', 'priority': 'high'}
        )
        
        formatter.print_test_success(test_case, 0.123)
        formatter.end_test_run()
        
        # Verify metadata was captured
        result = formatter.test_results[0]
        self.assertEqual(result.metadata['category'], 'regression')
        self.assertEqual(result.metadata['priority'], 'high')
        
        formatter.close()
    
    def test_performance_with_many_tests(self):
        """Test performance with many test results."""
        formatter = EnhancedOutputFormatter(
            format_type='standard',
            quiet=True,
            file_outputs=[self.file_config]
        )
        
        formatter.start_test_run("wobble tests/", 100)
        
        # Simulate many tests
        start_time = time.time()
        
        for i in range(100):
            test_case = MockTest("TestClass", f"test_{i:03d}")
            formatter.print_test_success(test_case, 0.001)
        
        end_time = time.time()
        formatter.end_test_run()
        formatter.close()
        
        # Should complete quickly
        total_time = end_time - start_time
        self.assertLess(total_time, 1.0, f"Processing 100 tests took {total_time:.3f}s")
        
        # Verify all results were captured
        self.assertEqual(len(formatter.test_results), 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)

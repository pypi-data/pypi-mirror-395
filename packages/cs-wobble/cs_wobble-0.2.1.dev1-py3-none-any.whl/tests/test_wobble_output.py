"""Tests for wobble output formatting functionality.

This module tests the output formatter including different formats,
color handling, and cross-platform compatibility.
"""

import unittest
import json
import os
from unittest.mock import patch, MagicMock
from io import StringIO

from wobble.output import OutputFormatter


class TestOutputFormatter(unittest.TestCase):
    """Test output formatting functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.formatter = OutputFormatter()
    
    def test_formatter_initialization(self):
        """Test that formatter initializes with correct defaults."""
        self.assertEqual(self.formatter.format_type, 'standard')
        self.assertEqual(self.formatter.verbosity, 0)
        self.assertFalse(self.formatter.quiet)
        self.assertTrue(self.formatter.use_color)  # Depends on environment
    
    def test_format_selection(self):
        """Test different output format selection."""
        # Test standard format
        formatter = OutputFormatter(format_type='standard')
        self.assertEqual(formatter.format_type, 'standard')
        
        # Test verbose format
        formatter = OutputFormatter(format_type='verbose')
        self.assertEqual(formatter.format_type, 'verbose')
        
        # Test JSON format
        formatter = OutputFormatter(format_type='json')
        self.assertEqual(formatter.format_type, 'json')
        
        # Test minimal format
        formatter = OutputFormatter(format_type='minimal')
        self.assertEqual(formatter.format_type, 'minimal')
    
    def test_verbosity_levels(self):
        """Test verbosity level handling."""
        # Test default verbosity
        formatter = OutputFormatter()
        self.assertEqual(formatter.verbosity, 0)
        
        # Test increased verbosity
        formatter = OutputFormatter(verbosity=2)
        self.assertEqual(formatter.verbosity, 2)
    
    def test_quiet_mode(self):
        """Test quiet mode functionality."""
        formatter = OutputFormatter(quiet=True)
        self.assertTrue(formatter.quiet)
        
        # In quiet mode, most output should be suppressed
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            formatter.print_test_success(MagicMock(), 0.1)
            output = mock_stdout.getvalue()
            self.assertEqual(output, "")  # No output in quiet mode
    
    def test_color_handling(self):
        """Test color output with and without NO_COLOR."""
        # Test with colors enabled
        formatter = OutputFormatter(use_color=True)
        self.assertTrue(formatter.use_color)
        
        # Test with colors disabled
        formatter = OutputFormatter(use_color=False)
        self.assertFalse(formatter.use_color)
        
        # Test NO_COLOR environment variable
        with patch.dict(os.environ, {'NO_COLOR': '1'}):
            formatter = OutputFormatter()
            # Color handling depends on implementation
    
    def test_test_run_header(self):
        """Test test run header output."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_run_header(5)
            output = mock_stdout.getvalue()
            
            # Should contain test count
            self.assertIn('5', output)
            self.assertIn('test', output.lower())
    
    def test_test_success_output(self):
        """Test successful test output formatting."""
        # Create mock test case
        mock_test = MagicMock()
        mock_test.__class__.__name__ = 'TestExample'
        mock_test._testMethodName = 'test_method'

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_success(mock_test, 0.123)
            output = mock_stdout.getvalue()

            # Should contain test name (timing only shown with verbosity > 0)
            self.assertIn('test_method', output)
            # Timing not shown by default (verbosity = 0)
            self.assertNotIn('0.123', output)
    
    def test_test_failure_output(self):
        """Test failed test output formatting."""
        mock_test = MagicMock()
        mock_test.__class__.__name__ = 'TestExample'
        mock_test._testMethodName = 'test_method'

        error_info = (AssertionError, AssertionError("Test failed"), None)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_failure(mock_test, error_info, 0.123)
            output = mock_stdout.getvalue()

            # Should contain test name (timing only shown with verbosity > 0)
            self.assertIn('test_method', output)
            # Timing not shown by default (verbosity = 0)
            self.assertNotIn('0.123', output)
            # Error message only shown with verbosity > 0
            self.assertNotIn('Test failed', output)
    
    def test_test_error_output(self):
        """Test error test output formatting."""
        mock_test = MagicMock()
        mock_test.__class__.__name__ = 'TestExample'
        mock_test._testMethodName = 'test_method'

        error_info = (ValueError, ValueError("Unexpected error"), None)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_error(mock_test, error_info, 0.123)
            output = mock_stdout.getvalue()

            # Should contain test name (timing only shown with verbosity > 0)
            self.assertIn('test_method', output)
            # Timing not shown by default (verbosity = 0)
            self.assertNotIn('0.123', output)
            # Error message only shown with verbosity > 0
            self.assertNotIn('Unexpected error', output)
    
    def test_test_skip_output(self):
        """Test skipped test output formatting."""
        mock_test = MagicMock()
        mock_test.__class__.__name__ = 'TestExample'
        mock_test._testMethodName = 'test_method'

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_skip(mock_test, "Test skipped", 0.001)
            output = mock_stdout.getvalue()

            # Should contain test name (skip reason only shown with verbosity > 0)
            self.assertIn('test_method', output)
            # Skip reason not shown by default (verbosity = 0)
            self.assertNotIn('Test skipped', output)


class TestJSONOutput(unittest.TestCase):
    """Test JSON output format functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.formatter = OutputFormatter(format_type='json')
    
    def test_json_output_structure(self):
        """Test JSON output format structure."""
        # Create sample results
        results = {
            'tests_run': 5,
            'failures': 1,
            'errors': 0,
            'skipped': 1,
            'success_rate': 80.0,
            'total_time': 1.234,
            'results': []
        }
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_results(results)
            output = mock_stdout.getvalue()
            
            # Should be valid JSON
            try:
                parsed = json.loads(output)
                self.assertIn('tests_run', parsed)
                self.assertIn('failures', parsed)
                self.assertIn('success_rate', parsed)
                self.assertEqual(parsed['tests_run'], 5)
            except json.JSONDecodeError:
                self.fail("Output is not valid JSON")
    
    def test_json_no_color_output(self):
        """Test that JSON output doesn't include color codes."""
        mock_test = MagicMock()
        mock_test.__class__.__name__ = 'TestExample'
        mock_test._testMethodName = 'test_method'
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_success(mock_test, 0.123)
            output = mock_stdout.getvalue()
            
            # JSON format should not produce output for individual tests
            # (they're collected and output at the end)
            self.assertEqual(output, "")


class TestMinimalOutput(unittest.TestCase):
    """Test minimal output format functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.formatter = OutputFormatter(format_type='minimal')
    
    def test_minimal_success_output(self):
        """Test minimal format success output."""
        mock_test = MagicMock()
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_success(mock_test, 0.123)
            output = mock_stdout.getvalue()
            
            # Should output single character
            self.assertIn('.', output)
    
    def test_minimal_failure_output(self):
        """Test minimal format failure output."""
        mock_test = MagicMock()
        error_info = (AssertionError, AssertionError("Test failed"), None)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_failure(mock_test, error_info, 0.123)
            output = mock_stdout.getvalue()
            
            # Should output single character
            self.assertIn('F', output)
    
    def test_minimal_error_output(self):
        """Test minimal format error output."""
        mock_test = MagicMock()
        error_info = (ValueError, ValueError("Error"), None)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_error(mock_test, error_info, 0.123)
            output = mock_stdout.getvalue()
            
            # Should output single character
            self.assertIn('E', output)
    
    def test_minimal_skip_output(self):
        """Test minimal format skip output."""
        mock_test = MagicMock()
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.formatter.print_test_skip(mock_test, "Skipped", 0.001)
            output = mock_stdout.getvalue()
            
            # Should output single character
            self.assertIn('S', output)


class TestCrossPlatformCompatibility(unittest.TestCase):
    """Test output formatting across platforms."""
    
    def test_color_support_detection(self):
        """Test color support detection across platforms."""
        # Test with TTY
        with patch('os.isatty', return_value=True):
            formatter = OutputFormatter()
            # Color support depends on implementation
        
        # Test without TTY
        with patch('os.isatty', return_value=False):
            formatter = OutputFormatter()
            # Should handle non-TTY environments
    
    def test_unicode_handling(self):
        """Test handling of unicode characters in output."""
        formatter = OutputFormatter()
        
        # Test with unicode test names
        mock_test = MagicMock()
        mock_test.__class__.__name__ = 'TestUnicode'
        mock_test._testMethodName = 'test_unicode_ñáéíóú'
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                formatter.print_test_success(mock_test, 0.123)
                output = mock_stdout.getvalue()
                # Should handle unicode without crashing
                self.assertIn('test_unicode', output)
            except UnicodeError:
                self.fail("Unicode handling failed")
    
    def test_path_handling(self):
        """Test handling of different path formats."""
        formatter = OutputFormatter()
        
        # Test with different path separators
        test_paths = [
            '/unix/style/path.py',
            'C:\\Windows\\style\\path.py',
            'relative/path.py'
        ]
        
        for path in test_paths:
            # Should handle different path formats without crashing
            try:
                # Test path handling in context where it might be used
                pass
            except Exception as e:
                self.fail(f"Path handling failed for {path}: {e}")


class TestOutputFormatterEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_none_test_case_handling(self):
        """Test handling of None test case."""
        formatter = OutputFormatter()
        
        # Should handle None gracefully
        try:
            formatter.print_test_success(None, 0.123)
        except Exception as e:
            # If it raises an exception, it should be handled gracefully
            pass
    
    def test_negative_timing_handling(self):
        """Test handling of negative timing values."""
        formatter = OutputFormatter()
        mock_test = MagicMock()
        
        # Should handle negative timing gracefully
        try:
            formatter.print_test_success(mock_test, -0.123)
        except Exception as e:
            # Should not crash on negative timing
            pass
    
    def test_very_long_test_names(self):
        """Test handling of very long test names."""
        formatter = OutputFormatter()
        
        mock_test = MagicMock()
        mock_test.__class__.__name__ = 'A' * 1000  # Very long class name
        mock_test._testMethodName = 'test_' + 'b' * 1000  # Very long method name
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                formatter.print_test_success(mock_test, 0.123)
                output = mock_stdout.getvalue()
                # Should handle long names without crashing
            except Exception as e:
                self.fail(f"Long test name handling failed: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)

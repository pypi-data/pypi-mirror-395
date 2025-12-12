"""Tests for wobble file I/O system.

This module tests the threaded file writing capabilities,
ordering guarantees, and performance requirements.
"""

import unittest
import tempfile
import threading
import time
import json
import os
from pathlib import Path
from datetime import datetime
import sys

# Add the parent directory to the path for imports during testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from wobble.file_io import ThreadedFileWriter, WriteOperation
from wobble.data_structures import TestResult, TestStatus, ErrorInfo, TestRunSummary


class TestWriteOperation(unittest.TestCase):
    """Test WriteOperation dataclass."""
    
    def test_write_operation_creation(self):
        """Test WriteOperation creation."""
        operation = WriteOperation(
            sequence_id=1,
            operation_type='test_result',
            data={'test': 'data'},
            timestamp=time.time()
        )
        
        self.assertEqual(operation.sequence_id, 1)
        self.assertEqual(operation.operation_type, 'test_result')
        self.assertEqual(operation.data, {'test': 'data'})
        self.assertIsInstance(operation.timestamp, float)


class TestThreadedFileWriter(unittest.TestCase):
    """Test ThreadedFileWriter functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test_output.txt'
        self.timestamp = datetime(2024, 1, 15, 14, 30, 25)
        
        # Create sample test results
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
            total_tests=2,
            passed=1,
            failed=1,
            errors=0,
            skipped=0,
            duration=0.3,
            start_time=self.timestamp,
            end_time=self.timestamp,
            command="wobble tests/"
        )
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_threaded_file_writer_creation(self):
        """Test ThreadedFileWriter initialization."""
        writer = ThreadedFileWriter(
            file_path=str(self.test_file),
            format_type='txt',
            verbosity=1
        )
        
        self.assertEqual(writer.file_path, self.test_file)
        self.assertEqual(writer.format_type, 'txt')
        self.assertEqual(writer.verbosity, 1)
        self.assertFalse(writer.append_mode)
        self.assertIsNotNone(writer.writer_thread)
        self.assertTrue(writer.writer_thread.is_alive())
        
        writer.close()
    
    def test_file_creation_and_directory_creation(self):
        """Test that file and directories are created properly."""
        nested_file = Path(self.temp_dir) / 'nested' / 'dir' / 'test.txt'
        
        writer = ThreadedFileWriter(
            file_path=str(nested_file),
            format_type='txt'
        )
        
        # File should be created
        self.assertTrue(nested_file.exists())
        self.assertTrue(nested_file.parent.exists())
        
        writer.close()
    
    def test_text_format_output(self):
        """Test text format file output."""
        writer = ThreadedFileWriter(
            file_path=str(self.test_file),
            format_type='txt',
            verbosity=1
        )
        
        # Write header
        writer.write_header("wobble tests/", "2024-01-15 14:30:00")
        
        # Write test results
        for result in self.test_results:
            writer.write_test_result(result)
        
        # Write summary
        writer.write_summary(self.summary)
        
        # Close and read file
        writer.close()
        
        content = self.test_file.read_text()
        
        # Verify content
        self.assertIn("=== Wobble Test Run ===", content)
        self.assertIn("wobble tests/", content)
        self.assertIn("test_pass", content)
        self.assertIn("test_fail", content)
        self.assertIn("=== Summary ===", content)
        self.assertIn("Total: 2", content)
        self.assertIn("Passed: 1", content)
        self.assertIn("Failed: 1", content)
    
    def test_json_format_output(self):
        """Test JSON format file output."""
        json_file = Path(self.temp_dir) / 'test_output.json'
        
        writer = ThreadedFileWriter(
            file_path=str(json_file),
            format_type='json',
            verbosity=2
        )
        
        # Write test results
        for result in self.test_results:
            writer.write_test_result(result)
        
        # Write summary
        writer.write_summary(self.summary)
        
        # Close and read file
        writer.close()
        
        content = json_file.read_text()
        data = json.loads(content)
        
        # Verify JSON structure
        self.assertIn('run_info', data)
        self.assertIn('test_results', data)
        self.assertEqual(len(data['test_results']), 2)
        
        # Verify test results
        self.assertEqual(data['test_results'][0]['name'], 'test_pass')
        self.assertEqual(data['test_results'][1]['name'], 'test_fail')
        
        # Verify verbosity level 2 includes error info
        self.assertIn('error_info', data['test_results'][1])
    
    def test_append_mode(self):
        """Test append mode functionality."""
        # Write initial content
        self.test_file.write_text("Existing content\n")
        
        writer = ThreadedFileWriter(
            file_path=str(self.test_file),
            format_type='txt',
            append_mode=True
        )
        
        writer.write_header("wobble tests/", "2024-01-15 14:30:00")
        writer.write_test_result(self.test_results[0])
        writer.close()
        
        content = self.test_file.read_text()
        
        # Should contain both existing and new content
        self.assertIn("Existing content", content)
        self.assertIn("=== Wobble Test Run ===", content)
    
    def test_concurrent_writes_ordering(self):
        """Test that concurrent writes maintain proper ordering."""
        writer = ThreadedFileWriter(
            file_path=str(self.test_file),
            format_type='txt',
            verbosity=1
        )
        
        # Create multiple test results
        results = []
        for i in range(10):
            result = TestResult(
                name=f"test_{i:02d}",
                classname="TestClass",
                status=TestStatus.PASS,
                duration=0.001 * i,
                timestamp=self.timestamp
            )
            results.append(result)
        
        # Write results concurrently
        threads = []
        for result in results:
            thread = threading.Thread(target=writer.write_test_result, args=(result,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Write summary
        summary = TestRunSummary(
            total_tests=10, passed=10, failed=0, errors=0, skipped=0,
            duration=1.0, start_time=self.timestamp, end_time=self.timestamp,
            command="wobble tests/"
        )
        writer.write_summary(summary)
        
        writer.close()
        
        # Verify ordering in output
        content = self.test_file.read_text()
        lines = content.split('\n')
        
        # Find test result lines
        test_lines = [line for line in lines if 'test_' in line and '✓' in line]
        
        # Verify results are in correct order
        for i, line in enumerate(test_lines):
            self.assertIn(f"test_{i:02d}", line)
    
    def test_performance_requirements(self):
        """Test that performance requirements are met."""
        writer = ThreadedFileWriter(
            file_path=str(self.test_file),
            format_type='json',
            verbosity=1
        )
        
        # Measure write latency
        num_operations = 100
        start_time = time.time()
        
        for i in range(num_operations):
            result = TestResult(
                name=f"test_{i}",
                classname="TestClass",
                status=TestStatus.PASS,
                duration=0.001,
                timestamp=self.timestamp
            )
            writer.write_test_result(result)
        
        end_time = time.time()
        
        # Calculate average latency
        avg_latency = (end_time - start_time) / num_operations
        
        # Should be less than 1ms per operation (queuing time)
        self.assertLess(avg_latency, 0.001, 
                       f"Average latency {avg_latency:.6f}s exceeds 1ms requirement")
        
        writer.close()
    
    def test_error_handling(self):
        """Test error handling in file operations."""
        # Test with invalid file path (read-only directory on Unix)
        if os.name != 'nt':  # Skip on Windows
            readonly_dir = Path(self.temp_dir) / 'readonly'
            readonly_dir.mkdir()
            readonly_dir.chmod(0o444)  # Read-only
            
            invalid_file = readonly_dir / 'test.txt'
            
            with self.assertRaises(Exception):
                ThreadedFileWriter(
                    file_path=str(invalid_file),
                    format_type='txt'
                )
    
    def test_context_manager(self):
        """Test context manager functionality."""
        with ThreadedFileWriter(str(self.test_file), 'txt') as writer:
            writer.write_test_result(self.test_results[0])
        
        # File should be closed and content written
        self.assertTrue(self.test_file.exists())
        content = self.test_file.read_text()
        self.assertIn("test_pass", content)
    
    def test_performance_stats(self):
        """Test performance statistics collection."""
        writer = ThreadedFileWriter(
            file_path=str(self.test_file),
            format_type='txt'
        )
        
        # Write some operations
        for result in self.test_results:
            writer.write_test_result(result)
        
        # Get stats
        stats = writer.get_performance_stats()
        
        # Verify stats structure
        self.assertIn('operations_written', stats)
        self.assertIn('elapsed_time', stats)
        self.assertIn('operations_per_second', stats)
        self.assertIn('queue_size', stats)
        self.assertIn('pending_writes', stats)
        self.assertIn('has_error', stats)
        
        # Verify some values
        self.assertGreaterEqual(stats['operations_written'], 0)
        self.assertGreater(stats['elapsed_time'], 0)
        self.assertFalse(stats['has_error'])
        
        writer.close()
    
    def test_verbosity_levels(self):
        """Test different verbosity levels in output."""
        for verbosity in [1, 2, 3]:
            test_file = Path(self.temp_dir) / f'test_v{verbosity}.txt'
            
            writer = ThreadedFileWriter(
                file_path=str(test_file),
                format_type='txt',
                verbosity=verbosity
            )
            
            # Write a failed test to see error details
            writer.write_test_result(self.test_results[1])  # Failed test
            writer.close()
            
            content = test_file.read_text()
            
            if verbosity >= 2:
                # Should include error details
                self.assertIn("Error:", content)
                self.assertIn("AssertionError", content)
            
            if verbosity >= 3:
                # Should include traceback
                self.assertIn("Traceback", content)


if __name__ == '__main__':
    unittest.main(verbosity=2)

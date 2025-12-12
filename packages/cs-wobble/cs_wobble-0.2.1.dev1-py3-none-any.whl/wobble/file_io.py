"""Concurrent file I/O system for wobble test results.

This module provides threaded file writing capabilities with ordered
processing to support high-performance file output without blocking
test execution.
"""

import threading
import queue
import time
import json
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

from .data_structures import TestResult, TestRunSummary, serialize_test_results, format_test_results_text


@dataclass
class WriteOperation:
    """Represents a file write operation with ordering information.
    
    Attributes:
        sequence_id: Unique sequence identifier for ordering
        operation_type: Type of operation ('test_result', 'summary', 'header')
        data: The data to write
        timestamp: When the operation was created
    """
    sequence_id: int
    operation_type: str
    data: Any
    timestamp: float


class ThreadedFileWriter:
    """Threaded file writer with ordered processing.
    
    This class provides background file writing with guaranteed ordering
    of write operations, supporting concurrent test execution while
    maintaining result sequence integrity.
    """
    
    def __init__(self, file_path: str, format_type: str, verbosity: int = 1, 
                 buffer_size: int = 1000, append_mode: bool = False):
        """Initialize the threaded file writer.
        
        Args:
            file_path: Path to the output file
            format_type: Output format ('json' or 'txt')
            verbosity: Output verbosity level (1-3)
            buffer_size: Maximum number of operations to buffer
            append_mode: Whether to append to existing file
        """
        self.file_path = Path(file_path)
        self.format_type = format_type.lower()
        self.verbosity = verbosity
        self.buffer_size = buffer_size
        self.append_mode = append_mode
        
        # Threading components
        self.write_queue = queue.Queue(maxsize=buffer_size)
        self.writer_thread: Optional[threading.Thread] = None
        self.shutdown_event = threading.Event()
        self.error_event = threading.Event()
        self.last_error: Optional[Exception] = None
        
        # Ordering components
        self.next_sequence_id = 0
        self.pending_writes: Dict[int, WriteOperation] = {}
        self.next_write_sequence = 0
        self.sequence_lock = threading.Lock()
        
        # File handling
        self.file_handle: Optional[Any] = None
        self.test_results: List[TestResult] = []
        self.run_summary: Optional[TestRunSummary] = None
        
        # Performance tracking
        self.operations_written = 0
        self.start_time = time.time()

        # Debug counters for queue operations
        self.put_count = 0
        self.task_done_count = 0
        
        self._start_writer_thread()
    
    def _start_writer_thread(self) -> None:
        """Start the background writer thread."""
        try:
            # Create directory if it doesn't exist
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open file in appropriate mode
            mode = 'a' if self.append_mode else 'w'
            self.file_handle = open(self.file_path, mode, encoding='utf-8')
            
            # Start writer thread
            self.writer_thread = threading.Thread(
                target=self._writer_loop, 
                name=f"FileWriter-{self.file_path.name}",
                daemon=True
            )
            self.writer_thread.start()
            
        except Exception as e:
            self.last_error = e
            self.error_event.set()
            raise
    
    def _writer_loop(self) -> None:
        """Main writer thread loop - simplified approach."""
        try:
            while not self.shutdown_event.is_set():
                try:
                    # Get operation from queue with timeout
                    operation = self.write_queue.get(timeout=1.0)

                    # Process operation immediately (no complex ordering)
                    self._write_operation(operation)

                    # Mark task as done
                    self.write_queue.task_done()
                    self.task_done_count += 1

                except queue.Empty:
                    # Timeout is normal, continue loop
                    continue

            # Process any remaining operations after shutdown signal
            while True:
                try:
                    operation = self.write_queue.get_nowait()
                    self._write_operation(operation)
                    self.write_queue.task_done()
                    self.task_done_count += 1
                except queue.Empty:
                    break

        except Exception as e:
            # Log the error for debugging
            import sys
            print(f"ERROR in writer thread: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            self.last_error = e
            self.error_event.set()
    
    def _process_pending_writes(self) -> None:
        """Process pending writes in sequence order - DEPRECATED in simplified approach."""
        # This method is no longer used in the simplified approach
        pass
    
    def _write_operation(self, operation: WriteOperation) -> None:
        """Write a single operation to the file.

        Args:
            operation: The write operation to execute
        """
        try:
            if operation.operation_type == 'test_result':
                self.test_results.append(operation.data)

                # For text format, write individual results immediately
                if self.format_type == 'txt':
                    self._write_text_result(operation.data)

            elif operation.operation_type == 'summary':
                self.run_summary = operation.data
                self._write_final_output()

            elif operation.operation_type == 'header':
                self._write_header(operation.data)

            elif operation.operation_type == 'discovery':
                self._write_discovery_results(operation.data)

            elif operation.operation_type == 'text':
                # Write raw text directly to file
                self.file_handle.write(operation.data + '\n')
                self.file_handle.flush()

        except Exception as e:
            # Log the error for debugging
            import sys
            print(f"ERROR in _write_operation: {e}", file=sys.stderr)
            print(f"Operation type: {operation.operation_type}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise
    
    def _write_header(self, header_data: Dict[str, Any]) -> None:
        """Write file header information.
        
        Args:
            header_data: Header information to write
        """
        if self.format_type == 'json':
            # For JSON, we'll write everything at the end
            pass
        else:
            # For text format, write header immediately
            self.file_handle.write("=== Wobble Test Run ===\n")
            self.file_handle.write(f"Command: {header_data.get('command', 'unknown')}\n")
            self.file_handle.write(f"Started: {header_data.get('start_time', 'unknown')}\n")
            self.file_handle.write("\n")
    
    def _write_final_output(self) -> None:
        """Write the final output with all collected results."""
        if not self.run_summary:
            return
            
        if self.format_type == 'json':
            # Write complete JSON output
            json_output = serialize_test_results(
                self.test_results, 
                self.run_summary, 
                self.verbosity
            )
            self.file_handle.write(json_output)
            self.file_handle.write('\n')
            
        else:
            # Write text format summary
            text_output = format_test_results_text(
                self.test_results,
                self.run_summary,
                self.verbosity
            )
            # Only write summary part since individual results were written already
            summary_lines = text_output.split('\n')
            summary_start = next(i for i, line in enumerate(summary_lines) if line.startswith('=== Summary ==='))
            summary_text = '\n'.join(summary_lines[summary_start:])
            self.file_handle.write(summary_text)
            self.file_handle.write('\n')

    def _write_discovery_results(self, discovery_data: Dict[str, Any]) -> None:
        """Write discovery results to file.

        Args:
            discovery_data: Discovery metadata containing test information
        """
        if self.format_type == 'json':
            # Write JSON format discovery results
            # Convert test objects to serializable format
            serializable_tests = {}
            discovered_tests = discovery_data.get('discovered_tests', {})

            for category, tests in discovered_tests.items():
                serializable_tests[category] = []
                for test in tests:
                    # Extract only serializable information
                    serializable_test = {
                        'name': test.get('test_method', 'unknown'),
                        'class': test.get('test_class', 'unknown'),
                        'module': test.get('test_module', 'unknown'),
                        'file_path': str(test.get('file_path', '')) if test.get('file_path') else None,
                        'metadata': test.get('metadata', {})
                    }
                    serializable_tests[category].append(serializable_test)

            json_output = {
                'discovery_results': {
                    'timestamp': discovery_data.get('timestamp', datetime.now()).isoformat(),
                    'total_tests': discovery_data.get('total_tests', 0),
                    'categories': discovery_data.get('categories', 0),
                    'discovered_tests': serializable_tests
                }
            }
            import json
            self.file_handle.write(json.dumps(json_output, indent=2))
            self.file_handle.write('\n')
        else:
            # Write text format discovery results
            self.file_handle.write("=== Wobble Test Discovery ===\n")
            self.file_handle.write(f"Timestamp: {discovery_data.get('timestamp', datetime.now()).isoformat()}\n")
            self.file_handle.write(f"Total tests: {discovery_data.get('total_tests', 0)}\n")
            self.file_handle.write(f"Categories: {discovery_data.get('categories', 0)}\n")
            self.file_handle.write("\n")

            discovered_tests = discovery_data.get('discovered_tests', {})
            for category, tests in discovered_tests.items():
                self.file_handle.write(f"{category}: {len(tests)} test(s)\n")
                if self.verbosity >= 2:
                    for test in tests:
                        self.file_handle.write(f"  - {test.get('name', 'unknown')}\n")
            self.file_handle.write("\n")

        # Flush to ensure data is written immediately
        self.file_handle.flush()

    def write_header(self, command: str, start_time: str) -> None:
        """Queue header information for writing.
        
        Args:
            command: The command that started the test run
            start_time: When the test run started
        """
        self._queue_operation('header', {
            'command': command,
            'start_time': start_time
        })
    
    def write_test_result(self, test_result: TestResult) -> None:
        """Queue a test result for writing.

        Args:
            test_result: The test result to write

        Raises:
            RuntimeError: If the writer has encountered an error
        """
        if self.error_event.is_set():
            raise RuntimeError(f"File writer error: {self.last_error}")

        self._queue_operation('test_result', test_result)
    
    def _write_text_result(self, test_result: TestResult) -> None:
        """Write individual test result in text format.
        
        Args:
            test_result: The test result to write
        """
        status_symbol = {
            'PASS': 'PASS',
            'FAIL': 'FAIL',
            'ERROR': 'ERROR',
            'SKIP': 'SKIP'
        }.get(test_result.status.value, '?')
        
        line = f"{status_symbol} {test_result.classname}.{test_result.name} ({test_result.duration:.3f}s)\n"
        
        # Write directly to file for immediate feedback
        if self.file_handle:
            self.file_handle.write(line)
            
            # Add error details for higher verbosity
            if self.verbosity >= 2 and test_result.error_info:
                self.file_handle.write(f"    Error: {test_result.error_info.type}: {test_result.error_info.message}\n")
                
                if self.verbosity >= 3:
                    # Add traceback for complete verbosity
                    traceback_lines = test_result.error_info.traceback.split('\n')
                    for tb_line in traceback_lines[:5]:  # Limit to first 5 lines
                        if tb_line.strip():
                            self.file_handle.write(f"    {tb_line}\n")
                    if len(traceback_lines) > 5:
                        self.file_handle.write("    ... (traceback truncated)\n")
            
            self.file_handle.flush()
    
    def write_summary(self, summary: TestRunSummary) -> None:
        """Queue test run summary for writing.

        Args:
            summary: The test run summary to write
        """
        self._queue_operation('summary', summary)

    def write_discovery_results(self, discovery_metadata: Dict[str, Any]) -> None:
        """Queue discovery results for writing.

        Args:
            discovery_metadata: Discovery results metadata
        """
        self._queue_operation('discovery', discovery_metadata)

    def write_text(self, text: str) -> None:
        """Queue raw text for writing.

        Args:
            text: Raw text to write to file
        """
        self._queue_operation('text', text)
    
    def _queue_operation(self, operation_type: str, data: Any) -> None:
        """Queue an operation for writing.
        
        Args:
            operation_type: Type of operation
            data: Data to write
            
        Raises:
            RuntimeError: If the writer has encountered an error
            queue.Full: If the write queue is full
        """
        if self.error_event.is_set():
            raise RuntimeError(f"File writer error: {self.last_error}")
        
        with self.sequence_lock:
            operation = WriteOperation(
                sequence_id=self.next_sequence_id,
                operation_type=operation_type,
                data=data,
                timestamp=time.time()
            )
            self.next_sequence_id += 1
        
        try:
            # Use timeout to avoid blocking indefinitely
            self.write_queue.put(operation, timeout=1.0)
            self.put_count += 1
        except queue.Full:
            raise RuntimeError("File writer queue is full - cannot accept more operations")
    
    def close(self) -> None:
        """Close the file writer and clean up resources."""
        # Signal shutdown
        self.shutdown_event.set()

        # Wait for queue to empty with timeout (avoid deadlock)
        if self.write_queue:
            try:
                # Use timeout-based approach instead of queue.join() to avoid deadlock
                start_time = time.time()
                timeout = 5.0
                while not self.write_queue.empty() and (time.time() - start_time) < timeout:
                    time.sleep(0.1)

                # If queue is still not empty after timeout, log debug info
                if not self.write_queue.empty():
                    import sys
                    print(f"WARNING: Queue not empty after {timeout}s timeout. "
                          f"put_count={self.put_count}, task_done_count={self.task_done_count}",
                          file=sys.stderr)
            except:
                pass  # Ignore errors during shutdown

        # Wait for writer thread to finish
        if self.writer_thread and self.writer_thread.is_alive():
            self.writer_thread.join(timeout=5.0)

        # Close file handle
        if self.file_handle:
            try:
                self.file_handle.flush()
                self.file_handle.close()
            except:
                pass  # Ignore errors during shutdown
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for the writer.
        
        Returns:
            Dictionary containing performance metrics
        """
        elapsed_time = time.time() - self.start_time
        ops_per_second = self.operations_written / elapsed_time if elapsed_time > 0 else 0
        
        return {
            'operations_written': self.operations_written,
            'elapsed_time': elapsed_time,
            'operations_per_second': ops_per_second,
            'queue_size': self.write_queue.qsize(),
            'pending_writes': len(self.pending_writes),
            'has_error': self.error_event.is_set(),
            'last_error': str(self.last_error) if self.last_error else None
        }
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

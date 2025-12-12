"""Data structures for wobble test results and file output.

This module provides strongly-typed data structures for test results,
error information, and test run summaries. These structures support
JSON serialization and validation for the file output system.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
import json
import os
import platform


class TestStatus(Enum):
    """Enumeration of possible test statuses."""
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    SKIP = "SKIP"


@dataclass
class ErrorInfo:
    """Information about test errors and failures.
    
    Attributes:
        type: The exception type name (e.g., 'AssertionError', 'ValueError')
        message: The error message
        traceback: The full traceback string
        file_path: Optional path to the file where error occurred
        line_number: Optional line number where error occurred
    """
    type: str
    message: str
    traceback: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    
    def __post_init__(self):
        """Validate error information."""
        if not self.type.strip():
            raise ValueError("Error type cannot be empty")
        if not self.message.strip():
            raise ValueError("Error message cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            'type': self.type,
            'message': self.message,
            'traceback': self.traceback
        }
        
        if self.file_path:
            result['file_path'] = self.file_path
        if self.line_number is not None:
            result['line_number'] = self.line_number
            
        return result


@dataclass
class TestResult:
    """Comprehensive test result information.
    
    Attributes:
        name: Test method name
        classname: Test class name
        status: Test execution status
        duration: Test execution time in seconds
        timestamp: When the test was executed
        metadata: Additional test metadata from decorators
        error_info: Error details if test failed/errored
        captured_output: Captured stdout/stderr during test execution
    """
    name: str
    classname: str
    status: TestStatus
    duration: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_info: Optional[ErrorInfo] = None
    captured_output: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        """Validate test result data."""
        if self.duration < 0:
            raise ValueError("Duration cannot be negative")
        if not self.name.strip():
            raise ValueError("Test name cannot be empty")
        if not self.classname.strip():
            raise ValueError("Test class name cannot be empty")
    
    def to_dict(self, verbosity: int = 1) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.
        
        Args:
            verbosity: Output verbosity level (1=Standard, 2=Detailed, 3=Complete)
            
        Returns:
            Dictionary representation suitable for JSON serialization
        """
        # Level 1: Standard - Basic test information
        result = {
            'name': self.name,
            'classname': self.classname,
            'status': self.status.value,
            'duration': round(self.duration, 6),  # Microsecond precision
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }
        
        # Level 2: Detailed - Add error details and enhanced metadata
        if verbosity >= 2:
            if self.error_info:
                result['error_info'] = self.error_info.to_dict()
            
            # Add enhanced metadata for debugging
            result['full_name'] = f"{self.classname}.{self.name}"
            
        # Level 3: Complete - Add environment and captured output
        if verbosity >= 3:
            result['environment'] = self._get_environment_info()
            if self.captured_output:
                result['captured_output'] = self.captured_output
            
        return result
    
    def _get_environment_info(self) -> Dict[str, Any]:
        """Get environment information for complete verbosity level."""
        return {
            'python_version': platform.python_version(),
            'platform': platform.platform(),
            'working_directory': os.getcwd(),
            'environment_variables': {
                key: value for key, value in os.environ.items()
                if key.startswith(('PYTHON', 'PATH', 'WOBBLE'))
            }
        }


@dataclass
class TestRunSummary:
    """Summary information for a complete test run.
    
    Attributes:
        total_tests: Total number of tests executed
        passed: Number of tests that passed
        failed: Number of tests that failed
        errors: Number of tests that had errors
        skipped: Number of tests that were skipped
        duration: Total execution time in seconds
        start_time: When the test run started
        end_time: When the test run ended
        command: The command line used to run tests
        exit_code: The exit code of the test run
    """
    total_tests: int
    passed: int
    failed: int
    errors: int
    skipped: int
    duration: float
    start_time: datetime
    end_time: datetime
    command: str
    exit_code: int = 0
    
    def __post_init__(self):
        """Validate test run summary."""
        if self.total_tests < 0:
            raise ValueError("Total tests cannot be negative")
        if self.passed < 0 or self.failed < 0 or self.errors < 0 or self.skipped < 0:
            raise ValueError("Test counts cannot be negative")
        if self.passed + self.failed + self.errors + self.skipped != self.total_tests:
            raise ValueError("Test counts do not sum to total tests")
        if self.duration < 0:
            raise ValueError("Duration cannot be negative")
        if self.end_time < self.start_time:
            raise ValueError("End time cannot be before start time")
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_tests == 0:
            return 100.0
        return (self.passed / self.total_tests) * 100.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'summary': {
                'total_tests': self.total_tests,
                'passed': self.passed,
                'failed': self.failed,
                'errors': self.errors,
                'skipped': self.skipped,
                'success_rate': round(self.success_rate, 2)
            },
            'timing': {
                'duration': round(self.duration, 6),
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat()
            },
            'execution': {
                'command': self.command,
                'exit_code': self.exit_code
            }
        }


class TestResultEncoder(json.JSONEncoder):
    """Custom JSON encoder for test result objects."""
    
    def default(self, obj):
        """Convert custom objects to JSON-serializable format."""
        if isinstance(obj, (TestResult, ErrorInfo, TestRunSummary)):
            return obj.to_dict()
        elif isinstance(obj, TestStatus):
            return obj.value
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def serialize_test_results(results: List[TestResult], 
                          summary: TestRunSummary,
                          verbosity: int = 1) -> str:
    """Serialize test results to JSON string.
    
    Args:
        results: List of test results
        summary: Test run summary
        verbosity: Output verbosity level
        
    Returns:
        JSON string representation
    """
    data = {
        'run_info': summary.to_dict(),
        'test_results': [result.to_dict(verbosity) for result in results]
    }
    
    return json.dumps(data, cls=TestResultEncoder, indent=2)


def format_test_results_text(results: List[TestResult], 
                           summary: TestRunSummary,
                           verbosity: int = 1) -> str:
    """Format test results as human-readable text.
    
    Args:
        results: List of test results
        summary: Test run summary
        verbosity: Output verbosity level
        
    Returns:
        Formatted text representation
    """
    lines = []
    
    # Header
    lines.append("=== Wobble Test Run Results ===")
    lines.append(f"Command: {summary.command}")
    lines.append(f"Started: {summary.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Duration: {summary.duration:.3f}s")
    lines.append("")
    
    # Test results
    for result in results:
        status_symbol = {
            TestStatus.PASS: "PASS",
            TestStatus.FAIL: "FAIL",
            TestStatus.ERROR: "ERROR",
            TestStatus.SKIP: "SKIP"
        }.get(result.status, "?")
        
        lines.append(f"{status_symbol} {result.classname}.{result.name} ({result.duration:.3f}s)")
        
        if verbosity >= 2 and result.error_info:
            lines.append(f"    Error: {result.error_info.type}: {result.error_info.message}")
            if verbosity >= 3:
                # Add traceback for complete verbosity
                traceback_lines = result.error_info.traceback.split('\n')
                for tb_line in traceback_lines[:5]:  # Limit to first 5 lines
                    if tb_line.strip():
                        lines.append(f"    {tb_line}")
                if len(traceback_lines) > 5:
                    lines.append("    ... (traceback truncated)")
    
    lines.append("")
    
    # Summary
    lines.append("=== Summary ===")
    lines.append(f"Total: {summary.total_tests}")
    lines.append(f"Passed: {summary.passed}")
    lines.append(f"Failed: {summary.failed}")
    lines.append(f"Errors: {summary.errors}")
    lines.append(f"Skipped: {summary.skipped}")
    lines.append(f"Success Rate: {summary.success_rate:.1f}%")
    lines.append(f"Exit Code: {summary.exit_code}")
    
    return '\n'.join(lines)

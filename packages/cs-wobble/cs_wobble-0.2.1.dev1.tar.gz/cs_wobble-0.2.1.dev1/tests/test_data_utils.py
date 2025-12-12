"""Centralized test data management utilities for Wobble testing framework.

This module provides standardized test data management following Cracking Shells
organization standards for centralized test data utilities.
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from unittest import TestCase


class WobbleTestDataLoader:
    """Centralized test data loader for Wobble test suite."""
    
    def __init__(self):
        """Initialize test data loader with standard paths."""
        self.test_dir = Path(__file__).parent
        self.test_data_dir = self.test_dir / "test_data"
        self.temp_dirs = []
    
    def create_fake_test_directory(self, name: str = "fake_tests") -> Path:
        """Create a fake test directory structure for discovery testing.

        Args:
            name: Name of the fake test directory

        Returns:
            Path to the created fake test directory
        """
        temp_dir = Path(tempfile.mkdtemp(prefix=f"wobble_{name}_"))
        self.temp_dirs.append(temp_dir)

        # Use the centralized method to create test files
        self._create_test_files_in_directory(temp_dir, name)

        return temp_dir
    
    def create_mixed_test_suite(self) -> Path:
        """Create a mixed test suite with various categories."""
        return self.create_fake_test_directory("mixed_suite")
    
    def create_comprehensive_test_suite(self) -> Path:
        """Create a comprehensive test suite with all categories."""
        temp_dir = Path(tempfile.mkdtemp(prefix="wobble_comprehensive_"))
        self.temp_dirs.append(temp_dir)

        # Use the centralized method to create test files
        self._create_test_files_in_directory(temp_dir, "comprehensive")

        # Also create additional comprehensive test files in the tests directory
        tests_dir = temp_dir / "tests"
        additional_files = {
            "test_regression.py": self._get_regression_test_content(),
            "test_development.py": self._get_development_test_content(),
            "test_slow.py": self._get_slow_test_content(),
            "test_uncategorized.py": self._get_uncategorized_test_content(),
        }

        for filename, content in additional_files.items():
            test_file = tests_dir / filename
            test_file.write_text(content, encoding='utf-8')

        return temp_dir
    
    def create_unicode_test_suite(self) -> Path:
        """Create test suite with unicode test names."""
        temp_dir = Path(tempfile.mkdtemp(prefix="wobble_unicode_"))
        self.temp_dirs.append(temp_dir)

        # Create tests subdirectory
        tests_dir = temp_dir / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)

        unicode_content = '''"""Test module with unicode characters."""
import unittest
from wobble.decorators import regression_test

class TestUnicodeHandling(unittest.TestCase):
    """Test class with unicode content."""

    @regression_test
    def test_unicode_ñ_handling(self):
        """Test with unicode ñ character in method name."""
        unicode_string = "Testing unicode: ñ"
        self.assertIsNotNone(unicode_string)

    def test_emoji_support(self):
        """Test with emoji characters."""
        emoji_string = "Testing emoji: 🚀"
        self.assertIsNotNone(emoji_string)
'''

        test_file = tests_dir / "test_unicode.py"
        test_file.write_text(unicode_content, encoding='utf-8')

        return temp_dir
    
    def cleanup_temp_directories(self):
        """Clean up all temporary test directories."""
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
        self.temp_dirs.clear()

    def _create_test_files_in_directory(self, directory: Path, name: str = "fake_tests") -> None:
        """Create test files in the specified directory.

        Args:
            directory: Directory where to create test files
            name: Name identifier for the test files
        """
        # Create tests subdirectory
        tests_dir = directory / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)

        # Create __init__.py in tests directory
        init_file = tests_dir / "__init__.py"
        init_file.write_text("# Test package\n", encoding='utf-8')

        # Create hierarchical subdirectories for hierarchical structure detection
        hierarchical_dirs = ["regression", "integration", "development"]
        for subdir_name in hierarchical_dirs:
            subdir = tests_dir / subdir_name
            subdir.mkdir(parents=True, exist_ok=True)

            # Create __init__.py in each subdirectory
            subdir_init = subdir / "__init__.py"
            subdir_init.write_text("# Test package\n", encoding='utf-8')

            # Create a test file in each subdirectory
            test_file = subdir / f"test_{subdir_name}.py"
            test_file.write_text(self._get_auth_test_content(), encoding='utf-8')

        # Create test files with various decorators in main tests directory
        test_files = {
            "test_auth.py": self._get_auth_test_content(),
            "test_models.py": self._get_models_test_content(),
            "test_utils.py": self._get_utils_test_content(),
            "test_integration.py": self._get_integration_test_content(),
        }

        for filename, content in test_files.items():
            test_file = tests_dir / filename
            test_file.write_text(content, encoding='utf-8')
    
    def _get_auth_test_content(self) -> str:
        """Get auth test file content."""
        return '''"""Authentication test module."""
import unittest
from wobble.decorators import regression_test, slow_test

class TestAuth(unittest.TestCase):
    
    @regression_test
    def test_login(self):
        """Test user login functionality."""
        pass
    
    @regression_test
    @slow_test
    def test_password_reset(self):
        """Test password reset functionality."""
        pass
    
    def test_logout(self):
        """Test user logout functionality."""
        pass
'''
    
    def _get_models_test_content(self) -> str:
        """Get models test file content."""
        return '''"""Models test module."""
import unittest
from wobble.decorators import integration_test

class TestModels(unittest.TestCase):
    
    @integration_test
    def test_user_model(self):
        """Test user model functionality."""
        pass
    
    def test_post_model(self):
        """Test post model functionality."""
        pass
'''
    
    def _get_utils_test_content(self) -> str:
        """Get utils test file content."""
        return '''"""Utilities test module."""
import unittest

class TestUtils(unittest.TestCase):
    
    def test_helper_function(self):
        """Test helper function."""
        pass
    
    def test_validation_utils(self):
        """Test validation utilities."""
        pass
'''
    
    def _get_integration_test_content(self) -> str:
        """Get integration test file content."""
        return '''"""Integration test module."""
import unittest
from wobble.decorators import integration_test, slow_test

class TestIntegration(unittest.TestCase):
    
    @integration_test
    @slow_test
    def test_api_integration(self):
        """Test API integration."""
        pass
    
    @integration_test
    def test_database_integration(self):
        """Test database integration."""
        pass
'''
    
    def _get_regression_test_content(self) -> str:
        """Get regression test file content."""
        return '''"""Regression test module."""
import unittest
from wobble.decorators import regression_test

class TestRegression(unittest.TestCase):
    
    @regression_test
    def test_bug_fix_123(self):
        """Test for bug fix #123."""
        pass
    
    @regression_test
    def test_bug_fix_456(self):
        """Test for bug fix #456."""
        pass
'''
    
    def _get_development_test_content(self) -> str:
        """Get development test file content."""
        return '''"""Development test module."""
import unittest
from wobble.decorators import development_test

class TestDevelopment(unittest.TestCase):
    
    @development_test
    def test_new_feature(self):
        """Test new feature under development."""
        pass
'''
    
    def _get_slow_test_content(self) -> str:
        """Get slow test file content."""
        return '''"""Slow test module."""
import unittest
from wobble.decorators import slow_test

class TestSlow(unittest.TestCase):
    
    @slow_test
    def test_performance_benchmark(self):
        """Test performance benchmark."""
        pass
'''
    
    def _get_uncategorized_test_content(self) -> str:
        """Get uncategorized test file content."""
        return '''"""Uncategorized test module."""
import unittest

class TestUncategorized(unittest.TestCase):
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        pass
    
    def test_edge_case(self):
        """Test edge case."""
        pass
'''


class WobbleTestBase(TestCase):
    """Base test class with common utilities for Wobble tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_data_loader = WobbleTestDataLoader()
        self.temp_files = []
    
    def tearDown(self):
        """Clean up test environment."""
        self.test_data_loader.cleanup_temp_directories()
        
        # Clean up temporary files
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def create_temp_file(self, content: str, suffix: str = ".txt") -> str:
        """Create a temporary file with given content.
        
        Args:
            content: Content to write to file
            suffix: File suffix
            
        Returns:
            Path to created temporary file
        """
        fd, temp_path = tempfile.mkstemp(suffix=suffix)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            os.close(fd)
            raise
        
        self.temp_files.append(temp_path)
        return temp_path
    
    def read_file(self, file_path: str) -> str:
        """Read content from file.
        
        Args:
            file_path: Path to file to read
            
        Returns:
            File content as string
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def assert_valid_json(self, json_string: str) -> Dict[str, Any]:
        """Assert that string is valid JSON and return parsed data.
        
        Args:
            json_string: JSON string to validate
            
        Returns:
            Parsed JSON data
            
        Raises:
            AssertionError: If JSON is invalid
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON: {e}")


# Global test data loader instance
test_data_loader = WobbleTestDataLoader()


def load_test_config(config_name: str) -> Dict[str, Any]:
    """Load test configuration by name.
    
    Args:
        config_name: Name of configuration to load
        
    Returns:
        Configuration dictionary
    """
    # Standard test configurations
    configs = {
        "test_settings": {
            "verbosity": 2,
            "format": "standard",
            "use_color": False
        },
        "discovery_settings": {
            "discover_verbosity": 3,
            "log_file_format": "json",
            "log_verbosity": 2
        }
    }
    
    return configs.get(config_name, {})


def load_mock_response(response_name: str) -> str:
    """Load mock response data by name.

    Args:
        response_name: Name of mock response to load

    Returns:
        Mock response content
    """
    # Standard mock responses
    responses = {
        "discovery_output_level_1": "Total tests discovered: 14\nRegression: 5\nUncategorized: 9",
        "discovery_output_level_2": "Total tests discovered: 14\nRegression: 5\nUncategorized: 9\n\nUncategorized tests:\n  TestUtils.test_helper_function (None)",
    }

    return responses.get(response_name, "")


# Legacy functions for backward compatibility with existing tests
def get_test_result_template(template_name: str) -> Dict[str, Any]:
    """Get test result template by name.

    Args:
        template_name: Name of template to load

    Returns:
        Test result template dictionary
    """
    templates = {
        "success": {
            "status": "PASS",
            "duration": 0.001,
            "error_info": None
        },
        "failure": {
            "status": "FAIL",
            "duration": 0.002,
            "error_info": {
                "type": "AssertionError",
                "message": "Test failed",
                "traceback": "Traceback..."
            }
        },
        "error": {
            "status": "ERROR",
            "duration": 0.001,
            "error_info": {
                "type": "RuntimeError",
                "message": "Test error",
                "traceback": "Traceback..."
            }
        },
        "with_error_info": {
            "status": "ERROR",
            "duration": 0.001,
            "error_info": {
                "type": "AssertionError",
                "message": "Test assertion failed",
                "traceback": "Traceback (most recent call last):\n  File \"test.py\", line 1, in <module>\n    assert False, \"Test assertion failed\"\nAssertionError: Test assertion failed",
                "file_path": "/path/to/test.py",
                "line_number": 42
            }
        },
        "test_example": {
            "name": "test_example_method",
            "classname": "TestExampleClass",
            "status": "PASS",
            "duration": 0.001,
            "error_info": None
        }
    }

    return templates.get(template_name, {})


def get_timing_config(config_name: str) -> Any:
    """Get timing configuration by name.

    Args:
        config_name: Name of timing configuration

    Returns:
        Timing configuration (can be dictionary or string)
    """
    configs = {
        "fast": {"min_duration": 0.001, "max_duration": 0.01},
        "slow": {"min_duration": 1.0, "max_duration": 5.0},
        "default": {"min_duration": 0.01, "max_duration": 0.1},
        "standard_timestamp": "2024-01-15T10:30:45.123456"
    }

    return configs.get(config_name, configs["default"])


def get_command_template(template_name: str) -> str:
    """Get command template by name.

    Args:
        template_name: Name of command template

    Returns:
        Command template string
    """
    templates = {
        "basic": "wobble --category regression",
        "verbose": "wobble --category all --verbose",
        "file_output": "wobble --category all --log-file results.txt"
    }

    return templates.get(template_name, "wobble")


def create_fake_test_directory(name: str = "fake_tests", base_path: Optional[Path] = None) -> Path:
    """Create a fake test directory (legacy function).

    Args:
        name: Name of the fake test directory
        base_path: Base path where to create the directory (optional)

    Returns:
        Path to the created fake test directory
    """
    loader = WobbleTestDataLoader()
    if base_path:
        # Create directory in specified base path
        test_dir = base_path / name
        test_dir.mkdir(parents=True, exist_ok=True)
        loader._create_test_files_in_directory(test_dir, name)
        return test_dir
    else:
        # Use default behavior
        test_dir = loader.create_fake_test_directory(name)
        return test_dir


def cleanup_fake_directory(directory_path: Union[str, Path]) -> None:
    """Clean up a fake test directory (legacy function).

    Args:
        directory_path: Path to directory to clean up
    """
    import shutil
    path_str = str(directory_path)
    if os.path.exists(path_str):
        shutil.rmtree(path_str, ignore_errors=True)

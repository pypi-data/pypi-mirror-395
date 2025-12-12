"""Test discovery engine for wobble framework.

This module provides functionality to discover and categorize tests across
different repository structures and organizational patterns.
"""

import os
import unittest
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any
from datetime import datetime
from .decorators import get_test_metadata, has_wobble_metadata


class TestDiscoveryEngine:
    """Core test discovery engine for wobble framework.
    
    Supports both hierarchical (tests/regression/, tests/integration/) and
    flat (tests/ with decorator-based categorization) directory structures.
    """
    
    def __init__(self, root_path: str = "."):
        """Initialize the discovery engine.
        
        Args:
            root_path: Root directory to search for tests (default: current directory)
        """
        self.root_path = Path(root_path).resolve()
        self.test_suites = {}
        self.discovered_tests = []
        
    def discover_tests(self, pattern: str = "test*.py") -> Dict[str, List]:
        """Discover all tests in the repository.
        
        Args:
            pattern: File pattern to match test files (default: "test*.py")
            
        Returns:
            Dictionary categorizing discovered tests by type
            
        Example:
            engine = TestDiscoveryEngine()
            tests = engine.discover_tests()
            print(f"Found {len(tests['regression'])} regression tests")
        """
        self.discovered_tests = []
        
        # Find all test directories
        test_dirs = self._find_test_directories()
        
        # Discover tests in each directory
        for test_dir in test_dirs:
            self._discover_in_directory(test_dir, pattern)
        
        # Categorize discovered tests
        categorized = self._categorize_tests()
        
        return categorized
    
    def _find_test_directories(self) -> List[Path]:
        """Find all directories containing tests.

        Returns:
            List of Path objects pointing to test directories
        """
        test_dirs = []
        discovered_paths = set()  # Track discovered paths to prevent duplicates

        # Look for common test directory patterns
        common_patterns = [
            "tests",
            "test",
            "Tests",
            "Test"
        ]

        for pattern in common_patterns:
            test_dir = self.root_path / pattern
            if test_dir.exists() and test_dir.is_dir():
                # Only add if not already discovered and contains actual test files
                if test_dir not in discovered_paths and self._contains_test_files(test_dir):
                    test_dirs.append(test_dir)
                    discovered_paths.add(test_dir)

                # Check for subdirectories (hierarchical structure)
                for subdir in test_dir.iterdir():
                    if (subdir.is_dir() and
                        not subdir.name.startswith('.') and
                        not subdir.name.startswith('__') and  # Skip __pycache__ etc.
                        subdir not in discovered_paths and
                        self._contains_test_files(subdir)):
                        test_dirs.append(subdir)
                        discovered_paths.add(subdir)

        return test_dirs

    def _contains_test_files(self, directory: Path) -> bool:
        """Check if directory contains actual test files (not just compiled files).

        Args:
            directory: Directory to check

        Returns:
            True if directory contains .py test files, False otherwise
        """
        try:
            for file_path in directory.iterdir():
                if (file_path.is_file() and
                    file_path.suffix == '.py' and
                    file_path.name.startswith('test')):
                    return True
            return False
        except (OSError, PermissionError):
            return False
    
    def _discover_in_directory(self, directory: Path, pattern: str) -> None:
        """Discover tests in a specific directory.
        
        Args:
            directory: Directory to search
            pattern: File pattern to match
        """
        try:
            # Use unittest's discovery mechanism
            loader = unittest.TestLoader()
            suite = loader.discover(str(directory), pattern=pattern)
            
            # Extract test information
            for test_group in suite:
                if hasattr(test_group, '_tests'):
                    for test_case in test_group._tests:
                        if hasattr(test_case, '_tests'):
                            for individual_test in test_case._tests:
                                self._process_test(individual_test, directory)
                        else:
                            self._process_test(test_case, directory)
                            
        except Exception as e:
            # Log discovery errors but continue
            print(f"Warning: Could not discover tests in {directory}: {e}")

    def _is_error_holder(self, test_case) -> bool:
        """Check if test case is an _ErrorHolder representing import/loading failure.

        Args:
            test_case: The test case object to check

        Returns:
            True if this is an _ErrorHolder, False otherwise
        """
        return test_case.__class__.__name__ == '_ErrorHolder'

    def _process_error_holder(self, error_holder, directory: Path) -> None:
        """Process an _ErrorHolder object representing an import/loading error.

        Args:
            error_holder: The _ErrorHolder object
            directory: Directory where the error occurred
        """
        # Extract error information from the _ErrorHolder
        error_description = getattr(error_holder, 'description', 'Unknown import error')
        error_id = error_holder.id() if hasattr(error_holder, 'id') else error_description

        # Parse the error description for more meaningful information
        enhanced_info = self._parse_error_holder_description(error_description)

        # Create error info for reporting
        error_info = {
            'error_holder': error_holder,
            'error_type': 'import_failure',
            'error_description': error_description,
            'error_id': error_id,
            'test_class': '_ErrorHolder',
            'test_module': 'unittest.suite',
            'directory': directory,
            'file_path': enhanced_info.get('file_path'),
            'metadata': {
                'is_error_holder': True,
                'enhanced_info': enhanced_info
            }
        }

        # Store in discovered tests under a special category
        if 'import_errors' not in self.discovered_tests:
            self.discovered_tests['import_errors'] = []
        self.discovered_tests['import_errors'].append(error_info)

        # Log the import error with enhanced information
        enhanced_message = self._format_enhanced_error_message(enhanced_info)
        print(f"Import/loading error detected: {enhanced_message} in {directory}")

    def _parse_error_holder_description(self, description: str) -> dict:
        """Parse _ErrorHolder description to extract meaningful information.

        Args:
            description: The error description from _ErrorHolder

        Returns:
            Dictionary with parsed information
        """
        import re

        # Initialize result
        result = {
            'original_description': description,
            'error_type': 'import_error',
            'test_class': None,
            'test_module': None,
            'file_path': None,
            'method_name': None,
            'enhanced_message': description
        }

        # Parse patterns like "setUpClass (test_hatch_installer.TestHatchInstaller)"
        setup_pattern = r'(setUpClass|setUp|tearDown|tearDownClass)\s*\(([^.]+)\.([^)]+)\)'
        match = re.match(setup_pattern, description)

        if match:
            method_name, module_name, class_name = match.groups()
            result.update({
                'method_name': method_name,
                'test_module': module_name,
                'test_class': class_name,
                'file_path': f"{module_name}.py",
                'enhanced_message': f"{method_name} failed in {class_name} ({module_name}.py)"
            })
        else:
            # Try to extract class and module from other patterns
            # Pattern like "module.ClassName"
            class_pattern = r'([^.]+)\.([^.]+)$'
            match = re.search(class_pattern, description)
            if match:
                module_name, class_name = match.groups()
                result.update({
                    'test_module': module_name,
                    'test_class': class_name,
                    'file_path': f"{module_name}.py",
                    'enhanced_message': f"Import failed for {class_name} in {module_name}.py"
                })

        return result

    def _format_enhanced_error_message(self, enhanced_info: dict) -> str:
        """Format an enhanced error message from parsed information.

        Args:
            enhanced_info: Parsed error information

        Returns:
            Enhanced error message string
        """
        if enhanced_info.get('method_name') and enhanced_info.get('test_class'):
            return (f"{enhanced_info['method_name']} failed in {enhanced_info['test_class']} "
                   f"(check {enhanced_info.get('file_path', 'test file')} for import issues)")
        elif enhanced_info.get('test_class'):
            return (f"Import failed for {enhanced_info['test_class']} "
                   f"(check {enhanced_info.get('file_path', 'test file')} for missing dependencies)")
        else:
            return f"Import error: {enhanced_info['original_description']}"
    
    def _process_test(self, test_case, directory: Path) -> None:
        """Process an individual test case.

        Args:
            test_case: The unittest test case or _ErrorHolder
            directory: Directory where the test was found
        """
        # Check if this is an _ErrorHolder representing an import/loading error
        if self._is_error_holder(test_case):
            self._process_error_holder(test_case, directory)
            return

        test_info = {
            'test_case': test_case,
            'test_method': test_case._testMethodName,
            'test_class': test_case.__class__.__name__,
            'test_module': test_case.__class__.__module__,
            'directory': directory,
            'file_path': None,
            'metadata': {}
        }
        
        # Try to get the actual test method
        try:
            test_method = getattr(test_case, test_case._testMethodName)
            test_info['metadata'] = get_test_metadata(test_method)
            
            # Try to determine file path
            if hasattr(test_case.__class__, '__file__'):
                test_info['file_path'] = Path(test_case.__class__.__file__)
            else:
                # Fallback: construct file path from module name and directory
                module_name = test_case.__class__.__module__
                if module_name:
                    # Handle different module name patterns
                    if '.' in module_name:
                        # For modules like 'development.test_development' or 'test_auth'
                        parts = module_name.split('.')
                        if len(parts) >= 2:
                            # Try subdirectory structure: development/test_development.py
                            subdir = parts[0]
                            module_file = parts[1]
                            potential_file = directory / subdir / f"{module_file}.py"
                            if potential_file.exists():
                                test_info['file_path'] = potential_file
                            else:
                                # Try flat structure: test_development.py
                                potential_file = directory / f"{module_file}.py"
                                if potential_file.exists():
                                    test_info['file_path'] = potential_file
                        else:
                            # Single part module name
                            module_file = parts[0]
                            potential_file = directory / f"{module_file}.py"
                            if potential_file.exists():
                                test_info['file_path'] = potential_file
                    else:
                        # No dots in module name
                        potential_file = directory / f"{module_name}.py"
                        if potential_file.exists():
                            test_info['file_path'] = potential_file
                
        except AttributeError:
            pass
        
        self.discovered_tests.append(test_info)
    
    def _categorize_tests(self) -> Dict[str, List]:
        """Categorize discovered tests by type.
        
        Returns:
            Dictionary with test categories as keys and test lists as values
        """
        categories = {
            'regression': [],
            'integration': [],
            'development': [],
            'uncategorized': []
        }
        
        for test_info in self.discovered_tests:
            category = self._determine_category(test_info)
            categories[category].append(test_info)
        
        return categories
    
    def _determine_category(self, test_info: Dict) -> str:
        """Determine the category of a test.
        
        Args:
            test_info: Test information dictionary
            
        Returns:
            Category string ('regression', 'integration', 'development', 'uncategorized')
        """
        # Check decorator-based categorization first
        metadata = test_info.get('metadata', {})
        if metadata.get('category'):
            return metadata['category']
        
        # Check directory-based categorization
        directory = test_info.get('directory')
        if directory:
            dir_name = directory.name.lower()
            
            if 'regression' in dir_name:
                return 'regression'
            elif 'integration' in dir_name:
                return 'integration'
            elif 'development' in dir_name or 'dev' in dir_name:
                return 'development'
        
        # Default to uncategorized
        return 'uncategorized'
    
    def get_test_count_summary(self) -> Dict[str, int]:
        """Get a summary of test counts by category.

        Returns:
            Dictionary with category names and test counts
        """
        if not self.discovered_tests:
            self.discover_tests()

        categorized = self._categorize_tests()
        return {category: len(tests) for category, tests in categorized.items()}

    def get_discovery_output(self, verbosity: int = 1) -> str:
        """Get formatted discovery output based on verbosity level.

        Args:
            verbosity: Output verbosity level (1=counts only, 2=uncategorized details, 3=all details)

        Returns:
            Formatted discovery output string
        """
        if not self.discovered_tests:
            self.discover_tests()

        categorized = self._categorize_tests()
        summary = {category: len(tests) for category, tests in categorized.items()}
        total_tests = sum(summary.values())

        output_lines = []

        # Level 1: Counts only (default behavior)
        output_lines.append(f"Total tests discovered: {total_tests}")

        for category in ['regression', 'integration', 'development', 'slow', 'skip_ci', 'uncategorized']:
            count = summary.get(category, 0)
            if count > 0:
                output_lines.append(f"{category.title()}: {count}")

        # Level 2: Add uncategorized test details
        if verbosity >= 2 and 'uncategorized' in categorized and categorized['uncategorized']:
            output_lines.append("\nUncategorized tests:")
            for test_info in categorized['uncategorized']:
                test_name = f"{test_info['test_class']}.{test_info['test_method']}"
                file_path = test_info.get('file_path', 'unknown')
                output_lines.append(f"  {test_name} ({file_path})")

        # Level 3: Add all test details
        if verbosity >= 3:
            for category in ['regression', 'integration', 'development', 'slow', 'skip_ci']:
                if category in categorized and categorized[category]:
                    output_lines.append(f"\n{category.title()} tests:")
                    for test_info in categorized[category]:
                        # Format as: tests/test_auth.py::TestAuth::test_valid_login
                        file_path = test_info.get('file_path', 'unknown')
                        if file_path != 'unknown' and file_path:
                            # Convert absolute path to relative path starting with tests/
                            file_path_obj = Path(file_path)
                            if 'tests' in file_path_obj.parts:
                                tests_index = file_path_obj.parts.index('tests')
                                relative_path = Path(*file_path_obj.parts[tests_index:])
                                test_name = f"{relative_path}::{test_info['test_class']}::{test_info['test_method']}"
                            else:
                                test_name = f"{file_path_obj.name}::{test_info['test_class']}::{test_info['test_method']}"
                        else:
                            test_name = f"{test_info['test_class']}.{test_info['test_method']}"

                        decorators = self._get_wobble_decorators(test_info)
                        decorator_str = f" [{', '.join(decorators)}]" if decorators else ""
                        output_lines.append(f"  {test_name}{decorator_str}")

        return "\n".join(output_lines)

    def get_discovery_data(self, verbosity: int = 1) -> Dict[str, Any]:
        """Get structured discovery data for JSON formatting.

        Args:
            verbosity: Output verbosity level (1=counts only, 2=uncategorized details, 3=all details)

        Returns:
            Structured discovery data dictionary
        """
        if not self.discovered_tests:
            self.discover_tests()

        categorized = self._categorize_tests()
        summary = {category: len(tests) for category, tests in categorized.items()}
        total_tests = sum(summary.values())

        # Base data structure matching design specification section 1.3
        discovery_data = {
            "discovery_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": total_tests,
                "categories": summary
            }
        }

        # Level 2: Add uncategorized test details (only if not level 3)
        if verbosity == 2 and 'uncategorized' in categorized and categorized['uncategorized']:
            uncategorized_tests = []
            for test_info in categorized['uncategorized']:
                # Convert file path to string for JSON serialization
                file_path = test_info.get('file_path', 'unknown')
                file_str = str(file_path) if file_path and file_path != 'unknown' else 'unknown'

                test_data = {
                    "name": f"{test_info['test_class']}.{test_info['test_method']}",
                    "class": test_info['test_class'],
                    "method": test_info['test_method'],
                    "module": test_info.get('module', 'unknown'),
                    "file": file_str,
                    "full_name": f"{test_info.get('module', 'unknown')}.{test_info['test_class']}.{test_info['test_method']}"
                }
                uncategorized_tests.append(test_data)
            discovery_data["discovery_summary"]["uncategorized"] = uncategorized_tests

        # Level 3: Add all test details by category
        if verbosity >= 3:
            tests_by_category = {}
            for category in ['regression', 'integration', 'development', 'slow', 'skip_ci', 'uncategorized']:
                if category in categorized and categorized[category]:
                    category_tests = []
                    for test_info in categorized[category]:
                        decorators = self._get_wobble_decorators(test_info)

                        # Convert file path to string for JSON serialization
                        file_path = test_info.get('file_path', 'unknown')
                        file_str = str(file_path) if file_path and file_path != 'unknown' else 'unknown'

                        test_data = {
                            "name": f"{test_info['test_class']}.{test_info['test_method']}",
                            "class": test_info['test_class'],
                            "method": test_info['test_method'],
                            "module": test_info.get('module', 'unknown'),
                            "file": file_str,
                            "full_name": f"{test_info.get('module', 'unknown')}.{test_info['test_class']}.{test_info['test_method']}",
                            "decorators": decorators
                        }
                        category_tests.append(test_data)
                    tests_by_category[category] = category_tests
            discovery_data["discovery_summary"]["tests_by_category"] = tests_by_category

        return discovery_data

    def _get_wobble_decorators(self, test_info: Dict) -> List[str]:
        """Extract Wobble decorator names from test info.

        Args:
            test_info: Test information dictionary

        Returns:
            List of Wobble decorator names
        """
        decorators = []
        metadata = test_info.get('metadata', {})

        # Check for Wobble-specific decorators
        if metadata.get('regression'):
            decorators.append('@regression_test')
        if metadata.get('integration'):
            decorators.append('@integration_test')
        if metadata.get('development'):
            decorators.append('@development_test')
        if metadata.get('slow'):
            decorators.append('@slow_test')
        if metadata.get('skip_ci'):
            decorators.append('@skip_ci')

        return decorators
    
    def filter_tests(self, 
                    categories: Optional[List[str]] = None,
                    exclude_slow: bool = False,
                    exclude_ci: bool = False) -> List[Dict]:
        """Filter tests based on criteria.
        
        Args:
            categories: List of categories to include (None = all)
            exclude_slow: Whether to exclude slow tests
            exclude_ci: Whether to exclude CI-skipped tests
            
        Returns:
            List of filtered test information dictionaries
        """
        if not self.discovered_tests:
            self.discover_tests()
        
        filtered = []
        
        for test_info in self.discovered_tests:
            # Check category filter
            if categories:
                test_category = self._determine_category(test_info)
                if test_category not in categories:
                    continue
            
            # Check slow test filter
            metadata = test_info.get('metadata', {})
            if exclude_slow and metadata.get('slow'):
                continue
            
            # Check CI skip filter
            if exclude_ci and metadata.get('skip_ci'):
                continue
            
            filtered.append(test_info)
        
        return filtered
    
    def supports_hierarchical_structure(self) -> bool:
        """Check if the repository uses hierarchical test structure.
        
        Returns:
            True if hierarchical structure is detected, False otherwise
        """
        test_dirs = self._find_test_directories()
        
        hierarchical_indicators = [
            'regression', 'integration', 'development', 'unit'
        ]
        
        for test_dir in test_dirs:
            if any(indicator in test_dir.name.lower() 
                   for indicator in hierarchical_indicators):
                return True
        
        return False
    
    def supports_decorator_structure(self) -> bool:
        """Check if the repository uses decorator-based test categorization.
        
        Returns:
            True if decorator-based structure is detected, False otherwise
        """
        if not self.discovered_tests:
            self.discover_tests()
        
        # Check if any tests have wobble metadata
        for test_info in self.discovered_tests:
            if test_info.get('metadata'):
                return True
        
        return False

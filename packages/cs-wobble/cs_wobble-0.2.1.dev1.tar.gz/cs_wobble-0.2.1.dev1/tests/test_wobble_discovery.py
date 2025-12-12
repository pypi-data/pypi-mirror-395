"""Tests for wobble test discovery functionality.

This module tests the test discovery engine that finds and categorizes tests
across different repository structures.
"""

import unittest
import tempfile
import os
from pathlib import Path
from wobble.discovery import TestDiscoveryEngine
from tests.test_data_utils import create_fake_test_directory, cleanup_fake_directory


class TestWobbleDiscoveryEngine(unittest.TestCase):
    """Test wobble test discovery engine."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.discovery_engine = TestDiscoveryEngine(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        cleanup_fake_directory(Path(self.temp_dir))
    
    def test_discovery_engine_initialization(self):
        """Test that discovery engine initializes correctly."""
        engine = TestDiscoveryEngine(".")
        self.assertIsNotNone(engine.root_path)
        self.assertEqual(engine.test_suites, {})
        self.assertEqual(engine.discovered_tests, [])
    
    def test_find_test_directories(self):
        """Test finding test directories."""
        # Create fake test directory using centralized utilities
        fake_test_dir = create_fake_test_directory('mixed_categories', Path(self.temp_dir))

        # Update discovery engine to use the fake test directory
        self.discovery_engine = TestDiscoveryEngine(str(fake_test_dir))

        # Test discovery
        test_dirs = self.discovery_engine._find_test_directories()

        # Should find the tests directory
        tests_dir = fake_test_dir / "tests"
        self.assertTrue(any(str(tests_dir) in str(d) for d in test_dirs))

        # Clean up
        cleanup_fake_directory(fake_test_dir)
    
    def test_supports_hierarchical_structure_detection(self):
        """Test detection of hierarchical test structure."""
        # Create fake hierarchical test directory using centralized utilities
        fake_test_dir = create_fake_test_directory('mixed_categories', Path(self.temp_dir))

        # Update discovery engine to use the fake test directory
        self.discovery_engine = TestDiscoveryEngine(str(fake_test_dir))

        # Test hierarchical detection
        self.assertTrue(self.discovery_engine.supports_hierarchical_structure())

        # Clean up
        cleanup_fake_directory(fake_test_dir)
    
    def test_get_test_count_summary(self):
        """Test getting test count summary."""
        # Create fake test directory using centralized utilities
        fake_test_dir = create_fake_test_directory('mixed_categories', Path(self.temp_dir))

        # Update discovery engine to use the fake test directory
        self.discovery_engine = TestDiscoveryEngine(str(fake_test_dir))

        # Get summary
        summary = self.discovery_engine.get_test_count_summary()

        # Clean up
        cleanup_fake_directory(fake_test_dir)
        
        # Should have discovered tests
        total_tests = sum(summary.values())
        self.assertGreater(total_tests, 0)
    
    def test_filter_tests_by_category(self):
        """Test filtering tests by category."""
        # This test validates the filtering mechanism
        # In a real scenario, tests would be categorized by decorators or directory structure
        
        # Discover all tests first
        self.discovery_engine.discover_tests()
        
        # Test filtering (should not crash even with no categorized tests)
        filtered = self.discovery_engine.filter_tests(categories=['regression'])
        self.assertIsInstance(filtered, list)
        
        # Test excluding slow tests
        filtered_no_slow = self.discovery_engine.filter_tests(exclude_slow=True)
        self.assertIsInstance(filtered_no_slow, list)
        
        # Test excluding CI tests
        filtered_no_ci = self.discovery_engine.filter_tests(exclude_ci=True)
        self.assertIsInstance(filtered_no_ci, list)


class TestWobbleDiscoveryIntegration(unittest.TestCase):
    """Integration tests for discovery engine with real test files."""
    
    def test_discover_current_repository_tests(self):
        """Test discovering tests in the current repository."""
        # Use current directory (should find our own tests)
        engine = TestDiscoveryEngine(".")
        
        discovered = engine.discover_tests()
        
        # Should find test categories
        self.assertIsInstance(discovered, dict)
        self.assertIn('uncategorized', discovered)
        
        # Should find some tests (at least our own)
        total_tests = sum(len(tests) for tests in discovered.values())
        self.assertGreater(total_tests, 0)
    
    def test_discovery_with_different_patterns(self):
        """Test discovery with different file patterns."""
        engine = TestDiscoveryEngine(".")
        
        # Test with default pattern
        default_tests = engine.discover_tests(pattern="test*.py")
        
        # Test with alternative pattern
        alt_tests = engine.discover_tests(pattern="*test.py")
        
        # Both should return valid results
        self.assertIsInstance(default_tests, dict)
        self.assertIsInstance(alt_tests, dict)
    
    def test_categorization_logic(self):
        """Test the test categorization logic."""
        engine = TestDiscoveryEngine(".")
        engine.discover_tests()
        
        # Test the categorization method with sample test info
        sample_test_info = {
            'metadata': {'category': 'regression'},
            'directory': Path('tests/regression')
        }
        
        category = engine._determine_category(sample_test_info)
        self.assertEqual(category, 'regression')
        
        # Test directory-based categorization
        dir_test_info = {
            'metadata': {},
            'directory': Path('tests/integration')
        }
        
        category = engine._determine_category(dir_test_info)
        self.assertEqual(category, 'integration')
        
        # Test uncategorized
        uncategorized_info = {
            'metadata': {},
            'directory': Path('tests')
        }
        
        category = engine._determine_category(uncategorized_info)
        self.assertEqual(category, 'uncategorized')


if __name__ == '__main__':
    unittest.main(verbosity=2)

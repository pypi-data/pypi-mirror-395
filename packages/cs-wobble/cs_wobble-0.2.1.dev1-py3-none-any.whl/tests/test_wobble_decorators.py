"""Tests for wobble decorators functionality.

This module tests the core decorator functionality that categorizes tests
according to the organizational testing guidelines.
"""

import unittest
from wobble.decorators import (
    regression_test, integration_test, development_test,
    slow_test, skip_ci, get_test_metadata, has_wobble_metadata
)


class TestWobbleDecorators(unittest.TestCase):
    """Test wobble decorator functionality."""
    
    def test_regression_test_decorator(self):
        """Test that regression_test decorator adds correct metadata."""
        @regression_test
        def sample_test():
            pass
        
        self.assertTrue(hasattr(sample_test, '_wobble_regression'))
        self.assertTrue(sample_test._wobble_regression)
        self.assertEqual(sample_test._wobble_category, 'regression')
    
    def test_integration_test_decorator(self):
        """Test that integration_test decorator adds correct metadata."""
        @integration_test(scope="component")
        def sample_test():
            pass
        
        self.assertTrue(hasattr(sample_test, '_wobble_integration'))
        self.assertTrue(sample_test._wobble_integration)
        self.assertEqual(sample_test._wobble_category, 'integration')
        self.assertEqual(sample_test._wobble_scope, 'component')
    
    def test_development_test_decorator(self):
        """Test that development_test decorator adds correct metadata."""
        @development_test(phase="feature-validation")
        def sample_test():
            pass
        
        self.assertTrue(hasattr(sample_test, '_wobble_development'))
        self.assertTrue(sample_test._wobble_development)
        self.assertEqual(sample_test._wobble_category, 'development')
        self.assertEqual(sample_test._wobble_phase, 'feature-validation')
    
    def test_slow_test_decorator(self):
        """Test that slow_test decorator adds correct metadata."""
        @slow_test
        def sample_test():
            pass
        
        self.assertTrue(hasattr(sample_test, '_wobble_slow'))
        self.assertTrue(sample_test._wobble_slow)
    
    def test_skip_ci_decorator(self):
        """Test that skip_ci decorator adds correct metadata."""
        @skip_ci
        def sample_test():
            pass
        
        self.assertTrue(hasattr(sample_test, '_wobble_skip_ci'))
        self.assertTrue(sample_test._wobble_skip_ci)
    
    def test_get_test_metadata(self):
        """Test metadata extraction from decorated functions."""
        @regression_test
        @slow_test
        def sample_test():
            pass
        
        metadata = get_test_metadata(sample_test)
        
        self.assertEqual(metadata['category'], 'regression')
        self.assertTrue(metadata['regression'])
        self.assertTrue(metadata['slow'])
    
    def test_has_wobble_metadata(self):
        """Test detection of wobble metadata."""
        @regression_test
        def decorated_test():
            pass
        
        def undecorated_test():
            pass
        
        self.assertTrue(has_wobble_metadata(decorated_test))
        self.assertFalse(has_wobble_metadata(undecorated_test))
    
    def test_decorator_preserves_function_properties(self):
        """Test that decorators preserve original function properties."""
        @regression_test
        def sample_function():
            """Sample docstring."""
            return "test_result"
        
        # Function should still work normally
        self.assertEqual(sample_function(), "test_result")
        
        # Docstring should be preserved
        self.assertEqual(sample_function.__doc__, "Sample docstring.")
        
        # Function name should be preserved
        self.assertEqual(sample_function.__name__, "sample_function")


class TestDecoratorCombinations(unittest.TestCase):
    """Test combinations of wobble decorators."""
    
    def test_multiple_decorators(self):
        """Test that multiple decorators can be combined."""
        @regression_test
        @slow_test
        @skip_ci
        def sample_test():
            pass
        
        metadata = get_test_metadata(sample_test)
        
        self.assertEqual(metadata['category'], 'regression')
        self.assertTrue(metadata['regression'])
        self.assertTrue(metadata['slow'])
        self.assertTrue(metadata['skip_ci'])
    
    def test_integration_with_scope(self):
        """Test integration decorator with different scopes."""
        @integration_test(scope="service")
        def service_test():
            pass
        
        @integration_test(scope="system")
        def system_test():
            pass
        
        service_metadata = get_test_metadata(service_test)
        system_metadata = get_test_metadata(system_test)
        
        self.assertEqual(service_metadata['scope'], 'service')
        self.assertEqual(system_metadata['scope'], 'system')
    
    def test_development_with_phase(self):
        """Test development decorator with phase information."""
        @development_test(phase="prototype")
        def prototype_test():
            pass
        
        @development_test()
        def general_dev_test():
            pass
        
        prototype_metadata = get_test_metadata(prototype_test)
        general_metadata = get_test_metadata(general_dev_test)
        
        self.assertEqual(prototype_metadata['phase'], 'prototype')
        self.assertNotIn('phase', general_metadata)


if __name__ == '__main__':
    unittest.main(verbosity=2)

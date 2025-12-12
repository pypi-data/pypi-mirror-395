"""Test file to demonstrate Wobble decorator display functionality."""

import unittest
from wobble.decorators import regression_test, integration_test, development_test, slow_test, skip_ci


class TestDecoratorDisplay(unittest.TestCase):
    """Test class to demonstrate decorator display."""
    
    @regression_test
    def test_regression_example(self):
        """Example regression test."""
        self.assertTrue(True)
    
    @integration_test
    def test_integration_example(self):
        """Example integration test."""
        self.assertTrue(True)
    
    @development_test
    def test_development_example(self):
        """Example development test."""
        self.assertTrue(True)
    
    @slow_test
    def test_slow_example(self):
        """Example slow test."""
        self.assertTrue(True)
    
    @skip_ci
    def test_skip_ci_example(self):
        """Example CI-skipped test."""
        self.assertTrue(True)
    
    @regression_test
    @slow_test
    def test_multiple_decorators(self):
        """Example test with multiple decorators."""
        self.assertTrue(True)
    
    def test_no_decorators(self):
        """Example test with no Wobble decorators."""
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

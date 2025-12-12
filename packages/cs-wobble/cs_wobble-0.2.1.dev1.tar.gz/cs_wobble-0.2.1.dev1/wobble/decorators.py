"""Core test decorators for wobble framework.

This module provides decorators for categorizing and tagging tests according to
the organizational testing guidelines.
"""

from functools import wraps
from typing import Optional, Callable, Any


def regression_test(func: Callable) -> Callable:
    """Mark test as regression test (permanent, prevents breaking changes).
    
    Regression tests are permanent tests that validate core functionality
    and prevent breaking changes. They should continue to pass throughout
    the software's lifecycle.
    
    Args:
        func: The test function to decorate
        
    Returns:
        The decorated function with regression test metadata
        
    Example:
        @regression_test
        def test_core_functionality(self):
            self.assertTrue(core_function())
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Add wobble metadata
    wrapper._wobble_regression = True
    wrapper._wobble_category = 'regression'
    
    return wrapper


def integration_test(scope: str = "component"):
    """Mark test as integration test with scope specification.

    Integration tests validate interactions between components or systems.
    This decorator requires parentheses and supports scope specification.

    Args:
        scope: The scope of integration testing
               - "component": Tests interaction between internal components
               - "service": Tests interaction with external services
               - "system": Tests end-to-end system integration

    Returns:
        Decorator function

    Example:
        @integration_test(scope="service")
        def test_api_integration(self):
            response = api_client.get("/health")
            self.assertEqual(response.status_code, 200)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Add wobble metadata
        wrapper._wobble_integration = True
        wrapper._wobble_category = 'integration'
        wrapper._wobble_scope = scope

        return wrapper

    return decorator


def development_test(phase: Optional[str] = None) -> Callable:
    """Mark test as development test (temporary validation).
    
    Development tests are temporary tests used during development to validate
    work in progress. They may be removed once the feature is stable.
    
    Args:
        phase: Optional phase identifier for the development work
               
    Returns:
        Decorator function that marks tests as development tests
        
    Example:
        @development_test(phase="feature-validation")
        def test_new_feature_behavior(self):
            result = new_feature()
            self.assertIsNotNone(result)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Add wobble metadata
        wrapper._wobble_development = True
        wrapper._wobble_category = 'development'
        if phase is not None:
            wrapper._wobble_phase = phase
        
        return wrapper
    
    return decorator


def slow_test(func: Callable) -> Callable:
    """Mark test as slow-running (>5 seconds).
    
    Slow tests are tests that take significant time to execute and may be
    skipped in certain environments or during rapid development cycles.
    
    Args:
        func: The test function to decorate
        
    Returns:
        The decorated function with slow test metadata
        
    Example:
        @slow_test
        @integration_test(scope="system")
        def test_full_system_workflow(self):
            # Long-running test that exercises the entire system
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Add wobble metadata
    wrapper._wobble_slow = True
    
    return wrapper


def skip_ci(func: Callable) -> Callable:
    """Mark test to skip in CI environment.
    
    Tests marked with this decorator will be skipped when running in
    continuous integration environments, typically for tests that require
    interactive input or local resources.
    
    Args:
        func: The test function to decorate
        
    Returns:
        The decorated function with CI skip metadata
        
    Example:
        @skip_ci
        def test_interactive_feature(self):
            # Test that requires user interaction
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Add wobble metadata
    wrapper._wobble_skip_ci = True
    
    return wrapper


def get_test_metadata(test_func: Callable) -> dict:
    """Extract wobble metadata from a test function.
    
    Args:
        test_func: The test function to analyze
        
    Returns:
        Dictionary containing all wobble metadata for the test
        
    Example:
        metadata = get_test_metadata(my_test_function)
        if metadata.get('category') == 'regression':
            print("This is a regression test")
    """
    metadata = {}
    
    # Extract category information
    if hasattr(test_func, '_wobble_category'):
        metadata['category'] = test_func._wobble_category
    
    # Extract specific test type flags
    if hasattr(test_func, '_wobble_regression'):
        metadata['regression'] = test_func._wobble_regression
    
    if hasattr(test_func, '_wobble_integration'):
        metadata['integration'] = test_func._wobble_integration
        if hasattr(test_func, '_wobble_scope'):
            metadata['scope'] = test_func._wobble_scope
    
    if hasattr(test_func, '_wobble_development'):
        metadata['development'] = test_func._wobble_development
        if hasattr(test_func, '_wobble_phase'):
            metadata['phase'] = test_func._wobble_phase
    
    # Extract additional flags
    if hasattr(test_func, '_wobble_slow'):
        metadata['slow'] = test_func._wobble_slow
    
    if hasattr(test_func, '_wobble_skip_ci'):
        metadata['skip_ci'] = test_func._wobble_skip_ci
    
    return metadata


def has_wobble_metadata(test_func: Callable) -> bool:
    """Check if a test function has any wobble metadata.
    
    Args:
        test_func: The test function to check
        
    Returns:
        True if the function has wobble metadata, False otherwise
    """
    wobble_attributes = [
        '_wobble_category', '_wobble_regression', '_wobble_integration',
        '_wobble_development', '_wobble_slow', '_wobble_skip_ci'
    ]
    
    return any(hasattr(test_func, attr) for attr in wobble_attributes)

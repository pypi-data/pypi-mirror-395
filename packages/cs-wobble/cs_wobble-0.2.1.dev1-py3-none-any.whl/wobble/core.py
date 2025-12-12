"""Core functionality for Wobble.

This module contains the main functionality of the wobble testing framework.
Core classes and functions for test discovery, execution, and reporting.
"""


def hello_world() -> str:
    """Return a simple greeting message.
    
    This is a placeholder function to demonstrate basic package structure.
    Replace this with your actual functionality.
    
    Returns:
        str: A greeting message
        
    Example:
        >>> from wobble.core import hello_world
        >>> hello_world()
        'Hello from Wobble!'
    """
    return "Hello from Wobble!"


class ExampleClass:
    """Example class to demonstrate package structure.
    
    This is a placeholder class. Replace with your actual classes.
    
    Attributes:
        name (str): The name associated with this instance
    """
    
    def __init__(self, name: str = "Wobble"):
        """Initialize the example class.

        Args:
            name (str): The name to associate with this instance
        """
        self.name = name
    
    def greet(self) -> str:
        """Return a personalized greeting.
        
        Returns:
            str: A personalized greeting message
            
        Example:
            >>> example = ExampleClass("World")
            >>> example.greet()
            'Hello, World! Welcome to Wobble.'
        """
        return f"Hello, {self.name}! Welcome to Wobble."
    
    def __str__(self) -> str:
        """Return string representation of the instance.
        
        Returns:
            str: String representation
        """
        return f"ExampleClass(name='{self.name}')"
    
    def __repr__(self) -> str:
        """Return detailed string representation of the instance.
        
        Returns:
            str: Detailed string representation
        """
        return f"ExampleClass(name='{self.name}')"

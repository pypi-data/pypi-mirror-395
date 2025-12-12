"""Wobble - Centralized testing package for Cracking Shells

This package provides centralized testing framework functionality for the CrackingShells organization.
"""

# Version will be managed by semantic-release
__version__ = "0.1.0"

# Import main functionality
from .decorators import (
    regression_test, integration_test, development_test,
    slow_test, skip_ci, get_test_metadata, has_wobble_metadata
)
from .discovery import TestDiscoveryEngine
from .runner import TestRunner
from .output import OutputFormatter
from .cli import main

# Define what gets imported with "from wobble import *"
__all__ = [
    # Decorators
    "regression_test", "integration_test", "development_test",
    "slow_test", "skip_ci", "get_test_metadata", "has_wobble_metadata",

    # Core classes
    "TestDiscoveryEngine", "TestRunner", "OutputFormatter",

    # CLI entry point
    "main"
]

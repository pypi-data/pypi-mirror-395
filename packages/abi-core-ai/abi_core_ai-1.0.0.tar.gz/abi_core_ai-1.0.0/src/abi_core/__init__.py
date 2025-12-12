"""
ABI Core - Agent-Based Infrastructure

A comprehensive toolkit for building, deploying, and managing AI agent infrastructures
with semantic layers, security policies, and collaborative workflows.
"""

__version__ = "1.0.0"
__author__ = "ABI Team"
__email__ = "team@abi-core.dev"

# Core CLI functionality
from .cli.main import cli

# Expose main modules for programmatic use
from . import common
from . import agent
from . import opa
from . import semantic
from . import security

__all__ = [
    "cli",
    "common", 
    "agent",
    "opa",
    "semantic",
    "security",
]
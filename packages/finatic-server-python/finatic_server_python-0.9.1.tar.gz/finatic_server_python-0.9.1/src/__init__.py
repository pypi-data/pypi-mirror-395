"""
Main SDK entry point.

This file is protected - customize exports as needed.
"""

# Re-export all other custom code (wrappers, utils, etc.)
# Re-export main client class explicitly (custom version that extends generated class)
# MUST come before export * from './custom' to ensure custom version is used
from .custom import *
from .custom import FinaticServer

# Re-export all generated code
from .generated import *

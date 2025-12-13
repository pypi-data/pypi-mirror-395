"""
Finatic Server Python SDK

This package re-exports everything from src to provide a clean import path:
    from finatic_server_python import FinaticServer

This matches the pattern used by:
    - Node.js: import { FinaticServer } from '@finatic/server-node'
    - TypeScript: import { FinaticConnect } from '@finatic/client'
    
Package name: finatic-server-python (pip install finatic-server-python)
Import name: finatic_server_python (from finatic_server_python import ...)
"""

# Re-export all from src
# When installed via pip, both src and finatic_server_python are in the same namespace
# In development, ensure src is importable by adding parent to path if needed
import sys
from pathlib import Path

# Add parent directory to path if src is not importable (development mode)
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src import *  # noqa: F403, F401

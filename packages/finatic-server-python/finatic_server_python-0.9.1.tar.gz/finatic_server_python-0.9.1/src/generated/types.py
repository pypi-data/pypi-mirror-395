"""
Type definitions for Finatic SDK.

This file is regenerated on each run - do not edit directly.
"""

from typing import TypeVar, Dict, Any, List, Optional, Generic

# Generic type variable for response data
T = TypeVar('T')

# Type alias for FinaticResponse structure
# This provides IntelliSense and type checking while runtime is a plain dict
FinaticResponse = Dict[str, Any]

# Note: At runtime, FinaticResponse[T] is just Dict[str, Any]
# The generic type parameter T is used for type hints and IntelliSense only
# The actual structure is: {
#   "success": {"data": T, "meta": dict | None},
#   "error": dict | None,
#   "warning": list[dict] | None
# }

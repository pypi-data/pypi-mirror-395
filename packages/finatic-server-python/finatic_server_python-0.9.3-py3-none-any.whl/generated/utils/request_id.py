"""
Request ID generator utility.

Generated - do not edit directly.
"""

import uuid


def generate_request_id() -> str:
    """Generate a unique request ID (UUID v4)."""
    return str(uuid.uuid4())

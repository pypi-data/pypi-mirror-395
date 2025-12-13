"""
Custom session wrapper - Extends generated wrapper.

This file is protected and will not be overwritten during regeneration.
Add your custom session logic here.
"""

from src.generated.wrappers.session import SessionWrapper


class CustomSessionWrapper(SessionWrapper):
    """Custom wrapper for session operations.

    Extend or override generated functions as needed.

    NOTE:
    - Portal URL caching is now handled in the generator (no-cache for get_portal_url)
    - Session creation methods (init_session, start_session) no longer have auth checks in generator
    - Response unwrapping is handled by the generator
    """

    # All session wrapper functionality is now handled by the generator
    # No custom overrides needed

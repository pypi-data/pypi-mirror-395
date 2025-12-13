"""
Custom brokers wrapper - Extends generated wrapper.

This file is protected and will not be overwritten during regeneration.
Add your custom brokers logic here.
"""

from src.generated.wrappers.brokers import BrokersWrapper


class CustomBrokersWrapper(BrokersWrapper):
    """Custom wrapper for brokers operations.

    Extend or override generated functions as needed.

    NOTE: Session headers and metadata transformation are now handled in the generator.
    """

    # Session headers are now automatically added by the generator for all broker endpoints
    # Metadata transformation is now handled by the generator for methods with with_metadata parameter
    # No custom overrides needed

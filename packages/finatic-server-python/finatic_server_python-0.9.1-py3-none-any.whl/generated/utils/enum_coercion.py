"""
Enum coercion utility (Phase 2C).

Generated - do not edit directly.

Provides case-insensitive matching of enum values.
Only matches actual enum value names (case-insensitive), no aliases.
"""

from typing import TypeVar, Type, Union, Optional

T = TypeVar('T')


def coerce_enum_value(
    input_value: Union[str, T, None],
    enum_class: Type[T],
    enum_name: str,
) -> Optional[T]:
    """Coerce a string or enum value to the matching enum value (case-insensitive).
    
    Args:
        input_value: String or enum value to coerce
        enum_class: Enum class to match against
        enum_name: Name of the enum (for error messages)
    
    Returns:
        The matching enum value, or None if input is None/undefined
    
    Raises:
        ValueError: If input cannot be coerced to a valid enum value
    
    Example:
        >>> status = coerce_enum_value('open', PublicPositionStatusEnum, 'positionStatus')
        >>> # Returns PublicPositionStatusEnum.Open (case-insensitive match)
    """
    if input_value is None:
        return None
    
    # If already an enum value, pass through
    if isinstance(input_value, enum_class):
        return input_value
    
    if isinstance(input_value, str):
        normalized = input_value.strip().lower()
        
        # Get all enum values
        enum_values = [e.value for e in enum_class]
        enum_keys = [e.name for e in enum_class]
        
        # Direct match by value (case-insensitive)
        for enum_val in enum_class:
            if enum_val.value.lower() == normalized:
                return enum_val
        
        # Match by key name (case-insensitive)
        for enum_val in enum_class:
            if enum_val.name.lower() == normalized:
                return enum_val
    
    # Not coercible - raise descriptive error
    allowed = ', '.join([e.value for e in enum_class])
    raise ValueError(f"Invalid {enum_name}: {input_value}. Allowed values: {allowed}")

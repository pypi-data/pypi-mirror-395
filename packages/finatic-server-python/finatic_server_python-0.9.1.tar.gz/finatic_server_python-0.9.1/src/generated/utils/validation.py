"""
Input validation utility with pydantic package (Phase 2B).

Generated - do not edit directly.
"""

from pydantic import BaseModel, Field, ValidationError as PydanticValidationError
from typing import Optional, Any, TypeVar, Type
from ..config import SdkConfig
from .error_handling import ValidationError

T = TypeVar('T', bound=BaseModel)


def validate_params(
    model_class: Type[T],
    params: dict,
    config: Optional[SdkConfig] = None
) -> T:
    """Validate parameters using pydantic model.
    
    Args:
        model_class: Pydantic model class
        params: Parameters to validate
        config: SDK configuration (optional)
    
    Returns:
        Validated model instance
    
    Raises:
        ValidationError: If validation fails and strict mode is enabled
    """
    if config and not config.validation_enabled:
        return model_class(**params)
    
    try:
        return model_class(**params)
    except PydanticValidationError as error:
        message = f"Validation failed: {error.errors()}"
        
        if config and config.validation_strict:
            raise ValidationError(message)
        else:
            import logging
            logging.warning(f"[Validation Warning] {message}")
            return model_class(**params)  # Try to create anyway

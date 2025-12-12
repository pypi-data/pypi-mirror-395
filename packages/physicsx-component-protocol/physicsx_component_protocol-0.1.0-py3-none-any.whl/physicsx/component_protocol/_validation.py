"""Validation utilities for ComponentFunction protocol compliance."""

from __future__ import annotations

import inspect
from typing import Any, cast, get_type_hints

from pydantic import BaseModel
from typeguard import check_type

from physicsx.component_protocol._protocol import ComponentFunction


def validate_component_function(
    function: Any, /
) -> ComponentFunction[BaseModel, BaseModel]:
    """Validate that a function conforms to ComponentFunction protocol.

    Performs comprehensive validation in 5 layers:
    1. Callable check
    2. Signature structure (1 parameter, no defaults, no *args/**kwargs)
    3. Type annotation presence (parameter and return)
    4. Pydantic BaseModel type requirements
    5. Protocol conformance (via typeguard)

    Args:
        function: The function to validate (positional-only)

    Returns:
        The same function object, validated for ComponentFunction conformance

    Raises:
        TypeError: If function doesn't conform, with specific explanation
    """
    # Layer 1: Callable check
    if not callable(function):
        raise TypeError(
            f"Component function must be callable, got {type(function).__name__}"
        )

    # Layer 2: Signature validation
    try:
        sig = inspect.signature(function)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Failed to inspect function signature: {e}") from e

    params = list(sig.parameters.values())

    if len(params) != 1:
        raise TypeError(
            f"Component function must accept exactly 1 parameter, got {len(params)}\n"
            f"Expected signature: def run(params: InputModel) -> OutputModel"
        )

    param = params[0]

    # Check for disallowed parameter kinds
    if param.kind == inspect.Parameter.VAR_POSITIONAL:
        raise TypeError(
            "Component parameter cannot be *args\n"
            "PXC-001 requires exactly one positional parameter"
        )
    if param.kind == inspect.Parameter.VAR_KEYWORD:
        raise TypeError(
            "Component parameter cannot be **kwargs\n"
            "PXC-001 requires exactly one positional parameter"
        )
    if param.kind == inspect.Parameter.KEYWORD_ONLY:
        raise TypeError(
            "Component parameter cannot be keyword-only\n"
            "PXC-001 requires a positional parameter"
        )

    # Check for default value
    if param.default != inspect.Parameter.empty:
        raise TypeError(
            "Component parameter must not have a default value\n"
            "PXC-001 requires a single required positional parameter"
        )

    # Layer 3: Type annotation verification
    try:
        hints = get_type_hints(function)
    except Exception as e:
        raise TypeError(f"Failed to extract type hints: {e}") from e

    if param.name not in hints:
        func_name = getattr(function, "__name__", "function")
        raise TypeError(
            f"Component parameter '{param.name}' must have a type annotation\n"
            f"Add type annotation: def {func_name}(params: YourInputModel) -> OutputModel"
        )

    if "return" not in hints:
        func_name = getattr(function, "__name__", "function")
        raise TypeError(
            f"Component function must have a return type annotation\n"
            f"Add return type: def {func_name}(params: InputModel) -> YourOutputModel"
        )

    param_type = hints[param.name]
    return_type = hints["return"]

    # Layer 4: Pydantic BaseModel verification
    def is_basemodel_type(type_hint: Any) -> bool:
        """Check if type hint is BaseModel or subclass."""
        try:
            if isinstance(type_hint, type) and issubclass(type_hint, BaseModel):
                return True
        except TypeError:
            pass
        return False

    if not is_basemodel_type(param_type):
        raise TypeError(
            f"Component parameter type must be a Pydantic BaseModel, got {param_type}\n"
            "Parameter type must inherit from pydantic.BaseModel"
        )

    if not is_basemodel_type(return_type):
        raise TypeError(
            f"Component return type must be a Pydantic BaseModel, got {return_type}\n"
            "Return type must inherit from pydantic.BaseModel"
        )

    # Layer 5: Protocol conformance (typeguard)
    try:
        check_type(function, ComponentFunction[BaseModel, BaseModel])
    except TypeError as e:
        raise TypeError(
            f"Function does not conform to ComponentFunction protocol: {e}"
        ) from e

    return cast(ComponentFunction[BaseModel, BaseModel], function)

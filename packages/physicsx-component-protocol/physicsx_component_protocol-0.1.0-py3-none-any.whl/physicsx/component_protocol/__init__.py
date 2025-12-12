"""PXC-001 Component Protocol.

This module implements the PXC-001 specification for PhysicsX pipeline components.
"""

from __future__ import annotations

from physicsx.component_protocol._protocol import (
    ComponentFunction,
    InputType,
    OutputType,
)
from physicsx.component_protocol._validation import validate_component_function

__all__ = [
    "ComponentFunction",
    "InputType",
    "OutputType",
    "validate_component_function",
]

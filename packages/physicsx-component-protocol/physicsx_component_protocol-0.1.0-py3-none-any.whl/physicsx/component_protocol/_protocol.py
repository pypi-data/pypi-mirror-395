"""PXC-001 Component Function Protocol definition.

This module defines the structural type required for PhysicsX pipeline components
using PEP 544 protocols and Pydantic models.
"""

from __future__ import annotations

from typing import Protocol, TypeVar

from pydantic import BaseModel

InputType = TypeVar("InputType", bound=BaseModel, contravariant=True)
OutputType = TypeVar("OutputType", bound=BaseModel, covariant=True)


class ComponentFunction(Protocol[InputType, OutputType]):
    """Python callable protocol for PhysicsX pipeline components.

    This protocol defines the structural type required for Python entry point
    functions using PEP 544 structural subtyping.

    The positional-only parameter marker (/) indicates that the parameter
    name is not part of the protocol specification. Implementations may
    use any parameter name.

    A compliant function must:
    - Accept a single positional argument of type InputType (Pydantic BaseModel)
    - Return a single Pydantic BaseModel output
    - Have no additional parameters, defaults, *args, or **kwargs
    """

    def __call__(self, _: InputType, /) -> OutputType:
        """Execute the component function.

        The function accepts a single positional argument of type InputType
        and returns an output of type OutputType. The parameter name is
        implementation-defined.

        Returns:
            Output result as a Pydantic BaseModel instance
        """
        ...

import inspect
from dataclasses import dataclass
from typing import Any, get_type_hints

from physicsx.component_protocol import ComponentFunction, validate_component_function
from pydantic import BaseModel


@dataclass(frozen=True)
class Component:
    """A validated PhysicsX component with resolved type information.

    Attributes:
        function: The validated component function.
        input_type: The Pydantic model type for the component's input.
        output_type: The Pydantic model type for the component's output.
    """

    function: ComponentFunction[BaseModel, BaseModel]
    input_type: type[BaseModel]
    output_type: type[BaseModel]


def resolve_component(obj: Any) -> Component:
    """Resolve and validate a component function with its input/output types.

    Args:
        obj: Any object that should be a valid component function.

    Returns:
        A Component with the validated function and resolved type hints.

    Raises:
        ValidationError: If the object is not a valid component function.
    """
    component_function = validate_component_function(obj)

    sig = inspect.signature(component_function)
    params = list(sig.parameters.values())
    param_name = params[0].name

    hints = get_type_hints(component_function)

    return Component(
        function=component_function,
        input_type=hints[param_name],
        output_type=hints["return"],
    )

import importlib.metadata


def resolve_entrypoint(component_name: str) -> importlib.metadata.EntryPoint:
    """Resolve a component entry point by name from the physicsx.components group.

    Args:
        component_name: Name of the component to resolve.

    Returns:
        The entry point for the component.

    Raises:
        LookupError: If the component is not found in the entry points group.
    """
    entry_points = importlib.metadata.entry_points(group="physicsx.components")
    for entry_point in entry_points:
        if entry_point.name == component_name:
            return entry_point

    available = [entry_point.name for entry_point in entry_points]
    raise LookupError(f"Component '{component_name}' not found. Available: {available}")

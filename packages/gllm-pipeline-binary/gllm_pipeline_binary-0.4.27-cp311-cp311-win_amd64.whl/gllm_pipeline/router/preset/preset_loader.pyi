from _typeshed import Incomplete
from typing import Any

PRESET_REGISTRY: Incomplete

def get_preset(router_type: str, modality: str, preset_name: str, **kwargs: Any) -> dict[str, Any]:
    '''Retrieve and execute a preset function based on router configuration.

    This function looks up a preset function from the `PRESET_REGISTRY` using the
    combination of router type, input modality, and preset name. If found, it executes
    the function with the given keyword arguments.

    Args:
        router_type (str): The type of router (e.g., "router").
        modality (str): The input modality (e.g., "image", "text").
        preset_name (str): The name of the preset (e.g., "domain_specific", "generic").
        **kwargs: Additional keyword arguments passed to the preset function.

    Returns:
        dict[str, Any]: A dictionary of router components (varies by router type).

    Raises:
        ValueError: If no matching preset is found in the registry.
    '''

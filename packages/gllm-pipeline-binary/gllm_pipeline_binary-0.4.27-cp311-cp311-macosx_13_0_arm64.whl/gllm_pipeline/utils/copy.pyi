from typing import Any

def safe_deepcopy(obj: Any) -> Any:
    """Deepcopy an object gracefully.

    Args:
        obj (Any): The object to copy.

    Returns:
        Any: The deep copied object, or the original object if deepcopy fails.
    """

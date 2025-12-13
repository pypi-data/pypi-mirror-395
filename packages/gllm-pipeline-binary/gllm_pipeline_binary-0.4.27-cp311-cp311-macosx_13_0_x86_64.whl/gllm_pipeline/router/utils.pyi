from typing import Any

def encode_bytes(value: Any, recursive: bool = False) -> Any:
    """Encode `bytes` objects into base64 strings for JSON serialization.

    This function converts `bytes` objects into UTF-8 base64-encoded strings. If
    `recursive` is enabled, it will traverse nested structures (lists and dictionaries)
    and encode all `bytes` instances found within them. Other data types remain
    unchanged.

    Behavior:
        1. If `value` is `bytes`, it is converted to a base64-encoded UTF-8 string.
        2. If `value` is a list or dict and `recursive` is True, encoding is applied
          to all nested elements.
        3. For unsupported types or when `recursive` is False, the original value is
          returned as-is.

    Args:
        value (Any): The value to process. Can be `bytes`, list, dict, or any other type.
        recursive (bool): If True, apply encoding recursively to all elements within
            lists and dictionaries. Defaults to False.

    Returns:
        Any: The base64-encoded string if `value` is `bytes`, a recursively processed
        structure if `recursive` is True, or the original value otherwise.
    """

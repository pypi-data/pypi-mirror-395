from gllm_pipeline.router.utils import encode_bytes as encode_bytes
from semantic_router.route import Route
from typing import Any

class BytesCompatRoute(Route):
    """A subclass of `Route` that provides JSON-serializable support for `bytes` in utterances.

    The primary motivation for this override is to prevent errors when `bytes`-based utterances are hashed
    during `semantic_router.routers.base.BaseRouter._write_hash`.

    `ByteCompatRoute` extends the standard `Route` class from the `semantic-router` library by ensuring that
    all `bytes` values in the `utterances` field are safely encoded using base64 when converting to a dictionary.
    This is essential for serializing routes containing binary data to formats like JSON, which does not
    support raw bytes.

    Use this class as a drop-in replacement when dealing with routes that include `bytes`-based utterances but still
    need to be serialized (e.g., for configuration exports or caching).
    """
    def to_dict(self) -> dict[str, Any]:
        '''Convert the route instance to a dictionary with all `bytes` in the `utterances`.

        This overrides the default `Route.to_dict()` to handle nested `bytes` inside lists or dictionaries.

        Returns:
            dict[str, Any]: A dictionary representation of the route, with all `bytes` values in `utterances`
            converted to base64-encoded UTF-8 strings.

        Example:
            >>> route = ByteCompatRoute(name="example", utterances=[b"binary1", "text"])
            >>> route.to_dict()
            {
                "name": "example",
                "utterances": ["YmluYXJ5MQ==", "text"],
                ...
            }

        Notes:
            - Only the `utterances` field is altered for byte safety; other fields remain untouched.
            - If the utterances contain nested lists or dicts with bytes, they will be recursively encoded.
        '''

import numpy as np
from gllm_datastore.vector_data_store.vector_data_store import BaseVectorDataStore as BaseVectorDataStore
from gllm_pipeline.router.aurelio_semantic_router.index.aurelio_index import BaseAurelioIndex as BaseAurelioIndex
from gllm_pipeline.router.utils import encode_bytes as encode_bytes
from semantic_router import Route
from typing import Any, Callable, TypeVar

ROUTE_PAYLOAD_KEY: str
UTTERANCE_PAYLOAD_KEY: str
T = TypeVar('T')

class VectorStoreAdapterIndex(BaseAurelioIndex):
    """A vector store-backed implementation of BaseAurelioIndex for use with AurelioSemanticRouter.

    This index performs similarity search over a backend vector store to retrieve relevant
    route payloads. The vector store must implement the BaseVectorDataStore interface and support
    async methods for querying by vector and filtering by metadata.
    """
    index: BaseVectorDataStore
    def __init__(self, index: BaseVectorDataStore, **kwargs: Any) -> None:
        """Initialize the VectorStoreAdapterIndex.

        Args:
            index (BaseVectorDataStore): The vector store instance used for retrieval.
            **kwargs: Additional keyword arguments forwarded to the BaseAurelioIndex.
        """
    def __len__(self) -> int:
        """Returns the total number of vectors in the index.

        If the index is not initialized returns 0.

        Returns:
            int: The total number of vectors.
        """
    def add(self, routes: list[str], utterances: list[str | bytes], **_):
        """Add route-utterance pairs into the vector store.

        Each utterance is associated with its route and encoded as a Chunk. Binary strings
        are automatically base64-encoded for safe storage.

        Args:
            routes (list[str]): List of route identifiers.
            utterances (list[str | bytes]): List of utterance strings or bytes.
            **_: Ignored. Included for interface compatibility.

        Raises:
            AssertionError: If `routes` and `utterances` have different lengths.
        """
    def get_routes(self) -> dict[str, list]:
        """Retrieve all routes and their corresponding utterances from the vector store.

        Returns:
            dict[str, list]: A dictionary where each key is a route and the value is a
            list of associated utterance strings.
        """
    def query(self, vector: np.ndarray, top_k: int = 5, route_filter: list[str] | None = None, retrieval_params: dict | None = None) -> tuple[np.ndarray, list[str]]:
        """Perform a similarity query using the provided vector, optionally filtering by route.

        Args:
            vector (np.ndarray): Query vector to search against stored vectors.
            top_k (int, optional): Maximum number of top matching results to return. Defaults to 5.
            route_filter (list[str] | None, optional): Optional list of route names to filter
                the search results by. If None, all routes are considered.
            retrieval_params (dict | None, optional): Filter parameters to narrow the search. Defaults to None.

        Returns:
            tuple[np.ndarray, list[str]]: A tuple containing:
                - A NumPy array of similarity scores.
                - A list of corresponding route names for each match.
        """
    def is_ready(self):
        """Checks if the index is ready to be used.

        This is a mandatory method to be implemented from `BaseIndex`.

        Returns:
            bool: True if the index has one or more vectors; False otherwise.
        """
    async def ais_ready(self) -> None:
        """Checks if the index is ready to be used in async.

        Returns:
            bool: True if the index has one or more vectors; False otherwise.
        """
    def load_routes_from_json(self, file_path: str, transform_utterance: Callable[[str], str | bytes] | None = None):
        """Load route-utterance pairs from a JSON file and insert them into the vector store.

        The JSON file must contain a dictionary mapping route names to lists of utterances.
        Each utterance can optionally be transformed before storage.

        Args:
            file_path (str): Path to a `.json` file containing routes and utterances.
            transform_utterance (Callable[[str], str | bytes] | None): Optional function to
                preprocess each utterance before storage. Must return `str` or `bytes`.

        Raises:
            ValueError: If the provided file is not a JSON file.
        """
    def load_routes_from_dict(self, routes: list[Route] | dict[str, list[str | bytes]], transform_utterance: Callable[[str], str | bytes] | None = None):
        """Load route-utterance pairs from a list of `Route` or a dictionary and insert into the vector store.

        This method supports two input formats:
            1. A list of `Route` objects from `semantic_router`, where each route has a `name` and `utterances`.
            2. A dictionary mapping route names (str) to lists of utterances (list[str]).

        Optionally, a `transform_utterance` function can be provided to process each utterance before storage.
        Utterances can be any type; use `transform_utterance` to ensure the final result is str or bytes.

        Args:
            routes (list[Route] | dict[str, list]): Route data in either list or dictionary format.
            transform_utterance (Callable[[str], str | bytes] | None): Optional function to transform
                each utterance before storage. Must return `str` or `bytes`.

        Raises:
            ValueError: If `routes` is not a list of `Route` objects or a dictionary,
                if route names are invalid,
                if utterances are not lists of non-empty strings,
                or if transformed utterances are not `str` or `bytes`.
        """

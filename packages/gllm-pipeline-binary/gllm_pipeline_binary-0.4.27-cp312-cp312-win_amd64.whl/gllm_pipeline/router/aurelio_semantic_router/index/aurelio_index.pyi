import abc
import numpy as np
from abc import ABC, abstractmethod
from semantic_router.index import BaseIndex
from typing import Any

class BaseAurelioIndex(BaseIndex, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the router index to be loaded by the AurelioSemanticRouter.

    The `BaseAurelioIndex` extends the `BaseIndex` class from the semantic router library.
    It can be used as a base class for a router index implementation that can be used with the assumption that
    the routes are already in the index. Therefore, the index will solely be used for retrieval purposes.

    Attributes:
        sync (bool): Flag to indicate that the index should be synchronized with the routes mapping.
            In this implementation, it's set to `True` by default to make sure that the RouteLayer object initialized
            with this index will perform the syncing process instead of blindly adding the routes to the index.

    Notes:
        To use this class, you need to implement the `get_routes` and `query` methods:
        1. `get_routes`: Retrieve a list of routes and their associated utterances from the index.
        2. `query`: Search the index for the query_vector and return top_k results.
    """
    sync: bool
    @abstractmethod
    def get_routes(self) -> dict[str, list[str]]:
        """Retrieves a dictionary of routes and their associated utterances from the index.

        Returns:
            dict[str, list[str]]: A dictionary where the key is the route name and the value is a list of utterances.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
    @abstractmethod
    def query(self, vector: np.ndarray, top_k: int = 5, route_filter: list[str] | None = None) -> tuple[np.ndarray, list[str]]:
        """Search the index with the input query vector and return top_k results.

        Args:
            vector (np.ndarray): The input vector to query.
            top_k (int, optional): The number of results to return. Defaults to 5.
            route_filter (list[str] | None, optional): The list of routes to filter the results by. Defaults to None.

        Returns:
            tuple[np.ndarray, list[str]]: A tuple containing the query vector and the list of results.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
    def add(self, embeddings: list[list[float]], routes: list[str], utterances: list[Any], function_schemas: list[dict[str, Any]] | None = None, metadata_list: list[dict[str, Any]] | None = None) -> None:
        """Add embeddings to the index.

        This method doesn't need to add any routes to the index since it's assumed that the routes are already in
        the index. Therefore, this method is left empty intentionally.

        Args:
            embeddings (list[list[float]]): A list of embedded vectors for the documents.
            routes (list[str]): A list of route names for the documents.
            utterances (list[Any]): A list of utterances for the documents.
            function_schemas (list[dict[str, Any]]): List of function schemas to add to the index.
            metadata_list (list[dict[str, Any]]): List of metadata to add to the index.

        Returns:
            None
        """

import numpy as np
from azure.search.documents import SearchClient
from gllm_pipeline.router.aurelio_semantic_router.index.aurelio_index import BaseAurelioIndex as BaseAurelioIndex

class AzureAISearchAurelioIndexConstants:
    """Defines Azure AI Search Aurelio index related constants."""
    CONTENT_FIELD: str
    SCORE_FIELD: str
    VECTOR_FIELD: str
    VECTOR_SEARCH_TYPE: str

class AzureAISearchAurelioIndexDefaults:
    """Defines default values for the AzureAISearchAurelioIndex class."""
    ROUTE_FIELD_NAME: str
    MAX_TOP_K: int
    MAX_SEARCH_ITERATIONS: int

class AzureAISearchAurelioIndex(BaseAurelioIndex):
    """A router index implementation for Azure AI Search to be used by the AurelioSemanticRouter.

    The `AzureAISearchAurelioIndex` class extends the `BaseAurelioIndex` class. It allows an Azure AI Search index to be
    used as a router index by the `AurelioSemanticRouter` class. Just like the `BaseAurelioIndex` class, this class also
    assumes that the routes are already in the index. Therefore, the index will solely be used for retrieval purposes.

    Attributes:
        client (SearchClient | None): The client to interact with the Azure AI Search index.
        route_field_name (str): The name of the field that contains the route name.
        max_top_k (int): The maximum number of results to return.
        max_search_iterations (int): The maximum number of search iterations to perform.
        sync (bool): Flag to indicate that the index should be synchronized with the routes mapping.
            In this implementation, it's set to `True` by default to make sure that the RouteLayer object initialized
            with this index will perform the syncing process instead of blindly adding the routes to the index.
    """
    client: SearchClient | None
    route_field_name: str
    max_top_k: int
    max_search_iterations: int
    def __init__(self, endpoint: str, index_name: str, api_key: str, route_field_name: str = ..., max_top_k: int = ..., max_search_iterations: int = ...) -> None:
        """Initialize the AzureAISearchIndex with the given service endpoint, index name, and API key.

        Args:
            endpoint (str): The endpoint of the Azure AI Search service.
            index_name (str): The name of the Azure AI Search index.
            api_key (str): The API key for the Azure AI Search service.
            route_field_name (str, optional): The name of the field that contains the route name.
                Defaults to AzureAISearchAurelioIndexDefaults.ROUTE_FIELD_NAME.
            max_top_k (int, optional): The maximum number of results to return.
                Defaults to AzureAISearchAurelioIndexDefaults.MAX_TOP_K.
            max_search_iterations (int, optional): The maximum number of search iterations to perform.
                Defaults to AzureAISearchAurelioIndexDefaults.MAX_SEARCH_ITERATIONS.

        Returns:
            None
        """
    def get_routes(self) -> dict[str, list[str]]:
        """Retrieves a dictionary of routes and their associated utterances from the Azure AI Search index.

        Returns:
            dict[str, list[str]]: A dictionary where the key is the route name and the value is a list of utterances.
        """
    def query(self, vector: np.ndarray, top_k: int = 5, route_filter: list[str] | None = None) -> tuple[np.ndarray, list[str]]:
        """Search the Azure AI Search index with the input query vector and return top_k results.

        Args:
            vector (np.ndarray): The input vector to query.
            top_k (int, optional): The number of results to return. Defaults to 5.
            route_filter (list[str] | None, optional): The list of routes to filter the results by. Defaults to None.

        Returns:
            tuple[np.ndarray, list[str]]: A tuple containing the query vector and the list of results.
        """

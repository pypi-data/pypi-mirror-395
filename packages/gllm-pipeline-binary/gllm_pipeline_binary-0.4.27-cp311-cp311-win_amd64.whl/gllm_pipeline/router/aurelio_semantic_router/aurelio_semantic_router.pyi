from _typeshed import Incomplete
from gllm_pipeline.router.aurelio_semantic_router.bytes_compat_route import BytesCompatRoute as BytesCompatRoute
from gllm_pipeline.router.aurelio_semantic_router.index.aurelio_index import BaseAurelioIndex as BaseAurelioIndex
from gllm_pipeline.router.preset.preset_loader import get_preset as get_preset
from gllm_pipeline.router.router import BaseRouter as BaseRouter
from semantic_router import Route
from semantic_router.encoders.base import DenseEncoder as DenseEncoder
from typing import Any

manager: Incomplete
logger: Incomplete
semantic_router_logger: Incomplete

class AurelioSemanticRouter(BaseRouter):
    """A router that utilizes the Aurelio Labs library to route the input source to the appropriate path.

    The `AurelioSemanticRouter` utilizes the Aurelio Labs library to route a given input source to an appropriate path
    based on the similarity with existing samples. If the determined route is not valid, it defaults to a predefined
    route.

    Attributes:
        route_layer (RouteLayer): The Aurelio Labs route layer that handles the routing logic.
        default_route (str): The default route to be used if the input source is not similar to any of the routes.
        valid_routes (set[str]): A set of valid routes for the router.

    Notes:
        For more information about the Aurelio Labs library, please refer to
        https://github.com/aurelio-labs/semantic-router
    """
    route_layer: Incomplete
    def __init__(self, default_route: str, valid_routes: set[str], encoder: DenseEncoder, routes: list[Route] | dict[str, list[str | bytes]] | None = None, index: BaseAurelioIndex | None = None, auto_sync: str = ..., **kwargs: Any) -> None:
        '''Initializes a new instance of the AurelioSemanticRouter class.

        To define the routes, at least one of the `routes` or `index` parameters must be provided.
        When both parameters are provided, the `routes` parameter is ignored.

        Args:
            default_route (str): The default route to be used if the input source is not similar to any of the routes.
            valid_routes (set[str]): A set of valid routes for the router.
            encoder (DenseEncoder): An Aurelio Labs dense encoder to encode the input source and the samples.
                The encoded vectors are used to calculate the similarity between the input source and the samples.
            routes (list[Route] | dict[str, list[str | bytes]] | None, optional): A list of Aurelio Labs Routes
                or a dictionary mapping route names to the list of samples. Ignored if `index` is provided.
                Defaults to None.
            index (BaseAurelioIndex | None, optional): A router index to retrieve the routes.
                If provided, it is prioritized over `routes`. Defaults to None.
            auto_sync (str, optional): The auto-sync mode for the router. Defaults to "local".
            kwargs (Any): Additional keyword arguments to be passed to the Aurelio Labs Route Layer.

        Raises:
            ValueError:
                1. If neither `routes` nor `index` is provided.
                2. If the parsed routes contains routes that are not in the set of valid routes.
                3. If the provided default route is not in the set of valid routes.
        '''
    @classmethod
    def from_preset(cls, modality: str, preset_name: str, preset_kwargs: dict | None = None, **kwargs) -> AurelioSemanticRouter:
        """Initialize the Aurelio semantic based router component using preset model configurations.

        Args:
            modality (str): type of modality input.
            preset_name (str): Name of the preset to use.
            preset_kwargs (dict | None): placeholder for preset additional arguments.
            **kwargs (Any): Additional arguments to pass for this class.

        Returns:
            AurelioSemanticRouter: Initialized aurelio semantic based router component using preset model.
        """
    @classmethod
    def from_file(cls, default_route: str, valid_routes: set[str], file_path: str) -> AurelioSemanticRouter:
        '''Creates a new instance of the AurelioSemanticRouter class from a file.

        This method creates a new instance of the AurelioSemanticRouter class from a file. It supports JSON and YAML
        file extensions.

        Args:
            default_route (str): The default route to be used if the input source is not similar to any of the routes.
            valid_routes (set[str]): A set of valid routes for the router.
            file_path (str): The path to the file containing the routes. The file extension must be either JSON or YAML.

        Returns:
            AurelioSemanticRouter: A new instance of the AurelioSemanticRouter class.

        Raises:
            ValueError: If the file extension is not ".json" or ".yaml".
        '''

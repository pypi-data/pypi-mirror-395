import abc
from _typeshed import Incomplete
from abc import ABC
from gllm_core.schema import Component

class BaseRouter(Component, ABC, metaclass=abc.ABCMeta):
    """An abstract base class for the routers used in Gen AI applications.

    This class provides a foundation for building routers in Gen AI applications. It includes initialization for
    default and valid routes and abstract routing logic that subclasses must implement.

    Attributes:
        default_route (str): The default route to use.
        valid_routes (set[str]): A set of valid routes for the router.
    """
    default_route: Incomplete
    valid_routes: Incomplete
    logger: Incomplete
    def __init__(self, default_route: str, valid_routes: set[str]) -> None:
        """Initializes a new instance of the BaseRouter class.

        Args:
            default_route (str): The default route to use.
            valid_routes (set[str]): A set of valid routes for the router.

        Raises:
            ValueError: If the provided default route is not in the set of valid routes.
        """
    async def route(self, source: str | bytes, route_filter: set[str] | None = None) -> str:
        """Routes an input source to the appropriate path.

        This method is a wrapper around the `_select_route` method. It first calls `_select_route` to get the selected
        route and then checks if the route is in the set of valid routes. If it is not, it returns the default route.

        Args:
            source (str | bytes): The input source to be routed.
            route_filter (set[str] | None, optional): An optional set of allowed routes. If provided, only the routes
                in the set are considered valid. Defaults to None.

        Returns:
            str: The selected route for the input source.

        Raises:
            ValueError: If the provided route filter contains invalid routes or if the default route is not included
                in the route filter.
        """

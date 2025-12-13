from _typeshed import Incomplete
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor, UsesLM
from gllm_pipeline.router.preset.preset_loader import get_preset as get_preset
from gllm_pipeline.router.router import BaseRouter as BaseRouter

DEFAULT_LM_OUTPUT_KEY: str

class LMBasedRouter(BaseRouter, UsesLM):
    '''A router that utilizes a language model to determine the appropriate route for an input source.

    This class routes a given input source to an appropriate path based on the output of a language model.
    If the determined route is not valid, it defaults to a predefined route.

    Attributes:
        lm_request_processor (LMRequestProcessor): The request processor that handles requests to the language model.
        default_route (str): The default route to be used if the language model\'s output is invalid.
        valid_routes (set[str]): A set of valid routes for the router.
        lm_output_key (str, optional): The key in the language model\'s output that contains the route.

    Notes:
        The `lm_request_processor` must be configured to:
        1. Take a "source" key as input. The input source of the router should be passed as the value of
            this "source" key.
        2. Return a JSON object which contains the selected route as a string. The key of the route is specified by the
        `lm_output_key` attribute. Furthermore, the selected route must be present in the `valid_routes` set.

        Output example, assuming the `lm_output_key` is "route":
        {
            "route": "<route_string>"
        }
    '''
    lm_request_processor: Incomplete
    lm_output_key: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor, default_route: str, valid_routes: set[str], lm_output_key: str = ...) -> None:
        """Initializes a new instance of the LMBasedRouter class.

        Args:
            lm_request_processor (LMRequestProcessor): The request processor that handles requests to the
                language model.
            default_route (str): The default route to be used if the language model's output is invalid.
            valid_routes (set[str]): A set of valid routes for the router.
            lm_output_key (str): The key in the language model's output that contains the route.
                Defaults to DEFAULT_LM_OUTPUT_KEY.

        Raises:
            ValueError: If the provided default route is not in the set of valid routes.
        """
    @classmethod
    def from_preset(cls, modality: str, preset_name: str, preset_kwargs: dict | None = None, **kwargs) -> LMBasedRouter:
        """Initialize the LM based router component using preset model configurations.

        Args:
            modality (str): type of modality input.
            preset_name (str): Name of the preset to use.
            preset_kwargs (dict | None): placeholder for preset additional arguments.
            **kwargs (Any): Additional arguments to pass for this class.

        Returns:
            LMBasedRouter: Initialized lm based router component using preset model.
        """

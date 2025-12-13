from _typeshed import Incomplete
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from gllm_pipeline.router.router import BaseRouter as BaseRouter

class SimilarityBasedRouter(BaseRouter):
    """A router that utilizes an embedding model to determine the appropriate route for an input text.

    This class routes a given input text to an appropriate path based on semantic similarity between
    the input text and predefined route examples. It calculates cosine similarity between the input
    text embedding and the embeddings of route examples, then selects the route with the highest
    similarity score above a threshold.

    Attributes:
        em_invoker (BaseEMInvoker): The embedding model invoker to use for vectorization.
        route_examples (dict[str, list[str]]): A mapping of route names to their example texts.
        similarity_threshold (float): The minimum similarity score required for a route to be selected.
        default_route (str): The default route to be used if no route meets the similarity threshold.
        valid_routes (set[str]): A set of valid routes for the router.
    """
    em_invoker: Incomplete
    route_examples: Incomplete
    similarity_threshold: Incomplete
    def __init__(self, em_invoker: BaseEMInvoker, route_examples: dict[str, list[str]], default_route: str, similarity_threshold: float = 0.5) -> None:
        '''Initializes a new instance of the SimilarityBasedRouter class.

        Args:
        em_invoker (BaseEMInvoker): The embedding model invoker to use for vectorization.
        route_examples (dict[str, list[str]]): A mapping of route names to their example texts.
            The keys define the valid routes, and values are example texts for each route.
        default_route (str): The default route to be used if no route meets the similarity threshold.
            Must be one of the keys in route_examples.
            Examples: "general", "fallback", "customer_service"
        similarity_threshold (float, optional): The minimum similarity score required for a route to be selected.
            Must be between 0 and 1. This threshold is compared against normalized cosine similarity scores,
            which are derived from the standard cosine similarity (ranging from -1 to 1) and converted to
            a 0-1 range where 0 indicates maximum dissimilarity and 1 indicates maximum similarity.
        Examples of route_examples:
                {
                    "tech_support": [
                        "I can\'t log in to my account",
                        "The app keeps crashing",
                        "Password reset not working",
                        "Getting error code 500"
                    ],
                    "billing": [
                        "How much do I owe?",
                        "I want to dispute a charge",
                        "When is my payment due?",
                        "Can I get a refund?"
                    ],
                    "general": [
                        "What are your business hours?",
                        "How do I contact support?",
                        "Tell me about your services",
                        "Where are you located?"
                    ]
                }

        Raises:
            ValueError:
                1. If route_examples is not a dictionary.
                2. If route_examples is falsy (None, empty dict, etc.).
                3. If the similarity threshold is not between 0 and 1.
                4. If the provided default route is not in the route_examples keys.
                5. If any route has an empty list of examples.
        '''
    def clear_cache(self) -> None:
        """Clears the cached route embeddings.

        This method clears the cached embeddings, forcing them to be regenerated
        on the next routing operation.
        """

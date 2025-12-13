from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from semantic_router.encoders.base import DenseEncoder
from typing import Any

class EMInvokerEncoder(DenseEncoder):
    """The gllm-inference EM Invoker-compatible Encoder.

    This encoder is for use with gllm-inference's EM Invokers.
    Includes handling of synchronous cases, since gllm-inference's EM Invokers are asynchronous.

    Attributes:
        name (str): The name of the encoder.
        score_threshold (float): The score threshold for the encoder.
    """
    def __init__(self, em_invoker: BaseEMInvoker, name: str = 'em-invoker-encoder', score_threshold: float = 0.0) -> None:
        '''Initialize the EM Invoker Encoder.

        Args:
            em_invoker (BaseEMInvoker): The EM Invoker to use.
            name (str, optional): The name of the encoder. Defaults to "em-invoker-encoder".
            score_threshold (float, optional): The score threshold for the encoder. Defaults to 0.0.
        '''
    def __call__(self, docs: list[Any]) -> list[list[float]]:
        """Call the EM Invoker.

        Handles both async and sync contexts by checking for existing event loop.
        If an event loop is not found, we run the invoke method in the current thread.
        If an event loop is found, we run the invoke method in a thread pool.
        In the case of a RuntimeError, we run the invoke method in the current thread.

        Args:
            docs (list[Any]): List of documents to be embedded.

        Returns:
            list[list[float]]: List of embeddings for each document.
        """
    async def acall(self, docs: list[Any], **kwargs: Any) -> list[list[float]]:
        """Call the EM Invoker, which is already an async function.

        Args:
            docs (list[Any]): List of documents to be embedded.
            **kwargs (Any): Additional keyword arguments. Not used, but required by the DenseEncoder interface.

        Returns:
            list[list[float]]: List of embeddings for each document.
        """

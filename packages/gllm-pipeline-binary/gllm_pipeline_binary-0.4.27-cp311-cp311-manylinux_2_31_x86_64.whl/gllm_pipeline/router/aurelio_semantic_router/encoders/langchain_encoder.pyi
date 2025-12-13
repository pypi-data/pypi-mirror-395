from langchain_core.embeddings import Embeddings as Embeddings
from semantic_router.encoders.base import DenseEncoder
from typing import Any

class LangchainEmbeddingsEncoder(DenseEncoder):
    """A wrapper encoder for LangChain-compatible embedding models.

    This encoder adapts any LangChain-compatible Embeddings instance to the
    Semantic Router interface by wrapping its `embed_documents` and `aembed_documents` methods.

    It supports both synchronous and asynchronous embedding calls and is useful
    when integrating LangChain embeddings with a semantic router pipeline.

    Attributes:
        name (str): The name of the encoder.
        score_threshold (float): Threshold for similarity scoring.
    """
    def __init__(self, embeddings: Embeddings, name: str = 'langchain-embeddings-encoder', score_threshold: float = 0.5) -> None:
        '''Initialize the LangchainEmbeddingsEncoder.

        Args:
            embeddings (Embeddings): A LangChain-compatible Embeddings instance.
            name (str, optional): Identifier for the encoder. Defaults to "langchain-embeddings-encoder".
            score_threshold (float, optional): Minimum similarity score to consider matches. Defaults to 0.5.
        '''
    def __call__(self, docs: list[Any]) -> list[list[float]]:
        """Synchronously embed a list of documents.

        Automatically handles execution context:
        1. If called inside an active asyncio loop, it runs the embedding call in a background thread.
        2. If no active loop is present, it runs the embedding call normally.
        3. If an event loop cannot be retrieved, falls back to `asyncio.run`.

        Args:
            docs (list[Any]): The documents to embed.

        Returns:
            list[list[float]]: A list of vector embeddings for each document.
        """
    async def acall(self, docs: list[Any]) -> list[list[float]]:
        """Asynchronously embed a list of documents.

        Calls the `aembed_documents` method of the underlying LangChain embeddings.

        Args:
            docs (list[Any]): The documents to embed.

        Returns:
            list[list[float]]: A list of vector embeddings for each document.
        """

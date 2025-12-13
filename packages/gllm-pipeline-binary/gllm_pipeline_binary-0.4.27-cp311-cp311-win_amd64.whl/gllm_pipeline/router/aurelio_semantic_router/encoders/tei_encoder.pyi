from semantic_router.encoders.huggingface import HFEndpointEncoder
from typing import Any

class TEIEncoder(HFEndpointEncoder):
    """TEI Endpoint Encoder.

    This encoder is used to encode documents into embeddings using the TEI endpoint.

    Attributes:
        name (str): The name of the encoder.
        huggingface_url (str): The base URL of the TEI endpoint, which is a HuggingFace endpoint.
        huggingface_api_key (str): The API key for the TEI endpoint.
        score_threshold (float): The score threshold for the encoder.
    """
    def __init__(self, base_url: str, name: str = 'tei-encoder', api_key: str = '<empty>', score_threshold: float = 0.0) -> None:
        '''Initialize the TEI Endpoint Encoder.

        Args:
            base_url (str): The base URL of the TEI endpoint, which is a HuggingFace endpoint.
            name (str, optional): The name of the encoder. Defaults to "tei-encoder".
            api_key (str, optional): The API key for the TEI endpoint. Defaults to "<empty>".
                Only do this if the endpoint does not require an API key.
            score_threshold (float, optional): The score threshold for the encoder. Defaults to 0.0.
        '''
    async def acall(self, docs: list[str], **kwargs: Any) -> list[list[float]]:
        """Asynchronously encodes a list of documents into embeddings.

        Args:
            docs (list[str]): A list of documents to encode.
            **kwargs (Any): Additional keyword arguments. Not used, but required by the BaseEncoder interface.

        Returns:
            list[list[float]]: A list of embeddings for the given documents.

        Raises:
            ValueError: If no embeddings are returned for a document.
        """
    def __call__(self, docs: list[str]) -> list[list[float]]:
        """Encodes a list of documents into embeddings using the Hugging Face API.

        Args:
            docs (list[str]): A list of documents to encode.

        Returns:
            list[list[float]]: A list of embeddings for the given documents.

        Raises:
            ValueError: If no embeddings are returned for a document.
        """

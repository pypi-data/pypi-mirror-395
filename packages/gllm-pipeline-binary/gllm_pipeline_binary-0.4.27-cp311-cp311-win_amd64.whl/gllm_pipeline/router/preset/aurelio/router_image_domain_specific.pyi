from _typeshed import Incomplete

ROUTES: Incomplete

def get_router_image_domain_specific(**_: dict) -> dict:
    '''Builds a domain-specific router preset for image-based input using CLIP embeddings.

    This preset is designed to classify images into domain-specific categories, such as
    engineering diagrams, healthcare scans, financial statements, etc. Each route is defined
    using representative natural language utterances (captions), which are embedded using
    OpenAI\'s CLIP model (ViT-B/32). These embeddings are indexed using a LocalIndex for fast
    similarity-based routing.

    Returns:
        dict: A dictionary containing:
            1. "default_route" (str): The fallback route if no strong match is found.
            2. "valid_routes" (set): Set of all valid route names.
            3. "encoder" (DenseEncoder): The CLIP encoder used to embed utterances and queries.
            4. "index" (BaseIndex): The index containing all route utterance embeddings.
            5. "auto_sync" (str): Value used for auto-sync mode ("local").
    '''

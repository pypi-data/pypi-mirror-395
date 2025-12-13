from gllm_pipeline.alias import PipelineState as PipelineState
from typing import Any

def shallow_dump(state: PipelineState) -> dict[str, Any]:
    """Convert Pydantic model to dict while preserving nested Pydantic objects.

    Args:
        state (PipelineState): The state to convert.

    Returns:
        dict[str, Any]: The state as a dictionary with preserved nested Pydantic objects.
    """

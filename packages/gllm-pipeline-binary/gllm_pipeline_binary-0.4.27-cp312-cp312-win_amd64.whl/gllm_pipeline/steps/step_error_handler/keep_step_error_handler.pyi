from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.utils.error_handling import ErrorContext as ErrorContext
from langgraph.runtime import Runtime as Runtime
from pydantic import BaseModel as BaseModel

class KeepStepErrorHandler(BaseStepErrorHandler):
    """Strategy that preserves the current state on error."""
    def __init__(self) -> None:
        """Initialize the keep error handler."""

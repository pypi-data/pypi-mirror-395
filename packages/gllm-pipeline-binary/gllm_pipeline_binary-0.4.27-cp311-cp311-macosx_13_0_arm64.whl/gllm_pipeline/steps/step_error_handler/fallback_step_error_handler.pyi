from _typeshed import Incomplete
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.utils.error_handling import ErrorContext as ErrorContext
from langgraph.runtime import Runtime as Runtime
from pydantic import BaseModel as BaseModel
from typing import Any, Callable

class FallbackStepErrorHandler(BaseStepErrorHandler):
    """Strategy that executes a fallback callable on error.

    Attributes:
        fallback (Callable[[Exception, dict[str, Any], Runtime[dict[str, Any] | BaseModel], ErrorContext], Any]):
            A callable that generates the fallback state dynamically.
            It should accept (error, state, runtime, context) and return a fallback state.
    """
    fallback: Incomplete
    def __init__(self, fallback: Callable[[Exception, dict[str, Any], Runtime[dict[str, Any] | BaseModel], ErrorContext], Any]) -> None:
        """Initialize the strategy with a fallback callable.

        Args:
            fallback (Callable[[Exception, dict[str, Any], Runtime[dict[str, Any] | BaseModel], ErrorContext], Any]):
                A callable that generates the fallback state dynamically.
                It should accept (error, state, runtime, context) and return a fallback state.
        """

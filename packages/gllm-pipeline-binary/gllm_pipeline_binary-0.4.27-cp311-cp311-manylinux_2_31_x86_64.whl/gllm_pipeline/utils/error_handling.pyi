from _typeshed import Incomplete
from gllm_pipeline.alias import PipelineState as PipelineState
from pydantic import BaseModel
from typing import Any

class ErrorContext(BaseModel):
    '''Standardized error context for pipeline steps.

    This model provides a structured way to represent error context information
    for pipeline steps, ensuring consistency in error messages across the pipeline.

    Attributes:
        exception (BaseException): The exception that was raised.
        step_name (str): The name of the pipeline step where the error occurred.
        step_type (str): The type of pipeline step where the error occurred.
        state (PipelineState | None): The pipeline state at the time of the error.
            Defaults to None.
        operation (str): Description of the operation being performed when the error occurred.
            Defaults to "execution".
        additional_context (str | None): Additional context to include in the error message.
            Defaults to None.
    '''
    model_config: Incomplete
    exception: BaseException
    step_name: str
    step_type: str
    state: PipelineState | None
    operation: str
    additional_context: str | None

class ValidationError(Exception):
    """Exception raised for errors in state validation.

    This exception is raised when input validation fails in pipeline steps.
    It provides more specific error information than a generic RuntimeError.

    Attributes:
        message (str): The error message explaining the validation failure.
    """
    message: Incomplete
    def __init__(self, message: str) -> None:
        """Initialize with an error message.

        Args:
            message (str): The error message explaining what validation failed.
        """

def create_error_context(exception: Exception, step_name: str, step_type: str, state: dict[str, Any], operation: str, **kwargs) -> ErrorContext:
    """Create standardized error context for composite steps.

    Args:
        exception (Exception): The exception that occurred.
        step_name (str): Name of the step.
        step_type (str): Type of the step.
        state (dict[str, Any]): Pipeline state at time of error.
        operation (str): Operation being performed.
        **kwargs (dict[str, Any]): Additional context key-value pairs.

    Returns:
        ErrorContext: ErrorContext object with standardized information.
    """

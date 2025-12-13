from _typeshed import Incomplete
from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec, PipelineState as PipelineState
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.utils.async_utils import execute_callable as execute_callable
from gllm_pipeline.utils.error_handling import ErrorContext as ErrorContext
from gllm_pipeline.utils.has_inputs_mixin import HasInputsMixin as HasInputsMixin
from gllm_pipeline.utils.input_map import shallow_dump as shallow_dump
from langchain_core.runnables import RunnableConfig as RunnableConfig
from langgraph.runtime import Runtime
from pydantic import BaseModel as BaseModel
from typing import Any, Callable

class StateOperatorStep(BasePipelineStep, HasInputsMixin):
    """A pipeline step that performs an operation on the pipeline state and updates it.

    This step executes a given operation using selected data from the current pipeline state and runtime configuration,
    then updates the state with the operation's result.

    Attributes:
        name (str): A unique identifier for this pipeline step.
        input_map (dict[str, str | Val] | None): Unified input map.
        output_state (str | list[str]): Key(s) to store the operation result in the pipeline state.
        operation (Callable[[dict[str, Any]], Any]): The operation to execute.
            Accepts a dictionary of input data, which consists of the extracted state and runtime configuration.
        retry_policy (RetryPolicy | None): Configuration for retry behavior using LangGraph's RetryPolicy.
    """
    output_state: Incomplete
    operation: Incomplete
    def __init__(self, name: str, input_states: list[str] | None = None, output_state: str | list[str] | None = None, operation: Callable[[dict[str, Any]], Any] | None = None, runtime_config_map: dict[str, str] | None = None, fixed_args: dict[str, Any] | None = None, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        '''Initializes a new StateOperatorStep.

        Args:
            name (str): A unique identifier for this pipeline step.
            input_states (list[str]): Keys of the state data required by the operation.
            output_state (str | list[str]): Key(s) to store the operation result in the pipeline state.
            operation (Callable[[dict[str, Any]], Any]): The operation to execute.
                It should accept a dictionary of input data and return the operation result.
            runtime_config_map (dict[str, str] | None, optional): Mapping of operation input arguments to
                runtime configuration keys. Defaults to None.
            fixed_args (dict[str, Any] | None, optional): Fixed arguments to be passed to the operation.
                Defaults to None.
            input_map (InputMapSpec | None, optional):
                Unified input map. Can be a dict (arg -> str|Val) or a list with elements:
                1. str for identity mapping
                2. dict[str, str] for state/config mapping
                3. dict[str, Val] for fixed args.
                Defaults to None.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using
                GLLM Core\'s RetryConfig. Defaults to None, in which case no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Strategy to handle errors during execution.
                Defaults to None, in which case the RaiseStepErrorHandler is used.
            cache_store ("BaseCache" | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.
        '''
    async def execute(self, state: PipelineState, runtime: Runtime[dict[str, Any] | BaseModel], config: RunnableConfig | None = None) -> dict[str, Any]:
        """Executes the operation and processes its output.

        This method validates inputs, prepares data, executes the operation, and formats the output for integration
        into the pipeline state.

        Args:
            state (PipelineState): The current state of the pipeline, containing all data.
            runtime (Runtime[dict[str, Any] | BaseModel]): Runtime information for this step's execution.
            config (RunnableConfig | None, optional): The runnable configuration. Defaults to None.

        Returns:
            dict[str, Any]: The update to the pipeline state after this step's operation.
                This includes new or modified data produced by the operation, not the entire state.

        Raises:
            RuntimeError: If an error occurs during operation execution.
        """

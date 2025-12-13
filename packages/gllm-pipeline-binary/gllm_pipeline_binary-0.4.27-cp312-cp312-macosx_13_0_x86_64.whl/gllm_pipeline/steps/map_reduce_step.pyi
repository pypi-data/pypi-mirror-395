from _typeshed import Incomplete
from gllm_core.schema import Component
from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.utils.async_utils import execute_callable as execute_callable
from gllm_pipeline.utils.error_handling import ErrorContext as ErrorContext
from gllm_pipeline.utils.has_inputs_mixin import HasInputsMixin as HasInputsMixin
from gllm_pipeline.utils.input_map import shallow_dump as shallow_dump
from langchain_core.runnables import RunnableConfig as RunnableConfig
from langgraph.runtime import Runtime as Runtime
from pydantic import BaseModel as BaseModel
from typing import Any, Callable

class MapReduceStep(BasePipelineStep, HasInputsMixin):
    """A step that applies a mapping function to multiple inputs and reduces the results.

    This step performs parallel processing of multiple input items using:
    1. A map function that processes each input item independently. The map function receives a dictionary
        containing the input values for the current item (derived from input_state_map, runtime_config_map,
        and fixed_args).
    2. A reduce function that combines all the mapped results.

    Note on parallel execution:
    1. For true parallelism, the map_func MUST be an async function or a Component.
    2. Synchronous map functions will block the event loop and run sequentially.

    Input handling:
    1. Automatically detects which inputs are lists/sequences.
    2. Ensures all list inputs have the same length.
    3. Broadcasts scalar values to match list lengths.
    4. If no list inputs, applies the map function once to the whole input.

    Internally, this step uses asyncio.gather() for efficient parallel execution.

    Attributes:
        name (str): A unique identifier for this step.
        map_func (Component | Callable[[dict[str, Any]], Any]): Function to apply to each input item.
            Will be run in parallel if the function is an asynchronous function.
        reduce_func (Callable[[list[Any]], Any]): Function to reduce the mapped results.
        input_map (dict[str, str | Any] | None): Unified input map.
        output_state (str): Key to store the reduced result in the pipeline state.
        retry_policy (RetryPolicy | None): Configuration for retry behavior using LangGraph's RetryPolicy.
    """
    map_func: Incomplete
    reduce_func: Incomplete
    output_state: Incomplete
    def __init__(self, name: str, output_state: str, map_func: Component | Callable[[dict[str, Any]], Any], reduce_func: Callable[[list[Any]], Any] = ..., input_state_map: dict[str, str] | None = None, runtime_config_map: dict[str, str] | None = None, fixed_args: dict[str, Any] | None = None, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        '''Initialize a new MapReduceStep.

        Args:
            name (str): A unique identifier for this step.
            output_state (str): Key to store the reduced result in the pipeline state.
            map_func (Component | Callable[[dict[str, Any]], Any]): Function to apply to each input item.
                The map function receives a dictionary containing the input values derived from input_state_map,
                runtime_config_map, and fixed_args.
            reduce_func (Callable[[list[Any]], Any], optional): Function to reduce the mapped results.
                Defaults to a function that returns the list of results as is.
            input_state_map (dict[str, str] | None, optional): Mapping of function arguments to pipeline state keys.
                Defaults to None.
            runtime_config_map (dict[str, str] | None, optional): Mapping of arguments to runtime config keys.
                Defaults to None.
            fixed_args (dict[str, Any] | None, optional): Fixed arguments to pass to the functions. Defaults to None.
            input_map (InputMapSpec | None, optional):
                Unified input map. Can be a dict (arg -> str|Val) or a list with elements:
                1. str for identity mapping
                2. dict[str, str] for state/config mapping
                3. dict[str, Val] for fixed args.
                If provided, it will be used directly instead of synthesizing from maps. Defaults to None.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using
                GLLM Core\'s RetryConfig. Defaults to None, in which case no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Strategy to handle errors during execution.
                Defaults to None, in which case the RaiseStepErrorHandler is used.
            cache_store ("BaseCache" | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.
        '''
    async def execute(self, state: dict[str, Any], runtime: Runtime[dict[str, Any] | BaseModel], config: RunnableConfig | None = None) -> dict[str, Any]:
        """Execute the map and reduce operations.

        Args:
            state (dict[str, Any]): The current state of the pipeline.
            runtime (Runtime[dict[str, Any] | BaseModel]): Runtime information for this step's execution.
            config (RunnableConfig | None, optional): The runnable configuration. Defaults to None.

        Returns:
            dict[str, Any]: The reduced result stored under output_state.

        Raises:
            RuntimeError: If an error occurs during execution.
        """

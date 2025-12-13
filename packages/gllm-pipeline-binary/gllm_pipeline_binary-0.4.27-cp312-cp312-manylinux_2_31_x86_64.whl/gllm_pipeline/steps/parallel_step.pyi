from _typeshed import Incomplete
from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec, PipelineSteps as PipelineSteps
from gllm_pipeline.steps.branching_step import BranchingStep as BranchingStep
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.utils.copy import safe_deepcopy as safe_deepcopy
from gllm_pipeline.utils.error_handling import ValidationError as ValidationError, create_error_context as create_error_context
from gllm_pipeline.utils.graph import create_edge as create_edge
from gllm_pipeline.utils.has_inputs_mixin import HasInputsMixin as HasInputsMixin
from gllm_pipeline.utils.input_map import shallow_dump as shallow_dump
from gllm_pipeline.utils.mermaid import MERMAID_HEADER as MERMAID_HEADER
from gllm_pipeline.utils.step_execution import execute_sequential_steps as execute_sequential_steps
from langchain_core.runnables import RunnableConfig as RunnableConfig
from langgraph.graph import StateGraph as StateGraph
from langgraph.runtime import Runtime as Runtime
from langgraph.types import RetryPolicy as RetryPolicy
from pydantic import BaseModel as BaseModel
from typing import Any

class ParallelStep(BranchingStep, HasInputsMixin):
    """A pipeline step that executes multiple branches in parallel.

    This step wraps multiple branches and executes them concurrently, then merges their results.
    Each branch can be either a single step or a list of steps to be executed sequentially.

    The step supports two execution modes controlled by the `squash` parameter:
    1. Squashed (default): Uses asyncio.gather() to run branches in parallel within a single LangGraph node. Use for:
       a. Better raw performance
       b. Simpler implementation
       c. Less overhead
       d. Less transparent for debugging and tracing
    2. Expanded (squash=False): Creates a native LangGraph structure with multiple parallel paths. Use for:
       a. More native LangGraph integration
       b. More transparent for debugging and tracing

    For memory optimization, you can specify input_states to pass only specific keys to branches.
    This is especially useful when the state is large but branches only need specific parts of it.
    If input_states is None (default), all state keys will be passed.

    Attributes:
        name (str): A unique identifier for this pipeline step.
        branches (dict[str, PipelineSteps]): The branches to execute in parallel.
        input_map (dict[str, str | Val] | None): Unified input map.
        squash (bool): Whether to squash execution into a single node.
            1. If True, uses asyncio.gather() to run branches in parallel. This will create a single node.
            2. If False, uses native LangGraph structures for parallelism. This will create multiple nodes.
        retry_policy (RetryPolicy | None): Configuration for retry behavior using LangGraph's RetryPolicy.
    """
    squash: Incomplete
    branches: Incomplete
    def __init__(self, name: str, branches: list[PipelineSteps] | dict[str, PipelineSteps], input_states: list[str] | None = None, squash: bool = True, runtime_config_map: dict[str, str] | None = None, fixed_args: dict[str, Any] | None = None, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        '''Initialize a new ParallelStep.

        Args:
            name (str): A unique identifier for this pipeline step.
            branches (list | dict[str, PipelineSteps]): The branches to execute in parallel. Can be either:
                **List format:**
                    Each branch can be:
                    1. A single step
                    2. A list of steps to execute sequentially
                    Example: [step1, [step2, step3], step4]
                **Dict format:**
                    Keys are branch names, values can be:
                    1. A single step
                    2. A list of steps to execute sequentially
                    Example: {"analysis": step1, "validation": [step2, step3], "cleanup": step4}
                    Enables more intuitive step exclusion using branch names.
            input_states (list[str] | None, optional): Keys from the state to pass to branches.
                If None, all state keys will be passed. Defaults to None.
            squash (bool, optional): Whether to squash execution into a single node.
                1. If True, uses asyncio.gather() to run branches in parallel. This will create a single node.
                2. If False, uses native LangGraph structures for parallelism. This will create multiple nodes.
                Defaults to True.
            runtime_config_map (dict[str, str] | None, optional): Mapping of input keys to runtime config keys.
                Defaults to None.
            fixed_args (dict[str, Any] | None, optional): Fixed arguments to be passed to the component.
                Defaults to None, in which case an empty dictionary is used.
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
    def add_to_graph(self, graph: StateGraph, previous_endpoints: list[str], retry_policy: RetryPolicy | None = None) -> list[str]:
        """Handle both squashed and expanded modes.

        For squashed mode: add the parallel step as a single node.
        For expanded mode: add the parallel step as a single node and add children to graph.

        Args:
            graph (StateGraph): The graph to add this step to.
            previous_endpoints (list[str]): Endpoints from previous steps to connect to.
            retry_policy (RetryPolicy | None, optional): Retry policy to propagate to child steps.
                Defaults to None, in which case the retry policy of the step is used.

        Returns:
            list[str]: Exit points after adding all child steps.
        """
    async def execute(self, state: dict[str, Any], runtime: Runtime[dict[str, Any] | BaseModel], config: RunnableConfig | None = None) -> dict[str, Any] | None:
        """Execute all branches in parallel and merge their results.

        This method is only used for the squashed approach. For the expanded approach,
        the execution is handled by the graph structure.

        Args:
            state (dict[str, Any]): The current state of the pipeline.
            runtime (Runtime[dict[str, Any] | BaseModel]): Runtime information for this step's execution.
            config (RunnableConfig | None, optional): The runnable configuration. Defaults to None.

        Returns:
            dict[str, Any] | None: The merged results from all parallel branches, or None if no updates were produced.

        Raises:
            asyncio.CancelledError: If execution is cancelled, preserved with added context.
            BaseInvokerError: If an error occurs during LM invocation.
            RuntimeError: For all other exceptions during execution, wrapped with context information.
            TimeoutError: If execution times out, preserved with added context.
            ValidationError: If input validation fails.
        """

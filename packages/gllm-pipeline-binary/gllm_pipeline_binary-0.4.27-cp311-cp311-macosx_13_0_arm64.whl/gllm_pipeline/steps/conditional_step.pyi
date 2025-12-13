from _typeshed import Incomplete
from dataclasses import dataclass
from gllm_core.event.event_emitter import EventEmitter as EventEmitter
from gllm_core.schema import Component
from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec, PipelineState as PipelineState, PipelineSteps as PipelineSteps
from gllm_pipeline.steps.branching_step import BranchingStep as BranchingStep
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.steps.terminator_step import TerminatorStep as TerminatorStep
from gllm_pipeline.types import Val as Val
from gllm_pipeline.utils.async_utils import execute_callable as execute_callable
from gllm_pipeline.utils.graph import create_edge as create_edge
from gllm_pipeline.utils.has_inputs_mixin import HasInputsMixin as HasInputsMixin
from gllm_pipeline.utils.input_map import shallow_dump as shallow_dump
from gllm_pipeline.utils.mermaid import MERMAID_HEADER as MERMAID_HEADER
from gllm_pipeline.utils.step_execution import execute_sequential_steps as execute_sequential_steps
from langchain_core.runnables import RunnableConfig as RunnableConfig
from langgraph.graph import StateGraph as StateGraph
from langgraph.runtime import Runtime as Runtime
from langgraph.types import Command, RetryPolicy as RetryPolicy
from pydantic import BaseModel as BaseModel
from typing import Any, Callable

ConditionType = Component | Callable[[dict[str, Any]], str]
DEFAULT_BRANCH: str

@dataclass
class ConditionInputs:
    """Container for different types of inputs used in condition evaluation.

    Attributes:
        merged (dict[str, Any]): Complete merged dictionary containing all state, config, and fixed args.
            Used for Callable conditions.
        mapped (dict[str, Any]): Dictionary containing only explicitly mapped inputs.
            Used for Component conditions.
        event_emitter (EventEmitter | None): Event emitter instance for logging.
        has_mapped_specs (bool): Whether the mapped inputs have specs or is a literal value.
    """
    merged: dict[str, Any]
    mapped: dict[str, Any]
    event_emitter: EventEmitter | None
    has_mapped_specs: bool

class ConditionalStep(BranchingStep, HasInputsMixin):
    '''A conditional pipeline step that conditionally executes different branches based on specified conditions.

    This step evaluates one or more conditions and selects a branch to execute based on the result.
    It provides flexibility in defining complex conditional logic within a pipeline.

    A minimal usage requires defining the branches to execute based on a `condition`, which is a callable
    that takes input from the state and returns a string identifying the branch to execute.

    The condition can be a `Component` or a `Callable`. The handling of inputs differs:
    1. If the condition is a `Component`, `input_map` is used to map the pipeline\'s
        state and config to the component\'s inputs.
    2. If the condition is a `Callable`, it receives a merged dictionary of the
        pipeline\'s state and config directly. In this case, `input_map` is not used
        to build the payload and should not be passed.

    Example:
    ```python
    ConditionalStep(
        name="UseCaseSelection",
        branches={"A": step_a, DEFAULT_BRANCH: step_b},
        condition=lambda x: "A" if "<A>" in x["query"] else "__default__"
    )
    ```
    This will execute `step_a` if the query contains "<A>", and `step_b` otherwise.

    The special key `__default__` (importable as DEFAULT_BRANCH) defines the default branch to execute
    if no other condition matches. If the DEFAULT_BRANCH is not defined and no condition matches,
    the step will raise an error.

    Attributes:
        name (str): A unique identifier for this pipeline step.
        branches (dict[str, BasePipelineStep | list[BasePipelineStep]]): Mapping of condition results to steps.
        condition (list[ConditionType] | None): The condition(s) to evaluate for branch selection.
        input_map (dict[str, str | Val] | None): Unified input map.
        output_state (str | None): Key to store the condition result in the state, if desired.
        condition_aggregator (Callable[[list[Any]], str]): Function to aggregate multiple condition results.
        retry_policy (RetryPolicy | None): Configuration for retry behavior using LangGraph\'s RetryPolicy.
        error_handler (BaseStepErrorHandler | None): Strategy to handle errors during execution.
    '''
    branches: Incomplete
    condition: Incomplete
    output_state: Incomplete
    condition_aggregator: Incomplete
    def __init__(self, name: str, branches: dict[str, BasePipelineStep | list[BasePipelineStep]], condition: ConditionType | list[ConditionType] | None = None, input_state_map: dict[str, str] | None = None, output_state: str | None = None, condition_aggregator: Callable[[list[Any]], str] = ..., runtime_config_map: dict[str, str] | None = None, fixed_args: dict[str, Any] | None = None, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        '''Initializes a new ConditionalStep.

        Args:
            name (str): A unique identifier for this pipeline step.
            branches (dict[str, BasePipelineStep | list[BasePipelineStep]]): Mapping of condition results to steps to
                execute.
            condition (ConditionType | list[ConditionType] | None, optional): The condition(s) to evaluate for branch
                selection. If a `Callable`, it receives the merged state and config as keyword arguments. If None,
                the condition is evaluated from the state. Defaults to None.
            input_state_map (dict[str, str] | None, optional): A dictionary mapping the state keys to the component\'s
                input keys. This is only used if the condition is a `Component`. Defaults to None.
            output_state (str | None, optional): Key to store the condition result in the state. If None, the
                output is not saved in the state. Defaults to None.
            condition_aggregator (Callable[[list[Any]], str], optional): Function to aggregate multiple condition
                results. Defaults to joining results with a semicolon (";").
            runtime_config_map (dict[str, str] | None, optional): A dictionary mapping the runtime config keys to the
                component\'s input keys. This is only used if the condition is a
                `Component`. Defaults to None.
            fixed_args (dict[str, Any] | None, optional): Fixed arguments to be passed to the condition.
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
    async def execute(self, state: PipelineState, runtime: Runtime[dict[str, Any] | BaseModel], config: RunnableConfig | None = None) -> Command:
        """Executes the conditional step, determines the route, and returns a Command.

        Args:
            state (PipelineState): The current state of the pipeline.
            runtime (Runtime[dict[str, Any] | BaseModel]): Runtime information for this step's execution.
            config (RunnableConfig | None, optional): The runnable configuration. Defaults to None.

        Returns:
            Command: A LangGraph Command object with 'goto' for routing and 'update' for state changes.
        """
    async def execute_direct(self, state: dict[str, Any], runtime: Runtime[dict[str, Any] | BaseModel], config: RunnableConfig | None = None) -> dict[str, Any] | None:
        """Execute this step directly, handling both branch selection and execution.

        This method is used when the step needs to be executed directly (e.g. in parallel execution).
        It will both select and execute the appropriate branch, unlike execute() which only handles selection.

        Args:
            state (dict[str, Any]): The current state of the pipeline.
            runtime (Runtime[dict[str, Any] | BaseModel]): Runtime information for this step's execution.
            config (RunnableConfig | None, optional): The runnable configuration. Defaults to None.

        Returns:
            dict[str, Any] | None: Updates to apply to the pipeline state, or None if no updates.
        """
    async def select_path(self, state: dict[str, Any], runtime: Runtime[dict[str, Any] | BaseModel]) -> str:
        """Determines the logical route key based on the evaluated condition(s).

        This method prepares input data, evaluates conditions, aggregates results,
        and determines the logical route key.

        Args:
            state (dict[str, Any]): The current state of the pipeline, containing all data.
            runtime (Runtime[dict[str, Any] | BaseModel]): Runtime information for this step's execution.

        Returns:
            str: The identifier of the selected logical route. Returns DEFAULT_BRANCH if an error occurs
                or if the condition result doesn't match any branch key.
        """

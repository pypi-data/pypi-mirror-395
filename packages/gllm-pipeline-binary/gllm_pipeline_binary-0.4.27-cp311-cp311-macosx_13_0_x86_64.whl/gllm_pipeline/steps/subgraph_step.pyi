from _typeshed import Incomplete
from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec, PipelineState as PipelineState
from gllm_pipeline.exclusions import ExclusionSet as ExclusionSet
from gllm_pipeline.pipeline.pipeline import Pipeline as Pipeline
from gllm_pipeline.steps.composite_step import BaseCompositeStep as BaseCompositeStep
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.utils.error_handling import ErrorContext as ErrorContext
from gllm_pipeline.utils.has_inputs_mixin import HasInputsMixin as HasInputsMixin
from gllm_pipeline.utils.input_map import shallow_dump as shallow_dump
from langchain_core.runnables import RunnableConfig as RunnableConfig
from langgraph.runtime import Runtime as Runtime
from pydantic import BaseModel as BaseModel
from typing import Any

class SubgraphStep(BaseCompositeStep, HasInputsMixin):
    """A pipeline step that executes another pipeline as a subgraph.

    This step allows for encapsulation and reuse of pipeline logic by treating another pipeline as a step.
    The subgraph can have its own state schema, and this step handles the mapping between the parent and
    subgraph states.

    Attributes:
        name (str): A unique identifier for this pipeline step.
        subgraph (Pipeline): The pipeline to be executed as a subgraph.
        input_map (dict[str, str | Val] | None): Unified input map.
        output_state_map (dict[str, str]): Mapping of parent pipeline state keys to subgraph output keys.
        retry_policy (RetryPolicy | None): Configuration for retry behavior using LangGraph's RetryPolicy.
    """
    subgraph: Incomplete
    output_state_map: Incomplete
    def __init__(self, name: str, subgraph: Pipeline, input_state_map: dict[str, str] | None = None, output_state_map: dict[str, str] | None = None, runtime_config_map: dict[str, str] | None = None, fixed_args: dict[str, Any] | None = None, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        '''Initializes a new SubgraphStep.

        Args:
            name (str): A unique identifier for this pipeline step.
            subgraph (Pipeline): The pipeline to be executed as a subgraph.
            input_state_map (dict[str, str]): Mapping of subgraph input keys to parent pipeline state keys.
                Defaults to None.
            output_state_map (dict[str, str] | None, optional): Mapping of parent pipeline state keys to
                subgraph output keys. Defaults to None.
            runtime_config_map (dict[str, str] | None, optional): Mapping of subgraph input keys to runtime
                configuration keys. Defaults to None, in which case an empty dictionary is used.
            fixed_args (dict[str, Any] | None, optional): Fixed arguments to be passed to the subgraph.
                Defaults to None, in which case an empty dictionary is used.
            input_map (InputMapSpec | None, optional):
                Unified input map. Can be a dict (arg -> str|Val) or a list with elements:
                1. str for identity mapping
                2. dict[str, str] for state/config mapping
                3. dict[str, Val] for fixed args.
                Defaults to None.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using the SDK\'s RetryConfig.
                If None, no retry policy is applied.
            error_handler (BaseStepErrorHandler | None, optional): Error handler to be used for this step.
                If None, no error handler is applied.
            cache_store ("BaseCache" | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.
        '''
    async def execute(self, state: PipelineState, runtime: Runtime[dict[str, Any] | BaseModel], config: RunnableConfig | None = None) -> dict[str, Any]:
        """Executes the subgraph and processes its output.

        This method prepares data, executes the subgraph, and formats the output for integration
        into the parent pipeline state. It only uses keys that are actually present in the state,
        ignoring missing keys to prevent errors.

        Args:
            state (PipelineState): The current state of the pipeline, containing all data.
            runtime (Runtime[dict[str, Any] | BaseModel]): Runtime information for this step's execution.
            config (RunnableConfig | None, optional): The runnable configuration. Defaults to None.

        Returns:
            dict[str, Any]: The update to the pipeline state after this step's operation.
                This includes new or modified data produced by the subgraph, not the entire state.
                If a requested output key is not present in the subgraph result, its value will be None.

        Raises:
            RuntimeError: If an error occurs during subgraph execution, with details about which step caused the error.
        """
    is_excluded: Incomplete
    def apply_exclusions(self, exclusions: ExclusionSet) -> None:
        """Apply exclusions to this subgraph and its children.

        Subgraph has no internal structural changes. It marks itself and
        uniformly propagates child exclusions to all subgraph steps.

        Args:
            exclusions (ExclusionSet): The exclusion set to apply.
        """

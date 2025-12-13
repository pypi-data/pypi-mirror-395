from _typeshed import Incomplete
from gllm_core.schema.tool import Tool
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import PipelineState as PipelineState
from gllm_pipeline.exclusions import ExclusionManager as ExclusionManager, ExclusionSet as ExclusionSet
from gllm_pipeline.pipeline.composer import Composer as Composer
from gllm_pipeline.pipeline.states import RAGState as RAGState
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.terminator_step import TerminatorStep as TerminatorStep
from gllm_pipeline.utils.graph import create_edge as create_edge
from gllm_pipeline.utils.mermaid import MERMAID_HEADER as MERMAID_HEADER, combine_mermaid_diagrams as combine_mermaid_diagrams, extract_step_diagrams as extract_step_diagrams
from gllm_pipeline.utils.typing_compat import TypedDict as TypedDict, is_typeddict as is_typeddict
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph as CompiledStateGraph
from pydantic import BaseModel
from typing import Any

DEFAULT_TOOL_NAME: str
INDENTATION: str

class Pipeline:
    '''Represents a sequence of steps executed in order, forming a pipeline.

    A pipeline can have zero or more steps. When a pipeline has no steps (empty list), it acts as a
    pass-through pipeline that simply returns the input state unchanged. This is useful when using
    the pipe (|) operator to define RAG State without requiring explicit steps.

    Attributes:
        steps (list[BasePipelineStep]): List of steps to be executed in the pipeline. Can be empty
            for a pass-through pipeline.
        state_type (type): The type of state used in the pipeline. Defaults to RAGState.
        recursion_limit (int): The maximum number of steps allowed.
        name (str | None): A name for this pipeline. Used when this pipeline is included as a subgraph.
            Defaults to None, in which case the name will be "Subgraph" followed by a unique identifier.
        exclusions (ExclusionManager): The exclusion manager for this pipeline.

    Usage examples:
        # Basic pipeline with steps
        ```python
        pipeline = Pipeline([retrieval_step, generation_step, terminator_step])
        ```

        # Empty pipeline (pass-through)
        ```python
        pipeline = Pipeline([])
        pipeline = Pipeline(None)
        ```

        # Pipeline with custom state type
        ```python
        class CustomState(TypedDict):
            user_query: str
            context: str
            response: str

        pipeline = Pipeline([retrieval_step, generation_step], state_type=CustomState)
        ```

        # Named pipeline for subgraph usage
        ```python
        pipeline = Pipeline([retrieval_step, generation_step], name="rag_pipeline")
        ```

        # Pipeline with caching
        ```python
        pipeline = Pipeline(
            [retrieval_step, generation_step],
            cache_store=cache_store,
            cache_config={"ttl": 3600, "name": "rag_cache"}
        )
        ```

        # Using pipe (|) operator to combine steps
        ```python
        pipeline = retrieval_step | generation_step | terminator_step
        ```
        # Using pipe (|) operator to combine step with pipeline
        ```python
        pipeline = Pipeline([retrieval_step, generation_step]) | terminator_step
        ```
        # Using pipe (|) operator to combine pipelines
        ```python
        pipeline1 = Pipeline([retrieval_step])
        pipeline2 = Pipeline([generation_step, terminator_step])
        combined_pipeline = pipeline1 | pipeline2
        ```

        # Configure step exclusion after initialization (set-only)
        ```python
        log_step = log(name="log_step", ...)
        retrieval_step = step(name="retrieval_step", ...)
        generation_step = step(name="generation_step", ...)
        pipeline = Pipeline([log_step, retrieval_step, generation_step])
        pipeline.exclusions.exclude("log_step")  # Skip logging step
        ```

        # Configure composite step exclusion
        ```python
        log_step = log(name="log_step", ...)
        retrieval_a_step = step(name="retrieval_a_step", ...)
        retrieval_b_step = step(name="retrieval_b_step", ...)
        parallel_step = parallel(
            name="parallel_step", {"retrieval_a": retrieval_a_step, "retrieval_b": retrieval_b_step},
        )
        pipeline = Pipeline([log_step, parallel_step])
        pipeline.exclusions.exclude("parallel_step")  # Skip the entire parallel step
        pipeline.exclusions.exclude("parallel_step.retrieval_a")  # Skip retrieval_a step
        pipeline.exclusions.exclude("parallel_step.retrieval_b")  # Skip retrieval_b step
        ```
    '''
    name: Incomplete
    steps: Incomplete
    recursion_limit: Incomplete
    def __init__(self, steps: list[BasePipelineStep] | None = None, state_type: TypedDict | type[BaseModel] = ..., input_type: TypedDict | type[BaseModel] | None = None, output_type: TypedDict | type[BaseModel] | None = None, context_schema: TypedDict | type[BaseModel] | None = None, recursion_limit: int = 30, name: str | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        '''Initializes the Pipeline with the given steps and state type.

        Args:
            steps (list[BasePipelineStep] | None, optional): List of steps to be executed in the pipeline.
                Defaults to None, in which case the steps will be `[]` and simply returns the input state unchanged.
            state_type (TypedDict | type[BaseModel], optional): The type of pipeline\'s overall internal state.
                Could be a TypedDict or a Pydantic BaseModel. Defaults to RAGState.
            input_type (TypedDict | type[BaseModel] | None, optional): The type of pipeline\'s input state.
                This state should be compatible with the pipeline\'s `state_type`.
                Could be a TypedDict or a Pydantic BaseModel. Defaults to None, in which case the input state type
                will be the same as the pipeline\'s `state_type`.
            output_type (TypedDict | type[BaseModel] | None, optional): The type of pipeline\'s output state.
                This state should be compatible with the pipeline\'s `state_type`.
                Could be a TypedDict or a Pydantic BaseModel. Defaults to None, in which case the output state type
                will be the same as the pipeline\'s `state_type`.
            context_schema (TypedDict | type[BaseModel] | None, optional): The type of pipeline\'s runtime context.
                Defaults to None, in which case no context schema will be used.
            recursion_limit (int, optional): The maximum number of steps allowed. Defaults to 30.
            name (str | None, optional): A name for this pipeline. Used when this pipeline is included as a subgraph.
                Defaults to None, in which case the name will be "Subgraph" followed by a unique identifier.
            cache_store ("BaseCache" | None, optional): The cache store to use for caching pipeline results.
                Defaults to None. Defaults to None, in which case no caching will be used.
            cache_config (dict[str, Any] | None, optional): Configuration for the cache store.
                Defaults to None, in which case no cache configuration will be used.
                The cache config should be a dictionary with the following keys:
                1. key_func (Callable | None, optional): A function to generate cache keys.
                    Defaults to None, in which case the cache instance will use its own key function.
                2. name (str | None, optional): The name of the cache.
                    Defaults to None, in which case the cache instance will use its own key function.
                3. ttl (int | None, optional): The time-to-live for the cache.
                    Defaults to None, in which case the cache will not have a TTL.
                4. matching_strategy (str | None, optional): The strategy for matching cache keys.
                    Defaults to None, in which case the cache instance will use "exact".
                5. matching_config (dict[str, Any] | None, optional): Configuration for the matching strategy.
                    Defaults to None, in which case the cache instance will use its
                    own default matching strategy configuration.
        '''
    @property
    def state_type(self) -> type:
        """The current state type of the pipeline.

        Returns:
            type: The current state type.
        """
    @state_type.setter
    def state_type(self, new_state_type: TypedDict | type[BaseModel]) -> None:
        """Sets a new state type for the pipeline.

        Args:
            new_state_type (TypedDict | type[BaseModel]): The new state type to set.

        Note:
            This operation will rebuild the pipeline graph if it has already been initialized, which can be
            computationally expensive for complex pipelines.
            It is recommended to set the state type before building the pipeline graph.
        """
    @property
    def graph(self) -> StateGraph:
        """The graph representation of the pipeline.

        If the graph doesn't exist yet, it will be built automatically.

        Returns:
            StateGraph: The graph representation of the pipeline.
        """
    @property
    def exclusions(self) -> ExclusionManager:
        """Get the exclusion manager for this pipeline.

        Returns:
            ExclusionManager: The exclusion manager for this pipeline.
        """
    @property
    def composer(self) -> Composer:
        """Get a Composer instance that manages this pipeline.

        The Composer provides a fluent API for building pipelines by chaining
        step-adding methods. It allows for easy composition of pipeline steps
        in a readable, chainable manner.

        Returns:
            Composer: A composer instance that manages this pipeline.
        """
    def as_tool(self, description: str | None = None) -> Tool:
        '''Convert the pipeline to a Tool instance.

        This method allows a Pipeline instance to be used as a tool, with the input schema
        being derived from the pipeline\'s input schema. The pipeline must have an input_type
        defined to be convertible as a tool.

        Args:
            description (str | None, optional): Optional description to associate with the tool.
                Defaults to None, in which case a description will be generated automatically.

        Returns:
            Tool: A Tool instance that wraps the pipeline.

        Raises:
            ValueError: If the pipeline does not have an input schema defined.

        Examples:
            ```python
            class InputState(TypedDict):
                user_query: str
                context: str

            class OutputState(TypedDict):
                result: str

            pipeline = Pipeline(
                [retrieval_step, generation_step],
                input_type=InputState,
                output_type=OutputState,
                name="rag_pipeline"
            )

            tool = pipeline.as_tool(description="Process user questions")
            result = await tool.invoke(user_query="What is AI?", context="")
            ```
        '''
    def clear(self) -> None:
        """Clears the pipeline by resetting steps, graph, and app to their initial state.

        This method resets the pipeline to an empty state, clearing all steps and
        invalidating any built graph or compiled app. Useful for reusing a pipeline
        instance with different configurations.
        """
    async def invoke(self, initial_state: PipelineState, config: dict[str, Any] | None = None, thread_id: str | None = None) -> dict[str, Any]:
        '''Runs the pipeline asynchronously with the given initial state and configuration.

        Args:
            initial_state (PipelineState): The initial state to start the pipeline with.
                This initial state should comply with the state type of the pipeline.
            config (dict[str, Any], optional): Additional configuration for the pipeline. User-defined config should not
                have "langgraph_" prefix as it should be reserved for internal use. Defaults to None.
            thread_id (str | None, optional): The thread ID for this specific pipeline invocation. This will be passed
                in the invocation_config.configurable when invoking the pipeline. Useful for checkpointing and
                tracking related invocations. Defaults to None.

        Returns:
            dict[str, Any]: The final state after the pipeline execution.
                If \'debug_state\' is set to True in the config, the state logs will be included
                in the final state with the key \'__state_logs__\'.

        Raises:
            BaseInvokerError: If an error occurs during LM invocation.
            asyncio.CancelledError: If the execution is cancelled, preserved with added context.
            TimeoutError: If the execution times out, preserved with added context.
            RuntimeError: If an error occurs during pipeline execution. If the error is due to a step
                execution, the step name will be included in the error message.
        '''
    def build_graph(self) -> None:
        """Builds the graph representation of the pipeline by connecting the steps."""
    def get_mermaid_diagram(self) -> str:
        """Generate a Mermaid diagram representation of the pipeline.

        Returns:
            str: The complete Mermaid diagram representation.
        """
    def __or__(self, other: Pipeline | BasePipelineStep) -> Pipeline:
        """Combines the current pipeline with another pipeline or step using the '|' operator.

        When combining two pipelines, the state types must match.

        Args:
            other (Pipeline | BasePipelineStep): The other pipeline or step to combine with.

        Returns:
            Pipeline: A new pipeline consisting of the combined steps.

        Raises:
            ValueError: If the state types of the pipelines do not match.
        """
    def __lshift__(self, other: Pipeline | BasePipelineStep) -> Pipeline:
        """Includes another pipeline or step using the '<<' operator.

        This allows for easy composition where:
        - If 'other' is a Pipeline: it becomes a subgraph within this pipeline
        - If 'other' is a BasePipelineStep: it's added directly to this pipeline's steps

        The syntax `pipeline1 << pipeline2` visually indicates pipeline2 being inserted into pipeline1.
        The syntax `pipeline << step` adds the step to the pipeline.

        Args:
            other (Pipeline | BasePipelineStep): The pipeline to include as a subgraph or step to add.

        Returns:
            Pipeline: A new pipeline with the other pipeline included as a subgraph step or with the step added.
        """
    def __rshift__(self, other: Pipeline | BasePipelineStep) -> Pipeline:
        """Includes this pipeline as a subgraph in another context using the '>>' operator.

        This allows for easy composition where:
        - If 'other' is a Pipeline: this pipeline becomes a subgraph within the other pipeline
        - If 'other' is a BasePipelineStep: a new pipeline is created with the step, and this pipeline
          is included as a subgraph within that pipeline

        The syntax `pipeline1 >> pipeline2` embeds pipeline1 as a subgraph within pipeline2
        (equivalent to pipeline2 << pipeline1).
        The syntax `pipeline >> step` creates a new pipeline with the step, and includes this pipeline
        as a subgraph within that pipeline.

        Args:
            other (Pipeline | BasePipelineStep): The pipeline to include this pipeline in as a subgraph,
                or a step to create a new pipeline with.

        Returns:
            Pipeline: A new pipeline with this pipeline included as a subgraph.
        """

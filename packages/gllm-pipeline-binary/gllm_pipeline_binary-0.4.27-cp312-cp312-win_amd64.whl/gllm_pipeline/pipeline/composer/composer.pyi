from gllm_core.schema import Component as Component
from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec
from gllm_pipeline.pipeline.composer.guard_composer import GuardComposer as GuardComposer
from gllm_pipeline.pipeline.composer.if_else_composer import IfElseComposer as IfElseComposer
from gllm_pipeline.pipeline.composer.parallel_composer import ParallelComposer as ParallelComposer
from gllm_pipeline.pipeline.composer.switch_composer import SwitchComposer as SwitchComposer
from gllm_pipeline.pipeline.composer.toggle_composer import ToggleComposer as ToggleComposer
from gllm_pipeline.pipeline.pipeline import Pipeline as Pipeline
from gllm_pipeline.schema import PipelineSteps as PipelineSteps
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from typing import Any, Callable, Self, overload

class Composer:
    """Fluent API for composing a pipeline out of simple steps.

    The composer accumulates steps in order and can build a `Pipeline` with
    a specified state type, recursion limit, and optional name.

    The Composer uses a manager-style API:
    1. When initialized with an existing `Pipeline` instance, it manages the pipeline in place.
    2. If none is provided, a new empty `Pipeline` with the default `RAGState` is created.

    Examples:
    ```python
    # With existing pipeline
    composer = Composer(existing_pipeline).no_op().terminate()
    pipeline = composer.done()
    ```

    ```python
    # With new pipeline
    composer = Composer().no_op().terminate()
    pipeline = composer.done()
    ```
    """
    def __init__(self, pipeline: Pipeline | None = None) -> None:
        """Create a composer that manages a pipeline instance.

        Args:
            pipeline (Pipeline | None, optional): Pipeline to modify. Defaults to None,
                in which case a new empty pipeline with the default `RAGState` is created.
        """
    def step(self, component: Component, input_map: InputMapSpec, output_state: str | list[str] | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, name: str | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> Self:
        '''Append a component step.

        Args:
            component (Component): The component to execute.
            input_map (InputMapSpec): Unified input mapping for the component.
            output_state (str | list[str] | None, optional): Key to store the result in the pipeline state.
                Defaults to None.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using
                GLLM Core\'s RetryConfig. Defaults to None, in which case no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Error handler to use for this step.
                Defaults to None, in which case no error handler is used.
            name (str | None, optional): A unique identifier for this step. If None, a name will be
                auto-generated with the prefix "step_". Defaults to None.
            cache_store (BaseCache | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.

        Returns:
            Self: The composer instance with this step appended.
        '''
    def map_reduce(self, input_map: InputMapSpec, output_state: str, map_func: Component | Callable[[dict[str, Any]], Any], reduce_func: Callable[[list[Any]], Any] = ..., retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> Self:
        """Append a map-reduce step.

        Args:
            input_map (InputMapSpec): Unified input mapping for the map function.
            output_state (str): Key to store the reduced result in the pipeline state.
            map_func (Component | Callable[[dict[str, Any]], Any]): Function to apply to each input item.
            reduce_func (Callable[[list[Any]], Any], optional): Function to reduce mapped results.
                Defaults to a function that returns the list of results as is.
            retry_config (RetryConfig | None, optional): Retry behavior configuration.
                Defaults to None, in which case no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Error handler to use for this step.
                Defaults to None, in which case the default error handler is used.
            cache_store (BaseCache | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.
            name (str | None, optional): Optional name for the step. Defaults to None.

        Returns:
            Self: The composer instance with this step appended.
        """
    def subgraph(self, subgraph: Pipeline, input_map: InputMapSpec | None = None, output_state_map: dict[str, str] | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> Self:
        """Append a subgraph step that executes another pipeline.

        Args:
            subgraph (Pipeline): The pipeline to be executed as a subgraph.
            input_map (InputMapSpec | None, optional): Unified input mapping for the subgraph. Defaults to None.
            output_state_map (dict[str, str] | None, optional): Map parent state keys to subgraph output keys.
                Defaults to None, in which case all outputs are passed through.
            retry_config (RetryConfig | None, optional): Retry behavior configuration.
                Defaults to None, in which case no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Error handler to use for this step.
                Defaults to None, in which case the default error handler is used.
            cache_store (BaseCache | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.
            name (str | None, optional): Optional name for the step. Defaults to None.

        Returns:
            Self: The composer instance with this step appended.
        """
    def log(self, message: str, is_template: bool = True, emit_kwargs: dict[str, Any] | None = None, retry_config: RetryConfig | None = None, name: str | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> Self:
        '''Append a log step.

        Args:
            message (str): The message to log.
            is_template (bool, optional): Whether the message is a template. Defaults to True.
            emit_kwargs (dict[str, Any] | None, optional): Keyword arguments to pass to the emit function.
                Defaults to None.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using
                GLLM Core\'s RetryConfig. Defaults to None, in which case no retry config is applied.
            name (str | None, optional): A unique identifier for this step. If None, a name will be
                auto-generated with the prefix "step_". Defaults to None.
            cache_store (BaseCache | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.

        Returns:
            Self: The composer instance with this step appended.
        '''
    def no_op(self, name: str | None = None) -> Self:
        '''Append a no-op step.

        Args:
            name (str | None, optional): A unique identifier for this step. If None, a name will be
                auto-generated with the prefix "no_op_". Defaults to None.

        Returns:
            Self: The composer instance with this step appended.
        '''
    def bundle(self, input_states: list[str] | dict[str, str], output_state: str | list[str], retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> Self:
        """Append a bundle step to combine multiple state keys.

        Args:
            input_states (list[str] | dict[str, str]): List of keys to bundle as-is or mapping of
                output field names to source state keys.
            output_state (str | list[str]): State key(s) to store the bundled result.
            retry_config (RetryConfig | None, optional): Retry configuration for the step. Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Error handler for this step. Defaults to None.
            cache_store (BaseCache | None, optional): Cache store for this step. Defaults to None.
            cache_config (dict[str, Any] | None, optional): Cache configuration for this step. Defaults to None.
            name (str | None, optional): Optional name for the step. Defaults to None.

        Returns:
            Self: The composer instance with this step appended.
        """
    def copy(self, input_state: str | list[str], output_state: str | list[str], retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> Self:
        '''Append a copy step to copy input state(s) to output state(s).

        This method creates a step that copies data from input state(s) to output state(s) without transformation.
        The function handles different scenarios:
        1. Single input to single output: Direct copy
        2. Single input to multiple outputs: Broadcast the input to all outputs
        3. Multiple inputs to single output: Pack all inputs into a list
        4. Multiple inputs to multiple outputs: Copy each input to corresponding output (must have same length)

        Args:
            input_state (str | list[str]): Input state key(s) to copy from.
            output_state (str | list[str]): Output state key(s) to copy to.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using
                GLLM Core\'s RetryConfig. Defaults to None, in which case no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Error handler to use for this step.
                Defaults to None, in which case no error handler is used.
            cache_store (BaseCache | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.
            name (str | None, optional): A unique identifier for this step. If None, a name will be
                auto-generated with the prefix "copy_". Defaults to None.

        Returns:
            Self: The composer instance with this step appended.
        '''
    def transform(self, operation: Callable[[dict[str, Any]], Any], input_map: InputMapSpec, output_state: str | list[str], retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, name: str | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> Self:
        '''Append a state operator step.

        Args:
            operation (Callable[[dict[str, Any]], Any]): The operation to apply to the state.
            input_map (InputMapSpec): Unified input mapping for the operation.
            output_state (str | list[str]): State key(s) to store the result in.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using
                GLLM Core\'s RetryConfig. Defaults to None, in which case no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Error handler to use for this step.
                Defaults to None, in which case no error handler is used.
            name (str | None, optional): A unique identifier for this step. If None, a name will be
                auto-generated with the prefix "transform_". Defaults to None.
            cache_store (BaseCache | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.

        Returns:
            Self: The composer instance with this step appended.
        '''
    def terminate(self, name: str | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> Self:
        '''Append a terminator step.

        Args:
            name (str | None, optional): A unique identifier for this step. If None, a name will be
                auto-generated with the prefix "terminator_". Defaults to None.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using
                GLLM Core\'s RetryConfig. Defaults to None, in which case no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Error handler to use for this step.
                Defaults to None, in which case no error handler is used.
            cache_store (BaseCache | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.

        Returns:
            Self: The composer instance with this step appended.
        '''
    def if_else(self, condition: Component | Callable[[dict[str, Any]], bool], if_branch: BasePipelineStep | list[BasePipelineStep], else_branch: BasePipelineStep | list[BasePipelineStep], input_map: InputMapSpec | None = None, output_state: str | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> Self:
        """Append a direct if/else conditional step.

        This is the direct-style counterpart to the builder returned by `when(...)`.
        Use this when you already have both branches available and prefer a single call.

        Args:
            condition (Component | Callable[[dict[str, Any]], bool]): The condition to evaluate.
            if_branch (BasePipelineStep | list[BasePipelineStep]): Step(s) to execute if condition is true.
            else_branch (BasePipelineStep | list[BasePipelineStep]): Step(s) to execute if condition is false.
            input_map (InputMapSpec | None, optional): Unified input mapping for the condition. Defaults to None.
            output_state (str | None, optional): Optional state key to store the condition result. Defaults to None.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using GLLM Core's
                `RetryConfig`. Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Strategy to handle errors during execution.
                Defaults to None.
            cache_store (BaseCache | None, optional): Cache store to be used for caching. Defaults to None.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None.
            name (str | None, optional): A unique identifier for the conditional step. If None, a name will be
                auto-generated. Defaults to None.

        Returns:
            Self: The composer instance with this step appended.
        """
    def when(self, condition: Component | Callable[[dict[str, Any]], bool], input_map: InputMapSpec | None = None, output_state: str | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> IfElseComposer:
        """Begin an if/else conditional using a fluent builder.

        Returns an `IfElseComposer` bound to this composer. Use `.then(...)` on the returned
        builder to set the true-branch, `.otherwise(...)` to set the false-branch, and `.end()`
        to finalize and return to the parent composer.

        Args:
            condition (Component | Callable[[dict[str, Any]], bool]): The condition to evaluate.
            input_map (InputMapSpec | None, optional): Unified input mapping for this conditional. Defaults to None.
            output_state (str | None, optional): Key to store the outcome state. Defaults to None.
            retry_config (RetryConfig | None, optional): Retry behavior configuration. Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Error handler. Defaults to None.
            cache_store (BaseCache | None, optional): Cache store to be used for caching. Defaults to None.
            cache_config (dict[str, Any] | None, optional): Cache configuration. Defaults to None.
            name (str | None, optional): Optional name for the step. Defaults to None.

        Returns:
            IfElseComposer: A builder to define the branches and finalize with `.end()`.
        """
    @overload
    def switch(self, condition: Component | Callable[[dict[str, Any]], str], *, input_map: InputMapSpec | None = ..., output_state: str | None = ..., retry_config: RetryConfig | None = ..., error_handler: BaseStepErrorHandler | None = ..., cache_store: BaseCache | None = ..., cache_config: dict[str, Any] | None = ..., name: str | None = ...) -> SwitchComposer: ...
    @overload
    def switch(self, condition: Component | Callable[[dict[str, Any]], str], *, branches: dict[str, BasePipelineStep | list[BasePipelineStep]], input_map: InputMapSpec | None = ..., output_state: str | None = ..., default: BasePipelineStep | list[BasePipelineStep] | None = ..., retry_config: RetryConfig | None = ..., error_handler: BaseStepErrorHandler | None = ..., cache_store: BaseCache | None = ..., cache_config: dict[str, Any] | None = ..., name: str | None = ...) -> Self: ...
    @overload
    def parallel(self, *, squash: bool = ..., input_map: InputMapSpec | None = ..., retry_config: RetryConfig | None = ..., error_handler: BaseStepErrorHandler | None = ..., cache_store: BaseCache | None = ..., cache_config: dict[str, Any] | None = ..., name: str | None = ...) -> ParallelComposer: ...
    @overload
    def parallel(self, *, branches: list[PipelineSteps] | dict[str, PipelineSteps], squash: bool = ..., input_map: InputMapSpec | None = ..., retry_config: RetryConfig | None = ..., error_handler: BaseStepErrorHandler | None = ..., cache_store: BaseCache | None = ..., cache_config: dict[str, Any] | None = ..., name: str | None = ...) -> Self: ...
    def parallel(self, *, branches: list[PipelineSteps] | dict[str, PipelineSteps] | None = None, squash: bool = True, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> Self | ParallelComposer:
        '''Create a parallel step (builder-style or direct-style).

        This method supports two usage patterns:
        1) Builder-style (no `branches` provided):
            ```python
            composer.parallel(input_states=["query"], squash=True, name="p")                 .fork(step_a)                 .fork([step_b1, step_b2])                 .end()
            ```

        2) Direct-style (provide `branches` list or dict):
            ```python
            composer.parallel(
                branches=[step_a, [step_b1, step_b2]],
                input_states=["query"],
                squash=True,
                name="p_direct",
            )
            ```

        Args:
            branches (list[PipelineSteps] | dict[str, PipelineSteps] | None, optional):
                Branches to execute in parallel. Each branch can be a single step or a list of steps to run
                sequentially. If omitted (builder-style), a `ParallelComposer` is returned to define forks via
                `.fork()`; if provided (direct-style), the parallel step is created and appended immediately.
                Defaults to None.
            squash (bool, optional): Whether to squash execution into a single node (async gather). If True, the
                parallel execution is represented by a single node; if False, native graph structures are used.
                Defaults to True.
            input_map (InputMapSpec | None, optional): Unified input mapping for all branches. Defaults to None.
            retry_config (RetryConfig | None, optional): Retry behavior configuration. Defaults to None, in which case
                no retry config is applied.
            error_handler (BaseStepErrorHandler | None, optional): Strategy to handle errors during execution.
                Defaults to None, in which case the default error handler is used.
            cache_store (BaseCache | None, optional): Cache store to be used for caching. Defaults to None, in which
                case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching. Defaults to
                None, in which case no cache configuration is used.
            name (str | None, optional): A unique identifier for the parallel step. Defaults to None.

        Returns:
            ParallelComposer | Self: If `branches` is omitted, returns a `ParallelComposer` builder; otherwise,
            returns the current composer after appending the constructed step.
        '''
    @overload
    def guard(self, condition: Component | Callable[[dict[str, Any]], bool], *, success_branch: BasePipelineStep | list[BasePipelineStep], failure_branch: BasePipelineStep | list[BasePipelineStep] | None = ..., input_map: InputMapSpec | None = ..., output_state: str | None = ..., retry_config: RetryConfig | None = ..., error_handler: BaseStepErrorHandler | None = ..., cache_store: BaseCache | None = ..., cache_config: dict[str, Any] | None = ..., name: str | None = ...) -> Self: ...
    @overload
    def guard(self, condition: Component | Callable[[dict[str, Any]], bool], *, success_branch: None = ..., failure_branch: BasePipelineStep | list[BasePipelineStep] | None = ..., input_map: InputMapSpec | None = ..., output_state: str | None = ..., retry_config: RetryConfig | None = ..., error_handler: BaseStepErrorHandler | None = ..., cache_store: BaseCache | None = ..., cache_config: dict[str, Any] | None = ..., name: str | None = ...) -> GuardComposer: ...
    @overload
    def toggle(self, condition: Component | Callable[[dict[str, Any]], bool] | str, *, if_branch: BasePipelineStep | list[BasePipelineStep], input_map: InputMapSpec | None = ..., output_state: str | None = ..., retry_config: RetryConfig | None = ..., error_handler: BaseStepErrorHandler | None = ..., cache_store: BaseCache | None = ..., cache_config: dict[str, Any] | None = ..., name: str | None = ...) -> Self: ...
    @overload
    def toggle(self, condition: Component | Callable[[dict[str, Any]], bool] | str, *, if_branch: None = ..., input_map: InputMapSpec | None = ..., output_state: str | None = ..., retry_config: RetryConfig | None = ..., error_handler: BaseStepErrorHandler | None = ..., cache_store: BaseCache | None = ..., cache_config: dict[str, Any] | None = ..., name: str | None = ...) -> ToggleComposer: ...
    def toggle(self, condition: Component | Callable[[dict[str, Any]], bool] | str, *, if_branch: BasePipelineStep | list[BasePipelineStep] | None = None, input_map: InputMapSpec | None = None, output_state: str | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> Self | ToggleComposer:
        """Create a toggle conditional (builder-style or direct-style).

        This method supports two usage patterns:
        1) Builder-style (no `if_branch` provided):
            ```python
            composer.toggle(condition)                 .then(enabled_steps)                 .end()
            ```

        2) Direct-style (provide `if_branch`):
            ```python
            composer.toggle(
                condition,
                if_branch=enabled_steps,
            )
            ```

        Args:
            condition (Component | Callable[[dict[str, Any]], bool] | str): The condition to evaluate.
                If a `Component`, it must return a boolean value. If a `Callable`, it must return
                a boolean value. If a `str`, it will be looked up in the merged state data.
            if_branch (BasePipelineStep | list[BasePipelineStep] | None, optional):
                Steps to execute if condition is true. If omitted (builder-style), a `ToggleComposer`
                is returned to define the branch via `.then()`; if provided (direct-style),
                the toggle step is created and appended immediately. Defaults to None, in which case
                a `ToggleComposer` is returned.
            input_map (InputMapSpec | None, optional): Unified input mapping for the condition. Defaults to None.
            output_state (str | None, optional): Optional state key to store the condition result. Defaults to None.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using GLLM Core's
                `RetryConfig`. Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Strategy to handle errors during execution.
                Defaults to None.
            cache_store (BaseCache | None, optional): Cache store to be used for caching. Defaults to None.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None.
            name (str | None, optional): A unique identifier for the conditional step. If None, a name will be
                auto-generated. Defaults to None.

        Returns:
            ToggleComposer | Self: If `if_branch` is omitted, returns a `ToggleComposer` builder; otherwise,
                returns the current composer after appending the constructed step.
        """
    def done(self) -> Pipeline:
        """Return the composed `Pipeline` instance.

        This does not build the execution graph. The graph is built when
        `Pipeline.graph` or `Pipeline.build_graph()` is accessed/called.

        Returns:
            Pipeline: The composed pipeline instance.
        """

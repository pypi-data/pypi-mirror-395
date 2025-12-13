from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec
from gllm_pipeline.pipeline.composer.composer import Composer as Composer
from gllm_pipeline.schema import PipelineSteps as PipelineSteps
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from typing import Any, Self

class ParallelComposer:
    '''Fluent builder for a parallel step.

    Usage:
        composer.parallel(name="p").fork(step_a).fork([step_b1, step_b2]).end()

    The builder collects forks as branches and constructs a `ParallelStep`
    using the functional helper `_func.parallel(...)`.
    '''
    def __init__(self, parent: Composer, *, squash: bool = True, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> None:
        """Initialize the ParallelComposer.

        Args:
            parent (Composer): The parent composer instance.
            squash (bool, optional): Whether to squash execution into a single node (async gather).
                Defaults to True.
            input_map (InputMapSpec | None, optional): Unified input mapping for all branches. Defaults to None.
            retry_config (RetryConfig | None, optional): Retry configuration. Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Error handler. Defaults to None.
            cache_store (BaseCache | None, optional): Optional cache store. Defaults to None.
            cache_config (dict[str, Any] | None, optional): Optional cache config. Defaults to None.
            name (str | None, optional): Optional name for the resulting step. Defaults to None.
        """
    def fork(self, branch: BasePipelineStep | list[BasePipelineStep]) -> Self:
        """Add a fork (branch) to execute in parallel.

        Args:
            branch (BasePipelineStep | list[BasePipelineStep]): Step(s) for this fork.

        Returns:
            Self: The builder instance for chaining.
        """
    def end(self) -> Composer:
        """Finalize and append the parallel step to the parent composer.

        Returns:
            Composer: The parent composer for continued chaining.
        """

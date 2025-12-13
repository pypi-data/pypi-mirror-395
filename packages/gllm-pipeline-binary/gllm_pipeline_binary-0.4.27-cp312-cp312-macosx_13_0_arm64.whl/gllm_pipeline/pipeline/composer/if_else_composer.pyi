from gllm_core.schema import Component as Component
from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec
from gllm_pipeline.pipeline.composer.composer import Composer as Composer
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from typing import Any, Callable, Self

class IfElseComposer:
    """Fluent builder for an if/else conditional.

    Usage:
        composer.when(cond).then(if_branch).otherwise(else_branch).end()

    After setting both branches, call `.end()` to append the conditional step and
    return back to the parent `Composer`.
    """
    def __init__(self, parent: Composer, condition: Component | Callable[[dict[str, Any]], bool], output_state: str | None = None, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> None:
        '''Initialize the IfElseComposer.

        Args:
            parent (Composer): The parent composer instance.
            condition (Component | Callable[[dict[str, Any]], bool]): The condition to evaluate.
            output_state (str | None, optional): Optional state key to store condition result. Defaults to None.
            input_map (InputMapSpec | None, optional): Unified input mapping for the condition. Defaults to None.
            retry_config (RetryConfig | None, optional): Retry configuration. Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Error handler. Defaults to None.
            cache_store (BaseCache | None, optional): Optional cache store. Defaults to None.
            cache_config (dict[str, Any] | None, optional): Optional cache config. Defaults to None.
            name (str | None, optional): Optional name for the resulting step. Defaults to None, in which case
                a name will be auto-generated with the prefix "IfElse_".
        '''
    def then(self, branch: BasePipelineStep | list[BasePipelineStep]) -> Self:
        """Define the branch to execute when the condition is true.

        Args:
            branch (BasePipelineStep | list[BasePipelineStep]): The step(s) for the true branch.

        Returns:
            Self: The builder instance for chaining.
        """
    def otherwise(self, branch: BasePipelineStep | list[BasePipelineStep]) -> Self:
        """Define the branch to execute when the condition is false.

        Args:
            branch (BasePipelineStep | list[BasePipelineStep]): The step(s) for the false branch.

        Returns:
            Self: The builder instance for chaining.
        """
    def end(self) -> Composer:
        """Finalize and append the conditional step to the parent composer.

        Returns:
            Composer: The parent composer for continued chaining.
        """

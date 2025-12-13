from gllm_core.schema import Component as Component
from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec
from gllm_pipeline.pipeline.composer.composer import Composer as Composer
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from typing import Any, Callable, Self

class SwitchComposer:
    '''Fluent builder for a switch conditional.

    Usage:
        composer.switch(cond).case("A", step_a).case("B", step_b).end()

    Optionally call `.default(...)` to set a fallback branch.
    '''
    def __init__(self, parent: Composer, condition: Component | Callable[[dict[str, Any]], str], output_state: str | None = None, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None, name: str | None = None) -> None:
        '''Initialize the SwitchComposer.

        Args:
            parent (Composer): The parent composer instance.
            condition (Component | Callable[[dict[str, Any]], str]): The condition to evaluate.
            output_state (str | None, optional): Optional state key to store condition result. Defaults to None.
            input_map (InputMapSpec | None, optional): Unified input mapping for the condition. Defaults to None.
            retry_config (RetryConfig | None, optional): Retry configuration. Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Error handler. Defaults to None.
            cache_store (BaseCache | None, optional): Optional cache store. Defaults to None.
            cache_config (dict[str, Any] | None, optional): Optional cache config. Defaults to None.
            name (str | None, optional): Optional name for the resulting step. Defaults to None, in which case
                a name will be auto-generated with the prefix "Switch_".
        '''
    def case(self, key: str, branch: BasePipelineStep | list[BasePipelineStep]) -> Self:
        """Add a case branch.

        Args:
            key (str): Case key to match against condition result.
            branch (BasePipelineStep | list[BasePipelineStep]): Step(s) to execute for this case.

        Returns:
            Self: The builder instance for chaining.
        """
    def default(self, branch: BasePipelineStep | list[BasePipelineStep]) -> Self:
        """Set the default branch for unmatched cases.

        Args:
            branch (BasePipelineStep | list[BasePipelineStep]): Default fallback branch.

        Returns:
            Self: The builder instance for chaining.
        """
    def end(self) -> Composer:
        """Finalize and append the switch conditional to the parent composer.

        Returns:
            Composer: The parent composer for continued chaining.
        """

from gllm_core.utils.retry import RetryConfig as RetryConfig
from gllm_datastore.cache.cache import BaseCache as BaseCache
from gllm_pipeline.alias import InputMapSpec as InputMapSpec
from gllm_pipeline.steps.conditional_step import ConditionType as ConditionType, ConditionalStep as ConditionalStep, DEFAULT_BRANCH as DEFAULT_BRANCH
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from gllm_pipeline.steps.step_error_handler.step_error_handler import BaseStepErrorHandler as BaseStepErrorHandler
from gllm_pipeline.steps.terminator_step import TerminatorStep as TerminatorStep
from typing import Any

class GuardStep(ConditionalStep):
    '''A conditional step that can terminate pipeline execution if a condition is not met.

    This step evaluates a condition and either:
    1. Continues execution through the success_branch if the condition is True
    2. Executes the failure_branch and terminates if the condition is False

    Example:
        ```python
        pipeline = (
            step_a
            | GuardStep(
                name="auth_check",
                condition=lambda x: x["is_authenticated"],
                success_branch=step_b,
                failure_branch=error_handling_step,
            )
            | step_c
        )
        ```

    Attributes:
        name (str): A unique identifier for this pipeline step.
        condition (ConditionType): The condition to evaluate.
        input_map (dict[str, str | Any] | None): Unified input map.
        success_branch (BasePipelineStep | list[BasePipelineStep]): Steps to execute if condition is True.
        failure_branch (BasePipelineStep | list[BasePipelineStep] | None): Steps to execute if condition is False.
            If None, pipeline terminates immediately on False condition.
        retry_policy (RetryPolicy | None): Configuration for retry behavior using LangGraph\'s RetryPolicy.
    '''
    def __init__(self, name: str, condition: ConditionType, success_branch: BasePipelineStep | list[BasePipelineStep], failure_branch: BasePipelineStep | list[BasePipelineStep] | None = None, input_state_map: dict[str, str] | None = None, output_state: str | None = None, runtime_config_map: dict[str, str] | None = None, fixed_args: dict[str, Any] | None = None, input_map: InputMapSpec | None = None, retry_config: RetryConfig | None = None, error_handler: BaseStepErrorHandler | None = None, cache_store: BaseCache | None = None, cache_config: dict[str, Any] | None = None) -> None:
        '''Initializes a new GuardStep.

        Args:
            name (str): A unique identifier for this pipeline step.
            condition (ConditionType): The condition to evaluate.
            success_branch (BasePipelineStep | list[BasePipelineStep]): Steps to execute if condition is True.
            failure_branch (BasePipelineStep | list[BasePipelineStep] | None, optional): Steps to execute if
                condition is False. If None, pipeline terminates immediately. Defaults to None.
            input_state_map (dict[str, str] | None, optional): Mapping of condition input arguments to
                pipeline state keys. Defaults to None.
            output_state (str | None, optional): Key to store the condition result in the pipeline state.
                Defaults to None.
            runtime_config_map (dict[str, str] | None, optional): Mapping of condition input arguments to runtime
                configuration keys. Defaults to None.
            fixed_args (dict[str, Any] | None, optional): Fixed arguments to be passed to the condition.
                Defaults to None.
            input_map (InputMapSpec | None, optional):
                Unified input map. Can be a dict (arg -> str|Val) or a list with elements:
                1. str for identity mapping
                2. dict[str, str] for state/config mapping
                3. dict[str, Val] for fixed args.
                Defaults to None.
            error_handler (BaseStepErrorHandler | None, optional): Strategy to handle errors during execution.
                Defaults to None, in which case the RaiseStepErrorHandler is used.
            retry_config (RetryConfig | None, optional): Configuration for retry behavior using
                GLLM Core\'s RetryConfig. Defaults to None, in which case no retry config is applied.
            cache_store ("BaseCache" | None, optional): Cache store to be used for caching.
                Defaults to None, in which case no cache store is used.
            cache_config (dict[str, Any] | None, optional): Cache configuration to be used for caching.
                Defaults to None, in which case no cache configuration is used.
        '''

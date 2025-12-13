from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep
from langchain_core.runnables import RunnableConfig as RunnableConfig
from langgraph.runtime import Runtime as Runtime
from pydantic import BaseModel as BaseModel
from typing import Any

class NoOpStep(BasePipelineStep):
    '''A step that does nothing.

    This step is useful when you want to add a step that does not perform any processing.
    For example, you can use this step to implement a toggle pattern for a certain component.

    Example:
    ```python
    pipeline = (
        step_a
        | ConditionalStep(
            name="branch",
            branches={
                "execute": step_b,
                "continue": NoOpStep("no_op")
            },
            condition=lambda x: "execute" if x["should_execute"] else "continue"
        )
        | step_c
    )
    ```

    Attributes:
        name (str): A unique identifier for this pipeline step.
    '''
    async def execute(self, state: dict[str, Any], runtime: Runtime[dict[str, Any] | BaseModel], config: RunnableConfig | None = None) -> None:
        """Executes this step, which does nothing.

        Args:
            state (dict[str, Any]): The current state of the pipeline.
            runtime (Runtime[dict[str, Any] | BaseModel]): Runtime information for this step's execution.
            config (RunnableConfig | None, optional): The runnable configuration. Defaults to None.

        Returns:
            None: This step does not modify the pipeline state.
        """

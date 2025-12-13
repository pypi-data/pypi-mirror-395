import abc
from _typeshed import Incomplete
from gllm_pipeline.alias import PipelineSteps as PipelineSteps
from gllm_pipeline.exclusions import ExclusionSet as ExclusionSet
from gllm_pipeline.steps.composite_step import BaseCompositeStep as BaseCompositeStep
from gllm_pipeline.steps.pipeline_step import BasePipelineStep as BasePipelineStep

class BranchingStep(BaseCompositeStep, metaclass=abc.ABCMeta):
    """Mixin-like base for composites that maintain named branches.

    Attributes:
        branches (dict[str, PipelineSteps]): The branches to execute in parallel.
    """
    branches: dict[str, PipelineSteps]
    is_excluded: Incomplete
    def apply_exclusions(self, exclusions: ExclusionSet) -> None:
        """Apply exclusions to this branching step and its children.

        Marks self excluded, lets subclass perform internal structural changes,
        then propagates exclusions to children per branch.

        Args:
            exclusions (ExclusionSet): The exclusion set to apply.
        """

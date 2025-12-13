from _typeshed import Incomplete
from gllm_pipeline.exclusions.exclusion_set import ExclusionSet as ExclusionSet
from gllm_pipeline.pipeline.pipeline import Pipeline as Pipeline

class ExclusionManager:
    """Exclusion manager for managing exclusions in a pipeline.

    This class provides a high-level interface for managing step exclusions in a pipeline.
    It handles the creation of exclusion sets, application to pipeline steps, and graph
    rebuilding when exclusions change.

    Attributes:
        pipeline (Pipeline): The pipeline instance to manage exclusions for.
    """
    pipeline: Incomplete
    def __init__(self, pipeline: Pipeline) -> None:
        """Initialize the exclusion manager.

        Args:
            pipeline: The pipeline instance to manage exclusions for.
        """
    def exclude(self, *paths: str) -> None:
        """Exclude one or more paths from execution.

        This method creates an exclusion set from the provided paths, applies the
        exclusions to all pipeline steps, updates the pipeline's exclusion state,
        and rebuilds the graph to reflect the new structure.

        Notes:
            This operation REPLACES the current exclusion set with the provided paths
            (it is not additive).

        Args:
            *paths: Variable number of dot-notation paths to exclude.
        """
    def include(self, *paths: str) -> None:
        """Include (un-exclude) one or more paths.

        This method removes the specified paths from the current exclusions by
        getting the current exclusion list, filtering out the specified paths,
        and applying the remaining exclusions.

        Notes:
            1. Mutually exclusive with `exclude` in intent: `include` removes from
               the existing exclusion set, whereas `exclude` replaces the entire set.
            2. If there are no current exclusions, calling `include` is a no-op.

        Args:
            *paths: Variable number of dot-notation paths to include (un-exclude).
        """
    def clear(self) -> None:
        """Clear all exclusions.

        This method removes all current exclusions from the pipeline, effectively
        including all steps in execution.
        """
    def list_excluded(self) -> list[str]:
        """List currently excluded steps.

        This method iterates through all pipeline steps and returns the names
        of steps that are currently marked as excluded.

        Returns:
            list[str]: List of step names that are currently excluded.
        """
    def get_current_exclusions(self) -> list[str]:
        """Get current exclusion paths.

        This method returns the list of paths that are currently excluded
        in the pipeline. If no exclusions are set, returns an empty list.

        Returns:
            list[str]: List of currently excluded paths.
        """

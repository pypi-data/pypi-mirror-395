from pydantic import BaseModel

class ExclusionSet(BaseModel):
    """Simple set of excluded step paths.

    This class manages a collection of step paths that should be excluded from execution.
    It provides methods to check if paths are excluded and to extract child exclusions
    for hierarchical step structures.

    Attributes:
        excluded_paths (set[str]): The set of excluded step paths.
    """
    excluded_paths: set[str]
    @classmethod
    def from_list(cls, paths: list[str]) -> ExclusionSet:
        """Create exclusion set from list of paths.

        Args:
            paths: List of dot-notation paths to exclude.

        Returns:
            ExclusionSet: New exclusion set containing the provided paths.
        """
    def is_excluded(self, path: str) -> bool:
        """Check if a path is excluded.

        Args:
            path: The step path to check for exclusion.

        Returns:
            bool: True if the path is excluded, False otherwise.
        """
    def get_child_exclusions(self, parent_path: str) -> ExclusionSet:
        '''Get exclusions for children of a parent path.

        This method extracts all exclusions that apply to children of the specified
        parent path. For example, if the exclusion set contains "parent.child1" and
        "parent.child2.grandchild", calling this method with "parent" will return
        an ExclusionSet containing "child1" and "child2.grandchild".

        Args:
            parent_path: The parent path to get child exclusions for.

        Returns:
            ExclusionSet: New exclusion set containing only child exclusions.
        '''

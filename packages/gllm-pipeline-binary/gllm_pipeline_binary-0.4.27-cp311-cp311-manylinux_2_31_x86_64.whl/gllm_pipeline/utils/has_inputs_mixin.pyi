from _typeshed import Incomplete
from gllm_pipeline.alias import PipelineState as PipelineState
from gllm_pipeline.types import Val as Val
from gllm_pipeline.utils.input_map import shallow_dump as shallow_dump
from langgraph.runtime import Runtime as Runtime
from pydantic import BaseModel as BaseModel
from typing import Any

class HasInputsMixin:
    '''Mixin class for steps that consume a unified input_map.

    The input_map maps argument names to either a state/config key (str) or a fixed value (Val).
    Resolution semantics:
    1. For str specs: read from state first; if missing, fall back to config["configurable"].
    2. For Val specs: use the literal value.

    Attributes:
        input_map (dict[str, str | Val]): Mapping of argument names to either a state/config key (str)
            or a fixed value (Val).
    '''
    input_map: Incomplete
    def __init__(self, input_map: dict[str, str | Val] | list[str | dict[str, str] | dict[str, Val]] | None = None) -> None:
        '''Initialize with a unified input_map.

        Args:
            input_map (dict[str, str | Val] | list[str | dict[str, str] | dict[str, Val]] | None):
                Mapping of argument names to either a state/config key (str) or a fixed value (Val).
                Also accepts a list form for ergonomics:
                1. str: identity mapping ("key" -> {"key": "key"})
                2. dict[str, str]: explicit mapping to state/config key
                3. dict[str, Val]: fixed/literal value
                Defaults to None, in which case an empty mapping is used.
        '''
    @classmethod
    def from_legacy_map(cls, input_state_map: dict[str, str] | None, runtime_config_map: dict[str, str] | None, fixed_args: dict[str, Any] | None) -> dict[str, str | Val]:
        """Synthesize an input_map from state/config mappings and fixed args.

        Precedence: fixed_args > runtime_config_map > input_state_map.

        Args:
            input_state_map (dict[str, str] | None, optional): Mapping of argument names to state keys.
                Defaults to None, in which case an empty mapping is used.
            runtime_config_map (dict[str, str] | None, optional): Mapping of argument names to runtime configuration
                keys. Defaults to None, in which case an empty mapping is used.
            fixed_args (dict[str, Any] | None, optional): Mapping of argument names to fixed values.
                Defaults to None, in which case an empty mapping is used.

        Returns:
            dict[str, str | Val]: The synthesized input_map.
        """

from _typeshed import Incomplete
from gllm_pipeline.router.router import BaseRouter as BaseRouter
from pydantic import BaseModel

class RouterSplitRule(BaseModel):
    '''Configuration class for defining input string splitting rules in rule-based router operations.

    Attributes:
        splitter (list[str]): A list of string delimiters used to split the input string. Defaults to [" "].
        beg_index (int | None, optional): Optional beginning index of the portion of the split result to keep.
            If None, the split result will be kept from the first element. Defaults to None.
        end_index (int | None, optional): Optional ending index of the portion of the split result to keep.
            If None, the split result will be kept until the last element. Defaults to None.
    '''
    splitter: list[str]
    beg_index: int | None
    end_index: int | None

class RouterRule(BaseModel):
    """Configuration class for defining keyword matching rules in rule-based router operations.

    Attributes:
        keywords (list[str]): A list of keywords to match against the input string.
        allow_substring (bool, optional): If True, allows matching if a keyword is a substring of the input.
            If False, requires an exact match between a keyword and either the full input or any of its split parts.
            Defaults to True.
        case_sensitive (bool, optional): If True, keyword matching will be case-sensitive. Defaults to True.
        alphanumeric_only (bool, optional): If True, only alphanumeric and whitespace characters will be considered
            during matching. Defaults to True.
        split_rule (list[RouterSplitRule] | None, optional): A list of `RouterSplitRule` objects that define how to
            split the input string before matching. If multiple are provided, the splits will be done sequentially.
            If None, no splitting will be applied. Defaults to None.
    """
    keywords: list[str]
    allow_substring: bool
    case_sensitive: bool
    alphanumeric_only: bool
    split_rule: list[RouterSplitRule] | None

class RouterRuleset(BaseModel):
    """Configuration class for defining a set of rules in rule-based router operations.

    Attributes:
        rules (list[RouterRule]): A list of `RouterRule` objects that define individual routing rules.
        match_all (bool, optional): If True, all rules must be matched for the ruleset to return True. If False,
            matching any rule will result in the ruleset returning True. Defaults to True.
    """
    rules: list[RouterRule]
    match_all: bool

class RuleBasedRouter(BaseRouter):
    """A rule-based router that directs the input text to an appropriate route based on a set of rules.

    The `RuleBasedRouter` routes incoming input text to different paths by evaluating a set of rules encapsulated in
    `RouterRuleset` objects. Each ruleset consists of multiple `RouterRule` objects, and the router determines which
    route to take based on the input text and the rules defined in the ruleset.

    If `match_all` is True in a `RouterRuleset`, all rules in that ruleset must match the input text for the
    associated route to be selected. If False, matching any rule in the ruleset will cause that route to be selected.
    If no match is found, the router defaults to the `default_route`.

    Attributes:
        ruleset_map (dict[str, RouterRuleset]): A mapping of route names to their corresponding rulesets.
        default_route (str): The default route to be taken if no ruleset matches the input text.
        valid_routes (set[str]): A set of valid routes that the router can direct to.
    """
    ruleset_map: Incomplete
    def __init__(self, ruleset_map: dict[str, RouterRuleset], default_route: str, valid_routes: set[str]) -> None:
        """Initializes a new instance of the RuleBasedRouter class.

        Args:
            ruleset_map (dict[str, RouterRuleset]): A mapping of route names to their corresponding rulesets.
            default_route (str): The default route to be taken if no ruleset matches the input text.
            valid_routes (set[str]): A set of valid routes for the router.

        Raises:
            ValueError:
                1. If the `ruleset_map` contains routes that are not in the set of valid routes.
                2. If the provided default route is not in the set of valid routes.
        """

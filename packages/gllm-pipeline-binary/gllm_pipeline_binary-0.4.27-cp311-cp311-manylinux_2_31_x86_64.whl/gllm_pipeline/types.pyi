from dataclasses import dataclass

@dataclass(frozen=True)
class Val:
    """A value wrapper that represents a fixed/literal input.

    Attributes:
        value (object): The literal value of the input.
    """
    value: object

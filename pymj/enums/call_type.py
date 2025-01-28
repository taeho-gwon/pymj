from enum import Enum, auto


class CallType(Enum):
    """Represents the call type."""

    CHII = auto()
    PON = auto()
    CONCEALED_KAN = auto()
    BIG_MELDED_KAN = auto()
    SMALL_MELDED_KAN = auto()

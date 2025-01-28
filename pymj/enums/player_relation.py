from enum import Enum, auto


class PlayerRelation(Enum):
    """Represents for player relation."""

    PREV = auto()
    ACROSS = auto()
    NEXT = auto()
    SELF = auto()

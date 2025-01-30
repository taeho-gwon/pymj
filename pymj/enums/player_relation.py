from enum import Enum, auto


class PlayerRelation(Enum):
    """Relative positions between Mahjong players at the table.

    Attributes:
        PREV: Counter-clockwise player (kamicha/上家).
        ACROSS: Opposite player (toimen/対面).
        NEXT: Clockwise player (shimocha/下家).
        SELF: Player's own position.

    """

    PREV = auto()
    ACROSS = auto()
    NEXT = auto()
    SELF = auto()

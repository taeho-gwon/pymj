from enum import Enum, auto


class DivisionPartType(Enum):
    """Define types of tile combinations that can form a valid division in a hand.

    Attributes:
        HEAD: A pair of identical tiles.
        SEQUENCE: Three consecutive tiles of the same suit.
        TRIPLE: Three identical tiles.
        QUAD: Four identical tiles.
        THIRTEEN_ORPHANS: Special case for thirteen_orphans

    """

    HEAD = auto()
    SEQUENCE = auto()
    TRIPLE = auto()
    QUAD = auto()
    THIRTEEN_ORPHANS = auto()

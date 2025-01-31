from enum import Enum, auto


class WaitType(Enum):
    """Define types of waiting patterns for completing hand.

    Attributes:
        SINGLE_WAIT: Wait for a specific tile for a complete hand.
        CLOSED_WAIT: Wait for a tile between two consecutive tiles.
        EDGE_WAIT : Wait for a tile at the edge of a sequence.
        DUAL_PON_WAIT: Wait for either of two tiles to form a triplet.
        SIDE_WAIT: Wait for a tile at the side of two consecutive tiles.
        ETC: Other miscellaneous waiting patterns.

    """

    SINGLE_WAIT = auto()
    CLOSED_WAIT = auto()
    EDGE_WAIT = auto()
    DUAL_PON_WAIT = auto()
    SIDE_WAIT = auto()
    ETC = auto()

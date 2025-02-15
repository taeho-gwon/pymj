from enum import Enum, auto


class DivisionPartState(Enum):
    """Define states indicating how a part of hand division was formed.

    Attributes:
        CONCEALED: The division part contains only self-drawn tiles.
        RON: The division part includes the winning tile from opponent's discard.
        OPENED: The division part was formed by calling opponent's discarded tile.

    """

    CONCEALED = auto()
    RON = auto()
    OPENED = auto()

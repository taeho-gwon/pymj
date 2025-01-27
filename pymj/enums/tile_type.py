from enum import Enum, auto


class TileType(Enum):
    """Represents the main types of Mahjong tiles."""

    MAN = auto()
    PIN = auto()
    SOU = auto()
    WIND = auto()
    DRAGON = auto()
    ETC = auto()

from enum import Enum, auto


class TileType(Enum):
    """Enum class for Tile Type (etc. manzu, pinzu, souzu...)."""

    MAN = auto()
    PIN = auto()
    SOU = auto()
    WIND = auto()
    DRAGON = auto()
    ETC = auto()

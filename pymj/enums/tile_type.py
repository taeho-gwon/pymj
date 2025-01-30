from enum import Enum, auto


class TileType(Enum):
    """Defines the basic types of tiles used in Mahjong.

    Represents the main categories of tiles found in the game, including numbered
    suits, honor tiles, and bonus tiles.

    Attributes:
        MAN: Character tiles numbered from 1 to 9.
        PIN: Circle/Dot tiles numbered from 1 to 9.
        SOU: Bamboo tiles numbered from 1 to 9.
        WIND: Directional tiles representing East, South, West, and North.
        DRAGON: Honor tiles including White, Green, and Red dragons.
        ETC: Supplementary tiles such as flowers and seasons.

    """

    MAN = auto()
    PIN = auto()
    SOU = auto()
    WIND = auto()
    DRAGON = auto()
    ETC = auto()

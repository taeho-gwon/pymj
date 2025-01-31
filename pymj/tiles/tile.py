from dataclasses import dataclass

from pymj.enums.tile_type import TileType


@dataclass(frozen=True)
class Tile:
    """Represents a single Mahjong tile with its type and numerical value.

    A tile consists of two main properties: a type (like Man, Pin, etc.) and a
    numerical value that identifies its rank within that type.

    Attributes:
        tile_type (TileType): The category of the tile
        value (int): The numerical rank of the tile:
            - Man/Pin/Sou: 1-9
            - Wind: East(1), South(2), West(3), North(4)
            - Dragon: White(1), Green(2), Red(3)
            - Etc: any value for special tiles

    Raises:
        ValueError: If value is invalid for the given tile_type:
            - Man/Pin/Sou: must be 1-9
            - Wind: must be 1-4
            - Dragon: must be 1-3

    Examples:
        >>> five_man = Tile(tile_type=TileType.MAN, value=5)  # 5 of Characters
        >>> east_wind = Tile(tile_type=TileType.WIND, value=1)  # East Wind

    """

    tile_type: TileType
    value: int

    def __post_init__(self) -> None:
        max_tile_map = {
            TileType.MAN: 9,
            TileType.PIN: 9,
            TileType.SOU: 9,
            TileType.WIND: 4,
            TileType.DRAGON: 3,
        }
        if self.tile_type is not TileType.ETC and not (
            1 <= self.value <= max_tile_map[self.tile_type]
        ):
            raise ValueError

    def __repr__(self) -> str:
        return f"{self.tile_type.name} {self.value}"


class Tiles:
    """Define tile categories and special tile combinations used in gameplay.

    Contains class variables representing different tile categories like numbered tiles,
    honor tiles, and special combinations such as terminals and sequence patterns.

    Attributes:
        MANS: Character tile indices (0-8).
        PINS: Circle tile indices (9-17).
        SOUS: Bamboo tile indices (18-26).
        WINDS: Wind tile indices (27-30).
        DRAGONS: Dragon tile indices (31-33).
        NUMBERS: All number tiles combined (MANS + PINS + SOUS).
        HONORS: All honor tiles combined (WINDS + DRAGONS).
        ALL : Standard set of all tiles used in gameplay.
        TERMINALS: Terminal number tile indices (1 and 9).
        TERMINALS_AND_HONORS: Terminal and honor tiles combined.
        SEQUENCE_STARTS: Indices that can start a complete sequence (1-7).
        PARTIAL_SEQUENCE_STARTS: Indices that can start partial sequence (1-8).
        SIMPLES: Simple number tile indices (2-8).
        GREENS: Indices for tiles used in all-green combinations.

    """

    MANS = list(range(9))
    PINS = list(range(9, 18))
    SOUS = list(range(18, 27))
    WINDS = [27, 28, 29, 30]
    DRAGONS = [31, 32, 33]

    NUMBERS = MANS + PINS + SOUS
    HONORS = WINDS + DRAGONS
    ALL = NUMBERS + HONORS

    TERMINALS = [MANS[0], MANS[8], PINS[0], PINS[8], SOUS[0], SOUS[8]]
    TERMINALS_AND_HONORS = TERMINALS + HONORS

    SEQUENCE_STARTS = MANS[0:7] + PINS[0:7] + SOUS[0:7]
    PARTIAL_SEQUENCE_STARTS = MANS[0:8] + PINS[0:8] + SOUS[0:8]

    SIMPLES = MANS[1:8] + PINS[1:8] + SOUS[1:8]
    GREENS = [SOUS[1], SOUS[2], SOUS[3], SOUS[5], SOUS[7], DRAGONS[1]]

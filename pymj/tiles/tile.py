from dataclasses import dataclass

from pymj.enums.tile_type import TileType


@dataclass(frozen=True)
class Tile:
    """Represents a single Mahjong tile with its type and numerical value.

    A tile consists of two main properties: a type (like Man, Pin, etc.) and a
    numerical value that identifies its rank within that type.

    Args:
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

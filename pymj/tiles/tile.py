from dataclasses import dataclass

from pymj.enums.tile_type import TileType


@dataclass(frozen=True)
class Tile:
    """A representation of a mahjong tile with its type and value.

    Each tile has a specific type and a numerical
    value representing its rank or number within that type.

    Attributes:
        tile_type (TileType): The type or suit of the Mahjong tile
            (e.g., man, pin, sou, wind, dragon, etc.(like flower).
        value (int): The numerical value of the tile within its type:
            - Number tiles (MAN/PIN/SOU): Values from 1 to 9
            - Wind tiles: East(1), South(2), West(3), North(4)
            - Dragon tiles: White(1), Green(2), Red(3)
            - ETC types: special tiles
    Raises:
        ValueError: If the provided value is outside the valid range for the
                   specified tile type. For example:
                   - Values > 9 for number tiles (MAN/PIN/SOU)
                   - Values > 4 for wind tiles
                   - Values > 3 for dragon tiles

    Examples:
        Creating a Five of Characters (5 Man):
        >>> five_man = Tile(tile_type=TileType.MAN, value=5)

        Creating an East Wind tile:
        >>> east_wind = Tile(tile_type=TileType.WIND, value=1)

        Creating a White Dragon tile:
        >>> white_dragon = Tile(tile_type=TileType.DRAGON, value=1)

        This will raise a ValueError (invalid value for PIN type):
        >>> invalid_tile = Tile(tile_type=TileType.PIN, value=10)

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

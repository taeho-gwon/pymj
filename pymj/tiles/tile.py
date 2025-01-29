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
        value (int): The numerical value of the tile within its type
            (typically ranges from 1 to 9 for number tiles,
            wind : east = 1, south = 2, west = 3, north = 4,
            dragon : white = 1, green = 2, red = 3).

    Example:
        # Creating a tile representing the 3pin
        tile = Tile(tile_type=TileType.PIN, value=3)

        # Creating a tile representing the East wind
        wind_tile = Tile(tile_type=TileType.WIND, value=1)

    """

    tile_type: TileType
    value: int

    def __repr__(self) -> str:
        return f"{self.tile_type.name} {self.value}"

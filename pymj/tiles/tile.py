from dataclasses import dataclass

from pymj.enums.tile_type import TileType


@dataclass(frozen=True, order=True)
class Tile:
    """Represents an individual Mahjong tile in the game.

    This class captures the essential characteristics of a Mahjong tile,
    including its type, value.

    Attributes
    ----------
        tile_type (TileType): The category of the tile (number, honor, wind)
        value (int): The numeric value or specific type of the tile

    """

    tile_type: TileType
    value: int

    def __repr__(self) -> str:
        """Provide a string representation of the tile.

        Returns
        -------
            str: A descriptive string of the tile

        """
        return f"{self.tile_type.name} {self.value}"

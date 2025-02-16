from __future__ import annotations

from typing import cast

from pymj.enums.tile_type import TileType
from pymj.tiles.tile import Tile


class TileIndex(int):
    """Represents a valid mahjong tile index.

    This class ensures that tile indices are always valid (0-33) and provides
    helpful methods for working with tile indices in a type-safe manner.

    Attributes:
        value (int): The underlying tile index value (0-33)
            - 0-8   : Man
            - 9-17  : Pin
            - 18-26 : Sou
            - 27-30 : Wind tiles
            - 31-33 : Dragon tiles

    """

    MAX_INDEX = 33
    SIZE = 34

    def __new__(cls, value: int) -> TileIndex:
        """Validate the tile index after initialization.

        Raises:
            ValueError: If value is not between 0 and 33

        """
        if not 0 <= value <= TileIndex.SIZE:
            raise ValueError
        return cast(TileIndex, super().__new__(cls, value))

    @staticmethod
    def create_from_tile(tile: Tile) -> TileIndex:
        """Convert a mahjong tile to its unique numerical index.

        Args:
            tile (Tile): A Tile object representing a mahjong tile.

        Returns:
            int: The unique index (0-33) corresponding to the input tile.
                - Man                          : 1-9 → 0-8
                - Pin                          : 1-9 → 9-17
                - Sou                          : 1-9 → 18-26
                - Wind (East/South/West/North) : 1-4 → 27-30
                - Dragon (White/Green/Red)     : 1-3 → 31-33


        Raises:
            ValueError: If the type of the tile is ETC

        """
        if tile.tile_type is TileType.ETC:
            raise ValueError

        base_index = {
            TileType.MAN: 0,
            TileType.PIN: 9,
            TileType.SOU: 18,
            TileType.WIND: 27,
            TileType.DRAGON: 31,
        }
        return TileIndex(base_index[tile.tile_type] + (tile.value - 1))

    def __add__(self, other: int) -> TileIndex:
        return TileIndex(int(self) + other)

    def __sub__(self, other: int) -> TileIndex:
        return TileIndex(int(self) - other)

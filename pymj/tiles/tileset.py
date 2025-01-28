from itertools import repeat
from typing import Iterable

from pymj.enums.tile_type import TileType
from pymj.tiles.tile import Tile


class Tileset:
    """Manages the complete set of Mahjong tiles."""

    def __init__(self) -> None:
        """Initialize the complete Mahjong tileset."""
        self._all_tiles: list[Tile] = list(self._initialize_all_tiles())

    @staticmethod
    def _create_one_tile(tile: Tile, tile_cnt: int) -> Iterable[Tile]:
        yield from repeat(tile, tile_cnt)

    @staticmethod
    def _create_one_type(
        tile_type: TileType, values: Iterable[int], tile_cnt: int
    ) -> Iterable[Tile]:
        for value in values:
            yield from Tileset._create_one_tile(Tile(tile_type, value), tile_cnt)

    @staticmethod
    def _initialize_all_tiles() -> Iterable[Tile]:
        tile_max_value_dict: dict[TileType, int] = {
            TileType.MAN: 9,
            TileType.PIN: 9,
            TileType.SOU: 9,
            TileType.WIND: 4,
            TileType.DRAGON: 3,
        }

        for tile_type, max_value in tile_max_value_dict.items():
            yield from Tileset._create_one_type(tile_type, range(1, max_value + 1), 4)

    def get_all_tiles_iter(self) -> Iterable[Tile]:
        """Return tileset iterable."""
        yield from self._all_tiles

    def get_all_tiles(self) -> list[Tile]:
        """Return shallow copy of tileset list."""
        return self._all_tiles[:]

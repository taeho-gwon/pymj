from pymj.enums.tile_type import TileType
from pymj.tiles.tile import Tile


class TileMapping:
    """Handles mapping between tiles and indices."""

    @staticmethod
    def tile_to_index(tile: Tile) -> int:
        """Convert a tile to its unique index."""
        base_index = {
            TileType.MAN: 0,
            TileType.PIN: 9,
            TileType.SOU: 18,
            TileType.WIND: 27,
            TileType.DRAGON: 31,
        }
        return base_index[tile.tile_type] + (tile.value - 1)

    @staticmethod
    def index_to_tile(index: int) -> Tile:
        """Convert an index to its corresponding tile."""
        if not 0 <= index < 34:
            raise ValueError

        if 0 <= index <= 8:
            return Tile(TileType.MAN, index + 1)
        elif 9 <= index <= 17:
            return Tile(TileType.PIN, index - 8)
        elif 18 <= index <= 26:
            return Tile(TileType.SOU, index - 17)
        elif 27 <= index <= 30:
            return Tile(TileType.WIND, index - 26)
        else:  # 31-33
            return Tile(TileType.DRAGON, index - 30)

from pymj.enums.tile_type import TileType
from pymj.tiles.tile import Tile


class TileMapping:
    """Maps mahjong tiles to numerical indices and vice versa.

    This class provides static methods to convert
    between Tile objects and their corresponding numerical indices (0-33).

    The mapping follows this pattern:
    - 0-8   : Man
    - 9-17  : Pin
    - 18-26 : Sou
    - 27-30 : Wind
    - 31-33 : Dragon

    The class ensures consistent mapping across the entire mahjong game implementation.
    """

    @staticmethod
    def tile_to_index(tile: Tile) -> int:
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
        return base_index[tile.tile_type] + (tile.value - 1)

    @staticmethod
    def index_to_tile(index: int) -> Tile:
        """Convert a numerical index back to its corresponding mahjong tile.

        Args:
            index (int): The numerical index (0-33) of a mahjong tile.

        Returns:
            Tile: The Tile object corresponding to the input index.

        Raises:
            ValueError: If the index is not within the valid range [0, 33].

        """
        if 0 <= index <= 8:
            return Tile(TileType.MAN, index + 1)
        elif 9 <= index <= 17:
            return Tile(TileType.PIN, index - 8)
        elif 18 <= index <= 26:
            return Tile(TileType.SOU, index - 17)
        elif 27 <= index <= 30:
            return Tile(TileType.WIND, index - 26)
        elif 31 <= index <= 33:
            return Tile(TileType.DRAGON, index - 30)
        else:
            raise ValueError

from pymj.tiles.call import Call
from pymj.tiles.tile import Tile


class Hand:
    """Represents a hand with in the game.

    This class manage concealed tiles, calls, and drawn_tile.
    Not validating for 14 tile_count or 4 tile max stuff.
    """

    def __init__(self) -> None:
        """Initialize hand class."""
        self.tiles: list[Tile] = []
        self.calls: list[Call] = []
        self._drawn_tile: Tile | None = None

    @property
    def drawn_tile(self) -> Tile | None:
        """Getter for self._drawn_tile."""
        return self._drawn_tile

    def draw_tile(self, tile: Tile) -> None:
        """Add a tile at drawn_tile.

        Args:
        ----
            tile: drawn tile

        Raises:
        ------
            Raise ValueError if drawn_tile already exists.

        """
        if self.drawn_tile:
            raise ValueError

        self._drawn_tile = tile

    def discard_tile(self, index: int = -1) -> Tile:
        """Discard a tile from given index.

        If index is -1, tsumogiri(discard drawn tile).

        Args:
        ----
            index: index of tile want to discard

        Raises:
        ------
            Raise ValueError if drawn_tile doesn't exist and index is -1.
            Raise ValueError if tile index is invalid.

        """
        if index == -1:
            if self.drawn_tile is None:
                raise ValueError

            temp = self.drawn_tile
            self._drawn_tile = None
            return temp

        else:
            try:
                return self.tiles.pop(index)
            except IndexError:
                raise ValueError from None

    def append_drawn_tile(self) -> None:
        """Put drawn tile in the tile list."""
        if self._drawn_tile:
            self.tiles.append(self._drawn_tile)
            self._drawn_tile = None

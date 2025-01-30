from pymj.tiles.call import Call
from pymj.tiles.tile import Tile


class Hand:
    """A class representing a player's hand.

    This class manages a player's hand,
    including concealed tiles, and the most recently drawn tile.
    The class provides basic hand management operations.

    Attributes:
        tiles (list[Tile]): List of concealed tiles in hand.
        calls (list[Call]): List of calls (revealed combinations).
        _drawn_tile (Tile | None): The most recently drawn tile, if any.

    """

    def __init__(self) -> None:
        """Initialize hand class."""
        self.tiles: list[Tile] = []
        self.calls: list[Call] = []
        self._drawn_tile: Tile | None = None

    @property
    def drawn_tile(self) -> Tile | None:
        """Get the most recently drawn tile.

        Returns:
            Tile | None: The most recently drawn tile.
                None if no tile has been drawn.

        """
        return self._drawn_tile

    def draw_tile(self, tile: Tile) -> None:
        """Draw a new tile into the hand.

        Places a new tile in the drawn tile position. This represents drawing
        a tile during a player's turn.

        Args:
            tile (Tile): The tile to be drawn.

        Raises:
            ValueError: If there is already a drawn tile in hand.

        """
        if self.drawn_tile:
            raise ValueError

        self._drawn_tile = tile

    def discard_tile(self, index: int = -1) -> Tile:
        """Discard a tile from the hand.

        Removes and returns a tile from either the drawn tile position or the main hand.
        When index is -1, performs tsumogiri (discards the drawn tile).

        Args:
            index (int, optional): Index of tile to discard from main hand.
                Defaults to -1 for tsumogiri.

        Returns:
            Tile: The discarded tile.

        Raises:
            ValueError: If trying to perform tsumogiri with no drawn tile,
                or if the specified index is invalid.

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
        """Add the drawn tile to the main hand.

        Moves the currently drawn tile to the main hand (tiles list) and
        clears the drawn tile position.
        """
        if self._drawn_tile:
            self.tiles.append(self._drawn_tile)
            self._drawn_tile = None

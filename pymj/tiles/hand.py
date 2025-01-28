from pymj.enums.call_type import CallType
from pymj.enums.player_relation import PlayerRelation
from pymj.tiles.call import Call
from pymj.tiles.tile import Tile


class Hand:
    """Represents a hand with in the game.

    This class manage concealed tiles, calls, and drawn_tile.
    Not validating for 14 tile_count or 4 tile max stuff.
    """

    def __init__(self) -> None:
        """Initialize hand class."""
        self._tiles: list[Tile] = []
        self._calls: list[Call] = []
        self._drawn_tile: Tile | None = None

    def add_tile(self, tile: Tile) -> None:
        """Add a tile at the end of the list.

        Args:
        ----
            tile: added tile

        """
        self._tiles.append(tile)

    def draw_tile(self, tile: Tile) -> None:
        """Add a tile at drawn_tile.

        Args:
        ----
            tile: drawn tile

        Raises:
        ------
            Raise ValueError if drawn_tile already exists.

        """
        if not self._drawn_tile:
            raise ValueError

        self._drawn_tile = tile

    def discard_tile(self, index: int = -1) -> None:
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
            if self._drawn_tile is None:
                raise ValueError
            self._drawn_tile = None

        try:
            self._tiles.pop(index)
        except IndexError:
            raise ValueError from None

    def add_call_from_discard(
        self,
        call_type: CallType,
        discarded_tile: Tile,
        indices: list[int],
        player_relation: PlayerRelation = PlayerRelation.PREV,
    ) -> None:
        """Add chii to call list.

        Args:
        ----
            call_type: call type (chi, pon, big melded kan)
            discarded_tile: discarded tile for calling.
            indices: tiles in hand use for making call.
            player_relation: relation with who discard the given tile.

        """
        if call_type not in {CallType.CHII, CallType.PON, CallType.BIG_MELDED_KAN}:
            raise ValueError

        if player_relation is PlayerRelation.SELF:
            raise ValueError

        if call_type is CallType.CHII and player_relation is not PlayerRelation.PREV:
            raise ValueError

        call = Call(
            [discarded_tile] + [self._tiles[index] for index in indices],
            call_type,
            player_relation,
        )
        indices.sort(reverse=True)

        for index in indices:
            self.discard_tile(index)
        self._calls.append(call)

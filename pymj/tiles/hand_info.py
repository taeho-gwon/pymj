from __future__ import annotations

from pymj.enums.call_type import CallType
from pymj.tiles.hand import Hand
from pymj.tiles.tile_count import TileCount


class HandInfo:
    """A class representing detailed information about a Mahjong hand's composition.

    This class maintains counts of tiles in both concealed part of the hand and calls.

    Attributes:
        concealed_count (TileCount): Count of tiles in the concealed part of the hand.
        call_counts (list[tuple[CallType, TileCount]]):
            List of call type and corresponding tile counts for each call.

    """

    def __init__(
        self,
        concealed_count: TileCount | None = None,
        call_counts: list[tuple[CallType, TileCount]] | None = None,
    ):
        """Initialize a new HandInfo instance.

        Args:
            concealed_count (TileCount | None): Initial count of concealed tiles.
                Defaults to empty TileCount if None.
            call_counts (list[tuple[CallType, TileCount]] | None):
                Initial list of call types and their tile counts.
                Defaults to empty list if None.

        """
        self.concealed_count: TileCount = (
            concealed_count if concealed_count else TileCount()
        )
        self.call_counts: list[tuple[CallType, TileCount]] = (
            call_counts if call_counts else []
        )

    @staticmethod
    def create_from_hand(hand: Hand, is_containing_drawn_tile: bool = True) -> HandInfo:
        """Create a HandInfo instance from a Hand object.

        Constructs a new HandInfo by counting tiles in the given hand, optionally
        including the most recently drawn tile. Also processes all calls (revealed
        combinations) in the hand.

        Args:
            hand (Hand): The hand to create information from.
            is_containing_drawn_tile (bool): Whether to include the drawn tile in the
                concealed count. Defaults to True.

        Returns:
            HandInfo: A new HandInfo instance representing the tile counts of the
                given hand.

        """
        tiles = hand.tiles[:]
        if is_containing_drawn_tile and hand.drawn_tile:
            tiles.append(hand.drawn_tile)

        concealed_count = TileCount.create_from_tiles(tiles)
        call_counts = [
            (call.call_type, TileCount.create_from_tiles(call.tiles))
            for call in hand.calls
        ]

        return HandInfo(concealed_count, call_counts)

    @property
    def total_count(self) -> TileCount:
        """Calculate the total count of all tiles in the hand.

        Combines the counts of concealed tiles and all tiles in calls to produce
        a total count of tiles in the hand.

        Returns:
            TileCount: The combined count of all tiles in both concealed hand
                and revealed combinations.

        """
        return sum(
            (call_count for _, call_count in self.call_counts),
            start=self.concealed_count,
        )

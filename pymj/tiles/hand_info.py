from __future__ import annotations

from pymj.enums.call_type import CallType
from pymj.tiles.hand import Hand
from pymj.tiles.tile_count import TileCount


class HandInfo:
    """Represent hand info containing tile count of concealed tiles and calls."""

    def __init__(
        self,
        concealed_count: TileCount | None = None,
        call_counts: list[tuple[CallType, TileCount]] | None = None,
    ):
        """Initialize hand info."""
        self.concealed_count: TileCount = (
            concealed_count if concealed_count else TileCount()
        )
        self.call_counts: list[tuple[CallType, TileCount]] = (
            call_counts if call_counts else []
        )

    @staticmethod
    def create_from_hand(hand: Hand, is_containing_drawn_tile: bool = True) -> HandInfo:
        """Create HandInfo class from hand.

        Args:
        ----
            hand: hand to create hand info
            is_containing_drawn_tile: True if hand info wants containing drawn_tile

        Returns:
        -------
            HandInfo class from hand

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
        """Calculate sum of all components in agari hand info.

        Returns
        -------
            TileCount: count of all tiles

        """
        return sum(
            (call_count for _, call_count in self.call_counts),
            start=self.concealed_count,
        )

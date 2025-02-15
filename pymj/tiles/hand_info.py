from __future__ import annotations

from pymj.enums.call_type import CallType
from pymj.tiles.hand import Hand
from pymj.tiles.tile import Tile
from pymj.tiles.tile_count import TileCount
from pymj.tiles.tile_mapping import TileMapping


class HandInfo:
    """Represents the complete hand information at the point of winning.

    This class stores information about concealed tiles, called tiles (melds),
    the winning tile, and whether the win was achieved by self-draw (tsumo).

    Attributes:
        concealed_count (TileCount): Count of concealed tiles in hand.
        call_counts (list[tuple[CallType, TileCount]]): List of called tiles with type.
        agari_tile (Tile | None): The winning tile, if any.
        is_tsumo (bool): Whether the win was achieved by self-draw.

    """

    def __init__(
        self,
        concealed_count: TileCount | None = None,
        call_counts: list[tuple[CallType, TileCount]] | None = None,
        agari_tile: Tile | None = None,
        is_tsumo: bool = False,
    ):
        """Initialize an HandInfo instance.

        Args:
            concealed_count (TileCount | None, optional):
                Count of concealed tiles. Defaults to None.
            call_counts (list[tuple[CallType, TileCount]] | None, optional):
                List of calls. Defaults to None.
            agari_tile (Tile | None, optional): The winning tile. Defaults to None.
            is_tsumo (bool, optional): Whether won by self-draw. Defaults to False.

        """
        self.concealed_count: TileCount = (
            concealed_count if concealed_count else TileCount()
        )
        self.call_counts: list[tuple[CallType, TileCount]] = (
            call_counts if call_counts else []
        )
        self.agari_tile = agari_tile
        self.is_tsumo = is_tsumo

    @staticmethod
    def create_from_hand(
        hand: Hand,
        agari_tile: Tile | None = None,
        is_tsumo: bool = False,
    ) -> HandInfo:
        """Create an HandInfo instance from a Hand object.

        Args:
            hand (Hand): The hand to create HandInfo from.
            agari_tile (Tile | None): The winning tile if different from drawn tile.
            is_tsumo (bool): Whether the win was achieved by self-draw.

        Returns:
            HandInfo: A new instance containing the hand information.

        Raises:
            ValueError: If both drawn_tile and agari_tile are given.

        """
        if hand.drawn_tile and agari_tile:
            raise ValueError

        concealed_counts = TileCount.create_from_tiles(hand.tiles)
        call_counts = [
            (call.call_type, TileCount.create_from_tiles(call.tiles))
            for call in hand.calls
        ]

        return HandInfo(
            concealed_count=concealed_counts,
            call_counts=call_counts,
            agari_tile=agari_tile or hand.drawn_tile,
            is_tsumo=is_tsumo,
        )

    @property
    def total_count(self) -> TileCount:
        """Calculates the total count of all tiles in the hand.

        Returns:
            TileCount: Sum of concealed tiles, called tiles, and the winning tile.

        """
        total_count = sum(
            (call_count for _, call_count in self.call_counts),
            start=TileCount(),
        )
        total_count = total_count + self.concealed_count
        if self.agari_tile:
            total_count[TileMapping.tile_to_index(self.agari_tile)] += 1

        return total_count

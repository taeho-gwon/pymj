from __future__ import annotations

from pymj.tiles.hand import Hand
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile import Tile
from pymj.tiles.tile_count import TileCount
from pymj.tiles.tile_mapping import TileMapping


class AgariHandInfo:
    """Represent hand info with agari tile."""

    def __init__(
        self,
        agari_tile: Tile,
        is_tsumo: bool = False,
        hand_info: HandInfo | None = None,
    ):
        """Initialize agari hand info."""
        self.agari_tile = agari_tile
        self.is_tsumo = is_tsumo
        self.hand_info = hand_info if hand_info else HandInfo()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AgariHandInfo):
            return False
        return (
            self.agari_tile == other.agari_tile
            and self.is_tsumo == other.is_tsumo
            and self.hand_info == other.hand_info
        )

    @staticmethod
    def create_from_hand(hand: Hand, agari_tile: Tile | None = None) -> AgariHandInfo:
        """Create AgariHandInfo class from hand.

        Args:
        ----
            hand: hand to create hand info
            agari_tile: tile when use for agari.

            Exactly one of agari_tile and hand.drawn_tile should have value.

        Returns:
        -------
            HandInfo class from hand

        Raises:
        ------
            ValueError if agari_tile and hand.drawn_tile are both None or both not None.

        """
        if hand.drawn_tile and agari_tile:
            raise ValueError

        agari_tile = agari_tile or hand.drawn_tile
        if not agari_tile:
            raise ValueError

        return AgariHandInfo(agari_tile, True, HandInfo.create_from_hand(hand, False))

    @property
    def total_count(self) -> TileCount:
        """Calculate sum of all components in agari hand info.

        Returns
        -------
            TileCount: count of all tiles

        """
        tile_count = self.hand_info.total_count
        tile_count[TileMapping.tile_to_index(self.agari_tile)] += 1
        return tile_count

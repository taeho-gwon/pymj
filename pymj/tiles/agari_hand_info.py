from __future__ import annotations

from pymj.tiles.hand import Hand
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile import Tile
from pymj.tiles.tile_count import TileCount
from pymj.tiles.tile_mapping import TileMapping


class AgariHandInfo:
    """Represents hand information for a winning (agari) state in a tile-based game.

    This class encapsulates details about a hand that has reached a winning condition,
    including the winning tile, the winning method, and hand composition.

    Attributes:
        agari_tile (Tile): The tile used to complete the winning hand.
        is_tsumo (bool): Indicates if the win was by tsumo or by ron.
        hand_info (HandInfo): Detailed information about the hand's composition.

    """

    def __init__(
        self,
        agari_tile: Tile,
        is_tsumo: bool = False,
        hand_info: HandInfo | None = None,
    ):
        """Initialize an AgariHandInfo instance.

        Args:
            agari_tile (Tile): The tile that completes the winning hand.
            is_tsumo (bool, optional): Whether the win is by self-draw.
                Defaults to False.
            hand_info (HandInfo, optional): Detailed hand information.
                Defaults to a new HandInfo.

        """
        self.agari_tile = agari_tile
        self.is_tsumo = is_tsumo
        self.hand_info = hand_info if hand_info else HandInfo()

    @staticmethod
    def create_from_hand(hand: Hand, agari_tile: Tile | None = None) -> AgariHandInfo:
        """Create an AgariHandInfo instance from a given hand.

        Args:
            hand (Hand): The hand to create hand info from.
            agari_tile (Tile, optional): Specific tile used for winning.
                Defaults to None.

        Returns:
            AgariHandInfo: An instance representing the winning hand state.

        Raises:
            ValueError: If both agari_tile and hand.drawn_tile are specified
                or neither is specified.

        """
        if hand.drawn_tile and agari_tile:
            raise ValueError

        agari_tile = agari_tile or hand.drawn_tile
        if not agari_tile:
            raise ValueError

        return AgariHandInfo(agari_tile, True, HandInfo.create_from_hand(hand, False))

    @property
    def total_count(self) -> TileCount:
        """Calculate the total tile count in the winning hand.

        Returns:
            TileCount: A count of all tiles in the hand, including the winning tile.

        """
        tile_count = self.hand_info.total_count
        tile_count[TileMapping.tile_to_index(self.agari_tile)] += 1
        return tile_count

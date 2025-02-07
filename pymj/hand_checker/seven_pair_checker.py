from pymj.enums.division_part_state import DivisionPartState
from pymj.enums.wait_type import WaitType
from pymj.hand_checker.base_hand_checker import BaseHandChecker
from pymj.tiles.division import Division
from pymj.tiles.division_part import DivisionPart
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile_constants import Tiles
from pymj.tiles.tile_count import TileCount


class SevenPairChecker(BaseHandChecker):
    """Check and calculate hand patterns of seven pairs."""

    def calculate_divisions(self, hand_info: HandInfo) -> list[Division]:
        """Create list of division containing seven pairs from given hand.

        Args:
            hand_info (HandInfo): Contains info about hand.

        Returns:
            list[Division]: List containing single division of seven pairs.

        Raises:
            ValueError: When hand cannot form seven pairs pattern.

        """
        if not hand_info.agari_tile or not self.check_agari(hand_info):
            raise ValueError

        division_parts = [
            DivisionPart.create_head(
                tile,
                (
                    DivisionPartState.CONCEALED
                    if hand_info.concealed_count[tile] == 2 or hand_info.is_tsumo
                    else DivisionPartState.RON
                ),
            )
            for tile in Tiles.ALL
            if hand_info.concealed_count[tile] > 0
        ]
        return [Division(division_parts, WaitType.SINGLE_WAIT)]

    def calculate_shanten(self, hand_info: HandInfo) -> int:
        """Calculate shanten number for seven pairs hand pattern.

        Args:
            hand_info: Contains information about tiles in hand and winning condition.

        Returns:
            int: Number of tiles away from tenpai, or INFINITE_SHANTEN if impossible.

        """
        if hand_info.concealed_count.num_tiles != 13:
            return self.INFINITE_SHANTEN

        agari_tile_count = (
            TileCount.create_from_tiles([hand_info.agari_tile])
            if hand_info.agari_tile
            else TileCount()
        )
        real_tile_count = hand_info.concealed_count + agari_tile_count

        num_pairs = sum(1 for num_tile in real_tile_count if num_tile >= 2)
        num_kinds = sum(1 for num_tile in real_tile_count if num_tile >= 1)
        return 6 - num_pairs + max(7 - num_kinds, 0)

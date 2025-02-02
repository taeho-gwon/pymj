from pymj.enums.division_part_state import DivisionPartState
from pymj.enums.wait_type import WaitType
from pymj.hand_checker.base_hand_checker import HandChecker
from pymj.tiles.division import Division
from pymj.tiles.division_part import DivisionPart
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile import Tiles
from pymj.tiles.tile_count import TileCount


class SevenPairChecker(HandChecker):
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
        if not self.check_agari(hand_info):
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
        ]
        return [Division(division_parts, WaitType.SINGLE_WAIT)]

    def calculate_shanten(self, hand_info: HandInfo) -> int:
        """Calculate shanten number for seven pairs pattern.

        Args:
            hand_info (HandInfo): Contains info about hand.

        Returns:
            int: Number of tile arrangements needed, where:
                -1: Complete hand
                 0: Ready hand (tenpai)
                >0: Number of arrangements needed

        Raises:
            ValueError: When hand does not contain exactly 13 concealed tiles.

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

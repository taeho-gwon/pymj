from pymj.enums.division_part_state import DivisionPartState
from pymj.enums.wait_type import WaitType
from pymj.hand_checker.base_hand_checker import BaseHandChecker
from pymj.tiles.division import Division
from pymj.tiles.division_part import DivisionPart
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile import Tiles
from pymj.tiles.tile_count import TileCount
from pymj.tiles.tile_mapping import TileMapping


class ThirteenOrphanChecker(BaseHandChecker):
    """Check and calculate thirteen orphans hand pattern."""

    def calculate_divisions(self, hand_info: HandInfo) -> list[Division]:
        """Calculate divisions for completed thirteen orphans hand pattern.

        Args:
            hand_info: Contains information about tiles in hand and winning condition.

        Returns:
            list[Division]: Single division containing thirteen orphans pattern.

        Raises:
            ValueError: When hand cannot form thirteen orphans pattern.

        """
        if not hand_info.agari_tile or not self.check_agari(hand_info):
            raise ValueError
        is_thirteen_waits = all(
            hand_info.concealed_count[tile] == 1 for tile in Tiles.TERMINALS_AND_HONORS
        )
        if is_thirteen_waits:
            wait_type = WaitType.THIRTEEN_ORPHANS_13WAIT
            head_idx = TileMapping.tile_to_index(hand_info.agari_tile)

        else:
            wait_type = WaitType.THIRTEEN_ORPHANS_1WAIT
            head_idx = next(
                tile
                for tile in Tiles.TERMINALS_AND_HONORS
                if hand_info.concealed_count[tile] == 2
            )

        state = (
            DivisionPartState.CONCEALED if hand_info.is_tsumo else DivisionPartState.RON
        )
        return [
            Division([DivisionPart.create_thirteen_orphans(head_idx, state)], wait_type)
        ]

    def calculate_shanten(self, hand_info: HandInfo) -> int:
        """Calculate shanten number for thirteen orphans hand pattern.

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

        is_orphan_pair_exist = any(
            real_tile_count[tile] > 1 for tile in Tiles.TERMINALS_AND_HONORS
        )
        num_orphan_kinds = sum(
            1 for tile in Tiles.TERMINALS_AND_HONORS if real_tile_count[tile] > 0
        )

        return 13 - num_orphan_kinds - int(is_orphan_pair_exist)

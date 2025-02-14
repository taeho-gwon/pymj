from copy import copy, deepcopy

from pymj.enums.division_part_state import DivisionPartState
from pymj.enums.division_part_type import DivisionPartType
from pymj.enums.wait_type import WaitType
from pymj.hand_checker.base_hand_checker import BaseHandChecker
from pymj.tiles.division import Division
from pymj.tiles.division_part import DivisionPart
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile_constants import Tiles
from pymj.tiles.tile_count import TileCount
from pymj.tiles.tile_mapping import TileMapping


class NormalFormChecker(BaseHandChecker):
    """Calculate shanten number for normal form hands and find possible divisions.

    Attributes:
        _tile_count (TileCount): Counter for concealed tiles in hand.
        _used_count (TileCount): Counter for all tiles including called tiles.
        _best_shanten (int): Current best shanten number found during calculation.

    """

    def __init__(self) -> None:
        """Initialize normal form checker."""
        self._tile_count: TileCount = TileCount()
        self._used_count: TileCount = TileCount()
        self._best_shanten: int = self.INFINITE_SHANTEN
        self._parts: list[DivisionPart] = []

    def calculate_shanten(self, hand_info: HandInfo) -> int:
        """Calculate shanten number for given hand information.

        Args:
            hand_info: Contains information about tiles in hand and called tiles.

        Returns:
            int: Minimum shanten number for the hand.

        Raises:
            ValueError: If number of tiles in hand is invalid.

        """
        self._best_shanten = self.INFINITE_SHANTEN

        num_calls = len(hand_info.call_counts)
        self._used_count = copy(hand_info.total_count)

        self._tile_count = copy(hand_info.concealed_count)
        if hand_info.agari_tile:
            self._tile_count[TileMapping.tile_to_index(hand_info.agari_tile)] += 1

        if hand_info.concealed_count.num_tiles % 3 != 1:
            raise ValueError

        if hand_info.concealed_count.num_tiles / 3 + num_calls != 4:
            raise ValueError

        for head in Tiles.ALL:
            if self._tile_count[head] < 2:
                continue
            self._tile_count[head] -= 2
            self._calculate_best_shanten(num_calls)
            self._tile_count[head] += 2

        self._calculate_best_shanten(num_calls, is_head_fixed=False)
        return self._best_shanten

    def _calculate_best_shanten(
        self,
        num_complete_sets: int,
        is_head_fixed: bool = True,
        index: int = 0,
    ) -> None:

        index = self._tile_count.find_earliest_nonzero_index(index)

        if index == 34:
            current_best_shanten = 5 - num_complete_sets - 2 * int(is_head_fixed)
            if current_best_shanten >= self._best_shanten:
                return
            self._calculate_best_shanten_step2(num_complete_sets, 0, is_head_fixed)
            return

        if self._can_make_triplet(index):
            self._tile_count[index] -= 3
            self._calculate_best_shanten(num_complete_sets + 1, is_head_fixed, index)
            self._tile_count[index] += 3

        if self._can_make_sequence(index):
            self._tile_count[index] -= 1
            self._tile_count[index + 1] -= 1
            self._tile_count[index + 2] -= 1
            self._calculate_best_shanten(num_complete_sets + 1, is_head_fixed, index)
            self._tile_count[index] += 1
            self._tile_count[index + 1] += 1
            self._tile_count[index + 2] += 1

        self._calculate_best_shanten(num_complete_sets, is_head_fixed, index + 1)

    def _calculate_best_shanten_step2(
        self,
        num_complete_sets: int,
        num_partial_sets: int,
        is_head_fixed: bool,
        index: int = 0,
    ) -> None:
        index = self._tile_count.find_earliest_nonzero_index(index)

        if num_complete_sets + num_partial_sets == 4 or index == 34:
            can_make_pair = is_head_fixed or any(
                self._tile_count[tile] == 1 and self._used_count[tile] < 4
                for tile in Tiles.ALL
            )
            current_shanten = (
                9
                - num_complete_sets * 2
                - num_partial_sets
                - int(is_head_fixed)
                - int(can_make_pair)
            )
            self._best_shanten = min(self._best_shanten, current_shanten)
            return

        if self._can_make_dual_pon_part(index):
            self._tile_count[index] -= 2
            self._calculate_best_shanten_step2(
                num_complete_sets, num_partial_sets + 1, is_head_fixed, index
            )
            self._tile_count[index] += 2

        if self._can_make_closed_part(index):
            self._tile_count[index] -= 1
            self._tile_count[index + 2] -= 1
            self._calculate_best_shanten_step2(
                num_complete_sets, num_partial_sets + 1, is_head_fixed, index
            )
            self._tile_count[index] += 1
            self._tile_count[index + 2] += 1

        if self._can_make_edge_part(index) or self._can_make_side_part(index):
            self._tile_count[index] -= 1
            self._tile_count[index + 1] -= 1
            self._calculate_best_shanten_step2(
                num_complete_sets, num_partial_sets + 1, is_head_fixed, index
            )
            self._tile_count[index] += 1
            self._tile_count[index + 1] += 1

        self._calculate_best_shanten_step2(
            num_complete_sets, num_partial_sets, is_head_fixed, index + 1
        )

    def _can_make_triplet(self, index: int, num: int = 1) -> bool:
        return self._tile_count[index] >= 3 * num

    def _can_make_sequence(self, index: int, num: int = 1) -> bool:
        return (
            Tiles.IS_SEQUENCE_STARTS[index]
            and self._tile_count[index] >= num
            and self._tile_count[index + 1] >= num
            and self._tile_count[index + 2] >= num
        )

    def _can_make_dual_pon_part(self, index: int) -> bool:
        return self._tile_count[index] >= 2 and self._used_count[index] < 4

    def _can_make_closed_part(self, index: int) -> bool:
        return (
            Tiles.IS_SEQUENCE_STARTS[index]
            and self._tile_count[index + 2] > 0
            and self._used_count[index + 1] < 4
        )

    def _can_make_side_part(self, index: int) -> bool:
        return (
            Tiles.IS_SIDE_WAIT_STARTS[index]
            and self._tile_count[index + 1] > 0
            and (self._used_count[index + 2] < 4 or self._used_count[index - 1] < 4)
        )

    def _can_make_edge_part(self, index: int) -> bool:
        if Tiles.IS_LEFT_EDGE_WAIT_STARTS[index]:
            return self._tile_count[index + 1] > 0 and self._used_count[index + 2] < 4
        elif Tiles.IS_RIGHT_EDGE_WAIT_STARTS[index]:
            return self._tile_count[index + 1] > 0 and self._used_count[index - 1] < 4
        else:
            return False

    def _can_make_head_part(self, index: int) -> bool:
        return self._tile_count[index] >= 2

    def calculate_divisions(self, hand_info: HandInfo) -> list[Division]:
        """Calculate all possible hand divisions based on given hand information.

        Args:
            hand_info: Complete hand information including
                concealed tiles, calls, and winning tile.
                HandInfo must contain valid agari_tile and pass check_agari validation.

        Returns:
            list[Division]: List of all possible hand divisions.
                Each division represents a unique way to group tiles into complete sets.

        Raises:
            ValueError: When hand cannot form normal agari pattern.

        """
        if not hand_info.agari_tile or not self.check_agari(hand_info):
            raise ValueError

        self._tile_count = copy(hand_info.concealed_count)
        agari_tile_index = TileMapping.tile_to_index(hand_info.agari_tile)
        self._tile_count[agari_tile_index] += 1

        call_parts = [
            DivisionPart.create_from_call(call_type, tile_count)
            for call_type, tile_count in hand_info.call_counts
        ]

        divisions: list[Division] = []
        for concealed_parts in self._calculate_concealed_parts():
            divisions.extend(
                NormalFormChecker._calculate_divisions_from_division_parts(
                    concealed_parts, call_parts, agari_tile_index, hand_info.is_tsumo
                )
            )

        return divisions

    def _calculate_concealed_parts(self) -> list[list[DivisionPart]]:
        concealed_parts: list[list[DivisionPart]] = []
        for head in Tiles.ALL:
            if self._tile_count[head] < 2:
                continue
            self._tile_count[head] -= 2
            head_part = DivisionPart.create_head(head, DivisionPartState.CONCEALED)
            self._parts.append(head_part)
            self._find_bodies()
            self._tile_count[head] += 2
        return concealed_parts

    def _find_bodies(self, index: int = 0) -> None:
        index = self._tile_count.find_earliest_nonzero_index(index)
        if index == 34:
            return

        for num_triplet in range(2):
            if self._can_make_triplet(index, num_triplet) and self._can_make_sequence(
                index, num_sequence := self._tile_count[index] - num_triplet * 3
            ):
                self._tile_count[index] = 0
                self._tile_count[index + 1] -= num_sequence
                self._tile_count[index + 2] -= num_sequence
                self._find_bodies(index + 1)
                self._tile_count[index] = 3 * num_triplet + num_sequence
                self._tile_count[index + 1] += num_sequence
                self._tile_count[index + 2] += num_sequence

    @staticmethod
    def _calculate_divisions_from_division_parts(
        concealed_parts: list[DivisionPart],
        call_parts: list[DivisionPart],
        agari_tile_index: int,
        is_tsumo: bool,
    ) -> list[Division]:
        divisions = []
        for idx, concealed_part in enumerate(concealed_parts):
            if concealed_part.tile_count[agari_tile_index] == 0:
                continue

            temp_concealed_parts = deepcopy(concealed_parts)
            temp_concealed_parts[idx].state = (
                DivisionPartState.CONCEALED if is_tsumo else DivisionPartState.RON
            )
            wait_type = NormalFormChecker._calculate_wait_type(
                temp_concealed_parts[idx], agari_tile_index
            )
            divisions.append(Division(temp_concealed_parts + call_parts, wait_type))
        return divisions

    @staticmethod
    def _calculate_wait_type(division_part: DivisionPart, agari_tile: int) -> WaitType:
        if division_part.type == DivisionPartType.HEAD:
            return WaitType.SINGLE_WAIT

        if division_part.type == DivisionPartType.TRIPLE:
            return WaitType.DUAL_PON_WAIT

        if (
            division_part.tile_count[agari_tile - 1] > 0
            and division_part.tile_count[agari_tile + 1] > 0
        ):
            return WaitType.CLOSED_WAIT

        if (
            division_part.tile_count[agari_tile - 2] > 0
            and division_part.tile_count[agari_tile - 1] > 0
        ):
            return (
                WaitType.EDGE_WAIT
                if Tiles.IS_LEFT_EDGE_WAIT_STARTS[agari_tile - 2]
                else WaitType.SIDE_WAIT
            )

        if (
            division_part.tile_count[agari_tile + 1] > 0
            and division_part.tile_count[agari_tile + 2] > 0
        ):
            return (
                WaitType.EDGE_WAIT
                if Tiles.IS_RIGHT_EDGE_WAIT_STARTS[agari_tile + 1]
                else WaitType.SIDE_WAIT
            )

        raise ValueError

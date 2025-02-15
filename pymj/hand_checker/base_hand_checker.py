from abc import ABC, abstractmethod
from copy import deepcopy

from pymj.enums.efficiency_data import EfficiencyData
from pymj.tiles.division import Division
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile_constants import Tiles
from pymj.tiles.tile_mapping import TileMapping


class BaseHandChecker(ABC):
    """Define abstract interface for checking hand completion and tile combinations.

    This abstract class provides methods to analyze tile combinations
    and validate winning conditions.

    Attributes:
            INFINITE_SHANTEN (int): Constant representing impossible hand arrangement.

    """

    INFINITE_SHANTEN = 100

    @abstractmethod
    def calculate_shanten(self, hand_info: HandInfo) -> int:
        """Calculate shanten number (minimum tile changes needed to reach tenpai).

        Args:
            hand_info (HandInfo): HandInfo object to calculate.

        Returns:
            int: Shanten number, where 0 means tenpai, -1 means winning hand.

        """

    @abstractmethod
    def calculate_divisions(self, hand_info: HandInfo) -> list[Division]:
        """Calculate all possible tile divisions for given hand.

        Args:
            hand_info (HandInfo): HandInfo object to calculate.

        Returns:
            list[Division]: List of possible tile combinations forming valid groups.

        """

    def check_agari(self, hand_info: HandInfo) -> bool:
        """Check if current hand forms a valid winning hand.

        Args:
            hand_info (HandInfo): HandInfo object to calculate.

        Returns:
            bool: True if hand is complete, False otherwise.

        """
        return self.calculate_shanten(hand_info) == -1

    def calculate_efficiency(self, hand_info: HandInfo) -> list[EfficiencyData]:
        """Calculate discard efficiency for each tile in the hand.

        Args:
            hand_info (HandInfo): Hand state including concealed tiles and winning tile.

        Returns:
            list[EfficiencyData]: List of efficiency data for each possible discard.

        Raises:
            ValueError: If hand tile count is not 3n+1 + agari_tile.

        """
        if hand_info.concealed_count.num_tiles % 3 != 1 or hand_info.agari_tile is None:
            raise ValueError

        shanten = self.calculate_shanten(hand_info)
        efficiency = []

        new_hand_info = deepcopy(hand_info)
        new_hand_info.concealed_count[
            TileMapping.tile_to_index(hand_info.agari_tile)
        ] += 1
        new_hand_info.agari_tile = None

        for discard_candidate in Tiles.ALL:
            if new_hand_info.concealed_count[discard_candidate] == 0:
                continue
            new_hand_info.concealed_count[discard_candidate] -= 1

            if shanten == self.calculate_shanten(new_hand_info):
                ukeire, num_ukeire = self._calculate_ukeire(new_hand_info, shanten)
                efficiency.append(
                    EfficiencyData(
                        discard_tile=discard_candidate,
                        ukeire=ukeire,
                        num_ukeire=num_ukeire,
                    )
                )
            new_hand_info.concealed_count[discard_candidate] += 1

        efficiency.sort(key=lambda x: (-x.num_ukeire, x.discard_tile))
        return efficiency

    def _calculate_ukeire(
        self, hand_info: HandInfo, shanten: int
    ) -> tuple[list[int], int]:
        ukeire = []
        num_ukeire = 0
        total_count = hand_info.total_count
        for draw_candidate in Tiles.ALL:
            if total_count[draw_candidate] == 4:
                continue
            hand_info.agari_tile = TileMapping.index_to_tile(draw_candidate)
            if shanten - 1 == self.calculate_shanten(hand_info):
                ukeire.append(draw_candidate)
                num_ukeire += 4 - total_count[draw_candidate]
            hand_info.agari_tile = None

        return ukeire, num_ukeire

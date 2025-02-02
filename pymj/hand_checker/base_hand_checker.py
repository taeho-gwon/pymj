from abc import ABC, abstractmethod

from pymj.tiles.division import Division
from pymj.tiles.hand_info import HandInfo


class HandChecker(ABC):
    """Define abstract interface for checking hand completion and tile combinations.

    This abstract class provides methods to analyze tile combinations
    and validate winning conditions.

    """

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
        return self.calculate_shanten(hand_info) == 0

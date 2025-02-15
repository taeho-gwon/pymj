from pymj.enums.division_part_state import DivisionPartState
from pymj.enums.division_part_type import DivisionPartType
from pymj.enums.wait_type import WaitType
from pymj.tiles.division_part import DivisionPart
from pymj.tiles.tile_count import TileCount


class Division:
    """Store and manage division parts and their properties.

    Attributes:
        parts (list[DivisionPart]): List containing different division parts.
        wait_type (WaitType): Type of wait formation for winning.

    """

    def __init__(self, parts: list[DivisionPart], wait_type: WaitType):
        """Store and manage division parts and their properties.

        Attributes:
            parts (list[DivisionPart]): List containing different division parts.
            wait_type (WaitType): Type of wait formation for winning.

        """
        self.parts = parts
        self.wait_type = wait_type

    @property
    def tile_count(self) -> TileCount:
        """Calculate total tile count from all division parts.

        Returns:
            TileCount: Sum of tile counts from all parts.

        """
        return sum((part.tile_count for part in self.parts), start=TileCount())

    @property
    def num_concealed_triplets(self) -> int:
        """Count number of concealed triplets and quads.

        Returns:
            int: Number of concealed triplets and quads.

        """
        return sum(
            1
            for part in self.parts
            if part.state is DivisionPartState.CONCEALED
            and (
                part.type is DivisionPartType.TRIPLE
                or part.type is DivisionPartType.QUAD
            )
        )

    @property
    def num_quads(self) -> int:
        """Count number of quad parts.

        Returns:
            int: Number of quad parts in division.

        """
        return sum(1 for part in self.parts if part.type is DivisionPartType.QUAD)

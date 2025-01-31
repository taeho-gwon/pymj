from __future__ import annotations

from pymj.enums.call_type import CallType
from pymj.enums.division_part_state import DivisionPartState
from pymj.enums.division_part_type import DivisionPartType
from pymj.tiles.tile import Tiles
from pymj.tiles.tile_count import TileCount


class DivisionPart:
    """Create and manage tile combinations for hand division.

    A DivisionPart represents a specific combination of tiles
    such as pairs, triples, sequences, or special combinations.
    It tracks the type, count, and state of the combination.

    Attributes:
        type (DivisionPartType): The type of the division part (head, triple, etc.)
        tile_count (TileCount): Counter tracking the number of each tile in this part
        state (DivisionPartState): The state of this combination

    """

    def __init__(
        self,
        division_part_type: DivisionPartType,
        tile_count: TileCount,
        state: DivisionPartState,
    ):
        """Initialize a new division part.

        Args:
            division_part_type (DivisionPartType):
                The type of division part (HEAD, TRIPLE, SEQUENCE, etc.)
            tile_count (TileCount): Counter tracking the number of each tile
            state (DivisionPartState): The current state of this tile combination

        """
        self.type = division_part_type
        self.tile_count = tile_count
        self.state = state

    @staticmethod
    def create_head(tile_index: int, state: DivisionPartState) -> DivisionPart:
        """Create a pair of identical tiles for use as a hand's head.

        Args:
            tile_index (int): Index of the tile to form the pair
            state (DivisionPartState): The concealment state of this part

        Returns:
            DivisionPart: A DivisionPart instance representing the pair

        """
        return DivisionPart(
            division_part_type=DivisionPartType.HEAD,
            tile_count=TileCount.create_from_indices([tile_index] * 2),
            state=state,
        )

    @staticmethod
    def create_triple(tile_index: int, state: DivisionPartState) -> DivisionPart:
        """Create a triple of identical tiles.

        Args:
            tile_index (int): Index of the tile to form the triple
            state (DivisionPartState): The concealment state of this part

        Returns:
            DivisionPart: A DivisionPart instance representing the triple

        """
        return DivisionPart(
            division_part_type=DivisionPartType.TRIPLE,
            tile_count=TileCount.create_from_indices([tile_index] * 3),
            state=state,
        )

    @staticmethod
    def create_straight(
        first_tile_index: int, state: DivisionPartState
    ) -> DivisionPart:
        """Create a sequence of three consecutive numbered tiles.

        Args:
            first_tile_index (int): Index of the first tile in the sequence
            state (DivisionPartState): The concealment state of this part

        Returns:
            DivisionPart: A DivisionPart instance representing the sequence

        Raises:
            ValueError: If first_tile_index is not a valid sequence starting point

        """
        if first_tile_index not in Tiles.STRAIGHT_STARTS:
            raise ValueError
        return DivisionPart(
            division_part_type=DivisionPartType.SEQUENCE,
            tile_count=TileCount.create_from_indices(
                [first_tile_index, first_tile_index + 1, first_tile_index + 2]
            ),
            state=state,
        )

    @staticmethod
    def create_thirteen_orphans(
        head_tile_index: int, state: DivisionPartState
    ) -> DivisionPart:
        """Create a special combination for the Thirteen Orphans pattern.

        Args:
            head_tile_index (int): Index of the tile that forms the pair
            state (DivisionPartState): The concealment state of this part

        Returns:
            DivisionPart: A DivisionPart instance representing the Thirteen Orphans

        """
        return DivisionPart(
            division_part_type=DivisionPartType.THIRTEEN_ORPHANS,
            tile_count=TileCount.create_from_indices(
                Tiles.TERMINALS_AND_HONORS + [head_tile_index]
            ),
            state=state,
        )

    @staticmethod
    def create_from_call(call_type: CallType, call_count: TileCount) -> DivisionPart:
        """Create a tile combination based on the type of call made.

        Args:
            call_type (CallType): Type of the call (Chii, Pon, or Kan)
            call_count (TileCount): Counter tracking the tiles involved in the call

        Returns:
            DivisionPart: A DivisionPart instance representing the called combination

        """
        match call_type:
            case CallType.CHII:
                part_type = DivisionPartType.SEQUENCE
            case CallType.PON:
                part_type = DivisionPartType.TRIPLE
            case _:
                part_type = DivisionPartType.QUAD

        return DivisionPart(
            division_part_type=part_type,
            tile_count=call_count,
            state=(
                DivisionPartState.CONCEALED
                if call_type is CallType.CONCEALED_KAN
                else DivisionPartState.OPENED
            ),
        )

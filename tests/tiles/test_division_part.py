import pytest

from pymj.enums.call_type import CallType
from pymj.enums.division_part_state import DivisionPartState
from pymj.enums.division_part_type import DivisionPartType
from pymj.tiles.division_part import DivisionPart
from pymj.tiles.tile_constants import Tiles
from pymj.tiles.tile_count import TileCount


def test_create_head():
    # Given: head tile and state
    head_index = 0
    state = DivisionPartState.RON

    # When: create_head
    head_part = DivisionPart.create_head(head_index, state)

    # Then: expected head_part is created
    assert head_part.tile_count[head_index] == 2
    assert head_part.type == DivisionPartType.HEAD
    assert head_part.state == state


def test_create_triple():
    # Given: triple tile and state
    triple_index = 0
    state = DivisionPartState.RON

    # When: create_head
    triple_part = DivisionPart.create_triple(triple_index, state)

    # Then: expected triple_part is created
    assert triple_part.tile_count[triple_index] == 3
    assert triple_part.type == DivisionPartType.TRIPLE
    assert triple_part.state == state


def test_create_sequence():
    # Given: sequence tile and state
    sequence_index = 0
    state = DivisionPartState.RON

    # When: create_sequence
    sequence_part = DivisionPart.create_sequence(sequence_index, state)

    # Then: expected sequence_part is created
    assert sequence_part.tile_count[sequence_index] == 1
    assert sequence_part.tile_count[sequence_index + 1] == 1
    assert sequence_part.tile_count[sequence_index + 2] == 1
    assert sequence_part.type == DivisionPartType.SEQUENCE
    assert sequence_part.state == state


def test_create_sequence_fail():
    # Given: tile cannaot make sequence and state
    invalid_sequence_index = 8  # 9m
    state = DivisionPartState.RON

    # Then: raise error when create_sequence
    with pytest.raises(ValueError):
        DivisionPart.create_sequence(invalid_sequence_index, state)


def test_create_thirteen_orphans():
    # Given: pair tile of thirteen orphan and state
    pair_index = 0
    state = DivisionPartState.RON

    # When: create_thirteen_orphans
    thirteen_orphan_part = DivisionPart.create_thirteen_orphans(pair_index, state)

    # Then: expected thirteen_orphan_part is created
    assert thirteen_orphan_part.tile_count[pair_index] == 2
    assert all(
        thirteen_orphan_part.tile_count[tile] == 1
        for tile in Tiles.TERMINALS_AND_HONORS
        if tile != pair_index
    )
    assert thirteen_orphan_part.type == DivisionPartType.THIRTEEN_ORPHANS
    assert thirteen_orphan_part.state == state


@pytest.mark.parametrize(
    "call_type, expected_part_type, expected_state, tile_indices",
    [
        (CallType.CHII, DivisionPartType.SEQUENCE, DivisionPartState.OPENED, [0, 1, 2]),
        (CallType.PON, DivisionPartType.TRIPLE, DivisionPartState.OPENED, [14, 14, 14]),
        (
            CallType.CONCEALED_KAN,
            DivisionPartType.QUAD,
            DivisionPartState.CONCEALED,
            [17, 17, 17, 17],
        ),
        (
            CallType.BIG_MELDED_KAN,
            DivisionPartType.QUAD,
            DivisionPartState.OPENED,
            [24, 24, 24, 24],
        ),
        (
            CallType.SMALL_MELDED_KAN,
            DivisionPartType.QUAD,
            DivisionPartState.OPENED,
            [31, 31, 31, 31],
        ),
    ],
)
def test_create_from_call(call_type, expected_part_type, expected_state, tile_indices):
    # Given: call_type and tile_counts
    tile_count = TileCount.create_from_indices(tile_indices)

    # When: create_from_call
    call_part = DivisionPart.create_from_call(call_type, tile_count)

    # Then: expected call part is created
    assert call_part.tile_count == tile_count
    assert call_part.state == expected_state

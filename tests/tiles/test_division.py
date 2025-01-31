import pytest

from pymj.enums.call_type import CallType
from pymj.enums.division_part_state import DivisionPartState
from pymj.enums.wait_type import WaitType
from pymj.tiles.division import Division
from pymj.tiles.division_part import DivisionPart
from pymj.tiles.tile_count import TileCount


@pytest.fixture
def sample_division():
    division_part1 = DivisionPart.create_head(0, DivisionPartState.RON)  # 1m head
    division_part2 = DivisionPart.create_triple(
        1, DivisionPartState.CONCEALED
    )  # 2m triple
    division_part3 = DivisionPart.create_from_call(
        CallType.PON, TileCount.create_from_indices([7, 7, 7])
    )  # 8m pon
    division_part4 = DivisionPart.create_from_call(
        CallType.CONCEALED_KAN, TileCount.create_from_indices([8, 8, 8, 8])
    )  # 9m quads
    division_part5 = DivisionPart.create_from_call(
        CallType.SMALL_MELDED_KAN, TileCount.create_from_indices([30, 30, 30, 30])
    )  # 9m quads

    return Division(
        [
            division_part1,
            division_part2,
            division_part3,
            division_part4,
            division_part5,
        ],
        WaitType.SINGLE_WAIT,
    )


def test_tile_count(sample_division):
    assert sample_division.tile_count[0] == 2
    assert sample_division.tile_count[1] == 3
    assert sample_division.tile_count[7] == 3
    assert sample_division.tile_count[8] == 4
    assert sample_division.tile_count[30] == 4


def test_num_concealed_triplets(sample_division):
    assert sample_division.num_concealed_triplets == 2


def test_num_quads(sample_division):
    assert sample_division.num_quads == 2

import pytest

from pymj.tiles.tile_count import TileCount
from pymj.tiles.tile_mapping import TileMapping


@pytest.fixture
def tile_count_123m456s78889p33z(hand_123m456s78889p33z):
    return TileCount.create_from_tiles(hand_123m456s78889p33z.tiles)


def test_create_from_tiles(hand_123m456s78889p33z):
    # Given : hand
    hand = hand_123m456s78889p33z

    # When : call create_from_tiles
    tile_count = TileCount.create_from_tiles(hand.tiles)

    # Then : tile_count create success
    assert tile_count[:] == [
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        3,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        0,
    ]


def test_create_from_indices(tile_count_123m456s78889p33z, hand_123m456s78889p33z):
    # Given : hand and indices
    hand = hand_123m456s78889p33z
    indices = [TileMapping.tile_to_index(tile) for tile in hand.tiles]

    # When : call create_from_tiles
    tile_count = TileCount.create_from_indices(indices)

    # Then : tile_count is same
    assert tile_count_123m456s78889p33z == tile_count


def test_num_tiles(tile_count_123m456s78889p33z):
    # Given: tile_count
    tile_count = tile_count_123m456s78889p33z

    # Then : num_tiles work success
    assert tile_count.num_tiles == 13

    # When : tile changed
    tile_count[0] += 1

    # Then: num_tiles increase
    assert tile_count.num_tiles == 14


def test_find_earliest_nonzero_index(tile_count_123m456s78889p33z):
    # Given : tile_count
    tile_count = tile_count_123m456s78889p33z

    # Then : find_earliest_nonzero_index works success
    assert tile_count.find_earliest_nonzero_index() == 0  # st -> 1m
    assert tile_count.find_earliest_nonzero_index(3) == 15  # 4m -> 7p
    assert tile_count.find_earliest_nonzero_index(19) == 21  # 2s -> 4s
    assert tile_count.find_earliest_nonzero_index(24) == 29  # 7s -> 3z
    assert tile_count.find_earliest_nonzero_index(32) == 34  # 6z -> end


def test_is_containing_only(tile_count_123m456s78889p33z):
    # Given : tile_count
    tile_count = tile_count_123m456s78889p33z
    indices = [index for index in range(34) if tile_count[index] > 0]

    # Then : is_containing_only works success
    assert tile_count.is_containing_only(indices)
    assert not tile_count.is_containing_only(indices[:-1])
    assert not tile_count.is_containing_only(indices[1:])
    assert tile_count.is_containing_only(indices + [6, 7])

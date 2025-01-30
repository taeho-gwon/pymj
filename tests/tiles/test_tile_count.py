import pytest

from pymj.tiles.tile_count import TileCount


def test_num_tiles():
    # Given: empty tile count
    empty_count = TileCount()

    # Then: count is 0
    assert empty_count.num_tiles == 0

    # Given: "112m" is given
    counts_112m = [0] * 34
    counts_112m[0] = 2
    counts_112m[1] = 1
    tile_count_112m = TileCount(counts_112m)

    # Then: count is 3
    assert tile_count_112m.num_tiles == 3

    # Given: all 34 tile is given
    all_tiles = [1] * 34
    all_tile_count = TileCount(all_tiles)

    # Then: count is 34
    assert all_tile_count.num_tiles == 34


def test_create_from_indices():
    # When: create_from_indices with empty indices list
    empty_count = TileCount.create_from_indices([])

    # Then: all elements are 0
    assert all(empty_count[i] == 0 for i in range(34))
    assert empty_count.num_tiles == 0

    # Given: indices for "112m"
    indices_112m = [0, 0, 1]

    # When: create_from_indices
    tile_count_112m = TileCount.create_from_indices(indices_112m)

    # Then: two 1m, and one 2m
    assert tile_count_112m[0] == 2
    assert tile_count_112m[1] == 1
    assert tile_count_112m[2] == 0

    # Given: indices for all tiles
    all_indices = list(range(34))

    # When: create_from_indices
    all_tile_count = TileCount.create_from_indices(all_indices)

    # Then: all elements are 1
    assert all(all_tile_count[i] == 1 for i in range(34))


def test_create_from_tiles(tiles):
    # When: create_from_indices with empty indices list
    empty_count = TileCount.create_from_tiles([])

    # Then: all elements are 0
    assert all(empty_count[i] == 0 for i in range(34))
    assert empty_count.num_tiles == 0

    # Given: indices for "112m"
    tiles_112m = [tiles["1m"], tiles["1m"], tiles["2m"]]

    # When: create_from_indices
    tile_count_112m = TileCount.create_from_tiles(tiles_112m)

    # Then: two 1m, and one 2m
    assert tile_count_112m[0] == 2
    assert tile_count_112m[1] == 1
    assert tile_count_112m[2] == 0

    # Given: indices for all tiles
    all_tiles = tiles.values()

    # When: create_from_indices
    all_tile_count = TileCount.create_from_tiles(all_tiles)

    # Then: all elements are 1
    assert all(all_tile_count[i] == 1 for i in range(34))


def test_find_earliest_nonzero_index():
    # Given: tile_counts for "14m"
    counts = [1, 0, 0, 1] + [0] * 30
    tile_count = TileCount(counts)

    # Then: earliest nonzero index is 0
    assert tile_count.find_earliest_nonzero_index() == 0

    # Then: earliest nonzero index greater than 1 is 3
    assert tile_count.find_earliest_nonzero_index(1) == 3

    # Then: earliest nonzero index greater than 10 is 34
    assert tile_count.find_earliest_nonzero_index(10) == 34

    # Then: raise error for invalid index
    with pytest.raises(ValueError):
        tile_count.find_earliest_nonzero_index(-1)
    with pytest.raises(ValueError):
        tile_count.find_earliest_nonzero_index(35)


def test_is_containing_only():
    # Given: empty tile count
    empty_count = TileCount()

    # Then: is_containing_only always return True
    assert empty_count.is_containing_only([])
    assert empty_count.is_containing_only([0])
    assert empty_count.is_containing_only([3, 6, 19, 22])

    # Given: tile count for "112m"
    counts = [0] * 34
    counts[0] = 2
    counts[1] = 1
    tile_count = TileCount(counts)

    # Then: is_containing_only for "12m"
    assert not tile_count.is_containing_only([0])
    assert tile_count.is_containing_only([0, 1])
    assert tile_count.is_containing_only([0, 1, 2, 3])
    assert tile_count.is_containing_only([0, 0, 1, 1])

    # Then: raise error for invalid index
    with pytest.raises(IndexError):
        tile_count.is_containing_only([0, 1, 34])

from pymj.tiles.tile_mapping import TileMapping


def test_tile_to_index(tiles):
    # Then: man is [0, 9), pin is [9, 18), sou is [18, 27)
    for value in range(9):
        assert TileMapping.tile_to_index(tiles[str(value + 1) + "m"]) == value
        assert TileMapping.tile_to_index(tiles[str(value + 1) + "p"]) == value + 9
        assert TileMapping.tile_to_index(tiles[str(value + 1) + "s"]) == value + 18

    # Then: honor is [27,34)
    for value in range(7):
        assert TileMapping.tile_to_index(tiles[str(value + 1) + "z"]) == value + 27


def test_index_to_tile(tiles):
    # Then: man is [0, 9), pin is [9, 18), sou is [18, 27)
    for value in range(9):
        assert TileMapping.index_to_tile(value) == tiles[str(value + 1) + "m"]
        assert TileMapping.index_to_tile(value + 9) == tiles[str(value + 1) + "p"]
        assert TileMapping.index_to_tile(value + 18) == tiles[str(value + 1) + "s"]

    # Then: honor is [27,34)
    for value in range(7):
        assert TileMapping.index_to_tile(value + 27) == tiles[str(value + 1) + "z"]

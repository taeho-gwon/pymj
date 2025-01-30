from pymj.tiles.tile_mapping import TileMapping


def test_tile_to_index_and_index_to_tile(tiles):
    tile_index_map = {"1m": 0, "6m": 5, "4p": 12, "9s": 26, "1z": 27, "6z": 32}
    for tile_str, tile_index in tile_index_map.items():
        tile = tiles[tile_str]
        assert TileMapping.tile_to_index(tile) == tile_index
        assert TileMapping.index_to_tile(tile_index) == tile

from pymj.tiles.tileset import Tileset


def test_get_all_tiles():
    # Given : tileset
    tileset = Tileset()

    # Then : tileset tile is 136
    assert len(tileset.get_all_tiles()) == 136


def test_get_all_tiles_iter():
    # Given : tileset
    tileset = Tileset()

    tile_cnt = 0
    for _ in tileset.get_all_tiles_iter():
        tile_cnt += 1

    # Then : tileset tile is 136
    assert tile_cnt == 136

from pymj.tiles.tileset import Tileset


def test_get_all_tiles():
    tileset = Tileset()

    assert len(tileset.get_all_tiles()) == 136


def test_get_all_tiles_iter():
    tileset = Tileset()

    tile_cnt = 0
    for _ in tileset.get_all_tiles_iter():
        tile_cnt += 1

    assert tile_cnt == 136

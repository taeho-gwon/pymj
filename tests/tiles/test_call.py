from contextlib import nullcontext

import pytest

from pymj.enums.call_type import CallType
from pymj.enums.tile_type import TileType
from pymj.tiles.call import Call
from pymj.tiles.tile import Tile


@pytest.mark.parametrize(
    "tiles, call_type, context",
    [
        (
            [Tile(TileType.MAN, 1), Tile(TileType.MAN, 2), Tile(TileType.MAN, 3)],
            CallType.CHII,
            nullcontext(),
        ),
        (
            [Tile(TileType.MAN, 9), Tile(TileType.MAN, 7), Tile(TileType.MAN, 8)],
            CallType.CHII,
            nullcontext(),
        ),
        (
            [Tile(TileType.SOU, 4)] * 3,
            CallType.PON,
            nullcontext(),
        ),
        (
            [Tile(TileType.PIN, 6)] * 4,
            CallType.CONCEALED_KAN,
            nullcontext(),
        ),
        (
            [Tile(TileType.WIND, 3)] * 4,
            CallType.BIG_MELDED_KAN,
            nullcontext(),
        ),
        (
            [Tile(TileType.DRAGON, 2)] * 4,
            CallType.SMALL_MELDED_KAN,
            nullcontext(),
        ),
        (
            [Tile(TileType.SOU, 6)] * 3,
            CallType.CONCEALED_KAN,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.SOU, 6)] * 5,
            CallType.CONCEALED_KAN,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.MAN, 2), Tile(TileType.PIN, 3), Tile(TileType.SOU, 4)],
            CallType.CHII,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.MAN, 7), Tile(TileType.MAN, 8), Tile(TileType.MAN, 8)],
            CallType.CHII,
            pytest.raises(ValueError),
        ),
        (
            [
                Tile(TileType.SOU, 6),
                Tile(TileType.SOU, 7),
                Tile(TileType.SOU, 9),
            ],
            CallType.CHII,
            pytest.raises(ValueError),
        ),
        (
            [
                Tile(TileType.SOU, 6),
                Tile(TileType.PIN, 6),
                Tile(TileType.SOU, 6),
            ],
            CallType.PON,
            pytest.raises(ValueError),
        ),
        (
            [
                Tile(TileType.WIND, 1),
                Tile(TileType.PIN, 1),
                Tile(TileType.DRAGON, 1),
                Tile(TileType.PIN, 1),
            ],
            CallType.BIG_MELDED_KAN,
            pytest.raises(ValueError),
        ),
    ],
)
def test_call(tiles, call_type, context):
    with context:
        Call(tiles, call_type)

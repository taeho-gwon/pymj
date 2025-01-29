from contextlib import nullcontext

import pytest

from pymj.enums.call_type import CallType
from pymj.enums.player_relation import PlayerRelation
from pymj.enums.tile_type import TileType
from pymj.tiles.call import Call
from pymj.tiles.tile import Tile


@pytest.mark.parametrize(
    "tiles, call_type, player_relation, context",
    [
        (
            [Tile(TileType.MAN, 1), Tile(TileType.MAN, 2), Tile(TileType.MAN, 3)],
            CallType.CHII,
            PlayerRelation.PREV,
            nullcontext(),
        ),
        (
            [Tile(TileType.MAN, 1), Tile(TileType.MAN, 2), Tile(TileType.MAN, 3)],
            CallType.CHII,
            PlayerRelation.ACROSS,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.MAN, 9), Tile(TileType.MAN, 7), Tile(TileType.MAN, 8)],
            CallType.CHII,
            PlayerRelation.PREV,
            nullcontext(),
        ),
        (
            [Tile(TileType.SOU, 4)] * 3,
            CallType.PON,
            PlayerRelation.PREV,
            nullcontext(),
        ),
        (
            [Tile(TileType.SOU, 4)] * 3,
            CallType.PON,
            PlayerRelation.SELF,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.PIN, 6)] * 4,
            CallType.CONCEALED_KAN,
            PlayerRelation.SELF,
            nullcontext(),
        ),
        (
            [Tile(TileType.PIN, 6)] * 4,
            CallType.CONCEALED_KAN,
            PlayerRelation.PREV,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.WIND, 3)] * 4,
            CallType.BIG_MELDED_KAN,
            PlayerRelation.PREV,
            nullcontext(),
        ),
        (
            [Tile(TileType.DRAGON, 2)] * 4,
            CallType.SMALL_MELDED_KAN,
            PlayerRelation.PREV,
            nullcontext(),
        ),
        (
            [Tile(TileType.SOU, 6)] * 3,
            CallType.CONCEALED_KAN,
            PlayerRelation.PREV,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.SOU, 6)] * 5,
            CallType.CONCEALED_KAN,
            PlayerRelation.PREV,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.MAN, 2), Tile(TileType.PIN, 3), Tile(TileType.SOU, 4)],
            CallType.CHII,
            PlayerRelation.PREV,
            pytest.raises(ValueError),
        ),
        (
            [Tile(TileType.MAN, 7), Tile(TileType.MAN, 8), Tile(TileType.MAN, 8)],
            CallType.CHII,
            PlayerRelation.PREV,
            pytest.raises(ValueError),
        ),
        (
            [
                Tile(TileType.SOU, 6),
                Tile(TileType.SOU, 7),
                Tile(TileType.SOU, 9),
            ],
            CallType.CHII,
            PlayerRelation.PREV,
            pytest.raises(ValueError),
        ),
        (
            [
                Tile(TileType.SOU, 6),
                Tile(TileType.PIN, 6),
                Tile(TileType.SOU, 6),
            ],
            CallType.PON,
            PlayerRelation.PREV,
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
            PlayerRelation.PREV,
            pytest.raises(ValueError),
        ),
    ],
)
def test_call(tiles, call_type, player_relation, context):
    with context:
        Call(tiles, call_type, player_relation)

from contextlib import nullcontext

import pytest

from pymj.enums.call_type import CallType
from pymj.enums.player_relation import PlayerRelation
from pymj.tiles.call import Call


@pytest.mark.parametrize(
    "tile_strs, call_type, player_relation",
    [
        (
            ["1m", "2m", "3m"],
            CallType.CHII,
            None,
        ),
        (
            ["9m", "7m", "8m"],
            CallType.CHII,
            PlayerRelation.PREV,
        ),
        (
            ["4s", "4s", "4s"],
            CallType.PON,
            PlayerRelation.ACROSS,
        ),
        (
            ["6p", "6p", "6p", "6p"],
            CallType.CONCEALED_KAN,
            None,
        ),
        (
            ["6p", "6p", "6p", "6p"],
            CallType.CONCEALED_KAN,
            PlayerRelation.SELF,
        ),
        (
            ["3z", "3z", "3z", "3z"],
            CallType.BIG_MELDED_KAN,
            PlayerRelation.NEXT,
        ),
        (
            ["6z", "6z", "6z", "6z"],
            CallType.SMALL_MELDED_KAN,
            PlayerRelation.PREV,
        ),
    ],
)
def test_init(tile_strs, call_type, player_relation, tiles):
    # Given: tiles for call and call_type and player_relation
    call_tiles = [tiles[tile_str] for tile_str in tile_strs]

    # Then: initialize success without error
    with nullcontext():
        Call(call_tiles, call_type, player_relation)


@pytest.mark.parametrize(
    "tile_strs, call_type",
    [
        (
            ["1m", "2m", "3m", "4m"],
            CallType.CHII,
        ),
        (
            ["1m", "2m", "3p"],
            CallType.CHII,
        ),
        (
            ["1z", "2z", "3z"],
            CallType.CHII,
        ),
        (
            ["4m", "4m", "4m", "4m"],
            CallType.PON,
        ),
        (
            ["4p", "5p", "4p"],
            CallType.PON,
        ),
        (
            ["1s", "1s", "1s"],
            CallType.CONCEALED_KAN,
        ),
        (
            ["1s", "1s", "1s"],
            CallType.BIG_MELDED_KAN,
        ),
        (
            ["1s", "1s", "1s"],
            CallType.SMALL_MELDED_KAN,
        ),
    ],
)
def test_init_fail_if_invalid_tiles(tile_strs, call_type, tiles):
    # Given: invalid tiles for call and call_type
    call_tiles = [tiles[tile_str] for tile_str in tile_strs]

    # Then: raise error when initialize
    with pytest.raises(ValueError):
        Call(call_tiles, call_type)


@pytest.mark.parametrize(
    "tile_strs, call_type, player_relation",
    [
        (["1m", "2m", "3m"], CallType.CHII, PlayerRelation.ACROSS),
        (["1m", "2m", "3m"], CallType.CHII, PlayerRelation.NEXT),
        (
            ["1m", "2m", "3m"],
            CallType.CHII,
            PlayerRelation.SELF,
        ),
        (
            ["4m", "4m", "4m"],
            CallType.PON,
            PlayerRelation.SELF,
        ),
        (
            ["5p", "5p", "5p", "5p"],
            CallType.CONCEALED_KAN,
            PlayerRelation.PREV,
        ),
        (
            ["5p", "5p", "5p", "5p"],
            CallType.CONCEALED_KAN,
            PlayerRelation.ACROSS,
        ),
        (
            ["5p", "5p", "5p", "5p"],
            CallType.CONCEALED_KAN,
            PlayerRelation.NEXT,
        ),
        (
            ["8s", "8s", "8s", "8s"],
            CallType.BIG_MELDED_KAN,
            PlayerRelation.SELF,
        ),
        (
            ["4z", "4z", "4z", "4z"],
            CallType.SMALL_MELDED_KAN,
            PlayerRelation.SELF,
        ),
    ],
)
def test_init_fail_if_invalid_player_relation(
    tile_strs, call_type, player_relation, tiles
):
    # Given: tiles for call and call type and invalid player relation
    call_tiles = [tiles[tile_str] for tile_str in tile_strs]

    # Then: raise error when initialize
    with pytest.raises(ValueError):
        Call(call_tiles, call_type, player_relation)

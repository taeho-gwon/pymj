import pytest

from pymj.enums.call_type import CallType
from pymj.enums.player_relation import PlayerRelation
from pymj.enums.tile_type import TileType
from pymj.tiles.call import Call
from pymj.tiles.hand import Hand
from pymj.tiles.hand_parser import HandParser
from pymj.tiles.tile import Tile


@pytest.mark.parametrize(
    "tile_str, expected",
    [
        ("1m", Tile(TileType.MAN, 1)),
        ("5m", Tile(TileType.MAN, 5)),
        ("2p", Tile(TileType.PIN, 2)),
        ("9p", Tile(TileType.PIN, 9)),
        ("4s", Tile(TileType.SOU, 4)),
        ("7s", Tile(TileType.SOU, 7)),
        ("1z", Tile(TileType.WIND, 1)),
        ("2z", Tile(TileType.WIND, 2)),
        ("3z", Tile(TileType.WIND, 3)),
        ("4z", Tile(TileType.WIND, 4)),
        ("5z", Tile(TileType.DRAGON, 1)),
        ("6z", Tile(TileType.DRAGON, 2)),
        ("7z", Tile(TileType.DRAGON, 3)),
    ],
)
def test_parse_tile(tile_str, expected):
    # When: parse_tile
    HandParser.parse_tile(tile_str)

    # Then: result is expected
    assert HandParser.parse_tile(tile_str) == expected


@pytest.mark.parametrize(
    "tile_str",
    [
        "11m",
        "03p",
        "8z",
        "m1",
        "1x",
        "1mm",
    ],
)
def test_parse_tile_fail(tile_str):
    # Then: raise error when parse invalid tile
    with pytest.raises(ValueError):
        HandParser.parse_tile(tile_str)


@pytest.mark.parametrize(
    "tile_group_str, expected_strs",
    [
        (
            "92454m",
            [
                "9m",
                "2m",
                "4m",
                "5m",
                "4m",
            ],
        ),
        (
            "1112345678999m",
            [
                "1m",
                "1m",
                "1m",
                "2m",
                "3m",
                "4m",
                "5m",
                "6m",
                "7m",
                "8m",
                "9m",
                "9m",
                "9m",
            ],
        ),
        (
            "22334455667788p",
            [
                "2p",
                "2p",
                "3p",
                "3p",
                "4p",
                "4p",
                "5p",
                "5p",
                "6p",
                "6p",
                "7p",
                "7p",
                "8p",
                "8p",
            ],
        ),
        (
            "22223444466688s",
            [
                "2s",
                "2s",
                "2s",
                "2s",
                "3s",
                "4s",
                "4s",
                "4s",
                "4s",
                "6s",
                "6s",
                "6s",
                "8s",
                "8s",
            ],
        ),
        (
            "1234567z",
            [
                "1z",
                "2z",
                "3z",
                "4z",
                "5z",
                "6z",
                "7z",
            ],
        ),
    ],
)
def test_parse_tile_group(tile_group_str, expected_strs, tiles):
    # When: parse_tile_group
    actual = HandParser.parse_tile_group(tile_group_str)
    expected = [tiles[expected_str] for expected_str in expected_strs]

    # Then: result is expected
    assert actual == expected


@pytest.mark.parametrize(
    "tile_group_str", ["1239p123z", "z1234", "1238z", "1233n", "5645mm"]
)
def test_parse_tile_group_fail(tile_group_str):
    # When: parse_tile_group with invalid string
    # Then: raise error
    with pytest.raises(ValueError):
        HandParser.parse_tile_group(tile_group_str)


@pytest.mark.parametrize(
    "call_str, expected_tile_strs, expected_call_type, expected_player_relation",
    [
        (
            "c<123s",
            ["1s", "2s", "3s"],
            CallType.CHII,
            PlayerRelation.PREV,
        ),
        (
            "p^555p",
            ["5p", "5p", "5p"],
            CallType.PON,
            PlayerRelation.ACROSS,
        ),
        (
            "k_9999m",
            ["9m", "9m", "9m", "9m"],
            CallType.CONCEALED_KAN,
            PlayerRelation.SELF,
        ),
        (
            "b>1111z",
            ["1z", "1z", "1z", "1z"],
            CallType.BIG_MELDED_KAN,
            PlayerRelation.NEXT,
        ),
        (
            "s<6666z",
            ["6z", "6z", "6z", "6z"],
            CallType.SMALL_MELDED_KAN,
            PlayerRelation.PREV,
        ),
    ],
)
def test_parse_call(
    call_str, expected_tile_strs, expected_call_type, expected_player_relation, tiles
):
    # When: parse_call
    actual = HandParser.parse_call(call_str)
    expected_tile = [
        tiles[expected_tile_str] for expected_tile_str in expected_tile_strs
    ]

    # Then: result is expected
    assert actual.tiles == expected_tile
    assert actual.call_type == expected_call_type
    assert actual.player_relation == expected_player_relation


@pytest.mark.parametrize(
    "call_str",
    ["c>123s", "p_123p", "k<1111z", "s1111p<", "x^111z"],
)
def test_parse_call_fail(call_str):
    # When: parse_call with invalid string
    # Then: raise error
    with pytest.raises(ValueError):
        HandParser.parse_call(call_str)


def test_parse_hand(tiles):
    # Given: valid hand string
    hand = Hand()
    tile_strs = ["1m", "2m", "3m", "4m"]
    hand.tiles = [tiles[tile_str] for tile_str in tile_strs]

    call1 = Call(
        [tiles["3z"], tiles["3z"], tiles["3z"]], CallType.PON, PlayerRelation.ACROSS
    )
    call2 = Call([tiles["8p"], tiles["7p"], tiles["9p"]], CallType.CHII)
    hand.calls = [call1, call2]

    hand_str = "1234m,p^333z,c<879p"

    # When: parse_hand
    actual = HandParser.parse_hand(hand_str)

    # Then: result is expected
    assert actual.tiles == hand.tiles

    assert len(actual.calls) == len(hand.calls)
    assert actual.calls[0].tiles == hand.calls[0].tiles
    assert actual.calls[0].call_type == hand.calls[0].call_type
    assert actual.calls[0].player_relation == hand.calls[0].player_relation

    assert actual.calls[1].tiles == hand.calls[1].tiles
    assert actual.calls[1].call_type == hand.calls[1].call_type
    assert actual.calls[1].player_relation == hand.calls[1].player_relation

import pytest

from pymj.enums.call_type import CallType
from pymj.enums.player_relation import PlayerRelation
from pymj.enums.tile_type import TileType
from pymj.tiles.call import Call
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
def test_parse_tile_group(tile_group_str, expected_strs):
    expected_tiles = [
        HandParser.parse_tile(expected_str) for expected_str in expected_strs
    ]
    assert HandParser.parse_tile_group(tile_group_str) == expected_tiles


@pytest.mark.parametrize(
    "tile_group_str", ["1239p123z", "z1234", "1238z", "1233n", "5645mm"]
)
def test_parse_tile_group_fail(tile_group_str):
    with pytest.raises(ValueError):
        HandParser.parse_tile_group(tile_group_str)


@pytest.mark.parametrize(
    "call_str, expected",
    [
        (
            "c<123s",
            Call(
                [Tile(TileType.SOU, 1), Tile(TileType.SOU, 2), Tile(TileType.SOU, 3)],
                CallType.CHII,
            ),
        ),
        (
            "p^555p",
            Call([Tile(TileType.PIN, 5)] * 3, CallType.PON, PlayerRelation.ACROSS),
        ),
        (
            "k_9999m",
            Call(
                [Tile(TileType.MAN, 9)] * 4, CallType.CONCEALED_KAN, PlayerRelation.SELF
            ),
        ),
        (
            "b>1111z",
            Call(
                [Tile(TileType.WIND, 1)] * 4,
                CallType.BIG_MELDED_KAN,
                PlayerRelation.NEXT,
            ),
        ),
        (
            "s<6666z",
            Call(
                [Tile(TileType.DRAGON, 2)] * 4,
                CallType.SMALL_MELDED_KAN,
                PlayerRelation.PREV,
            ),
        ),
    ],
)
def test_parse_call(call_str, expected):
    assert HandParser.parse_call(call_str) == expected


@pytest.mark.parametrize(
    "call_str",
    ["c>123s", "p_123p", "k<1111z", "s1111p<", "x^111z"],
)
def test_parse_call_fail(call_str):
    with pytest.raises(ValueError):
        HandParser.parse_call(call_str)


def test_parse_hand(hand_123m456s78889p33z):
    expected = hand_123m456s78889p33z
    hand = HandParser.parse_hand("123m456s78889p33z")

    assert hand.tiles == expected.tiles
    assert hand.calls == expected.calls
    assert hand.drawn_tile == expected.drawn_tile

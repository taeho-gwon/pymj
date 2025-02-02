import pytest

from pymj.hand_checker.seven_pair_checker import SevenPairChecker
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.hand_parser import HandParser


@pytest.mark.skip
def test_calculate_divisions():
    raise AssertionError()


@pytest.mark.parametrize(
    "hand_str, agari_tile, expected_shanten",
    [
        ("1122334455667m", "7m", -1),
        ("1122334455667m", "1m", 0),
        ("1112233445566m", "1m", 1),
        ("1112233445566m", None, 1),
        ("1122334455677m", None, 0),
    ],
)
def test_calculate_shanten(hand_str, agari_tile, expected_shanten, tiles):
    hand = HandParser.parse_hand(hand_str)
    tile = tiles[agari_tile] if agari_tile else None
    hand_info = HandInfo.create_from_hand(hand, tile, True)

    seven_pair_checker = SevenPairChecker()

    assert seven_pair_checker.calculate_shanten(hand_info) == expected_shanten

import pytest

from pymj.enums.division_part_type import DivisionPartType
from pymj.enums.wait_type import WaitType
from pymj.hand_checker.seven_pair_checker import SevenPairChecker
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.hand_parser import HandParser


def test_calculate_divisions(tiles):
    # Given: hand info and seven pair checker
    hand = HandParser.parse_hand("1122334455667m")
    hand.draw_tile(tiles["7m"])
    hand_info = HandInfo.create_from_hand(hand, None, True)
    seven_pair_checker = SevenPairChecker()

    # When: calculate_divisions
    divisions = seven_pair_checker.calculate_divisions(hand_info)

    # Then: one division
    assert len(divisions) == 1

    # Then: single wait
    assert divisions[0].wait_type is WaitType.SINGLE_WAIT

    # Then all part is head
    assert all(part.type == DivisionPartType.HEAD for part in divisions[0].parts)


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
    # Given: hand info and seven pair checker
    hand = HandParser.parse_hand(hand_str)
    tile = tiles[agari_tile] if agari_tile else None
    hand_info = HandInfo.create_from_hand(hand, tile, True)
    seven_pair_checker = SevenPairChecker()

    # Then: result of calculate shanten is expected
    assert seven_pair_checker.calculate_shanten(hand_info) == expected_shanten

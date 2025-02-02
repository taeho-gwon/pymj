import pytest

from pymj.enums.division_part_type import DivisionPartType
from pymj.enums.wait_type import WaitType
from pymj.hand_checker.thirteen_orphan_checker import ThirteenOrphanChecker
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.hand_parser import HandParser


def test_calculate_divisions(tiles):
    # Given: hand info and seven pair checker
    hand = HandParser.parse_hand("19m19p19s1234567z")
    hand.draw_tile(tiles["7z"])
    hand_info = HandInfo.create_from_hand(hand)
    thirteen_orphan_checker = ThirteenOrphanChecker()

    # When: calculate_divisions
    divisions = thirteen_orphan_checker.calculate_divisions(hand_info)

    # Then: one division
    assert len(divisions) == 1

    # Then: 13wait
    assert divisions[0].wait_type is WaitType.THIRTEEN_ORPHANS_13WAIT

    # Then: thirteen orphans part type
    assert len(divisions[0].parts) == 1
    assert divisions[0].parts[0].type is DivisionPartType.THIRTEEN_ORPHANS


@pytest.mark.parametrize(
    "hand_str, expected_shanten",
    [
        ("123m456p789s1112z", 8),
        ("123m456p789s11122z", 8),
        ("135m466p479s1122z", 8),
        ("334m33889p1457s4z", 10),
        ("3558m4p25668s345z", 10),
        ("1199m4p1147s13457z", 4),
        ("1199m1199p1199s12z", 4),
        ("19m149s18p1223456z", 1),
        ("69m5678p2789s344z7p", 8),
        ("119m19p19s1234567z", -1),
    ],
)
def test_calculate_shanten(hand_str, expected_shanten):
    # Given: hand info and thirteen orphan checker
    hand = HandParser.parse_hand(hand_str)
    if len(hand.tiles) == 14:
        hand.draw_tile(hand.tiles[-1])
        hand.discard_tile(13)

    hand_info = HandInfo.create_from_hand(hand)
    thirteen_orphan_checker = ThirteenOrphanChecker()

    # Then: result of calculate shanten is expected
    assert thirteen_orphan_checker.calculate_shanten(hand_info) == expected_shanten

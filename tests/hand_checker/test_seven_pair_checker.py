import pytest

from pymj.enums.division_part_type import DivisionPartType
from pymj.enums.efficiency_data import EfficiencyData
from pymj.enums.wait_type import WaitType
from pymj.hand_checker.seven_pair_checker import SevenPairChecker
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.hand_parser import HandParser
from pymj.tiles.tile_mapping import TileMapping


def test_calculate_divisions(tiles):
    # Given: hand info and seven pair checker
    hand = HandParser.parse_hand("1122334455667m")
    hand.draw_tile(tiles["7m"])
    hand_info = HandInfo.create_from_hand(hand)
    seven_pair_checker = SevenPairChecker()

    # When: calculate_divisions
    divisions = seven_pair_checker.calculate_divisions(hand_info)

    # Then: one division
    assert len(divisions) == 1

    # Then: single wait
    assert divisions[0].wait_type is WaitType.SINGLE_WAIT

    # Then: all seven parts are head
    assert len(divisions[0].parts) == 7
    assert all(part.type == DivisionPartType.HEAD for part in divisions[0].parts)


@pytest.mark.parametrize(
    "hand_str, expected_shanten",
    [
        ("11223344556677m", -1),
        ("11122334455667m", 0),
        ("11112233445566m", 1),
        ("1112233445566m", 1),
        ("1122334455677m", 0),
    ],
)
def test_calculate_shanten(hand_str, expected_shanten):
    # Given: hand info and seven pair checker
    hand = HandParser.parse_hand(hand_str)
    if len(hand.tiles) == 14:
        hand.draw_tile(hand.tiles[-1])
        hand.discard_tile(13)

    hand_info = HandInfo.create_from_hand(hand)
    seven_pair_checker = SevenPairChecker()

    # Then: result of calculate shanten is expected
    assert seven_pair_checker.calculate_shanten(hand_info) == expected_shanten


@pytest.mark.parametrize(
    "hand_str, expected",
    [
        (
            "1188m557889p4466s",
            [
                ("7p", ["9p"], 3),
                ("9p", ["7p"], 3),
            ],
        ),
        (
            "11789m6789p45566s",
            [
                ("7m", ["8m", "9m", "6p", "7p", "8p", "9p", "4s"], 21),
                ("8m", ["7m", "9m", "6p", "7p", "8p", "9p", "4s"], 21),
                ("9m", ["7m", "8m", "6p", "7p", "8p", "9p", "4s"], 21),
                ("6p", ["7m", "8m", "9m", "7p", "8p", "9p", "4s"], 21),
                ("7p", ["7m", "8m", "9m", "6p", "8p", "9p", "4s"], 21),
                ("8p", ["7m", "8m", "9m", "6p", "7p", "9p", "4s"], 21),
                ("9p", ["7m", "8m", "9m", "6p", "7p", "8p", "4s"], 21),
                ("4s", ["7m", "8m", "9m", "6p", "7p", "8p", "9p"], 21),
            ],
        ),
    ],
)
def test_calculate_efficiency(hand_str, expected, tiles):
    hand = HandParser.parse_hand(hand_str)
    hand.draw_tile(hand.tiles[-1])
    hand.discard_tile(13)
    hand_info = HandInfo.create_from_hand(hand)

    expected_efficiency = [
        EfficiencyData(
            discard_tile=TileMapping.tile_to_index(tiles[discard_tile_code]),
            ukeire=[
                TileMapping.tile_to_index(tiles[ukeire]) for ukeire in ukeire_codes
            ],
            num_ukeire=num_ukeire,
        )
        for discard_tile_code, ukeire_codes, num_ukeire in expected
    ]

    seven_pair_checker = SevenPairChecker()
    assert seven_pair_checker.calculate_efficiency(hand_info) == expected_efficiency

import pytest

from pymj.enums.efficiency_data import EfficiencyData
from pymj.enums.wait_type import WaitType
from pymj.hand_checker.normal_form_checker import NormalFormChecker
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.hand_parser import HandParser
from pymj.tiles.tile_mapping import TileMapping


@pytest.mark.parametrize(
    "hand_str, expected_shanten",
    [
        ("123m456p789s1112z", 0),
        ("123m456p789s1111z", 1),
        ("123m4569999p789s", 1),
        ("123m456p789s11122z", -1),
        ("135m466p479s1122z", 3),
        ("334m33889p1457s4z", 4),
        ("3558m4p25668s345z", 5),
        ("1199m4p1147s13457z", 5),
        ("1199m1199p1199s12z", 3),
        ("19m149s18p1223456z", 7),
        ("69m5678p2789s344z7p", 2),
        ("9m5678p12789s344z7p", 1),
    ],
)
def test_calculate_shanten(hand_str, expected_shanten):
    # Given: hand info and seven pair checker
    hand = HandParser.parse_hand(hand_str)
    if len(hand.tiles) == 14:
        hand.draw_tile(hand.tiles[-1])
        hand.discard_tile(13)

    hand_info = HandInfo.create_from_hand(hand)
    normal_form_checker = NormalFormChecker()

    # Then: result of calculate shanten is expected
    assert normal_form_checker.calculate_shanten(hand_info) == expected_shanten


def test_calculate_divisions(tiles):
    # Given: hand info and seven pair checker
    hand = HandParser.parse_hand("12345689m123p99s")
    hand.draw_tile(tiles["7m"])
    hand_info = HandInfo.create_from_hand(hand)
    hand_info.is_tsumo = False
    normal_form_checker = NormalFormChecker()

    # When: calculate_divisions
    divisions = normal_form_checker.calculate_divisions(hand_info)

    # Then: one division
    assert len(divisions) == 1

    # Then: edge wait
    assert divisions[0].wait_type is WaitType.EDGE_WAIT

    # Then: five parts exist
    assert len(divisions[0].parts) == 5


@pytest.mark.parametrize(
    "hand_str, expected",
    [
        (
            "69m5678p2789s344z7p",
            [
                (
                    "9m",
                    [
                        "4m",
                        "5m",
                        "6m",
                        "7m",
                        "8m",
                        "6p",
                        "9p",
                        "1s",
                        "2s",
                        "3s",
                        "4s",
                        "3z",
                        "4z",
                    ],
                    46,
                ),
                (
                    "3z",
                    [
                        "4m",
                        "5m",
                        "6m",
                        "7m",
                        "8m",
                        "9m",
                        "6p",
                        "9p",
                        "1s",
                        "2s",
                        "3s",
                        "4s",
                        "4z",
                    ],
                    46,
                ),
                (
                    "6m",
                    ["7m", "8m", "9m", "6p", "9p", "1s", "2s", "3s", "4s", "3z", "4z"],
                    38,
                ),
                (
                    "2s",
                    ["4m", "5m", "6m", "7m", "8m", "9m", "6p", "9p", "3z", "4z"],
                    34,
                ),
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

    normal_form_checker = NormalFormChecker()
    assert normal_form_checker.calculate_efficiency(hand_info) == expected_efficiency

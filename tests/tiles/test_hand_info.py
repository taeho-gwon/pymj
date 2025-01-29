from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile_count import TileCount


def test_create_from_hand(hand_123m456s78889p33z):
    # Given : hand info is given
    hand = hand_123m456s78889p33z
    hand_info = HandInfo.create_from_hand(hand)

    # Then : hand info created ok
    expected_concealed_count = TileCount.create_from_tiles(hand.tiles)
    expected_call_counts = [
        (call.call_type, TileCount.create_from_tiles(call.tiles)) for call in hand.calls
    ]

    assert hand_info.concealed_count == expected_concealed_count
    assert hand_info.call_counts == expected_call_counts


def test_total_count(hand_123m456s78889p33z):
    # Given : hand info is given
    hand = hand_123m456s78889p33z
    hand_info = HandInfo.create_from_hand(hand)

    expected = TileCount.create_from_tiles(hand.tiles)
    # Then : total count is ok
    assert hand_info.total_count == expected

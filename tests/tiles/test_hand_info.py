from pymj.enums.call_type import CallType
from pymj.tiles.call import Call
from pymj.tiles.hand import Hand
from pymj.tiles.hand_info import HandInfo


def test_create_from_hand(tiles):
    # Given: hand with calls
    hand = Hand()
    hand_tiles = ["1m", "2m", "3m"]
    for tile_str in hand_tiles:
        hand.draw_tile(tiles[tile_str])
        hand.append_drawn_tile()

    hand.calls.append(Call([tiles["3z"]] * 3, CallType.PON))
    hand.calls.append(Call([tiles["4p"]] * 4, CallType.BIG_MELDED_KAN))

    # When: create from hand
    hand_info = HandInfo.create_from_hand(hand)

    # Then: hand info created ok
    assert hand_info.concealed_count[0] == 1  # 0 -> 1m
    assert hand_info.concealed_count[1] == 1  # 1 -> 2m
    assert hand_info.concealed_count[2] == 1  # 2 -> 3m

    assert hand_info.call_counts[0][0] == CallType.PON
    assert hand_info.call_counts[0][1][29] == 3  # 29 -> 3z(West)

    assert hand_info.call_counts[1][0] == CallType.BIG_MELDED_KAN
    assert hand_info.call_counts[1][1][12] == 4  # 12 -> 4p


def test_total_count(tiles):
    # Given: hand info is given
    hand = Hand()
    hand_tiles = ["1m", "2m", "3m"]
    for tile_str in hand_tiles:
        hand.draw_tile(tiles[tile_str])
        hand.append_drawn_tile()

    hand.calls.append(Call([tiles["3z"]] * 3, CallType.PON))
    hand.calls.append(Call([tiles["4p"]] * 4, CallType.BIG_MELDED_KAN))
    hand_info = HandInfo.create_from_hand(hand)

    # When: total_count
    actual = hand_info.total_count

    # Then: actual result is valid
    assert actual[0] == 1  # 0 -> 1m
    assert actual[1] == 1  # 1 -> 2m
    assert actual[2] == 1  # 2 -> 3m
    assert actual[29] == 3  # 29 -> 3z(West)
    assert actual[12] == 4  # 12 -> 4p

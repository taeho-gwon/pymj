from pymj.tiles.agari_hand_info import AgariHandInfo
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile_count import TileCount


def test_create_from_hand(hand_123m456s78889p33z, tiles):
    # Given: agari hand info from hand with agari tile
    hand = hand_123m456s78889p33z
    agari_tile = tiles["3z"]
    hand.draw_tile(agari_tile)
    agari_hand_info = AgariHandInfo.create_from_hand(hand)

    # Then : created agari hand info is from hand
    assert agari_hand_info.agari_tile == agari_tile
    expected_hand_info = HandInfo.create_from_hand(hand, False)

    assert agari_hand_info.hand_info == expected_hand_info


def test_total_count(hand_123m456s78889p33z, tiles):
    # Given: agari hand info from hand with agari tile
    hand = hand_123m456s78889p33z
    agari_tile = tiles["3z"]
    hand.draw_tile(agari_tile)
    agari_hand_info = AgariHandInfo.create_from_hand(hand)

    expected = TileCount.create_from_tiles(hand.tiles + [agari_tile])

    # Then: total count is ok
    assert agari_hand_info.total_count == expected

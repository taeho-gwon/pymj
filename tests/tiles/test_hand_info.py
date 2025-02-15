import pytest

from pymj.tiles.hand import Hand
from pymj.tiles.hand_info import HandInfo
from pymj.tiles.tile_mapping import TileMapping


def test_create_from_hand(tiles):
    # Given : empty hand and agari tile
    hand = Hand()
    agari_tile = tiles["3z"]
    hand.draw_tile(agari_tile)

    # When : create_from_hand
    agari_hand_info = HandInfo.create_from_hand(hand, is_tsumo=True)

    # Then : attributes are expected
    assert agari_hand_info.agari_tile == agari_tile
    assert agari_hand_info.is_tsumo


def test_create_from_hand_fail(tiles):
    # Given: empty hand and agari tile
    hand = Hand()
    hand.draw_tile(tiles["3z"])

    # Then: raise error if both drawn_tile and agari_tile are exist.
    with pytest.raises(ValueError):
        HandInfo.create_from_hand(hand, tiles["3m"])


def test_total_count(tiles):
    # Given: agari hand info
    tile_1m = tiles["1m"]
    agari_hand_info = HandInfo(agari_tile=tile_1m)

    # When: total_count
    total_count = agari_hand_info.total_count

    # Then: 1
    index_1m = TileMapping.tile_to_index(tile_1m)
    assert total_count[index_1m] == 1

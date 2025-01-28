from contextlib import nullcontext

import pytest


def test_draw_tile(hand_123m456s78889p33z, tiles):
    # Given: hand and drawn_tile
    hand = hand_123m456s78889p33z
    drawn_tile = tiles["8p"]

    # Then: draw success
    with nullcontext():
        hand.draw_tile(drawn_tile)

    # Then: draw fail when double draw
    with pytest.raises(ValueError):
        hand.draw_tile(drawn_tile)


def test_discard_tile(hand_123m456s78889p33z, tiles):
    # Given: hand and drawn_tile
    hand = hand_123m456s78889p33z
    drawn_tile = tiles["8p"]

    # Then: discard fail when draw tile is None
    with pytest.raises(ValueError):
        hand.discard_tile()

    # Then: discard success
    with nullcontext():
        hand.draw_tile(drawn_tile)
        assert hand.discard_tile() == drawn_tile
        assert hand.drawn_tile is None


def test_append_drawn_tile(hand_123m456s78889p33z, tiles):
    # Given: hand and drawn_tile and draw it
    hand = hand_123m456s78889p33z
    original_tiles = hand_123m456s78889p33z.tiles[:]
    drawn_tile = tiles["8p"]
    hand.draw_tile(drawn_tile)

    # When: append_drawn_tile
    hand.append_drawn_tile()

    # Then: drawn tile append success
    assert hand.tiles == original_tiles + [drawn_tile]

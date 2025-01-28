from contextlib import nullcontext

import pytest


def test_draw_tile(hand_123m456s78889p33z, tiles):
    hand = hand_123m456s78889p33z
    drawn_tile = tiles["8p"]

    with nullcontext():
        hand.draw_tile(drawn_tile)

    with pytest.raises(ValueError):
        hand.draw_tile(drawn_tile)


def test_discard_tile(hand_123m456s78889p33z, tiles):
    hand = hand_123m456s78889p33z
    drawn_tile = tiles["8p"]
    with pytest.raises(ValueError):
        hand.discard_tile()

    with nullcontext():
        hand.draw_tile(drawn_tile)
        assert hand.discard_tile() == drawn_tile
        assert hand.drawn_tile is None


def test_append_drawn_tile(hand_123m456s78889p33z, tiles):
    hand = hand_123m456s78889p33z
    original_tiles = hand_123m456s78889p33z.tiles[:]
    drawn_tile = tiles["8p"]

    hand.draw_tile(drawn_tile)
    hand.append_drawn_tile()
    assert hand.tiles == original_tiles + [drawn_tile]

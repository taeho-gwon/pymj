from contextlib import nullcontext

import pytest

from pymj.tiles.hand import Hand


def test_draw_tile(tiles):
    # Given: hand and drawn_tile
    hand = Hand()
    drawn_tile = tiles["8p"]

    # Then: draw without errors
    with nullcontext():
        hand.draw_tile(drawn_tile)

    # Then: draw fail when double draw
    with pytest.raises(ValueError):
        hand.draw_tile(drawn_tile)


def test_discard_tile(tiles):
    # Given: hand and drawn_tile
    hand = Hand()
    drawn_tile = tiles["8p"]

    # Then: discard fail when draw tile is None
    with pytest.raises(ValueError):
        hand.discard_tile()

    # Then: discard without errors
    with nullcontext():
        hand.draw_tile(drawn_tile)
        assert hand.discard_tile() == drawn_tile
        assert hand.drawn_tile is None


def test_append_drawn_tile(tiles):
    # Given: hand and drawn_tile and draw it
    hand = Hand()
    drawn_tile = tiles["8p"]
    hand.draw_tile(drawn_tile)

    # When: append_drawn_tile
    hand.append_drawn_tile()

    # Then: drawn tile append successfully
    assert hand.tiles == [drawn_tile]

    # Given : new drawn_tile and draw it
    drawn_tile2 = tiles["3z"]
    hand.draw_tile(drawn_tile2)

    # When: append_drawn_tile
    hand.append_drawn_tile()

    # Then: second drawn tile append successfully
    assert hand.tiles == [drawn_tile, drawn_tile2]

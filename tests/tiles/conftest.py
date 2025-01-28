import pytest

from pymj.enums.tile_type import TileType
from pymj.tiles.hand import Hand
from pymj.tiles.tile import Tile


@pytest.fixture
def tiles():
    """Fixture for tiles by string."""
    mans = {str(value) + "m": Tile(TileType.MAN, value) for value in range(1, 10)}
    pins = {str(value) + "p": Tile(TileType.PIN, value) for value in range(1, 10)}
    sous = {str(value) + "s": Tile(TileType.SOU, value) for value in range(1, 10)}
    winds = {str(value) + "z": Tile(TileType.WIND, value) for value in range(1, 5)}
    dragons = {
        str(value + 4) + "z": Tile(TileType.DRAGON, value) for value in range(1, 4)
    }

    return mans | pins | sous | winds | dragons


@pytest.fixture
def hand_123m456s78889p33z(tiles):
    """Fixture for ready-made hand."""
    hand = Hand()
    tile_str = "1m2m3m4s5s6s7p8p8p8p9p3z3z"
    hand.tiles = [
        tiles[tile_num + tile_type]
        for tile_num, tile_type in zip(tile_str[::2], tile_str[1::2], strict=False)
    ]

    return hand

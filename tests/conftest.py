import pytest

from pymj.enums.tile_type import TileType
from pymj.tiles.tile import Tile


@pytest.fixture
def tiles():
    mans = {str(value) + "m": Tile(TileType.MAN, value) for value in range(1, 10)}
    pins = {str(value) + "p": Tile(TileType.PIN, value) for value in range(1, 10)}
    sous = {str(value) + "s": Tile(TileType.SOU, value) for value in range(1, 10)}
    winds = {str(value) + "z": Tile(TileType.WIND, value) for value in range(1, 5)}
    dragons = {
        str(value + 4) + "z": Tile(TileType.DRAGON, value) for value in range(1, 4)
    }

    return mans | pins | sous | winds | dragons

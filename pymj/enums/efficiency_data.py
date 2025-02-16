from __future__ import annotations

from dataclasses import dataclass

from pymj.tiles.tile_index import TileIndex


@dataclass
class EfficiencyData:
    """Store information about a discard's efficiency and potential useful tiles.

    Attributes:
        discard_tile (int): ID of the tile considered for discard.
        ukeire (list[int]): List of tile IDs that would improve the hand after discard.
        num_ukeire (int): Total count of useful tiles after discard.

    """

    discard_tile: TileIndex
    ukeire: list[TileIndex]
    num_ukeire: int

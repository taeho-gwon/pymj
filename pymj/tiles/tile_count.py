from __future__ import annotations

from typing import Iterable, Iterator, Sequence, SupportsIndex, overload

from pymj.tiles.tile import Tile
from pymj.tiles.tile_mapping import TileMapping


class TileCount:
    """Represent length 34 list for counting tiles.

    indices are following.
    Man : 0~8
    Pin : 9~17
    Sou : 18~26
    Wind : 27~30
    Dragon : 31~33

    Examples
    --------
        "1112345678999m" -> [3, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, ...]

    """

    def __init__(self, counts: list[int] | None = None) -> None:
        """Initialize tile count class."""
        self._counts: list[int] = counts if counts else [0] * 34

    @property
    def num_tiles(self) -> int:
        """Calculate all number of tiles.

        Returns
        -------
            sum of self.counts

        """
        return sum(self._counts)

    @staticmethod
    def create_from_indices(tiles: Iterable[int]) -> TileCount:
        """Create TileCount class from tile indices.

        Args:
        ----
            tiles: indices of tiles

        Returns:
        -------
            TileCount class containing info of given indices.

        """
        tile_count = TileCount()
        for tile in tiles:
            tile_count[tile] += 1
        return tile_count

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile]) -> TileCount:
        """Create TileCount class from tiles.

        Tile version of create_from_indices

        Args:
        ----
            tiles: indices of tiles

        Returns:
        -------
            TileCount class containing info of given indices.

        """
        return TileCount.create_from_indices(
            TileMapping.tile_to_index(tile) for tile in tiles
        )

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, TileCount):
            return NotImplemented
        return self._counts == other._counts

    def __add__(self, other: TileCount) -> TileCount:
        return TileCount(
            [count1 + count2 for count1, count2 in zip(self, other, strict=False)]
        )

    @overload
    def __getitem__(self, index: SupportsIndex) -> int: ...

    @overload
    def __getitem__(self, index: slice) -> list[int]: ...

    def __getitem__(self, idx: SupportsIndex | slice) -> int | list[int]:
        return self._counts[idx]

    def __setitem__(self, index: SupportsIndex, value: int) -> None:
        self._counts[index] = value

    def __iter__(self) -> Iterator[int]:
        return iter(self._counts)

    def find_earliest_nonzero_index(self, index: int = 0) -> int:
        """Return earliest nonzero index in TileCount great or equal than index.

        Args:
        ----
            index: start index for searching

        Returns:
        -------
            earliest nonzero index of self._counts which is bigger than index.
            if all elements are zero, return len(self._counts) == 34

        """
        while index < len(self._counts) and self._counts[index] == 0:
            index += 1
        return index

    def is_containing_only(self, indices: Sequence[int]) -> bool:
        """Check values are all zero not contained in given indices.

        Args:
        ----
            indices: indices for check containing only

        Returns:
        -------
            True if all index not in indices is zero.
            else False

        """
        return sum(self._counts[index] for index in indices) == sum(self._counts)

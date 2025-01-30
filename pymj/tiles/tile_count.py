from __future__ import annotations

from typing import Iterable, Iterator, Sequence, SupportsIndex, overload

from pymj.tiles.tile import Tile
from pymj.tiles.tile_mapping import TileMapping


class TileCount:
    """A class for counting mahjong tiles using a fixed-length array representation.

    This class tracks the count of each tile type using a 34-length array.
    Each index in the array corresponds to a specific tile type,
    and the value at that index represents the count of that tile type.

    The 34 indices are organized as follows:
    - Man    : 0-8    (1-9)
    - Pin    : 9-17   (1-9)
    - Sou    : 18-26  (1-9)
    - Wind   : 27-30  (East, South, West, North)
    - Dragon : 31-33  (White, Green, Red)

    This representation allows for efficient operations like checking hand completeness,
    calculating tile combinations.

    Attributes
    ----------
    _counts : list[int]
        A list of 34 integers representing the count of each tile type.
        Each value represents how many of that specific tile are present.

    Examples
    --------
    Creating a TileCount from a typical hand string:
        "1112345678999m" represents a hand with:
        This would be represented as: [3,1,1,1,1,1,1,1,3,0,0,...]

    """

    def __init__(self, counts: list[int] | None = None) -> None:
        """Initialize a new TileCount instance with optional initial counts.

        Creates a new TileCount object either with a provided list of counts or
        initializes a new empty count list (all zeros). When providing initial counts,
        the list is copied to prevent unintended modifications to the original data.

        Parameters
        ----------
        counts : list[int] | None, optional
            Initial tile counts to use. If provided, must be a list of 34 integers.
            If None, initializes all counts to 0. Default is None.

        Raises
        ------
        ValueError
            If the provided counts list does not have exactly 34 elements.
            This is required because tiles are represented by 34 unique types,
            and each position in the list corresponds to a specific tile type.

        """
        if counts is None:
            self._counts = [0] * 34
        else:
            if len(self._counts) != 34:
                raise ValueError
            self._counts = counts[:]

    @property
    def num_tiles(self) -> int:
        """Calculate the total number of tiles represented in this count.

        This property sums all tile counts to determine the total number of
        tiles present. This is useful for validating hand sizes and checking
        completion conditions in mahjong rules.

        Returns
        -------
        int
            The total number of tiles across all tile types.

        Examples
        --------
        >>> tc = TileCount([1,1,1,0,0,0,0,0,0] + [0]*25)  # Three tiles
        >>> tc.num_tiles
        3

        """
        return sum(self._counts)

    @staticmethod
    def create_from_indices(tiles: Iterable[int]) -> TileCount:
        """Create a new TileCount instance from a sequence of tile indices.

        This factory method creates a TileCount object by counting occurrences
        of each tile index in the provided sequence. This is useful when working
        with tile representations that use index numbers rather than Tile objects.

        Parameters
        ----------
        tiles : Iterable[int]
            A sequence of tile indices (0-33) to count.
            Each index should correspond to the standard tile mapping:
            - 0-8   : Man
            - 9-17  : Pin
            - 18-26 : Sou
            - 27-30 : Wind
            - 31-33 : Dragon

        Returns
        -------
        TileCount
            A new TileCount instance containing the counts of the provided indices.

        Examples
        --------
        >>> # Create a count with two 1-man (index 0) and one 2-man (index 1)
        >>> tc = TileCount.create_from_indices([0, 0, 1])
        >>> tc[0]  # Count of 1-man
        2

        """
        tile_count = TileCount()
        for tile in tiles:
            tile_count[tile] += 1
        return tile_count

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile]) -> TileCount:
        """Create a new TileCount instance from a sequence of Tile objects.

        Similar to create_from_indices, but accepts Tile objects instead of
        raw indices. This method converts each Tile object to its corresponding
        index using TileMapping before counting.

        Parameters
        ----------
        tiles : Iterable[Tile]
            A sequence of Tile objects to count.

        Returns
        -------
        TileCount
            A new TileCount instance containing the counts of the provided tiles.

        Examples
        --------
        >>> # Assuming Tile objects for 1-man are created
        >>> tiles = [Tile(TileType.MAN, 1)] * 2 + [Tile(TileType.MAN, 2)]
        >>> tc = TileCount.create_from_tiles(tiles)
        >>> tc[0]  # Count of 1-man
        2

        """
        return TileCount.create_from_indices(
            TileMapping.tile_to_index(tile) for tile in tiles
        )

    def __eq__(self, other: object) -> bool:
        """Compare this TileCount instance with another for equality.

        Two TileCount instances are considered equal if they have identical
        counts for all tile types.

        Parameters
        ----------
        other : object
            The object to compare with this TileCount instance.

        Returns
        -------
        bool
            True if other is a TileCount instance with identical counts,
            False otherwise.

        Examples
        --------
        >>> tc1 = TileCount([1,1,1] + [0]*31)
        >>> tc2 = TileCount([1,1,1] + [0]*31)
        >>> tc1 == tc2
        True

        """
        if not isinstance(other, TileCount):
            return False
        return self._counts == other._counts

    def __add__(self, other: TileCount) -> TileCount:
        """Add two TileCount instances element-wise.

        Creates a new TileCount instance where each count is the sum of
        the corresponding counts from both operands.

        Parameters
        ----------
        other : TileCount
            The TileCount instance to add to this one.

        Returns
        -------
        TileCount
            A new TileCount instance with summed counts.

        Examples
        --------
        >>> tc1 = TileCount([1,0,0] + [0]*31)
        >>> tc2 = TileCount([1,1,0] + [0]*31)
        >>> tc3 = tc1 + tc2
        >>> tc3[0]  # 1 + 1 = 2
        2

        """
        return TileCount(
            [count1 + count2 for count1, count2 in zip(self, other, strict=False)]
        )

    @overload
    def __getitem__(self, key: SupportsIndex) -> int: ...

    @overload
    def __getitem__(self, key: slice) -> list[int]: ...

    def __getitem__(self, key: SupportsIndex | slice) -> int | list[int]:
        """Access tile counts using index or slice notation.

        Provides direct access to tile counts using standard Python indexing.
        Supports both single index access and slicing operations.

        Parameters
        ----------
        key : SupportsIndex | slice
            Either a single index (0-33) or a slice object.
            - Single index returns the count for that specific tile type
            - Slice returns a list of counts for the specified range

        Returns
        -------
        int | list[int]
            For single index: the count of the specified tile type
            For slice: a list of counts for the specified range

        Examples
        --------
        >>> tc = TileCount([1,2,3] + [0]*31)
        >>> tc[0]  # Single index access
        1
        >>> tc[0:3]  # Slice access
        [1, 2, 3]

        """
        return self._counts[key]

    def __setitem__(self, key: SupportsIndex, value: int) -> None:
        """Set the count for a specific tile type.

        Parameters
        ----------
        key : SupportsIndex
            The index (0-33) of the tile type to modify
        value : int
            The new count value to set

        Examples
        --------
        >>> tc = TileCount()
        >>> tc[0] = 2  # Set count of 1-man to 2

        """
        self._counts[key] = value

    def __iter__(self) -> Iterator[int]:
        """Create an iterator over the tile counts.

        Enables iteration over all tile counts in sequence, useful for
        processing all tile types in order.

        Returns
        -------
        Iterator[int]
            An iterator yielding counts for each tile type from index 0 to 33

        Examples
        --------
        >>> tc = TileCount([1,1,1] + [0]*31)
        >>> list(tc)  # Convert iterator to list
        [1, 1, 1, 0, 0, ...]

        """
        return iter(self._counts)

    def find_earliest_nonzero_index(self, index: int = 0) -> int:
        """Find the first index with a non-zero count, starting from a given position.

        This method searches through the counts array from the specified starting
        index and returns the first position where the count is greater than zero.
        This is particularly useful for iterating through tiles in sequential order
        while skipping empty positions.

        Parameters
        ----------
        index : int, optional
            The starting position for the search. Default is 0.

        Returns
        -------
        int
            The first index >= start_index where count > 0.
            Returns 34 if no non-zero counts are found.

        Examples
        --------
        >>> tc = TileCount([0,0,1,0,2,0] + [0]*28)  # Counts at index 2 and 4
        >>> tc.find_earliest_nonzero_index()
        2
        >>> tc.find_earliest_nonzero_index(3)
        4

        """
        while index < len(self._counts) and self._counts[index] == 0:
            index += 1
        return index

    def is_containing_only(self, indices: Sequence[int]) -> bool:
        """Check if non-zero counts appear only at specified indices.

        This method verifies that all tiles in the count are accounted for
        by the provided indices. This is useful for checking if a hand
        contains only specific types of tiles, such as verifying suit purity
        or checking for special hand patterns.

        Parameters
        ----------
        indices : Sequence[int]
            The indices to check for non-zero counts.
            All other indices must have zero counts for the method to return True.

        Returns
        -------
        bool
            True if all non-zero counts appear only at the specified indices,
            False otherwise.

        Examples
        --------
        >>> tc = TileCount([1,1,1,0,0,0,0,0,0] + [0]*25)  # Only first three indices
        >>> tc.is_containing_only([0,1,2])
        True
        >>> tc.is_containing_only([0,1])  # Missing index 2
        False

        """
        return sum(self._counts[index] for index in indices) == sum(self._counts)

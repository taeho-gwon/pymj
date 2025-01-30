from __future__ import annotations

from typing import Iterable, Iterator, Sequence, SupportsIndex, overload

from pymj.tiles.tile import Tile
from pymj.tiles.tile_mapping import TileMapping


class TileCount:
    """A class for counting mahjong tiles using a fixed-length array representation.

    This class tracks the count of each tile type using a 34-length array. Each index
    in the array corresponds to a specific tile type, and the value at that index
    represents the count of that tile type.

    The array indices are organized into the following tile categories:
        Man (Characters)   : 0-8    (1-9 man)
        Pin (Circles)      : 9-17   (1-9 pin)
        Sou (Bamboo)      : 18-26  (1-9 sou)
        Wind              : 27-30  (East, South, West, North)
        Dragon            : 31-33  (White, Green, Red)

    This array-based representation enables efficient operations for hand analysis,
    such as checking completeness or calculating possible tile combinations.

    Attributes:
        _counts (list[int]): A 34-element integer list where each element represents
            the count of a specific tile type (0-4 tiles possible per type).

    Examples:
        A typical hand string "1112345678999m" would be represented as follows:
            The first few elements would be [3,1,1,1,1,1,1,1,3,0,0,...] where:
                - Index 0 has value 3 (three 1-man tiles)
                - Indices 1-7 have value 1 (one each of 2-8 man)
                - Index 8 has value 3 (three 9-man tiles)
                - Remaining indices are 0 (no other tiles present)

    """

    def __init__(self, counts: list[int] | None = None) -> None:
        """Initialize a new TileCount instance with optional initial counts.

        Creates a new TileCount object with either provided tile counts or empty counts.
        When initial counts are provided, they are copied to prevent data modification.

        Args:
            counts (list[int] | None, optional): List of 34 integers representing tile
                counts. If None, initializes all counts to 0. Defaults to None.

        Raises:
            ValueError: If the provided counts list does not have exactly 34 elements,
                which is required for representing all mahjong tile types.

        """
        if counts is None:
            self._counts = [0] * 34
        else:
            if len(counts) != 34:
                raise ValueError
            self._counts = counts[:]

    @property
    def num_tiles(self) -> int:
        """Create a new TileCount instance from a sequence of tile indices.

        A factory method that counts occurrences of tile indices and creates a
        corresponding TileCount object. Designed for working with numeric tile
        representations.

        Args:
            tiles (Iterable[int]): Sequence of tile indices (0-33) where:
                0-8: Man tiles
                9-17: Pin tiles
                18-26: Sou tiles
                27-30: Wind tiles
                31-33: Dragon tiles

        Returns:
            TileCount: A new instance with counts of provided tile indices.

        Example:
            >>> tc = TileCount.create_from_indices([0, 0, 1])  # Two 1-man, one 2-man
            >>> tc[0]  # Count of 1-man tiles
            2

        """
        return sum(self._counts)

    @staticmethod
    def create_from_indices(tiles: Iterable[int]) -> TileCount:
        """Create a new TileCount instance from a sequence of tile indices.

        A factory method that creates a TileCount by counting occurrences of numerical
        tile indices, useful for working with index-based tile representations.

        Args:
            tiles (Iterable[int]): Sequence of tile indices (0-33) where:
                0-8: Man tiles
                9-17: Pin tiles
                18-26: Sou tiles
                27-30: Wind tiles
                31-33: Dragon tiles

        Returns:
            TileCount: A new instance with counts of provided tile indices.

        Example:
            >>> tc = TileCount.create_from_indices([0, 0, 1])  # Two 1-man, one 2-man
            >>> tc[0]  # Count of 1-man tiles
            2

        """
        tile_count = TileCount()
        for tile in tiles:
            tile_count[tile] += 1
        return tile_count

    @staticmethod
    def create_from_tiles(tiles: Iterable[Tile]) -> TileCount:
        """Create a new TileCount instance from a sequence of Tile objects.

        A factory method similar to create_from_indices but works with Tile objects.
        The method first converts each Tile object into its corresponding index
        using TileMapping, then creates a count of these indices.

        Args:
            tiles (Iterable[Tile]): A sequence of Tile objects to be counted.

        Returns:
            TileCount: A new instance containing the counts of the provided tiles.

        Example:
            >>> tiles = [Tile(TileType.MAN, 1)] * 2 + [Tile(TileType.MAN, 2)]
            >>> tc = TileCount.create_from_tiles(tiles)  # Two 1-man, one 2-man
            >>> tc[0]  # Count of 1-man tiles
            2

        """
        return TileCount.create_from_indices(
            TileMapping.tile_to_index(tile) for tile in tiles
        )

    def __eq__(self, other: object) -> bool:
        """Compare this TileCount instance with another for equality.

        Checks if two TileCount instances represent the same tile distribution by
        comparing their internal count arrays. Equality means that both instances have
        exactly the same number of each tile type.

        Args:
            other (object): The object to compare against this TileCount instance. Can
                be any type, but only returns True if it's another TileCount with
                identical counts.

        Returns:
            bool: True if 'other' is a TileCount instance with identical tile counts,
                False in all other cases (including comparison with non-TileCount
                objects).

        Example:
            >>> tc1 = TileCount([1,1,1] + [0]*31)  # Three tiles: one each of first
                                                   # three types
            >>> tc2 = TileCount([1,1,1] + [0]*31)  # Same distribution
            >>> tc1 == tc2
            True

        """
        if not isinstance(other, TileCount):
            return False
        return self._counts == other._counts

    def __add__(self, other: TileCount) -> TileCount:
        """Add two TileCount instances element-wise.

        Creates a new TileCount instance by summing the corresponding tile counts from
        both operands. This is used when combining tile counts from different hands or
        sets.

        Args:
           other (TileCount): Another TileCount instance whose counts will be added to
               this instance's counts.

        Returns:
           TileCount: A new instance where each position contains the sum of tile
               counts from both operands at that position.

        Example:
           >>> tc1 = TileCount([1,0,0] + [0]*31)  # One 1-man tile
           >>> tc2 = TileCount([1,1,0] + [0]*31)  # One 1-man and one 2-man tile
           >>> tc3 = tc1 + tc2
           >>> tc3[0]  # Count of 1-man tiles: 1 + 1 = 2
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

        Implements Python's standard indexing interface to provide convenient access to
        tile counts. Supports both single-index lookups and slice operations for
        accessing multiple counts at once.

        Args:
           key (SupportsIndex | slice): The index or slice to access the counts:
               - For single index (0-33): Returns count of specific tile type
               - For slice: Returns list of counts within specified range

        Returns:
           int | list[int]: Either a single tile count (when using index) or a list of
               counts (when using slice).

        Example:
           >>> tc = TileCount([1,2,3] + [0]*31)  # First three tiles have counts 1,2,3
           >>> tc[0]  # Get count of first tile type (1-man)
           1
           >>> tc[0:3]  # Get counts of first three tile types
           [1, 2, 3]

        """
        return self._counts[key]

    def __setitem__(self, key: SupportsIndex, value: int) -> None:
        """Set the count value for a specified mahjong tile type.

        Args:
            key (SupportsIndex): Index of the tile type (0-33) to modify.
            value (int): New count value to set for the specified tile.

        Raises:
            IndexError: If key is outside the valid range of 0-33.
            ValueError: If value is negative.

        Examples:
            >>> tc = TileCount()
            >>> tc[0] = 2  # Sets the count of 1-man tile to 2

        """
        self._counts[key] = value

    def __iter__(self) -> Iterator[int]:
        """Create an iterator for sequentially accessing all tile counts.

        This method implements the iterator protocol,
        allowing iteration over all tile counts in their natural order (0 to 33).

        Args:
            None

        Returns:
            Iterator[int]: An iterator that yields the count value for each tile type.
                The counts are yielded in ascending order of tile indices.

        Examples:
            >>> tc = TileCount([1,1,1] + [0]*31) # First three tiles have count 1
            >>> list(tc)  # Converting iterator to list shows all counts
            [1, 1, 1, 0, 0, ...]
            >>> for count in tc:  # Iterate through counts directly
            ...     # Process each tile count

        """
        return iter(self._counts)

    def find_earliest_nonzero_index(self, index: int = 0) -> int:
        """Find the first index with a positive count.

        This method performs a linear search through the tile counts,
        starting from a given index,
        to find the first tile that has a count greater than zero.
        This functionality is essential for efficient sequential processing of tiles,
        as it allows skipping over empty positions.

        Args:
            index (int, optional): The starting position from which to begin the search.
                Must be between 0 and 33 inclusive. Defaults to 0.

        Returns:
            int: The index of the first non-zero count encountered during the search.
                - If a non-zero count is found, returns its index (between index and 33)
                - If no non-zero counts are found, returns 34
                - Always returns a value >= the input index

        Raises:
            ValueError: If the starting index is negative or greater than 34.

        Examples:
            >>> # Initialize with counts of 1 at index 2 and 2 at index 4
            >>> tc = TileCount([0,0,1,0,2,0] + [0]*28)
            >>> tc.find_earliest_nonzero_index()  # Search from beginning
            2
            >>> tc.find_earliest_nonzero_index(3)  # Search starting from index 3
            4

        """
        while index < len(self._counts) and self._counts[index] == 0:
            index += 1
        return index

    def is_containing_only(self, indices: Sequence[int]) -> bool:
        """Verify that non-zero tile counts exist only at the specified indices.

        This method performs a validation check to ensure that tiles are present
        (have non-zero counts) only at the provided index positions.
        All other positions must have zero count for the validation to pass.

        Args:
            indices (Sequence[int]): A sequence of valid tile indices
                where non-zero counts are allowed.
                Each index in the sequence must be between 0 and 33 inclusive.
                The sequence can be any iterable type (list, tuple, set, etc.).

        Returns:
            bool: The validation result:
                - True if all non-zero counts appear exclusively at the given indices
                - False if any non-zero count is found at an unspecified index

        Raises:
            ValueError: If any of the provided indices are outside the range [0, 33].
            TypeError: If indices argument is not a sequence type.

        Examples:
            >>> # Initialize with counts of 1 at indices 0, 1, and 2
            >>> tc = TileCount([1,1,1,0,0,0,0,0,0] + [0]*25)
            >>> tc.is_containing_only([0,1,2])  # Check exact match
            True
            >>> tc.is_containing_only([0,1])  # Fails: index 2 has count
            False
            >>> tc.is_containing_only([0,1,2,3])  # Passes: extra index is allowed
            True

        """
        return sum(self._counts[index] for index in indices) == sum(self._counts)

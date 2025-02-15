from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TileIndex:
    """Represents a valid mahjong tile index.

    This class ensures that tile indices are always valid (0-33) and provides
    helpful methods for working with tile indices in a type-safe manner.

    Attributes:
        value (int): The underlying tile index value (0-33)
            - 0-8   : Man
            - 9-17  : Pin
            - 18-26 : Sou
            - 27-30 : Wind tiles
            - 31-33 : Dragon tiles

    """

    value: int
    MAX_INDEX = 33
    SIZE = 34

    def __post_init__(self) -> None:
        """Validate the tile index after initialization.

        Raises:
            ValueError: If value is not between 0 and 33

        """
        if not 0 <= self.value <= 33:
            raise ValueError

    def __str__(self) -> str:
        return str(self.value)

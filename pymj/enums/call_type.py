from enum import Enum, auto


class CallType(Enum):
    """Types of tile combinations that can be declared during gameplay.

    Attributes:
        CHII: Sequence of three consecutive numbered tiles of the same suit,
            formed by claiming another player's discard tile.
        PON: Three identical tiles, formed by claiming another player's discard
            and revealing two matching tiles from hand.
        CONCEALED_KAN: Four identical tiles, all from player's own hand
            without any claims.
        BIG_MELDED_KAN: Four identical tiles, formed by claiming a discard
            and revealing three matching tiles from hand.
        SMALL_MELDED_KAN: Four identical tiles, formed by adding a fourth
            matching tile to an existing PON.

    """

    CHII = auto()
    PON = auto()
    CONCEALED_KAN = auto()
    BIG_MELDED_KAN = auto()
    SMALL_MELDED_KAN = auto()

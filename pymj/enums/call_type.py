from enum import Enum, auto


class CallType(Enum):
    """Represents different types of calls that can be declared.

    It can be formed by calling another player's discard or using tiles from hand.

    Attributes
    ----------
    CHII
        A sequence of three consecutive numbered tiles of the same suit.

    PON
        A triplet of three identical tiles.

    CONCEALED_KAN
        A quad made with four identical tiles from one's own hand.

    BIG_MELDED_KAN
        A quad formed by calling a discard and revealing three identical tiles.

    SMALL_MELDED_KAN
        A quad created by adding a fourth tile to an existing pon.

    """

    CHII = auto()
    PON = auto()
    CONCEALED_KAN = auto()
    BIG_MELDED_KAN = auto()
    SMALL_MELDED_KAN = auto()

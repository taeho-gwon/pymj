from dataclasses import dataclass

_MANS = tuple(range(9))
_PINS = tuple(range(9, 18))
_SOUS = tuple(range(18, 27))
_WINDS = (27, 28, 29, 30)
_DRAGONS = (31, 32, 33)

_NUMBERS = _MANS + _PINS + _SOUS
_HONORS = _WINDS + _DRAGONS
_ALL = _NUMBERS + _HONORS

_TERMINALS = (_MANS[0], _MANS[8], _PINS[0], _PINS[8], _SOUS[0], _SOUS[8])
_TERMINALS_AND_HONORS = _TERMINALS + _HONORS

_SEQUENCE_STARTS = _MANS[0:7] + _PINS[0:7] + _SOUS[0:7]
_SIDE_WAIT_STARTS = _MANS[1:7] + _PINS[1:7] + _SOUS[1:7]
_LEFT_EDGE_WAIT_STARTS = (_MANS[0], _PINS[0], _SOUS[0])
_RIGHT_EDGE_WAIT_STARTS = (_MANS[7], _PINS[7], _SOUS[7])

_SIMPLES = _MANS[1:8] + _PINS[1:8] + _SOUS[1:8]
_GREENS = (_SOUS[1], _SOUS[2], _SOUS[3], _SOUS[5], _SOUS[7], _DRAGONS[1])

_IS_SEQUENCE_STARTS = [tile in _SEQUENCE_STARTS for tile in _ALL]
_IS_SIDE_WAIT_STARTS = [tile in _SIDE_WAIT_STARTS for tile in _ALL]
_IS_LEFT_EDGE_WAIT_STARTS = [tile in _LEFT_EDGE_WAIT_STARTS for tile in _ALL]
_IS_RIGHT_EDGE_WAIT_STARTS = [tile in _RIGHT_EDGE_WAIT_STARTS for tile in _ALL]


@dataclass(frozen=True)
class Tiles:
    """Define core tile categories and special combinations for gameplay mechanics.

    Attributes:
        MANS: Character tile indices ranging from 0 to 8
        PINS: Circle tile indices ranging from 9 to 17
        SOUS: Bamboo tile indices ranging from 18 to 26
        WINDS: Wind tile indices ranging from 27 to 30
        DRAGONS: Dragon tile indices ranging from 31 to 33
        NUMBERS: Combined number tiles (MANS + PINS + SOUS)
        HONORS: Combined honor tiles (WINDS + DRAGONS)
        ALL: Complete set of all standard tiles
        TERMINALS: Terminal number tiles (1 and 9)
        TERMINALS_AND_HONORS: Combined terminal and honor tiles
        SEQUENCE_STARTS: Valid starting indices for sequences (1-7)
        SIDE_WAIT_STARTS: Valid starting indices for side waits
        LEFT_EDGE_WAIT_STARTS: Valid starting indices for left edge waits
        RIGHT_EDGE_WAIT_STARTS: Valid starting indices for right edge waits
        SIMPLES: Simple number tiles ranging from 2 to 8
        GREENS: Tiles used in all-green combinations
        IS_SEQUENCE_STARTS: Boolean flags for valid sequence starts
        IS_SIDE_WAIT_STARTS: Boolean flags for valid side waits
        IS_LEFT_EDGE_WAIT_STARTS: Boolean flags for left edge waits
        IS_RIGHT_EDGE_WAIT_STARTS: Boolean flags for right edge waits

    """

    MANS = _MANS
    PINS = _PINS
    SOUS = _SOUS
    WINDS = _WINDS
    DRAGONS = _DRAGONS

    NUMBERS = _NUMBERS
    HONORS = _HONORS
    ALL = _ALL

    TERMINALS = _TERMINALS
    TERMINALS_AND_HONORS = _TERMINALS_AND_HONORS

    SEQUENCE_STARTS = _SEQUENCE_STARTS
    SIDE_WAIT_STARTS = _SIDE_WAIT_STARTS
    LEFT_EDGE_WAIT_STARTS = _LEFT_EDGE_WAIT_STARTS
    RIGHT_EDGE_WAIT_STARTS = _RIGHT_EDGE_WAIT_STARTS

    SIMPLES = _SIMPLES
    GREENS = _GREENS

    IS_SEQUENCE_STARTS = _IS_SEQUENCE_STARTS
    IS_SIDE_WAIT_STARTS = _IS_SIDE_WAIT_STARTS
    IS_LEFT_EDGE_WAIT_STARTS = _IS_LEFT_EDGE_WAIT_STARTS
    IS_RIGHT_EDGE_WAIT_STARTS = _IS_RIGHT_EDGE_WAIT_STARTS

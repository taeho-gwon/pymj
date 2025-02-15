import re
from itertools import chain
from typing import ClassVar

from pymj.enums.call_type import CallType
from pymj.enums.player_relation import PlayerRelation
from pymj.enums.tile_type import TileType
from pymj.tiles.call import Call
from pymj.tiles.hand import Hand
from pymj.tiles.tile import Tile


class HandParser:
    """Parser for converting between Hand instances and string representations."""

    TILE_TYPE_MAP: ClassVar[dict[str, TileType]] = {
        "m": TileType.MAN,
        "p": TileType.PIN,
        "s": TileType.SOU,
    }
    CALL_TYPE_MAP: ClassVar[dict[str, CallType]] = {
        "c": CallType.CHII,
        "p": CallType.PON,
        "k": CallType.CONCEALED_KAN,
        "b": CallType.BIG_MELDED_KAN,
        "s": CallType.SMALL_MELDED_KAN,
    }
    PLAYER_RELATION_MAP: ClassVar[dict[str, PlayerRelation]] = {
        "<": PlayerRelation.PREV,
        "^": PlayerRelation.ACROSS,
        ">": PlayerRelation.NEXT,
        "_": PlayerRelation.SELF,
    }

    @staticmethod
    def parse_tile(tile_str: str) -> Tile:
        """Parse a single tile string into a Tile object.

        Args:
        ----
            tile_str (str): Tile string (e.g., '1m', '5p', '6z')

        Returns:
        -------
            Tile: Parsed Tile object

        Raises:
        ------
            ValueError: If the tile string format is invalid

        """
        # Extract the number and type characters
        match = re.fullmatch(r"(\d)([mpsz])", tile_str)
        if not match:
            raise ValueError

        number = int(match.group(1))
        tile_type_char = match.group(2)

        # Determine tile type based on the type character
        if tile_type_char == "z":
            if 1 <= number <= 4:
                tile_type = TileType.WIND
            elif 5 <= number <= 7:
                tile_type = TileType.DRAGON
                number -= 4
            else:
                raise ValueError
        else:
            tile_type = HandParser.TILE_TYPE_MAP[tile_type_char]

        return Tile(tile_type=tile_type, value=number)

    @staticmethod
    def parse_tile_group(group: str) -> list[Tile]:
        """Parse a tile group like '123m' or '456p' into a list of Tile objects.

        Args:
        ----
            group (str): Tile group string (e.g., '123m', '456p', '567z')

        Returns:
        -------
            list[Tile]: List of parsed Tile objects

        """
        match = re.fullmatch(r"(\d+)([mpsz])", group)
        if not match:
            raise ValueError

        numbers = match.group(1)
        tile_type_char = match.group(2)

        return [HandParser.parse_tile(num + tile_type_char) for num in numbers]

    @staticmethod
    def parse_call(call_str: str) -> Call:
        """Parse a call string into a Call object.

        Args:
        ----
            call_str (str): Call string (e.g., 'c<789p', 'p^111s', 'b_1111m')

        Returns:
        -------
            Call: Parsed Call object

        Raises:
        ------
            ValueError: If the call string format is invalid

        """
        # Parse call string
        match = re.match(r"([cpbks])([<^>_])(\d+[mpsz])", call_str)
        if not match:
            raise ValueError

        call_type_char = match.group(1)
        player_relation_char = match.group(2)
        tiles_str = match.group(3)

        return Call(
            tiles=HandParser.parse_tile_group(tiles_str),
            call_type=HandParser.CALL_TYPE_MAP[call_type_char],
            player_relation=HandParser.PLAYER_RELATION_MAP[player_relation_char],
        )

    @staticmethod
    def parse_hand(hand_str: str) -> Hand:
        """Parse a string representation into a Hand object.

        Format: "123m456p,c<789p,p^111s,k_2222m"
        - Basic tiles: 123m (man), 456p (pin), 789s (sou), 1234z (wind), 567z (dragon)
        - Call format: [type][player_relation][tiles]
            * Call types:
                - c (chii)
                - p (pon)
                - k (concealed kan)
                - b (big melded kan)
                - s (small melded kan)
            * Player relations:
                - < (prev)
                - ^ (across)
                - > (next)
                - _ (self)
            Example: c<789p (chii from previous player)

        Args:
        ----
            hand_str (str): String representation of hand (e.g., "123m456p,c<789p")

        Returns:
        -------
            Hand: Hand object containing the parsed tiles and calls

        Raises:
        ------
            ValueError: If the string format is invalid

        """
        # Split the hand string into base tiles and calls
        parts = hand_str.split(",")

        # Create a new Hand object
        hand = Hand()

        # Parse base tiles (first part)
        hand.tiles = list(
            chain.from_iterable(
                HandParser.parse_tile_group(group)
                for group in re.findall(r"\d+[mpsz]", parts[0])
            ),
        )
        hand.calls = [HandParser.parse_call(call_str) for call_str in parts[1:]]
        return hand

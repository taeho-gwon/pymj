from pymj.enums.call_type import CallType
from pymj.enums.player_relation import PlayerRelation
from pymj.enums.tile_type import TileType
from pymj.tiles.tile import Tile


class Call:
    """A class representing a melded combination of tiles.

    This class manages the validation and storage of tile combinations formed through
    calls (melds) during gameplay. It ensures that all game rules regarding tile
    combinations and player relations are properly enforced.

    Attributes:
        tiles (list[Tile]): List of tiles forming the meld. The first tile must be
            the called tile from another player.
        call_type (CallType): Type of the call. See CallType enum for detailed
            descriptions.
        player_relation (PlayerRelation): Relationship to the player whose tile was
            called. SELF for concealed kan, PREV for chii, can vary for other calls.

    Raises:
        ValueError: If the tiles don't match the requirements for the specified call
            type, or if the player relation is invalid for the call type.

    """

    def __init__(
        self,
        tiles: list[Tile],
        call_type: CallType,
        player_relation: PlayerRelation | None = None,
    ) -> None:
        """Initialize a new Call instance representing a tile combination.

        Creates a new Call object that manages a valid combination of tiles formed
        through calls or melds.

        Args:
            tiles (list[Tile]): The tiles forming the combination. First tile must be
                the called tile.
            call_type (CallType): The type of combination being formed.
            player_relation (PlayerRelation | None, optional):
                Relation to the player who discarded the called tile.
                Defaults to SELF for concealed kan and PREV for others.

        Raises:
            ValueError: If tiles don't form a valid combination or player relation is
                invalid.

        """
        self.tiles = tiles
        self.call_type = call_type

        if player_relation is None:
            self.player_relation = (
                PlayerRelation.SELF
                if call_type is CallType.CONCEALED_KAN
                else PlayerRelation.PREV
            )

        else:
            self.player_relation = player_relation

        self._validate_init()

    def _validate_init(self) -> None:
        tile_count_dict: dict[CallType, int] = {
            CallType.CHII: 3,
            CallType.PON: 3,
            CallType.CONCEALED_KAN: 4,
            CallType.BIG_MELDED_KAN: 4,
            CallType.SMALL_MELDED_KAN: 4,
        }

        if len(self.tiles) != tile_count_dict[self.call_type]:
            raise ValueError(
                f"{self.call_type.name} need exactly"
                f"{tile_count_dict[self.call_type]} tiles, not {len(self.tiles)}."
            )

        if self.call_type is CallType.CHII:
            self._validate_chii()

        else:
            if not all(tile == self.tiles[0] for tile in self.tiles):
                raise ValueError("Pon and Kan tiles must be the same tiles.")

            if (
                self.call_type is CallType.CONCEALED_KAN
                and self.player_relation is not PlayerRelation.SELF
            ):
                raise ValueError

            if (
                self.call_type is not CallType.CONCEALED_KAN
                and self.player_relation is PlayerRelation.SELF
            ):
                raise ValueError

    def _validate_chii(self) -> None:
        assert len(self.tiles) == 3

        if self.player_relation is not PlayerRelation.PREV:
            raise ValueError

        tile_type = self.tiles[0].tile_type
        if (
            self.tiles[1].tile_type is not tile_type
            or self.tiles[2].tile_type is not tile_type
        ):
            raise ValueError("Chi tiles must be the same type.")

        if tile_type not in {TileType.MAN, TileType.PIN, TileType.SOU}:
            raise ValueError(f"{tile_type.name} cannot be chii tiles.")

        numbers = sorted(tile.value for tile in self.tiles)

        if numbers[1] != numbers[0] + 1 or numbers[2] != numbers[1] + 1:
            raise ValueError(f"chi tiles numbers {numbers} must be consecutive.")

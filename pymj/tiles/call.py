from pymj.enums.call_type import CallType
from pymj.enums.player_relation import PlayerRelation
from pymj.enums.tile_type import TileType
from pymj.tiles.tile import Tile


class Call:
    """Represents a call object for mahjong hand."""

    def __init__(
        self,
        tiles: list[Tile],
        call_type: CallType,
        player_relation: PlayerRelation | None = None,
    ) -> None:
        """Initialize for call class.

        Args:
        ----
            tiles (list[Tile]): tile list for calls.
                If Chii type, first tile must be other's tile.
            call_type (CallType): type of call (chii, pon, kan...)
            player_relation (PlayerRelation | None):
                relation of player who discard called tile.
                If None, SELF for concealed kan, else PREV

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Call):
            return False
        return (
            self.tiles == other.tiles
            and self.call_type == other.call_type
            and self.player_relation == other.player_relation
        )

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

        if tile_type is TileType.WIND or tile_type is TileType.DRAGON:
            raise ValueError(f"{tile_type.name} cannot be chii tiles.")

        numbers = sorted(tile.value for tile in self.tiles)

        if numbers[1] != numbers[0] + 1 or numbers[2] != numbers[1] + 1:
            raise ValueError(f"chi tiles numbers {numbers} must be consecutive.")

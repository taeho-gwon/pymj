from pymj.hand_checker.base_hand_checker import BaseHandChecker
from pymj.tiles.division import Division
from pymj.tiles.hand_info import HandInfo


def test_check_agari(mocker):
    # Given: mock hand checker and hand info
    class MockBaseHandChecker(BaseHandChecker):
        def calculate_divisions(self, hand_info: HandInfo) -> list[Division]:
            return []

        def calculate_shanten(self, hand_info: HandInfo) -> int:
            return 0

    mock_hand_checker = MockBaseHandChecker()
    mock_calculate_shanten = mocker.patch.object(
        mock_hand_checker, "calculate_shanten", autospec=True
    )
    hand_info = HandInfo()

    # When: shanten is -1
    mock_calculate_shanten.return_value = -1

    # Then: check agari is True
    assert mock_hand_checker.check_agari(hand_info)

    # When: shanten is not -1
    mock_calculate_shanten.return_value = 1

    # Then: check agari is False
    assert not mock_hand_checker.check_agari(hand_info)

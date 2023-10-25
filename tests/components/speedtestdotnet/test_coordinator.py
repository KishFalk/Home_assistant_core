"""Tests for SpeedTest coordinator."""
from unittest.mock import Mock
import pytest
from homeassistant.components.speedtestdotnet import SpeedTestDataCoordinator
from homeassistant.core import HomeAssistant


async def test_calc_download_percentage() -> None:
    """Test the calculation of the upload percentage function."""
    hass = Mock(spec=HomeAssistant)
    coordinator = SpeedTestDataCoordinator(hass, None, None)

    paid_download_speed = 50.0
    actual_download_speed = 40.0

    expected_percentage = (actual_download_speed / paid_download_speed) * 100

    result = coordinator.calc_download_percentage_test(
        actual_download_speed, paid_download_speed
    )
    assert result == expected_percentage


async def test_calc_upload_percentage() -> None:
    """Test the calculation of the upload percentage function."""
    hass = Mock(spec=HomeAssistant)
    coordinator = SpeedTestDataCoordinator(hass, None, None)

    paid_download_speed = 50.0
    actual_download_speed = 40.0

    expected_percentage = (actual_download_speed / paid_download_speed) * 100

    result = coordinator.calc_upload_percentage_test(
        actual_download_speed, paid_download_speed
    )
    assert result == expected_percentage

@pytest.mark.parametrize(
    ("download", "ping", "expected_result"),
    [
        (0.5, 10, "Literal potato speeds."),
        (5, 10, "Kinda trashy."),
        (25, 10, "Granny dial-up internet."),
        (75, 10, "Nothing special, really"),
        (150, 10, "Just above average. Bet you feel special."),
        (100, 250, "Every online shooter's worst nightmare."),
    ],
)
def test_generate_funny_rating(download, ping, expected_result) -> None:
    """Test the generate_funny_rating function."""
    assert (
        SpeedTestDataCoordinator.generate_funny_rating(None, download, ping)
        == expected_result
    )

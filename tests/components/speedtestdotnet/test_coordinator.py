"""Tests for SpeedTest coordinator."""
from unittest.mock import Mock

from homeassistant.components.speedtestdotnet.coordinator import (
    SpeedTestDataCoordinator,
)
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

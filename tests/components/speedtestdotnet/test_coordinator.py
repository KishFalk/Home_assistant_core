"""Tests for SpeedTest coordinator."""

import pytest

from homeassistant.components.speedtestdotnet import SpeedTestDataCoordinator


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

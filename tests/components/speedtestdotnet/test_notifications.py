"""Tests for SpeedTest notification."""

MAX_STATES = {"download": 100, "upload": 100}

MOCK_STATES = [
    {"ping": 18, "download": 45.68, "upload": 83.79},
    {"ping": 18, "download": 98.43, "upload": 76.16},
    {"ping": 53, "download": 98.43, "upload": 83.79},
    {"ping": 53, "download": 45.68, "upload": 83.79},
    {"ping": 18, "download": 45.68, "upload": 76.16},
    {"ping": 53, "download": 98.43, "upload": 76.16},
]


async def test_history_average() -> None:
    """Test averaging history states."""
    return


async def test_validate() -> None:
    """Test validating averages."""
    return

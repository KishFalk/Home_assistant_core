"""Tests for SpeedTest notification."""
from homeassistant.components.speedtestdotnet.notifications import (
    SpeedtestdotnetNotifications,
)
from homeassistant.core import HomeAssistant

MAX_STATES = {"download": 100, "upload": 100}
sensor_names = ["download", "ping", "upload"]


class MockNotificationsState:
    """Mock class for state attribute."""

    def __init__(self, state: str) -> None:
        """Initialise class."""
        self.state = state


MOCK_STATES = [
    {
        "download": [
            MockNotificationsState("45"),  # 50
            MockNotificationsState("55"),
        ],
        "ping": [
            MockNotificationsState("55"),  # 60
            MockNotificationsState("65"),
        ],
        "upload": [
            MockNotificationsState("70.0"),  # 65
            MockNotificationsState("60.0"),
        ],
    },
    {
        "download": [
            MockNotificationsState("98.56"),  # 99.28
            MockNotificationsState("100.00"),
        ],
        "ping": [
            MockNotificationsState("20"),
            MockNotificationsState("14"),
        ],
        "upload": [
            MockNotificationsState("90.0"),  # 85
            MockNotificationsState("80.0"),
        ],
    },
]

MOCK_AVG_RESULTS = [
    {"download": {"value": 50.0}, "ping": {"value": 60.0}, "upload": {"value": 65.0}},
    {"download": {"value": 99.28}, "ping": {"value": 17.0}, "upload": {"value": 85.0}},
]

MOCK_VALIDATE_RESULTS = [
    {"download": False, "ping": False, "upload": False},
    {"download": True, "ping": True, "upload": True},
]


async def test_history_average(hass: HomeAssistant) -> None:
    """Test averaging history states."""
    notif = SpeedtestdotnetNotifications()
    await notif.create(hass, 100, 100)
    for i, val in enumerate(MOCK_STATES):
        for sensor_name in sensor_names:
            result = notif.average(val[sensor_name])
            assert result["value"] == MOCK_AVG_RESULTS[i][sensor_name]["value"]


async def test_validate(hass: HomeAssistant) -> None:
    """Test validating averages."""
    notif = SpeedtestdotnetNotifications()
    await notif.create(hass, 100, 100)
    for i, val in enumerate(MOCK_AVG_RESULTS):
        result = notif.validate(val)
        assert result == MOCK_VALIDATE_RESULTS[i]

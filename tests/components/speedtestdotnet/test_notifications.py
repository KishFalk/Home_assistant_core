"""Tests for SpeedTest notification."""
from unittest.mock import patch

from homeassistant.components.speedtestdotnet import notifications as n
from homeassistant.core import HomeAssistant

MAX_STATES = {"download": 100, "ping": 50, "upload": 100}
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
    {
        "download": [MockNotificationsState("98,56")],
        "ping": [MockNotificationsState("2-0")],
        "upload": [MockNotificationsState("90Ä0")],
    },
]

MOCK_AVG_RESULTS = [
    {
        "download": {"value": 50.0, "count": 2},
        "ping": {"value": 60.0, "count": 2},
        "upload": {"value": 65.0, "count": 2},
    },
    {
        "download": {"value": 99.28, "count": 2},
        "ping": {"value": 17.0, "count": 2},
        "upload": {"value": 85.0, "count": 2},
    },
    {
        "download": {"value": 0.0, "count": 0},
        "ping": {"value": 0.0, "count": 0},
        "upload": {"value": 0.0, "count": 0},
    },
]

MOCK_VALIDATE_RESULTS = [
    {"download": False, "ping": False, "upload": False},
    {"download": True, "ping": True, "upload": True},
    {"download": False, "ping": False, "upload": False},
]

MOCK_COMPARE = [
    {"value": 80, "threshold": 0.9, "less_than": False, "max_value": 100},
    {"value": 95, "threshold": 0.9, "less_than": False, "max_value": 100},
    {"value": 80, "threshold": 1.0, "less_than": True, "max_value": 50},
    {"value": 30, "threshold": 1.0, "less_than": True, "max_value": 50},
]

MOCK_COMPARE_RESULTS = [False, True, False, True]


async def test_history_average(hass: HomeAssistant) -> None:
    """Test averaging history states."""
    notif = n.SpeedtestdotnetNotifications()
    await notif.create(hass, MAX_STATES["download"], MAX_STATES["upload"])
    for i, val in enumerate(MOCK_STATES):
        for sensor_name in sensor_names:
            result = notif.average(val[sensor_name])
            assert result["value"] == MOCK_AVG_RESULTS[i][sensor_name]["value"]


async def test_validate(hass: HomeAssistant) -> None:
    """Test validating averages."""
    notif = n.SpeedtestdotnetNotifications()
    await notif.create(hass, MAX_STATES["download"], MAX_STATES["upload"])
    for i, val in enumerate(MOCK_AVG_RESULTS):
        result = notif.validate(val)
        assert result == MOCK_VALIDATE_RESULTS[i]


async def test_compare(hass: HomeAssistant) -> None:
    """Test the compare function for state thresholds."""
    notif = n.SpeedtestdotnetNotifications()
    await notif.create(hass, MAX_STATES["download"], MAX_STATES["upload"])

    for i, val in enumerate(MOCK_COMPARE):
        result = notif.compare(val["value"], val)
        assert result == MOCK_COMPARE_RESULTS[i]


@patch.object(n.SpeedtestdotnetNotifications, "get_sensor_history")
@patch.object(n.SpeedtestdotnetNotifications, "send_notification")
async def test_update(
    mock_history, mock_send_notification, hass: HomeAssistant
) -> None:
    """Test the update method."""
    mock_history.get_sensor_history.side_effect = MOCK_STATES
    mock_history.mock_send_notification.return_value = None
    notif = n.SpeedtestdotnetNotifications()
    await notif.create(hass, MAX_STATES["upload"], MAX_STATES["upload"])

    assert await notif.update() is True

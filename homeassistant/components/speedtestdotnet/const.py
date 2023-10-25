"""Constants used by Speedtest.net."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "speedtestdotnet"

CONF_SERVER_NAME: Final = "server_name"
CONF_SERVER_ID: Final = "server_id"
CONF_PAID_DOWNLOAD_SPEED: Final = "paid_download_speed"
CONF_PAID_UPLOAD_SPEED: Final = "paid_upload_speed"


ATTR_BYTES_RECEIVED: Final = "bytes_received"
ATTR_BYTES_SENT: Final = "bytes_sent"
ATTR_SERVER_COUNTRY: Final = "server_country"
ATTR_SERVER_ID: Final = "server_id"
ATTR_SERVER_NAME: Final = "server_name"


DEFAULT_NAME: Final = "SpeedTest"
DEFAULT_SCAN_INTERVAL: Final = 60
DEFAULT_SERVER: Final = "*Auto Detect"

ATTRIBUTION: Final = "Data retrieved from Speedtest.net by Ookla"

ICON: Final = "mdi:speedometer"

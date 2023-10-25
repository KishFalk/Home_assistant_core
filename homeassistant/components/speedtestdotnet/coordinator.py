"""Coordinator for speedtestdotnet."""

from datetime import timedelta
import logging
from typing import Any, cast

import speedtest

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_PAID_DOWNLOAD_SPEED,
    CONF_PAID_UPLOAD_SPEED,
    CONF_SERVER_ID,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SERVER,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class SpeedTestDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Get the latest data from speedtest.net."""

    config_entry: ConfigEntry

    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, api: speedtest.Speedtest
    ) -> None:
        """Initialize the data object."""
        self.hass = hass
        self.config_entry = config_entry
        self.api = api
        self.servers: dict[str, dict] = {DEFAULT_SERVER: {}}
        super().__init__(
            self.hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=DEFAULT_SCAN_INTERVAL),
        )

    def update_servers(self) -> None:
        """Update list of test servers."""
        test_servers = self.api.get_servers()
        test_servers_list = []
        for servers in test_servers.values():
            for server in servers:
                test_servers_list.append(server)
        for server in sorted(
            test_servers_list,
            key=lambda server: (
                server["country"],
                server["name"],
                server["sponsor"],
            ),
        ):
            self.servers[
                f"{server['country']} - {server['sponsor']} - {server['name']}"
            ] = server

    def update_data(self) -> dict[str, Any]:
        """Get the latest data from speedtest.net."""
        self.update_servers()
        self.api.closest.clear()
        if self.config_entry.options.get(CONF_SERVER_ID):
            server_id = self.config_entry.options.get(CONF_SERVER_ID)
            self.api.get_servers(servers=[server_id])

        best_server = self.api.get_best_server()
        _LOGGER.debug(
            "Executing speedtest.net speed test with server_id: %s",
            best_server["id"],
        )
        self.api.download()
        self.api.upload()

        result_dict = cast(dict[str, Any], self.api.results.dict())
        result_dict["download_percentage"] = self.calc_download_percentage(
            round(result_dict["download"] / 10**6, 2)
        )
        result_dict["upload_percentage"] = self.calc_upload_percentage(
            round(result_dict["upload"] / 10**6, 2)
        )
        result_dict = cast(dict[str, Any], self.api.results.dict())
        result_dict["funny_rating"] = self.generate_funny_rating(
            float(round(result_dict["download"] / 10**6, 2)),
            float(result_dict["ping"]),
        )
        return result_dict

    def generate_funny_rating(self, download: float, ping: float) -> str:
        """Generate a funny rating based on download speed."""
        funny_rating = ""
        if ping > 200:
            funny_rating = "Every online shooter's worst nightmare."
        elif download < 1:
            funny_rating = "Literal potato speeds."
        elif download < 10:
            funny_rating = "Kinda trashy."
        elif download < 50:
            funny_rating = "Granny dial-up internet."
        elif download < 100:
            funny_rating = "Nothing special, really"
        elif download < 250:
            funny_rating = "Just above average. Bet you feel special."
        elif download < 500:
            funny_rating = "You're probably paying too much."
        elif download < 750:
            funny_rating = "Is it bring your HomeAssistant to work day?"
        elif download <= 1000:
            funny_rating = "Dude. Stop."
        elif download > 1000:
            funny_rating = "Absolutely God-tier."

        return funny_rating

    async def _async_update_data(self) -> dict[str, Any]:
        """Update Speedtest data."""
        try:
            return await self.hass.async_add_executor_job(self.update_data)
        except speedtest.NoMatchedServers as err:
            raise UpdateFailed("Selected server is not found.") from err
        except speedtest.SpeedtestException as err:
            raise UpdateFailed(err) from err

    def calc_download_percentage(self, actual_download_speed: float) -> Any:
        """Calculate the download percentage between the paid and actual download speed."""
        paid_download_speed = self.config_entry.data.get(CONF_PAID_DOWNLOAD_SPEED)
        if paid_download_speed is not None:
            return (actual_download_speed / paid_download_speed) * 100
        return None

    def calc_upload_percentage(self, actual_upload_speed: float) -> Any:
        """Calculate the upload percentage between the paid and actual upload speed."""
        paid_upload_speed = self.config_entry.data.get(CONF_PAID_UPLOAD_SPEED)
        if paid_upload_speed is not None:
            return (actual_upload_speed / paid_upload_speed) * 100
        return None

    def calc_download_percentage_test(
        self, actual_download_speed: float, paid_download_speed: float
    ) -> float:
        """Test the calculation of the download percentage between the paid and actual download speed."""
        return (actual_download_speed / paid_download_speed) * 100

    def calc_upload_percentage_test(
        self, actual_upload_speed: float, paid_upload_speed: float
    ) -> float:
        """Test the calculation of the upload percentage between the paid and actual download speed."""
        return (actual_upload_speed / paid_upload_speed) * 100

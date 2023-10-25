""""Support for calculating average sensor states and sending notifications."""
import datetime as dt
from datetime import timedelta

from homeassistant.components import persistent_notification
from homeassistant.components.recorder import history
from homeassistant.core import HomeAssistant


class SpeedtestdotnetNotifications:
    """Class updating average sensor states."""

    hass: HomeAssistant
    # Information and threshold functions for each sensor
    sensors = [
        {
            "name": "download",
            "id": "sensor.speedtest_download",
            "function": lambda a: a,
            "threshold": 0.9,
            "less_than": False,
        },
        {
            "name": "ping",
            "id": "sensor.speedtest_ping",
            "function": lambda a: a,
            "threshold": 1.0,
            "max_value": 50,
            "less_than": True,
        },
        {
            "name": "upload",
            "id": "sensor.speedtest_upload",
            "function": lambda a: a,
            "threshold": 0.8,
            "less_than": False,
        },
    ]

    def __init__(self) -> None:
        """Initialise the SpeedtestdotnetNotifications class."""

    @classmethod
    async def create(
        cls,
        hass: HomeAssistant,
        paid_download: int,
        paid_upload: int,
    ) -> None:
        """Initialise the SpeedtestdotnetNotifications class."""
        self = cls()
        self.hass = hass
        self.sensors[0]["max_value"] = paid_download
        self.sensors[2]["max_value"] = paid_upload

    def average(self, data: list) -> dict:
        """Calculate averges of each sensor's data.

        Returns a dictionary with the sum, count, and average (value) of each sensor.
        """
        # Setup dictionary to store average results of each sensor
        result = {"sum": 0.0, "count": 0, "value": 0.0}

        # Count the sum of all states
        for item in data:
            try:
                result["sum"] += float(item.state)
                result["count"] += 1
            except ValueError:
                pass

        # Calculate the average value (state)
        if result["count"] > 0:
            result["value"] = result["sum"] / result["count"]

        return result

    def compare(self, value: int, sensor_data: dict) -> bool:
        """Compare average value with threshold."""
        if not sensor_data["less_than"]:
            return value > int(sensor_data["max_value"]) * float(
                sensor_data["threshold"]
            )

        return value < int(sensor_data["max_value"]) * float(sensor_data["threshold"])

    def validate(self, data: dict) -> dict:
        """Validate sensor data to see if the minimum thresholds are met.

        Returns a dictionary with the result of each sensor.
        """
        result = {}

        for sensor in self.sensors:
            current_data = data[sensor["name"]]
            # Check if the sensor data is within the acceptable threshold.
            if (
                self.compare(current_data["value"], sensor)
                and current_data["count"] > 0
            ):
                result[sensor["name"]] = True
            else:
                result[sensor["name"]] = False

        return result

    def send_notification(self, title: str, message: str) -> None:
        """Send a notification using the REST API to the home assistant UI."""
        persistent_notification.create(self.hass, message=message, title=title)

    async def get_sensor_history(self, period_days: int, entity_id: str) -> list:
        """Get history of sensor states."""
        # Get the start date as a datetime object
        start_date = dt.datetime.now(dt.UTC) - timedelta(days=period_days)
        response = await self.hass.async_add_executor_job(
            history.state_changes_during_period,
            self.hass,
            start_date,
            None,
            entity_id,
            True,
        )
        return response[entity_id]

    async def update(self) -> bool:
        """Update and validate sensor averages."""
        result = {}
        averages = {}
        # Get average values from each sensor
        for sensor in self.sensors:
            response = await self.get_sensor_history(30, str(sensor["id"]))
            averages[sensor["name"]] = self.average(response)

        # Validate average values
        if len(averages) != 0:
            result = self.validate(averages)
            # Check if any sensor failed to meet the requirement and send a notification to the user.
            failed_sensors = [x for x in self.sensors if result[x["name"]] is False]
            if len(failed_sensors) > 0:
                failed_sensors_str = ", ".join([str(x["name"]) for x in failed_sensors])
                title = "Internet speed is slower than expected."
                message = f"Speedtest.net has detected that the internet speed does not meet the minimum acceptable requirement this month. Affected sensor(s) is/are {failed_sensors_str}.\n\nPlease find more information about how to improve connection speeds on our knowledgebase (https://www.speedtest.net/about/knowledge). \n\nIf you get this notification often, try changing the minimum threshold values in the integration settings."
                self.send_notification(title, message)

        return True

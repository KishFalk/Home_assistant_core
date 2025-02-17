"""Tests for SpeedTest config flow."""
from unittest.mock import MagicMock

from homeassistant import config_entries
from homeassistant.components import speedtestdotnet
from homeassistant.components.speedtestdotnet.const import (
    CONF_PAID_DOWNLOAD_SPEED,
    CONF_PAID_UPLOAD_SPEED,
    CONF_SERVER_ID,
    CONF_SERVER_NAME,
    DOMAIN,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


async def test_flow_works(hass: HomeAssistant) -> None:
    """Test user config."""
    result = await hass.config_entries.flow.async_init(
        speedtestdotnet.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    user_input = {CONF_PAID_DOWNLOAD_SPEED: 50.0, CONF_PAID_UPLOAD_SPEED: 30.0}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=user_input
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY


async def test_options(hass: HomeAssistant, mock_api: MagicMock) -> None:
    """Test updating options."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="SpeedTest",
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_SERVER_NAME: "Country1 - Sponsor1 - Server1",
        },
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        CONF_SERVER_NAME: "Country1 - Sponsor1 - Server1",
        CONF_SERVER_ID: "1",
    }
    await hass.async_block_till_done()

    # test setting server name to "*Auto Detect"
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_SERVER_NAME: "*Auto Detect",
        },
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        CONF_SERVER_NAME: "*Auto Detect",
        CONF_SERVER_ID: None,
    }


async def test_integration_already_configured(hass: HomeAssistant) -> None:
    """Test integration is already configured."""
    entry = MockConfigEntry(
        domain=DOMAIN,
    )
    entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(
        speedtestdotnet.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"


async def test_valid_paid_speed_input(hass: HomeAssistant) -> None:
    """Test valid paid download and upload speed input."""
    result = await hass.config_entries.flow.async_init(
        speedtestdotnet.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    user_input = {CONF_PAID_DOWNLOAD_SPEED: 50.0, CONF_PAID_UPLOAD_SPEED: 30.0}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=user_input
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY


async def test_default_paid_speed_input(hass: HomeAssistant) -> None:
    """Test default paid download and upload speed input."""
    result = await hass.config_entries.flow.async_init(
        speedtestdotnet.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    user_input = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=user_input
    )
    assert result["type"] == FlowResultType.FORM

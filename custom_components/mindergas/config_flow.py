"""Config flow for MinderGas integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .api import MinderGasAPI
from .const import (
    CONF_API_KEY,
    CONF_POST_METER_READING,
    CONF_POST_TIME,
    CONF_POST_METER_ENTITY_ID,
    CONF_UPDATE_STATS,
    CONF_UPDATE_TIME,
    CONF_RANDOMIZE_POST_TIME,
    DEFAULT_POST_TIME,
    DEFAULT_UPDATE_TIME,
    DOMAIN,
    POST_METER_WINDOW_START,
    POST_METER_WINDOW_END,
)

_LOGGER = logging.getLogger(__name__)


def _is_time_in_post_window(time_str: str) -> bool:
    """Check if time is within the meter posting window (00:05-01:00)."""
    if isinstance(time_str, str):
        try:
            hour, minute = map(int, time_str.split(":"))
        except (ValueError, IndexError):
            return False
    else:
        hour = time_str.hour
        minute = time_str.minute
    
    # Convert to minutes since midnight
    current_minutes = hour * 60 + minute
    window_start = 5  # 00:05
    window_end = 60   # 01:00
    
    return window_start <= current_minutes <= window_end


def _post_time_validator(user_input):
    """Validate post_meter_time is within window when not using random time."""
    post_meter = user_input.get(CONF_POST_METER_READING)
    randomize = user_input.get(CONF_RANDOMIZE_POST_TIME)
    post_time = user_input.get(CONF_POST_TIME)
    
    if post_meter and not randomize and post_time:
        if not _is_time_in_post_window(post_time):
            raise vol.Invalid("Time must be between 00:05 and 01:00")
    
    return user_input


class MinderGasConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MinderGas."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Return the options flow."""
        return MinderGasOptionsFlow()

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate API key
            api_key = user_input.get(CONF_API_KEY)
            
            if not api_key:
                errors[CONF_API_KEY] = "invalid_api_key"
            else:
                # Test the API key
                api = MinderGasAPI(api_key)
                try:
                    # Try to get yearly usage to validate the API key
                    result = await api.get_yearly_usage()
                    
                    # If we get here without exception, the API key is valid
                    # (result can be dict if we have data, None if 404/no data yet)
                    self.api_key = api_key
                    return await self.async_step_meter_config()
                    
                except ValueError as err:
                    # API client raises ValueError on auth errors
                    _LOGGER.error("Invalid API key: %s", err)
                    errors[CONF_API_KEY] = "invalid_auth"
                except Exception as err:
                    _LOGGER.error("Error validating API key: %s", err)
                    errors[CONF_API_KEY] = "cannot_connect"
                finally:
                    await api.close()

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "learn_more": "https://mindergas.nl/member/api",
            },
        )

    async def async_step_meter_config(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Configure meter reading settings."""
        errors = {}

        if user_input is not None:
            if user_input.get(CONF_POST_METER_READING):
                if not user_input.get(CONF_POST_METER_ENTITY_ID):
                    errors[CONF_POST_METER_ENTITY_ID] = "required"
                elif not user_input.get(CONF_RANDOMIZE_POST_TIME):
                    # Only validate time if not using random
                    if not user_input.get(CONF_POST_TIME):
                        errors[CONF_POST_TIME] = "required"
                    elif not _is_time_in_post_window(user_input.get(CONF_POST_TIME)):
                        errors[CONF_POST_TIME] = "time_out_of_window"
                
                if not errors:
                    self.meter_config = user_input
                    return await self.async_step_stats_config()
            else:
                self.meter_config = user_input
                return await self.async_step_stats_config()

        # Get available entities for meter reading
        hass: HomeAssistant = self.hass
        entity_ids = []
        
        if hass.states:
            for state in hass.states.async_all():
                # Look for sensor entities that might be gas meter readings
                entity_id = state.entity_id
                if entity_id.startswith("sensor."):
                    entity_ids.append(entity_id)

        meter_entity_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain="sensor",
            )
        ) if entity_ids else selector.TextSelector()

        schema_dict = {
            vol.Required(
                CONF_POST_METER_READING,
                default=True,
            ): bool,
            vol.Optional(
                CONF_POST_METER_ENTITY_ID,
                default="",
            ): meter_entity_selector,
            vol.Optional(
                CONF_RANDOMIZE_POST_TIME,
                default=False,
            ): bool,
            vol.Optional(
                CONF_POST_TIME,
                default=DEFAULT_POST_TIME,
            ): selector.TimeSelector(
                selector.TimeSelectorConfig(),
            ),
        }

        return self.async_show_form(
            step_id="meter_config",
            data_schema=vol.Schema(schema_dict),
            errors=errors,
            description_placeholders={
                "window_start": POST_METER_WINDOW_START,
                "window_end": POST_METER_WINDOW_END,
            },
        )

    async def async_step_stats_config(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Configure statistics update settings."""
        if user_input is not None:
            data = {
                CONF_API_KEY: self.api_key,
                **self.meter_config,
                **user_input,
            }
            
            await self.async_set_unique_id(self.api_key)
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title="MinderGas",
                data=data,
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_UPDATE_STATS,
                    default=True,
                ): bool,
                vol.Optional(
                    CONF_UPDATE_TIME,
                    default=DEFAULT_UPDATE_TIME,
                ): selector.TimeSelector(
                    selector.TimeSelectorConfig(),
                ),
            }
        )

        return self.async_show_form(
            step_id="stats_config",
            data_schema=schema,
        )


class MinderGasOptionsFlow(config_entries.OptionsFlow):
    """Options flow for MinderGas integration."""

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Clear post_time if using random
            if user_input.get(CONF_RANDOMIZE_POST_TIME):
                user_input[CONF_POST_TIME] = None
            elif user_input.get(CONF_POST_TIME) is None:
                # Set default if post_time is None and not using random
                user_input[CONF_POST_TIME] = DEFAULT_POST_TIME
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        # Use default post_time if None (was cleared due to randomize)
        post_time_value = options.get(CONF_POST_TIME)
        if post_time_value is None:
            post_time_value = DEFAULT_POST_TIME
        
        schema_dict = {
            vol.Optional(
                CONF_POST_METER_READING,
                default=options.get(CONF_POST_METER_READING, True),
            ): bool,
            vol.Optional(
                CONF_RANDOMIZE_POST_TIME,
                default=options.get(CONF_RANDOMIZE_POST_TIME, False),
            ): bool,
            vol.Optional(
                CONF_POST_TIME,
                default=post_time_value,
            ): selector.TimeSelector(
                selector.TimeSelectorConfig(),
            ),
            vol.Optional(
                CONF_UPDATE_STATS,
                default=options.get(CONF_UPDATE_STATS, True),
            ): bool,
            vol.Optional(
                CONF_UPDATE_TIME,
                default=options.get(CONF_UPDATE_TIME, DEFAULT_UPDATE_TIME),
            ): selector.TimeSelector(
                selector.TimeSelectorConfig(),
            ),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_dict),
            description_placeholders={
                "learn_more": "https://mindergas.nl/member/api",
            },
        )

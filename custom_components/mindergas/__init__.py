"""The MinderGas integration."""
import logging
from datetime import datetime, timedelta
from random import randint
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_change

from .api import MinderGasAPI
from .const import (
    CONF_API_KEY,
    CONF_POST_METER_READING,
    CONF_POST_TIME,
    CONF_POST_METER_ENTITY_ID,
    CONF_UPDATE_STATS,
    CONF_UPDATE_TIME,
    CONF_RANDOMIZE_POST_TIME,
    DOMAIN,
    SENSOR_PLATFORM,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: Final = [SENSOR_PLATFORM]

# Set up custom icon - this tells HA to use our icon.png from the integration folder
ENTITY_ICON = "mdi:gas-cylinder"

# Service/Action names
SERVICE_UPDATE_STATS = "update_stats"
SERVICE_POST_METER_READING = "post_meter_reading"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up MinderGas integration from YAML config (if any)."""
    # This integration uses config flow, so no YAML setup
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MinderGas from a config entry."""
    
    _LOGGER.info("async_setup_entry called for MinderGas")
    
    if entry is None:
        _LOGGER.error("No config entry provided for mindergas integration")
        return False
    
    _LOGGER.debug("Config entry ID: %s", entry.entry_id)
    
    try:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.debug("hass.data initialized")
        
        api_key = entry.data.get(CONF_API_KEY)
        if not api_key:
            _LOGGER.error("API key not configured for MinderGas integration")
            return False
        
        _LOGGER.debug("API key found, initializing MinderGasAPI")
        api = MinderGasAPI(api_key, session=None)
        _LOGGER.debug("MinderGasAPI initialized")
        
        hass.data[DOMAIN][entry.entry_id] = {
            "api": api,
            "config": entry.data,
            "options": entry.options,
            "unsub_tracker": [],
            "yearly_usage": None,
            "forecast": None,
            "degree_day": None,
        }
        _LOGGER.debug("Integration data structure initialized")
        
    except Exception as err:
        _LOGGER.error("Failed to initialize integration data: %s", err, exc_info=True)
        return False
    
    # Get effective config (options override entry data)
    def get_option(key: str, default=None):
        """Get option value, falling back to config entry data."""
        return entry.options.get(key, entry.data.get(key, default))
    
    # Fetch and store initial stats data
    if get_option(CONF_UPDATE_STATS):
        try:
            _LOGGER.info("Fetching initial stats data...")
            yearly_usage = await api.get_yearly_usage()
            forecast = await api.get_yearly_forecast()
            degree_day = await api.get_usage_per_degree_day()
            
            # Store data in hass.data
            if yearly_usage:
                hass.data[DOMAIN][entry.entry_id]["yearly_usage"] = yearly_usage
                _LOGGER.debug("Stored yearly_usage data: %s", yearly_usage)
            if forecast:
                hass.data[DOMAIN][entry.entry_id]["forecast"] = forecast
                _LOGGER.debug("Stored forecast data: %s", forecast)
            if degree_day:
                hass.data[DOMAIN][entry.entry_id]["degree_day"] = degree_day
                _LOGGER.debug("Stored degree_day data: %s", degree_day)
            
            _LOGGER.info("Initial stats data fetched successfully")
        except Exception as err:
            _LOGGER.warning("Failed to fetch initial stats: %s", err)
    
    # Set up platforms 
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )
    _LOGGER.debug("Platform setup task created")
    
    # Register service/action handlers
    async def handle_update_stats(call):
        """Handle update_stats action."""
        _LOGGER.info("Action 'update_stats' triggered")
        api = hass.data[DOMAIN][entry.entry_id]["api"]
        try:
            _LOGGER.debug("Fetching yearly usage...")
            yearly_usage = await api.get_yearly_usage()
            _LOGGER.debug("Yearly usage retrieved: %s", yearly_usage)
            
            _LOGGER.debug("Fetching yearly forecast...")
            forecast = await api.get_yearly_forecast()
            _LOGGER.debug("Yearly forecast retrieved: %s", forecast)
            
            _LOGGER.debug("Fetching usage per degree day...")
            degree_day = await api.get_usage_per_degree_day()
            _LOGGER.debug("Usage per degree day retrieved: %s", degree_day)
            
            if yearly_usage is not None:
                hass.data[DOMAIN][entry.entry_id]["yearly_usage"] = yearly_usage
            if forecast is not None:
                hass.data[DOMAIN][entry.entry_id]["forecast"] = forecast
            if degree_day is not None:
                hass.data[DOMAIN][entry.entry_id]["degree_day"] = degree_day
            
            _LOGGER.info("Manual stats update completed successfully")
            
            # Refresh sensor states by firing event that sensors listen to
            hass.bus.async_fire(
                f"{DOMAIN}_stats_updated",
                {"entry_id": entry.entry_id}
            )
        except Exception as err:
            _LOGGER.error("Error updating stats: %s", err, exc_info=True)
    
    async def handle_post_meter_reading(call):
        """Handle post_meter_reading action."""
        _LOGGER.info("Action 'post_meter_reading' triggered")
        api = hass.data[DOMAIN][entry.entry_id]["api"]
        meter_entity_id = get_option(CONF_POST_METER_ENTITY_ID)
        
        _LOGGER.debug("Meter entity ID configured: %s", meter_entity_id)
        
        if not meter_entity_id:
            _LOGGER.error("Meter entity ID not configured")
            return
        
        meter_value = hass.states.get(meter_entity_id)
        if not meter_value:
            _LOGGER.error("Meter entity %s not found", meter_entity_id)
            return
        
        _LOGGER.debug("Meter entity state: %s", meter_value.state)
        
        try:
            reading = float(meter_value.state)
            _LOGGER.debug("Parsed meter reading: %s", reading)
            
            # Post reading for today
            date_str = datetime.now().strftime("%Y-%m-%d")
            _LOGGER.debug("Posting meter reading for date: %s, value: %s", date_str, reading)
            
            result = await api.post_meter_reading(date_str, reading)
            _LOGGER.info("Manual meter reading posted successfully: date=%s, reading=%s, result=%s", date_str, reading, result)
        except Exception as err:
            _LOGGER.error("Error posting meter reading: %s", err, exc_info=True)
    
    try:
        _LOGGER.debug("Registering services")
        hass.services.async_register(DOMAIN, SERVICE_UPDATE_STATS, handle_update_stats)
        hass.services.async_register(DOMAIN, SERVICE_POST_METER_READING, handle_post_meter_reading)
        _LOGGER.debug("Services registered successfully")
    except Exception as err:
        _LOGGER.error("Error registering services: %s", err, exc_info=True)
        return False
    
    # Setup options flow
    try:
        _LOGGER.debug("Setting up options flow")
        entry.async_on_unload(entry.add_update_listener(async_update_entry))
        _LOGGER.debug("Options flow setup completed")
    except Exception as err:
        _LOGGER.error("Error setting up options flow: %s", err, exc_info=True)
        return False
    
    _LOGGER.info("MinderGas integration setup completed successfully")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Unsubscribe from scheduled tasks
        data = hass.data[DOMAIN][entry.entry_id]
        for unsub in data.get("unsub_tracker", []):
            unsub()
        
        # Close API session
        api = data.get("api")
        if api:
            await api.close()
        
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_update_entry(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)

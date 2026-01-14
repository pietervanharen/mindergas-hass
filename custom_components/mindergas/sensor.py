"""Sensors for MinderGas integration."""
import logging
from datetime import date
from typing import Any, Callable, Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfVolume
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .api import MinderGasAPI
from .const import DOMAIN, CONF_UPDATE_STATS

_LOGGER = logging.getLogger(__name__)

# Unit mapping from API to Home Assistant
UNIT_MAP = {
    "cubic_meter": UnitOfVolume.CUBIC_METERS,
    "kilowatt_hour": UnitOfEnergy.KILO_WATT_HOUR,
    "gigajoule": "GJ",
    "megajoule": "MJ",
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities."""
    
    entities = []
    
    # Add stats sensors if enabled
    if config_entry.data.get(CONF_UPDATE_STATS):
        entities.extend(
            [
                # Yearly usage sensors
                MinderGasYearlyUsagePeriodStartSensor(hass, config_entry),
                MinderGasYearlyUsagePeriodEndSensor(hass, config_entry),
                MinderGasYearlyHeatingUsageSensor(hass, config_entry),
                MinderGasYearlyTotalUsageSensor(hass, config_entry),
                
                # Yearly forecast sensors
                MinderGasYearlyForecastPeriodStartSensor(hass, config_entry),
                MinderGasYearlyForecastPeriodEndSensor(hass, config_entry),
                MinderGasYearlyHeatingForecastSensor(hass, config_entry),
                MinderGasYearlyTotalForecastSensor(hass, config_entry),
                
                # Degree day sensor
                MinderGasUsagePerDegreeDaySensor(hass, config_entry),
            ]
        )
    
    async_add_entities(entities)


class MinderGasBaseSensor(SensorEntity):
    """Base class for MinderGas sensors."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry):
        """Initialize the sensor."""
        self.hass = hass
        self.config_entry = config_entry
        self._attr_attribution = "Data provided by MinderGas"
        self._attr_should_poll = False
        self._unsub_update = None
        # Use domain and unique_id for entity_id
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": "MinderGas",
            "manufacturer": "MinderGas",
        }

    def _get_data(self) -> dict[str, Any]:
        """Safely get data from hass.data."""
        try:
            if DOMAIN not in self.hass.data:
                return {}
            if self.config_entry.entry_id not in self.hass.data[DOMAIN]:
                return {}
            return self.hass.data[DOMAIN][self.config_entry.entry_id]
        except (KeyError, TypeError):
            return {}

    async def async_added_to_hass(self) -> None:
        """Subscribe to updates."""
        await super().async_added_to_hass()
        
        # Subscribe to stats update events
        @callback
        def handle_stats_update(event):
            """Handle stats update event."""
            if event.data.get("entry_id") == self.config_entry.entry_id:
                self.async_write_ha_state()
        
        self._unsub_update = self.hass.bus.async_listen(
            f"{DOMAIN}_stats_updated",
            handle_stats_update,
        )
        
        # Trigger initial update
        await self._async_update()

    async def async_will_remove_from_hass(self) -> None:
        """Unsubscribe from updates."""
        await super().async_will_remove_from_hass()
        if self._unsub_update:
            self._unsub_update()

    async def _async_update(self) -> None:
        """Update sensor state."""
        pass


class MinderGasYearlyUsagePeriodStartSensor(MinderGasBaseSensor):
    """Sensor for yearly usage period start date."""

    _attr_unique_id = "mindergas_yearly_usage_period_start"
    _attr_name = "Yearly Usage Period Start"
    _attr_icon = "mdi:calendar-start"
    _attr_device_class = SensorDeviceClass.DATE

    @property
    def native_value(self) -> Optional[date]:
        """Return the sensor value."""
        data = self._get_data()
        yearly_usage = data.get("yearly_usage")
        
        if yearly_usage:
            date_str = yearly_usage.get("date_from")
            if date_str:
                return date.fromisoformat(date_str)
        
        return None


class MinderGasYearlyUsagePeriodEndSensor(MinderGasBaseSensor):
    """Sensor for yearly usage period end date."""

    _attr_unique_id = "mindergas_yearly_usage_period_end"
    _attr_name = "Yearly Usage Period End"
    _attr_icon = "mdi:calendar-end"
    _attr_device_class = SensorDeviceClass.DATE

    @property
    def native_value(self) -> Optional[date]:
        """Return the sensor value."""
        data = self._get_data()
        yearly_usage = data.get("yearly_usage")
        
        if yearly_usage:
            date_str = yearly_usage.get("date_to")
            if date_str:
                return date.fromisoformat(date_str)
        
        return None


class MinderGasYearlyForecastPeriodStartSensor(MinderGasBaseSensor):
    """Sensor for yearly forecast period start date."""

    _attr_unique_id = "mindergas_yearly_forecast_period_start"
    _attr_name = "Yearly Forecast Period Start"
    _attr_icon = "mdi:calendar-start"
    _attr_device_class = SensorDeviceClass.DATE

    @property
    def native_value(self) -> Optional[date]:
        """Return the sensor value."""
        data = self._get_data()
        forecast = data.get("forecast")
        
        if forecast:
            date_str = forecast.get("date_from")
            if date_str:
                return date.fromisoformat(date_str)
        
        return None


class MinderGasYearlyForecastPeriodEndSensor(MinderGasBaseSensor):
    """Sensor for yearly forecast period end date."""

    _attr_unique_id = "mindergas_yearly_forecast_period_end"
    _attr_name = "Yearly Forecast Period End"
    _attr_icon = "mdi:calendar-end"
    _attr_device_class = SensorDeviceClass.DATE

    @property
    def native_value(self) -> Optional[date]:
        """Return the sensor value."""
        data = self._get_data()
        forecast = data.get("forecast")
        
        if forecast:
            date_str = forecast.get("date_to")
            if date_str:
                return date.fromisoformat(date_str)
        
        return None


class MinderGasYearlyHeatingUsageSensor(MinderGasBaseSensor):
    """Sensor for yearly heating usage."""

    _attr_unique_id = "mindergas_yearly_heating_usage"
    _attr_name = "Yearly Heating Usage"
    _attr_icon = "mdi:fire"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.VOLUME

    @property
    def native_value(self) -> Optional[float]:
        """Return the sensor value."""
        data = self._get_data()
        yearly_usage = data.get("yearly_usage")
        
        if yearly_usage and "heating" in yearly_usage:
            return yearly_usage["heating"].get("value")
        
        return None

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement."""
        data = self._get_data()
        yearly_usage = data.get("yearly_usage")
        
        if yearly_usage and "heating" in yearly_usage:
            unit = yearly_usage["heating"].get("unit")
            return UNIT_MAP.get(unit, unit)
        
        return None


class MinderGasYearlyTotalUsageSensor(MinderGasBaseSensor):
    """Sensor for yearly total usage."""

    _attr_unique_id = "mindergas_yearly_total_usage"
    _attr_name = "MinderGas Yearly Total Usage"
    _attr_icon = "mdi:meter-gas"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.VOLUME

    @property
    def native_value(self) -> Optional[float]:
        """Return the sensor value."""
        data = self._get_data()
        yearly_usage = data.get("yearly_usage")
        
        if yearly_usage and "total" in yearly_usage:
            return yearly_usage["total"].get("value")
        
        return None

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement."""
        data = self._get_data()
        yearly_usage = data.get("yearly_usage")
        
        if yearly_usage and "total" in yearly_usage:
            unit = yearly_usage["total"].get("unit")
            return UNIT_MAP.get(unit, unit)
        
        return None


class MinderGasYearlyHeatingForecastSensor(MinderGasBaseSensor):
    """Sensor for yearly heating forecast."""

    _attr_unique_id = "mindergas_yearly_heating_forecast"
    _attr_name = "Yearly Heating Forecast"
    _attr_icon = "mdi:fire"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> Optional[float]:
        """Return the sensor value."""
        data = self._get_data()
        forecast = data.get("forecast")
        
        if forecast and "heating" in forecast:
            return forecast["heating"].get("value")
        
        return None

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement."""
        data = self._get_data()
        forecast = data.get("forecast")
        
        if forecast and "heating" in forecast:
            unit = forecast["heating"].get("unit")
            return UNIT_MAP.get(unit, unit)
        
        return None


class MinderGasYearlyTotalForecastSensor(MinderGasBaseSensor):
    """Sensor for yearly total forecast."""

    _attr_unique_id = "mindergas_yearly_total_forecast"
    _attr_name = "Yearly Total Forecast"
    _attr_icon = "mdi:meter-gas"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> Optional[float]:
        """Return the sensor value."""
        data = self._get_data()
        forecast = data.get("forecast")
        
        if forecast and "total" in forecast:
            return forecast["total"].get("value")
        
        return None

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement."""
        data = self._get_data()
        forecast = data.get("forecast")
        
        if forecast and "total" in forecast:
            unit = forecast["total"].get("unit")
            return UNIT_MAP.get(unit, unit)
        
        return None


class MinderGasUsagePerDegreeDaySensor(MinderGasBaseSensor):
    """Sensor for usage per degree day."""

    _attr_unique_id = "mindergas_usage_per_degree_day"
    _attr_name = "Usage Per Degree Day"
    _attr_icon = "mdi:thermometer-lines"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> Optional[float]:
        """Return the sensor value."""
        data = self._get_data()
        degree_day = data.get("degree_day")
        
        if degree_day and "avg_last_365_days" in degree_day:
            return degree_day["avg_last_365_days"].get("value")
        
        return None

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement."""
        data = self._get_data()
        degree_day = data.get("degree_day")
        
        if degree_day and "avg_last_365_days" in degree_day:
            unit = degree_day["avg_last_365_days"].get("unit")
            return UNIT_MAP.get(unit, unit)
        
        return None

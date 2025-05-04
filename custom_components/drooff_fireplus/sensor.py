from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        DrooffSensor(coordinator, "temperature", "Temperatur", "°C"),
        DrooffSensor(coordinator, "slider", "Luftschieberstellung", "%"),
        DrooffSensor(coordinator, "draft", "Feinzug", "")
    ])

class DrooffSensor(SensorEntity):
    def __init__(self, coordinator, key, name, unit):
        self.coordinator = coordinator
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = f"drooff_{key}"
        self._key = key

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)

    async def async_update(self):
        await self.coordinator.async_request_refresh()

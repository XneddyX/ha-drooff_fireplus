from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, LOGGER
from .coordinator import DrooffDataUpdateCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = DrooffDataUpdateCoordinator(hass, entry logger=LOGGER,)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True
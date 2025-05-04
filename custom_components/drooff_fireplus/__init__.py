from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant



from .coordinator import DrooffDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry
    ) -> bool:
    """Set up the Drooff Fire+ integration from a config entry."""   
    coordinator = DrooffDataUpdateCoordinator(hass, entry)
    
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setup(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True

async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
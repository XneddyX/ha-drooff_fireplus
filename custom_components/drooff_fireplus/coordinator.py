import aiohttp
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
# from homeassistant.config_entries import ConfigEntry
from datetime import timedelta
from .const import DOMAIN, LOGGER

class DrooffDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass,  entry):
        super().__init__(
            hass=hass, 
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=entry.data["interval"])
        )

        self.ip = entry.data["ip"]

    async def _async_update_data(self):
        url = f"http://{self.ip}/php/easpanel.php"
        LOGGER.debug(f"Fetching data from {url}")
        try:
            async with async_timeout.timeout(5):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        text = await response.text()
                        LOGGER.debug(f"Response: {text}")
                        if response.status != 200:
                            raise UpdateFailed(f"Error fetching data: {response.status}")
                        values = text.strip().split("\n")
                        return {
                            "temperature": float(values[5]),
                            "slider": float(values[6]),
                            "draft": float(values[7]),
                            "raw": values
                        }
        except Exception as e:
            raise UpdateFailed(f"Error fetching data: {e}")

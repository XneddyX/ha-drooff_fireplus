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
                        raw = await response.text()
                        LOGGER.debug(f"Raw response: {raw}")
                        if raw.startswith('\ufeff') or raw.startswith('ï»¿'):
                            raw = raw.lstrip('\ufeff').lstrip('ï»¿')
                        LOGGER.debug(f"Raw response 2: {raw}")
                        clean = raw.strip('"')
                        LOGGER.debug(f"Cleaned response: {clean}")
                        decoded = bytes(clean, "utf-8").decode("unicode_escape")
                        LOGGER.debug(f"Decoded response: {decoded}")
                        values = decoded.strip().split("\n")
                        LOGGER.debug(f"Parsed values: {values}")

                        return {
                            "temperature": float(values[5]),
                            "slider": float(values[6]),
                            "draft": float(values[7]),
                            "raw": values
                        }
        except Exception as e:
            raise UpdateFailed(f"Error fetching data: {e}")

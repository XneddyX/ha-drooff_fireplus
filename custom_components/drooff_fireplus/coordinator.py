import aiohttp
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed


class DrooffDataUpdateCoordinator(DataUpdateCoordinator):

    async def _async_update_data(self):
        url = f"http://{self.ip}/php/easpanel.php"
        try:
            async with async_timeout.timeout(5):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        text = await response.text()
                        values = text.strip().split("\n")
                        return {
                            "temperature": float(values[5]),
                            "slider": float(values[6]),
                            "draft": float(values[7]),
                            "raw": values
                        }
        except Exception as e:
            raise UpdateFailed(f"Error fetching data: {e}")

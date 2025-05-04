from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, DEFAULT_INTERVAL, DEFAULT_IP

class DrooffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input:
            return self.async_create_entry(title="Drooff Fire+", data=user_input)

        schema = vol.Schema({
            vol.Required("ip", default=DEFAULT_IP): str,
            vol.Required("interval", default=DEFAULT_INTERVAL): int,
        })

        return self.async_show_form(step_id="user", data_schema=schema)

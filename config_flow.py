"""Config flow for the NEP Viewer integration."""

from __future__ import annotations

import logging

import voluptuous as vol
from aiohttp import ClientSession

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import CannotConnect, InvalidAuth, NepViewerApi
from .const import CONF_SN, DOMAIN

_LOGGER = logging.getLogger(__name__)


class NepViewerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NEP Viewer."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            session: ClientSession = async_create_clientsession(self.hass)

            api = NepViewerApi(
                session=session,
                email=user_input[CONF_EMAIL],
                password=user_input[CONF_PASSWORD],
                sn=user_input[CONF_SN],
            )

            try:
                await api.async_login()

            except InvalidAuth:
                errors["base"] = "invalid_auth"

            except CannotConnect:
                errors["base"] = "cannot_connect"

            except Exception as err:
                _LOGGER.exception(
                    "Unexpected error during NEP Viewer login: %s",
                    err,
                )
                errors["base"] = "unknown"

            else:
                await self.async_set_unique_id(user_input[CONF_EMAIL])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="NEP Viewer",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_SN): str,
                }
            ),
            errors=errors,
        )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
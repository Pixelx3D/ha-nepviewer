"""DataUpdateCoordinator for the NEP Viewer integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import NepViewerApi
from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class NepViewerDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Class to manage fetching NEP Viewer data."""

    def __init__(self, hass: HomeAssistant, api: NepViewerApi) -> None:
        """Initialize the coordinator."""
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from the API."""
        try:
            return await self.api.async_get_data()
        except Exception as err:
            _LOGGER.exception("NEPVIEWER: Coordinator update failed")
            raise UpdateFailed(
                f"Error communicating with NEP Viewer API: {err}"
            ) from err
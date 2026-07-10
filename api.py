"""API client for the NEP Viewer integration."""

from __future__ import annotations

import asyncio
import logging

from aiohttp import ClientError, ClientSession

from .const import API_BASE, LOGIN_ENDPOINT, REQUEST_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class NepViewerError(Exception):
    """Base exception for NEP Viewer."""


class InvalidAuth(NepViewerError):
    """Invalid authentication."""


class CannotConnect(NepViewerError):
    """Unable to connect to the NEP Viewer API."""


class NepViewerApi:
    """NEP Viewer API client."""

    def __init__(
        self,
        session: ClientSession,
        email: str,
        password: str,
        sn: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._email = email
        self._password = password
        self._sn = sn
        self._token: str | None = None

    @property
    def token(self) -> str | None:
        """Return the authentication token."""
        return self._token

    async def async_login(self) -> bool:
        """Authenticate against the NEP Viewer API."""

        url = f"{API_BASE}{LOGIN_ENDPOINT}"

        payload = {
            "account": self._email,
            "password": self._password,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://user.nepviewer.com",
            "Client": "web",
            "Oem": "NEP",
            "Lan": "1",
            "App": "0",
        }

        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                response = await self._session.post(
                    url,
                    json=payload,
                    headers=headers,
                )

            if response.status in (401, 403):
                raise InvalidAuth

            if response.status != 200:
                raise CannotConnect

            data = await response.json()

        except TimeoutError as err:
            raise CannotConnect from err

        except ClientError as err:
            raise CannotConnect from err

        if data.get("code") != 200:
            raise InvalidAuth

        token = (
            data.get("data", {})
            .get("tokenInfo", {})
            .get("token")
        )

        if not token:
            raise InvalidAuth

        self._token = token

        return True

    async def async_get_data(self) -> dict:
        """Fetch the latest plant data from the NEP Viewer API."""

        if self._token is None:
            await self.async_login()

        url = f"{API_BASE}/v2/device/statistics/overview"

        headers = {
            "Authorization": self._token,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://user.nepviewer.com",
            "Client": "web",
            "Oem": "NEP",
            "Lan": "1",
            "App": "0",
        }

        payload = {
            "sn": self._sn,
        }

        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                response = await self._session.post(
                    url,
                    json=payload,
                    headers=headers,
                )

            if response.status != 200:
                _LOGGER.error(
                    "POST %s returned HTTP %s",
                    url,
                    response.status,
                )
                raise CannotConnect

            data = await response.json()

            if data.get("code") != 200:
                _LOGGER.error("NEP API returned: %s", data)
                raise CannotConnect

            return data

        except TimeoutError as err:
            raise CannotConnect from err

        except ClientError as err:
            raise CannotConnect from err
"""MinderGas API client."""
import logging
from datetime import datetime
from typing import Optional

import aiohttp

from .const import (
    API_BASE_URL,
    API_VERSION,
    ENDPOINT_GET_FORECAST,
    ENDPOINT_GET_USAGE_PER_DEGREE_DAY,
    ENDPOINT_GET_YEARLY_USAGE,
    ENDPOINT_POST_METER,
)

_LOGGER = logging.getLogger(__name__)


class MinderGasAPI:
    """MinderGas API client."""

    def __init__(self, api_key: str, session: Optional[aiohttp.ClientSession] = None):
        """Initialize the API client."""
        self.api_key = api_key
        self.session = session
        self._close_session = False

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
            self._close_session = True
        return self.session

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._close_session and self.session:
            await self.session.close()

    def _get_headers(self) -> dict:
        """Get required headers for API requests."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "API-VERSION": API_VERSION,
            "AUTH-TOKEN": self.api_key,
        }

    async def post_meter_reading(self, date: str, reading: float) -> bool:
        """
        Post a meter reading to MinderGas.

        Args:
            date: Date in format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
            reading: The meter reading value

        Returns:
            True if successful, False otherwise
        """
        session = await self._get_session()
        url = f"{API_BASE_URL}{ENDPOINT_POST_METER}"
        data = {"date": date, "reading": reading}

        try:
            async with session.post(url, json=data, headers=self._get_headers()) as resp:
                if resp.status == 201:
                    _LOGGER.debug("Successfully posted meter reading: %s", reading)
                    return True
                elif resp.status == 401:
                    _LOGGER.error("Invalid API key")
                    return False
                elif resp.status == 402:
                    _LOGGER.error("Payment required - API access expired")
                    return False
                elif resp.status == 403:
                    _LOGGER.error("API access blocked - too many requests")
                    return False
                elif resp.status == 422:
                    text = await resp.text()
                    _LOGGER.error("Validation error posting meter reading: %s", text)
                    return False
                else:
                    _LOGGER.error(
                        "Unexpected status %s posting meter reading: %s",
                        resp.status,
                        await resp.text(),
                    )
                    return False
        except Exception as err:
            _LOGGER.error("Error posting meter reading: %s", err)
            return False

    async def get_yearly_usage(self) -> Optional[dict]:
        """
        Get yearly usage data.

        Returns:
            Dictionary with usage data or None if request failed
        """
        session = await self._get_session()
        url = f"{API_BASE_URL}{ENDPOINT_GET_YEARLY_USAGE}"

        try:
            async with session.get(url, headers=self._get_headers()) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    _LOGGER.debug("Retrieved yearly usage data")
                    return data
                elif resp.status == 404:
                    _LOGGER.debug("No usage data available yet")
                    return None
                elif resp.status == 401:
                    _LOGGER.error("Invalid API key")
                    raise ValueError("Invalid API key provided")
                elif resp.status == 402:
                    _LOGGER.error("Payment required - API access expired")
                    raise ValueError("API access expired - payment required")
                elif resp.status == 403:
                    _LOGGER.error("API access blocked - too many requests")
                    raise ValueError("API access blocked - too many requests")
                else:
                    _LOGGER.error(
                        "Unexpected status %s getting yearly usage: %s",
                        resp.status,
                        await resp.text(),
                    )
                    return None
        except Exception as err:
            _LOGGER.error("Error getting yearly usage: %s", err)
            return None

    async def get_yearly_forecast(self) -> Optional[dict]:
        """
        Get yearly forecast data.

        Returns:
            Dictionary with forecast data or None if request failed
        """
        session = await self._get_session()
        url = f"{API_BASE_URL}{ENDPOINT_GET_FORECAST}"

        try:
            async with session.get(url, headers=self._get_headers()) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    _LOGGER.debug("Retrieved yearly forecast data")
                    return data
                elif resp.status == 404:
                    _LOGGER.debug("Not enough data to forecast yet")
                    return None
                elif resp.status == 401:
                    _LOGGER.error("Invalid API key")
                    return None
                elif resp.status == 402:
                    _LOGGER.error("Payment required - API access expired")
                    return None
                elif resp.status == 403:
                    _LOGGER.error("API access blocked - too many requests")
                    return None
                else:
                    _LOGGER.error(
                        "Unexpected status %s getting yearly forecast: %s",
                        resp.status,
                        await resp.text(),
                    )
                    return None
        except Exception as err:
            _LOGGER.error("Error getting yearly forecast: %s", err)
            return None

    async def get_usage_per_degree_day(self) -> Optional[dict]:
        """
        Get usage per degree day data.

        Returns:
            Dictionary with usage per degree day or None if request failed
        """
        session = await self._get_session()
        url = f"{API_BASE_URL}{ENDPOINT_GET_USAGE_PER_DEGREE_DAY}"

        try:
            async with session.get(url, headers=self._get_headers()) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    _LOGGER.debug("Retrieved usage per degree day data")
                    return data
                elif resp.status == 404:
                    _LOGGER.debug("No usage per degree day data available yet")
                    return None
                elif resp.status == 401:
                    _LOGGER.error("Invalid API key")
                    return None
                elif resp.status == 402:
                    _LOGGER.error("Payment required - API access expired")
                    return None
                elif resp.status == 403:
                    _LOGGER.error("API access blocked - too many requests")
                    return None
                else:
                    _LOGGER.error(
                        "Unexpected status %s getting usage per degree day: %s",
                        resp.status,
                        await resp.text(),
                    )
                    return None
        except Exception as err:
            _LOGGER.error("Error getting usage per degree day: %s", err)
            return None

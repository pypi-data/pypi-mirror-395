import aiohttp
import asyncio
import logging
import datetime
import typing
from aiohttp import ClientSession
from urllib.parse import urljoin

LOGGER = logging.getLogger(__name__)

class FlussApiClientError(Exception):
    """Exception to indicate a general API error."""

class FlussDeviceError(FlussApiClientError):
    """Exception to indicate an error occurred when retrieving devices."""

class FlussApiClientCommunicationError(FlussApiClientError):
    """Exception to indicate a communication error."""

class FlussApiClientAuthenticationError(FlussApiClientError):
    """Exception to indicate an authentication error."""


class FlussApiClient:
    """Fluss+ API Client."""

    def __init__(
        self,
        api_key: str,
        session: typing.Optional[ClientSession] = None,
        timeout: int = 10,
    ) -> None:
        """Initialize the Fluss+ API Client."""
        self._api_key = api_key
        self._base_url = "https://zgekzokxrl.execute-api.eu-west-1.amazonaws.com/v1/api/"
        self._timeout = timeout
        self._session = session or ClientSession()

    async def async_get_devices(self) -> typing.Any:
        """Get data from the API."""
        try:
            return await self._api_wrapper(
                method="GET",
                endpoint="device/list",
                headers={"Authorization": self._api_key},
            )
        except FlussApiClientError as error:
            LOGGER.error("Failed to get devices: %s", error)
            raise FlussDeviceError("Failed to retrieve devices") from error

    async def async_trigger_device(self, device_id: str) -> typing.Any:
        """Trigger the device."""
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        return await self._api_wrapper(
            method="POST",
            endpoint=f"device/{device_id}/trigger",
            headers={"Authorization": self._api_key},
            data={"timeStamp": timestamp, "metaData": {}},
        )

    async def _api_wrapper(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> typing.Any:
        """Make a request to the Fluss API."""
        url = urljoin(self._base_url, endpoint)
        try:
            async with asyncio.timeout(self._timeout):
                async with self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                ) as response:
                    if response.status == 401:
                        raise FlussApiClientAuthenticationError("Invalid credentials")
                    elif response.status == 403:
                        raise FlussApiClientAuthenticationError("Access forbidden")
                    response.raise_for_status()
                    return await response.json()

        except asyncio.TimeoutError as e:
            LOGGER.error("Timeout error fetching information from %s", url)
            raise FlussApiClientCommunicationError("Timeout error fetching information") from e
        except aiohttp.ClientError as ex:
            LOGGER.error("Client error fetching information from %s: %s", url, ex)
            raise FlussApiClientCommunicationError("Error fetching information") from ex
        except FlussApiClientAuthenticationError as auth_ex:
            LOGGER.error("Authentication error: %s", auth_ex)
            raise
        except Exception as exception:
            LOGGER.error("Unexpected error occurred: %s", exception)
            raise FlussApiClientError("An unexpected error occurred") from exception

    async def close(self):
        """Close the aiohttp session if it was created by this client."""
        if self._session and not self._session.closed:
            await self._session.close()

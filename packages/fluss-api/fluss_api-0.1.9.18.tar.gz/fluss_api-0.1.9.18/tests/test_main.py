import asyncio  # noqa: D100
from datetime import datetime
import socket
from unittest.mock import AsyncMock, Mock, patch

import aiohttp
import pytest

from fluss_api.main import (
    FlussApiClient,
    FlussApiClientAuthenticationError,
    FlussApiClientCommunicationError,
    FlussApiClientError,
    FlussDeviceError,
)
from aiohttp import ClientSession

@pytest.fixture
async def mock_hass():  # noqa: D103
    hass = Mock(spec=ClientSession)
    hass.data = {}  # Add missing attribute
    hass.bus = Mock()
    hass.async_update_entry = AsyncMock()  # Add missing method
    return hass


@pytest.fixture
async def api_client(mock_hass:"https://zgekzokxrl.execute-api.eu-west-1.amazonaws.com/v1/api/") -> FlussApiClient:  # type: ignore # noqa: D103, PGH003
    client = FlussApiClient("test_api_key", mock_hass)
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_async_get_devices(api_client) -> None:  # noqa: D103
    """Test the async_get_devices method."""
    with patch.object(
        api_client, "_api_wrapper", new=AsyncMock(return_value={"devices": []})
    ) as mock_api_wrapper:
        devices = await api_client.async_get_devices()
        assert devices == {"devices": []}
        mock_api_wrapper.assert_called_once_with(
            method="get",
            url="https://zgekzokxrl.execute-api.eu-west-1.amazonaws.com/v1/api/device/list",
            headers={"Authorization": "test_api_key"},
        )


@pytest.mark.asyncio
async def test_async_get_devices_error(api_client) -> None:
    """Test error handling in async_get_devices method."""
    with (
        patch.object(
            api_client,
            "_api_wrapper",
            new=AsyncMock(side_effect=FlussApiClientError("Error")),
        ) as mock_api_wrapper,
        patch("homeassistant.components.fluss.api.LOGGER.error") as mock_logger,
    ):
        with pytest.raises(FlussDeviceError):
            await api_client.async_get_devices()
        mock_api_wrapper.assert_called_once()
        # Comparing string representations to avoid object identity issues
        mock_logger.assert_called_once()
        logged_args = mock_logger.call_args[0]
        assert logged_args[0] == "Failed to get devices: %s"
        assert str(logged_args[1]) == "Error"


@pytest.mark.asyncio
async def test_async_trigger_device(api_client) -> None:  # noqa: D103
    """Test the async_trigger_device method."""
    with patch.object(
        api_client, "_api_wrapper", new=AsyncMock(return_value={})
    ) as mock_api_wrapper:
        response = await api_client.async_trigger_device("device_id")
        assert response == {}
        mock_api_wrapper.assert_called_once_with(
            method="post",
            url="https://zgekzokxrl.execute-api.eu-west-1.amazonaws.com/v1/api/device/device_id/trigger",
            headers={"Authorization": "test_api_key"},
            data={
                "timeStamp": int(datetime.now().timestamp() * 1000),
                "metaData": {},
            },
        )


@pytest.mark.asyncio
async def test_api_wrapper_authentication_error(api_client) -> None:  # noqa: D103
    """Test authentication error handling in _api_wrapper."""
    mock_response = AsyncMock()
    mock_response.status = 401
    with (
        patch.object(
            api_client._session, "request", new=AsyncMock(return_value=mock_response)
        ),
        pytest.raises(FlussApiClientAuthenticationError),
    ):
        await api_client._api_wrapper("get", "test_url")


@pytest.mark.asyncio
async def test_api_wrapper_communication_error(api_client) -> None:  # noqa: D103
    """Test communication error handling in _api_wrapper."""
    with (
        patch.object(
            api_client._session,
            "request",
            new=AsyncMock(side_effect=aiohttp.ClientError),
        ),
        pytest.raises(FlussApiClientCommunicationError),
    ):
        await api_client._api_wrapper("get", "test_url")


@pytest.mark.asyncio
async def test_api_wrapper_timeout_error(api_client) -> None:  # noqa: D103
    """Test timeout error handling in _api_wrapper."""
    with (
        patch.object(
            api_client._session,
            "request",
            new=AsyncMock(side_effect=asyncio.TimeoutError),
        ),
        pytest.raises(FlussApiClientCommunicationError),
    ):
        await api_client._api_wrapper("get", "test_url")


@pytest.mark.asyncio
async def test_api_wrapper_socket_error(api_client) -> None:  # noqa: D103
    """Test socket error handling in _api_wrapper."""
    with (
        patch.object(
            api_client._session, "request", new=AsyncMock(side_effect=socket.gaierror)
        ),
        pytest.raises(FlussApiClientCommunicationError),
    ):
        await api_client._api_wrapper("get", "test_url")


@pytest.mark.asyncio
async def test_api_wrapper_general_error(api_client) -> None:  # noqa: D103
    """Test general error handling in _api_wrapper."""
    with (
        patch.object(
            api_client._session, "request", new=AsyncMock(side_effect=Exception)
        ),
        pytest.raises(FlussApiClientError),
    ):
        await api_client._api_wrapper("get", "test_url")


@pytest.mark.asyncio
async def test_api_wrapper_success(api_client) -> None:
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"key": "value"}
    with patch.object(
        api_client._session, "request", new=AsyncMock(return_value=mock_response)
    ):
        result = await api_client._api_wrapper("get", "test_url")
        assert result == {"key": "value"}

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pandas as pd
import pytest

from orion.acrecer.acrecer import (
    AcrecerAPIError,
    AcrecerAuthService,
    AcrecerPropertiesService,
    get_all_properties_acrecer_by_city,
    get_all_properties_acrecer_by_city_sync,
)

# Marks all tests in this module as asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_httpx_client():
    """Fixture to mock httpx.AsyncClient."""
    return AsyncMock(spec=httpx.AsyncClient)


# --- Tests for AcrecerAuthService ---


@patch("orion.acrecer.acrecer.config")
async def test_auth_service_get_jwt_token_success(mock_config, mock_httpx_client):
    """Test successful JWT token retrieval."""
    mock_config.SUBJECT_MLS_ACRECER = "test_subject"
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"JWT": "test_token"}
    mock_httpx_client.get.return_value = mock_response

    auth_service = AcrecerAuthService()
    token = await auth_service.get_jwt_token(mock_httpx_client)

    assert token == "test_token"
    mock_httpx_client.get.assert_called_once()


@patch("orion.acrecer.acrecer.config")
async def test_auth_service_get_jwt_token_http_error(mock_config, mock_httpx_client):
    """Test HTTP error during token retrieval."""
    mock_config.SUBJECT_MLS_ACRECER = "test_subject"
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_httpx_client.get.side_effect = httpx.HTTPStatusError("Server Error", request=MagicMock(), response=mock_response)

    auth_service = AcrecerAuthService()
    with pytest.raises(AcrecerAPIError):
        await auth_service.get_jwt_token(mock_httpx_client)


def test_auth_service_init_no_subject():
    """Test ValueError if subject is not configured."""
    with patch("orion.acrecer.acrecer.config", SUBJECT_MLS_ACRECER=None):
        with pytest.raises(ValueError, match="SUBJECT_MLS_ACRECER no está configurado"):
            AcrecerAuthService()


# --- Tests for AcrecerPropertiesService ---


async def test_properties_service_fetch_page_success(mock_httpx_client):
    """Test successful fetching of a properties page."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"searchResults": [{"id": 1, "name": "Prop1"}]}
    mock_httpx_client.get.return_value = mock_response

    properties_service = AcrecerPropertiesService(jwt_token="test_token")
    results = await properties_service.fetch_properties_page(mock_httpx_client, "MEDELLÍN", 1)

    assert len(results) == 1
    assert results[0]["id"] == 1
    assert results[0]["ciudad"] == "MEDELLÍN"  # Check city is added


async def test_properties_service_fetch_page_empty(mock_httpx_client):
    """Test fetching a page with no results."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"searchResults": []}
    mock_httpx_client.get.return_value = mock_response

    properties_service = AcrecerPropertiesService(jwt_token="test_token")
    results = await properties_service.fetch_properties_page(mock_httpx_client, "MEDELLÍN", 1)

    assert len(results) == 0


async def test_properties_service_fetch_all_for_city(mocker):
    """Test fetching all properties for a city with pagination."""
    # Mock the service's own method to avoid actual async calls within the test
    mocker.patch("asyncio.sleep", new_callable=AsyncMock)
    mock_fetch_page = mocker.patch(
        "orion.acrecer.acrecer.AcrecerPropertiesService.fetch_properties_page",
        new_callable=AsyncMock,
    )
    # Simulate two pages of results, then an empty page to stop the loop
    mock_fetch_page.side_effect = [
        [{"id": 1}],
        [{"id": 2}],
        [],
    ]

    properties_service = AcrecerPropertiesService(jwt_token="test_token")
    all_props = await properties_service.fetch_all_properties_for_city(AsyncMock(), "MEDELLÍN")

    assert len(all_props) == 2
    assert mock_fetch_page.call_count == 3


# --- Tests for AcrecerClient and Wrapper Functions ---


@patch("orion.acrecer.acrecer.AcrecerClient.get_all_properties_by_cities", new_callable=AsyncMock)
async def test_wrapper_get_all_properties_by_city(mock_get_all):
    """Test the async wrapper function."""
    mock_get_all.return_value = pd.DataFrame([{"id": 1}])
    df = await get_all_properties_acrecer_by_city(cities=["MEDELLÍN"])
    assert not df.empty
    mock_get_all.assert_called_once_with(cities=["MEDELLÍN"])


@patch("orion.acrecer.acrecer.asyncio.run")
@patch("orion.acrecer.acrecer.get_all_properties_acrecer_by_city")
def test_wrapper_get_all_properties_by_city_sync(mock_async_func, mock_asyncio_run):
    """Test the sync wrapper function."""
    mock_asyncio_run.return_value = pd.DataFrame([{"id": 1}])
    df = get_all_properties_acrecer_by_city_sync(cities=["MEDELLÍN"])

    assert not df.empty
    mock_async_func.assert_called_once_with(cities=["MEDELLÍN"])
    mock_asyncio_run.assert_called_once()

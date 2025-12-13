import pytest
from unittest.mock import AsyncMock, patch
import aiohttp

from biosites.base import DEFAULT_USER_AGENT
from biosites.extractor import LinkExtractor
from biosites.extractors.instabio import InstaBioExtractor


@pytest.mark.asyncio
async def test_default_user_agent():
    """Test that the default user agent is set correctly."""
    extractor = LinkExtractor()

    # Check that default user agent is the expected value
    assert (
        DEFAULT_USER_AGENT
        == "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    )

    # Check that generic extractor has the default user agent
    assert extractor._generic_extractor.user_agent == DEFAULT_USER_AGENT


@pytest.mark.asyncio
async def test_custom_user_agent():
    """Test that custom user agent is properly set."""
    custom_ua = "MyCustomBot/1.0"
    extractor = LinkExtractor(user_agent=custom_ua)

    # Check that all extractors have the custom user agent
    assert extractor._generic_extractor.user_agent == custom_ua

    # Check that registered extractors also have the custom user agent
    for registered_extractor in extractor._extractors:
        assert registered_extractor.user_agent == custom_ua


@pytest.mark.asyncio
async def test_user_agent_in_requests():
    """Test that user agent is included in HTTP requests."""
    custom_ua = "TestBot/2.0"

    # Create an extractor with custom user agent
    extractor = InstaBioExtractor(user_agent=custom_ua)

    # Mock the session.get method to capture headers
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 404  # Return 404 so it doesn't try to parse
        mock_response.__aenter__.return_value = mock_response
        mock_get.return_value = mock_response

        # Try to fetch JSON data (will fail but we can check headers)
        result = await extractor._fetch_json_data("test_id")
        assert result is None

        # Verify that get was called with the correct headers
        assert mock_get.called
        call_kwargs = mock_get.call_args[1]
        assert "headers" in call_kwargs
        assert call_kwargs["headers"]["User-Agent"] == custom_ua


@pytest.mark.asyncio
async def test_base_extractor_user_agent_in_fetch():
    """Test that BaseLinkExtractor passes user agent in fetch_html."""
    from biosites.extractors.littly import LittlyExtractor

    custom_ua = "FetchBot/3.0"
    extractor = LittlyExtractor(user_agent=custom_ua)

    # Mock the session.get to capture headers
    with patch.object(aiohttp.ClientSession, "get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = "<html></html>"
        mock_response.raise_for_status = AsyncMock()
        mock_response.__aenter__.return_value = mock_response
        mock_get.return_value = mock_response

        # Fetch HTML
        await extractor.fetch_html("https://example.com")

        # Verify headers were passed
        assert mock_get.called
        call_kwargs = mock_get.call_args[1]
        assert "headers" in call_kwargs
        assert call_kwargs["headers"]["User-Agent"] == custom_ua

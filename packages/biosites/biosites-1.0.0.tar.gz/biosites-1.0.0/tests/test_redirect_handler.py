import pytest
from unittest.mock import AsyncMock, patch
import aiohttp

from biosites.redirect_handler import RedirectHandler
from biosites.extractor import LinkExtractor


@pytest.mark.asyncio
async def test_is_shortener():
    """Test detection of URL shortener domains."""
    handler = RedirectHandler()

    # Known shorteners
    assert handler.is_shortener("https://bit.ly/abc123")
    assert handler.is_shortener("http://tinyurl.com/test")
    assert handler.is_shortener("https://t.co/something")
    assert handler.is_shortener("https://rebrand.ly/link")
    assert handler.is_shortener("https://custom.bit.ly/test")

    # Not shorteners
    assert not handler.is_shortener("https://linktree.com/user")
    assert not handler.is_shortener("https://google.com")
    assert not handler.is_shortener("https://github.com/user")


@pytest.mark.asyncio
async def test_resolve_url_with_301_redirect():
    """Test resolving URL with 301 redirect."""
    handler = RedirectHandler()

    # Mock the session.get to simulate redirect
    with patch.object(aiohttp.ClientSession, "get") as mock_get:
        # First request returns 301
        mock_response_301 = AsyncMock()
        mock_response_301.status = 301
        mock_response_301.headers = {"Location": "https://linktree.com/user"}
        mock_response_301.__aenter__.return_value = mock_response_301

        # Second request returns 200 (final destination)
        mock_response_200 = AsyncMock()
        mock_response_200.status = 200
        mock_response_200.text.return_value = "<html>Final page</html>"
        mock_response_200.__aenter__.return_value = mock_response_200

        mock_get.side_effect = [mock_response_301, mock_response_200]

        final_url, chain = await handler.resolve_url("https://bit.ly/test")

        assert final_url == "https://linktree.com/user"
        assert "https://bit.ly/test" in chain


@pytest.mark.asyncio
async def test_resolve_url_with_meta_refresh():
    """Test resolving URL with meta refresh redirect."""
    handler = RedirectHandler()

    html_with_meta = """
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url=https://linktree.com/user">
    </head>
    </html>
    """

    with patch.object(aiohttp.ClientSession, "get") as mock_get:
        # First request returns HTML with meta refresh
        mock_response_meta = AsyncMock()
        mock_response_meta.status = 200
        mock_response_meta.text.return_value = html_with_meta
        mock_response_meta.__aenter__.return_value = mock_response_meta

        # Second request returns final page
        mock_response_final = AsyncMock()
        mock_response_final.status = 200
        mock_response_final.text.return_value = "<html>Final</html>"
        mock_response_final.__aenter__.return_value = mock_response_final

        mock_get.side_effect = [mock_response_meta, mock_response_final]

        final_url, chain = await handler.resolve_url("https://shorturl.at/test")

        assert final_url == "https://linktree.com/user"
        assert "https://shorturl.at/test" in chain


@pytest.mark.asyncio
async def test_resolve_url_with_javascript_redirect():
    """Test resolving URL with JavaScript redirect."""
    handler = RedirectHandler()

    html_with_js = """
    <html>
    <script>
        window.location.href = "https://bio.site/user";
    </script>
    </html>
    """

    with patch.object(aiohttp.ClientSession, "get") as mock_get:
        # First request returns HTML with JS redirect
        mock_response_js = AsyncMock()
        mock_response_js.status = 200
        mock_response_js.text.return_value = html_with_js
        mock_response_js.__aenter__.return_value = mock_response_js

        # Second request returns final page
        mock_response_final = AsyncMock()
        mock_response_final.status = 200
        mock_response_final.text.return_value = "<html>Final</html>"
        mock_response_final.__aenter__.return_value = mock_response_final

        mock_get.side_effect = [mock_response_js, mock_response_final]

        final_url, chain = await handler.resolve_url("https://t.co/abc")

        assert final_url == "https://bio.site/user"
        assert "https://t.co/abc" in chain


@pytest.mark.asyncio
async def test_resolve_bitly_intermediate_page():
    """Test resolving bit.ly intermediate page."""
    handler = RedirectHandler()

    # Simulated bit.ly intermediate page
    html_intermediate = """
    <html>
    <body><a href="https://linktr.ee/user">moved here</a></body>
    </html>
    """

    with patch.object(aiohttp.ClientSession, "get") as mock_get:
        # First request returns intermediate page
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = html_intermediate
        mock_response.__aenter__.return_value = mock_response

        # Second request returns final page
        mock_response_final = AsyncMock()
        mock_response_final.status = 200
        mock_response_final.text.return_value = "<html>Final</html>"
        mock_response_final.__aenter__.return_value = mock_response_final

        mock_get.side_effect = [mock_response, mock_response_final]

        final_url, chain = await handler.resolve_url("https://bit.ly/test")

        assert final_url == "https://linktr.ee/user"
        assert "https://bit.ly/test" in chain


@pytest.mark.asyncio
async def test_no_follow_redirects():
    """Test that redirects are not followed when disabled."""
    handler = RedirectHandler(follow_redirects=False)

    final_url, chain = await handler.resolve_url("https://bit.ly/test")

    assert final_url == "https://bit.ly/test"
    assert chain == []


@pytest.mark.asyncio
async def test_max_redirects():
    """Test that max redirects limit is respected."""
    handler = RedirectHandler(max_redirects=2)

    with patch.object(aiohttp.ClientSession, "get") as mock_get:
        # Create infinite redirect loop
        mock_response = AsyncMock()
        mock_response.status = 301
        mock_response.headers = {"Location": "https://example.com/redirect"}
        mock_response.__aenter__.return_value = mock_response

        # Will be called multiple times
        mock_get.return_value = mock_response

        final_url, chain = await handler.resolve_url("https://bit.ly/loop")

        # Should stop after max_redirects
        assert len(chain) <= 2


@pytest.mark.asyncio
async def test_link_extractor_with_shortener():
    """Test LinkExtractor with URL shortener."""
    # Create a mock response for redirect
    with patch.object(RedirectHandler, "resolve_url") as mock_resolve:
        mock_resolve.return_value = (
            "https://linktree.com/user",
            ["https://bit.ly/test"],
        )

        extractor = LinkExtractor()
        result = await extractor.extract("https://bit.ly/test")

        # Should have redirect info in metadata
        assert result.metadata is not None
        assert result.metadata.get("original_url") == "https://bit.ly/test"
        assert "redirect_chain" in result.metadata
        assert result.service_type == "Linktree"


@pytest.mark.asyncio
async def test_link_extractor_without_shortener():
    """Test LinkExtractor with direct URL (no redirect)."""
    extractor = LinkExtractor()

    # Direct linktree URL should not trigger redirect resolution
    with patch.object(RedirectHandler, "resolve_url") as mock_resolve:
        # Should not be called for non-shortener URLs
        result = await extractor.extract("https://linktree.com/user")
        mock_resolve.assert_not_called()

        # Should not have redirect metadata
        assert result.metadata is None or "redirect_chain" not in result.metadata

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from biosites.extractors.linkbio_co import LinkBioCoExtractor


@pytest.fixture
def linkbio_html():
    fixture_path = Path(__file__).parent / "fixtures" / "linkbio_co.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.mark.asyncio
async def test_linkbio_co_extract_links(linkbio_html):
    extractor = LinkBioCoExtractor()
    links = await extractor.extract_links(
        linkbio_html, "https://linkbio.co/5092216HSqYLq"
    )

    # Test link count
    assert len(links) == 6, f"Expected 6 links, got {len(links)}"

    # Get all URLs for easier testing
    extracted_urls = [str(link.url) for link in links]

    # Test for expected URLs (from the fixture)
    expected_urls = [
        "https://www.amazon.jp/hz/wishlist/ls/2VUHLDLU0S8F9?ref_=wl_share",
        "https://youtube.com/@karin_1004?si=MDX5lYdsG_0TmtJi",
        "https://www.instagram.com/karin_moon1004",
        "https://www.bigo.tv/user/karin_moon",
        "https://www.tiktok.com/@1004karin",  # This was missing protocol in original
        "https://twitter.com/karinhime1004",
    ]

    for expected_url in expected_urls:
        assert expected_url in extracted_urls, f"Missing expected URL: {expected_url}"

    # Verify no linkbio.co or CDN URLs included
    for url in extracted_urls:
        assert "linkbio.co" not in url, f"linkbio.co URL should be filtered: {url}"
        assert "linkcdn.cc" not in url, f"CDN URL should be filtered: {url}"
        assert "instabio.cc" not in url, f"instabio.cc URL should be filtered: {url}"

    # Test that titles are extracted
    link_dict = {str(link.url): link for link in links}

    # Check some titles
    assert (
        link_dict[
            "https://www.amazon.jp/hz/wishlist/ls/2VUHLDLU0S8F9?ref_=wl_share"
        ].title
        == "Amazon"
    )
    assert (
        link_dict["https://youtube.com/@karin_1004?si=MDX5lYdsG_0TmtJi"].title
        == "YouTube"
    )
    assert link_dict["https://www.instagram.com/karin_moon1004"].title == "インスタ"
    assert link_dict["https://www.bigo.tv/user/karin_moon"].title == "BIGO LIVE"
    assert link_dict["https://www.tiktok.com/@1004karin"].title == "TikTok"
    twitter_link = link_dict["https://twitter.com/karinhime1004"]
    assert twitter_link.title is not None
    assert "Twitter" in twitter_link.title or "X" in twitter_link.title


@pytest.mark.asyncio
async def test_linkbio_co_can_handle():
    extractor = LinkBioCoExtractor()

    # Should handle linkbio.co URLs
    assert extractor.can_handle("https://linkbio.co/username")
    assert extractor.can_handle("http://linkbio.co/someuser")
    assert extractor.can_handle("https://www.linkbio.co/profile")

    # Should not handle other URLs
    assert not extractor.can_handle("https://linktree.com/user")
    assert not extractor.can_handle("https://example.com")
    assert not extractor.can_handle("https://instabio.cc/user")


@pytest.mark.asyncio
async def test_linkbio_co_url_fixing():
    extractor = LinkBioCoExtractor()

    # Test HTML with URL missing protocol
    html_with_broken_url = """<script>window.__data={"content":{"cmpts":[{"links":[{"link":"www.tiktok.com/@user","title":"TikTok"}]}]}}</script>"""
    links = await extractor.extract_links(
        html_with_broken_url, "https://linkbio.co/test"
    )

    assert len(links) == 1
    assert str(links[0].url) == "https://www.tiktok.com/@user"


@pytest.fixture
def linkbio_vertty_html():
    """Fixture for linkbio.co page that requires JSON endpoint fetching."""
    fixture_path = Path(__file__).parent / "fixtures" / "linkbio_vertty.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def linkbio_vertty_json():
    """Fixture for JSON data from the endpoint."""
    fixture_path = Path(__file__).parent / "fixtures" / "linkbio_vertty.json"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_linkbio_co_json_endpoint(linkbio_vertty_html, linkbio_vertty_json):
    """Test linkbio.co extractor with JSON endpoint fetching (e.g., https://linkbio.co/vertty)."""
    extractor = LinkBioCoExtractor()

    # Mock the JSON fetch to use our fixture
    with patch.object(
        extractor, "_fetch_json_data", new_callable=AsyncMock
    ) as mock_fetch:
        mock_fetch.return_value = linkbio_vertty_json

        links = await extractor.extract_links(
            linkbio_vertty_html, "https://linkbio.co/vertty"
        )

    # Should find links from the JSON endpoint
    assert len(links) > 0, "Should extract links from JSON endpoint"

    # Get all URLs for easier testing
    extracted_urls = [str(link.url) for link in links]

    # Verify no linkbio.co or CDN URLs included
    for url in extracted_urls:
        assert "linkbio.co" not in url, f"linkbio.co URL should be filtered: {url}"
        assert "linkcdn.cc" not in url, f"CDN URL should be filtered: {url}"
        assert "instabio.cc" not in url, f"instabio.cc URL should be filtered: {url}"

    # Test that the bio ID extraction works
    bio_id = extractor._extract_bio_id(linkbio_vertty_html)
    assert bio_id is not None, "Should extract bio ID from HTML"

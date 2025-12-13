import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from biosites.extractors.instabio import InstaBioExtractor


@pytest.fixture
def instabio_html():
    fixture_path = Path(__file__).parent / "fixtures" / "instabio_qwer.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def instabio_json():
    fixture_path = Path(__file__).parent / "fixtures" / "instabio_qwer.json"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_instabio_extract_links(instabio_html, instabio_json):
    extractor = InstaBioExtractor()

    # Mock the JSON fetch to use our fixture
    with patch.object(
        extractor, "_fetch_json_data", new_callable=AsyncMock
    ) as mock_fetch:
        mock_fetch.return_value = instabio_json

        links = await extractor.extract_links(
            instabio_html, "https://instabio.cc/QWER_beyourharmony"
        )

    # Test link count
    assert len(links) > 0

    # Get all URLs for easier testing
    extracted_urls = [str(link.url) for link in links]

    # Test for expected URLs (from the JSON fixture)
    expected_urls = [
        # Shop links
        "https://www.yes24.com/product/category/series/003001018002001?SeriesNumber=360433",
        "https://hottracks.kyobobook.co.kr/ht/record/detail/2300186596129",
        "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=364869081",
        "https://shop.weverse.io/ko/shop/KRW/artists/157",
        # Social links
        "https://youtube.com/@qwer_band_official?si=Pj7WXWj83T5tMSRL",
        "https://x.com/official_QWER",
        "https://www.instagram.com/qwerband_official",
        "https://www.threads.com/@qwerband_official",
        "https://www.tiktok.com/@qwerband_official?_t=ZS-8wfgNf7Ai2c&_r=1",
    ]

    for expected_url in expected_urls:
        assert expected_url in extracted_urls, f"Missing expected URL: {expected_url}"

    # Verify no instabio.cc URLs included
    for url in extracted_urls:
        assert "instabio.cc" not in url, f"instabio.cc URL should be filtered: {url}"
        assert "linkcdn.cc" not in url, f"CDN URL should be filtered: {url}"

    # Test that titles are extracted
    link_dict = {str(link.url): link for link in links}

    # Check some titles
    assert (
        link_dict[
            "https://www.yes24.com/product/category/series/003001018002001?SeriesNumber=360433"
        ].title
        == "YES24"
    )
    assert (
        link_dict[
            "https://hottracks.kyobobook.co.kr/ht/record/detail/2300186596129"
        ].title
        == "HOTTRACKS"
    )
    assert (
        link_dict["https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=364869081"].title
        == "ALADIN"
    )
    assert (
        link_dict["https://shop.weverse.io/ko/shop/KRW/artists/157"].title == "Weverse"
    )

    # Social media titles
    youtube_link = link_dict["https://youtube.com/@qwer_band_official?si=Pj7WXWj83T5tMSRL"]
    assert youtube_link.title is not None
    assert "YouTube" in youtube_link.title
    
    twitter_link = link_dict["https://x.com/official_QWER"]
    assert twitter_link.title is not None
    assert "Twitter" in twitter_link.title or "x" in twitter_link.title.lower()


@pytest.mark.asyncio
async def test_instabio_can_handle():
    extractor = InstaBioExtractor()

    # Should handle instabio.cc URLs
    assert extractor.can_handle("https://instabio.cc/username")
    assert extractor.can_handle("http://instabio.cc/someuser")
    assert extractor.can_handle("https://www.instabio.cc/profile")

    # Should not handle other URLs
    assert not extractor.can_handle("https://linktree.com/user")
    assert not extractor.can_handle("https://example.com")


@pytest.mark.asyncio
async def test_instabio_extract_bio_id():
    extractor = InstaBioExtractor()

    # Test HTML with bio ID
    html_with_id = """<script>window.__data={"bio":{"id":"7052606MNYm7F"}}</script>"""
    bio_id = extractor._extract_bio_id(html_with_id)
    assert bio_id == "7052606MNYm7F"

    # Test HTML without bio ID
    html_without_id = """<script>window.__data={}</script>"""
    bio_id = extractor._extract_bio_id(html_without_id)
    assert bio_id is None


@pytest.fixture
def instabio_embedded_html():
    """Fixture for instabio.cc page with embedded content (e.g., etoilegriotte)."""
    fixture_path = Path(__file__).parent / "fixtures" / "instabio_etoilegriotte.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.mark.asyncio
async def test_instabio_embedded_content(instabio_embedded_html):
    """Test instabio.cc extractor with embedded content (e.g., https://instabio.cc/etoilegriotte)."""
    extractor = InstaBioExtractor()

    # Should extract links directly from embedded content without fetching JSON
    links = await extractor.extract_links(
        instabio_embedded_html, "https://instabio.cc/etoilegriotte"
    )

    # Should find links from embedded content
    assert len(links) > 0, "Should extract links from embedded content"

    # Get all URLs for easier testing
    extracted_urls = [str(link.url) for link in links]

    # Check for some expected URLs from etoilegriotte page
    expected_patterns = [
        "etoilegriotte.booth.pm",  # Web Store
        "suzuri.jp/etoilegriotte",  # SUZURI SHOP
        "www.etoilegriotte.com",  # Website
        "instagram.com/etoile_griotte",  # Instagram
        "twitter.com/etoile_griotte",  # Twitter
    ]

    for pattern in expected_patterns:
        found = any(pattern in url for url in extracted_urls)
        assert found, f"Should find URL containing: {pattern}"

    # Verify no instabio.cc URLs included
    for url in extracted_urls:
        assert "instabio.cc" not in url, f"instabio.cc URL should be filtered: {url}"
        assert "linkcdn.cc" not in url, f"CDN URL should be filtered: {url}"

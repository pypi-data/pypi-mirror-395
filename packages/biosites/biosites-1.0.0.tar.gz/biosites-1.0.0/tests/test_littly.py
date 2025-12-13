from pathlib import Path
import pytest

from biosites.extractors.littly import LittlyExtractor


@pytest.fixture
def littly_html():
    fixture_path = Path(__file__).parent / "fixtures" / "littly_yellowballoon.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.mark.asyncio
async def test_littly_extractor_can_handle():
    extractor = LittlyExtractor()

    # Should handle litt.ly URLs
    assert extractor.can_handle("https://litt.ly/yellowballoon")
    assert extractor.can_handle("http://litt.ly/someuser")
    assert extractor.can_handle("https://www.litt.ly/profile")

    # Should not handle other URLs
    assert not extractor.can_handle("https://linktree.com/user")
    assert not extractor.can_handle("https://example.com")


@pytest.mark.asyncio
async def test_littly_extract_links(littly_html):
    extractor = LittlyExtractor()
    links = await extractor.extract_links(littly_html, "https://litt.ly/yellowballoon")

    # Should extract multiple links
    assert len(links) > 0

    # Check first few expected links
    expected_urls = [
        "https://pkg.ybtour.co.kr/promotion/promotionDetail.yb?mstNo=20000031204",
        "https://pkg.ybtour.co.kr/promotion/promotionDetail.yb?mstNo=20000030788",
        "https://pkg.ybtour.co.kr/promotion/promotionDetail.yb?mstNo=20000029675",
    ]

    extracted_urls = [str(link.url).split("&")[0] for link in links]

    for expected_url in expected_urls:
        assert expected_url in extracted_urls, f"Expected {expected_url} not found"

    # Check that links have titles
    for link in links[:3]:
        assert link.title is not None
        assert len(link.title) > 0

    # Check metadata
    for link in links:
        assert "type" in link.metadata
        assert "key" in link.metadata


@pytest.mark.asyncio
async def test_littly_extract_links_with_invalid_html():
    extractor = LittlyExtractor()

    # Test with HTML without script#data
    html_no_script = "<html><body><h1>No script here</h1></body></html>"
    links = await extractor.extract_links(html_no_script, "https://litt.ly/test")
    assert len(links) == 0

    # Test with invalid base64
    html_invalid_base64 = (
        '<html><body><script id="data">invalid base64!</script></body></html>'
    )
    links = await extractor.extract_links(html_invalid_base64, "https://litt.ly/test")
    assert len(links) == 0

    # Test with valid base64 but invalid JSON
    html_invalid_json = (
        '<html><body><script id="data">bm90IGpzb24=</script></body></html>'
    )
    links = await extractor.extract_links(html_invalid_json, "https://litt.ly/test")
    assert len(links) == 0


@pytest.mark.asyncio
async def test_littly_full_process(littly_html):
    from biosites import LinkExtractor

    # Mock the fetch_html method to use our fixture
    class MockLittlyExtractor(LittlyExtractor):
        async def fetch_html(self, url: str, proxy=None) -> str:
            return littly_html

    extractor = LinkExtractor()
    # Replace the registered extractor with our mock
    extractor._extractors = [MockLittlyExtractor()]

    result = await extractor.extract("https://litt.ly/yellowballoon")

    assert result.source_url
    assert len(result.links) > 0
    assert result.service_type in ["Littly", "MockLittly"]  # Allow both for test
    assert len(result.errors) == 0

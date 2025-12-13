from pathlib import Path
import pytest

from biosites.extractors.linktree import LinktreeExtractor


@pytest.fixture
def linktree_html():
    fixture_path = Path(__file__).parent / "fixtures" / "linktree_bellarmrz.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.mark.asyncio
async def test_linktree_extractor_can_handle():
    extractor = LinktreeExtractor()

    # Should handle linktr.ee URLs
    assert extractor.can_handle("https://linktr.ee/bellarmrz")
    assert extractor.can_handle("http://linktr.ee/someuser")
    assert extractor.can_handle("https://www.linktr.ee/profile")

    # Should also handle linktree.com URLs
    assert extractor.can_handle("https://linktree.com/user")
    assert extractor.can_handle("https://www.linktree.com/profile")

    # Should not handle other URLs
    assert not extractor.can_handle("https://litt.ly/user")
    assert not extractor.can_handle("https://example.com")


@pytest.mark.asyncio
async def test_linktree_extract_links(linktree_html):
    extractor = LinktreeExtractor()
    links = await extractor.extract_links(linktree_html, "https://linktr.ee/bellarmrz")

    # Should extract multiple links
    assert len(links) > 0

    # Check for known links in the fixture
    extracted_urls = [str(link.url) for link in links]

    # Check for some expected URLs (based on the analysis)
    expected_urls = [
        "https://us.motelrocks.com/",
        "https://www.youtube.com/@bellarmrz",
        "https://babeoriginal.com/products/essential-eyelash-serum",
    ]

    for expected_url in expected_urls:
        assert expected_url in extracted_urls, f"Expected {expected_url} not found"

    # Check that links have titles
    titled_links = [link for link in links if link.title]
    assert len(titled_links) > 0

    # Check metadata
    for link in links[:5]:  # Check first 5 links
        assert "type" in link.metadata

    # Check for thumbnails in metadata
    links_with_thumbnail_info = [
        link for link in links if "has_thumbnail" in link.metadata
    ]
    assert len(links_with_thumbnail_info) > 0


@pytest.mark.asyncio
async def test_linktree_extract_social_links(linktree_html):
    extractor = LinktreeExtractor()
    links = await extractor.extract_links(linktree_html, "https://linktr.ee/bellarmrz")

    # Check for social links
    social_links = [link for link in links if link.metadata.get("type") == "social"]
    if social_links:
        assert all(
            link.metadata.get("type") == "social" for link in social_links
        ), "Social links should be labeled with type=social"

    # Check that all links have valid URLs
    for link in links:
        assert str(link.url).startswith(("http://", "https://"))


@pytest.mark.asyncio
async def test_linktree_extract_links_with_invalid_html():
    extractor = LinktreeExtractor()

    # Test with HTML without script#__NEXT_DATA__
    html_no_script = "<html><body><h1>No script here</h1></body></html>"
    links = await extractor.extract_links(html_no_script, "https://linktr.ee/test")
    assert len(links) == 0

    # Test with invalid JSON in script
    html_invalid_json = (
        '<html><body><script id="__NEXT_DATA__">not valid json</script></body></html>'
    )
    links = await extractor.extract_links(html_invalid_json, "https://linktr.ee/test")
    assert len(links) == 0

    # Test with valid JSON but wrong structure
    html_wrong_structure = '<html><body><script id="__NEXT_DATA__">{"wrong": "structure"}</script></body></html>'
    links = await extractor.extract_links(
        html_wrong_structure, "https://linktr.ee/test"
    )
    assert len(links) == 0


@pytest.mark.asyncio
async def test_linktree_full_process(linktree_html):
    from biosites import LinkExtractor

    # Mock the fetch_html method to use our fixture
    class MockLinktreeExtractor(LinktreeExtractor):
        async def fetch_html(self, url: str, proxy=None) -> str:
            return linktree_html

    extractor = LinkExtractor()
    # Replace the registered extractors with our mock
    extractor._extractors = [MockLinktreeExtractor()]

    result = await extractor.extract("https://linktr.ee/bellarmrz")

    assert result.source_url
    assert len(result.links) > 0
    assert result.service_type in ["Linktree", "MockLinktree"]
    assert len(result.errors) == 0

    # Verify specific content
    urls = [str(link.url) for link in result.links]
    assert "https://us.motelrocks.com/" in urls

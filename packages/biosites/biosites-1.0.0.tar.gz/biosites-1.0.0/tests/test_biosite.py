import pytest
from pathlib import Path

from biosites.extractors.biosite import BioSiteExtractor


@pytest.fixture
def biosite_html():
    fixture_path = Path(__file__).parent / "fixtures" / "biosite_aidenarata.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.mark.asyncio
async def test_biosite_extract_links(biosite_html):
    extractor = BioSiteExtractor()
    links = await extractor.extract_links(biosite_html, "https://bio.site/aidenarata")

    # Test link count
    assert len(links) > 0

    # Get all URLs for easier testing
    extracted_urls = [str(link.url) for link in links]

    # Test for expected URLs (from the fixture)
    # Note: mailto links are not extracted as they're not HTTP URLs
    expected_urls = [
        "https://www.instagram.com/aidenarata",
        "https://www.tiktok.com/@aidenarata",
        "https://x.com/aidenarata",
        "https://www.hachettebookgroup.com/articles/yhanm_promo/",
        "https://aidenarata.com/",
        "https://aidenarata.substack.com/",
        "https://aidenarata.merchtable.com/",
    ]

    for expected_url in expected_urls:
        assert expected_url in extracted_urls, f"Missing expected URL: {expected_url}"

    # Verify no bio.site URLs included
    for url in extracted_urls:
        assert "bio.site" not in url, f"bio.site URL should be filtered: {url}"
        assert "unfold-dev.com" not in url, f"CDN URL should be filtered: {url}"
        assert "media.bio.site" not in url, (
            f"media.bio.site URL should be filtered: {url}"
        )

    # Test that titles are extracted
    link_dict = {str(link.url): link for link in links}

    # Check some titles (URLs may have trailing slashes)
    assert link_dict["https://aidenarata.com/"].title == "website"
    assert link_dict["https://aidenarata.substack.com/"].title == "newsletter"
    assert link_dict["https://aidenarata.merchtable.com/"].title == "shop"
    instagram_link = link_dict["https://www.instagram.com/aidenarata"]
    assert instagram_link.title is not None
    assert "instagram" in instagram_link.title.lower()


@pytest.mark.asyncio
async def test_biosite_can_handle():
    extractor = BioSiteExtractor()

    # Should handle bio.site URLs
    assert extractor.can_handle("https://bio.site/username")
    assert extractor.can_handle("http://bio.site/someuser")
    assert extractor.can_handle("https://www.bio.site/profile")

    # Should not handle other URLs
    assert not extractor.can_handle("https://linktree.com/user")
    assert not extractor.can_handle("https://example.com")

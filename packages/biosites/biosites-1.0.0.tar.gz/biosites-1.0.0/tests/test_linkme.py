"""Test LinkMe extractor."""

from pathlib import Path

import pytest

from biosites.extractors.linkme import LinkMeExtractor


@pytest.fixture
def linkme_html():
    """Load LinkMe test fixture."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    with open(fixtures_dir / "linkme_hadilhoney.html", encoding="utf-8") as f:
        return f.read()


@pytest.mark.asyncio
async def test_linkme_extractor(linkme_html):
    """Test LinkMe link extraction."""
    extractor = LinkMeExtractor()

    # Test can_handle
    assert extractor.can_handle("https://link.me/hadilhoney")
    assert extractor.can_handle("http://link.me/user")
    assert not extractor.can_handle("https://linktree.com/user")

    # Extract links
    links = await extractor.extract_links(linkme_html, "https://link.me/hadilhoney")

    # Should have extracted links
    assert len(links) == 4

    # Check first link (Instagram)
    first_link = links[0]
    assert first_link.title == "Instagram"
    assert str(first_link.url) == "https://www.instagram.com/Hadil.Honey"
    assert first_link.metadata["category"] == "Instagram"
    assert first_link.metadata["face_value"] == "Hadil.Honey"

    # Check second link (Snapchat)
    second_link = links[1]
    assert second_link.title == "Snapchat"
    assert str(second_link.url) == "https://www.snapchat.com/add/Shawddiecold"
    assert second_link.metadata["category"] == "Snapchat"

    # Check third link (Twitter)
    third_link = links[2]
    assert third_link.title == "Twitter"
    assert str(third_link.url) == "https://www.twitter.com/HadilHoneyy"

    # Check fourth link (TikTok)
    fourth_link = links[3]
    assert fourth_link.title == "Tiktok"
    assert str(fourth_link.url) == "https://www.tiktok.com/@Hadil.honeyy"


@pytest.mark.asyncio
async def test_linkme_empty_profile():
    """Test LinkMe extractor with empty or malformed HTML."""
    extractor = LinkMeExtractor()

    # Test with empty HTML
    links = await extractor.extract_links("", "https://link.me/test")
    assert links == []

    # Test with HTML without NEXT_DATA
    html_no_data = "<html><body>No data here</body></html>"
    links = await extractor.extract_links(html_no_data, "https://link.me/test")
    assert links == []

    # Test with malformed JSON
    html_bad_json = '<script id="__NEXT_DATA__">{bad json}</script>'
    links = await extractor.extract_links(html_bad_json, "https://link.me/test")
    assert links == []

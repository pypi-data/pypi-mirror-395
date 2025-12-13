import pytest
from pathlib import Path
from biosites.extractors.litlink import LitLinkExtractor


@pytest.fixture
def extractor():
    """Shared LitLinkExtractor instance"""
    return LitLinkExtractor()


@pytest.fixture
def mukuri_html():
    """Load mukuri fixture"""
    fixture_path = Path(__file__).parent / "fixtures" / "litlink_mukuri.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def niwaniniwaniwatori_html():
    """Load niwaniniwaniwatori fixture"""
    fixture_path = (
        Path(__file__).parent / "fixtures" / "litlink_niwaniniwaniwatori.html"
    )
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


class TestLitLinkExtractor:
    """Test suite for LitLinkExtractor"""

    def test_can_handle(self, extractor):
        """Test URL detection"""
        assert extractor.can_handle("https://lit.link/en/mukuri")
        assert extractor.can_handle("https://lit.link/mukuri")
        assert not extractor.can_handle("https://linktr.ee/example")

    def test_url_exclusion(self, extractor):
        """Test that lit.link URLs are properly excluded"""
        # URLs that should be excluded
        excluded_urls = [
            "https://lit.link/en/mukuri",
            "https://storage.lit.link/image.jpg",
            "https://cdn.lit.link/assets/logo.png",
            "https://subdomain.lit.link/page",
        ]

        for url in excluded_urls:
            assert extractor._should_exclude_url(url), f"URL should be excluded: {url}"

        # URLs that should NOT be excluded
        allowed_urls = [
            "https://www.instagram.com/user",
            "https://twitter.com/user",
            "https://www.tiktok.com/@user",
            "https://mukuri.thebase.in/",
        ]

        for url in allowed_urls:
            assert not extractor._should_exclude_url(url), (
                f"URL should not be excluded: {url}"
            )

    @pytest.mark.asyncio
    async def test_extract_mukuri(self, extractor, mukuri_html):
        """Test extraction from lit.link/en/mukuri page"""
        links = await extractor.extract_links(mukuri_html, "https://lit.link/en/mukuri")

        # Check that we extracted links
        assert len(links) > 0

        # Expected URLs based on actual fixture content
        expected_urls = [
            "https://www.instagram.com/mukuri/",
            "https://twitter.com/mukuri",
            "https://mukuri.thebase.in/",
            "https://suzuri.jp/powachang",
            "https://store.line.me/stickershop/product/1411702/ja",
        ]

        # Check that all expected URLs are present
        all_urls = [str(link.url) for link in links]
        for expected_url in expected_urls:
            # Handle trailing slash variations
            found = any(url.rstrip("/") == expected_url.rstrip("/") for url in all_urls)
            assert found, f"Expected URL {expected_url} not found in links: {all_urls}"

        # Check that links have the correct source metadata
        for link in links:
            assert link.url
            assert link.metadata
            assert link.metadata.get("source") == "html_link"

        # Verify we got the right number of unique links (should be 7)
        unique_urls = set(str(link.url) for link in links)
        assert len(unique_urls) == 7, (
            f"Expected 7 unique URLs, got {len(unique_urls)}: {unique_urls}"
        )

        # Verify NO lit.link URLs are included
        lit_link_urls = [url for url in all_urls if "lit.link" in url]
        assert len(lit_link_urls) == 0, (
            f"Found lit.link URLs that should be excluded: {lit_link_urls}"
        )

    @pytest.mark.asyncio
    async def test_extract_niwaniniwaniwatori(self, extractor, niwaniniwaniwatori_html):
        """Test extraction from lit.link/en/niwaniniwaniwatori page"""
        links = await extractor.extract_links(
            niwaniniwaniwatori_html, "https://lit.link/en/niwaniniwaniwatori"
        )

        # Should extract approximately 27 links
        assert len(links) >= 25, f"Expected at least 25 links, got {len(links)}"
        assert len(links) <= 30, f"Expected at most 30 links, got {len(links)}"

        # Verify NO lit.link URLs are included
        lit_link_urls = [str(link.url) for link in links if "lit.link" in str(link.url)]
        assert len(lit_link_urls) == 0, (
            f"Found lit.link URLs that should be excluded: {lit_link_urls}"
        )

        # Check for known social media links
        urls = [str(link.url) for link in links]

        # These social links should be present
        assert "https://www.instagram.com/niwatori__diet/" in urls
        assert "https://twitter.com/niwatori__tw" in urls
        assert "https://www.tiktok.com/@niwatori__tk" in urls

        # Check that some links have titles (product descriptions)
        titled_links = [link for link in links if link.title and len(link.title) > 10]
        assert len(titled_links) > 10, (
            "Should have at least 10 links with substantial titles"
        )

        # Verify metadata is set for HTML links
        html_links = [
            link
            for link in links
            if link.metadata and link.metadata.get("source") == "html_link"
        ]
        assert len(html_links) > 20, (
            f"Expected most links to be from HTML, got {len(html_links)}"
        )


@pytest.mark.parametrize(
    "test_case",
    [
        {
            "fixture": "litlink_mukuri.html",
            "url": "https://lit.link/en/mukuri",
            "min_links": 7,
            "max_links": 7,
            "expected_urls": [
                "https://www.instagram.com/mukuri/",
                "https://twitter.com/mukuri",
                "https://mukuri.thebase.in/",
            ],
        },
        {
            "fixture": "litlink_niwaniniwaniwatori.html",
            "url": "https://lit.link/en/niwaniniwaniwatori",
            "min_links": 25,
            "max_links": 30,
            "expected_urls": [
                "https://www.instagram.com/niwatori__diet/",
                "https://twitter.com/niwatori__tw",
                "https://www.tiktok.com/@niwatori__tk",
            ],
        },
    ],
)
@pytest.mark.asyncio
async def test_litlink_extraction_parametrized(test_case):
    """Parametrized test for different lit.link pages"""
    extractor = LitLinkExtractor()

    # Load fixture
    fixture_path = Path(__file__).parent / "fixtures" / test_case["fixture"]
    with open(fixture_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract links
    links = await extractor.extract_links(html, test_case["url"])

    # Check link count
    assert len(links) >= test_case["min_links"], (
        f"Expected at least {test_case['min_links']} links, got {len(links)}"
    )
    assert len(links) <= test_case["max_links"], (
        f"Expected at most {test_case['max_links']} links, got {len(links)}"
    )

    # Verify NO lit.link URLs are included
    all_urls = [str(link.url) for link in links]
    lit_link_urls = [url for url in all_urls if "lit.link" in url]
    assert len(lit_link_urls) == 0, (
        f"Found lit.link URLs that should be excluded: {lit_link_urls}"
    )

    # Check expected URLs are present
    for expected_url in test_case["expected_urls"]:
        found = any(url.rstrip("/") == expected_url.rstrip("/") for url in all_urls)
        assert found, f"Expected URL {expected_url} not found"

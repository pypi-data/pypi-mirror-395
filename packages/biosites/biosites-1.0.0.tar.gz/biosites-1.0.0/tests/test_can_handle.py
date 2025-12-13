import pytest

from biosites.extractor import LinkExtractor


@pytest.mark.asyncio
async def test_can_handle_specific_services():
    """Test that can_handle correctly identifies specific services."""
    extractor = LinkExtractor()

    # Test known services
    test_cases = [
        ("https://linktree.com/username", (True, "Linktree")),
        ("https://linktr.ee/username", (True, "Linktree")),
        ("https://litt.ly/username", (True, "Littly")),
        ("https://instabio.cc/username", (True, "InstaBio")),
        ("https://linkbio.co/username", (True, "LinkBioCo")),
        ("https://bio.site/username", (True, "BioSite")),
        ("https://lit.link/username", (True, "LitLink")),
        ("https://link.inpock.co.kr/username", (True, "InPock")),
        ("https://inpk.link/username", (True, "InPock")),
    ]

    for url, expected in test_cases:
        result = extractor.can_handle(url)
        assert result == expected, f"URL {url} should return {expected}, got {result}"


@pytest.mark.asyncio
async def test_can_handle_generic():
    """Test that can_handle returns Generic for unknown services."""
    extractor = LinkExtractor()

    # Test unknown services
    unknown_urls = [
        "https://example.com/page",
        "https://google.com",
        "https://github.com/user",
        "https://randomsite.org/profile",
    ]

    for url in unknown_urls:
        can_handle, service = extractor.can_handle(url)
        assert can_handle is False, f"Unknown URL {url} should return False"
        assert service == "Generic", f"Unknown URL {url} should use Generic extractor"


@pytest.mark.asyncio
async def test_can_handle_with_custom_extractor():
    """Test that can_handle works with custom registered extractors."""
    from biosites.base import BaseLinkExtractor
    from biosites.models import ExtractedLink

    class CustomExtractor(BaseLinkExtractor):
        def can_handle(self, url: str) -> bool:
            return "custom.example" in url

        async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
            return []

    extractor = LinkExtractor()

    # Register custom extractor
    custom = CustomExtractor()
    extractor.register_extractor(custom)

    # Test custom extractor
    can_handle, service = extractor.can_handle("https://custom.example/page")
    assert can_handle is True
    assert service == "Custom"

    # Test that it doesn't affect other URLs
    can_handle, service = extractor.can_handle("https://other.com/page")
    assert can_handle is False
    assert service == "Generic"


@pytest.mark.asyncio
async def test_can_handle_priority():
    """Test that first matching extractor takes priority."""
    extractor = LinkExtractor()

    # linktree.com should be handled by Linktree extractor
    can_handle, service = extractor.can_handle("https://linktree.com/user")
    assert service == "Linktree"

    # Even with query parameters or paths
    can_handle, service = extractor.can_handle("https://linktree.com/user?param=value")
    assert service == "Linktree"

    can_handle, service = extractor.can_handle("https://linktr.ee/user/links")
    assert service == "Linktree"

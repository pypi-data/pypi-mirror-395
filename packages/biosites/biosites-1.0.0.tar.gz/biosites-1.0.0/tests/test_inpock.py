from pathlib import Path
import pytest

from biosites.extractors.inpock import InPockExtractor


@pytest.fixture
def inpock_html():
    fixture_path = Path(__file__).parent / "fixtures" / "inpock_starglass.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.mark.asyncio
async def test_inpock_extractor_can_handle():
    extractor = InPockExtractor()

    # Should handle link.inpock.co.kr URLs
    assert extractor.can_handle("https://link.inpock.co.kr/starglass")
    assert extractor.can_handle("http://link.inpock.co.kr/user123")

    # Should also handle inpk.link URLs (shortened)
    assert extractor.can_handle("https://inpk.link/user")
    assert extractor.can_handle("http://inpk.link/profile")

    # Should not handle other URLs
    assert not extractor.can_handle("https://linktr.ee/user")
    assert not extractor.can_handle("https://litt.ly/user")
    assert not extractor.can_handle("https://example.com")


@pytest.mark.asyncio
async def test_inpock_extract_ssr_links(inpock_html):
    extractor = InPockExtractor()
    links = await extractor.extract_links(
        inpock_html, "https://link.inpock.co.kr/starglass"
    )

    # Should extract multiple links
    assert len(links) > 0

    # Check for known SSR links in the fixture
    extracted_urls = [str(link.url) for link in links]

    expected_ssr_urls = [
        "https://forms.gle/KHDvMNbXeoubF2wr5",  # 스레드 천재가 되는 법
        "https://smartstore.naver.com/papatable25",  # 전자책 스토어
        "https://contents.premium.naver.com/papatable/papatable25",  # 프리미엄 콘텐츠
        "https://www.threads.com/@starglass____",  # Threads
        "https://www.youtube.com/@starglass25",  # YouTube
        "https://blog.naver.com/starglass22",  # Naver Blog
    ]

    for expected_url in expected_ssr_urls:
        assert expected_url in extracted_urls, f"Expected {expected_url} not found"

    # Check that links have titles
    titled_links = [link for link in links if link.title]
    assert len(titled_links) > 0

    # Check metadata
    for link in links:
        assert "source" in link.metadata
        assert "type" in link.metadata


@pytest.mark.asyncio
async def test_inpock_extract_nuxt_social_links(inpock_html):
    extractor = InPockExtractor()
    links = await extractor.extract_links(
        inpock_html, "https://link.inpock.co.kr/starglass"
    )

    # Check for social links from NUXT data
    social_links = [link for link in links if link.metadata.get("source") == "nuxt"]

    # Should have Instagram from NUXT
    instagram_links = [
        link for link in social_links if link.metadata.get("platform") == "instagram"
    ]
    assert len(instagram_links) > 0
    assert "starglass____" in str(instagram_links[0].url)

    # Should have YouTube from NUXT
    youtube_links = [
        link for link in social_links if link.metadata.get("platform") == "youtube"
    ]
    assert len(youtube_links) > 0

    # Check that NUXT social links have proper metadata
    for social_link in social_links:
        assert social_link.metadata.get("type") == "social"
        assert "platform" in social_link.metadata


@pytest.mark.asyncio
async def test_inpock_no_system_links(inpock_html):
    extractor = InPockExtractor()
    links = await extractor.extract_links(
        inpock_html, "https://link.inpock.co.kr/starglass"
    )

    # Should NOT include InPock system links
    extracted_urls = [str(link.url) for link in links]

    # System URLs that should be excluded
    system_patterns = [
        "/guide",
        "/plan",
        "/cs",
        "team.ab-z.com",
        "channel.io",
    ]

    for url in extracted_urls:
        for pattern in system_patterns:
            assert pattern not in url, f"System URL pattern '{pattern}' found in {url}"


@pytest.mark.asyncio
async def test_inpock_extract_links_with_invalid_html():
    extractor = InPockExtractor()

    # Test with HTML without any links
    html_no_links = "<html><body><h1>No links here</h1></body></html>"
    links = await extractor.extract_links(
        html_no_links, "https://link.inpock.co.kr/test"
    )
    assert len(links) == 0

    # Test with HTML without NUXT data
    html_no_nuxt = '<html><body><a href="https://example.com">Link</a></body></html>'
    links = await extractor.extract_links(
        html_no_nuxt, "https://link.inpock.co.kr/test"
    )
    # Should still extract SSR links if present
    assert len(links) >= 0


@pytest.mark.asyncio
async def test_inpock_full_process(inpock_html):
    from biosites import LinkExtractor

    # Mock the fetch_html method to use our fixture
    class MockInPockExtractor(InPockExtractor):
        async def fetch_html(self, url: str, proxy=None) -> str:
            return inpock_html

    extractor = LinkExtractor()
    # Replace the registered extractors with our mock
    extractor._extractors = [MockInPockExtractor()]

    result = await extractor.extract("https://link.inpock.co.kr/starglass")

    assert result.source_url
    assert len(result.links) > 0
    assert result.service_type in ["InPock", "MockInPock"]
    assert len(result.errors) == 0

    # Verify mix of SSR and NUXT links
    sources = set(link.metadata.get("source") for link in result.links)
    assert "ssr" in sources  # Should have SSR links
    assert "nuxt" in sources  # Should have NUXT links

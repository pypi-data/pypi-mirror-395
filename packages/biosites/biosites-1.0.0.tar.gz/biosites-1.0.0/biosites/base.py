from abc import ABC, abstractmethod
from urllib.parse import urlparse
from pydantic import HttpUrl

from selectolax.parser import HTMLParser
import aiohttp

from .models import ExtractedLink, ExtractionResult

# Default user agent for all requests
DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"


class BaseLinkExtractor(ABC):
    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        proxy: str | None = None,
        user_agent: str | None = None,
    ):
        self.session = session
        self._owns_session = session is None
        self.proxy = proxy
        self.user_agent = user_agent or DEFAULT_USER_AGENT

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        pass

    @abstractmethod
    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        pass

    async def fetch_html(self, url: str, proxy: str | None = None) -> str:
        # Use provided proxy or fall back to instance proxy
        proxy_url = proxy or self.proxy

        if self._owns_session:
            async with aiohttp.ClientSession() as session:
                return await self._fetch_with_session(session, url, proxy_url)
        else:
            assert self.session is not None
            return await self._fetch_with_session(self.session, url, proxy_url)

    async def _fetch_with_session(
        self, session: aiohttp.ClientSession, url: str, proxy: str | None = None
    ) -> str:
        headers = {"User-Agent": self.user_agent}
        async with session.get(url, proxy=proxy, headers=headers) as response:
            response.raise_for_status()
            return await response.text()

    async def process(self, url: str, proxy: str | None = None) -> ExtractionResult:
        try:
            html = await self.fetch_html(url, proxy)
            links = await self.extract_links(html, url)

            return ExtractionResult(
                source_url=HttpUrl(url),
                service_type=self.__class__.__name__.replace("Extractor", ""),
                links=links,
                raw_html=html,
            )
        except Exception as e:
            return ExtractionResult(
                source_url=HttpUrl(url),
                service_type=self.__class__.__name__.replace("Extractor", ""),
                links=[],
                errors=[str(e)],
            )


class GenericLinkExtractor(BaseLinkExtractor):
    def can_handle(self, url: str) -> bool:
        return True

    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        parser = HTMLParser(html)
        links = []

        for node in parser.css("a[href]"):
            href = node.attributes.get("href", "")
            if not href:
                continue

            title = node.text(strip=True) or None

            try:
                if href.startswith("http"):
                    link_url = href
                elif href.startswith("//"):
                    link_url = f"https:{href}"
                elif href.startswith("/"):
                    parsed = urlparse(url)
                    link_url = f"{parsed.scheme}://{parsed.netloc}{href}"
                else:
                    continue

                links.append(
                    ExtractedLink(
                        url=HttpUrl(link_url),
                        title=title,
                    )
                )
            except Exception:
                continue

        return links

import aiohttp

from .base import BaseLinkExtractor, GenericLinkExtractor
from .extractors import (
    BioSiteExtractor,
    InPockExtractor,
    InstaBioExtractor,
    LinkBioCoExtractor,
    LinkMeExtractor,
    LinktreeExtractor,
    LitLinkExtractor,
    LittlyExtractor,
)
from .models import ExtractionResult
from .redirect_handler import RedirectHandler


class LinkExtractor:
    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        proxy: str | None = None,
        user_agent: str | None = None,
        follow_redirects: bool = True,
    ):
        self.session = session
        self.proxy = proxy
        self.user_agent = user_agent
        self.follow_redirects = follow_redirects
        self._extractors: list[BaseLinkExtractor] = []
        self._generic_extractor = GenericLinkExtractor(session, proxy, user_agent)
        self._redirect_handler = RedirectHandler(
            session, user_agent, follow_redirects=follow_redirects
        )

        self._register_extractors()

    def _register_extractors(self) -> None:
        # Register specific extractors
        self.register_extractor(
            BioSiteExtractor(self.session, self.proxy, self.user_agent)
        )
        self.register_extractor(
            InPockExtractor(self.session, self.proxy, self.user_agent)
        )
        self.register_extractor(
            InstaBioExtractor(self.session, self.proxy, self.user_agent)
        )
        self.register_extractor(
            LinkBioCoExtractor(self.session, self.proxy, self.user_agent)
        )
        self.register_extractor(
            LinkMeExtractor(self.session, self.proxy, self.user_agent)
        )
        self.register_extractor(
            LinktreeExtractor(self.session, self.proxy, self.user_agent)
        )
        self.register_extractor(
            LitLinkExtractor(self.session, self.proxy, self.user_agent)
        )
        self.register_extractor(
            LittlyExtractor(self.session, self.proxy, self.user_agent)
        )

    def register_extractor(self, extractor: BaseLinkExtractor) -> None:
        self._extractors.append(extractor)

    def _get_extractor_for_url(self, url: str) -> BaseLinkExtractor:
        for extractor in self._extractors:
            if extractor.can_handle(url):
                return extractor
        return self._generic_extractor

    def can_handle(self, url: str) -> tuple[bool, str]:
        """Check if URL can be handled and return which service will handle it.

        Returns:
            tuple: (can_handle, service_name)
                - can_handle: True if a specific extractor can handle it, False for generic
                - service_name: Name of the service that will handle the URL
        """
        for extractor in self._extractors:
            if extractor.can_handle(url):
                service_name = extractor.__class__.__name__.replace("Extractor", "")
                return (True, service_name)

        # Generic extractor always handles URLs
        return (False, "Generic")

    def get_supported_services(self) -> list[str]:
        """Get list of all supported services.

        Returns:
            list: Names of all supported services (excluding Generic)
        """
        services = []
        for extractor in self._extractors:
            service_name = extractor.__class__.__name__.replace("Extractor", "")
            services.append(service_name)
        return services

    async def extract(self, url: str, proxy: str | None = None) -> ExtractionResult:
        # Use provided proxy or fall back to instance proxy
        proxy_url = proxy or self.proxy

        # Resolve redirects if needed
        final_url = url
        redirect_chain: list[str] = []
        if self.follow_redirects and self._redirect_handler.is_shortener(url):
            final_url, redirect_chain = await self._redirect_handler.resolve_url(
                url, proxy_url
            )

        # Get appropriate extractor for the final URL
        extractor = self._get_extractor_for_url(final_url)

        # Process the final URL
        result = await extractor.process(final_url, proxy_url)

        # Add redirect information to result if there were redirects
        if redirect_chain:
            if not result.metadata:
                result.metadata = {}
            result.metadata["original_url"] = url
            result.metadata["redirect_chain"] = redirect_chain

        return result

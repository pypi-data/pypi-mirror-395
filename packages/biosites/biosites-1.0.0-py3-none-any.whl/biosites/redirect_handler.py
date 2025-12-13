"""
Redirect handler for following URL redirections and shorteners.
"""

import re
from urllib.parse import urlparse

import aiohttp
from selectolax.parser import HTMLParser

from .base import DEFAULT_USER_AGENT


class RedirectHandler:
    """Handles URL redirections and shorteners like bit.ly, tinyurl, etc."""

    # Known URL shorteners that commonly use redirects
    SHORTENER_DOMAINS = {
        "bit.ly",
        "bitly.com",
        "tinyurl.com",
        "tiny.cc",
        "ow.ly",
        "is.gd",
        "goo.gl",
        "short.link",
        "shorte.st",
        "t.co",
        "t.me",
        "rebrand.ly",
        "rb.gy",
        "shorturl.at",
        "v.gd",
        "cutt.ly",
        "clck.ru",
        "bl.ink",
        "buff.ly",
    }

    # Known bio link services - stop redirects when we reach these
    BIOLINK_DOMAINS = {
        "linktr.ee",
        "linktree.com",
        "litt.ly",
        "litlink.com",
        "lit.link",
        "link.inpock.co.kr",
        "instabio.cc",
        "linkbio.co",
        "bio.site",
        "link.me",
    }

    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        user_agent: str | None = None,
        max_redirects: int = 10,
        follow_redirects: bool = True,
    ):
        """Initialize redirect handler.

        Args:
            session: Optional aiohttp session to reuse
            user_agent: User agent for requests
            max_redirects: Maximum number of redirects to follow
            follow_redirects: Whether to follow redirects automatically
        """
        self.session = session
        self._owns_session = session is None
        self.user_agent = user_agent or DEFAULT_USER_AGENT
        self.max_redirects = max_redirects
        self.follow_redirects = follow_redirects

    def is_shortener(self, url: str) -> bool:
        """Check if URL is from a known shortener service."""
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            # Check if domain matches any known shortener
            for domain in self.SHORTENER_DOMAINS:
                if hostname == domain or hostname.endswith(f".{domain}"):
                    return True
        except Exception:
            pass
        return False

    def is_biolink_service(self, url: str) -> bool:
        """Check if URL is from a known bio link service."""
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            # Check if domain matches any known bio link service
            for domain in self.BIOLINK_DOMAINS:
                if hostname == domain or hostname.endswith(f".{domain}"):
                    return True
        except Exception:
            pass
        return False

    async def resolve_url(
        self, url: str, proxy: str | None = None
    ) -> tuple[str, list[str]]:
        """Resolve a URL by following redirects.

        Args:
            url: URL to resolve
            proxy: Optional proxy URL

        Returns:
            tuple: (final_url, redirect_chain)
                - final_url: The final resolved URL
                - redirect_chain: List of URLs in the redirect chain
        """
        if not self.follow_redirects:
            return (url, [])

        headers = {"User-Agent": self.user_agent}
        redirect_chain: list[str] = []
        current_url = url

        # Create session if needed
        if self._owns_session:
            async with aiohttp.ClientSession() as session:
                final_url = await self._follow_redirects(
                    session, current_url, headers, proxy, redirect_chain
                )
        else:
            assert self.session is not None
            final_url = await self._follow_redirects(
                self.session, current_url, headers, proxy, redirect_chain
            )

        return (final_url, redirect_chain)

    async def _follow_redirects(
        self,
        session: aiohttp.ClientSession,
        url: str,
        headers: dict[str, str],
        proxy: str | None,
        redirect_chain: list[str],
    ) -> str:
        """Follow redirects for a URL."""
        current_url = url
        redirects_followed = 0

        while redirects_followed < self.max_redirects:
            try:
                # Make request without auto-redirect to handle manually
                async with session.get(
                    current_url,
                    headers=headers,
                    proxy=proxy,
                    allow_redirects=False,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    # If not a redirect, check for meta refresh or JavaScript redirects
                    if response.status not in (301, 302, 303, 307, 308):
                        # Check for intermediate pages (like bit.ly warning pages)
                        if response.status == 200:
                            text = await response.text()
                            extracted_url = self._extract_redirect_from_html(text)
                            if extracted_url and extracted_url != current_url:
                                redirect_chain.append(current_url)
                                current_url = extracted_url
                                redirects_followed += 1
                                # Stop if we've reached a bio link service
                                if self.is_biolink_service(current_url):
                                    break
                                continue
                        # No more redirects
                        break

                    # Get redirect location
                    location = response.headers.get("Location")
                    if not location:
                        break

                    # Handle relative URLs
                    if not location.startswith(("http://", "https://")):
                        parsed = urlparse(current_url)
                        if location.startswith("/"):
                            location = f"{parsed.scheme}://{parsed.netloc}{location}"
                        else:
                            # Relative to current path
                            base_path = "/".join(current_url.split("/")[:-1])
                            location = f"{base_path}/{location}"

                    redirect_chain.append(current_url)
                    current_url = location
                    redirects_followed += 1

                    # Stop if we've reached a bio link service
                    if self.is_biolink_service(current_url):
                        break

            except (aiohttp.ClientError, TimeoutError):
                # If request fails, return what we have
                break

        # Ensure final URL is absolute
        if not current_url.startswith(("http://", "https://")):
            # Build absolute URL from the last valid URL in chain
            if redirect_chain:
                last_url = redirect_chain[-1]
                parsed = urlparse(last_url)
                if current_url.startswith("/"):
                    current_url = f"{parsed.scheme}://{parsed.netloc}{current_url}"
                else:
                    base_path = "/".join(last_url.split("/")[:-1])
                    current_url = f"{base_path}/{current_url}"

        return current_url

    def _extract_redirect_from_html(self, html: str) -> str | None:
        """Extract redirect URL from HTML (meta refresh or JavaScript)."""
        # Try meta refresh
        meta_match = re.search(
            r'<meta[^>]*http-equiv=["\']\s*refresh\s*["\'][^>]*content=["\'][^"\']*url=([^"\'\s>]+)',
            html,
            re.IGNORECASE,
        )
        if meta_match:
            return meta_match.group(1)

        # Try JavaScript redirects
        js_patterns = [
            r'window\.location\s*=\s*["\']([^"\']+)["\']',
            r'window\.location\.href\s*=\s*["\']([^"\']+)["\']',
            r'window\.location\.replace\s*\(\s*["\']([^"\']+)["\']',
            r'location\.href\s*=\s*["\']([^"\']+)["\']',
        ]

        for pattern in js_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(1)

        # Try to find links in intermediate pages (like bit.ly)
        parser = HTMLParser(html)

        # Look for the first external link
        for link in parser.css("a[href]"):
            href = link.attributes.get("href", "")
            if href and href.startswith(("http://", "https://")):
                # Avoid self-referential links
                parsed_href = urlparse(href)
                if parsed_href.hostname and not self.is_shortener(href):
                    return href

        return None

    async def resolve_multiple(
        self, urls: list[str], proxy: str | None = None
    ) -> dict[str, tuple[str, list[str]]]:
        """Resolve multiple URLs concurrently.

        Args:
            urls: List of URLs to resolve
            proxy: Optional proxy URL

        Returns:
            dict: Mapping of original URL to (resolved_url, redirect_chain)
        """
        import asyncio

        tasks = []
        for url in urls:
            tasks.append(self.resolve_url(url, proxy))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        resolved: dict[str, tuple[str, list[str]]] = {}
        for original_url, result in zip(urls, results):
            if isinstance(result, Exception):
                # If resolution failed, use original URL
                resolved[original_url] = (original_url, [])
            elif isinstance(result, tuple):
                resolved[original_url] = result
            else:
                # Fallback case - shouldn't happen but handle gracefully
                resolved[original_url] = (original_url, [])

        return resolved

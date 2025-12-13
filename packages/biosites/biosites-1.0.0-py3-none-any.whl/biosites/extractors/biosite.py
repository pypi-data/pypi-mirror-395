import json
import re
from typing import cast
from urllib.parse import urlparse

from pydantic import HttpUrl
from selectolax.parser import HTMLParser

from ..base import BaseLinkExtractor
from ..models import ExtractedLink


class BioSiteExtractor(BaseLinkExtractor):
    """Extractor for bio.site links."""

    def can_handle(self, url: str) -> bool:
        """Check if URL is from bio.site."""
        return "bio.site" in url

    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        """Extract links from bio.site page."""
        links: list[ExtractedLink] = []

        # Try to extract from window.initial_state JSON
        links.extend(self._extract_json_links(html))

        # Fallback to HTML extraction if JSON method fails
        if not links:
            links.extend(self._extract_html_links(html))

        # Filter out bio.site's own URLs
        links = self._filter_service_urls(links)

        # Deduplicate
        return self._deduplicate_links(links)

    def _extract_json_links(self, html: str) -> list[ExtractedLink]:
        """Extract links from window.initial_state JSON."""
        links: list[ExtractedLink] = []

        # Find window.initial_state JSON
        match = re.search(r"window\.initial_state\s*=\s*({.*?});", html, re.DOTALL)
        if not match:
            return links

        try:
            data = json.loads(match.group(1))

            # Extract social links
            for section in data.get("body", []):
                if section.get("type") == "section_social":
                    handles = section.get("section", {}).get("handles", [])
                    for handle in handles:
                        url = handle.get("url")
                        if url:
                            # Decode unicode escape sequences
                            url = url.encode().decode("unicode_escape")
                            title = (
                                f"{handle.get('type', '')} - {handle.get('value', '')}"
                            )
                            links.append(
                                ExtractedLink(
                                    url=url,
                                    title=title.strip(" - "),
                                )
                            )

                # Extract regular links
                elif section.get("type") == "section_links":
                    section_links = section.get("section", {}).get("links", [])
                    for link in section_links:
                        url = link.get("url")
                        if url:
                            # Decode unicode escape sequences
                            url = url.encode().decode("unicode_escape")
                            # Skip mailto links as they're not HTTP URLs
                            if url.startswith("mailto:"):
                                continue
                            links.append(
                                ExtractedLink(
                                    url=url,
                                    title=link.get("name", ""),
                                )
                            )

        except (json.JSONDecodeError, KeyError, AttributeError):
            # JSON parsing failed, will try HTML fallback
            pass

        return links

    def _extract_html_links(self, html: str) -> list[ExtractedLink]:
        """Fallback extraction from HTML structure."""
        links = []
        parser = HTMLParser(html)

        # Look for links in the body section
        for link_elem in parser.css('a[data-cy="biosite-link"]'):
            href = link_elem.attributes.get("href", "")
            if href and href.startswith(("http://", "https://")):
                # Try to get the title from the link text
                title_elem = link_elem.css_first('[data-cy="link-text-name"]')
                title = ""
                if title_elem:
                    title = title_elem.text(strip=True)

                try:
                    links.append(ExtractedLink(url=cast(HttpUrl, href), title=title))
                except (ValueError, TypeError):
                    # Skip invalid URLs
                    pass

        # Also look for social links
        for social_elem in parser.css('div[data-cy="biosite-social"] a'):
            href = social_elem.attributes.get("href", "")
            if href and href.startswith(("http://", "https://")):
                # Get social type from parent div
                parent = social_elem.parent
                if parent:
                    social_type = parent.attributes.get("data-social-type", "")
                    try:
                        links.append(
                            ExtractedLink(url=cast(HttpUrl, href), title=social_type)
                        )
                    except (ValueError, TypeError):
                        # Skip invalid URLs
                        pass

        return links

    def _filter_service_urls(self, links: list[ExtractedLink]) -> list[ExtractedLink]:
        """Remove bio.site's internal URLs."""
        filtered = []
        for link in links:
            if not self._is_service_url(str(link.url)):
                filtered.append(link)
        return filtered

    def _is_service_url(self, url: str) -> bool:
        """Check if URL belongs to bio.site itself."""
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            # Skip bio.site domains and CDN domains
            return any(
                domain in hostname
                for domain in ["bio.site", "unfold-dev.com", "media.bio.site"]
            )
        except Exception:
            return "bio.site" in url

    def _deduplicate_links(self, links: list[ExtractedLink]) -> list[ExtractedLink]:
        """Remove duplicate URLs, keeping the one with more metadata."""
        seen = {}
        for link in links:
            url_str = str(link.url)
            if url_str not in seen:
                seen[url_str] = link
            else:
                # Keep the one with more info
                existing = seen[url_str]
                if not existing.title and link.title:
                    seen[url_str] = link
                elif link.title and len(link.title) > len(existing.title or ""):
                    seen[url_str] = link
        return list(seen.values())

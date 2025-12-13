import json
import re
from typing import Any, cast
from urllib.parse import urlparse

import aiohttp
from pydantic import HttpUrl
from selectolax.parser import HTMLParser

from ..base import BaseLinkExtractor
from ..models import ExtractedLink


class InstaBioExtractor(BaseLinkExtractor):
    """Extractor for instabio.cc links."""

    def can_handle(self, url: str) -> bool:
        """Check if URL is from instabio.cc."""
        return "instabio.cc" in url

    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        """Extract links from instabio.cc page."""
        links: list[ExtractedLink] = []

        # First, try to extract links directly from embedded window.__data
        links.extend(self._extract_embedded_links(html))

        # If no links found in embedded data, try fetching from separate JSON endpoint
        if not links:
            bio_id = self._extract_bio_id(html)
            if bio_id:
                # Fetch the JSON data
                json_data = await self._fetch_json_data(bio_id)
                if json_data:
                    links.extend(self._extract_links_from_json(json_data))

        # Fallback to HTML extraction if both methods fail
        if not links:
            links.extend(self._extract_html_links(html))

        # Filter out instabio.cc's own URLs
        links = self._filter_service_urls(links)

        # Deduplicate
        return self._deduplicate_links(links)

    def _extract_embedded_links(self, html: str) -> list[ExtractedLink]:
        """Extract links directly from embedded window.__data in HTML."""
        links: list[ExtractedLink] = []

        # Try to find window.__data with flexible spacing
        patterns = [
            r"window\.__data\s*=\s*({.*?});</script>",
            r"window\.__data=({.*?});</script>",
            r"window\.__data\s*=\s*({.*?})\s*</script>",
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(1))

                    # Check if content.cmpts exists (embedded format like linkbio.co)
                    content = data.get("content", {})
                    if "cmpts" in content:
                        cmpts = content.get("cmpts", [])

                        for component in cmpts:
                            # Extract regular links from button components
                            if "links" in component:
                                for link_item in component.get("links", []):
                                    link_url = link_item.get("link") or link_item.get(
                                        "link1", ""
                                    )
                                    if link_url:
                                        # Fix URLs that don't have protocol
                                        if not link_url.startswith(
                                            ("http://", "https://", "//")
                                        ):
                                            if "." in link_url and "/" in link_url:
                                                link_url = f"https://{link_url}"

                                        if link_url and link_url.startswith(
                                            ("http://", "https://")
                                        ):
                                            title = link_item.get("title", "")
                                            try:
                                                links.append(
                                                    ExtractedLink(
                                                        url=cast(HttpUrl, link_url),
                                                        title=title,
                                                    )
                                                )
                                            except (ValueError, TypeError):
                                                pass

                            # Extract social links
                            elif component.get("type") == 2 and "subs" in component:
                                for social_item in component.get("subs", []):
                                    link_url = social_item.get("link", "")
                                    if link_url and link_url.startswith(
                                        ("http://", "https://")
                                    ):
                                        platform = social_item.get(
                                            "title", ""
                                        ) or self._guess_platform_from_url(link_url)
                                        try:
                                            links.append(
                                                ExtractedLink(
                                                    url=cast(HttpUrl, link_url),
                                                    title=platform,
                                                )
                                            )
                                        except (ValueError, TypeError):
                                            pass

                        # If we found links, return them
                        if links:
                            return links

                except (json.JSONDecodeError, KeyError, AttributeError):
                    continue

        return links

    def _extract_bio_id(self, html: str) -> str | None:
        """Extract bio ID from window.__data."""
        # Try to find window.__data with flexible spacing
        patterns = [
            r"window\.__data\s*=\s*({.*?});",
            r"window\.__data=({.*?});",
            r"window\.__data\s*=\s*({.*?})\s*</script>",
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(1))
                    bio_id = data.get("bio", {}).get("id")
                    if bio_id:
                        return str(bio_id)
                except (json.JSONDecodeError, KeyError, AttributeError):
                    continue

        return None

    async def _fetch_json_data(self, bio_id: str) -> dict[str, Any] | None:
        """Fetch JSON data from the API endpoint."""
        json_url = f"https://bio.linkcdn.cc/upload/lnkcmpts/{bio_id}.json"
        headers = {"User-Agent": self.user_agent}

        try:
            if self.session:
                async with self.session.get(
                    json_url, proxy=self.proxy, headers=headers
                ) as response:
                    if response.status == 200:
                        data: dict[str, Any] = await response.json()
                        return data
            else:
                # Create a temporary session if none exists
                async with aiohttp.ClientSession() as session:
                    proxy_url = self.proxy if self.proxy else None
                    async with session.get(
                        json_url, proxy=proxy_url, headers=headers
                    ) as response:
                        if response.status == 200:
                            response_data: dict[str, Any] = await response.json()
                            return response_data
        except Exception:
            pass

        return None

    def _extract_links_from_json(
        self, json_data: dict[str, Any]
    ) -> list[ExtractedLink]:
        """Extract links from the JSON data."""
        links: list[ExtractedLink] = []

        # Parse the cmpts field which contains JSON string
        cmpts_str = json_data.get("cmpts", "")
        if not cmpts_str:
            return links

        try:
            cmpts = json.loads(cmpts_str)

            for component in cmpts:
                # Extract regular links from button components
                if component.get("type") == 10 and "links" in component:
                    for link_item in component.get("links", []):
                        link_url = link_item.get("link") or link_item.get("link1", "")
                        if link_url and link_url.startswith(("http://", "https://")):
                            title = link_item.get("title", "")
                            try:
                                links.append(
                                    ExtractedLink(
                                        url=cast(HttpUrl, link_url),
                                        title=title,
                                    )
                                )
                            except (ValueError, TypeError):
                                pass

                # Extract social links
                elif component.get("type") == 2 and "subs" in component:
                    for social_item in component.get("subs", []):
                        link_url = social_item.get("link", "")
                        if link_url and link_url.startswith(("http://", "https://")):
                            # Get platform name from title or type
                            platform = social_item.get("title", "")
                            if not platform:
                                # Try to guess from URL
                                platform = self._guess_platform_from_url(link_url)

                            try:
                                links.append(
                                    ExtractedLink(
                                        url=cast(HttpUrl, link_url),
                                        title=platform,
                                    )
                                )
                            except (ValueError, TypeError):
                                pass

        except (json.JSONDecodeError, KeyError, AttributeError):
            pass

        return links

    def _guess_platform_from_url(self, url: str) -> str:
        """Guess platform name from URL."""
        domain_map = {
            "instagram.com": "Instagram",
            "twitter.com": "Twitter",
            "x.com": "Twitter/X",
            "youtube.com": "YouTube",
            "tiktok.com": "TikTok",
            "facebook.com": "Facebook",
            "threads.net": "Threads",
            "threads.com": "Threads",
        }

        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            for domain, name in domain_map.items():
                if domain in hostname:
                    return name
        except Exception:
            pass

        return ""

    def _extract_html_links(self, html: str) -> list[ExtractedLink]:
        """Fallback extraction from HTML structure."""
        links: list[ExtractedLink] = []
        parser = HTMLParser(html)

        # Look for any link elements that might be rendered
        for link_elem in parser.css("a[href]"):
            href = link_elem.attributes.get("href", "")
            if href and href.startswith(("http://", "https://")):
                title = link_elem.text(strip=True)
                try:
                    links.append(ExtractedLink(url=cast(HttpUrl, href), title=title))
                except (ValueError, TypeError):
                    pass

        return links

    def _filter_service_urls(self, links: list[ExtractedLink]) -> list[ExtractedLink]:
        """Remove instabio.cc's internal URLs."""
        filtered = []
        for link in links:
            if not self._is_service_url(str(link.url)):
                filtered.append(link)
        return filtered

    def _is_service_url(self, url: str) -> bool:
        """Check if URL belongs to instabio.cc itself."""
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            # Skip instabio.cc domains and CDN domains
            return any(
                domain in hostname
                for domain in ["instabio.cc", "linkcdn.cc", "bio.linkcdn.cc"]
            )
        except Exception:
            return "instabio.cc" in url

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

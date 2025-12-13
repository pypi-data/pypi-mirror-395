import json
import re
from urllib.parse import urlparse
from pydantic import HttpUrl
from ..base import BaseLinkExtractor
from ..models import ExtractedLink


class LitLinkExtractor(BaseLinkExtractor):
    def can_handle(self, url: str) -> bool:
        return "lit.link" in url

    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        links = []

        # Extract profile data from JavaScript
        # Look for the JSON data containing snsIconLinks and profileLinks
        profile_pattern = r'"snsIconLinks":\[(.*?)\].*?"profileLinks":\[(.*?)\]'
        match = re.search(profile_pattern, html, re.DOTALL)

        if match:
            try:
                # Extract SNS icon links
                sns_json_str = "[" + match.group(1) + "]"
                sns_json_str = self._clean_json_string(sns_json_str)
                sns_data = json.loads(sns_json_str)

                for item in sns_data:
                    if "url" in item:
                        # Skip lit.link internal URLs
                        if self._should_exclude_url(item["url"]):
                            continue
                        try:
                            link = ExtractedLink(
                                url=HttpUrl(item["url"]),
                                title=item.get("type", "").title(),
                                metadata={
                                    "source": "sns_icon",
                                    "type": item.get("type", ""),
                                },
                            )
                            links.append(link)
                        except Exception:
                            continue

                # Extract profile links
                profile_json_str = "[" + match.group(2) + "]"
                profile_json_str = self._clean_json_string(profile_json_str)
                profile_data = json.loads(profile_json_str)

                for item in profile_data:
                    if "buttonLink" in item and item["buttonLink"]:
                        button = item["buttonLink"]
                        if "url" in button and button["url"]:
                            # Skip lit.link internal URLs
                            if self._should_exclude_url(button["url"]):
                                continue

                            description = button.get("description", "")
                            # Build title with description if available
                            title = button.get("title", "")
                            if description:
                                title = f"{title} {description}".strip()

                            try:
                                link = ExtractedLink(
                                    url=HttpUrl(button["url"]),
                                    title=title,
                                    metadata={
                                        "source": "profile_link",
                                        "type": button.get("urlType", "others"),
                                        "icon_url": button.get("iconUrl", ""),
                                    },
                                )
                                links.append(link)
                            except Exception:
                                continue
            except (json.JSONDecodeError, AttributeError):
                # If JSON parsing fails, fall back to regex extraction
                pass

        if not links:
            # Fallback 1: try to extract links from a more general pattern
            # Look for objects with url properties
            url_pattern = r'"url"\s*:\s*"(https?://[^"]+)"'
            urls = re.findall(url_pattern, html)

            # Also try to find associated titles
            for found_url in urls:
                # Skip lit.link internal URLs (exclude URLs with lit.link hostname)
                if self._should_exclude_url(found_url):
                    continue

                # Try to find a title near this URL
                title = self._find_nearby_title(html, found_url)
                try:
                    link = ExtractedLink(
                        url=HttpUrl(found_url), title=title or found_url
                    )
                    links.append(link)
                except Exception:
                    continue

        # Fallback 2: Extract from regular HTML <a> tags if still no links
        if not links:
            from selectolax.parser import HTMLParser

            parser = HTMLParser(html)

            # Look for all links in <a> tags
            for a_tag in parser.css("a[href]"):
                href = a_tag.attributes.get("href", "") or ""
                href = href.strip()
                if not href or not href.startswith(("http://", "https://")):
                    continue

                # Skip lit.link internal URLs
                if self._should_exclude_url(href):
                    continue

                # Get link text
                text = a_tag.text(strip=True) or None

                try:
                    link = ExtractedLink(
                        url=HttpUrl(href), title=text, metadata={"source": "html_link"}
                    )
                    links.append(link)
                except Exception:
                    continue

        return self._deduplicate_links(links)

    def _should_exclude_url(self, url: str) -> bool:
        """Check if URL should be excluded (lit.link internal URLs)"""
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            # Exclude lit.link domains and subdomains
            return "lit.link" in hostname or hostname.endswith(".lit.link")
        except Exception:
            # If we can't parse, check simple string match as fallback
            return "lit.link" in url

    def _clean_json_string(self, json_str: str) -> str:
        """Clean up escaped characters in JSON string"""
        # Remove escape characters that might break JSON parsing
        json_str = json_str.replace('\\"', '"')
        json_str = json_str.replace("\\\\", "\\")
        return json_str

    def _find_nearby_title(self, html: str, url: str) -> str | None:
        """Try to find a title near the URL in the HTML"""
        # Look for patterns like "title":"...", "url":"..."
        pattern = r'"title"\s*:\s*"([^"]+)"[^}]*?"url"\s*:\s*"' + re.escape(url) + '"'
        match = re.search(pattern, html)
        if match:
            return match.group(1)

        # Also try reverse order
        pattern = r'"url"\s*:\s*"' + re.escape(url) + r'"[^}]*?"title"\s*:\s*"([^"]+)"'
        match = re.search(pattern, html)
        if match:
            return match.group(1)

        return None

    def _deduplicate_links(self, links: list[ExtractedLink]) -> list[ExtractedLink]:
        """Remove duplicate links, keeping the one with more metadata"""
        seen = {}
        for link in links:
            url_str = str(link.url)
            if url_str not in seen:
                seen[url_str] = link
            else:
                # Keep the one with more information
                existing = seen[url_str]
                if (not existing.title or existing.title == url_str) and link.title:
                    seen[url_str] = link
                elif link.metadata and not existing.metadata:
                    seen[url_str] = link

        return list(seen.values())

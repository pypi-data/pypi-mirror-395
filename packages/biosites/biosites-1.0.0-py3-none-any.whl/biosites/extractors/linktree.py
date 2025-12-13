import json
from pydantic import HttpUrl
from selectolax.parser import HTMLParser

from ..base import BaseLinkExtractor
from ..models import ExtractedLink


class LinktreeExtractor(BaseLinkExtractor):
    def can_handle(self, url: str) -> bool:
        return "linktr.ee" in url or "linktree.com" in url

    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        links: list[ExtractedLink] = []
        parser = HTMLParser(html)

        # Find the script#__NEXT_DATA__ element
        script_element = parser.css_first("script#__NEXT_DATA__")
        if not script_element:
            return links

        try:
            # Get the JSON content
            json_content = script_element.text().strip()
            if not json_content:
                return links

            # Parse JSON
            data = json.loads(json_content)

            # Navigate to links in the data structure
            props = data.get("props", {})
            page_props = props.get("pageProps", {})
            link_items = page_props.get("links", [])

            # Extract links
            for item in link_items:
                # Get the URL from the item
                item_url = item.get("url", "").strip()
                if not item_url:
                    continue

                # Skip if it's not a valid URL
                if not item_url.startswith(("http://", "https://")):
                    # Some URLs might be relative or malformed
                    if item_url.startswith("//"):
                        item_url = f"https:{item_url}"
                    else:
                        continue

                # Get title and other metadata
                title = item.get("title", "").strip() or None
                link_type = item.get("type", "")
                link_id = item.get("id", "")
                thumbnail = item.get("thumbnail", "")

                # Get context if available
                context = item.get("context", {})

                # Create ExtractedLink
                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(item_url),
                            title=title,
                            icon_url=HttpUrl(thumbnail)
                            if thumbnail and thumbnail.startswith("http")
                            else None,
                            metadata={
                                "type": link_type,
                                "id": link_id,
                                "has_thumbnail": bool(thumbnail),
                                "context": context if context else None,
                            },
                        )
                    )
                except Exception:
                    # Skip invalid URLs
                    continue

            # Also extract social links if available
            social_links = page_props.get("socialLinks", [])
            for social_item in social_links:
                social_url = social_item.get("url", "").strip()
                if not social_url or not social_url.startswith(("http://", "https://")):
                    continue

                platform = social_item.get("type", "social")

                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(social_url),
                            title=f"{platform.title()} Profile",
                            metadata={
                                "type": "social",
                                "platform": platform,
                            },
                        )
                    )
                except Exception:
                    continue

        except (ValueError, json.JSONDecodeError):
            # If we can't parse JSON, return empty list
            return links

        return links

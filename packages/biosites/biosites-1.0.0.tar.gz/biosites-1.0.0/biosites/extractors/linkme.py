"""
LinkMe extractor for link.me profiles.
"""

import json
import re
from typing import Any

from ..base import BaseLinkExtractor
from ..models import ExtractedLink


class LinkMeExtractor(BaseLinkExtractor):
    """Extractor for LinkMe profiles."""

    def can_handle(self, url: str) -> bool:
        return "link.me" in url.lower()

    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        """Extract links from LinkMe profile page."""
        links: list[ExtractedLink] = []

        # Find the __NEXT_DATA__ script tag
        script_match = re.search(
            r'<script id="__NEXT_DATA__"[^>]*>([^<]+)</script>', html, re.DOTALL
        )

        if not script_match:
            return links

        try:
            # Parse the JSON data
            data = json.loads(script_match.group(1))
            profile_data = data.get("props", {}).get("pageProps", {}).get("profile", {})

            # Extract webLinks
            web_links = profile_data.get("webLinks", [])
            for link_category in web_links:
                title = link_category.get("title", "")
                for link_item in link_category.get("links", []):
                    link_value = link_item.get("linkValue", "")
                    if link_value:
                        # Build metadata
                        metadata: dict[str, Any] = {
                            "category": title,
                            "face_value": link_item.get("faceValue"),
                            "is_custom": link_item.get("isCustom", False),
                        }

                        # Clean up metadata - remove None values
                        metadata = {k: v for k, v in metadata.items() if v is not None}

                        links.append(
                            ExtractedLink(
                                url=link_value,
                                title=title,
                                metadata=metadata,
                            )
                        )

            # Also extract infoLinks if present
            info_links = profile_data.get("infoLinks")
            if info_links and isinstance(info_links, list):
                for info_link in info_links:
                    if isinstance(info_link, dict):
                        link_url = info_link.get("linkValue", "")
                        if link_url:
                            links.append(
                                ExtractedLink(
                                    url=link_url,
                                    title=info_link.get("title", ""),
                                    metadata={"type": "info_link"},
                                )
                            )

            # Extract businessInfo links if present
            business_info = profile_data.get("businessInfo")
            if business_info and isinstance(business_info, dict):
                # Check for website
                website = business_info.get("website", "")
                if website:
                    links.append(
                        ExtractedLink(
                            url=website,
                            title="Business Website",
                            metadata={"type": "business"},
                        )
                    )

        except (json.JSONDecodeError, KeyError, TypeError):
            pass

        return links

import json
import pybase64
from pydantic import HttpUrl
from selectolax.parser import HTMLParser

from ..base import BaseLinkExtractor
from ..models import ExtractedLink


class LittlyExtractor(BaseLinkExtractor):
    def can_handle(self, url: str) -> bool:
        return "litt.ly" in url

    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        links: list[ExtractedLink] = []
        parser = HTMLParser(html)

        # Find the script#data element
        script_element = parser.css_first("script#data")
        if not script_element:
            return links

        try:
            # Get the base64 content
            base64_content = script_element.text().strip()
            if not base64_content:
                return links

            # Decode base64
            decoded = pybase64.b64decode(base64_content).decode("utf-8")

            # Parse JSON
            data = json.loads(decoded)

            # Extract links from blocks
            blocks = data.get("blocks", [])
            for block in blocks:
                # Only process blocks that are in use
                if not block.get("use", False):
                    continue

                # Get the URL from the block
                block_url = block.get("url", "").strip()
                if not block_url:
                    continue

                # Skip if it's not a valid URL
                if not block_url.startswith(("http://", "https://")):
                    continue

                # Get title and other metadata
                title = block.get("title", "").strip() or None
                block_type = block.get("type", "")

                # Create ExtractedLink
                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(block_url),
                            title=title,
                            metadata={
                                "type": block_type,
                                "form": block.get("form", ""),
                                "key": block.get("key", ""),
                            },
                        )
                    )
                except Exception:
                    # Skip invalid URLs
                    continue

        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            # If we can't decode or parse, return empty list
            return links

        return links

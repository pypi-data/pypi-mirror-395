import re
from pydantic import HttpUrl
from selectolax.parser import HTMLParser

from ..base import BaseLinkExtractor
from ..models import ExtractedLink


class InPockExtractor(BaseLinkExtractor):
    def can_handle(self, url: str) -> bool:
        return "link.inpock.co.kr" in url or "inpk.link" in url

    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        links: list[ExtractedLink] = []

        # Extract from SSR content first (main links)
        links.extend(self._extract_ssr_links(html))

        # Extract social links from NUXT data
        links.extend(self._extract_nuxt_social_links(html))

        # Remove duplicates by URL
        seen_urls = set()
        unique_links = []
        for link in links:
            url_str = str(link.url)
            if url_str not in seen_urls:
                seen_urls.add(url_str)
                unique_links.append(link)

        return unique_links

    def _extract_ssr_links(self, html: str) -> list[ExtractedLink]:
        """Extract user links from server-side rendered content"""
        links: list[ExtractedLink] = []
        parser = HTMLParser(html)

        # InPock system URLs to exclude
        SYSTEM_URLS = [
            "team.ab-z.com",
            "/admin",
            "/offer",
            "inpock.co.kr/admin",
            "channel.io",
            "d155kgavghly9c",
            "d13k46lqgoj3d6",  # CDN URLs
        ]

        # Find the main content area
        # Look for link blocks in the interaction-block-wrapper class
        link_blocks = parser.css("div.interaction-block-wrapper a")

        for block in link_blocks:
            href = block.attributes.get("href", "") or ""
            href = href.strip()
            if not href:
                continue

            # Skip InPock system links (be more selective)
            if any(system_url in href for system_url in SYSTEM_URLS):
                continue

            # Skip only specific relative URLs
            if href in ["/", "/guide", "/plan", "/cs", "/subscribe"]:
                continue

            # Extract title from the block
            title = None
            title_elem = block.css_first("p.title")
            if title_elem:
                title_text = title_elem.text(strip=True)
                if title_text:
                    # Clean up title (remove extra whitespace and newlines)
                    title = " ".join(title_text.split())

            # Only process valid external URLs
            if href.startswith(("http://", "https://")):
                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(href),
                            title=title,
                            metadata={"source": "ssr", "type": "link"},
                        )
                    )
                except Exception:
                    continue

        return links

    def _extract_nuxt_social_links(self, html: str) -> list[ExtractedLink]:
        """Extract social links from window.__NUXT__ data"""
        links: list[ExtractedLink] = []

        # Find window.__NUXT__ script
        match = re.search(r"window\.__NUXT__=(.*?);</script>", html, re.DOTALL)
        if not match:
            return links

        nuxt_str = match.group(1)

        # Extract Instagram username
        insta_match = re.search(r'insta_username:"([^"]+)"', nuxt_str)
        if insta_match:
            username = insta_match.group(1)
            if username and username != "null":
                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(f"https://www.instagram.com/{username}/"),
                            title=f"Instagram @{username}",
                            metadata={
                                "source": "nuxt",
                                "type": "social",
                                "platform": "instagram",
                                "username": username,
                            },
                        )
                    )
                except Exception:
                    pass

        # Extract YouTube URL
        youtube_match = re.search(r'youtube_url:"([^"]+)"', nuxt_str)
        if youtube_match:
            youtube_url = youtube_match.group(1)
            if youtube_url and youtube_url != "null":
                # Decode unicode escapes
                youtube_url = youtube_url.encode().decode("unicode_escape")
                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(youtube_url),
                            title="YouTube Channel",
                            metadata={
                                "source": "nuxt",
                                "type": "social",
                                "platform": "youtube",
                            },
                        )
                    )
                except Exception:
                    pass

        # Extract Naver Blog URL
        blog_match = re.search(r'naver_blog_url:"([^"]+)"', nuxt_str)
        if blog_match:
            blog_url = blog_match.group(1)
            if blog_url and blog_url != "null":
                # Decode unicode escapes
                blog_url = blog_url.encode().decode("unicode_escape")
                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(blog_url),
                            title="Naver Blog",
                            metadata={
                                "source": "nuxt",
                                "type": "social",
                                "platform": "naver_blog",
                            },
                        )
                    )
                except Exception:
                    pass

        # Extract TikTok username if available
        tiktok_match = re.search(r'tiktok_username:"([^"]+)"', nuxt_str)
        if tiktok_match:
            username = tiktok_match.group(1)
            if username and username != "null":
                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(f"https://www.tiktok.com/@{username}"),
                            title=f"TikTok @{username}",
                            metadata={
                                "source": "nuxt",
                                "type": "social",
                                "platform": "tiktok",
                                "username": username,
                            },
                        )
                    )
                except Exception:
                    pass

        # Extract Facebook username if available
        facebook_match = re.search(r'facebook_username:"([^"]+)"', nuxt_str)
        if facebook_match:
            username = facebook_match.group(1)
            if username and username != "null":
                try:
                    links.append(
                        ExtractedLink(
                            url=HttpUrl(f"https://www.facebook.com/{username}"),
                            title=f"Facebook @{username}",
                            metadata={
                                "source": "nuxt",
                                "type": "social",
                                "platform": "facebook",
                                "username": username,
                            },
                        )
                    )
                except Exception:
                    pass

        return links

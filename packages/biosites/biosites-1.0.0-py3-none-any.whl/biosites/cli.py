#!/usr/bin/env python
import argparse
import asyncio
import json
import os
import sys
from datetime import datetime

from .extractor import LinkExtractor
from .models import ExtractionResult


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="biosites",
        description="Extract links from bio link services (Linktree, litt.ly, etc.)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  biosites https://litt.ly/yellowballoon
  biosites https://litt.ly/yellowballoon --output json
  biosites https://litt.ly/yellowballoon -o json > links.json
        """.strip(),
    )

    parser.add_argument(
        "url",
        help="URL of the bio link page to extract",
    )

    parser.add_argument(
        "-o",
        "--output",
        choices=["cli", "json"],
        default="cli",
        help="Output format (default: cli)",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output in CLI mode",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show additional information",
    )

    parser.add_argument(
        "--proxy",
        help="HTTP proxy URL (e.g., http://proxy.example.com:8080). Can also be set via HTTP_PROXY environment variable",
    )

    parser.add_argument(
        "--user-agent",
        help="Custom User-Agent header for requests (default: Chrome on macOS)",
    )

    parser.add_argument(
        "--no-follow-redirects",
        action="store_true",
        help="Don't follow URL redirects (useful for debugging shortened URLs)",
    )

    return parser


def format_cli_output(
    result: ExtractionResult, no_color: bool = False, verbose: bool = False
) -> str:
    output = []

    # Colors for terminal
    if not no_color and sys.stdout.isatty():
        RESET = "\033[0m"
        BOLD = "\033[1m"
        GREEN = "\033[32m"
        BLUE = "\033[34m"
        YELLOW = "\033[33m"
        RED = "\033[31m"
        GRAY = "\033[90m"
    else:
        RESET = BOLD = GREEN = BLUE = YELLOW = RED = GRAY = ""

    # Header
    output.append(f"\n{BOLD}{'=' * 60}{RESET}")
    output.append(f"{BOLD}Bio Links Extraction Results{RESET}")
    output.append(f"{BOLD}{'=' * 60}{RESET}\n")

    # Source info
    output.append(f"{BOLD}Source URL:{RESET} {BLUE}{result.source_url}{RESET}")
    if result.service_type:
        output.append(f"{BOLD}Service:{RESET} {GREEN}{result.service_type}{RESET}")

    if verbose and result.extraction_timestamp:
        output.append(f"{BOLD}Extracted:{RESET} {result.extraction_timestamp}")

    # Show redirect info if present
    if verbose and result.metadata and "redirect_chain" in result.metadata:
        output.append(f"\n{YELLOW}Followed redirects:{RESET}")
        original = result.metadata.get("original_url", "")
        if original:
            output.append(f"  {BOLD}Original:{RESET} {original}")
        for redirect in result.metadata["redirect_chain"]:
            output.append(f"  {GRAY}→ {redirect}{RESET}")
        output.append(f"  {GREEN}→ {result.source_url}{RESET} (final)")

    # Links count
    output.append(
        f"\n{BOLD}Found {GREEN}{len(result.links)}{RESET} {BOLD}links:{RESET}\n"
    )

    # Links
    if result.links:
        for i, link in enumerate(result.links, 1):
            # Link number and title
            title = link.title or "(No title)"
            output.append(f"{BOLD}{i:2}.{RESET} {title}")

            # URL (truncate if too long for display)
            url_str = str(link.url)
            if len(url_str) > 80 and not verbose:
                # Truncate query parameters for display
                if "?" in url_str:
                    base_url = url_str.split("?")[0]
                    url_str = f"{base_url}?..."
                elif len(url_str) > 80:
                    url_str = url_str[:77] + "..."

            output.append(f"    {GRAY}→ {url_str}{RESET}")

            # Metadata in verbose mode
            if verbose and link.metadata:
                for key, value in link.metadata.items():
                    if value:
                        output.append(f"    {GRAY}  {key}: {value}{RESET}")

            # Add spacing between links
            if i < len(result.links):
                output.append("")
    else:
        output.append(f"{YELLOW}No links found.{RESET}")

    # Errors
    if result.errors:
        output.append(f"\n{RED}{BOLD}Errors:{RESET}")
        for error in result.errors:
            output.append(f"  {RED}• {error}{RESET}")

    output.append(f"\n{BOLD}{'=' * 60}{RESET}\n")

    return "\n".join(output)


def format_json_output(result: ExtractionResult) -> str:
    # Convert to dict for JSON serialization
    data = {
        "source_url": str(result.source_url),
        "service_type": result.service_type,
        "extraction_timestamp": datetime.now().isoformat(),
        "links_count": len(result.links),
        "links": [
            {
                "url": str(link.url),
                "title": link.title,
                "description": link.description,
                "icon_url": str(link.icon_url) if link.icon_url else None,
                "metadata": link.metadata,
            }
            for link in result.links
        ],
        "errors": result.errors,
        "metadata": result.metadata,
    }

    return json.dumps(data, indent=2, ensure_ascii=False)


async def extract_links(
    url: str,
    proxy: str | None = None,
    user_agent: str | None = None,
    follow_redirects: bool = True,
) -> ExtractionResult:
    extractor = LinkExtractor(
        proxy=proxy, user_agent=user_agent, follow_redirects=follow_redirects
    )
    result = await extractor.extract(url)
    # Add timestamp
    result.extraction_timestamp = datetime.now().isoformat()
    return result


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    # Determine proxy: CLI arg takes precedence over environment variable
    proxy = args.proxy or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")

    if proxy and args.verbose:
        print(f"Using proxy: {proxy}", file=sys.stderr)

    if args.user_agent and args.verbose:
        print(f"Using User-Agent: {args.user_agent}", file=sys.stderr)

    follow_redirects = not args.no_follow_redirects
    if args.verbose and not follow_redirects:
        print("Redirect following disabled", file=sys.stderr)

    try:
        # Run the async extraction
        result = asyncio.run(
            extract_links(
                args.url,
                proxy=proxy,
                user_agent=args.user_agent,
                follow_redirects=follow_redirects,
            )
        )

        # Format output based on selected format
        if args.output == "json":
            print(format_json_output(result))
        else:
            print(format_cli_output(result, args.no_color, args.verbose))

        # Exit with error code if there were errors
        if result.errors and not result.links:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

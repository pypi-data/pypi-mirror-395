"""
Web Tools

Tools for web content extraction, downloading, and search.

Usage:
    from innerloop.tooling import fetch, download, search

    loop = Loop(model="...", tools=[fetch, download, search])
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
import trafilatura
from bs4 import BeautifulSoup

from ..types import ToolContext
from .base import tool
from .filesystem import _secure_path

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


@tool
async def fetch(ctx: ToolContext, url: str) -> str:
    """
    Fetch a webpage and extract its readable content as markdown.

    Uses trafilatura for content extraction - removes navigation, ads, etc.
    Returns the main article/page content.

    Args:
        url: URL to fetch (http or https)
    """
    # Validate URL scheme
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Invalid URL scheme '{parsed.scheme}'. Only http and https allowed."
        )

    async with httpx.AsyncClient(timeout=ctx.tool_timeout) as client:
        resp = await client.get(url, headers=HEADERS, follow_redirects=True)
        resp.raise_for_status()
        html = resp.text

    # Extract with trafilatura
    content = trafilatura.extract(
        html,
        include_links=True,
        include_formatting=True,
        include_images=False,
        output_format="markdown",
    )

    if not content:
        # Fallback: try to get any text
        content = trafilatura.extract(html, favor_recall=True)

    if not content:
        return "(Could not extract readable content from this page)"

    # Truncate if too long
    if len(content) > 15000:
        content = content[:15000] + "\n\n... (truncated)"

    return content


@tool
async def download(ctx: ToolContext, url: str, path: str) -> str:
    """
    Download a file from a URL to a local path.

    Preserves original file format. Path is relative to workdir.

    Args:
        url: URL to download from (http or https)
        path: Local path to save file (relative to working directory)
    """
    # Validate URL scheme
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Invalid URL scheme '{parsed.scheme}'. Only http and https allowed."
        )

    # Resolve path relative to workdir with security check
    dest = _secure_path(path, ctx.workdir)

    # Create parent directories
    dest.parent.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient(timeout=ctx.tool_timeout) as client:
        resp = await client.get(url, headers=HEADERS, follow_redirects=True)
        resp.raise_for_status()

        # Write binary content
        dest.write_bytes(resp.content)

    size = dest.stat().st_size
    return f"Downloaded {url} to {path} ({size:,} bytes)"


@dataclass
class SearchResult:
    """A single search result."""

    title: str
    url: str
    snippet: str


def _parse_brave_results(html: str, num_results: int) -> list[SearchResult]:
    """Parse Brave search HTML to extract results."""
    soup = BeautifulSoup(html, "html.parser")
    results: list[SearchResult] = []

    # Find all search result snippets with data-type="web"
    snippets = soup.select('div.snippet[data-type="web"]')

    for snippet in snippets:
        if len(results) >= num_results:
            break

        # Get the main link and title
        title_link = snippet.select_one("a.result-header")
        if not title_link:
            continue

        url = title_link.get("href", "")
        if not url or "brave.com" in str(url):
            continue

        title_el = title_link.select_one(".title")
        title = (
            title_el.get_text(strip=True)
            if title_el
            else title_link.get_text(strip=True)
        )

        # Get the snippet/description
        desc_el = snippet.select_one(".snippet-content, .snippet-description")
        snippet_text = desc_el.get_text(strip=True) if desc_el else ""

        # Remove date prefix if present (e.g., "Jan 15, 2024 - ")
        snippet_text = re.sub(r"^[A-Z][a-z]+ \d+, \d{4}\s*[-–]\s*", "", snippet_text)

        if title and url:
            results.append(
                SearchResult(title=str(title), url=str(url), snippet=snippet_text)
            )

    return results


@tool
async def search(
    ctx: ToolContext,
    query: str,
    num_results: int = 5,
    fetch_content: bool = False,
) -> str:
    """
    Search the web using Brave Search.

    Returns titles, URLs, and snippets. Set fetch_content=True to also
    extract readable content from each result (slower but more detailed).

    Args:
        query: Search query string
        num_results: Number of results to return (default: 5)
        fetch_content: Whether to fetch and extract content from each result
    """
    async with httpx.AsyncClient(timeout=ctx.tool_timeout) as client:
        resp = await client.get(
            "https://search.brave.com/search",
            params={"q": query},
            headers=HEADERS,
            follow_redirects=True,
        )
        resp.raise_for_status()
        html = resp.text

    results = _parse_brave_results(html, num_results)

    if not results:
        return "No results found."

    # Optionally fetch content from each result
    if fetch_content:
        async with httpx.AsyncClient(timeout=10) as client:
            for r in results:
                try:
                    resp = await client.get(
                        r.url, headers=HEADERS, follow_redirects=True
                    )
                    if resp.status_code == 200:
                        content = trafilatura.extract(
                            resp.text,
                            include_formatting=True,
                            output_format="markdown",
                        )
                        if content:
                            r.snippet = content[:2000]
                except Exception as e:
                    # Log but continue - keep original snippet
                    logger.debug("Failed to fetch content for %s: %s", r.url, e)

    # Format output
    lines: list[str] = []
    for i, r in enumerate(results, 1):
        lines.append(f"--- Result {i} ---")
        lines.append(f"Title: {r.title}")
        lines.append(f"URL: {r.url}")
        if r.snippet:
            lines.append(f"Snippet: {r.snippet[:500]}")
        lines.append("")

    return "\n".join(lines)


# Bundle
WEB_TOOLS = [fetch, download, search]

__all__ = [
    "fetch",
    "download",
    "search",
    "WEB_TOOLS",
]

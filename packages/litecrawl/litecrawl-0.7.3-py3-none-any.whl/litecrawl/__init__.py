"""Minimal asynchronous cron-friendly Playwright-based targeted web crawler."""

from __future__ import annotations

import asyncio
import hashlib
import ipaddress
import json
import logging
import re
import socket
import time
import urllib.robotparser
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin, urlparse, urlunparse

import aiosqlite
import filetype
from lxml import html
from playwright.async_api import BrowserContext, Page, Response, Route, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

# Default values
DEFAULT_HEADERS = {"User-Agent": "litecrawl"}
DEFAULT_VIEWPORT = {"width": 2160, "height": 3840}
DEFAULT_BLOCK_RESOURCES = {"image", "font", "media"}

# Cache for SSRF safety decisions, keyed by hostname
_SSRF_SAFE_CACHE: dict[str, bool] = {}

# Mime map for extension guessing
MIME_MAP = {
    # HTML
    "text/html": "html",
    "application/xhtml+xml": "html",
    # Data / text
    "text/csv": "csv",
    "text/plain": "txt",
    "application/json": "json",
    "text/xml": "xml",
    "application/xml": "xml",
    # Non-binary images
    "image/svg+xml": "svg",
}

# --- Hooks Definitions ---
PageReadyHook = Callable[[str, Response, Page], Awaitable[None]]
LinkExtractHook = Callable[[str, Response, Page, str], Awaitable[list[str]]]
ContentExtractHook = Callable[[str, Response, Page, str], Awaitable[Any]]
DownstreamHook = Callable[[str, Response | None, Page | None, str | None, Any, bool, str], Awaitable[None]]


@dataclass
class PageRecord:
    norm_url: str
    first_seen_time: int
    last_inlink_seen_time: int
    last_crawl_time: int | None
    next_crawl_time: int | None
    error_count: int
    content_hash: str


class RobotsGatekeeper:
    """Simple cache for robots.txt parsing."""
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.parsers: dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def can_fetch(self, url: str) -> bool:
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Check if we need to fetch (Double-check locking pattern)
        if domain not in self.parsers:
            async with self._lock:
                if domain not in self.parsers:
                    parser = urllib.robotparser.RobotFileParser()
                    robots_url = urlunparse((parsed.scheme, domain, "/robots.txt", "", "", ""))
                    try:
                        await asyncio.get_running_loop().run_in_executor(None, parser.set_url, robots_url)
                        await asyncio.get_running_loop().run_in_executor(None, parser.read)
                    except Exception:
                        pass
                    self.parsers[domain] = parser
        
        return self.parsers[domain].can_fetch(self.user_agent, url)


class DownloadResponseAdapter:
    """
    Duck-types a Playwright Response object for downloaded files.
    """
    def __init__(self, download, path: str):
        self.url = download.url
        self.status = 200
        self.ok = True
        self._path = path
        
        # Calculate size immediately
        import os
        try:
            self._size = os.path.getsize(path)
        except OSError:
            self._size = 0
            
        self.headers = {
            "content-length": str(self._size),
            "content-type": "application/octet-stream",
        }

    async def body(self) -> bytes:
        def read_file():
            with open(self._path, "rb") as f:
                return f.read()
        return await asyncio.get_running_loop().run_in_executor(None, read_file)
    
    async def text(self) -> str:
        b = await self.body()
        return b.decode("utf-8", errors="replace")


def litecrawl(
    sqlite_path: str,
    start_urls: list[str],
    **kwargs
) -> None:
    """Synchronous wrapper for litecrawl_async."""
    asyncio.run(litecrawl_async(sqlite_path, start_urls, **kwargs))


async def litecrawl_async(
    sqlite_path: str,
    start_urls: list[str],
    normalize_patterns: list[dict[str, str]] | None = None,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    n_claims: int = 100,
    n_concurrent: int = 10,
    check_robots_txt: bool = True,
    check_ssrf: bool = True,
    max_file_size: int = 50 * 1024 * 1024, # (50 mb)
    pw_headers: dict[str, str] | None = None,
    pw_scroll_rounds: int = 3,
    pw_scroll_timeout_ms: int = 800,
    pw_scroll_selector: str = "body",
    pw_timeout_ms: int = 15000,
    pw_viewport: dict | None = None,
    pw_block_resources: set[str] | None = None,
    page_ready_hook: PageReadyHook | None = None,
    link_extract_hook: LinkExtractHook | None = None,
    content_extract_hook: ContentExtractHook | None = None,
    downstream_hook: DownstreamHook | None = None,
    new_interval_sec: int = 60 * 60 * 24,
    min_interval_sec: int = 60 * 60,
    max_interval_sec: int = 60 * 60 * 24 * 30,
    fresh_factor: float = 0.2,
    stale_factor: float = 2.0,
    inlink_retention_sec: int = 60 * 60 * 24 * 31,
    error_threshold: int = 3,
    processing_timeout_sec: int = 60 * 10,
) -> None:
    """Async entry point for the crawler."""
    pw_headers = pw_headers or DEFAULT_HEADERS
    pw_viewport = pw_viewport or DEFAULT_VIEWPORT
    if pw_block_resources is None:
        pw_block_resources = DEFAULT_BLOCK_RESOURCES

    _validate_intervals(
        min_interval_sec=min_interval_sec,
        max_interval_sec=max_interval_sec,
        fresh_factor=fresh_factor,
        stale_factor=stale_factor,
    )

    # Convenience
    patterns = normalize_patterns, include_patterns, exclude_patterns
    intervals = new_interval_sec, min_interval_sec, max_interval_sec, fresh_factor, stale_factor

    page_ready_hook = _wrap_hook(page_ready_hook or _page_ready_hook)
    link_extract_hook = _wrap_hook(link_extract_hook or _link_extract_hook)
    content_extract_hook = _wrap_hook(content_extract_hook or _content_extract_hook)
    downstream_hook = _wrap_hook(downstream_hook or _downstream_hook)

    robots = RobotsGatekeeper(pw_headers.get("User-Agent", "litecrawl")) if check_robots_txt else None

    async with aiosqlite.connect(sqlite_path) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("PRAGMA journal_mode=WAL;")
        await _create_schema(db)
        
        # 1. Prune expired URLs
        await _cleanup_retention(db, inlink_retention_sec)
        
        # 2. Bootstrap Start URLs
        await _bootstrap_start_urls(
            db=db,
            start_urls=start_urls,
            patterns=patterns,
            check_ssrf=check_ssrf,
        )

        # 3. Cleanup stalled processing
        await _cleanup_processing(
            db=db,
            intervals=intervals,
            processing_timeout_sec=processing_timeout_sec,
        )

        claimed_records = await _claim_pages(db=db, limit=n_claims)
        if not claimed_records:
            return

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=pw_viewport,
            user_agent=pw_headers.get("User-Agent"),
            extra_http_headers=pw_headers,
        )
        
        semaphore = asyncio.Semaphore(n_concurrent)
        
        # Use asyncio.gather for the batch
        tasks = [
            asyncio.create_task(
                _process_page(
                    record=record,
                    sqlite_path=sqlite_path,
                    context=context,
                    semaphore=semaphore,
                    robots=robots,
                    patterns=patterns,
                    check_ssrf=check_ssrf,
                    max_file_size=max_file_size,
                    pw_scroll_rounds=pw_scroll_rounds,
                    pw_scroll_timeout_ms=pw_scroll_timeout_ms,
                    pw_scroll_selector=pw_scroll_selector,
                    pw_timeout_ms=pw_timeout_ms,
                    pw_block_resources=pw_block_resources,
                    page_ready_hook=page_ready_hook,
                    link_extract_hook=link_extract_hook,
                    content_extract_hook=content_extract_hook,
                    downstream_hook=downstream_hook,
                    intervals=intervals,
                    error_threshold=error_threshold,
                )
            )
            for record in claimed_records
        ]
        await asyncio.gather(*tasks)
        
        await context.close()
        await browser.close()


def normalize_and_validate_url(
    url: str,
    base_url: str | None,
    patterns: tuple[list[dict[str, str]] | None, list[str] | None, list[str] | None],
) -> str | None:
    """Normalize and validate a URL."""
    normalize_patterns, include_patterns, exclude_patterns = patterns
    try:
        candidate = url.strip()
        base = base_url.strip() if base_url else None

        if base and not urlparse(candidate).scheme:
            candidate = urljoin(base, candidate)

        parsed = urlparse(candidate)
        if not parsed.scheme:
            return None

        scheme = parsed.scheme.lower()
        if scheme not in {"http", "https"}:
            return None

        hostname = parsed.hostname or ""
        port = parsed.port
        if port in (80, 443):
            netloc = hostname
        else:
            netloc = parsed.netloc

        path = parsed.path or "/"
        normalized = urlunparse((scheme, netloc, path, parsed.params, parsed.query, ""))

        if normalize_patterns:
            for pattern in normalize_patterns:
                pattern_value = pattern.get("pattern")
                replace_value = pattern.get("replace", "")
                if pattern_value is None:
                    continue
                normalized = re.sub(pattern_value, replace_value, normalized)

        # Re-parse to ensure integrity after regex
        parsed_normalized = urlparse(normalized)
        final_scheme = parsed_normalized.scheme.lower()
        
        if final_scheme not in {"http", "https"} or not parsed_normalized.netloc:
            return None

        normalized = urlunparse(
            (
                final_scheme,
                parsed_normalized.netloc,
                parsed_normalized.path or "/",
                parsed_normalized.params,
                parsed_normalized.query,
                "",
            )
        )

        if include_patterns and not any(re.search(pattern, normalized) for pattern in include_patterns):
            return None

        if exclude_patterns and any(re.search(pattern, normalized) for pattern in exclude_patterns):
            return None

        return normalized
    except Exception:
        return None


async def _is_safe_url(url: str) -> bool:
    """Prevents SSRF by checking for private IP addresses (async, with hostname cache)."""
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False

        # Check cache first
        cached = _SSRF_SAFE_CACHE.get(hostname)
        if cached is not None:
            return cached

        # If it looks like an IP literal, check it directly
        try:
            ip = ipaddress.ip_address(hostname)
            safe = not (ip.is_private or ip.is_loopback or ip.is_link_local)
            _SSRF_SAFE_CACHE[hostname] = safe
            return safe
        except ValueError:
            # Domain name: need DNS resolution (do it via the event loop, not blocking)
            loop = asyncio.get_running_loop()
            try:
                # This is already executed in a thread pool under the hood
                addr_info = await loop.getaddrinfo(hostname, None)
            except socket.gaierror:
                _SSRF_SAFE_CACHE[hostname] = False
                return False  # DNS failure -> unsafe/unusable

            safe = True
            for _, _, _, _, sockaddr in addr_info:
                ip_str = sockaddr[0]
                ip = ipaddress.ip_address(ip_str)
                if ip.is_private or ip.is_loopback or ip.is_link_local:
                    safe = False
                    break

            _SSRF_SAFE_CACHE[hostname] = safe
            return safe

    except Exception:
        # Any parsing/lookup weirdness => treat as unsafe
        return False


async def _process_page(
    record: PageRecord,
    sqlite_path: str,
    context: BrowserContext,
    semaphore: asyncio.Semaphore,
    **kwargs,
) -> None:
    try:
        # Open distinct connection per task for transaction isolation
        async with aiosqlite.connect(sqlite_path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA journal_mode=WAL;")
            async with semaphore:
                await _process_page_inner(record=record, db=db, context=context, **kwargs)
    except Exception:
        logger.exception(f"Worker crashed on {record.norm_url}")


async def _process_page_inner(
    record: PageRecord,
    db: aiosqlite.Connection,
    context: BrowserContext,
    robots: RobotsGatekeeper | None,
    patterns: tuple[list[dict[str, str]] | None, list[str] | None, list[str] | None],
    check_ssrf: bool,
    max_file_size: int,
    pw_scroll_rounds: int,
    pw_scroll_timeout_ms: int,
    pw_scroll_selector: str,
    pw_timeout_ms: int,
    pw_block_resources: set[str],
    page_ready_hook: PageReadyHook,
    link_extract_hook: LinkExtractHook,
    content_extract_hook: ContentExtractHook,
    downstream_hook: DownstreamHook,
    intervals: tuple[int, int, int, float, float],
    error_threshold: int,
) -> None:

    # convenience
    norm_url = record.norm_url

    # Pre-flight Validation
    normalized = normalize_and_validate_url(
        url=norm_url,
        base_url=None,
        patterns=patterns
    )
    
    # Handle Normalization Change
    if normalized != norm_url:
        # Delete old
        await downstream_hook(norm_url, None, None, None, None, False, "Invalid URL")
        await _delete_page_record(db, norm_url)
        # If Normalization -> Invalid
        if normalized is None:
            return
        # Ensure New Normalized URL
        record = await _ensure_page_record(db, normalized, claim_if_free=True)
        if not record:
            # The target URL is already processing by another worker.
            return
        norm_url = record.norm_url

    # Security: SSRF
    if check_ssrf and not await _is_safe_url(norm_url):
        # Delete old
        await downstream_hook(norm_url, None, None, None, None, False, "Unsafe URL")
        await _delete_page_record(db, norm_url)
        return

    # Robots.txt Check
    if robots:
        can_fetch = await robots.can_fetch(norm_url)
        if not can_fetch:
            # Back off
            await downstream_hook(norm_url, None, None, None, None, False, "Blocked by robots.txt")
            await _end_process(db, record, content_hash="", is_fresh=False, error_count=None, intervals=intervals)
            return

    # Create the page
    page = await context.new_page()

    try:
        # Set timeframe
        page.set_default_timeout(pw_timeout_ms)

        # Configure resource blocking
        if pw_block_resources:
            async def _route_handler(route: Route) -> None:
                if route.request.resource_type in pw_block_resources:
                    await route.abort()
                else:
                    await route.continue_()
            await page.route("**/*", _route_handler)

        # Navigation
        response = await _goto(page, norm_url)
        
        # Check for succes, end if not
        if response is None or not (200 <= response.status < 300):
            error_count = record.error_count + 1
            if error_count < error_threshold:
                # Soft error - reschedule without downstream
                await _end_process(db, record, content_hash=None, is_fresh=False,
                                   error_count=error_count, intervals=intervals)
                return
            # Hard error - proceed to finalize with None content
            await downstream_hook(norm_url, response, page, None, None, False, "Response error")
            await _end_process(db, record, content_hash="", is_fresh=False, error_count=error_count, intervals=intervals)
            return

        # Check Redirects
        redirect_normalized = normalize_and_validate_url(
            url=response.url if isinstance(response, DownloadResponseAdapter) else page.url,
            base_url=None,
            patterns=patterns
        )

        if redirect_normalized != norm_url:
            # Finalize source as stub
            await downstream_hook(norm_url, response, page, None, None, False, "Redirected")
            await _end_process(db, record, content_hash="", is_fresh=False, error_count=0, intervals=intervals)
            if not redirect_normalized or (check_ssrf and not await _is_safe_url(redirect_normalized)):
                # Invalid redirect target
                return

            # Switch context to new URL
            record = await _ensure_page_record(db, redirect_normalized, claim_if_free=True)
            if not record:
                # Target busy, abort
                return
            norm_url = record.norm_url

            # Redirect Robots.txt Check
            if robots:
                can_fetch = await robots.can_fetch(norm_url)
                if not can_fetch:
                    # Back off
                    await downstream_hook(norm_url, None, None, None, None, False, "Blocked by robots.txt")
                    await _end_process(db, record, content_hash="", is_fresh=False, error_count=0, intervals=intervals)
                    return

        # Check size before we move data from Browser
        try:
            content_length = int(response.headers.get("content-length", 0))
        except Exception:
            content_length = 0
        if content_length > max_file_size:
            logger.warning(f"Skipping {norm_url}: Max file size exceeded ({content_length} bytes)")
            await downstream_hook(norm_url, response, page, None, None, False, "Max file size exceeded")
            await _end_process(db, record, content_hash="", is_fresh=False, error_count=None, intervals=intervals)
            return

        # Establish content type
        extension = await _guess_extension(response)

        # Perform interactions on HTML pages
        if extension == "html":
            # Scroll
            if pw_scroll_rounds > 0:
                await _perform_scrolls(page, pw_scroll_rounds, pw_scroll_timeout_ms, pw_scroll_selector)
            # Apply custom page interaction
            await page_ready_hook(norm_url, response, page)

        # Link discovery
        found_links = await link_extract_hook(norm_url, response, page, extension)

        # Insert and count actual new links
        new_links_found = await _batch_insert_links(
            db=db,
            source_url=norm_url,
            raw_links=found_links,
            patterns=patterns,
            check_ssrf=check_ssrf
        )

        # Handle payload
        content = await content_extract_hook(norm_url, response, page, extension)

        # Generate hash
        if content is not None:
            content_hash = _compute_stable_hash(content)
        else:
            content_hash = ""
            
        content_changed = (content is not None) and (record.content_hash != content_hash)

        # Establish page freshness
        is_fresh = new_links_found or content_changed

        # finalize
        await downstream_hook(norm_url, response, page, extension, content, is_fresh, "Success")
        await _end_process(db, record, content_hash=content_hash, is_fresh=is_fresh, error_count=0, intervals=intervals)

    finally:

        # Always close page
        await page.close()


async def _batch_insert_links(
    db: aiosqlite.Connection,
    source_url: str,
    raw_links: list[str],
    patterns: tuple[list[dict[str, str]] | None, list[str] | None, list[str] | None],
    check_ssrf: bool,
) -> bool:
    """Batch inserts/updates found links to avoid N+1 queries."""
    normalize_patterns, include_patterns, exclude_patterns = patterns
    valid_urls = set()
    for raw in raw_links:
        normalized = normalize_and_validate_url(
            url=raw,
            base_url=source_url,
            patterns=patterns
        )
        try:
            if normalized and (not check_ssrf or await _is_safe_url(normalized)):
                valid_urls.add(normalized)
        except Exception:
            pass
            
    if not valid_urls:
        return False
    
    valid_urls = list(valid_urls)
    existing_count = 0

    # Batch check for fresh links before inserting
    for i in range(0, len(valid_urls), 500):
        chunk = valid_urls[i:i+500]
        placeholders = ",".join("?" for _ in chunk)
        cursor = await db.execute(
            f"SELECT COUNT(*) FROM pages WHERE norm_url IN ({placeholders})",
            chunk,
        )
        (chunk_count,) = await cursor.fetchone()
        existing_count += chunk_count

    fresh_links = existing_count < len(valid_urls)

    # Batch insert new
    cursor = await db.executemany(
        """
        INSERT OR IGNORE INTO pages(
            norm_url, first_seen_time, last_inlink_seen_time,
            last_crawl_time, next_crawl_time, processing_time
        )
        VALUES (?, unixepoch(), unixepoch(), NULL, NULL, NULL)
        """,
        [(url,) for url in valid_urls]
    )
    
    # Batch update existing (retention)
    for i in range(0, len(valid_urls), 500):
        chunk = valid_urls[i:i+500]
        await db.execute(
            f"UPDATE pages SET last_inlink_seen_time = unixepoch() WHERE norm_url IN ({','.join('?' for _ in chunk)})",
            chunk
        )
    
    await db.commit()

    return fresh_links


async def _end_process(
    db: aiosqlite.Connection,
    record: PageRecord,
    content_hash: str | None,
    is_fresh: bool,
    error_count: int | None,
    intervals: tuple[int, int, int, float, float],
) -> None:
    """
    Upsert the page after processing.
    """
    next_interval = _calculate_next_interval(
        record=record,
        is_fresh=is_fresh,
        intervals=intervals
    )
    error_count = error_count if error_count is not None else record.error_count
    content_hash = content_hash if content_hash is not None else record.content_hash
    await db.execute(
        """
        INSERT INTO pages(
            norm_url, first_seen_time, last_inlink_seen_time, 
            last_crawl_time, next_crawl_time, processing_time, error_count, content_hash
        )
        VALUES (?, unixepoch(), unixepoch(), unixepoch(), unixepoch() + ?, NULL, ?, ?)
        ON CONFLICT(norm_url) DO UPDATE SET
            last_crawl_time = excluded.last_crawl_time,
            next_crawl_time = excluded.next_crawl_time,
            processing_time = NULL,
            error_count = excluded.error_count,
            content_hash = excluded.content_hash;
        """,
        (record.norm_url, next_interval, error_count, content_hash),
    )
    await db.commit()


def _wrap_hook(hook: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """
    Wraps a hook in an error logging block.
    """
    async def wrapped(*args, **kwargs) -> Any:
        try:
            return await hook(*args, **kwargs)
        except Exception as exc:
            norm_url = args[0] if args else "<unknown>"
            logger.error(
                "%s error for %s: %s",
                getattr(hook, "__name__", repr(hook)),
                norm_url,
                exc,
            )
    return wrapped


async def _delete_page_record(db: aiosqlite.Connection, norm_url: str) -> None:
    """
    Deletes a single page record.
    """
    await db.execute("DELETE FROM pages WHERE norm_url = ?", (norm_url,))
    await db.commit()


async def _ensure_page_record(
    db: aiosqlite.Connection, norm_url: str, claim_if_free: bool
) -> PageRecord | None:
    """
    Ensures a record exists. 
    If claim_if_free is True, attempts to lock it (processing_time=now).
    Returns None if the record exists but is ALREADY locked by another worker.
    """
    # 1. Ensure existence
    await db.execute(
        """
        INSERT OR IGNORE INTO pages(
            norm_url, first_seen_time, last_inlink_seen_time
        )
        VALUES (?, unixepoch(), unixepoch())
        """,
        (norm_url,),
    )
    await db.commit()

    if claim_if_free:
        # 2. Attempt to claim ONLY if processing_time is NULL
        cursor = await db.execute(
            """
            UPDATE pages 
            SET processing_time = unixepoch() 
            WHERE norm_url = ? AND processing_time IS NULL
            """,
            (norm_url,)
        )
        if cursor.rowcount == 0:
            await db.commit()
            # It was already locked by someone else, or didn't exist (handled by insert)
            # Check if it's locked
            async with db.execute("SELECT processing_time FROM pages WHERE norm_url = ?", (norm_url,)) as cur:
                row = await cur.fetchone()
                if row and row["processing_time"] is not None:
                    return None # Busy
        await db.commit()

    # 3. Fetch
    query = """
    SELECT norm_url, first_seen_time, last_inlink_seen_time, 
           last_crawl_time, next_crawl_time, error_count, content_hash
    FROM pages WHERE norm_url = ?
    """
    cursor = await db.execute(query, (norm_url,))
    row = await cursor.fetchone()
    
    if not row:
        return None

    return PageRecord(
        norm_url=row["norm_url"],
        first_seen_time=row["first_seen_time"],
        last_inlink_seen_time=row["last_inlink_seen_time"],
        last_crawl_time=row["last_crawl_time"],
        next_crawl_time=row["next_crawl_time"],
        error_count=row["error_count"],
        content_hash=row["content_hash"],
    )


def _validate_intervals(**kwargs) -> None:
    if kwargs["min_interval_sec"] <= 0:
        raise ValueError("min_interval_sec must be > 0")
    if kwargs["max_interval_sec"] < kwargs["min_interval_sec"]:
        raise ValueError("max_interval_sec must be >= min_interval_sec")
    if kwargs["fresh_factor"] > 1.0:
        raise ValueError("fresh_factor must be <= 1.0")
    if kwargs["stale_factor"] < 1.0:
        raise ValueError("stale_factor must be >= 1.0")


async def _create_schema(db: aiosqlite.Connection) -> None:
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS pages (
          norm_url              TEXT PRIMARY KEY,
          first_seen_time       INTEGER NOT NULL,
          last_inlink_seen_time INTEGER NOT NULL,
          last_crawl_time       INTEGER NULL,
          next_crawl_time       INTEGER NULL,
          processing_time       INTEGER NULL,
          error_count           INTEGER NOT NULL DEFAULT 0,
          content_hash          TEXT NOT NULL DEFAULT ''
        );
        """
    )
    await db.execute("CREATE INDEX IF NOT EXISTS idx_pages_last_inlink_seen ON pages(last_inlink_seen_time);")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_pages_next_crawl ON pages(next_crawl_time);")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_pages_processing ON pages(processing_time);")
    await db.commit()


async def _cleanup_retention(db: aiosqlite.Connection, retention_sec: int) -> None:
    cutoff = int(time.time()) - retention_sec
    await db.execute("DELETE FROM pages WHERE last_inlink_seen_time < ?", (cutoff,))
    await db.commit()


async def _bootstrap_start_urls(
    db: aiosqlite.Connection,
    start_urls: list[str],
    patterns: tuple[list[dict[str, str]] | None, list[str] | None, list[str] | None],
    check_ssrf: bool,
) -> None:

    normalize_patterns, include_patterns, exclude_patterns = patterns

    valid_starts = []
    for raw in start_urls:
        norm = normalize_and_validate_url(raw, None, patterns)
        if norm and (not check_ssrf or await _is_safe_url(norm)):
            valid_starts.append(norm)

    if not valid_starts:
        return

    await db.executemany(
        """
        INSERT INTO pages(
            norm_url, first_seen_time, last_inlink_seen_time
        )
        VALUES (?, unixepoch(), unixepoch())
        ON CONFLICT(norm_url) DO UPDATE SET
            last_inlink_seen_time = unixepoch()
        """,
        [(url,) for url in valid_starts]
    )
    await db.commit()


async def _cleanup_processing(
    db: aiosqlite.Connection,
    intervals: tuple[int, int, int, float, float],
    processing_timeout_sec: int,
) -> None:

    new_interval_sec, min_interval_sec, max_interval_sec, fresh_factor, stale_factor = intervals

    cutoff = int(time.time()) - processing_timeout_sec
    # We select timed-out rows
    cursor = await db.execute(
        """
        SELECT norm_url, last_crawl_time, next_crawl_time
        FROM pages
        WHERE processing_time IS NOT NULL AND processing_time < ?
        """,
        (cutoff,),
    )
    rows = await cursor.fetchall()
    
    # We can batch update these too, but logic requires calculating interval per row.
    # Given recovery is rare, loop is acceptable here.
    for row in rows:
        last_crawl = row["last_crawl_time"]
        next_crawl = row["next_crawl_time"]
        
        prev_interval = (next_crawl - last_crawl) if (last_crawl and next_crawl) else new_interval_sec
        next_interval_val = min(int(prev_interval * stale_factor), max_interval_sec)
        
        await db.execute(
            """
            UPDATE pages
            SET processing_time = NULL,
                next_crawl_time = unixepoch() + ?
            WHERE norm_url = ?
            """,
            (next_interval_val, row["norm_url"]),
        )
    await db.commit()


async def _claim_pages(db: aiosqlite.Connection, limit: int) -> list[PageRecord]:
    await db.execute("BEGIN IMMEDIATE;")
    cursor = await db.execute(
        """
        SELECT norm_url, first_seen_time, last_inlink_seen_time, 
               last_crawl_time, next_crawl_time, error_count, content_hash
        FROM pages
        WHERE (next_crawl_time IS NULL OR next_crawl_time <= unixepoch())
          AND processing_time IS NULL
        ORDER BY next_crawl_time IS NULL DESC, next_crawl_time ASC
        LIMIT ?
        """,
        (limit,),
    )
    rows = await cursor.fetchall()
    records = [
        PageRecord(
            norm_url=row["norm_url"],
            first_seen_time=row["first_seen_time"],
            last_inlink_seen_time=row["last_inlink_seen_time"],
            last_crawl_time=row["last_crawl_time"],
            next_crawl_time=row["next_crawl_time"],
            error_count=row["error_count"],
            content_hash=row["content_hash"],
        )
        for row in rows
    ]
    if records:
        placeholders = ",".join("?" for _ in records)
        await db.execute(
            f"UPDATE pages SET processing_time = unixepoch() WHERE norm_url IN ({placeholders})",
            [record.norm_url for record in records],
        )
    await db.commit()
    return records


async def _goto(page: Page, url: str) -> Response | None:
    """
    Robust navigation that handles standard pages AND forced downloads (PDFs/ZIPs).
    If page.goto crashes due to a download, it captures the file and returns an adapter.
    """
    downloads: list[Any] = []
    download_event = asyncio.Event()

    # Attach listener before navigation
    def _on_download(d):
        downloads.append(d)
        download_event.set()
    page.on("download", _on_download)

    try:
        # Normal navigation
        return await page.goto(url)
        
    except Exception as exc:
        # Test if a download event caused the exception.
        try:
            await asyncio.wait_for(download_event.wait(), timeout=0.1)
        except TimeoutError:
            pass  # No download event came, it was a real error
        
        if downloads:
            # It was a download!
            download = downloads[-1]
            try:
                path = await download.path()
                if path:
                    return DownloadResponseAdapter(download, path)
            except Exception as e:
                logger.warning(f"Download succeeded but file save failed for {url}: {e}")
                return None
        
        # It was a real error (Timeout, DNS, etc.)
        logger.warning(f"Failed to navigate to {url}: {exc}")

    finally:
        # Avoid accumulating handlers on the same page
        try:
            page.off("download", _on_download)
        except Exception:
            pass

    return None


async def _guess_extension(response):
    """
    Downloads body (if safe), checks magic bytes, and returns extension.
    Bytes are checked first to minimize risk of binary sent with
    text/html content-type header.
    """
    # 1. Load bytes
    try:
        body_bytes = await response.body()
    except Exception:
        return ""

    # 2. Magic bytes check
    kind = filetype.guess(body_bytes)
    if kind:
        return kind.extension

    # 3. Header fallback
    mime_type = response.headers.get("content-type", "").lower().split(';')[0].strip()

    # Return extension
    return MIME_MAP.get(mime_type) or ""


def _compute_stable_hash(payload: Any) -> str:
    if payload is None:
        data = b""
    elif isinstance(payload, bytes):
        data = payload
    elif isinstance(payload, str):
        data = payload.encode("utf-8")
    else:
        try:
            data = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        except Exception:
            data = str(payload).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _calculate_next_interval(
    *,
    record: PageRecord,
    is_fresh: bool,
    intervals: tuple[int, int, int, float, float],
) -> int:
    """
    Calculate and return interval to next crawl in seconds.
    """
    new_interval_sec, min_interval_sec, max_interval_sec, fresh_factor, stale_factor = intervals
    if record.last_crawl_time is None or record.next_crawl_time is None:
        return new_interval_sec
    prev_interval = record.next_crawl_time - record.last_crawl_time
    if is_fresh:
        return int(max(prev_interval * fresh_factor, min_interval_sec))
    return int(min(prev_interval * stale_factor, max_interval_sec))


async def _perform_scrolls(page: Page, rounds: int, max_wait_ms: int, selector: str = "body") -> None:
    # 1. Quick check if element exists
    try:
        if await page.locator(selector).count() == 0:
            return
    except Exception:
        return

    # 2. Get initial height
    try:
        previous_height = await page.evaluate(
            "(sel) => { const el = document.querySelector(sel); return el ? el.scrollHeight : 0; }",
            selector,
        )
    except Exception:
        return

    for _ in range(max(rounds, 0)):
        try:
            # --- STEP A: AIM THE MOUSE ---
            # Force hover to ensure the wheel event targets the correct container
            await page.locator(selector).first.hover(force=True)

            # --- STEP B: CALCULATE DISTANCE ---
            delta_needed = await page.evaluate(
                """(sel) => {
                    const el = document.querySelector(sel);
                    if (!el) return 0;

                    // Treat both BODY and HTML as the 'Global Window' scroll
                    const isGlobal = el.tagName === 'BODY' || el.tagName === 'HTML';
                    
                    const currentScroll = isGlobal ? window.scrollY : el.scrollTop;
                    const clientHeight = isGlobal ? window.innerHeight : el.clientHeight;

                    // Distance to bottom + buffer
                    return el.scrollHeight - currentScroll - clientHeight + 1000;
                }""",
                selector,
            )

            # If we are already effectively at the bottom, stop.
            # We allow a small buffer (e.g., < 50px) because calculations aren't always pixel-perfect.
            if delta_needed < 50:
                break

            # --- STEP C: FLING ---
            await page.mouse.wheel(0, int(delta_needed))

            # --- STEP D: SMART WAIT ---
            try:
                await page.wait_for_function(
                    """([sel, prev]) => {
                        const el = document.querySelector(sel);
                        if (!el) return false;
                        return el.scrollHeight > prev;
                    }""",
                    [selector, previous_height],
                    timeout=max_wait_ms,
                    polling=200, # Low CPU usage
                )
            except PlaywrightTimeoutError:
                break

            # Update height for next round
            previous_height = await page.evaluate(
                "(sel) => { const el = document.querySelector(sel); return el ? el.scrollHeight : 0; }",
                selector,
            )

        except Exception:
            # If anything crashes (locator triggers, browser disconnected), stop the loop.
            break


# --- Default Hooks ---

async def _page_ready_hook(
    url: str,
    response: Response,
    page: Page
) -> None:
    """
    Default page interaction is nothing.
    """
    pass


async def _link_extract_hook(
    url: str,
    response: Response,
    page: Page,
    extension: str
) -> list[str]:
    """
    Extracts raw links from HTML bytes using lxml with recovery.
    """
    # Sanity check
    if extension != "html" or page is None:
        return []
    # Using DOM state to include dynamically generated links
    try:
        parser = html.HTMLParser(recover=True)
        content = (await page.content()).encode("utf-8")
        document = html.fromstring(content, parser=parser)
    except Exception:
        return []
    # Three types of HTML attributes are considered links
    hrefs = [e.get("href") for e in document.xpath("//a[@href]") if e.get("href")]
    actions = [e.get("action") for e in document.xpath("//form[@action]") if e.get("action")]
    frames = [e.get("src") for e in document.xpath("//iframe[@src]") if e.get("src")]
    return hrefs + actions + frames


async def _content_extract_hook(
    url: str,
    response: Response,
    page: Page,
    extension: str
) -> Any:
    """
    Returns DOM state as bytes for HTML, else raw bytes.
    """
    # DOM state for HTML, else bytes
    if extension == 'html' and page is not None:
        try:
            return (await page.content()).encode("utf-8")
        except Exception:
            pass
    try:
        return await response.body()
    except Exception:
        return None


async def _downstream_hook(
    url: str,
    response: Response | None,
    page: Page | None,
    extension: str | None,
    content: Any,
    is_fresh: bool,
    message: str
) -> None:
    """
    Default downstream action is nothing.
    """
    pass


__all__ = ["litecrawl", "litecrawl_async", "normalize_and_validate_url"]
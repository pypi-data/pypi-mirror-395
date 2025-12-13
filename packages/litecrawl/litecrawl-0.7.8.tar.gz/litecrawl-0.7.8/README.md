# litecrawl

`litecrawl` is a minimal, asynchronous web crawler designed for targeted data acquisition. It sits in the operational middle ground: more robust than a simple loop of `requests.get()`, but significantly lighter and easier to manage than heavy, distributed crawling clusters (like Scrapy Cluster).

It is designed as a **tool, not a system**. It exposes a single, idempotent function that manages its own state via SQLite. It is intended to be invoked periodically (e.g., via cron) to incrementally build and maintain a dataset.

## Design Philosophy

The architecture follows a "crash-only" software philosophy. It assumes the process will eventually terminate—whether by completion, error, or an external timeout—and ensures that the state remains consistent for the next run.

1.  **State Persistence:** All crawl state (URLs, schedules, content hashes, error counts) is stored in a local SQLite database (WAL mode). This allows the crawler to be stopped and restarted at any time without data loss.
2.  **Transaction Isolation:** Each worker task maintains its own database connection, ensuring that partial crawls or crashes in one tab do not corrupt the shared state.
3.  **Adaptive Scheduling:** Unlike simple scrapers that hit every URL on every run, `litecrawl` calculates a `next_crawl_time` for each page. It uses `fresh_factor` and `stale_factor` multipliers to revisit frequently changing pages often and stable pages rarely.
4.  **SSRF & Robot Safety:** Built-in safeguards against Server-Side Request Forgery (private IP blocking) and a thread-safe, debounced `robots.txt` parser that prevents request flooding.

## Installation

Requires Python 3.12+, Playwright, and filetype.

```bash
# Recommended (uv)
uv add litecrawl
uv run playwright install chromium

# Or pip
pip install litecrawl
python -m playwright install chromium
```

## Quick Start

Create a Python script (e.g., `crawler.py`) that calls the entry point. The function will initialize the database schema automatically.

```python
from litecrawl import litecrawl

# Define your configuration
litecrawl(
    sqlite_path="company_news.db",
    start_urls=["https://example.com/news"],
    
    # Only follow links matching these patterns
    include_patterns=[r"https://example\.com/news/.*"],
    
    # Normalize URLs to avoid duplicates (e.g., strip tracking params)
    normalize_patterns=[{"pattern": r"\?utm_source=.*", "replace": ""}],
    
    # Operational settings
    n_concurrent=5,      # Parallel tabs
    n_claims=100,        # Pages to process per run
    fresh_factor=0.5,    # Re-crawl rapidly if content changes
    stale_factor=2.0     # Back off if content is static
)
```

### Deployment via Cron

To run the crawler continuously, set up a cron job. We wrap the execution in `timeout` to handle potential browser hangs or memory leaks gracefully at the OS level.

```bash
# Run every minute. Kills the process if it exceeds 10 minutes.
* * * * * cd /path/to/project && /usr/bin/timeout 10m uv run python crawler.py >> /var/log/crawl.log 2>&1
```

## Configuration Reference

`litecrawl` is configured entirely through arguments passed to the main function.

### Targeting & Discovery
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `sqlite_path` | `str` | Path to the SQLite DB. Created automatically if missing. |
| `start_urls` | `list[str]` | Entry points. Always re-injected on every run to ensure the root is alive. |
| `include_patterns` | `list[str]` | Regex list. Only links matching these are added to the DB. |
| `exclude_patterns` | `list[str]` | Regex list. Links matching these are ignored. |
| `normalize_patterns` | `list[dict]` | Regex replacements (`{"pattern": "...", "replace": "..."}`) applied to URLs before storage. |
| `check_robots_txt` | `bool` | If `True` (default), respects robots.txt rules (cached & debounced). |
| `check_ssrf` | `bool` | If `True` (default), prevents connections to private/local IP addresses. |
| `max_file_size` | `int` | Max content-length in bytes before aborting (default: 50MB). |

### Scheduling & Operations
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `n_claims` | `int` | Maximum number of pages to process in one execution. |
| `n_concurrent` | `int` | Number of parallel browser tabs. |
| `fresh_factor` | `float` | Multiplier (< 1.0) to reduce interval if content changes. |
| `stale_factor` | `float` | Multiplier (> 1.0) to increase interval if content is static. |
| `new_interval_sec` | `int` | Initial crawl interval for newly discovered pages (default: 24h). |
| `min_interval_sec` | `int` | Minimum time between crawls (floor). |
| `max_interval_sec` | `int` | Maximum time between crawls (ceiling). |
| `inlink_retention_sec`| `int` | Prune pages not seen in links for this duration (default: 31 days). |
| `error_threshold` | `int` | Max consecutive errors before giving up on a page (default: 3). |
| `processing_timeout_sec`| `int` | Safety timeout to unlock stuck pages (default: 10 mins). |

### Browser Control
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `pw_headers` | `dict` | HTTP headers (e.g., User-Agent, Cookies). |
| `pw_viewport` | `dict` | Viewport size (default: 4k vertical). |
| `pw_block_resources` | `set` | Resource types to abort (default: `{"image", "font", "media"}`). |
| `pw_scroll_rounds` | `int` | How many times to scroll to bottom before extracting (for infinite scroll). |
| `pw_scroll_selector` | `str` | CSS selector to target for scrolling (default: `"body"`). |
| `pw_scroll_timeout_ms`| `int` | Wait time between scroll events to allow content loading. |
| `pw_timeout_ms` | `int` | Page load timeout in milliseconds. |

### Hooks (Async Callables)
| Parameter | Description |
| :--- | :--- |
| `page_ready_hook` | Called after navigation/scroll but before extraction. Used for clicks or logins. |
| `link_extract_hook` | Overrides default logic. Returns a list of URLs to add to the frontier. |
| `content_extract_hook` | Extracts the specific data/payload to be hashed and stored. |
| `downstream_hook` | Called at the end of processing. Used to export data (e.g., to API/S3). |

## Advanced Usage

Even when using the synchronous `litecrawl` wrapper, **all hooks must be `async` functions**.

### 1. Structured Data & Change Detection

`litecrawl` determines if a page is "fresh" by hashing the return value of your `content_extract_hook`.
*   If you return a **Dictionary**, the crawler automatically sorts the keys and dumps it to JSON before hashing. This ensures deterministic hashes.
*   **Crucial:** Do not include timestamps, random numbers, or ad-rotation IDs in your returned dictionary. These will cause the hash to change on every run, tricking the scheduler into thinking the content is always "fresh."

```python
async def structured_extract(url, response, page, extension):
    """
    Extracts metadata. Returns a dict.
    """
    return {
        "title": await page.title(),
        "price": await page.locator(".price").inner_text(),
        # "scraped_at": time.time()  <-- WRONG! This breaks change detection.
    }

litecrawl(..., content_extract_hook=structured_extract)
```

### 2. The Downstream Hook (Export)

This is where data leaves the crawler. It is called *immediately* after the database is updated. The `message` argument provides context (e.g., "Success", "Redirected", "Blocked by robots.txt", "Response error").

**Note:** Because this hook is also used for error reporting, `response`, `page`, and `content` may be `None`.

```python
async def push_to_api(url, response, page, extension, content, is_fresh, message):
    """
    content: The result from your content_extract_hook (e.g., the dict above)
    is_fresh: True if content hash changed OR new links were found.
    message: Status string.
    """
    # Only push successful, fresh data
    if message == "Success" and is_fresh and content:
        payload = {
            "url": url,
            "data": content, 
            "crawled_at": time.time() # Add timestamps HERE, not in extraction
        }
        await my_api_client.post("/ingest", json=payload)
    
    elif message == "Response error":
        print(f"Failed to fetch {url} - Status: {response.status if response else 'Unknown'}")

litecrawl(..., downstream_hook=push_to_api)
```

### 3. Custom Interaction (Login/Cookies)

Use `page_ready_hook` to interact with the page before links or content are touched.

```python
async def handle_popups(url, response, page):
    # Click generic "Accept Cookies" buttons
    try:
        await page.click("#accept-cookies-btn", timeout=2000)
    except:
        pass
        
    # Wait for a specific element to ensure dynamic content loaded
    await page.wait_for_selector(".dynamic-content")

litecrawl(..., page_ready_hook=handle_popups)
```

## Operational Best Practices

1.  **Partitioning:** If you need to crawl 10 distinct websites, it is better to set up 10 separate cron entries with 10 separate SQLite files rather than one massive monolithic crawl. This isolates failures and simplifies configuration.
2.  **Concurrency:** Keep `n_concurrent` moderate (5-20). While SQLite WAL mode handles concurrency well, extremely high contention from hundreds of workers on a single file can degrade performance.
3.  **Backups:** The `sqlite_path` file contains your entire crawl state (frontier, history, hashes). Back it up regularly.
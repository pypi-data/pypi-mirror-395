# Mobbin Crawler

A reliable and resumable crawler for extracting app flows and screens from Mobbin.com.

## Overview

This crawler extracts design inspiration data from Mobbin in three phases:

1. **Phase 0 (seed.py)**: Crawl iOS and Web app listings to generate `apps_seed.json`
2. **Phase 1 (index.py)**: For each app, crawl flows and screens, saving to `screens.json`
3. **Catalog (catalog.py)**: Generate aggregated `catalog.json` from collected screens

## Features

- ✅ **Resumable**: Tracks completed apps, can restart from where it left off
- ✅ **Fallback Support**: Handles apps without flows (screens-only mode)
- ✅ **Deduplication**: Prevents duplicate screens
- ✅ **Rate Limiting**: Random delays between requests
- ✅ **Resource Blocking**: Skips images/fonts/media for faster crawling
- ✅ **Retry Logic**: Retries failed apps up to 2 times
- ✅ **Progress Saving**: Saves progress every 10 apps

## Project Structure

```
src/
  tools/
    mobbin_crawl/
      run.py          # Main entry point
      seed.py         # Phase 0: Generate apps seed
      index.py        # Phase 1: Crawl flows & screens
      catalog.py      # Generate catalog
      utils.py        # Utility functions
  data/
    apps_seed.json    # Output: All apps (platform, name, URL)
    screens.json      # Output: All screens (platform, app, flow?, screen_url)
    apps_done.json    # State: Completed apps
    catalog.json      # Output: Aggregated catalog (apps & flows)
```

## Requirements

```bash
pip install playwright
playwright install chromium
```

## Usage

### Run Complete Pipeline

```bash
cd src/tools/mobbin_crawl
python run.py
```

This runs all three phases sequentially.

### Run Individual Phases

```bash
# Phase 0: Generate apps seed
python seed.py

# Phase 1: Crawl flows & screens
python index.py

# Generate catalog
python catalog.py
```

## Output Data Formats

### apps_seed.json

```json
[
  {
    "platform": "Mobile",
    "app": "Google Gemini",
    "app_page_url": "https://mobbin.com/apps/...",
    "discovered_at": "2025-10-27T12:00:00Z"
  }
]
```

### screens.json

With flows:
```json
{
  "platform": "Mobile",
  "app": "Google Gemini",
  "flow": "Onboarding",
  "screen_url": "https://cdn.mobbin.com/.../1.webp",
  "dataset_version": "2025.10"
}
```

Without flows (fallback):
```json
{
  "platform": "Mobile",
  "app": "Google Chrome",
  "screen_url": "https://cdn.mobbin.com/.../1.webp",
  "dataset_version": "2025.10"
}
```

### catalog.json

```json
{
  "apps": [
    {
      "platform": "Mobile",
      "app": "Google Gemini",
      "has_flows": true,
      "screens_count": 42
    }
  ],
  "flows": [
    {
      "platform": "Mobile",
      "app": "Google Gemini",
      "flow": "Onboarding",
      "screens_count": 8
    }
  ]
}
```

## Configuration

### Credentials

Update in `seed.py` and `index.py`:
```python
EMAIL = "your-email@example.com"
PASSWORD = "your-password"
```

### Crawler Settings

- `max_scroll_attempts`: Maximum scroll rounds (default: 50 for seed, 100 for apps)
- `no_change_count`: Stop after N rounds with no new data (default: 3)
- `random_delay()`: 600-1200ms between scrolls

## Resume & Retry

The crawler automatically resumes from where it left off:

1. `apps_done.json` tracks completed apps
2. On restart, only remaining apps are crawled
3. `screens.json` is append-only (duplicates removed later)

To restart from scratch:
```bash
rm src/data/apps_done.json
rm src/data/screens.json
```

## Troubleshooting

### Login Issues

If login fails:
- Check credentials
- Mobbin may require captcha (run headless=False to debug)
- Consider using `storageState` to persist session

### Missing Flows

Some apps don't have `/flows` pages. The crawler automatically:
1. Tries `/flows` first
2. Falls back to `/screens` if no flows detected
3. Omits `flow` field in output

### Rate Limiting

If you see 429 errors:
- Increase `random_delay()` range
- Reduce concurrency (currently sequential)
- Add longer waits between apps

## Performance

- **Phase 0**: ~5-10 minutes (depends on total apps)
- **Phase 1**: ~2-5 seconds per app (depends on # of screens)
- **Catalog**: <1 second

For ~700 apps, expect total runtime of ~2-4 hours.

## Notes

- Crawls in headless mode by default
- Blocks images/fonts/media to speed up crawling
- Uses highest resolution from `srcset` when available
- Normalizes app and flow names (trim + collapse whitespace)

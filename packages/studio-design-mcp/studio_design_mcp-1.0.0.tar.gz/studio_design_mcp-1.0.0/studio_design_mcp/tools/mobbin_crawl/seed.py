"""
Phase 0: App Seed Generation

Crawl iOS and Web app listing pages to generate apps_seed.json.
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright, Page, BrowserContext
from utils import (
    normalize_app_name,
    make_app_key,
    get_timestamp,
    save_json_array,
    random_delay
)


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
APPS_SEED_FILE = DATA_DIR / "apps_seed.json"
COOKIES_FILE = DATA_DIR / "mobbin_cookies.json"

# Entry URLs
ENTRY_URLS = {
    "Mobile": "https://mobbin.com/search/apps/ios?content_type=apps",
    "Web": "https://mobbin.com/search/apps/web?content_type=apps"
}

# Mobbin credentials
EMAIL = "menghuihu@microsoft.com"
PASSWORD = "9X4q7B2m"


async def login(page: Page, context: BrowserContext):
    """Login to Mobbin and save cookies."""
    print("🔐 Logging in to Mobbin...")
    await page.goto("https://mobbin.com/login", wait_until="domcontentloaded")
    await page.wait_for_timeout(2000)
    
    # Fill email
    await page.get_by_role("textbox", name="Email").fill(EMAIL)
    await page.get_by_role("button", name="Continue", exact=True).click()
    await page.wait_for_timeout(1000)
    
    # Fill password
    await page.get_by_role("textbox", name="Password").fill(PASSWORD)
    await page.get_by_role("textbox", name="Password").press("Enter")
    await page.wait_for_timeout(3000)
    
    # Save cookies
    cookies = await context.cookies()
    COOKIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(COOKIES_FILE, 'w') as f:
        json.dump(cookies, f)
    print(f"💾 Cookies saved to {COOKIES_FILE}")


async def load_cookies(context: BrowserContext) -> bool:
    """Load cookies if they exist. Returns True if cookies were loaded."""
    if COOKIES_FILE.exists():
        print(f"🍪 Loading cookies from {COOKIES_FILE}")
        with open(COOKIES_FILE, 'r') as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)
        return True
    return False
    
    print("✅ Logged in successfully")


async def scroll_and_extract_apps(page: Page, platform: str) -> list:
    """
    Scroll the app listing page and extract all apps.
    
    Returns:
        List of app dictionaries with platform, app name, and URL
    """
    print(f"\n📱 Extracting {platform} apps...")
    
    all_apps = []
    seen_urls = set()
    consecutive_no_new = 0
    scroll_count = 0
    max_scrolls = 500
    
    # Keep track of URLs in browser to avoid re-sending duplicates
    await page.evaluate("window.seenUrls = new Set();")
    
    # Extract apps BEFORE starting to scroll (get the initial batch)
    print("   Extracting initial batch...")
    initial_apps = await page.evaluate("""
        () => {
            const newApps = [];
            const listItems = document.querySelectorAll('li');
            
            for (const item of listItems) {
                const heading = item.querySelector('h3');
                if (!heading) continue;
                
                const appName = heading.textContent.trim();
                const links = item.querySelectorAll('a[href*="/screens"]');
                
                for (const link of links) {
                    const href = link.getAttribute('href');
                    if (href && href.includes('/screens')) {
                        const fullUrl = href.startsWith('http') ? href : 'https://mobbin.com' + href;
                        
                        if (!window.seenUrls.has(fullUrl)) {
                            window.seenUrls.add(fullUrl);
                            newApps.push({
                                name: appName,
                                url: fullUrl
                            });
                        }
                        break;
                    }
                }
            }
            
            return newApps;
        }
    """)
    
    # Add initial batch
    for app_data in initial_apps:
        url = app_data['url']
        if url not in seen_urls:
            all_apps.append({
                "platform": platform,
                "app": normalize_app_name(app_data['name']),
                "app_page_url": url,
                "discovered_at": get_timestamp()
            })
            seen_urls.add(url)
    
    print(f"   Initial batch: {len(all_apps)} apps")
    
    # Now start scrolling
    while scroll_count < max_scrolls:
        # Scroll down FIRST
        await page.evaluate("window.scrollBy(0, window.innerHeight * 2)")
        await page.wait_for_timeout(1500)  # Wait for new content
        
        # Then extract new apps
        new_apps = await page.evaluate("""
            () => {
                const newApps = [];
                const listItems = document.querySelectorAll('li');
                
                for (const item of listItems) {
                    const heading = item.querySelector('h3');
                    if (!heading) continue;
                    
                    const appName = heading.textContent.trim();
                    const links = item.querySelectorAll('a[href*="/screens"]');
                    
                    for (const link of links) {
                        const href = link.getAttribute('href');
                        if (href && href.includes('/screens')) {
                            const fullUrl = href.startsWith('http') ? href : 'https://mobbin.com' + href;
                            
                            if (!window.seenUrls.has(fullUrl)) {
                                window.seenUrls.add(fullUrl);
                                newApps.push({
                                    name: appName,
                                    url: fullUrl
                                });
                            }
                            break;
                        }
                    }
                }
                
                return newApps;
            }
        """)
        
        # Add new apps to our list
        if len(new_apps) > 0:
            for app_data in new_apps:
                url = app_data['url']
                if url not in seen_urls:
                    all_apps.append({
                        "platform": platform,
                        "app": normalize_app_name(app_data['name']),
                        "app_page_url": url,
                        "discovered_at": get_timestamp()
                    })
                    seen_urls.add(url)
            
            consecutive_no_new = 0
            if len(all_apps) % 50 == 0:
                print(f"   {len(all_apps)} apps collected...")
        else:
            consecutive_no_new += 1
            
            # Stop if no new apps for 5 consecutive scrolls
            if consecutive_no_new >= 5:
                print(f"   No new apps for 5 scrolls, stopping...")
                break
        
        scroll_count += 1
    
    print(f"✅ Extracted {len(all_apps)} {platform} apps")
    return all_apps


async def crawl_platform(page: Page, platform: str, url: str) -> list:
    """Crawl a single platform (iOS or Web)."""
    print(f"\n🌐 Crawling {platform} apps from {url}")
    
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(3000)
    
    # Wait for app list to be visible first
    try:
        await page.wait_for_selector('li h3', timeout=10000)
        print("   ✅ App list loaded")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not find app list elements: {e}")
    
    # NOW scroll to top and wait for content to reload
    print("   📜 Scrolling to top...")
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(3000)  # Wait longer for content to reload at top
    
    # Extract all apps with infinite scroll
    apps = await scroll_and_extract_apps(page, platform)
    
    return apps


async def main():
    """Main entry point for Phase 0."""
    print("="*60)
    print("🚀 Phase 0: App Seed Generation")
    print("="*60)
    
    all_apps = []
    seen_keys = set()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        # Block unnecessary resources
        await page.route("**/*", lambda route: (
            route.abort() if route.request.resource_type in ["font", "media"]  # Keep images and CSS for debugging
            else route.continue_()
        ))
        
        # Try to load cookies first
        cookies_loaded = await load_cookies(context)
        
        if cookies_loaded:
            # Test if cookies are still valid
            print("🧪 Testing if cookies are still valid...")
            await page.goto("https://mobbin.com/search/apps/ios?content_type=apps", wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            
            # Check if we're logged in (look for app list)
            try:
                await page.wait_for_selector('li h3', timeout=5000)
                print("✅ Cookies are valid, skipping login")
            except:
                print("⚠️  Cookies expired, need to login again")
                await login(page, context)
        else:
            # No cookies, need to login
            await login(page, context)
        
        # Crawl each platform
        for platform, url in ENTRY_URLS.items():
            apps = await crawl_platform(page, platform, url)
            
            # Deduplicate by platform::app key
            for app in apps:
                key = make_app_key(app['platform'], app['app'])
                if key not in seen_keys:
                    all_apps.append(app)
                    seen_keys.add(key)
        
        print("\n🔍 Browser will stay open for 10 seconds so you can inspect...")
        await page.wait_for_timeout(10000)
        
        await browser.close()
    
    # Save to apps_seed.json
    print(f"\n💾 Saving {len(all_apps)} apps to {APPS_SEED_FILE}")
    save_json_array(APPS_SEED_FILE, all_apps)
    
    print(f"\n✅ Phase 0 Complete!")
    print(f"   Total apps: {len(all_apps)}")
    print(f"   Mobile: {sum(1 for a in all_apps if a['platform'] == 'Mobile')}")
    print(f"   Web: {sum(1 for a in all_apps if a['platform'] == 'Web')}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())

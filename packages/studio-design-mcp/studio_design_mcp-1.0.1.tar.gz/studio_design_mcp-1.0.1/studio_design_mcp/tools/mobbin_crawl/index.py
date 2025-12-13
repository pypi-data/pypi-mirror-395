"""
Phase 1: App Flows & Screens Crawler

Correct flow:
1. Get app URL from apps_seed.json (e.g., .../screens)
2. Replace /screens with /flows 
3. Extract flow name from page and collect screen images
4. Output: {platform, app, flow, screen_url}
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright, Page, BrowserContext
from utils import (
    normalize_text,
    make_app_key,
    make_screen_key,
    load_json_array,
    save_json_array,
    load_json_set,
    save_json_set,
    extract_highest_res_image,
    random_delay
)


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
APPS_SEED_FILE = DATA_DIR / "apps_seed.json"
SCREENS_FILE = DATA_DIR / "screens.json"
APPS_DONE_FILE = DATA_DIR / "apps_done.json"
APPS_SKIPPED_FILE = DATA_DIR / "apps_skipped.json"
COOKIES_FILE = DATA_DIR / "mobbin_cookies.json"

# Mobbin credentials
EMAIL = "menghuihu@microsoft.com"
PASSWORD = "9X4q7B2m"


async def save_cookies(context: BrowserContext):
    """Save cookies to file."""
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


async def login(page: Page, context: BrowserContext):
    """Login to Mobbin and save cookies."""
    print("🔐 Logging in to Mobbin...")
    await page.goto("https://mobbin.com/login", wait_until="domcontentloaded")
    await page.wait_for_timeout(4000)  # Wait longer for page and email field to be ready

    # Fill email
    await page.get_by_role("textbox", name="Email").fill(EMAIL)
    await page.wait_for_timeout(2000)  # Extra wait before clicking Continue
    await page.get_by_role("button", name="Continue", exact=True).click()
    await page.wait_for_timeout(1500)

    # Fill password
    await page.get_by_role("textbox", name="Password").fill(PASSWORD)
    await page.get_by_role("textbox", name="Password").press("Enter")
    await page.wait_for_timeout(3000)
    
    print("✅ Logged in successfully")
    
    # Save cookies after successful login
    await save_cookies(context)


async def extract_flow_name_and_images(page: Page, app_name: str) -> list:
    """
    Extract screen images with their flow names from current page view.
    
    Args:
        app_name: The app name to remove from alt text
    
    Returns:
        List of {flow_name, src, srcset, alt}
    """
    data = await page.evaluate("""
        (appName) => {
            const images = [];
            const skipped = [];  // Track skipped images for debugging
            
            // Find all images with alt text containing "screen"
            const imgs = document.querySelectorAll('img[alt*="screen"]');
            
            for (const img of imgs) {
                const alt = img.alt || '';
                const src = img.src || '';
                const srcset = img.srcset || '';
                
                // Only Mobbin CDN images with screen keyword
                if (src && src.includes('bytescale.mobbin.com') && alt.includes('screen')) {
                    // Extract flow name from alt text
                    // Format: "AppName FlowName screen" or just "FlowName screen"
                    let flowName = alt.replace(/\\s+screen\\s*$/i, '').trim();
                    const originalFlowName = flowName;  // Keep for debugging
                    
                    // IMPORTANT: Filter out images that don't contain the app name
                    // This prevents capturing other apps' screens (Nike Run Club, Apple Health, etc.)
                    if (appName && flowName.length > 0) {
                        const appNameLower = appName.toLowerCase();
                        const flowNameLower = flowName.toLowerCase();
                        
                        // Check if alt text contains the app name
                        if (!flowNameLower.includes(appNameLower)) {
                            skipped.push({
                                reason: 'no_app_name',
                                original: originalFlowName,
                                alt: alt
                            });
                            continue;  // Skip this image - it's from another app
                        }
                        
                        // If starts with app name, remove it to get clean flow name
                        if (flowNameLower.startsWith(appNameLower)) {
                            flowName = flowName.substring(appName.length).trim();
                        }
                    }
                    
                    // Only add if we have a non-empty flow name
                    if (flowName.length > 0) {
                        images.push({
                            flow_name: flowName,
                            src: src,
                            srcset: srcset,
                            alt: alt
                        });
                    } else {
                        // Track skipped images
                        skipped.push({
                            reason: 'empty_flow_name',
                            original: originalFlowName,
                            after_removal: flowName,
                            alt: alt
                        });
                    }
                }
            }
            
            return { images, skipped };
        }
    """, app_name)
    
    return data


async def crawl_app(page: Page, app_record: dict) -> tuple[str, list]:
    """
    Crawl a single app's flows and screens.
    
    Returns:
        (status, screens_list)
        status: "success", "skipped", or "failed"
    """
    platform = app_record['platform']
    app = app_record['app']
    app_url = app_record['app_page_url']
    
    print(f"\n📱 Crawling: {platform} - {app}")
    print(f"   URL: {app_url}")
    
    try:
        # Convert /screens to /flows
        if not app_url.endswith('/screens'):
            print(f"   ⚠️  Warning: URL doesn't end with /screens, skipping")
            return "skipped", []

        flows_url = app_url.replace('/screens', '/flows')
        print(f"   Flows URL: {flows_url}")

        # Navigate to flows page with error handling
        try:
            response = await page.goto(flows_url, wait_until="domcontentloaded", timeout=15000)
        except Exception as nav_error:
            # Handle navigation errors (redirects, aborts, etc.)
            if "ERR_ABORTED" in str(nav_error) or "net::ERR" in str(nav_error):
                print(f"   ⚠️  Navigation aborted (likely redirect or invalid page)")
                print(f"   ⏭️  Skipping this app")
                return "skipped", []
            raise  # Re-raise other errors

        await page.wait_for_timeout(2000)

        # Check if we were redirected or if /flows page doesn't exist
        current_url = page.url

        # Case 1: Redirected back to /screens (flows page doesn't exist)
        if '/flows' not in current_url or '/screens' in current_url:
            print(f"   ⚠️  App doesn't have /flows page (redirected to {current_url})")
            print(f"   ⏭️  Skipping this app")
            return "skipped", []

        # Case 2: Check for 404 or error page
        if response and response.status >= 400:
            print(f"   ⚠️  HTTP {response.status} error accessing /flows page")
            print(f"   ⏭️  Skipping this app")
            return "skipped", []

        # Case 3: Check if page has flow content (look for images with "screen" in alt)
        has_content = await page.evaluate("""
            () => {
                const imgs = document.querySelectorAll('img[alt*="screen"]');
                return imgs.length > 0;
            }
        """)

        if not has_content:
            print(f"   ⚠️  No flow content found on page")
            print(f"   ⏭️  Skipping this app")
            return "skipped", []

        print(f"   ✅ Valid /flows page detected")

        # Wait for initial content to fully load before starting to scroll
        await page.wait_for_timeout(8000)  # 8 seconds for complete initial load

        all_screens = []
        seen_urls = set()
        seen_flows = set()
        flow_screen_counts = {}  # Track screens per flow
        no_change_count = 0
        max_scroll_attempts = 300  # Further increase
        scroll_attempts = 0
        
        # Scroll and collect all screens with their flow names
        total_skipped_count = 0
        while scroll_attempts < max_scroll_attempts:
            # Extract images from current view (each image has its flow name)
            result = await extract_flow_name_and_images(page, app)
            current_images = result['images']
            skipped_images = result['skipped']
            
            # Print skipped images for debugging (only first batch)
            if scroll_attempts == 0 and len(skipped_images) > 0:
                other_apps = [s for s in skipped_images if s.get('reason') == 'no_app_name']
                empty_flows = [s for s in skipped_images if s.get('reason') == 'empty_flow_name']
                
                if other_apps:
                    print(f"   🚫 Filtered {len(other_apps)} images from other apps:")
                    for skip in other_apps[:5]:  # Show first 5
                        print(f"      - '{skip['original']}'")
                
                if empty_flows:
                    print(f"   ⚠️  Skipped {len(empty_flows)} images with empty flow names:")
                    for skip in empty_flows[:3]:  # Show first 3
                        print(f"      - Alt: '{skip['alt']}'")
                        print(f"        Original: '{skip['original']}' → After removal: '{skip['after_removal']}'")
            
            total_skipped_count += len(skipped_images)
            
            # Process images
            previous_count = len(all_screens)
            
            for img_data in current_images:
                flow_name = normalize_text(img_data['flow_name'])
                screen_url = extract_highest_res_image(img_data['srcset'], img_data['src'])
                
                # Debug: Track if screen_url is empty
                if not screen_url:
                    print(f"   ⚠️  Empty screen_url for flow: {flow_name}, alt: {img_data.get('alt', 'N/A')}")
                    continue
                
                # Track unique flows
                if flow_name not in seen_flows:
                    seen_flows.add(flow_name)
                    flow_screen_counts[flow_name] = 0
                    print(f"   📂 Found flow: {flow_name}")
                
                # Use flow name in the key to allow same screen in different flows
                key = make_screen_key(platform, app, screen_url, flow_name)
                if key not in seen_urls:
                    all_screens.append({
                        "platform": platform,
                        "app": app,
                        "flow": flow_name,
                        "screen_url": screen_url
                    })
                    seen_urls.add(key)
                    flow_screen_counts[flow_name] += 1
            
            new_screens_count = len(all_screens) - previous_count
            
            if new_screens_count == 0:
                no_change_count += 1
                if no_change_count >= 8:  # Increased to 8
                    print(f"   ⏹️  No new screens for 8 scrolls, stopping...")
                    break
            else:
                no_change_count = 0
                if len(all_screens) % 100 == 0 or new_screens_count > 10:
                    print(f"      {len(all_screens)} screens (+ {new_screens_count} new)")
            
            # Scroll down - faster since lazy load only loads data
            await page.evaluate("window.scrollBy(0, window.innerHeight * 1.5)")
            await page.wait_for_timeout(800)  # Keep fast for efficiency
            scroll_attempts += 1
        
        # Print summary with screens per flow
        print(f"✅ Completed: {len(all_screens)} screens across {len(seen_flows)} flows")
        if total_skipped_count > 0:
            print(f"   ⚠️  Total skipped images: {total_skipped_count} (empty flow name after app name removal)")
        if len(seen_flows) > 0:
            print(f"   Flow breakdown:")
            for flow, count in sorted(flow_screen_counts.items(), key=lambda x: -x[1]):
                print(f"      - {flow}: {count} screens")
        return "success", all_screens
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return "failed", []


async def main():
    """Main entry point for Phase 1."""
    import sys
    
    # Parse command line arguments
    test_mode = False
    test_limit = 3
    start_index = 0
    batch_size = None  # None means no limit, process all remaining
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            test_mode = True
            if len(sys.argv) > 2:
                test_limit = int(sys.argv[2])
        elif sys.argv[1] == '--start':
            test_mode = True
            if len(sys.argv) > 2:
                start_index = int(sys.argv[2])
                test_limit = 1  # Default to 1 app when using --start
            if len(sys.argv) > 3:
                test_limit = int(sys.argv[3])
        elif sys.argv[1] == '--batch':
            # Batch mode: process N apps from remaining
            if len(sys.argv) > 2:
                batch_size = int(sys.argv[2])
    
    print("="*60)
    print("🚀 Phase 1: Crawling App Flows & Screens")
    if test_mode:
        if start_index > 0:
            print(f"   🧪 TEST MODE: Starting from index {start_index}, crawling {test_limit} apps")
        else:
            print(f"   🧪 TEST MODE: Only crawling first {test_limit} apps")
    elif batch_size:
        print(f"   📦 BATCH MODE: Processing {batch_size} apps from remaining")
    print("="*60)
    
    # Load apps seed
    print(f"\n📖 Loading apps from {APPS_SEED_FILE}")
    apps = load_json_array(APPS_SEED_FILE)
    print(f"   Total apps: {len(apps)}")
    
    # Load completed apps
    apps_done = load_json_set(APPS_DONE_FILE)
    print(f"   Already completed: {len(apps_done)}")
    
    # Load skipped apps
    apps_skipped = load_json_set(APPS_SKIPPED_FILE)
    if len(apps_skipped) > 0:
        print(f"   Already skipped: {len(apps_skipped)}")
    
    # Filter remaining apps (exclude both done and skipped)
    remaining_apps = [
        app for app in apps
        if make_app_key(app['platform'], app['app']) not in apps_done
        and make_app_key(app['platform'], app['app']) not in apps_skipped
    ]
    
    print(f"   Total remaining: {len(remaining_apps)}")
    
    # Apply limits based on mode
    if test_mode:
        if start_index > 0:
            # Start from specific index
            print(f"   🧪 Starting from index {start_index}")
            remaining_apps = remaining_apps[start_index:start_index + test_limit]
        elif len(remaining_apps) > test_limit:
            print(f"   🧪 Limiting to first {test_limit} apps for testing")
            remaining_apps = remaining_apps[:test_limit]
    elif batch_size and len(remaining_apps) > batch_size:
        # Batch mode: take first N from remaining
        print(f"   📦 Processing first {batch_size} apps from remaining")
        remaining_apps = remaining_apps[:batch_size]
    
    print(f"   Will process: {len(remaining_apps)} apps")
    
    if not remaining_apps:
        print("\n✅ All apps already crawled!")
        return
    
    # Load existing screens
    existing_screens = load_json_array(SCREENS_FILE)
    all_screens = existing_screens.copy()
    print(f"   Existing screens: {len(existing_screens)}")
    
    # Crawl apps
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headless mode for better performance
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        # Block unnecessary resources for faster loading
        await page.route("**/*", lambda route: (
            route.abort() if route.request.resource_type in ["font", "media"]
            else route.continue_()
        ))
        
        # Try to load cookies first
        cookies_loaded = await load_cookies(context)
        
        if cookies_loaded:
            # Test if cookies are still valid
            print("🧪 Testing if cookies are still valid...")
            await page.goto("https://mobbin.com/browse/ios/apps", wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            
            # Check if we're logged in (look for user-specific content)
            try:
                # Try to find something that only appears when logged in
                await page.wait_for_selector('img[alt*="screen"]', timeout=5000)
                print("✅ Cookies are valid, skipping login")
            except:
                print("⚠️  Cookies expired, need to login again")
                await login(page, context)
        else:
            # No cookies, need to login
            await login(page, context)
        
        # Crawl each app
        for i, app_record in enumerate(remaining_apps, 1):
            print(f"\n[{i}/{len(remaining_apps)}]", end=" ")
            
            app_key = make_app_key(app_record['platform'], app_record['app'])
            
            # Try crawling with retry
            max_retries = 2
            for attempt in range(max_retries):
                status, screens = await crawl_app(page, app_record)
                
                if status == "success":
                    # Add screens to collection
                    all_screens.extend(screens)
                    
                    # Mark as done
                    apps_done.add(app_key)
                    
                    # Save progress periodically
                    if i % 10 == 0:
                        print(f"\n💾 Saving progress...")
                        save_json_array(SCREENS_FILE, all_screens)
                        save_json_set(APPS_DONE_FILE, apps_done)
                        save_json_set(APPS_SKIPPED_FILE, apps_skipped)
                    
                    break
                    
                elif status == "skipped":
                    # App doesn't have /flows page, save separately (no retry needed)
                    print(f"   📝 Recording as skipped (no /flows page)")
                    apps_skipped.add(app_key)
                    break
                    
                else:  # status == "failed"
                    if attempt < max_retries - 1:
                        print(f"   Retrying ({attempt + 2}/{max_retries})...")
                        await page.wait_for_timeout(3000)
                    else:
                        # Mark as done even on failure to avoid infinite retry
                        print(f"   📝 Marking as completed (failed after retries)")
                        apps_done.add(app_key)
        
        # Final save
        print(f"\n💾 Saving final results...")
        save_json_array(SCREENS_FILE, all_screens)
        save_json_set(APPS_DONE_FILE, apps_done)
        save_json_set(APPS_SKIPPED_FILE, apps_skipped)
        
        print(f"\n🔍 Browser will stay open for 10 seconds for inspection...")
        await page.wait_for_timeout(10000)
        
        await browser.close()
    
    print(f"\n" + "="*60)
    print(f"✅ Phase 1 Complete!")
    print(f"   Total screens collected: {len(all_screens)}")
    print(f"   Apps completed: {len(apps_done)}")
    print(f"   Apps skipped: {len(apps_skipped)}")
    print(f"   Saved to: {SCREENS_FILE}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())

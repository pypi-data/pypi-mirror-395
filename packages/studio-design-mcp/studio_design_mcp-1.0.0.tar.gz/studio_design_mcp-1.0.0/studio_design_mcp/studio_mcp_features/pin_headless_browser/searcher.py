"""
Simplified Pinterest Searcher

Search Pinterest for images and extract high-resolution URLs.
Returns: image URL, pin URL, and title/alt text.
"""

import asyncio
from dataclasses import dataclass, asdict
from typing import List, Optional
from urllib.parse import quote_plus
from playwright.async_api import async_playwright


@dataclass
class PinImage:
    """Represents a single image result from Pinterest."""
    image_url: str
    pin_url: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PinterestSearchResult:
    """Container for Pinterest search results."""
    query: str
    images: List[PinImage]
    total_found: int
    status: str = "success"
    message: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "query": self.query,
            "total_found": self.total_found,
            "message": self.message,
            "images": [img.to_dict() for img in self.images],
        }


class PinterestSearcher:
    """Search and extract images from Pinterest."""

    def __init__(self, headless: bool = True):
        """
        Initialize Pinterest searcher.
        
        Args:
            headless: Run browser in headless mode (default: True)
        """
        self.headless = headless
        self.base_url = "https://www.pinterest.com"

    async def search(self, query: str, max_images: int = 10, timeout: int = 90) -> PinterestSearchResult:
        """
        Search Pinterest for images.

        Args:
            query: Search keyword (e.g., "living room", "mobile app", "logo")
            max_images: Maximum number of images to return (default: 10)
            timeout: Overall operation timeout in seconds (default: 90)

        Returns:
            PinterestSearchResult with images and metadata
        """
        try:
            # Wrap entire operation in timeout
            return await asyncio.wait_for(
                self._perform_search(query, max_images),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return PinterestSearchResult(
                query=query,
                images=[],
                total_found=0,
                status="error",
                message=f"Search timed out after {timeout} seconds"
            )
        except Exception as e:
            return PinterestSearchResult(
                query=query,
                images=[],
                total_found=0,
                status="error",
                message=f"Search failed: {str(e)}"
            )

    async def _perform_search(self, query: str, max_images: int) -> PinterestSearchResult:
        """Internal method to perform the actual search."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 900}
                )
                page = await context.new_page()
                
                # Navigate to search page with timeout
                encoded_query = quote_plus(query)
                search_url = f"{self.base_url}/search/pins/?q={encoded_query}"
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(2000)
                
                # Dismiss cookie consent or overlays if present
                await self._dismiss_overlays(page)
                
                # Extract initial images and scroll to load more if needed
                images = []
                seen_urls = set()
                max_scroll_attempts = 15
                no_change_count = 0
                
                # If we need more images, scroll and load more content
                scroll_attempts = 0
                while scroll_attempts < max_scroll_attempts and len(images) < max_images:
                    # Extract ALL images from current page state (including previously loaded ones)
                    # The _extract_images method will return all visible images, we filter duplicates here
                    try:
                        all_current_images = await asyncio.wait_for(
                            self._extract_images(page, max_images * 2),  # Extract more than needed
                            timeout=10.0
                        )
                        
                        previous_count = len(images)
                        
                        # Add new unique images to our collection
                        for img in all_current_images:
                            if img.image_url not in seen_urls:
                                images.append(img)
                                seen_urls.add(img.image_url)
                                if len(images) >= max_images:
                                    break
                        
                        # If we have enough images, stop scrolling
                        if len(images) >= max_images:
                            break
                        
                        # Check if no new content loaded after scrolling
                        if len(images) == previous_count:
                            no_change_count += 1
                            # Stop if no new content for 3 consecutive attempts
                            if no_change_count >= 3:
                                break
                        else:
                            no_change_count = 0  # Reset counter when we get new content
                            
                    except asyncio.TimeoutError:
                        # Continue to next scroll if extraction times out
                        pass
                    
                    # Only scroll if we need more images
                    if len(images) < max_images:
                        # Scroll down progressively (not to the very bottom at once)
                        # This ensures better loading of lazy-loaded images
                        await page.evaluate("window.scrollBy(0, window.innerHeight * 1.5)")
                        await page.wait_for_timeout(2000)  # Wait for images to load
                        scroll_attempts += 1
                        
                        # Dismiss any overlays that might have appeared after scrolling
                        await self._dismiss_overlays(page)
                
                await browser.close()
                
                return PinterestSearchResult(
                    query=query,
                    images=images[:max_images],
                    total_found=len(images),
                    status="success"
                )
                
        except Exception as e:
            raise Exception(f"Pinterest search failed: {str(e)}")

    async def _dismiss_overlays(self, page):
        """Dismiss cookie consent and signup overlays."""
        selectors = [
            'button[aria-label="Accept"]',
            'button:has-text("Accept all")',
            'button:has-text("I agree")',
            'button:has-text("Allow all")',
            'button[aria-label="Close Bottom Right Upsell"]',  # Sign in popup
            'div[role="dialog"] button[aria-label="Close"]',
            'button[aria-label="Close"]',
        ]
        for sel in selectors:
            try:
                btn = await page.query_selector(sel)
                if btn and await btn.is_visible():
                    await btn.click(timeout=1000)
                    await page.wait_for_timeout(200)
            except Exception:
                continue

    async def _extract_images(self, page, limit: int) -> List[PinImage]:
        """Extract images from current viewport."""
        if limit <= 0:
            return []
        
        results = []
        seen = set()
        
        try:
            # Use JavaScript to extract pins more accurately
            pins_data = await page.evaluate("""
                () => {
                    const pins = [];
                    // Target pin cards within list items, excluding shop carousel
                    const listItems = document.querySelectorAll('[role="listitem"]');
                    
                    for (const item of listItems) {
                        // Skip the "Shop living room" carousel
                        const heading = item.querySelector('h2');
                        if (heading && heading.textContent.toLowerCase().includes('shop')) {
                            continue;
                        }
                        
                        // Find pin cards (real pins, not ads)
                        const pinCard = item.querySelector('[role="group"]');
                        if (!pinCard) continue;
                        
                        const link = pinCard.querySelector('a[href*="/pin/"]');
                        const img = pinCard.querySelector('img');
                        
                        if (link && img) {
                            const href = link.getAttribute('href');
                            const srcset = img.getAttribute('srcset');
                            const src = img.getAttribute('src');
                            const alt = img.getAttribute('alt');
                            
                            // Extract highest resolution URL from srcset
                            let imageUrl = src;
                            if (srcset) {
                                // srcset format: "url1 1x, url2 2x, url3 3x, url4 4x"
                                const sources = srcset.split(',').map(s => s.trim());
                                if (sources.length > 0) {
                                    // Get the last (highest resolution) source
                                    const lastSource = sources[sources.length - 1];
                                    imageUrl = lastSource.split(' ')[0];
                                }
                            }
                            
                            // Skip if no valid image URL
                            if (!imageUrl || imageUrl.startsWith('data:')) continue;
                            
                            // Check if it's likely an ad by looking for price buttons
                            const hasPrice = pinCard.textContent.includes('$') && 
                                           (pinCard.textContent.includes('Overstock') || 
                                            pinCard.textContent.includes('Etsy') ||
                                            pinCard.textContent.includes('Amazon'));
                            
                            if (hasPrice) continue;
                            
                            pins.push({
                                pin_url: href,
                                image_url: imageUrl,
                                title: alt
                            });
                        }
                    }
                    
                    return pins;
                }
            """)
            
            for pin_data in pins_data:
                if len(results) >= limit:
                    break
                
                image_url = pin_data.get('image_url', '')
                if not image_url or image_url in seen:
                    continue
                
                pin_url = pin_data.get('pin_url', '')
                if pin_url and not pin_url.startswith('http'):
                    pin_url = f"https://www.pinterest.com{pin_url}"
                
                results.append(
                    PinImage(
                        image_url=image_url,
                        pin_url=pin_url,
                        title=pin_data.get('title')
                    )
                )
                seen.add(image_url)
                
        except Exception as e:
            # Fallback to simple extraction if JavaScript fails
            pass
        
        return results

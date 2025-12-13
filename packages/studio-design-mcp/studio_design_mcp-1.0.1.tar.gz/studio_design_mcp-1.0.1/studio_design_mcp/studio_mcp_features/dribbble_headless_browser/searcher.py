"""
Simplified Dribbble Searcher

Search Dribbble for design shots and extract high-resolution images.
Returns: shot URL, HD image URL, and title.
"""

import asyncio
from dataclasses import dataclass, asdict
from typing import List, Optional
from playwright.async_api import async_playwright


@dataclass
class DribbbleShot:
    """Represents a single design shot from Dribbble."""
    shot_url: str
    image_url: str
    title: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DribbbleSearchResult:
    """Container for Dribbble search results."""
    query: str
    shots: List[DribbbleShot]
    total_found: int
    status: str = "success"
    message: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "query": self.query,
            "total_found": self.total_found,
            "message": self.message,
            "shots": [shot.to_dict() for shot in self.shots],
        }


class DribbbleSearcher:
    """Search and extract design shots from Dribbble."""

    def __init__(self, headless: bool = True):
        """
        Initialize Dribbble searcher.
        
        Args:
            headless: Run browser in headless mode (default: True)
        """
        self.headless = headless
        self.base_url = "https://dribbble.com"

    async def search(self, query: str, max_shots: int = 10, timeout: int = 90) -> DribbbleSearchResult:
        """
        Search Dribbble for design shots.

        Args:
            query: Search keyword (e.g., "mobile app", "logo", "dashboard")
            max_shots: Maximum number of shots to return (default: 10)
            timeout: Overall operation timeout in seconds (default: 90)

        Returns:
            DribbbleSearchResult with shots and metadata
        """
        try:
            # Wrap entire operation in timeout
            return await asyncio.wait_for(
                self._perform_search(query, max_shots),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return DribbbleSearchResult(
                query=query,
                shots=[],
                total_found=0,
                status="error",
                message=f"Search timed out after {timeout} seconds"
            )
        except Exception as e:
            return DribbbleSearchResult(
                query=query,
                shots=[],
                total_found=0,
                status="error",
                message=f"Search failed: {str(e)}"
            )

    async def _perform_search(self, query: str, max_shots: int) -> DribbbleSearchResult:
        """Internal method to perform the actual search."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Navigate to search page with timeout
                search_url = f"{self.base_url}/search/{query}"
                await page.goto(search_url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(2000)
                
                # Dismiss cookie consent if present
                try:
                    await page.get_by_role("button", name="Accept All").click(timeout=3000)
                except Exception:
                    pass  # Cookie banner not present or already dismissed
                
                # Extract shots from initial page load (without any scrolling)
                shots = []
                seen_urls = set()
                
                # First, extract shots from initial page
                try:
                    initial_shots = await asyncio.wait_for(
                        self._extract_shots(page, max_shots),
                        timeout=10.0
                    )
                    for shot in initial_shots:
                        if shot.shot_url not in seen_urls:
                            shots.append(shot)
                            seen_urls.add(shot.shot_url)
                            if len(shots) >= max_shots:
                                break
                except asyncio.TimeoutError:
                    pass
                
                # If we need more shots, scroll and load more content
                scroll_attempts = 0
                max_scroll_attempts = 20  # Prevent infinite scrolling
                no_change_count = 0  # Track consecutive attempts with no new content
                
                while scroll_attempts < max_scroll_attempts and len(shots) < max_shots:
                    # Scroll to bottom
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(2000)  # Wait for content to load after scroll
                    scroll_attempts += 1
                    
                    # Extract newly loaded shots
                    try:
                        batch = await asyncio.wait_for(
                            self._extract_shots(page, max_shots - len(shots)),
                            timeout=10.0
                        )
                        
                        previous_count = len(shots)
                        for shot in batch:
                            if shot.shot_url not in seen_urls:
                                shots.append(shot)
                                seen_urls.add(shot.shot_url)
                                if len(shots) >= max_shots:
                                    break
                        
                        # Check if no new content loaded
                        if len(shots) == previous_count:
                            no_change_count += 1
                            # If no new content for 3 consecutive attempts, stop scrolling
                            if no_change_count >= 3:
                                break
                        else:
                            no_change_count = 0  # Reset counter if we got new content
                            
                    except asyncio.TimeoutError:
                        # Continue to next scroll if extraction times out
                        continue
                
                await browser.close()
                
                return DribbbleSearchResult(
                    query=query,
                    shots=shots[:max_shots],
                    total_found=len(shots),
                    status="success"
                )
                
        except Exception as e:
            raise Exception(f"Dribbble search failed: {str(e)}")

    async def _extract_shots(self, page, limit: int) -> List[DribbbleShot]:
        """Extract shots from current page state."""
        if limit <= 0:
            return []
        
        try:
            # Extract shot data using JavaScript (with timeout)
            shot_data = await page.evaluate(f"""
                () => {{
                    // Target the shots grid specifically to avoid nav/footer items
                    const shots = document.querySelectorAll('ol.shots-grid > li');
                    const results = [];
                    
                    for (let i = 0; i < shots.length && results.length < {limit}; i++) {{
                            const shot = shots[i];
                            const img = shot.querySelector('img');
                            const link = shot.querySelector('a[href*="/shots/"]');
                            
                            if (img && link) {{
                                // Prioritize data-src for lazy-loaded images
                                const imgSrc = img.getAttribute('data-src') || img.getAttribute('src');
                                const shotUrl = link.getAttribute('href');
                                
                                // Extract title: try aria-label first, fallback to URL slug
                                let title = null;
                                
                                // Look for link with aria-label containing "View"
                                const linkWithAria = shot.querySelector('a[aria-label^="View"]');
                                if (linkWithAria) {{
                                    const ariaLabel = linkWithAria.getAttribute('aria-label');
                                    title = ariaLabel.replace(/^View\s+/i, '');
                                }}
                                
                                // Fallback: extract from shot URL slug
                                if (!title && shotUrl) {{
                                    const urlParts = shotUrl.split('/').pop().split('-');
                                    if (urlParts.length > 1) {{
                                        title = urlParts.slice(1).join(' ')
                                            .split(' ')
                                            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                                            .join(' ');
                                    }}
                                }}
                                
                                // Last resort: use img alt (truncate at 100 chars to avoid tags)
                                if (!title) {{
                                    const altText = img.getAttribute('alt') || '';
                                    title = altText.substring(0, 100);
                                }}
                                
                                // Check for ad markers
                                const hasAdMarkers = shot.textContent.includes('Hide ads') || 
                                                    shot.textContent.includes('Advertise');
                                
                                // Only valid shot images from Dribbble CDN (exclude avatars, ads and other assets)
                                if (imgSrc && imgSrc.includes('cdn.dribbble.com') && 
                                    imgSrc.match(/\.(jpg|jpeg|png|gif|webp)/i) &&
                                    !imgSrc.includes('/avatars/') &&
                                    shotUrl && shotUrl.startsWith('/shots/') &&
                                    !hasAdMarkers) {{
                                    
                                    // Get HD URL by removing resize/crop parameters
                                    let hdUrl = imgSrc.split('?')[0];
                                    
                                    // Build full shot URL
                                    let fullShotUrl = shotUrl.startsWith('http') ? shotUrl : '{self.base_url}' + shotUrl;
                                    
                                    results.push({{
                                        shot_url: fullShotUrl,
                                        image_url: hdUrl,
                                        title: title.substring(0, 100) || null
                                    }});
                                }}
                            }}
                        }}
                        
                        return results;
                    }}
                """)
            
            # Convert to DribbbleShot objects
            return [DribbbleShot(**shot) for shot in shot_data]
            
        except Exception as e:
            # Return empty list on error
            return []


async def search_dribbble(query: str, max_shots: int = 10, timeout: int = 90) -> DribbbleSearchResult:
    """
    Convenience function to search Dribbble.
    
    Args:
        query: Search keyword
        max_shots: Maximum number of shots to return
        timeout: Overall operation timeout in seconds (default: 90)
        
    Returns:
        DribbbleSearchResult with shots and metadata
    """
    searcher = DribbbleSearcher()
    return await searcher.search(query, max_shots, timeout)
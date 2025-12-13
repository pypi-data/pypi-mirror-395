import asyncio
import argparse
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pin_headless_browser.searcher import PinterestSearcher


async def main():
    parser = argparse.ArgumentParser(description="Run a Pinterest search and print results as JSON.")
    parser.add_argument("--query", "-q", type=str, default="mobile app onboarding", help="Search query")
    parser.add_argument("--max", "-m", type=int, default=6, help="Max images to fetch")
    args = parser.parse_args()

    print(f"Searching Pinterest for: '{args.query}' (max {args.max} images)")
    print("-" * 60)
    
    searcher = PinterestSearcher(headless=True)
    result = await searcher.search(args.query, max_images=args.max)
    
    print(f"\nStatus: {result.status}")
    print(f"Total found: {result.total_found}")
    if result.message:
        print(f"Message: {result.message}")
    
    print(f"\nImages ({len(result.images)}):")
    for i, img in enumerate(result.images, 1):
        print(f"\n{i}. {img.title or 'No title'}")
        print(f"   Image URL: {img.image_url[:80]}...")
        print(f"   Pin URL: {img.pin_url or 'N/A'}")


if __name__ == "__main__":
    asyncio.run(main())

"""
Test script for simplified Dribbble searcher.
"""

import asyncio
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dribbble_headless_browser.searcher import search_dribbble


async def test_dribbble_search():
    """Test Dribbble search functionality."""
    print("=" * 60)
    print("🎨 Testing Dribbble Search")
    print("=" * 60)
    
    # Test configuration
    query = "logo"
    max_shots = 10
    
    print(f"\nSearching for: '{query}'")
    print(f"Max shots: {max_shots}")
    print("-" * 60)
    
    # Perform search
    result = await search_dribbble(query, max_shots)
    
    # Display results
    print(f"\nStatus: {result.status}")
    if result.message:
        print(f"Message: {result.message}")
    
    print(f"Total found: {result.total_found}")
    print(f"\n📸 Shots:")
    print("-" * 60)
    
    for i, shot in enumerate(result.shots, 1):
        print(f"\n[{i}] {shot.title or 'Untitled'}")
        print(f"  Shot URL: {shot.shot_url}")
        print(f"  Image: {shot.image_url}")
    
    # Save to JSON
    output_file = f"dribbble_{query}_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"✅ Complete! Results saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_dribbble_search())
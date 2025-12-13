"""
Mobbin Crawler - Main Entry Point

Run the complete crawling pipeline:
1. Phase 0: Generate apps seed
2. Phase 1: Crawl apps flows & screens
3. Generate catalog
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from seed import main as run_phase_0
from index import main as run_phase_1
from catalog import generate_catalog


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


async def main():
    """Run the complete crawling pipeline."""
    print_header("🚀 MOBBIN CRAWLER")
    
    print("This will run the complete crawling pipeline:")
    print("  1. Phase 0: Generate apps seed (iOS & Web)")
    print("  2. Phase 1: Crawl each app's flows & screens")
    print("  3. Generate catalog from collected data")
    print()
    
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Aborted.")
        return
    
    try:
        # Phase 0
        print_header("Phase 0: Apps Seed Generation")
        await run_phase_0()
        
        # Phase 1
        print_header("Phase 1: Crawl Flows & Screens")
        await run_phase_1()
        
        # Generate catalog
        print_header("Catalog Generation")
        generate_catalog()
        
        print_header("✅ CRAWLING COMPLETE!")
        print("Output files:")
        print("  - src/data/apps_seed.json")
        print("  - src/data/screens.json")
        print("  - src/data/apps_done.json")
        print("  - src/data/catalog.json")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        print("Progress has been saved. You can resume by running again.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

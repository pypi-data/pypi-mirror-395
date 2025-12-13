"""
Catalog Generation

Generate catalog.json from screens.json (offline post-processing).
"""

from pathlib import Path
from collections import defaultdict
from utils import load_json_array, save_json_array


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SCREENS_FILE = DATA_DIR / "screens.json"
CATALOG_FILE = DATA_DIR / "catalog.json"


def generate_catalog():
    """Generate catalog from screens.json."""
    print("="*60)
    print("📊 Generating Catalog")
    print("="*60)
    
    # Load screens
    print(f"\n📖 Loading screens from {SCREENS_FILE}")
    screens = load_json_array(SCREENS_FILE)
    print(f"   Total screens: {len(screens)}")
    
    if not screens:
        print("❌ No screens found!")
        return
    
    # Aggregate data
    app_stats = defaultdict(lambda: {"screens_count": 0, "has_flows": False})
    flow_stats = defaultdict(lambda: {"screens_count": 0})
    
    for screen in screens:
        platform = screen.get('platform', '')
        app = screen.get('app', '')
        flow = screen.get('flow')
        
        if not platform or not app:
            continue
        
        # App stats
        app_key = f"{platform}::{app}"
        app_stats[app_key]["screens_count"] += 1
        
        # Flow stats (only if flow exists)
        if flow:
            app_stats[app_key]["has_flows"] = True
            flow_key = f"{platform}::{app}::{flow}"
            flow_stats[flow_key]["screens_count"] += 1
    
    # Build catalog
    apps = []
    flows = []
    
    # Apps
    for app_key, stats in app_stats.items():
        platform, app = app_key.split("::", 1)
        apps.append({
            "platform": platform,
            "app": app,
            "has_flows": stats["has_flows"],
            "screens_count": stats["screens_count"]
        })
    
    # Flows (only for apps with flows)
    for flow_key, stats in flow_stats.items():
        platform, app, flow = flow_key.split("::", 2)
        flows.append({
            "platform": platform,
            "app": app,
            "flow": flow,
            "screens_count": stats["screens_count"]
        })
    
    # Sort
    apps.sort(key=lambda x: (x['platform'], x['app']))
    flows.sort(key=lambda x: (x['platform'], x['app'], x['flow']))
    
    catalog = {
        "apps": apps,
        "flows": flows
    }
    
    # Save
    print(f"\n💾 Saving catalog to {CATALOG_FILE}")
    save_json_array(CATALOG_FILE, catalog)
    
    print(f"\n✅ Catalog Generated!")
    print(f"   Apps: {len(apps)}")
    print(f"   - With flows: {sum(1 for a in apps if a['has_flows'])}")
    print(f"   - Without flows: {sum(1 for a in apps if not a['has_flows'])}")
    print(f"   Flows: {len(flows)}")
    print("="*60)


if __name__ == "__main__":
    generate_catalog()

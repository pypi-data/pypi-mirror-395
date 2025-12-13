"""
Clean apps with only one flow from apps_done and screens data
"""
import json
from pathlib import Path
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SCREENS_FILE = DATA_DIR / "screens.json"
APPS_DONE_FILE = DATA_DIR / "apps_done.json"

def make_app_key(platform, app):
    """Create a unique key for an app."""
    return f"{platform}|{app}"

def clean_single_flow_apps():
    """Remove apps with only 1 flow from both screens and apps_done."""
    
    print("=" * 70)
    print("Cleaning apps with single flow")
    print("=" * 70)
    
    # Load screens data
    print("\n1. Loading screens data...")
    with open(SCREENS_FILE, 'r') as f:
        screens = json.load(f)
    print(f"   Total screens before: {len(screens)}")
    
    # Find apps with only 1 flow
    print("\n2. Analyzing flows per app...")
    app_flows = defaultdict(set)
    for screen in screens:
        app_key = f"{screen['platform']} - {screen['app']}"
        app_flows[app_key].add(screen['flow'])
    
    single_flow_apps = set()
    for app, flows in app_flows.items():
        if len(flows) == 1:
            single_flow_apps.add(app)
    
    print(f"   Found {len(single_flow_apps)} apps with only 1 flow:")
    for app in sorted(single_flow_apps):
        print(f"      - {app}")
    
    # Remove these apps from screens
    print("\n3. Removing screens from single-flow apps...")
    cleaned_screens = []
    removed_count = 0
    
    for screen in screens:
        app_key = f"{screen['platform']} - {screen['app']}"
        if app_key not in single_flow_apps:
            cleaned_screens.append(screen)
        else:
            removed_count += 1
    
    print(f"   Removed {removed_count} screens")
    print(f"   Remaining screens: {len(cleaned_screens)}")
    
    # Load apps_done
    print("\n4. Loading apps_done data...")
    with open(APPS_DONE_FILE, 'r') as f:
        apps_done = json.load(f)
    print(f"   Total apps_done before: {len(apps_done)}")
    
    # Remove single-flow apps from apps_done
    print("\n5. Removing single-flow apps from apps_done...")
    cleaned_apps_done = []
    removed_apps = []
    
    for app_key in apps_done:
        # Parse the app_key format: "platform::app_name"
        parts = app_key.split('::')
        if len(parts) == 2:
            platform, app_name = parts
            display_key = f"{platform} - {app_name}"
            
            if display_key not in single_flow_apps:
                cleaned_apps_done.append(app_key)
            else:
                removed_apps.append(display_key)
    
    print(f"   Removed {len(removed_apps)} apps from apps_done:")
    for app in sorted(removed_apps):
        print(f"      - {app}")
    print(f"   Remaining apps_done: {len(cleaned_apps_done)}")
    
    # Confirm before saving
    print("\n" + "=" * 70)
    print("Summary:")
    print(f"  - Screens: {len(screens)} → {len(cleaned_screens)} ({removed_count} removed)")
    print(f"  - Apps done: {len(apps_done)} → {len(cleaned_apps_done)} ({len(removed_apps)} removed)")
    print("=" * 70)
    
    response = input("\nDo you want to save these changes? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        # Save cleaned screens
        print("\n6. Saving cleaned screens...")
        with open(SCREENS_FILE, 'w') as f:
            json.dump(cleaned_screens, f, indent=2)
        print(f"   ✅ Saved {len(cleaned_screens)} screens to {SCREENS_FILE}")
        
        # Save cleaned apps_done
        print("\n7. Saving cleaned apps_done...")
        with open(APPS_DONE_FILE, 'w') as f:
            json.dump(cleaned_apps_done, f, indent=2)
        print(f"   ✅ Saved {len(cleaned_apps_done)} apps to {APPS_DONE_FILE}")
        
        print("\n" + "=" * 70)
        print("✅ Cleanup completed successfully!")
        print("You can now re-crawl these apps to get complete data.")
        print("=" * 70)
    else:
        print("\n❌ Changes not saved. Exiting...")

if __name__ == "__main__":
    clean_single_flow_apps()

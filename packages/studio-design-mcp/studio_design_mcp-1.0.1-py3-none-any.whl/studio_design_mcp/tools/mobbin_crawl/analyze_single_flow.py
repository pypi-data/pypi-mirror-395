"""
Analyze apps with only one flow - likely incomplete crawls
"""
import json
from pathlib import Path
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SCREENS_FILE = DATA_DIR / "screens.json"

def analyze_flows():
    """Find apps with only 1 flow."""
    print("Loading screens data...")
    with open(SCREENS_FILE, 'r') as f:
        screens = json.load(f)
    
    print(f"Total screens: {len(screens)}")
    
    # Count flows per app
    app_flows = defaultdict(set)
    app_screen_counts = defaultdict(int)
    
    for screen in screens:
        app_key = f"{screen['platform']} - {screen['app']}"
        app_flows[app_key].add(screen['flow'])
        app_screen_counts[app_key] += 1
    
    # Find apps with only 1 flow
    single_flow_apps = []
    for app, flows in app_flows.items():
        if len(flows) == 1:
            single_flow_apps.append({
                'app': app,
                'flow': list(flows)[0],
                'screen_count': app_screen_counts[app]
            })
    
    # Sort by app name
    single_flow_apps.sort(key=lambda x: x['app'])
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"Total apps crawled: {len(app_flows)}")
    print(f"Apps with only 1 flow: {len(single_flow_apps)} ({len(single_flow_apps)/len(app_flows)*100:.1f}%)")
    print(f"{'='*70}")
    
    # Print details
    print(f"\nApps with single flow (likely incomplete):")
    print(f"{'='*70}")
    for item in single_flow_apps:
        print(f"{item['app']:<40} | {item['flow']:<20} | {item['screen_count']:>3} screens")
    
    # Print statistics
    print(f"\n{'='*70}")
    print(f"Statistics:")
    print(f"  - Apps with 1 flow: {len(single_flow_apps)}")
    print(f"  - Apps with 2+ flows: {len(app_flows) - len(single_flow_apps)}")
    
    # Show flow distribution
    flow_counts = defaultdict(int)
    for flows in app_flows.values():
        flow_counts[len(flows)] += 1
    
    print(f"\nFlow count distribution:")
    for count in sorted(flow_counts.keys()):
        print(f"  - {count} flow(s): {flow_counts[count]} apps")
    
    return single_flow_apps

if __name__ == "__main__":
    analyze_flows()

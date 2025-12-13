"""
Mobbin Search MCP Tools

Two tools for searching Mobbin design data:
1. search_mobbin_flows - Find flows for given app(s)
2. search_mobbin_screens - Get screens for given app(s) and flow(s)
"""

import json
from pathlib import Path
from typing import Union, List, Dict, Any
import re


# ============================================================================
# Configuration
# ============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "mobbin"
CATALOG_FILE = DATA_DIR / "catalog.json"
# Load screens from 8 split files
SCREENS_FILES = [DATA_DIR / f"screens_part{i}.json" for i in range(1, 9)]


# ============================================================================
# Helper Functions
# ============================================================================

def normalize_name(name: str) -> str:
    """Normalize app/flow name for matching (lowercase, remove special chars)."""
    return re.sub(r'[^a-z0-9]', '', name.lower())


def find_matching_apps(query: str, catalog_apps: List[Dict]) -> Dict[str, Any]:
    """
    Find apps matching the query.
    
    Returns:
        {
            "exact_matches": [...],  # Exact matches (normalized)
            "partial_matches": [...]  # Partial matches
        }
    """
    query_normalized = normalize_name(query)
    exact_matches = []
    partial_matches = []
    
    for app_data in catalog_apps:
        app_name = app_data['app']
        app_normalized = normalize_name(app_name)
        
        if app_normalized == query_normalized:
            exact_matches.append(app_data)
        elif query_normalized in app_normalized:
            partial_matches.append(app_data)
    
    return {
        "exact_matches": exact_matches,
        "partial_matches": partial_matches
    }


# ============================================================================
# Data Loading Functions
# ============================================================================

def load_catalog() -> Dict[str, Any]:
    """Load catalog.json from disk."""
    with open(CATALOG_FILE, 'r') as f:
        return json.load(f)


def load_screens_for_query(app_names: List[str], flow_names: List[str] = None) -> List[Dict]:
    """
    Load screens from disk and filter by app(s) and flow(s).
    
    Args:
        app_names: List of app names to match
        flow_names: Optional list of flow names to match
        
    Returns:
        List of matching screen objects
    """
    # Normalize search criteria
    app_names_normalized = {normalize_name(name) for name in app_names}
    flow_names_normalized = {normalize_name(name) for name in flow_names} if flow_names else None
    
    results = []
    
    # Load from all 8 part files
    for screens_file in SCREENS_FILES:
        if not screens_file.exists():
            continue
            
        with open(screens_file, 'r') as f:
            screens = json.load(f)
            
            for screen in screens:
                # Check app match
                screen_app_normalized = normalize_name(screen['app'])
                if screen_app_normalized not in app_names_normalized:
                    continue
                
                # Check flow match (if specified)
                if flow_names_normalized:
                    screen_flow_normalized = normalize_name(screen.get('flow', ''))
                    if screen_flow_normalized not in flow_names_normalized:
                        continue
                
                results.append(screen)
    
    return results


# ============================================================================
# Tool 1: Search Mobbin Flows
# ============================================================================

def search_mobbin_flows(app_names: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Search for flows in given app(s).
    
    Args:
        app_names: Single app name or list of app names
        
    Returns:
        {
            "status": "success" | "partial" | "not_found",
            "results": [
                {
                    "app": "Instagram",
                    "platform": "Mobile",
                    "flows": ["Onboarding", "Profile", ...],
                    "flow_count": 45,
                    "total_screens": 1234
                }
            ],
            "not_found": [...],  # Apps not found
            "suggestions": {...}  # Suggestions for not found apps
        }
    """
    # Normalize input
    if isinstance(app_names, str):
        app_names = [app_names]
    
    # Load catalog
    catalog = load_catalog()
    catalog_apps = catalog['apps']
    catalog_flows = catalog['flows']
    
    # Build flow lookup: {(platform, app): [flows]}
    flows_by_app = {}
    for flow_data in catalog_flows:
        key = (flow_data['platform'], flow_data['app'])
        if key not in flows_by_app:
            flows_by_app[key] = []
        flows_by_app[key].append({
            'name': flow_data['flow'],
            'screen_count': flow_data['screens_count']
        })
    
    results = []
    not_found = []
    suggestions = {}
    
    for query in app_names:
        matches = find_matching_apps(query, catalog_apps)
        
        if matches['exact_matches']:
            # Found exact match(es)
            for app_data in matches['exact_matches']:
                platform = app_data['platform']
                app = app_data['app']
                key = (platform, app)
                
                app_flows = flows_by_app.get(key, [])
                
                results.append({
                    'app': app,
                    'platform': platform,
                    'flows': [f['name'] for f in app_flows],
                    'flow_count': len(app_flows),
                    'total_screens': app_data['screens_count']
                })
        else:
            # No exact match
            not_found.append(query)
            if matches['partial_matches']:
                # Provide suggestions (limit to 10)
                suggestions[query] = [
                    f"{app['platform']} - {app['app']}" 
                    for app in matches['partial_matches'][:10]
                ]
    
    # Determine status
    if results and not not_found:
        status = "success"
    elif results and not_found:
        status = "partial"
    else:
        status = "not_found"
    
    response = {
        "status": status,
        "results": results
    }
    
    if not_found:
        response["not_found"] = not_found
    
    if suggestions:
        response["suggestions"] = suggestions
        response["message"] = "Some apps not found. See 'suggestions' for similar apps."
    
    return response


# ============================================================================
# Tool 2: Search Mobbin Screens
# ============================================================================

def search_mobbin_screens(
    app_names: Union[str, List[str]], 
    flow_names: Union[str, List[str]] = None
) -> Dict[str, Any]:
    """
    Get screens for given app(s) and flow(s).
    
    Args:
        app_names: Single app name or list of app names
        flow_names: Optional single flow name or list of flow names
        
    Returns:
        {
            "status": "success" | "error",
            "results": [
                {
                    "app": "Instagram",
                    "platform": "Mobile",
                    "flow": "Onboarding",
                    "screens": [
                        {"screen_url": "...", "index": 1},
                        ...
                    ],
                    "screen_count": 12
                }
            ],
            "total_screens": 234,
            "message": "..."
        }
    """
    # Normalize input
    if isinstance(app_names, str):
        app_names = [app_names]
    
    if flow_names:
        if isinstance(flow_names, str):
            flow_names = [flow_names]
    
    # Load screens
    try:
        screens = load_screens_for_query(app_names, flow_names)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error loading screens: {str(e)}",
            "total_screens": 0
        }
    
    if not screens:
        message = f"No screens found for app(s): {', '.join(app_names)}"
        if flow_names:
            message += f" and flow(s): {', '.join(flow_names)}"
        message += ". Please use search_mobbin_flows first to verify app and flow names."
        
        return {
            "status": "error",
            "message": message,
            "total_screens": 0
        }
    
    # Group screens by (platform, app, flow)
    grouped = {}
    for screen in screens:
        key = (screen['platform'], screen['app'], screen['flow'])
        if key not in grouped:
            grouped[key] = []
        
        # Strip query parameters from URL to remove watermark/footer
        url = screen['screen_url']
        if '?' in url:
            url = url.split('?')[0]
            
        grouped[key].append(url)
    
    # Build results
    results = []
    for (platform, app, flow), screen_urls in grouped.items():
        results.append({
            'platform': platform,
            'app': app,
            'flow': flow,
            'screens': [
                {'screen_url': url, 'index': i + 1} 
                for i, url in enumerate(screen_urls)
            ],
            'screen_count': len(screen_urls)
        })
    
    # Sort results
    results.sort(key=lambda x: (x['platform'], x['app'], x['flow']))
    
    return {
        "status": "success",
        "results": results,
        "total_screens": len(screens)
    }


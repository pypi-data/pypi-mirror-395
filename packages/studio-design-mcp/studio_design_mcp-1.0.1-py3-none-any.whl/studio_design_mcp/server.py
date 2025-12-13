from mcp.server.fastmcp import FastMCP
import asyncio
import os
import sys
from typing import List, Dict, Optional, Union

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from studio_mcp_features.pin_headless_browser.searcher import PinterestSearcher
from studio_mcp_features.dribbble_headless_browser.searcher import search_dribbble
from config import config
import logging

# Create MCP server instance
logging.basicConfig(level=logging.INFO)
mcp = FastMCP("designer-studio-mcp")

logger = logging.getLogger(__name__)

# Ensure logger has at least one handler to avoid "No handlers" warnings
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Log initialization
logger.info("🎨 Designer Studio MCP - Mobbin & Dribbble & Pinterest Search")

# Pinterest and Dribbble require no auth
logger.info("📌 Pinterest search available (no auth required)")
logger.info("🎯 Dribbble search available (no auth required)")
logger.info("📱 Mobbin search available (local catalog data)")

@mcp.tool()
async def search_pinterest_images(query: str, max_images: int = 10):
    """
    Search Pinterest.com public pins by keyword and return image results.

    Args:
        query (str, required): Search query, e.g., 'living room', 'mobile onboarding'.
        max_images (int, optional): Maximum number of images to return. Defaults to 10.

    Returns:
        Dict containing:
        - status: "success" or "error"
        - query: Original search query
        - images: List of image data with URLs, titles, and optional pin links
        - total_found: Total number of images found
        - message: Status message or error details
    """
    try:
        searcher = PinterestSearcher(headless=True)
        result = await searcher.search(query, max_images)
        # result is a PinterestSearchResult dataclass; return dict for MCP clients
        return result.to_dict() if hasattr(result, "to_dict") else result
    except Exception as e:
        logger.error(f"Error in search_pinterest_images: {e}")
        return {
            "status": "error",
            "query": query,
            "message": f"Pinterest search failed: {str(e)}",
            "images": [],
            "total_found": 0,
        }

@mcp.tool()
async def search_dribbble_shots(query: str, max_shots: int = 12):
    """
    Search Dribbble.com for design shots by keyword and return shot results.

    Args:
        query (str, required): Search query, e.g., 'mobile app design', 'login page ui', 'dashboard'.
        max_shots (int, optional): Maximum number of shots to return. Defaults to 12.

    Returns:
        Dict containing:
        - status: "success" or "error"
        - query: Original search query
        - shots: List of shots, each with shot_url, image_url, and title
        - total_found: Total number of shots found
        - message: Status message or error details (if error)
    """
    try:
        result = await search_dribbble(query, max_shots)
        # result is a DribbbleSearchResult dataclass; return dict for MCP clients
        return result.to_dict() if hasattr(result, "to_dict") else result
    except Exception as e:
        logger.error(f"Error in search_dribbble_shots: {e}")
        return {
            "status": "error",
            "query": query,
            "message": f"Dribbble search failed: {str(e)}",
            "shots": [],
            "total_found": 0,
        }

@mcp.tool()
async def search_mobbin_flows(app_names: Union[str, List[str]]):
    """
    Search for flows in Mobbin app(s) from local catalog data.
    
    Use this tool to discover what flows are available for one or more apps.
    
    Args:
        app_names (Union[str, List[str]], required): Single app name (e.g., "Instagram") or list of app names.
                                                     Supports partial matching.
    
    Returns:
        Dict containing:
        - status: "success", "partial", or "not_found"
        - results: List of apps with their flows and details
        - not_found: List of apps not found (if any)
        - suggestions: Similar app names for not found apps (if any)
        
    Example:
        search_mobbin_flows("Instagram")
        search_mobbin_flows(["Instagram", "Twitter"])
    """
    try:
        from studio_mcp_features.mobbin_search.searcher import search_mobbin_flows as search_flows_impl
        result = search_flows_impl(app_names)
        return result
    except Exception as e:
        logger.error(f"Error in search_mobbin_flows: {e}")
        return {
            "status": "error",
            "message": f"Mobbin flows search failed: {str(e)}",
            "results": []
        }

@mcp.tool()
async def search_mobbin_screens(app_names: Union[str, List[str]], flow_names: Union[str, List[str]] = None):
    """
    Get screens for Mobbin app(s) and flow(s) from local data.
    
    Use this tool to retrieve actual screen URLs for specific apps and flows.
    Tip: Use search_mobbin_flows first to see available flows.
    
    Args:
        app_names (Union[str, List[str]], required): Single app name or list of app names
        flow_names (Union[str, List[str]], optional): Single flow name or list of flow names (returns all flows if not specified)
        
    Returns:
        Dict containing:
        - status: "success" or "error"
        - results: List of results grouped by app and flow with screen URLs
        - total_screens: Total number of screens found
        - message: Error message if no screens found
        
    Example:
        search_mobbin_screens("Instagram", "Onboarding")
        search_mobbin_screens(["Instagram", "Twitter"], ["Onboarding", "Profile"])
        search_mobbin_screens("Instagram")  # All flows
    """
    try:
        from studio_mcp_features.mobbin_search.searcher import search_mobbin_screens as search_screens_impl
        result = search_screens_impl(app_names, flow_names)
        return result
    except Exception as e:
        logger.error(f"Error in search_mobbin_screens: {e}")
        return {
            "status": "error",
            "message": f"Mobbin screens search failed: {str(e)}",
            "results": [],
            "total_screens": 0
        }

def serve():
    """Start the MCP server."""
    return mcp.run()

if __name__ == "__main__":
    serve()

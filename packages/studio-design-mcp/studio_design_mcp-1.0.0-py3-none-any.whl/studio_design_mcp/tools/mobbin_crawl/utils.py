"""Utility functions for Mobbin crawler."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set
import random


def normalize_text(text: str) -> str:
    """Normalize text: trim and collapse whitespace."""
    if not text:
        return ""
    return " ".join(text.strip().split())


def normalize_app_name(name: str) -> str:
    """Normalize app name for use as unique key."""
    return normalize_text(name)


def make_app_key(platform: str, app: str) -> str:
    """Generate unique key for app."""
    return f"{platform}::{app}"


def make_screen_key(platform: str, app: str, screen_url: str, flow: str = None) -> str:
    """
    Generate unique key for screen.
    
    Args:
        platform: Platform name (Mobile/Web)
        app: App name
        screen_url: Screen image URL
        flow: Optional flow name - if provided, allows same screen_url in different flows
    
    Returns:
        Unique key string
    """
    if flow:
        return f"{platform}::{app}::{flow}::{screen_url}"
    return f"{platform}::{app}::{screen_url}"


def load_json_set(filepath: Path) -> Set[str]:
    """Load a JSON array file into a set."""
    if not filepath.exists():
        return set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return set(data)
            return set()
    except Exception as e:
        print(f"Warning: Failed to load {filepath}: {e}")
        return set()


def save_json_set(filepath: Path, data: Set[str]):
    """Save a set to JSON array file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(sorted(list(data)), f, indent=2, ensure_ascii=False)


def append_jsonl(filepath: Path, record: Dict[str, Any]):
    """Append a record to JSONL file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def load_jsonl(filepath: Path) -> List[Dict[str, Any]]:
    """Load all records from JSONL file."""
    if not filepath.exists():
        return []
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def save_json_array(filepath: Path, records: List[Dict[str, Any]]):
    """Save records to JSON array file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def load_json_array(filepath: Path) -> List[Dict[str, Any]]:
    """Load records from JSON array file."""
    if not filepath.exists():
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def random_delay(min_ms: int = 600, max_ms: int = 1200) -> float:
    """Generate random delay in seconds."""
    return random.randint(min_ms, max_ms) / 1000.0


def extract_highest_res_image(srcset: str, src: str = "") -> str:
    """
    Extract the highest resolution image URL from srcset.
    
    Args:
        srcset: Image srcset attribute (e.g., "url1 1x, url2 2x, url3 4x")
        src: Fallback src attribute
        
    Returns:
        Highest resolution image URL
    """
    if not srcset:
        return src
    
    # Parse srcset: "url1 1x, url2 2x, url3 4x"
    sources = [s.strip() for s in srcset.split(',')]
    if not sources:
        return src
    
    # Get the last source (usually highest resolution)
    last_source = sources[-1]
    parts = last_source.split()
    if parts:
        return parts[0]
    
    return src


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + 'Z'


def dedupe_screens(screens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate screens based on screen_url."""
    seen = set()
    unique = []
    for screen in screens:
        key = screen.get('screen_url', '')
        if key and key not in seen:
            seen.add(key)
            unique.append(screen)
    return unique

"""
Analytics caching system for performance optimization.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class AnalyticsCache:
    """Manage analytics data caching."""
    
    def __init__(self, cache_file: Optional[Path] = None):
        """
        Initialize cache manager.
        
        Args:
            cache_file: Path to cache file. Defaults to .stride/analytics.json
        """
        if cache_file is None:
            cache_file = Path.cwd() / ".stride" / "analytics.json"
        
        self.cache_file = cache_file
        self.cache_data = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cached analytics data."""
        if not self.cache_file.exists():
            return {}
        
        try:
            content = self.cache_file.read_text(encoding="utf-8")
            return json.loads(content)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def save_cache(self, metrics: Dict, checksums: Dict):
        """
        Save metrics to cache.
        
        Args:
            metrics: Calculated metrics dictionary.
            checksums: Sprint checksums for validation.
        """
        self.cache_data = {
            "last_calculated": datetime.now().isoformat(),
            "sprint_count": len(checksums),
            "metrics": metrics,
            "sprint_checksums": checksums,
        }
        
        # Ensure directory exists
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write cache file
        self.cache_file.write_text(
            json.dumps(self.cache_data, indent=2, default=str),
            encoding="utf-8"
        )
    
    def is_cache_valid(self, current_checksums: Dict) -> bool:
        """
        Check if cached data is still valid.
        
        Args:
            current_checksums: Current sprint checksums.
            
        Returns:
            True if cache is valid, False otherwise.
        """
        if not self.cache_data:
            return False
        
        cached_checksums = self.cache_data.get("sprint_checksums", {})
        
        # If sprint count changed, cache is invalid
        if len(cached_checksums) != len(current_checksums):
            return False
        
        # If any sprint changed, cache is invalid
        for sprint_id, checksum in current_checksums.items():
            if cached_checksums.get(sprint_id) != checksum:
                return False
        
        return True
    
    def get_cached_metrics(self) -> Optional[Dict]:
        """
        Get cached metrics if available.
        
        Returns:
            Cached metrics dictionary or None if not available.
        """
        return self.cache_data.get("metrics")
    
    def get_cache_age(self) -> Optional[str]:
        """
        Get age of cached data.
        
        Returns:
            Human-readable cache age or None if no cache.
        """
        if not self.cache_data:
            return None
        
        last_calc = self.cache_data.get("last_calculated")
        if not last_calc:
            return None
        
        try:
            cached_time = datetime.fromisoformat(last_calc)
            age = datetime.now() - cached_time
            
            if age.days > 0:
                return f"{age.days} day{'s' if age.days > 1 else ''} ago"
            elif age.seconds >= 3600:
                hours = age.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif age.seconds >= 60:
                minutes = age.seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                return "just now"
        except:
            return None
    
    def clear_cache(self):
        """Clear cached data."""
        if self.cache_file.exists():
            self.cache_file.unlink()
        self.cache_data = {}


def calculate_sprint_checksum(sprint_folder: Path) -> str:
    """
    Calculate checksum for a sprint folder to detect changes.
    
    Args:
        sprint_folder: Path to sprint directory.
        
    Returns:
        MD5 checksum string.
    """
    # Combine modification times of key files
    files = ["project.md", "plan.md", "implementation.md", "retrospective.md"]
    checksum_data = []
    
    for file_name in files:
        file_path = sprint_folder / file_name
        if file_path.exists():
            try:
                mtime = file_path.stat().st_mtime
                checksum_data.append(f"{file_name}:{mtime}")
            except OSError:
                pass
    
    # If no files found, use folder name
    if not checksum_data:
        checksum_data.append(sprint_folder.name)
    
    combined = "|".join(checksum_data)
    return hashlib.md5(combined.encode()).hexdigest()


def calculate_all_checksums(sprint_folders: list) -> Dict[str, str]:
    """
    Calculate checksums for all sprint folders.
    
    Args:
        sprint_folders: List of Path objects for sprint directories.
        
    Returns:
        Dictionary mapping sprint_id to checksum.
    """
    checksums = {}
    for folder in sprint_folders:
        sprint_id = folder.name
        checksums[sprint_id] = calculate_sprint_checksum(folder)
    
    return checksums

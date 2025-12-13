"""
High-level analytics API that orchestrates parsing, calculation, and caching.
"""

from pathlib import Path
from typing import Dict, Optional
from .sprint_parser import scan_sprint_folders, parse_all_sprints
from .metrics_calculator import MetricsCalculator
from .analytics_cache import AnalyticsCache, calculate_all_checksums


def get_metrics(
    stride_dir: Optional[Path] = None,
    use_cache: bool = True,
    force_refresh: bool = False
) -> Dict:
    """
    Get sprint metrics with intelligent caching.
    
    Args:
        stride_dir: Path to .stride directory. Defaults to current directory.
        use_cache: Whether to use cached data if available.
        force_refresh: Force recalculation even if cache is valid.
        
    Returns:
        Dictionary containing all calculated metrics.
    """
    if stride_dir is None:
        stride_dir = Path.cwd() / ".stride"
    
    # Initialize cache
    cache = AnalyticsCache(stride_dir / "analytics.json")
    
    # Scan sprint folders
    sprint_folders = scan_sprint_folders(stride_dir)
    
    if not sprint_folders:
        # No sprints found
        return {
            "counts": {"total_sprints": 0},
            "duration": {"has_duration_data": False},
            "tasks": {"total_tasks": 0},
            "quality": {"process_adoption_rate": 0},
            "trends": {"has_trend_data": False},
            "summary": {
                "health_score": 0,
                "productivity_level": "none",
                "process_maturity": "none",
                "overall_status": "no_data"
            },
        }
    
    # Calculate current checksums
    current_checksums = calculate_all_checksums(sprint_folders)
    
    # Try to use cache if requested
    if use_cache and not force_refresh and cache.is_cache_valid(current_checksums):
        cached_metrics = cache.get_cached_metrics()
        if cached_metrics:
            return cached_metrics
    
    # Calculate fresh metrics
    sprint_data = parse_all_sprints(stride_dir)
    calculator = MetricsCalculator(sprint_data)
    metrics = calculator.calculate_all_metrics()
    
    # Save to cache
    cache.save_cache(metrics, current_checksums)
    
    return metrics


def get_sprint_summary(sprint_id: str, stride_dir: Optional[Path] = None) -> Optional[Dict]:
    """
    Get summary metrics for a specific sprint.
    
    Args:
        sprint_id: Sprint identifier (e.g., "sprint-001").
        stride_dir: Path to .stride directory. Defaults to current directory.
        
    Returns:
        Dictionary with sprint metrics or None if not found.
    """
    if stride_dir is None:
        stride_dir = Path.cwd() / ".stride"
    
    sprint_folders = scan_sprint_folders(stride_dir)
    sprint_folder = next((f for f in sprint_folders if f.name == sprint_id), None)
    
    if not sprint_folder:
        return None
    
    from .sprint_parser import parse_sprint
    sprint_data = parse_sprint(sprint_folder)
    
    return {
        "sprint_id": sprint_data.sprint_id,
        "title": sprint_data.title,
        "status": sprint_data.status,
        "created_date": sprint_data.created_date.isoformat(),
        "duration_days": sprint_data.duration_days,
        "total_tasks": sprint_data.total_tasks,
        "completed_tasks": sprint_data.completed_tasks,
        "task_completion_rate": sprint_data.task_completion_rate,
        "has_planning": sprint_data.has_planning,
        "has_implementation": sprint_data.has_implementation,
        "has_retrospective": sprint_data.has_retrospective,
        "process_compliance_score": sprint_data.process_compliance_score,
    }


def clear_analytics_cache(stride_dir: Optional[Path] = None):
    """
    Clear the analytics cache.
    
    Args:
        stride_dir: Path to .stride directory. Defaults to current directory.
    """
    if stride_dir is None:
        stride_dir = Path.cwd() / ".stride"
    
    cache = AnalyticsCache(stride_dir / "analytics.json")
    cache.clear_cache()


def get_cache_info(stride_dir: Optional[Path] = None) -> Optional[Dict]:
    """
    Get information about the current cache.
    
    Args:
        stride_dir: Path to .stride directory. Defaults to current directory.
        
    Returns:
        Dictionary with cache information or None if no cache.
    """
    if stride_dir is None:
        stride_dir = Path.cwd() / ".stride"
    
    cache = AnalyticsCache(stride_dir / "analytics.json")
    
    if not cache.cache_data:
        return None
    
    return {
        "last_calculated": cache.cache_data.get("last_calculated"),
        "sprint_count": cache.cache_data.get("sprint_count"),
        "cache_age": cache.get_cache_age(),
    }

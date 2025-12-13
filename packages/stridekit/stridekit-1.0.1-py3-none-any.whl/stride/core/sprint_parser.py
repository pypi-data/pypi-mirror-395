"""
Sprint parser for extracting data from sprint files.
"""

import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
from ..models import SprintData


def scan_sprint_folders(stride_dir: Optional[Path] = None) -> List[Path]:
    """
    Scan and return all sprint directories.
    
    Args:
        stride_dir: Path to .stride directory. Defaults to current directory.
        
    Returns:
        List of Path objects for sprint directories.
    """
    if stride_dir is None:
        stride_dir = Path.cwd() / ".stride"
    
    sprints_dir = stride_dir / "sprints"
    
    if not sprints_dir.exists():
        return []
    
    # Find all sprint-* folders
    sprint_folders = []
    for folder in sprints_dir.iterdir():
        if folder.is_dir() and folder.name.startswith("sprint-"):
            sprint_folders.append(folder)
    
    # Sort by sprint number
    return sorted(sprint_folders, key=lambda p: _extract_sprint_number(p.name))


def _extract_sprint_number(sprint_id: str) -> int:
    """Extract numeric part from sprint-XXX."""
    match = re.search(r'sprint-(\d+)', sprint_id)
    return int(match.group(1)) if match else 0


def parse_sprint(sprint_folder: Path) -> SprintData:
    """
    Parse a sprint folder and extract all data.
    
    Args:
        sprint_folder: Path to sprint directory.
        
    Returns:
        SprintData object with all extracted information.
    """
    sprint_id = sprint_folder.name
    
    # Parse individual files
    project_data = _parse_project_file(sprint_folder / "project.md")
    plan_data = _parse_plan_file(sprint_folder / "plan.md")
    impl_data = _parse_implementation_file(sprint_folder / "implementation.md")
    retro_data = _parse_retrospective_file(sprint_folder / "retrospective.md")
    
    # Check which files exist
    files_present = []
    for file_name in ["project.md", "plan.md", "implementation.md", "retrospective.md", "design.md", "proposal.md"]:
        if (sprint_folder / file_name).exists():
            files_present.append(file_name)
    
    # Calculate duration
    duration_days = None
    if project_data.get("created_date") and project_data.get("completed_date"):
        delta = project_data["completed_date"] - project_data["created_date"]
        duration_days = delta.total_seconds() / 86400  # Convert to days
    
    # Calculate task completion rate
    total_tasks = plan_data.get("total_tasks", 0)
    completed_tasks = plan_data.get("completed_tasks", 0)
    task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return SprintData(
        sprint_id=sprint_id,
        title=project_data.get("title", sprint_id),
        description=project_data.get("description", ""),
        status=project_data.get("status", "unknown"),
        created_date=project_data.get("created_date", datetime.now()),
        completed_date=project_data.get("completed_date"),
        duration_days=duration_days,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=plan_data.get("pending_tasks", 0),
        task_completion_rate=task_completion_rate,
        has_planning=(sprint_folder / "plan.md").exists(),
        has_implementation=(sprint_folder / "implementation.md").exists(),
        has_retrospective=(sprint_folder / "retrospective.md").exists(),
        has_design=(sprint_folder / "design.md").exists(),
        has_proposal=(sprint_folder / "proposal.md").exists(),
        retrospective_length=retro_data.get("retrospective_length", 0),
        learnings_count=retro_data.get("learnings_count", 0),
        folder_path=sprint_folder,
        files_present=files_present,
    )


def _parse_project_file(file_path: Path) -> Dict:
    """
    Extract metadata from project.md.
    
    Args:
        file_path: Path to project.md
        
    Returns:
        Dictionary with extracted data.
    """
    if not file_path.exists():
        return {}
    
    content = file_path.read_text(encoding="utf-8")
    data = {}
    
    # Try YAML frontmatter first
    if content.startswith("---"):
        yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            try:
                frontmatter = yaml.safe_load(yaml_match.group(1))
                if frontmatter:
                    data.update(frontmatter)
                    
                    # Convert date strings to datetime objects
                    for date_field in ["created", "created_date", "start", "start_date"]:
                        if date_field in data and isinstance(data[date_field], str):
                            try:
                                data["created_date"] = datetime.fromisoformat(data[date_field])
                            except:
                                pass
                    
                    for date_field in ["completed", "completed_date", "end", "end_date"]:
                        if date_field in data and isinstance(data[date_field], str):
                            try:
                                data["completed_date"] = datetime.fromisoformat(data[date_field])
                            except:
                                pass
            except:
                pass
    
    # Extract title from first heading
    if "title" not in data:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            data["title"] = title_match.group(1).strip()
    
    # Extract description (text after first heading, before next heading)
    if "description" not in data:
        desc_match = re.search(r'^#\s+.+\n\n(.+?)(?:\n#{1,6}\s|\n---|\Z)', content, re.DOTALL | re.MULTILINE)
        if desc_match:
            data["description"] = desc_match.group(1).strip()[:200]  # First 200 chars
    
    # Detect status from content
    if "status" not in data:
        status_patterns = {
            "completed": [r'\[✓\].*completed', r'\[x\].*completed', r'status.*completed'],
            "active": [r'\[⚡\].*active', r'\[>\].*active', r'status.*active', r'in progress'],
            "paused": [r'\[⏸\].*paused', r'\[//\].*paused', r'status.*paused'],
            "abandoned": [r'\[✗\].*abandoned', r'\[-\].*abandoned', r'status.*abandoned'],
        }
        
        for status, patterns in status_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    data["status"] = status
                    break
            if "status" in data:
                break
    
    # Extract dates from content if not in frontmatter
    if "created_date" not in data:
        date_patterns = [
            r'created[:\s]+(\d{4}-\d{2}-\d{2})',
            r'start[:\s]+(\d{4}-\d{2}-\d{2})',
            r'date[:\s]+(\d{4}-\d{2}-\d{2})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    data["created_date"] = datetime.strptime(match.group(1), '%Y-%m-%d')
                    break
                except:
                    pass
    
    # Fallback to file modification time
    if "created_date" not in data:
        data["created_date"] = datetime.fromtimestamp(file_path.stat().st_mtime)
    
    return data


def _parse_plan_file(file_path: Path) -> Dict:
    """
    Extract task data from plan.md.
    
    Args:
        file_path: Path to plan.md
        
    Returns:
        Dictionary with task counts and completion rate.
    """
    if not file_path.exists():
        return {"total_tasks": 0, "completed_tasks": 0, "pending_tasks": 0}
    
    content = file_path.read_text(encoding="utf-8")
    
    # Find all task markers
    # Patterns: - [ ] task, - [x] task, - [X] task, * [ ] task, etc.
    all_tasks = re.findall(r'^[\s]*[-*]\s*\[(.)\]', content, re.MULTILINE)
    
    total_tasks = len(all_tasks)
    completed_tasks = sum(1 for mark in all_tasks if mark.lower() == 'x')
    pending_tasks = total_tasks - completed_tasks
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    }


def _parse_implementation_file(file_path: Path) -> Dict:
    """
    Extract implementation data.
    
    Args:
        file_path: Path to implementation.md
        
    Returns:
        Dictionary with implementation status.
    """
    if not file_path.exists():
        return {"has_implementation": False}
    
    content = file_path.read_text(encoding="utf-8")
    
    return {
        "has_implementation": True,
        "implementation_length": len(content),
    }


def _parse_retrospective_file(file_path: Path) -> Dict:
    """
    Extract learnings from retrospective.md.
    
    Args:
        file_path: Path to retrospective.md
        
    Returns:
        Dictionary with retrospective data.
    """
    if not file_path.exists():
        return {
            "has_retrospective": False,
            "retrospective_length": 0,
            "learnings_count": 0,
        }
    
    content = file_path.read_text(encoding="utf-8")
    
    # Count words (basic quality indicator)
    word_count = len(content.split())
    
    # Extract sections - count bullet points as learnings
    learnings = re.findall(r'^[\s]*[-*]\s+(.+)$', content, re.MULTILINE)
    learnings_count = len(learnings)
    
    return {
        "has_retrospective": True,
        "retrospective_length": word_count,
        "learnings_count": learnings_count,
    }


def parse_all_sprints(stride_dir: Optional[Path] = None) -> List[SprintData]:
    """
    Parse all sprints in the project.
    
    Args:
        stride_dir: Path to .stride directory. Defaults to current directory.
        
    Returns:
        List of SprintData objects.
    """
    sprint_folders = scan_sprint_folders(stride_dir)
    return [parse_sprint(folder) for folder in sprint_folders]

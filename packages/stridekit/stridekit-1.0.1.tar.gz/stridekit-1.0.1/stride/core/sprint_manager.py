"""
Logic for managing sprints (CRUD operations).
"""

from typing import List, Optional
from pathlib import Path
from datetime import datetime
from ..models import Sprint, SprintProgress, StrideTask, CheckboxItem, ImplementationLogEntry
from ..constants import (
    SprintStatus, 
    STRIDE_DIR, 
    SPRINTS_DIR,
    FILE_PROPOSAL,
    FILE_PLAN,
    FILE_DESIGN,
    FILE_IMPLEMENTATION,
    FILE_RETROSPECTIVE
)
from .markdown_parser import MarkdownParser

class SprintManager:
    """Manager for sprint operations."""
    
    def __init__(self, base_path: Path = Path.cwd()):
        self.base_path = base_path
        self.sprints_dir = base_path / STRIDE_DIR / SPRINTS_DIR

    def _determine_status(self, sprint_path: Path) -> SprintStatus:
        if (sprint_path / FILE_RETROSPECTIVE).exists():
            return SprintStatus.COMPLETED
        if (sprint_path / FILE_IMPLEMENTATION).exists():
            return SprintStatus.ACTIVE
        if (sprint_path / FILE_PLAN).exists():
            return SprintStatus.PROPOSED
        return SprintStatus.PROPOSED

    def _extract_sprint_title(self, sprint_path: Path) -> str:
        """Extract sprint title from proposal.md."""
        proposal_path = sprint_path / FILE_PROPOSAL
        if proposal_path.exists():
            try:
                content = proposal_path.read_text(encoding='utf-8')
                title = MarkdownParser.extract_title(content)
                if title:
                    return title
            except Exception:
                pass
        return sprint_path.name
    
    def _parse_acceptance_criteria(self, sprint_path: Path) -> List[CheckboxItem]:
        """Parse acceptance criteria from proposal.md."""
        proposal_path = sprint_path / FILE_PROPOSAL
        if not proposal_path.exists():
            return []
        
        try:
            content = proposal_path.read_text(encoding='utf-8')
            section = MarkdownParser.extract_section(content, "Acceptance Criteria", level=2)
            return MarkdownParser.parse_checkboxes(section)
        except Exception:
            return []
    
    def _parse_plan_strides(self, sprint_path: Path) -> List[StrideTask]:
        """Parse strides from plan.md."""
        plan_path = sprint_path / FILE_PLAN
        if not plan_path.exists():
            return []
        
        try:
            content = plan_path.read_text(encoding='utf-8')
            stride_infos = MarkdownParser.parse_strides(content)
            
            # Convert to StrideTask models
            stride_tasks = []
            for info in stride_infos:
                stride_tasks.append(StrideTask(
                    stride_number=info.number,
                    stride_name=info.name,
                    purpose=info.purpose.strip(),
                    tasks=[CheckboxItem(text=task.text, checked=task.checked, line_number=task.line_number) 
                           for task in info.tasks],
                    completion_definition=info.completion_definition.strip()
                ))
            
            return stride_tasks
        except Exception:
            return []
    
    def _parse_implementation_logs(self, sprint_path: Path, limit: int = 5) -> List[ImplementationLogEntry]:
        """Parse recent implementation logs."""
        impl_path = sprint_path / FILE_IMPLEMENTATION
        if not impl_path.exists():
            return []
        
        try:
            content = impl_path.read_text(encoding='utf-8')
            log_infos = MarkdownParser.parse_implementation_logs(content, limit=limit)
            
            # Convert to model
            return [ImplementationLogEntry(
                timestamp=log.timestamp,
                stride_name=log.stride_name,
                tasks_addressed=log.tasks_addressed,
                decisions=log.decisions,
                notes=log.notes,
                changes=log.changes
            ) for log in log_infos]
        except Exception:
            return []
    
    def _calculate_progress(self, sprint_path: Path) -> SprintProgress:
        """Calculate overall sprint progress."""
        strides = self._parse_plan_strides(sprint_path)
        acceptance = self._parse_acceptance_criteria(sprint_path)
        
        # Calculate totals from strides
        total_tasks = sum(stride.total_tasks for stride in strides)
        completed_tasks = sum(stride.completed_tasks for stride in strides)
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
        
        # Calculate acceptance criteria
        ac_completed, ac_total, ac_percentage = MarkdownParser.calculate_completion(acceptance)
        
        return SprintProgress(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            completion_percentage=completion_percentage,
            strides=strides,
            acceptance_criteria_total=ac_total,
            acceptance_criteria_completed=ac_completed,
            acceptance_criteria_percentage=ac_percentage
        )

    def get_sprint(self, sprint_id: str, include_progress: bool = False) -> Optional[Sprint]:
        """
        Retrieve a sprint by ID.
        
        Args:
            sprint_id: The sprint identifier
            include_progress: Whether to parse and include progress data
        """
        sprint_path = self.sprints_dir / sprint_id
        if not sprint_path.exists() or not sprint_path.is_dir():
            return None
            
        status = self._determine_status(sprint_path)
        
        # Get file stats
        stat = sprint_path.stat()
        created_at = datetime.fromtimestamp(stat.st_ctime)
        updated_at = datetime.fromtimestamp(stat.st_mtime)
        
        # Extract title
        title = self._extract_sprint_title(sprint_path)
        
        # Build sprint object
        sprint = Sprint(
            id=sprint_id,
            title=title,
            status=status,
            path=str(sprint_path),
            created_at=created_at,
            updated_at=updated_at
        )
        
        # Add progress data if requested
        if include_progress:
            sprint.progress = self._calculate_progress(sprint_path)
            sprint.acceptance_criteria = self._parse_acceptance_criteria(sprint_path)
            sprint.recent_logs = self._parse_implementation_logs(sprint_path, limit=5)
        
        return sprint
    
    def get_sprint_details(self, sprint_id: str) -> Optional[Sprint]:
        """Retrieve a sprint with full details including progress."""
        return self.get_sprint(sprint_id, include_progress=True)

    def list_sprints(self) -> List[Sprint]:
        """List all sprints."""
        if not self.sprints_dir.exists():
            return []
            
        sprints = []
        for item in self.sprints_dir.iterdir():
            if item.is_dir():
                sprint = self.get_sprint(item.name)
                if sprint:
                    sprints.append(sprint)
        
        # Sort by creation time, newest first
        sprints.sort(key=lambda x: x.created_at, reverse=True)
        return sprints

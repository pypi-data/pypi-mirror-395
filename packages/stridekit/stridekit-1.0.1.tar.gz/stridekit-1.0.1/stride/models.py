"""
Pydantic data models for Stride entities.
"""

from datetime import datetime
from typing import List, Optional
from pathlib import Path
from dataclasses import dataclass
from pydantic import BaseModel, Field
from .constants import SprintStatus


class CheckboxItem(BaseModel):
    """Model representing a checkbox item from markdown."""
    text: str
    checked: bool
    line_number: int = 0


class StrideTask(BaseModel):
    """Model representing a stride milestone with tasks."""
    stride_number: int
    stride_name: str
    purpose: str = ""
    tasks: List[CheckboxItem] = Field(default_factory=list)
    completion_definition: str = ""
    
    @property
    def completed_tasks(self) -> int:
        """Count of completed tasks."""
        return sum(1 for task in self.tasks if task.checked)
    
    @property
    def total_tasks(self) -> int:
        """Total number of tasks."""
        return len(self.tasks)
    
    @property
    def completion_percentage(self) -> float:
        """Percentage of tasks completed."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100


class SprintProgress(BaseModel):
    """Model representing overall sprint progress."""
    total_tasks: int = 0
    completed_tasks: int = 0
    completion_percentage: float = 0.0
    strides: List[StrideTask] = Field(default_factory=list)
    acceptance_criteria_total: int = 0
    acceptance_criteria_completed: int = 0
    acceptance_criteria_percentage: float = 0.0
    
    @property
    def current_stride(self) -> Optional[StrideTask]:
        """Get the current stride being worked on (first incomplete stride)."""
        for stride in self.strides:
            if stride.completed_tasks < stride.total_tasks:
                return stride
        return None


class ImplementationLogEntry(BaseModel):
    """Model representing an implementation log entry."""
    timestamp: str
    stride_name: str
    tasks_addressed: List[str] = Field(default_factory=list)
    decisions: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    changes: List[str] = Field(default_factory=list)


class Sprint(BaseModel):
    """Model representing a single sprint."""
    id: str
    title: str
    status: SprintStatus
    path: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    progress: Optional[SprintProgress] = None
    acceptance_criteria: List[CheckboxItem] = Field(default_factory=list)
    recent_logs: List[ImplementationLogEntry] = Field(default_factory=list)


class Project(BaseModel):
    """Model representing the Stride project configuration."""
    name: str
    version: str = "0.1.0"


@dataclass
class SprintData:
    """Data class for sprint analytics."""
    sprint_id: str
    title: str
    description: str
    status: str
    created_date: datetime
    completed_date: Optional[datetime]
    duration_days: Optional[float]
    
    # Task data
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    task_completion_rate: float
    
    # Process compliance
    has_planning: bool
    has_implementation: bool
    has_retrospective: bool
    has_design: bool
    has_proposal: bool
    
    # Quality indicators
    retrospective_length: int
    learnings_count: int
    
    # Metadata
    folder_path: Path
    files_present: List[str]
    
    @property
    def is_completed(self) -> bool:
        """Check if sprint is completed."""
        return self.status.lower() == "completed"
    
    @property
    def is_active(self) -> bool:
        """Check if sprint is active."""
        return self.status.lower() == "active"
    
    @property
    def process_compliance_score(self) -> float:
        """Calculate process compliance (0-100)."""
        checks = [
            self.has_planning,
            self.has_implementation,
            self.has_retrospective,
        ]
        return (sum(checks) / len(checks)) * 100

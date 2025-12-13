"""
Metrics calculator for sprint analytics.
"""

import statistics
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from ..models import SprintData


class MetricsCalculator:
    """Calculate all metrics from sprint data."""
    
    def __init__(self, sprint_data: List[SprintData]):
        """
        Initialize calculator with sprint data.
        
        Args:
            sprint_data: List of SprintData objects to analyze.
        """
        self.sprints = sprint_data
    
    def calculate_all_metrics(self) -> Dict:
        """
        Calculate all metrics at once.
        
        Returns:
            Dictionary containing all calculated metrics.
        """
        if not self.sprints:
            return self._empty_metrics()
        
        return {
            "counts": self.calculate_counts(),
            "duration": self.calculate_duration_metrics(),
            "tasks": self.calculate_task_metrics(),
            "quality": self.calculate_quality_metrics(),
            "trends": self.calculate_trends(),
            "summary": self.calculate_summary(),
        }
    
    def calculate_counts(self) -> Dict:
        """Calculate sprint count metrics."""
        total = len(self.sprints)
        
        status_counts = {}
        for sprint in self.sprints:
            status = sprint.status.lower()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        active = status_counts.get("active", 0)
        completed = status_counts.get("completed", 0)
        abandoned = status_counts.get("abandoned", 0)
        paused = status_counts.get("paused", 0)
        
        return {
            "total_sprints": total,
            "active_sprints": active,
            "completed_sprints": completed,
            "abandoned_sprints": abandoned,
            "paused_sprints": paused,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "abandonment_rate": (abandoned / total * 100) if total > 0 else 0,
            "active_ratio": (active / total * 100) if total > 0 else 0,
        }
    
    def calculate_duration_metrics(self) -> Dict:
        """Calculate duration analysis metrics."""
        durations = [s.duration_days for s in self.sprints if s.duration_days is not None and s.duration_days > 0]
        
        if not durations:
            return {
                "has_duration_data": False,
                "average_duration": 0,
                "median_duration": 0,
                "min_duration": 0,
                "max_duration": 0,
            }
        
        return {
            "has_duration_data": True,
            "average_duration": statistics.mean(durations),
            "median_duration": statistics.median(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "std_dev": statistics.stdev(durations) if len(durations) > 1 else 0,
            "durations_under_3_days": sum(1 for d in durations if d <= 3),
            "durations_3_to_7_days": sum(1 for d in durations if 3 < d <= 7),
            "durations_over_7_days": sum(1 for d in durations if d > 7),
            "fastest_sprint": self._find_sprint_by_duration(min(durations)),
            "slowest_sprint": self._find_sprint_by_duration(max(durations)),
        }
    
    def calculate_task_metrics(self) -> Dict:
        """Calculate task and productivity metrics."""
        total_tasks = sum(s.total_tasks for s in self.sprints)
        completed_tasks = sum(s.completed_tasks for s in self.sprints)
        pending_tasks = sum(s.pending_tasks for s in self.sprints)
        
        # Calculate average for completed sprints only
        completed_sprints = [s for s in self.sprints if s.is_completed]
        
        if completed_sprints:
            avg_tasks = sum(s.total_tasks for s in completed_sprints) / len(completed_sprints)
            avg_completed = sum(s.completed_tasks for s in completed_sprints) / len(completed_sprints)
            sprint_velocity = avg_completed
        else:
            avg_tasks = 0
            avg_completed = 0
            sprint_velocity = 0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "task_completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "average_tasks_per_sprint": avg_tasks,
            "average_completed_per_sprint": avg_completed,
            "sprint_velocity": sprint_velocity,
        }
    
    def calculate_quality_metrics(self) -> Dict:
        """Calculate process and quality indicators."""
        total = len(self.sprints)
        
        with_planning = sum(1 for s in self.sprints if s.has_planning)
        with_impl = sum(1 for s in self.sprints if s.has_implementation)
        with_retro = sum(1 for s in self.sprints if s.has_retrospective)
        with_design = sum(1 for s in self.sprints if s.has_design)
        with_proposal = sum(1 for s in self.sprints if s.has_proposal)
        
        # Calculate average retrospective length
        retros = [s.retrospective_length for s in self.sprints if s.has_retrospective]
        avg_retro_length = statistics.mean(retros) if retros else 0
        
        # Calculate average learnings
        learnings = [s.learnings_count for s in self.sprints if s.has_retrospective]
        avg_learnings = statistics.mean(learnings) if learnings else 0
        
        return {
            "sprints_with_planning": with_planning,
            "sprints_with_implementation": with_impl,
            "sprints_with_retrospective": with_retro,
            "sprints_with_design": with_design,
            "sprints_with_proposal": with_proposal,
            "planning_coverage": (with_planning / total * 100) if total > 0 else 0,
            "implementation_coverage": (with_impl / total * 100) if total > 0 else 0,
            "retrospective_coverage": (with_retro / total * 100) if total > 0 else 0,
            "process_adoption_rate": ((with_planning + with_impl + with_retro) / (total * 3) * 100) if total > 0 else 0,
            "average_retrospective_length": avg_retro_length,
            "average_learnings_count": avg_learnings,
        }
    
    def calculate_trends(self) -> Dict:
        """Calculate historical trends."""
        if not self.sprints:
            return {"has_trend_data": False}
        
        # Sort by creation date
        sorted_sprints = sorted(self.sprints, key=lambda s: s.created_date)
        
        # Calculate sprints per time period
        now = datetime.now()
        
        # Last 7 days
        last_7_days = sum(1 for s in sorted_sprints if (now - s.created_date).days <= 7)
        
        # Last 30 days
        last_30_days = sum(1 for s in sorted_sprints if (now - s.created_date).days <= 30)
        
        # Last 90 days
        last_90_days = sum(1 for s in sorted_sprints if (now - s.created_date).days <= 90)
        
        # Group by week
        weeks = {}
        for sprint in sorted_sprints:
            week = sprint.created_date.strftime("%Y-W%U")
            weeks[week] = weeks.get(week, 0) + 1
        
        # Group by month
        months = {}
        for sprint in sorted_sprints:
            month = sprint.created_date.strftime("%Y-%m")
            months[month] = months.get(month, 0) + 1
        
        # Calculate velocity trend
        velocity_trend = self._calculate_velocity_trend(sorted_sprints)
        
        # Calculate completion rate trend
        completion_trend = self._calculate_completion_trend(sorted_sprints)
        
        return {
            "has_trend_data": True,
            "sprints_last_7_days": last_7_days,
            "sprints_last_30_days": last_30_days,
            "sprints_last_90_days": last_90_days,
            "sprints_by_week": weeks,
            "sprints_by_month": months,
            "velocity_trend": velocity_trend,
            "completion_rate_trend": completion_trend,
        }
    
    def calculate_summary(self) -> Dict:
        """Calculate high-level summary metrics."""
        counts = self.calculate_counts()
        duration = self.calculate_duration_metrics()
        tasks = self.calculate_task_metrics()
        quality = self.calculate_quality_metrics()
        
        health_score = self._calculate_health_score(counts, tasks, quality)
        productivity_level = self._assess_productivity(tasks)
        process_maturity = self._assess_process_maturity(quality)
        
        return {
            "health_score": health_score,
            "productivity_level": productivity_level,
            "process_maturity": process_maturity,
            "overall_status": self._assess_overall_status(health_score),
        }
    
    # Helper methods
    
    def _empty_metrics(self) -> Dict:
        """Return empty metrics structure."""
        return {
            "counts": {"total_sprints": 0},
            "duration": {"has_duration_data": False},
            "tasks": {"total_tasks": 0},
            "quality": {"process_adoption_rate": 0},
            "trends": {"has_trend_data": False},
            "summary": {"health_score": 0, "productivity_level": "none"},
        }
    
    def _find_sprint_by_duration(self, duration: float) -> str:
        """Find sprint ID with specific duration."""
        for sprint in self.sprints:
            if sprint.duration_days == duration:
                return sprint.sprint_id
        return "unknown"
    
    def _calculate_velocity_trend(self, sorted_sprints: List[SprintData]) -> str:
        """Calculate if velocity is improving, stable, or declining."""
        if len(sorted_sprints) < 4:
            return "insufficient_data"
        
        # Compare recent sprints to older ones
        midpoint = len(sorted_sprints) // 2
        older_sprints = sorted_sprints[:midpoint]
        recent_sprints = sorted_sprints[midpoint:]
        
        older_velocity = statistics.mean([s.completed_tasks for s in older_sprints if s.completed_tasks > 0])
        recent_velocity = statistics.mean([s.completed_tasks for s in recent_sprints if s.completed_tasks > 0])
        
        if recent_velocity > older_velocity * 1.1:
            return "improving"
        elif recent_velocity < older_velocity * 0.9:
            return "declining"
        else:
            return "stable"
    
    def _calculate_completion_trend(self, sorted_sprints: List[SprintData]) -> str:
        """Calculate if completion rate is improving."""
        if len(sorted_sprints) < 4:
            return "insufficient_data"
        
        midpoint = len(sorted_sprints) // 2
        older_sprints = sorted_sprints[:midpoint]
        recent_sprints = sorted_sprints[midpoint:]
        
        older_rate = sum(1 for s in older_sprints if s.is_completed) / len(older_sprints) * 100
        recent_rate = sum(1 for s in recent_sprints if s.is_completed) / len(recent_sprints) * 100
        
        if recent_rate > older_rate * 1.1:
            return "improving"
        elif recent_rate < older_rate * 0.9:
            return "declining"
        else:
            return "stable"
    
    def _calculate_health_score(self, counts: Dict, tasks: Dict, quality: Dict) -> int:
        """Calculate overall project health score (0-100)."""
        score = 0
        
        # Completion rate contributes 40%
        completion_rate = counts.get("completion_rate", 0)
        score += completion_rate * 0.4
        
        # Task completion rate contributes 30%
        task_completion = tasks.get("task_completion_rate", 0)
        score += task_completion * 0.3
        
        # Process adoption contributes 20%
        process_adoption = quality.get("process_adoption_rate", 0)
        score += process_adoption * 0.2
        
        # Low abandonment rate contributes 10%
        abandonment = counts.get("abandonment_rate", 0)
        score += (100 - abandonment) * 0.1
        
        return int(score)
    
    def _assess_productivity(self, tasks: Dict) -> str:
        """Assess productivity level based on velocity."""
        velocity = tasks.get("sprint_velocity", 0)
        
        if velocity >= 10:
            return "high"
        elif velocity >= 5:
            return "medium"
        elif velocity > 0:
            return "low"
        else:
            return "none"
    
    def _assess_process_maturity(self, quality: Dict) -> str:
        """Assess how well the process is being followed."""
        adoption = quality.get("process_adoption_rate", 0)
        
        if adoption >= 80:
            return "mature"
        elif adoption >= 50:
            return "developing"
        elif adoption > 0:
            return "early"
        else:
            return "none"
    
    def _assess_overall_status(self, health_score: int) -> str:
        """Assess overall project status."""
        if health_score >= 80:
            return "excellent"
        elif health_score >= 60:
            return "good"
        elif health_score >= 40:
            return "fair"
        else:
            return "needs_improvement"

"""
Validation logic for sprint documents.
"""

from typing import Dict, List, Set, Tuple
from pathlib import Path
import re
from ..models import Sprint
from ..constants import (
    FILE_PROPOSAL, FILE_PLAN, FILE_DESIGN, FILE_IMPLEMENTATION, 
    FILE_RETROSPECTIVE, SprintStatus
)


class TemplateStructure:
    """Defines the expected structure for each sprint file type."""
    
    # Required sections for each file type (H2 headers)
    PROPOSAL_SECTIONS = [
        "Why",
        "What",
        "Acceptance Criteria",
        "Success Definition",
        "Impact"
    ]
    
    PLAN_SECTIONS = [
        "Overview",
        "Strides",
        "Approach",
        "Dependencies",
        "Risks"
    ]
    
    DESIGN_SECTIONS = [
        "Architecture",
        "Data Flow",
        "APIs / Interfaces",
        "Data Models"
    ]
    
    IMPLEMENTATION_SECTIONS = [
        "Timestamp:",  # Special case - looking for timestamped entries
    ]
    
    RETROSPECTIVE_SECTIONS = [
        "What Worked",
        "What Didn't",
        "Lessons Learned",
        "Recommendations"
    ]
    
    # Optional but recommended sections
    PROPOSAL_OPTIONAL = ["Dependencies", "Risks & Assumptions", "Milestone Alignment"]
    PLAN_OPTIONAL = ["Validation Plan", "Completion Conditions"]
    DESIGN_OPTIONAL = ["Decisions & Trade-offs", "Security & Compliance Considerations"]
    RETROSPECTIVE_OPTIONAL = ["Project Context Updates"]


class Validator:
    """Validator for sprint documents with template verification."""
    
    def __init__(self):
        self.template = TemplateStructure()
    
    def validate_sprint(self, sprint: Sprint) -> Dict[str, List[str]]:
        """
        Validate a sprint's documents against templates.
        Returns a dictionary of errors, warnings, and info.
        """
        errors = []
        warnings = []
        info = []
        sprint_path = Path(sprint.path)

        # 1. Check required files based on sprint status
        file_errors, file_warnings = self._validate_files(sprint_path, sprint.status)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

        # 2. Validate proposal.md structure
        if (sprint_path / FILE_PROPOSAL).exists():
            prop_errors, prop_warnings, prop_info = self._validate_proposal(sprint_path / FILE_PROPOSAL)
            errors.extend(prop_errors)
            warnings.extend(prop_warnings)
            info.extend(prop_info)

        # 3. Validate plan.md structure
        if (sprint_path / FILE_PLAN).exists():
            plan_errors, plan_warnings, plan_info = self._validate_plan(sprint_path / FILE_PLAN)
            errors.extend(plan_errors)
            warnings.extend(plan_warnings)
            info.extend(plan_info)

        # 4. Validate design.md structure (if exists)
        if (sprint_path / FILE_DESIGN).exists():
            design_errors, design_warnings, design_info = self._validate_design(sprint_path / FILE_DESIGN)
            errors.extend(design_errors)
            warnings.extend(design_warnings)
            info.extend(design_info)

        # 5. Validate implementation.md (if exists)
        if (sprint_path / FILE_IMPLEMENTATION).exists():
            impl_errors, impl_warnings, impl_info = self._validate_implementation(sprint_path / FILE_IMPLEMENTATION)
            errors.extend(impl_errors)
            warnings.extend(impl_warnings)
            info.extend(impl_info)

        # 6. Validate retrospective.md (if exists)
        if (sprint_path / FILE_RETROSPECTIVE).exists():
            retro_errors, retro_warnings, retro_info = self._validate_retrospective(sprint_path / FILE_RETROSPECTIVE)
            errors.extend(retro_errors)
            warnings.extend(retro_warnings)
            info.extend(retro_info)

        # 7. Cross-file consistency checks
        consistency_errors, consistency_warnings = self._validate_consistency(sprint_path, sprint.status)
        errors.extend(consistency_errors)
        warnings.extend(consistency_warnings)

        return {
            "errors": errors,
            "warnings": warnings,
            "info": info
        }
    
    def _validate_files(self, sprint_path: Path, status: SprintStatus) -> Tuple[List[str], List[str]]:
        """Validate that required files exist based on sprint status."""
        errors = []
        warnings = []
        
        # Always required
        if not (sprint_path / FILE_PROPOSAL).exists():
            errors.append(f"Missing required file: {FILE_PROPOSAL}")
        
        if not (sprint_path / FILE_PLAN).exists():
            errors.append(f"Missing required file: {FILE_PLAN}")
        
        # Status-specific requirements
        if status == SprintStatus.ACTIVE:
            if not (sprint_path / FILE_IMPLEMENTATION).exists():
                warnings.append(f"Sprint is ACTIVE but missing {FILE_IMPLEMENTATION}")
        
        if status == SprintStatus.COMPLETED:
            if not (sprint_path / FILE_IMPLEMENTATION).exists():
                errors.append(f"Sprint is COMPLETED but missing {FILE_IMPLEMENTATION}")
            if not (sprint_path / FILE_RETROSPECTIVE).exists():
                warnings.append(f"Sprint is COMPLETED but missing {FILE_RETROSPECTIVE}")
        
        # Design is optional but recommended for complex sprints
        if not (sprint_path / FILE_DESIGN).exists():
            warnings.append(f"Optional file missing: {FILE_DESIGN} (recommended for complex sprints)")
        
        return errors, warnings
    
    def _extract_sections(self, content: str) -> Set[str]:
        """Extract all H2 section headers from markdown content."""
        sections = set()
        # Match ## Header but not ### or more
        pattern = re.compile(r'^##\s+([^#\n]+)', re.MULTILINE)
        matches = pattern.findall(content)
        
        for match in matches:
            # Clean up the header text
            section = match.strip()
            # Remove markdown formatting
            section = re.sub(r'\*\*', '', section)
            sections.add(section)
        
        return sections
    
    def _validate_proposal(self, file_path: Path) -> Tuple[List[str], List[str], List[str]]:
        """Validate proposal.md structure."""
        errors = []
        warnings = []
        info = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            sections = self._extract_sections(content)
            
            # Check required sections
            missing_required = []
            for required in self.template.PROPOSAL_SECTIONS:
                if required not in sections:
                    missing_required.append(required)
            
            if missing_required:
                errors.append(f"{FILE_PROPOSAL}: Missing required sections: {', '.join(missing_required)}")
            
            # Check for acceptance criteria checkboxes
            if "Acceptance Criteria" in sections:
                if "- [ ]" not in content and "- [x]" not in content:
                    warnings.append(f"{FILE_PROPOSAL}: Acceptance Criteria section has no checkboxes")
            
            # Check for template placeholders
            if "[" in content and "]" in content:
                placeholder_pattern = re.compile(r'\[(?:Explain|Describe|State|List|Brief)[^\]]*\]')
                placeholders = placeholder_pattern.findall(content)
                if placeholders:
                    warnings.append(f"{FILE_PROPOSAL}: Contains {len(placeholders)} template placeholders that should be filled")
            
            # Check optional sections
            missing_optional = [opt for opt in self.template.PROPOSAL_OPTIONAL if opt not in sections]
            if missing_optional:
                info.append(f"{FILE_PROPOSAL}: Optional sections not included: {', '.join(missing_optional)}")
            
        except Exception as e:
            errors.append(f"{FILE_PROPOSAL}: Failed to read or parse file: {str(e)}")
        
        return errors, warnings, info
    
    def _validate_plan(self, file_path: Path) -> Tuple[List[str], List[str], List[str]]:
        """Validate plan.md structure."""
        errors = []
        warnings = []
        info = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            sections = self._extract_sections(content)
            
            # Check required sections
            missing_required = []
            for required in self.template.PLAN_SECTIONS:
                if required not in sections:
                    missing_required.append(required)
            
            if missing_required:
                errors.append(f"{FILE_PLAN}: Missing required sections: {', '.join(missing_required)}")
            
            # Check for strides
            stride_pattern = re.compile(r'###\s+\*\*Stride\s+\d+:', re.IGNORECASE)
            strides = stride_pattern.findall(content)
            if not strides:
                errors.append(f"{FILE_PLAN}: No strides defined (should have ### **Stride N: Name**)")
            else:
                info.append(f"{FILE_PLAN}: Found {len(strides)} stride(s) defined")
            
            # Check for tasks
            if "- [ ]" not in content and "- [x]" not in content:
                warnings.append(f"{FILE_PLAN}: No tasks defined (should have checkbox items)")
            else:
                task_count = content.count("- [ ]") + content.count("- [x]")
                info.append(f"{FILE_PLAN}: Found {task_count} task(s) defined")
            
            # Check for template placeholders
            placeholder_pattern = re.compile(r'\[(?:Brief|Describe|Explain|List)[^\]]*\]')
            placeholders = placeholder_pattern.findall(content)
            if placeholders:
                warnings.append(f"{FILE_PLAN}: Contains {len(placeholders)} template placeholders")
            
            # Check optional sections
            missing_optional = [opt for opt in self.template.PLAN_OPTIONAL if opt not in sections]
            if missing_optional:
                info.append(f"{FILE_PLAN}: Optional sections not included: {', '.join(missing_optional)}")
            
        except Exception as e:
            errors.append(f"{FILE_PLAN}: Failed to read or parse file: {str(e)}")
        
        return errors, warnings, info
    
    def _validate_design(self, file_path: Path) -> Tuple[List[str], List[str], List[str]]:
        """Validate design.md structure."""
        errors = []
        warnings = []
        info = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            sections = self._extract_sections(content)
            
            # Check required sections
            missing_required = []
            for required in self.template.DESIGN_SECTIONS:
                if required not in sections:
                    missing_required.append(required)
            
            if missing_required:
                warnings.append(f"{FILE_DESIGN}: Missing recommended sections: {', '.join(missing_required)}")
            
            # Check for template placeholders
            placeholder_pattern = re.compile(r'\[(?:Describe|Explain|List)[^\]]*\]')
            placeholders = placeholder_pattern.findall(content)
            if placeholders:
                warnings.append(f"{FILE_DESIGN}: Contains {len(placeholders)} template placeholders")
            
            # Check optional sections
            missing_optional = [opt for opt in self.template.DESIGN_OPTIONAL if opt not in sections]
            if missing_optional:
                info.append(f"{FILE_DESIGN}: Optional sections not included: {', '.join(missing_optional)}")
            
        except Exception as e:
            errors.append(f"{FILE_DESIGN}: Failed to read or parse file: {str(e)}")
        
        return errors, warnings, info
    
    def _validate_implementation(self, file_path: Path) -> Tuple[List[str], List[str], List[str]]:
        """Validate implementation.md structure."""
        errors = []
        warnings = []
        info = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check for timestamped entries
            timestamp_pattern = re.compile(r'##\s+\[Timestamp:', re.IGNORECASE)
            entries = timestamp_pattern.findall(content)
            
            if not entries:
                warnings.append(f"{FILE_IMPLEMENTATION}: No timestamped log entries found")
            else:
                info.append(f"{FILE_IMPLEMENTATION}: Found {len(entries)} log entry/entries")
            
            # Check for subsections in entries
            has_tasks = "### Tasks Addressed" in content
            has_decisions = "### Decisions" in content
            has_changes = "### Changes Made" in content
            
            if not has_tasks:
                warnings.append(f"{FILE_IMPLEMENTATION}: Missing '### Tasks Addressed' subsections")
            if not has_decisions:
                warnings.append(f"{FILE_IMPLEMENTATION}: Missing '### Decisions' subsections")
            if not has_changes:
                warnings.append(f"{FILE_IMPLEMENTATION}: Missing '### Changes Made' subsections")
            
            # Check for template placeholders
            if "[Stride Name]" in content or "[Task ID" in content:
                warnings.append(f"{FILE_IMPLEMENTATION}: Contains template placeholders that should be replaced")
            
        except Exception as e:
            errors.append(f"{FILE_IMPLEMENTATION}: Failed to read or parse file: {str(e)}")
        
        return errors, warnings, info
    
    def _validate_retrospective(self, file_path: Path) -> Tuple[List[str], List[str], List[str]]:
        """Validate retrospective.md structure."""
        errors = []
        warnings = []
        info = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            sections = self._extract_sections(content)
            
            # Check required sections
            missing_required = []
            for required in self.template.RETROSPECTIVE_SECTIONS:
                if required not in sections:
                    missing_required.append(required)
            
            if missing_required:
                errors.append(f"{FILE_RETROSPECTIVE}: Missing required sections: {', '.join(missing_required)}")
            
            # Check for template placeholders
            placeholder_pattern = re.compile(r'\[(?:Identify|Extract|State|Document)[^\]]*\]')
            placeholders = placeholder_pattern.findall(content)
            if placeholders:
                warnings.append(f"{FILE_RETROSPECTIVE}: Contains {len(placeholders)} template placeholders")
            
            # Check optional sections
            missing_optional = [opt for opt in self.template.RETROSPECTIVE_OPTIONAL if opt not in sections]
            if missing_optional:
                info.append(f"{FILE_RETROSPECTIVE}: Optional sections not included: {', '.join(missing_optional)}")
            
        except Exception as e:
            errors.append(f"{FILE_RETROSPECTIVE}: Failed to read or parse file: {str(e)}")
        
        return errors, warnings, info
    
    def _validate_consistency(self, sprint_path: Path, status: SprintStatus) -> Tuple[List[str], List[str]]:
        """Validate cross-file consistency."""
        errors = []
        warnings = []
        
        has_impl = (sprint_path / FILE_IMPLEMENTATION).exists()
        has_retro = (sprint_path / FILE_RETROSPECTIVE).exists()
        
        # Logical file presence checks
        if has_retro and not has_impl:
            errors.append(f"Found {FILE_RETROSPECTIVE} but missing {FILE_IMPLEMENTATION}")
        
        if status == SprintStatus.PROPOSED and has_impl:
            warnings.append(f"Sprint status is PROPOSED but {FILE_IMPLEMENTATION} exists - consider updating status")
        
        if status == SprintStatus.COMPLETED and not has_retro:
            warnings.append(f"Sprint status is COMPLETED but {FILE_RETROSPECTIVE} is missing")
        
        return errors, warnings

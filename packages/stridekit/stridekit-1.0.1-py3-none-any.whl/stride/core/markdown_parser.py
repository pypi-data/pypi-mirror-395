"""
Markdown parsing utilities for extracting structured content from sprint files.
"""

import re
from typing import List, Optional, Tuple, Dict
from datetime import datetime
from pathlib import Path


class CheckboxItem:
    """Represents a checkbox item from markdown."""

    def __init__(self, text: str, checked: bool, line_number: int = 0):
        self.text = text
        self.checked = checked
        self.line_number = line_number


class StrideInfo:
    """Represents a stride milestone from plan.md."""

    def __init__(
        self,
        number: int,
        name: str,
        purpose: str = "",
        tasks: List[CheckboxItem] = None,
        completion_definition: str = "",
    ):
        self.number = number
        self.name = name
        self.purpose = purpose
        self.tasks = tasks or []
        self.completion_definition = completion_definition


class ImplementationLogEntry:
    """Represents a single log entry from implementation.md."""

    def __init__(
        self,
        timestamp: str,
        stride_name: str,
        tasks_addressed: List[str] = None,
        decisions: List[str] = None,
        notes: List[str] = None,
        changes: List[str] = None,
    ):
        self.timestamp = timestamp
        self.stride_name = stride_name
        self.tasks_addressed = tasks_addressed or []
        self.decisions = decisions or []
        self.notes = notes or []
        self.changes = changes or []


class MarkdownParser:
    """Parser for extracting structured content from markdown files."""

    # Regex patterns
    CHECKBOX_PATTERN = re.compile(r"^\s*-\s+\[([ xX])\]\s+(.+)$")
    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")
    STRIDE_HEADING_PATTERN = re.compile(r"###\s+\*\*Stride\s+(\d+):\s+(.+?)\*\*")
    TIMESTAMP_PATTERN = re.compile(r"##\s+\[Timestamp:\s+([^\]]+)\]\s+Stride:\s+(.+)")

    @staticmethod
    def parse_checkboxes(content: str) -> List[CheckboxItem]:
        """
        Parse checkbox items from markdown content.

        Args:
            content: Markdown content containing checkboxes

        Returns:
            List of CheckboxItem objects
        """
        items = []
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            match = MarkdownParser.CHECKBOX_PATTERN.match(line)
            if match:
                check_state = match.group(1)
                text = match.group(2).strip()
                checked = check_state.lower() == "x"
                items.append(CheckboxItem(text, checked, line_num))

        return items

    @staticmethod
    def extract_section(content: str, heading: str, level: int = 2) -> str:
        """
        Extract content under a specific heading.

        Args:
            content: Full markdown content
            heading: The heading text to find
            level: Heading level (1-6)

        Returns:
            Content under that heading until next same-level heading
        """
        lines = content.split("\n")
        section_lines = []
        in_section = False
        heading_prefix = "#" * level
        target = f"{heading_prefix} {heading}"

        for line in lines:
            # Check if we've reached the target heading
            if line.strip().startswith(target):
                in_section = True
                continue

            # If we're in the section and hit another same-level heading, stop
            if in_section:
                if line.startswith(heading_prefix + " ") and not line.startswith(
                    heading_prefix + "#"
                ):
                    break
                section_lines.append(line)

        return "\n".join(section_lines).strip()

    @staticmethod
    def parse_strides(content: str) -> List[StrideInfo]:
        """
        Parse stride milestones from plan.md.

        Args:
            content: Content of plan.md

        Returns:
            List of StrideInfo objects
        """
        strides = []
        lines = content.split("\n")
        current_stride = None
        current_section = None

        i = 0
        while i < len(lines):
            line = lines[i]

            # Match stride heading
            stride_match = MarkdownParser.STRIDE_HEADING_PATTERN.match(line)
            if stride_match:
                # Save previous stride
                if current_stride:
                    strides.append(current_stride)

                # Start new stride
                number = int(stride_match.group(1))
                name = stride_match.group(2).strip()
                current_stride = StrideInfo(number, name)
                current_section = None
                i += 1
                continue

            # If we're in a stride, check for subsections
            if current_stride:
                if line.startswith("**Purpose:**"):
                    current_section = "purpose"
                    i += 1
                    continue
                elif line.startswith("**Tasks:**"):
                    current_section = "tasks"
                    i += 1
                    continue
                elif line.startswith("**Completion Definition:**"):
                    current_section = "completion"
                    i += 1
                    continue
                elif line.startswith("###") or line.startswith("---"):
                    # End of current stride
                    if line.startswith("###") and "Stride" in line:
                        # Let the next iteration handle this
                        continue
                    current_section = None

                # Add content to current section
                if current_section == "purpose" and line.strip() and not line.startswith("["):
                    current_stride.purpose += line.strip() + " "
                elif current_section == "tasks":
                    checkbox_match = MarkdownParser.CHECKBOX_PATTERN.match(line)
                    if checkbox_match:
                        check_state = checkbox_match.group(1)
                        text = checkbox_match.group(2).strip()
                        checked = check_state.lower() == "x"
                        current_stride.tasks.append(CheckboxItem(text, checked, i + 1))
                elif current_section == "completion" and line.strip() and not line.startswith("["):
                    current_stride.completion_definition += line.strip() + " "

            i += 1

        # Don't forget the last stride
        if current_stride:
            strides.append(current_stride)

        return strides

    @staticmethod
    def parse_implementation_logs(
        content: str, limit: Optional[int] = None
    ) -> List[ImplementationLogEntry]:
        """
        Parse implementation log entries from implementation.md.

        Args:
            content: Content of implementation.md
            limit: Maximum number of entries to return (most recent first)

        Returns:
            List of ImplementationLogEntry objects
        """
        entries = []
        lines = content.split("\n")
        current_entry = None
        current_section = None

        for line in lines:
            # Match timestamp heading
            timestamp_match = MarkdownParser.TIMESTAMP_PATTERN.match(line)
            if timestamp_match:
                # Save previous entry
                if current_entry:
                    entries.append(current_entry)

                # Start new entry
                timestamp = timestamp_match.group(1).strip()
                stride_name = timestamp_match.group(2).strip()
                current_entry = ImplementationLogEntry(timestamp, stride_name)
                current_section = None
                continue

            # If we're in an entry, check for subsections
            if current_entry:
                if line.startswith("### Tasks Addressed"):
                    current_section = "tasks"
                    continue
                elif line.startswith("### Decisions"):
                    current_section = "decisions"
                    continue
                elif line.startswith("### Notes"):
                    current_section = "notes"
                    continue
                elif line.startswith("### Changes Made"):
                    current_section = "changes"
                    continue
                elif line.startswith("---"):
                    current_section = None
                    continue

                # Add content to current section
                if current_section and line.strip() and line.startswith("-"):
                    item = line.strip()[1:].strip()  # Remove leading dash
                    if not item.startswith("[") and item:  # Skip template placeholders
                        if current_section == "tasks":
                            current_entry.tasks_addressed.append(item)
                        elif current_section == "decisions":
                            current_entry.decisions.append(item)
                        elif current_section == "notes":
                            current_entry.notes.append(item)
                        elif current_section == "changes":
                            current_entry.changes.append(item)

        # Don't forget the last entry
        if current_entry:
            entries.append(current_entry)

        # Return most recent first
        entries.reverse()

        if limit:
            return entries[:limit]
        return entries

    @staticmethod
    def extract_title(content: str) -> str:
        """
        Extract the title from a markdown document (first H1 heading).

        Args:
            content: Markdown content

        Returns:
            Title text or empty string if not found
        """
        lines = content.split("\n")
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                # Remove common prefixes
                title = re.sub(
                    r"^(Proposal|Plan|Implementation|Design|Retrospective):\s*", "", title
                )
                return title
        return ""

    @staticmethod
    def calculate_completion(checkboxes: List[CheckboxItem]) -> Tuple[int, int, float]:
        """
        Calculate completion statistics from a list of checkboxes.

        Args:
            checkboxes: List of CheckboxItem objects

        Returns:
            Tuple of (completed_count, total_count, percentage)
        """
        if not checkboxes:
            return 0, 0, 0.0

        total = len(checkboxes)
        completed = sum(1 for cb in checkboxes if cb.checked)
        percentage = (completed / total * 100) if total > 0 else 0.0

        return completed, total, percentage

    @staticmethod
    def group_checkboxes_by_category(content: str) -> Dict[str, List[CheckboxItem]]:
        """
        Group checkboxes by their preceding heading (category).

        Args:
            content: Markdown content with headings and checkboxes

        Returns:
            Dictionary mapping category names to checkbox lists
        """
        groups = {}
        lines = content.split("\n")
        current_category = "General"

        for line_num, line in enumerate(lines, 1):
            # Check for heading
            heading_match = MarkdownParser.HEADING_PATTERN.match(line)
            if heading_match:
                heading_text = heading_match.group(2).strip()
                # Use h3 and h4 as categories
                if heading_match.group(1) in ["###", "####"]:
                    current_category = heading_text
                    if current_category not in groups:
                        groups[current_category] = []

            # Check for checkbox
            checkbox_match = MarkdownParser.CHECKBOX_PATTERN.match(line)
            if checkbox_match:
                check_state = checkbox_match.group(1)
                text = checkbox_match.group(2).strip()
                checked = check_state.lower() == "x"

                if current_category not in groups:
                    groups[current_category] = []
                groups[current_category].append(CheckboxItem(text, checked, line_num))

        return groups

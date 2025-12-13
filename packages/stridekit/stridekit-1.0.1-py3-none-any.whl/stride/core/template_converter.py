"""
Template Converter - Converts Stride command templates to agent-specific formats.

Supports 9 different format types across 19 AI coding assistants:
1. yaml-rich-metadata: Claude, CodeBuddy, Crush, Qoder
2. yaml-name-id: Cursor, iFlow
3. yaml-arguments: Codex, Auggie, Factory
4. yaml-xml-tags: Amazon Q, OpenCode
5. yaml-auto-exec: Windsurf
6. yaml-github-copilot: GitHub Copilot
7. toml: Qwen, Gemini, Codex
8. markdown-heading: Cline, RooCode
9. no-frontmatter: KiloCode
"""

import re
from typing import Dict, Optional


class TemplateConverter:
    """
    Converts Stride command templates from base markdown format to agent-specific formats.
    """

    # Stride markers for managed content
    STRIDE_START = "<!-- STRIDE:START -->"
    STRIDE_END = "<!-- STRIDE:END -->"

    # Command display names mapping
    COMMAND_NAMES = {
        "init": "Init",
        "derive": "Derive",
        "lite": "Lite",
        "status": "Status",
        "plan": "Plan",
        "present": "Present",
        "implement": "Implement",
        "feedback": "Feedback",
        "review": "Review",
        "complete": "Complete",
    }

    @classmethod
    def convert(
        cls,
        content: str,
        format_type: str,
        command_name: str,
        agent_key: str = ""
    ) -> str:
        """
        Convert template content to specified format.

        Args:
            content: Original markdown template content
            format_type: Target format type (yaml-rich-metadata, toml, etc.)
            command_name: Command name (init, plan, etc.)
            agent_key: Agent identifier for special handling

        Returns:
            Converted content in target format
        """
        # Extract parts from original content
        description = cls._extract_description(content)
        body = cls._extract_body(content)

        # Convert based on format type
        if format_type == "yaml-rich-metadata":
            return cls._convert_yaml_rich_metadata(command_name, description, body)
        elif format_type == "yaml-name-id":
            return cls._convert_yaml_name_id(command_name, description, body)
        elif format_type == "yaml-arguments":
            if agent_key == "factory":
                return cls._convert_yaml_arguments_factory(description, body)
            else:
                return cls._convert_yaml_arguments(description, body)
        elif format_type == "yaml-xml-tags":
            if agent_key == "opencode":
                return cls._convert_yaml_xml_tags_opencode(command_name, description, body)
            else:
                return cls._convert_yaml_xml_tags_amazonq(command_name, description, body)
        elif format_type == "yaml-auto-exec":
            return cls._convert_yaml_auto_exec(description, body)
        elif format_type == "yaml-github-copilot":
            return cls._convert_yaml_github_copilot(description, body)
        elif format_type == "toml":
            return cls._convert_toml(description, body)
        elif format_type == "markdown-heading":
            return cls._convert_markdown_heading(command_name, description, body)
        elif format_type == "no-frontmatter":
            return cls._convert_no_frontmatter(body)
        else:  # yaml-basic (default)
            return content

    @classmethod
    def _extract_description(cls, content: str) -> str:
        """Extract description from YAML frontmatter."""
        match = re.search(r'^---\s*\ndescription:\s*(.+?)\s*\n---', content, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return "Stride command"

    @classmethod
    def _extract_body(cls, content: str) -> str:
        """Extract body content between STRIDE markers."""
        # Try to find content between markers
        start_marker = cls.STRIDE_START
        end_marker = cls.STRIDE_END
        
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            body = content[start_idx + len(start_marker):end_idx].strip()
            return body
        
        # Fallback: extract everything after frontmatter and $ARGUMENTS
        # Remove YAML frontmatter
        content_without_yaml = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.MULTILINE | re.DOTALL)
        # Remove $ARGUMENTS line
        content_without_args = re.sub(r'^\$ARGUMENTS\s*\n', '', content_without_yaml, flags=re.MULTILINE)
        return content_without_args.strip()

    @classmethod
    def _convert_yaml_rich_metadata(cls, command_name: str, description: str, body: str) -> str:
        """
        Format Type 1: Rich YAML metadata with name, category, tags.
        Used by: Claude, CodeBuddy, Crush, Qoder
        """
        display_name = cls.COMMAND_NAMES.get(command_name, command_name.title())
        
        return f"""---
name: Stride: {display_name}
description: {description}
category: Stride
tags: [stride, {command_name}]
---

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

    @classmethod
    def _convert_yaml_name_id(cls, command_name: str, description: str, body: str) -> str:
        """
        Format Type 2: YAML with explicit name (slash-prefixed) and id.
        Used by: Cursor, iFlow
        """
        return f"""---
name: /stride-{command_name}
id: stride-{command_name}
category: Stride
description: {description}
---

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

    @classmethod
    def _convert_yaml_arguments(cls, description: str, body: str) -> str:
        """
        Format Type 3: YAML with argument-hint.
        Used by: Codex, Auggie
        """
        return f"""---
description: {description}
argument-hint: command arguments
---

$ARGUMENTS

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

    @classmethod
    def _convert_yaml_arguments_factory(cls, description: str, body: str) -> str:
        """
        Format Type 3b: YAML with $ARGUMENTS at END of body.
        Used by: Factory Droid
        """
        return f"""---
description: {description}
argument-hint: command arguments
---

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}

$ARGUMENTS
"""

    @classmethod
    def _convert_yaml_xml_tags_amazonq(cls, command_name: str, description: str, body: str) -> str:
        """
        Format Type 4a: YAML with XML-tagged arguments.
        Used by: Amazon Q
        """
        context_map = {
            "init": "The user wants to initialize or validate their Stride project context.",
            "derive": "The user wants to derive sprint details from an existing proposal.",
            "lite": "The user wants to create a lightweight sprint without full planning.",
            "plan": "The user wants to create a detailed sprint plan.",
            "present": "The user wants to present the sprint plan for review.",
            "implement": "The user wants to implement the sprint plan.",
            "feedback": "The user wants to provide feedback on sprint progress.",
            "review": "The user wants to review sprint implementation.",
            "complete": "The user wants to mark the sprint as complete.",
            "status": "The user wants to check sprint status.",
        }
        
        context = context_map.get(command_name, f"The user wants to execute the {command_name} command.")
        
        return f"""---
description: {description}
---

{context}

<UserRequest>
  $ARGUMENTS
</UserRequest>

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

    @classmethod
    def _convert_yaml_xml_tags_opencode(cls, command_name: str, description: str, body: str) -> str:
        """
        Format Type 4b: YAML with rich context and XML-tagged arguments.
        Used by: OpenCode
        """
        context_map = {
            "init": "The user wants to initialize their Stride project. Use the stride instructions below.",
            "derive": "The user wants to derive sprint details from an existing proposal. Find the proposal and follow the instructions below.",
            "lite": "The user wants to create a lightweight sprint. Follow the stride instructions below.",
            "plan": "The user wants to create a detailed sprint plan. Follow the stride instructions below.",
            "present": "The user wants to present the sprint plan. Follow the stride instructions below.",
            "implement": "The user wants to implement the sprint. Follow the stride instructions below. If you're not sure or if ambiguous, ask for clarification from the user.",
            "feedback": "The user wants to provide sprint feedback. Follow the stride instructions below.",
            "review": "The user wants to review the sprint. Follow the stride instructions below.",
            "complete": "The user wants to complete the sprint. Follow the stride instructions below.",
            "status": "The user wants to check sprint status. Follow the stride instructions below.",
        }
        
        context = context_map.get(command_name, f"The user wants to execute the {command_name} stride command. Follow the instructions below.")
        
        return f"""---
description: {description}
---

{context}

<UserRequest>
  $ARGUMENTS
</UserRequest>

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

    @classmethod
    def _convert_yaml_auto_exec(cls, description: str, body: str) -> str:
        """
        Format Type 5: YAML with auto_execution_mode.
        Used by: Windsurf
        """
        return f"""---
description: {description}
auto_execution_mode: 3
---

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

    @classmethod
    def _convert_yaml_github_copilot(cls, description: str, body: str) -> str:
        """
        Format Type 6: GitHub Copilot format with $ARGUMENTS.
        Used by: GitHub Copilot
        """
        return f"""---
description: {description}
---

$ARGUMENTS

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

    @classmethod
    def _convert_toml(cls, description: str, body: str) -> str:
        """
        Format Type 7: TOML format with triple-quoted prompt.
        Used by: Qwen, Gemini, Codex
        """
        # Escape any triple quotes in the body
        body_escaped = body.replace('"""', r'\"\"\"')
        
        return f"""description = "{description}"

prompt = \"\"\"
{cls.STRIDE_START}
{body_escaped}
{cls.STRIDE_END}
\"\"\"
"""

    @classmethod
    def _convert_markdown_heading(cls, command_name: str, description: str, body: str) -> str:
        """
        Format Type 8: Markdown heading without YAML frontmatter.
        Used by: Cline, RooCode
        """
        display_name = cls.COMMAND_NAMES.get(command_name, command_name.title())
        
        return f"""# Stride: {display_name}

{description}

{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

    @classmethod
    def _convert_no_frontmatter(cls, body: str) -> str:
        """
        Format Type 9: No frontmatter, just content.
        Used by: KiloCode
        """
        return f"""{cls.STRIDE_START}
{body}
{cls.STRIDE_END}
"""

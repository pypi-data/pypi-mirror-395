"""
Agent Registry - Configuration for all supported AI agents.

Defines agent configurations for 20 AI agents with their specific
directory structures and file extensions.
"""

from dataclasses import dataclass, field
from typing import Dict, List


# Agent categories for UI grouping
AGENT_CATEGORIES = {
    "ai_editors": {
        "emoji": "🎯",
        "title": "AI Editors",
        "description": "A fully integrated, fresh experience",
        "agents": ["cursor", "windsurf"]
    },
    "agents": {
        "emoji": "🤖",
        "title": "Agents",
        "description": "Letting AI take control of the terminal/files",
        "agents": ["cline", "roocode", "factory", "opencode", "kilocode", "antigravity"]
    },
    "assistants": {
        "emoji": "💡",
        "title": "Assistants",
        "description": "Autocomplete and standard help",
        "agents": ["github-copilot", "amazon-q", "auggie", "iflow", "codebuddy", "costrict"]
    },
    "cli_tools": {
        "emoji": "💻",
        "title": "CLI Tools",
        "description": "Terminal junkies and scripts",
        "agents": ["gemini", "claude", "qoder", "qwen", "codex"]
    },
    "specialized": {
        "emoji": "⚡",
        "title": "Specialized",
        "description": "Unique capabilities",
        "agents": ["crush"]
    }
}


# Agents that require root-level documentation files
AGENT_ROOT_FILES = {
    "claude": "CLAUDE.md",
    "cline": "CLINE.md",
    "codebuddy": "CODEBUDDY.md",
    "costrict": "COSTRICT.md",
    "iflow": "IFLOW.md",
    "qoder": "QODER.md",
    "qwen": "QWEN.md",
}


@dataclass
class AgentConfig:
    """
    Configuration for a specific AI agent.

    Attributes:
        name: Display name of agent
        key: Unique identifier (lowercase, hyphenated)
        directory: Agent-specific directory path (e.g., ".claude/commands/stride")
        extension: File extension including dot (e.g., ".md", ".toml", ".prompt.md")
        description: Brief description of the agent
        format_type: Template format type (yaml-rich-metadata, toml, markdown-heading, etc.)
        special_handling: List of special case flags (global-install, archive-rewrite, etc.)
        filename_pattern: Filename pattern - "{command}" or "stride-{command}"
    """
    name: str
    key: str
    directory: str
    extension: str
    description: str = ""
    format_type: str = "yaml-basic"
    special_handling: List[str] = field(default_factory=list)
    filename_pattern: str = "stride-{command}"


class AgentRegistry:
    """
    Registry of all supported AI agents with their configurations.
    
    Supports 20 AI coding agents across 5 categories.
    """

    AGENTS: Dict[str, AgentConfig] = {
        # 1. Claude Code
        "claude": AgentConfig(
            name="Claude Code",
            key="claude",
            directory=".claude/commands/stride",
            extension=".md",
            description="Anthropic's Claude with code execution",
            format_type="yaml-rich-metadata",
            filename_pattern="{command}",
        ),
        # 2. Cline
        "cline": AgentConfig(
            name="Cline",
            key="cline",
            directory=".clinerules/workflows",
            extension=".md",
            description="VS Code extension for autonomous coding",
            format_type="markdown-heading",
            filename_pattern="stride-{command}",
        ),
        # 3. Auggie
        "auggie": AgentConfig(
            name="Auggie",
            key="auggie",
            directory=".augment/commands",
            extension=".md",
            description="Augment's AI coding assistant",
            format_type="yaml-arguments",
            filename_pattern="stride-{command}",
        ),
        # 4. CodeBuddy
        "codebuddy": AgentConfig(
            name="CodeBuddy",
            key="codebuddy",
            directory=".codebuddy/commands/stride",
            extension=".md",
            description="AI pair programming assistant",
            format_type="yaml-rich-metadata",
            filename_pattern="{command}",
        ),
        # 5. Costrict
        "costrict": AgentConfig(
            name="Costrict",
            key="costrict",
            directory=".cospec/openspec/commands",
            extension=".md",
            description="Constraint-based coding agent",
            format_type="yaml-arguments",
            filename_pattern="stride-{command}",
        ),
        # 6. Qoder
        "qoder": AgentConfig(
            name="Qoder",
            key="qoder",
            directory=".qoder/commands/stride",
            extension=".md",
            description="Quality-focused code generator",
            format_type="yaml-rich-metadata",
            filename_pattern="{command}",
        ),
        # 7. Qwen (TOML format)
        "qwen": AgentConfig(
            name="Qwen",
            key="qwen",
            directory=".qwen/commands",
            extension=".toml",
            description="Alibaba's Qwen coding model",
            format_type="toml",
            filename_pattern="stride-{command}",
        ),
        # 8. RooCode
        "roocode": AgentConfig(
            name="RooCode",
            key="roocode",
            directory=".roo/commands",
            extension=".md",
            description="Kangaroo-themed coding assistant",
            format_type="markdown-heading",
            filename_pattern="stride-{command}",
        ),
        # 9. Crush
        "crush": AgentConfig(
            name="Crush",
            key="crush",
            directory=".crush/commands/stride",
            extension=".md",
            description="High-performance code crusher",
            format_type="yaml-rich-metadata",
            filename_pattern="{command}",
        ),
        # 10. Cursor
        "cursor": AgentConfig(
            name="Cursor",
            key="cursor",
            directory=".cursor/commands",
            extension=".md",
            description="AI-powered code editor",
            format_type="yaml-name-id",
            filename_pattern="stride-{command}",
        ),
        # 11. Factory Droid
        "factory": AgentConfig(
            name="Factory Droid",
            key="factory",
            directory=".factory/commands",
            extension=".md",
            description="Code factory automation agent",
            format_type="yaml-arguments",
            filename_pattern="stride-{command}",
        ),
        # 12. Gemini CLI (TOML format)
        "gemini": AgentConfig(
            name="Gemini CLI",
            key="gemini",
            directory=".gemini/commands/stride",
            extension=".toml",
            description="Google's Gemini for command line",
            format_type="toml",
            filename_pattern="{command}",
        ),
        # 13. OpenCode
        "opencode": AgentConfig(
            name="OpenCode",
            key="opencode",
            directory=".opencode/command",
            extension=".md",
            description="Open-source coding agent",
            format_type="yaml-xml-tags",
            special_handling=["archive-rewrite"],
            filename_pattern="stride-{command}",
        ),
        # 14. KiloCode
        "kilocode": AgentConfig(
            name="KiloCode",
            key="kilocode",
            directory=".kilocode/workflows",
            extension=".md",
            description="Scalable code generation",
            format_type="no-frontmatter",
            filename_pattern="stride-{command}",
        ),
        # 15. Codex (TOML format)
        "codex": AgentConfig(
            name="Codex",
            key="codex",
            directory="~/.codex/prompts",
            extension=".md",
            description="OpenAI Codex integration",
            format_type="yaml-arguments",
            special_handling=["global-install"],
            filename_pattern="stride-{command}",
        ),
        # 16. GitHub Copilot (special .prompt.md extension)
        "github-copilot": AgentConfig(
            name="GitHub Copilot",
            key="github-copilot",
            directory=".github/prompts",
            extension=".prompt.md",
            description="GitHub's AI pair programmer",
            format_type="yaml-github-copilot",
            filename_pattern="stride-{command}",
        ),
        # 17. Amazon Q
        "amazon-q": AgentConfig(
            name="Amazon Q",
            key="amazon-q",
            directory=".amazonq/prompts",
            extension=".md",
            description="AWS's AI coding assistant",
            format_type="yaml-xml-tags",
            filename_pattern="stride-{command}",
        ),
        # 18. Antigravity
        "antigravity": AgentConfig(
            name="Antigravity",
            key="antigravity",
            directory=".agent/workflows",
            extension=".md",
            description="Zero-gravity coding experience",
            format_type="yaml-basic",
            filename_pattern="stride-{command}",
        ),
        # 19. Windsurf
        "windsurf": AgentConfig(
            name="Windsurf",
            key="windsurf",
            directory=".windsurf/workflows",
            extension=".md",
            description="Flow-based coding agent",
            format_type="yaml-auto-exec",
            filename_pattern="stride-{command}",
        ),
        # 20. iFlow
        "iflow": AgentConfig(
            name="iFlow",
            key="iflow",
            directory=".iflow/commands",
            extension=".md",
            description="Flow-based AI coding assistant",
            format_type="yaml-name-id",
            filename_pattern="stride-{command}",
        ),
    }

    @classmethod
    def get_agent(cls, agent_key: str) -> AgentConfig:
        """
        Get agent configuration by key.

        Args:
            agent_key: Agent identifier (e.g., "claude", "github-copilot")

        Returns:
            AgentConfig instance

        Raises:
            KeyError: If agent_key is not found
        """
        if agent_key not in cls.AGENTS:
            available = ", ".join(sorted(cls.AGENTS.keys()))
            raise KeyError(
                f"Unknown agent: '{agent_key}'. Available agents: {available}"
            )
        return cls.AGENTS[agent_key]

    @classmethod
    def list_agents(cls) -> list:
        """
        List all supported agent keys in alphabetical order.

        Returns:
            Sorted list of agent keys
        """
        return sorted(cls.AGENTS.keys())

    @classmethod
    def get_agent_names(cls) -> Dict[str, str]:
        """
        Get mapping of agent keys to display names.

        Returns:
            Dictionary mapping key -> name
        """
        return {key: config.name for key, config in cls.AGENTS.items()}
    
    @classmethod
    def get_agent_by_name(cls, name: str) -> AgentConfig:
        """
        Get agent configuration by display name.

        Args:
            name: Display name (e.g., "Claude Code")

        Returns:
            AgentConfig instance

        Raises:
            KeyError: If name is not found
        """
        for config in cls.AGENTS.values():
            if config.name == name:
                return config
        raise KeyError(f"Unknown agent name: '{name}'")

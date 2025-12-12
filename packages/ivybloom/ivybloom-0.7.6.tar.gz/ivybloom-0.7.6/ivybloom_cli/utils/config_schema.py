"""
Machine-readable configuration schema utilities for IvyBloom CLI.

This module defines descriptions and shapes for configuration keys and
builds a normalized schema merged with actual defaults from Config.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


# Descriptive metadata for config keys, independent of defaults.
# Default values are sourced from Config.defaults at runtime to avoid drift.
CONFIG_DESCRIPTIONS: Dict[str, Dict[str, Any]] = {
    "api_url": {
        "type": "string",
        "description": "Base API endpoint for all requests.",
        "env_vars": ["IVY_ORCHESTRATOR_URL", "IVYBLOOM_API_URL"],
        "group": "endpoints",
    },
    "frontend_url": {
        "type": "string",
        "description": "Web app URL used for browser auth and link checks.",
        "env_vars": ["IVY_FRONTEND_URL"],
        "group": "endpoints",
    },
    "output_format": {
        "type": "string",
        "description": "Default output format for commands.",
        "choices": ["json", "yaml", "table", "csv"],
        "group": "display",
    },
    "theme": {
        "type": "string",
        "description": "CLI theme for visual output.",
        "choices": ["light", "dark"],
        "group": "display",
    },
    "show_welcome": {
        "type": "boolean",
        "description": "Show welcome screen at startup.",
        "group": "display",
    },
    "timeout": {
        "type": "integer",
        "description": "Request timeout in seconds.",
        "group": "network",
    },
    "retries": {
        "type": "integer",
        "description": "Retry attempts for transient failures.",
        "group": "network",
    },
    "debug": {
        "type": "boolean",
        "description": "Enable verbose debug logging.",
        "env_vars": ["IVYBLOOM_DEBUG"],
        "group": "diagnostics",
    },
    "disable_keyring": {
        "type": "boolean",
        "description": "Disable OS keyring; use file-based credentials.",
        "group": "security",
    },
    "tui_refresh_interval_secs": {
        "type": "integer",
        "description": "Refresh interval (seconds) for TUI follow screens.",
        "group": "tui",
    },
    "tui_test_preview_max_chars": {
        "type": "integer",
        "description": "Max characters in TUI test preview output.",
        "group": "tui",
    },
    "cli_test_preview_max_chars": {
        "type": "integer",
        "description": "Max characters in CLI test preview output.",
        "group": "cli",
    },
    # Nested: visualization.*
    "visualization.prefer_flatprot": {
        "type": "boolean",
        "description": "Prefer FlatProt for structure visuals.",
        "group": "visualization",
    },
    "visualization.flatprot_output_format": {
        "type": "string",
        "description": "FlatProt image format.",
        "choices": ["svg", "png"],
        "group": "visualization",
    },
    "visualization.flatprot_auto_open": {
        "type": "boolean",
        "description": "Auto-open generated visualizations.",
        "group": "visualization",
    },
    "visualization.viewer_command": {
        "type": "string",
        "description": "Custom viewer command for artifacts.",
        "group": "visualization",
    },
    # env map
    "env": {
        "type": "object",
        "description": "Optional map of environment overrides (e.g., IVY_ORCHESTRATOR_URL, IVY_FRONTEND_URL, ENVIRONMENT).",
        "group": "advanced",
    },
    # Not in defaults by design; exposed for completeness.
    "default_project_id": {
        "type": "string",
        "description": "Default project used when not provided on commands.",
        "group": "projects",
    },
}


def _get_from_defaults(defaults: Dict[str, Any], key_path: str) -> Any:
    parts = key_path.split(".")
    value: Any = defaults
    for p in parts:
        if not isinstance(value, dict) or p not in value:
            return None
        value = value[p]
    return value


def build_config_schema(defaults: Dict[str, Any]) -> Dict[str, Any]:
    """Build a normalized, machine-readable schema merged with provided defaults.

    Returns a dict with schema metadata and an ordered list of key descriptors.
    """
    keys: List[Dict[str, Any]] = []
    for key_path, meta in CONFIG_DESCRIPTIONS.items():
        entry: Dict[str, Any] = {
            "key": key_path,
            "type": meta.get("type", "string"),
            "description": meta.get("description", ""),
        }
        default_value = _get_from_defaults(defaults, key_path)
        entry["default"] = default_value
        if "choices" in meta:
            entry["choices"] = list(meta["choices"])  # shallow copy
        if "env_vars" in meta:
            entry["env_vars"] = list(meta["env_vars"])  # shallow copy
        if "group" in meta:
            entry["group"] = meta["group"]
        keys.append(entry)

    schema: Dict[str, Any] = {
        "schema_version": 1,
        "name": "ivybloom-cli-config",
        "keys": keys,
    }
    return schema



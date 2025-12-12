"""
Tool-related API helpers.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Union

from .base import APIClientError, JSONDict


class ToolsClientMixin:
    """Mixin providing tool endpoints."""

    def list_tools(self, verbose: bool = False) -> List[Dict[str, Any]]:
        """List available tools."""
        params = {"verbose": True} if verbose else None
        data: Union[JSONDict, List[JSONDict]] = self.get("/api/cli/tools", params=params)
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            return [data]
        return []

    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """Get schema for a specific tool."""
        try:
            return self.get(f"/api/cli/tools/{tool_name}/schema")
        except Exception:
            pass

        tools_verbose = self.list_tools(verbose=True)
        if not isinstance(tools_verbose, list):
            raise APIClientError(
                "Unexpected response while loading tools list for schema"
            )

        def normalize(value: Any) -> str:
            return str(value).strip().lower() if value is not None else ""

        target = tool_name.strip().lower()
        for tool in tools_verbose:
            if not isinstance(tool, dict):
                continue
            candidates = [
                normalize(tool.get("name")),
                normalize(tool.get("id")),
                normalize(tool.get("tool")),
                normalize(tool.get("slug")),
            ]
            if target in candidates:
                schema_obj = tool.get("schema") or tool.get("parameters")
                if isinstance(schema_obj, dict):
                    return schema_obj
                if isinstance(schema_obj, str):
                    try:
                        return json.loads(schema_obj)
                    except Exception:
                        pass
                return {
                    "description": tool.get("description", ""),
                    "parameters": {},
                }

        raise APIClientError(f"Schema for tool '{tool_name}' not found in tools list")


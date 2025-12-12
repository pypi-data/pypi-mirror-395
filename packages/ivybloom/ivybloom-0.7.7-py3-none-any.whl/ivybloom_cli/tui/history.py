"""Lightweight persistence for TUI custom run history."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..utils.config import Config


class HistoryManager:
    """Persist and retrieve custom CLI run history in the user's config dir."""

    def __init__(
        self,
        config: Config,
        filename: str = "custom_run_history.json",
        max_entries: int = 50,
    ) -> None:
        """Initialize with config and optional overrides."""
        self.config = config
        self.filepath = self.config.config_dir / filename
        self.max_entries = max_entries

    def _load(self) -> List[Dict[str, Any]]:
        """Return stored history entries; empty list on error."""
        if not self.filepath.exists():
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as file_handle:
                data = json.load(file_handle)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save(self, entries: List[Dict[str, Any]]) -> None:
        """Persist history entries, swallowing errors to avoid user-facing failures."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.filepath, "w", encoding="utf-8") as file_handle:
                json.dump(entries, file_handle, indent=2)
        except Exception:
            # Fail silently; history isn't critical
            pass

    def add_entry(
        self, args: str, env_overrides: Optional[Dict[str, str]] = None
    ) -> None:
        """Append a new entry and trim to max entries."""
        entries = self._load()
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "args": args,
            "env": env_overrides or {},
        }
        entries = [entry] + entries
        if len(entries) > self.max_entries:
            entries = entries[: self.max_entries]
        self._save(entries)

    def list_entries(self) -> List[Dict[str, Any]]:
        """Return all stored entries."""
        return self._load()

    def clear(self) -> None:
        """Delete all stored entries."""
        self._save([])



"""Miscellaneous TUI helper tests for coverage."""

from __future__ import annotations

from typing import Dict

from ivybloom_cli.tui.accel import detect_capabilities
from ivybloom_cli.tui.artifact_preview import ArtifactPreviewRegistry, register_default_previewers
from ivybloom_cli.tui.smiles_visualizer import render_smiles_unicode, summarize_smiles


def test_detect_capabilities_defaults_truecolor_flag() -> None:
    caps = detect_capabilities(
        {
            "TERM": "xterm-256color",
            "TERM_PROGRAM": "WezTerm",
            "COLORTERM": "truecolor",
            "WEZTERM_EXECUTABLE": "/bin/wezterm",
        }
    )
    assert caps["truecolor"] is True
    assert caps["wezterm"] is True


def test_artifact_preview_registry_registers_defaults() -> None:
    registry = register_default_previewers(ArtifactPreviewRegistry())
    # JSON preview should return either table or string for simple payload
    result = registry.preview(b'[{"a":1,"b":2}]', "data.json", "application/json")
    assert result is not None


def test_smiles_visualizer_fallback_paths() -> None:
    # RDKit likely unavailable; ensure fallback does not raise
    text = render_smiles_unicode("C")
    assert "SMILES" in text or text
    summary = summarize_smiles("C")
    assert "SMILES" in summary



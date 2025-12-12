"""Unit tests for TUI screens helpers."""

from __future__ import annotations

from typing import Any

from ivybloom_cli.tui.screens import _resolve_selected_index


class DummyEvent:
    def __init__(self, index: Any = None, item: Any = None) -> None:
        self.index = index
        self.item = item


class DummyListView:
    def __init__(self, index: Any = None, children: list[Any] | None = None) -> None:
        self.index = index
        self.children = children or []


def test_resolve_selected_index_prefers_event_index() -> None:
    event = DummyEvent(index=2)
    lv = DummyListView(index=5)
    assert _resolve_selected_index(event, lv) == 2


def test_resolve_selected_index_falls_back_to_list_view() -> None:
    event = DummyEvent(index=None)
    lv = DummyListView(index=3)
    assert _resolve_selected_index(event, lv) == 3


def test_resolve_selected_index_scans_children_then_zero() -> None:
    child = object()
    event = DummyEvent(index=None, item=child)
    lv = DummyListView(index=None, children=[object(), child])
    assert _resolve_selected_index(event, lv) == 1

    event_missing = DummyEvent(index=None, item=None)
    lv_missing = DummyListView(index=None, children=[])
    assert _resolve_selected_index(event_missing, lv_missing) == 0



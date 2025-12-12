from __future__ import annotations

from typing import List

import pytest

from ivybloom_cli.utils import interactive


def _queue_input(responses: List[str]):
    iterator = iter(responses)

    def _inner(prompt: str) -> str:
        return next(iterator, "")

    return _inner


def test_select_from_list_returns_selection(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(interactive, "_INQUIRER_AVAILABLE", False)
    items = [
        {"id": "a", "name": "Alpha"},
        {"id": "b", "name": "Beta"},
        {"id": "c", "name": "Gamma"},
    ]
    selected = interactive.select_from_list(
        items,
        title="Pick an item",
        input_func=_queue_input(["2"]),
    )
    assert selected == "b"


def test_select_from_list_handles_empty(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(interactive, "_INQUIRER_AVAILABLE", False)
    assert (
        interactive.select_from_list([], title="Pick", input_func=_queue_input([""]))
        is None
    )


def test_confirm_action_respects_default(monkeypatch: pytest.MonkeyPatch):
    assert interactive.confirm_action(
        "Proceed?", default=True, input_func=_queue_input([""])
    )
    assert interactive.confirm_action(
        "Proceed?", default=False, input_func=_queue_input(["yes"])
    )


def test_prompt_text_with_validator(monkeypatch: pytest.MonkeyPatch):
    validator = lambda value: value.isdigit()  # noqa: E731
    assert (
        interactive.prompt_text(
            "Enter number",
            validator=validator,
            input_func=_queue_input(["abc"]),
        )
        is None
    )
    assert (
        interactive.prompt_text(
            "Enter number",
            validator=validator,
            input_func=_queue_input(["42"]),
        )
        == "42"
    )


def test_prompt_multi_select_parses_indices(monkeypatch: pytest.MonkeyPatch):
    items = [
        {"id": "a", "name": "Alpha"},
        {"id": "b", "name": "Beta"},
        {"id": "c", "name": "Gamma"},
    ]
    selected = interactive.prompt_multi_select(
        items,
        title="Pick",
        input_func=_queue_input(["1, 3, 5"]),
    )
    assert selected == ["a", "c"]

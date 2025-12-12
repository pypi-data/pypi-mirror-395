"""Interactive utilities for IvyBloom CLI.

Lightweight helpers (uses rich + themed console) for:
- List selection with optional filtering and paging
- Project/job action pickers
- Simple prompts (text, choice, multi-select)
- Rendering helpers (panel, key-value table)
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

try:
    # Optional enhanced prompts
    from InquirerPy import inquirer as _inq

    _INQUIRER_AVAILABLE = True
except Exception:
    _INQUIRER_AVAILABLE = False

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .colors import get_console

console = get_console()
InputFunc = Callable[[str], str]


def _truncate(text: Optional[str], max_len: int) -> str:
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _apply_filter(
    items: List[Dict[str, Any]],
    query: str,
    display_key: str,
    description_key: Optional[str],
) -> List[Dict[str, Any]]:
    if not query:
        return items
    lowered = query.lower()
    filtered: List[Dict[str, Any]] = []
    for item in items:
        label = str(item.get(display_key, ""))
        description = str(item.get(description_key, "")) if description_key else ""
        if lowered in label.lower() or (description_key and lowered in description.lower()):
            filtered.append(item)
    return filtered


def _render_page(
    title: str,
    subtitle: str,
    page_items: List[Dict[str, Any]],
    display_key: str,
    description_key: Optional[str],
    max_display: int,
    total_count: int,
    page: int,
    enable_search: bool,
    allow_cancel: bool,
) -> str:
    console.print()
    console.print(Panel.fit(Text(f"{title}\n{subtitle}"), border_style="blue"))

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("#", style="cyan", width=4)
    table.add_column("Item", style="white")
    if description_key:
        table.add_column("Description", style="dim")

    for idx, item in enumerate(page_items, 1):
        label = _truncate(str(item.get(display_key, "Unknown")), 60)
        row = [f"{idx}.", label]
        if description_key:
            desc = _truncate(str(item.get(description_key, "")), 80)
            row.append(desc)
        table.add_row(*row)

    console.print(table)

    if total_count > max_display:
        remaining = max(total_count - ((page + 1) * max_display), 0)
        console.print(f"[dim]... and {remaining} more items[/dim]")

    navigation: List[str] = []
    if page > 0:
        navigation.append("p=prev")
    if (page + 1) * max_display < total_count:
        navigation.append("n=next")
    if enable_search:
        navigation.append("/=search")
    if allow_cancel:
        navigation.append("q=quit")

    prompt = f"Select (1-{len(page_items)})"
    if navigation:
        prompt += f" | {', '.join(navigation)}"
    prompt += ": "
    return prompt


def select_from_list(
    items: List[Dict[str, Any]],
    title: str,
    display_key: str = "name",
    id_key: str = "id",
    description_key: Optional[str] = None,
    max_display: int = 10,
    allow_cancel: bool = True,
    enable_search: bool = True,
    *,
    input_func: InputFunc = input,
) -> Optional[str]:
    """Interactive selection from a list with optional search and paging."""
    if not items:
        console.print("[yellow]No items available for selection.[/yellow]")
        return None

    if _INQUIRER_AVAILABLE and len(items) <= 200:
        try:
            choices = [str(it.get(display_key, "")) for it in items]
            result = _inq.fuzzy(message=title, choices=choices).execute()
            for item in items:
                if str(item.get(display_key, "")) == result:
                    return str(item.get(id_key))
        except Exception:
            pass

    page = 0
    query = ""

    while True:
        filtered = _apply_filter(items, query, display_key, description_key) if enable_search else items
        if not filtered:
            console.print("[yellow]No matching items. Clearing filter.[/yellow]")
            if enable_search and query:
                query = ""
                page = 0
                continue
            return None

        total = len(filtered)
        max_page = max(0, (total - 1) // max_display)
        page = min(page, max_page)
        start = page * max_display
        end = min(start + max_display, total)
        page_items = filtered[start:end]

        if not page_items:
            console.print("[yellow]No items to display.[/yellow]")
            return None

        subtitle = f"{total} item(s)" + (f" • filter: '{query}'" if query else "")
        prompt = _render_page(
            title=title,
            subtitle=subtitle,
            page_items=page_items,
            display_key=display_key,
            description_key=description_key,
            max_display=max_display,
            total_count=total,
            page=page,
            enable_search=enable_search,
            allow_cancel=allow_cancel,
        )

        response = input_func(prompt).strip()
        lowered = response.lower()

        if allow_cancel and lowered in {"q", "quit", "exit"}:
            return None
        if lowered == "n" and page < max_page:
            page += 1
            continue
        if lowered == "p" and page > 0:
            page -= 1
            continue
        if enable_search and (response.startswith("/") or lowered == "s"):
            query = response[1:] if response.startswith("/") else input_func("Filter text: ").strip()
            page = 0
            continue

        try:
            selection = int(response)
        except ValueError:
            console.print("[red]Invalid input[/red]")
            continue

        if 1 <= selection <= len(page_items):
            selected = page_items[selection - 1]
            return str(selected.get(id_key))
        console.print(f"[red]Enter a number between 1 and {len(page_items)}[/red]")


def select_job_action(job_data: Dict[str, Any]) -> Optional[str]:
    """Pick an action to perform on a job."""
    job_id = job_data.get("job_id") or job_data.get("id", "Unknown")
    job_title = job_data.get("job_title", "Untitled")
    job_type = job_data.get("job_type") or job_data.get("tool_name", "Unknown")
    status = job_data.get("status", "Unknown")

    console.print("\n[bold cyan]Job Actions for:[/bold cyan]")
    console.print(f"  [cyan]ID:[/cyan] {job_id}")
    console.print(f"  [cyan]Title:[/cyan] {job_title}")
    console.print(f"  [cyan]Type:[/cyan] {job_type}")
    console.print(f"  [cyan]Status:[/cyan] {status}")

    actions: List[Dict[str, Any]] = [
        {
            "id": "status",
            "name": "📊 View Status",
            "description": "Show detailed job status and progress",
        }
    ]
    if status.upper() in {"COMPLETED", "SUCCESS"}:
        actions.extend(
            [
                {
                    "id": "results",
                    "name": "📄 View Results",
                    "description": "Show job results and metadata",
                },
                {
                    "id": "download",
                    "name": "📥 Download Files",
                    "description": "Download result files and artifacts",
                },
            ]
        )
    if status.upper() in {"PENDING", "PROCESSING", "STARTED"}:
        actions.extend(
            [
                {
                    "id": "follow",
                    "name": "👁️  Monitor Live",
                    "description": "Watch job progress in real-time",
                },
                {
                    "id": "cancel",
                    "name": "❌ Cancel Job",
                    "description": "Cancel the running job",
                },
            ]
        )

    return select_from_list(
        items=actions,
        title="Available Actions",
        display_key="name",
        id_key="id",
        description_key="description",
        allow_cancel=True,
    )


def select_project_action(project_data: Dict[str, Any]) -> Optional[str]:
    """Pick an action to perform on a project."""
    project_id = project_data.get("project_id") or project_data.get("id", "Unknown")
    project_name = project_data.get("name", "Untitled")

    console.print("\n[bold cyan]Project Actions for:[/bold cyan]")
    console.print(f"  [cyan]ID:[/cyan] {project_id}")
    console.print(f"  [cyan]Name:[/cyan] {project_name}")

    actions = [
        {
            "id": "info",
            "name": "ℹ️  View Details",
            "description": "Show detailed project information",
        },
        {
            "id": "jobs",
            "name": "📋 View Jobs",
            "description": "List all jobs in this project",
        },
        {
            "id": "create_job",
            "name": "🚀 Create Job",
            "description": "Run a new job in this project",
        },
    ]

    return select_from_list(
        items=actions,
        title="Available Actions",
        display_key="name",
        id_key="id",
        description_key="description",
        allow_cancel=True,
    )


def confirm_action(
    message: str,
    default: bool = False,
    *,
    input_func: InputFunc = input,
) -> bool:
    """Ask for confirmation with a y/n prompt."""
    default_text = "Y/n" if default else "y/N"
    prompt = f"{message} ({default_text}): "
    try:
        response = input_func(prompt).strip().lower()
        if not response:
            return default
        return response in {"y", "yes", "true", "1"}
    except KeyboardInterrupt:
        return False


def prompt_text(
    message: str,
    default: Optional[str] = None,
    validator: Optional[Callable[[str], bool]] = None,
    *,
    input_func: InputFunc = input,
) -> Optional[str]:
    """Prompt for a line of text with optional default and validator."""
    prompt = f"{message}"
    if default is not None:
        prompt += f" [{default}]"
    prompt += ": "
    try:
        value = input_func(prompt)
        if not value and default is not None:
            value = default
        if validator and value is not None and not validator(value):
            console.print("[red]Invalid value[/red]")
            return None
        return value
    except KeyboardInterrupt:
        return None


def prompt_choice(
    message: str,
    choices: List[str],
    default: Optional[str] = None,
    *,
    input_func: InputFunc = input,
) -> Optional[str]:
    """Prompt to select one from a list of string choices."""
    if default and default not in choices:
        default = None
    choice_text = ", ".join(choices)
    prompt = f"{message} ({choice_text})"
    if default is not None:
        prompt += f" [{default}]"
    prompt += ": "
    try:
        value = input_func(prompt).strip()
        if not value and default is not None:
            value = default
        if value not in choices:
            console.print("[red]Please choose one of the listed options[/red]")
            return None
        return value
    except KeyboardInterrupt:
        return None


def prompt_multi_select(
    items: List[Dict[str, Any]],
    title: str,
    display_key: str = "name",
    id_key: str = "id",
    description_key: Optional[str] = None,
    max_display: int = 10,
    *,
    input_func: InputFunc = input,
) -> List[str]:
    """Prompt to select multiple items via comma-separated numbers."""
    if not items:
        console.print("[yellow]No items to select[/yellow]")
        return []

    console.print(Panel.fit(Text(title), border_style="blue"))
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("#", style="cyan", width=4)
    table.add_column("Item", style="white")
    if description_key:
        table.add_column("Description", style="dim")

    display_items = items[:max_display]
    for idx, item in enumerate(display_items, 1):
        label = _truncate(str(item.get(display_key, "Unknown")), 60)
        row = [f"{idx}.", label]
        if description_key:
            desc = _truncate(str(item.get(description_key, "")), 80)
            row.append(desc)
        table.add_row(*row)
    console.print(table)

    try:
        raw = input_func(
            f"Select one or more (e.g., 1,3,4) [max {len(display_items)}]: "
        ).strip()
        if not raw:
            return []
        selected: List[str] = []
        for token in raw.split(","):
            token = token.strip()
            if not token:
                continue
            idx = int(token)
            if 1 <= idx <= len(display_items):
                selected.append(str(display_items[idx - 1].get(id_key)))
        return selected
    except (ValueError, KeyboardInterrupt):
        return []


def render_panel(title: str, lines: List[str], border_style: str = "blue") -> None:
    """Render a simple panel with multiple lines of text."""
    text = "\n".join(lines)
    console.print(Panel.fit(Text(text), title=title, border_style=border_style))


def render_kv_table(title: str, rows: List[Dict[str, str]]) -> None:
    """Render a simple key-value table."""
    table = Table(title=title)
    table.add_column("Key", style="cyan", width=24)
    table.add_column("Value", style="white")
    for row in rows:
        table.add_row(str(row.get("key", "")), str(row.get("value", "")))
    console.print(table)

"""
Schema loading, validation, and presentation helpers for `ivybloom run`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence

from rich.table import Table

from ...client.api_client import IvyBloomAPIClient
from ...utils.colors import get_console
from ...utils.printing import emit_json
from ...utils.schema_loader import (
    build_json_schema,
    get_tool_schema,
    normalize_parameters_schema,
)

console = get_console()


def _validate_parameters(params: Mapping[str, Any], schema_data: Mapping[str, Any]) -> List[str]:
    """Validate parameters against tool schema (recursive)."""
    normalized = normalize_parameters_schema(schema_data)
    properties = normalized.get("properties", {}) or {}
    required_fields = normalized.get("required", []) or []

    errors = _collect_required_errors(params, required_fields)
    errors.extend(_collect_unknown_errors(params, properties))

    for param_name, schema in properties.items():
        if param_name in params:
            errors.extend(_validate_value(params[param_name], schema or {}, param_name))
    return errors


def _collect_required_errors(
    params: Mapping[str, Any], required_fields: Sequence[str]
) -> List[str]:
    """Check required parameters at the top level."""
    errors: List[str] = []
    for required_field in required_fields:
        if required_field not in params:
            errors.append(f"Missing required parameter: {required_field}")
    return errors


def _collect_unknown_errors(
    params: Mapping[str, Any], properties: Mapping[str, Any]
) -> List[str]:
    """Ensure only known parameters are provided at the top level."""
    errors: List[str] = []
    for param_name in params.keys():
        if param_name == "__features__":
            continue
        if param_name not in properties:
            errors.append(f"Unknown parameter: {param_name}")
    return errors


def _validate_value(value: Any, schema: Mapping[str, Any], path: str) -> List[str]:
    """Validate a single value against its schema definition."""
    errors: List[str] = []
    param_type = schema.get("type")
    enum_values = schema.get("enum")
    if enum_values is not None and value not in enum_values:
        errors.append(f"{path} must be one of: {', '.join(map(str, enum_values))}")
        return errors

    errors.extend(_validate_primitive_type(value, param_type, path))
    errors.extend(_validate_numeric_bounds(value, schema, path))
    errors.extend(_validate_string_bounds(value, schema, path))
    errors.extend(_validate_array(value, schema, path))
    errors.extend(_validate_object(value, schema, path))
    return errors


def _validate_primitive_type(value: Any, param_type: str | None, path: str) -> List[str]:
    """Validate primitive type expectations."""
    if param_type == "integer" and not isinstance(value, int):
        return [f"{path} must be an integer"]
    if param_type == "number" and not isinstance(value, (int, float)):
        return [f"{path} must be a number"]
    if param_type == "boolean" and not isinstance(value, bool):
        return [f"{path} must be true or false"]
    if param_type == "string" and not isinstance(value, str):
        return [f"{path} must be a string"]
    if param_type == "array" and not isinstance(value, list):
        return [f"{path} must be an array"]
    if param_type == "object" and not isinstance(value, dict):
        return [f"{path} must be an object"]
    return []


def _validate_numeric_bounds(value: Any, schema: Mapping[str, Any], path: str) -> List[str]:
    """Validate numeric bounds when applicable."""
    errors: List[str] = []
    if isinstance(value, (int, float)):
        if "min" in schema and value < schema["min"]:
            errors.append(f"{path} must be >= {schema['min']}")
        if "max" in schema and value > schema["max"]:
            errors.append(f"{path} must be <= {schema['max']}")
    return errors


def _validate_string_bounds(value: Any, schema: Mapping[str, Any], path: str) -> List[str]:
    """Validate string length bounds when applicable."""
    errors: List[str] = []
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path} length must be >= {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path} length must be <= {schema['maxLength']}")
    return errors


def _validate_array(value: Any, schema: Mapping[str, Any], path: str) -> List[str]:
    """Validate array constraints and recurse into items."""
    errors: List[str] = []
    if not isinstance(value, list):
        return errors

    if "minItems" in schema and len(value) < schema["minItems"]:
        errors.append(f"{path} must contain at least {schema['minItems']} items")
    if "maxItems" in schema and len(value) > schema["maxItems"]:
        errors.append(f"{path} must contain at most {schema['maxItems']} items")
    items_schema = schema.get("items")
    if isinstance(items_schema, dict):
        for idx, item in enumerate(value):
            errors.extend(_validate_value(item, items_schema, f"{path}[{idx}]"))
    return errors


def _validate_object(value: Any, schema: Mapping[str, Any], path: str) -> List[str]:
    """Validate object properties, required keys, and recurse into children."""
    errors: List[str] = []
    if not isinstance(value, dict):
        return errors
    props = schema.get("properties") or {}
    required = schema.get("required") or []
    for req in required:
        if req not in value:
            errors.append(f"Missing required parameter: {path}.{req}")
    for key in value.keys():
        if props and key not in props:
            errors.append(f"Unknown parameter: {path}.{key}")
    for key, child_schema in props.items():
        if key in value:
            errors.extend(_validate_value(value[key], child_schema, f"{path}.{key}"))
    return errors


def _show_tool_schema(client: IvyBloomAPIClient, tool_name: str) -> None:
    """Display tool schema information for a given tool."""
    schema_data = get_tool_schema(tool_name, client)
    if not schema_data:
        console.print(f"[red]❌ Schema for '{tool_name}' not found[/red]")
        return

    console.print(f"[bold cyan]🧬 {tool_name.title()} - Parameter Schema[/bold cyan]")
    console.print(f"   {schema_data.get('description', 'No description available')}")
    console.print()

    normalized = normalize_parameters_schema(schema_data)
    properties = normalized.get("properties", {})
    required_fields = normalized.get("required", [])

    if properties:
        _render_schema_table(properties, required_fields)
        console.print()
        _print_example(tool_name, properties, required_fields)
    else:
        console.print("[yellow]No parameter information available[/yellow]")


def _render_schema_table(properties: Mapping[str, Any], required_fields: Sequence[str]) -> None:
    """Render parameter schema in a table."""
    table = Table(title="Parameters", show_header=True, header_style="bold cyan")
    table.add_column("Parameter", style="green")
    table.add_column("Type", style="blue")
    table.add_column("Required", style="red")
    table.add_column("Description", style="white")
    table.add_column("Default", style="dim")

    for param_name, param_info in properties.items():
        param_type = param_info.get("type", "unknown")
        description = param_info.get("description", "No description")
        is_required = "Yes" if param_name in required_fields else "No"
        default = str(param_info.get("default", "")) if "default" in param_info else ""
        if param_info.get("enum"):
            description = (
                f"{description} [choices: {', '.join(map(str, param_info['enum']))}]"
            )
        table.add_row(param_name, param_type, is_required, description, default)
    console.print(table)


def _print_example(
    tool_name: str, properties: Mapping[str, Any], required_fields: Sequence[str]
) -> None:
    """Print a short usage example using required fields."""
    console.print("[bold]Usage Example:[/bold]")
    example_params: List[str] = []
    for param_name in required_fields[:3]:
        param_info = properties.get(param_name, {})
        param_type = param_info.get("type", "string")
        example_params.append(_example_for_type(param_name, param_type))
    param_str = " ".join(example_params)
    console.print(f"  [green]ivybloom run {tool_name} {param_str}[/green]")


def _example_for_type(param_name: str, param_type: str) -> str:
    """Return a sample parameter string for the given type."""
    if param_type == "string":
        return f'{param_name}="example_value"'
    if param_type == "integer":
        return f"{param_name}=5"
    if param_type == "number":
        return f"{param_name}=1.5"
    if param_type == "boolean":
        return f"{param_name}=true"
    return f"{param_name}=value"


def _show_dry_run(
    tool_name: str,
    params: Mapping[str, Any],
    project_id: str | None,
    job_title: str | None,
) -> None:
    """Show what would be executed in a dry run."""
    console.print("[yellow]🧪 Dry Run - No job will be submitted[/yellow]")
    console.print()
    console.print(f"[bold]Tool:[/bold] {tool_name}")
    if job_title:
        console.print(f"[bold]Title:[/bold] {job_title}")
    if project_id:
        console.print(f"[bold]Project:[/bold] {project_id}")

    console.print("[bold]Parameters:[/bold]")
    if params:
        for key, value in params.items():
            console.print(f"  • {key}: {value}")
    else:
        console.print("  (none)")

    console.print()
    console.print("[green]✅ Parameter validation passed![/green]")
    console.print("[dim]Run without --dry-run to execute the job.[/dim]")


def _emit_verbose_payload(
    tool_name: str,
    tool_params: Mapping[str, Any],
    project_id: str | None,
    job_title: str | None,
    schema_data: Mapping[str, Any],
) -> None:
    """Emit verbose JSON for dry-run including schema hints."""
    payload = {
        "tool_name": tool_name,
        "parameters": tool_params,
        "project_id": project_id,
        "job_title": job_title,
        "validation": {"errors": []},
        "schema_hints": normalize_parameters_schema(schema_data),
        "json_schema": build_json_schema(schema_data),
    }
    emit_json(payload)


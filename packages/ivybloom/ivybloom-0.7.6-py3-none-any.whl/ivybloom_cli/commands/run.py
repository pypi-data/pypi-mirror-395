"""
Run command for executing individual tools.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence

import click
from rich.console import Console

from ..client.api_client import IvyBloomAPIClient
from ..utils.auth import AuthManager
from ..utils.colors import get_console, print_error, print_success, print_warning
from ..utils.schema_loader import build_json_schema, get_tool_schema, resolve_tool_name
from ..utils.printing import emit_json
from .run_helpers import (
    _emit_verbose_payload,
    _looks_like_uniprot_accession,
    _normalize_param_keys,
    _parse_feature_directives,
    _parse_parameters,
    _preprocess_tool_parameters,
    _resolve_uniprot_sequence,
    _show_dry_run,
    _show_tool_schema,
    _validate_parameters,
)

console: Console = get_console()

@click.command()
@click.argument('tool_name')
@click.argument('parameters', nargs=-1)
@click.option('--project-id', help='Project ID to run the job in')
@click.option('--job-title', help='Custom title for the job')
@click.option('--wait', is_flag=True, help='Wait for job completion')
@click.option('--dry-run', is_flag=True, help='Validate parameters without executing')
@click.option('--show-schema', is_flag=True, help='Show tool parameter schema and exit')
@click.option('--output-format', default='table', type=click.Choice(['json', 'yaml', 'table']), help='Output format')
@click.option('--json-verbose', is_flag=True, help='Print verbose JSON payload with resolved parameters and schema hints (implies --output-format json)')
@click.option('--need', 'needs', multiple=True, help='Declare required features or outputs (name or name=value). Can be repeated.')
@click.option('--want', 'wants', multiple=True, help='Declare optional features or outputs (name or name=value). Can be repeated.')
@click.option('--feature', 'features', multiple=True, help='Set feature flags (name or name=value). Can be repeated.')
@click.pass_context
def run(ctx, tool_name, parameters, project_id, job_title, wait, dry_run, show_schema, output_format, json_verbose, needs, wants, features):
    """Run a tool with parameters and feature flags."""
    config = ctx.obj['config']
    auth_manager = AuthManager(config)
    
    if not auth_manager.is_authenticated():
        console.print("[red]❌ Not authenticated. Run 'ivybloom auth login' first.[/red]")
        return
    
    try:
        _run_command_flow(
            config=config,
            auth_manager=auth_manager,
            tool_name=tool_name,
            parameters=parameters,
            project_id=project_id,
            job_title=job_title,
            wait=wait,
            dry_run=dry_run,
            show_schema=show_schema,
            output_format=output_format,
            json_verbose=json_verbose,
            needs=needs,
            wants=wants,
            features=features,
        )
    except Exception as e:
        console.print(f"[red]❌ Error executing tool: {e}[/red]")

def _run_command_flow(
    *,
    config: Any,
    auth_manager: AuthManager,
    tool_name: str,
    parameters: Sequence[str],
    project_id: Optional[str],
    job_title: Optional[str],
    wait: bool,
    dry_run: bool,
    show_schema: bool,
    output_format: str,
    json_verbose: bool,
    needs: Sequence[str],
    wants: Sequence[str],
    features: Sequence[str],
) -> None:
    """Execute the run command flow after authentication."""
    resolved_tool = _announce_alias(tool_name)
    with IvyBloomAPIClient(config, auth_manager) as client:
        if _maybe_show_schema(client, resolved_tool, show_schema):
            return

        schema_data = _load_schema(client, resolved_tool)
        if not schema_data:
            return

        tool_params = _build_tool_parameters(
            parameters=parameters,
            needs=needs,
            wants=wants,
            features=features,
            tool_name=resolved_tool,
            schema_data=schema_data,
        )
        if _handle_validation_errors(tool_params, schema_data, resolved_tool):
            return
        if _handle_dry_run(
            tool_name=resolved_tool,
            tool_params=tool_params,
            project_id=project_id,
            job_title=job_title,
            schema_data=schema_data,
            json_verbose=json_verbose,
        ):
            return

        _submit_and_render(
            client=client,
            tool_name=resolved_tool,
            tool_params=tool_params,
            project_id=project_id,
            job_title=job_title,
            wait=wait,
            output_format=output_format,
            json_verbose=json_verbose,
            schema_data=schema_data,
        )


def _build_tool_parameters(
    *,
    parameters: Sequence[str],
    needs: Sequence[str],
    wants: Sequence[str],
    features: Sequence[str],
    tool_name: str,
    schema_data: Mapping[str, Any],
) -> Dict[str, Any]:
    """Parse, normalize, and preprocess tool parameters."""
    tool_params = _normalize_param_keys(_parse_parameters(parameters))
    feature_directives = _parse_feature_directives(needs, wants, features)
    if feature_directives:
        tool_params["__features__"] = feature_directives
    return _preprocess_tool_parameters(tool_name, tool_params, schema_data)


def _render_validation_errors(errors: Sequence[str], tool_name: str) -> None:
    """Render parameter validation errors with guidance."""
    console.print("[red]❌ Parameter validation failed:[/red]")
    for error in errors:
        console.print(f"   • {error}")
    console.print()
    console.print(
        f"[dim]💡 Run 'ivybloom tools info {tool_name}' to see parameter requirements[/dim]"
    )


def _handle_dry_run(
    *,
    tool_name: str,
    tool_params: Mapping[str, Any],
    project_id: Optional[str],
    job_title: Optional[str],
    schema_data: Mapping[str, Any],
    json_verbose: bool,
) -> bool:
    """Handle dry-run output paths."""
    if json_verbose:
        _emit_verbose_payload(tool_name, tool_params, project_id, job_title, schema_data)
        return True
    _show_dry_run(tool_name, tool_params, project_id, job_title)
    return True


def _build_job_payload(
    *,
    tool_name: str,
    tool_params: Mapping[str, Any],
    project_id: Optional[str],
    job_title: Optional[str],
    wait: bool,
) -> Dict[str, Any]:
    """Assemble job submission payload."""
    job_data: Dict[str, Any] = {
        "tool_name": tool_name,
        "parameters": tool_params,
        "wait_for_completion": wait,
    }
    if project_id:
        job_data["project_id"] = project_id
    if job_title:
        job_data["job_title"] = job_title
    return job_data


def _announce_alias(tool_name: str) -> str:
    """Resolve tool aliases and display the mapping."""
    resolved_tool = resolve_tool_name(tool_name)
    if resolved_tool != tool_name:
        console.print(f"[dim]Using alias: {tool_name} → {resolved_tool}[/dim]")
    return resolved_tool


def _maybe_show_schema(
    client: IvyBloomAPIClient, tool_name: str, show_schema: bool
) -> bool:
    """Show tool schema and return True if handled."""
    if not show_schema:
        return False
    _show_tool_schema(client, tool_name)
    return True


def _load_schema(
    client: IvyBloomAPIClient, tool_name: str
) -> Optional[Mapping[str, Any]]:
    """Fetch and normalize a tool schema, rendering errors when missing."""
    schema_data = get_tool_schema(tool_name, client)
    if not schema_data:
        _render_missing_tool(tool_name)
        return None
    return schema_data


def _handle_validation_errors(
    tool_params: Mapping[str, Any],
    schema_data: Mapping[str, Any],
    tool_name: str,
) -> bool:
    """Validate parameters and render errors; return True when handled."""
    validation_errors = _validate_parameters(tool_params, schema_data)
    if validation_errors:
        _render_validation_errors(validation_errors, tool_name)
        return True
    return False


def _submit_and_render(
    *,
    client: IvyBloomAPIClient,
    tool_name: str,
    tool_params: Mapping[str, Any],
    project_id: Optional[str],
    job_title: Optional[str],
    wait: bool,
    output_format: str,
    json_verbose: bool,
    schema_data: Mapping[str, Any],
) -> None:
    """Submit a job then render the response."""
    job_data = _build_job_payload(
        tool_name=tool_name,
        tool_params=tool_params,
        project_id=project_id,
        job_title=job_title,
        wait=wait,
    )
    console.print(f"[cyan]🚀 Submitting {tool_name} job...[/cyan]")
    job_result = client.create_job(job_data)
    _render_job_response(
        client=client,
        job_result=job_result,
        output_format=output_format,
        json_verbose=json_verbose,
        job_data=job_data,
        schema_data=schema_data,
        tool_name=tool_name,
        wait=wait,
    )


def _render_job_response(
    *,
    client: IvyBloomAPIClient,
    job_result: Mapping[str, Any],
    output_format: str,
    json_verbose: bool,
    job_data: Mapping[str, Any],
    schema_data: Mapping[str, Any],
    tool_name: str,
    wait: bool,
) -> None:
    """Render job submission response based on requested format."""
    if json_verbose:
        verbose_payload = {
            "request": job_data,
            "response": job_result,
            "schema_hints": schema_data,
            "json_schema": build_json_schema(schema_data),
        }
        emit_json(verbose_payload)
        return
    if output_format == "json":
        emit_json(job_result)
        return
    if output_format == "yaml":
        import yaml

        console.print(yaml.dump(job_result, default_flow_style=False))
        return

    _render_table_summary(job_result, tool_name, job_data)
    if wait:
        console.print()
        console.print("[yellow]⏳ Waiting for job completion...[/yellow]")
        job_id = str(job_result.get("job_id", ""))
        if job_id:
            _wait_for_completion(client, job_id)


def _wait_for_completion(client: IvyBloomAPIClient, job_id: str) -> None:
    """Wait for job completion and show results."""
    from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
    import time

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Waiting for job completion...", total=None)
        while True:
            try:
                status_result = client.get_job_status(job_id)
                status = status_result.get("status", "unknown")
                if status in ["completed", "failed", "cancelled"]:
                    progress.update(task, description=f"Job {status}!")
                    time.sleep(0.5)
                    break
                progress.update(task, description=f"Job running... ({status})")
                time.sleep(3)
            except KeyboardInterrupt:
                progress.update(task, description="Cancelled by user!")
                time.sleep(0.5)
                console.print(
                    "\n[yellow]Stopped waiting, but job continues running on server.[/yellow]"
                )
                console.print(
                    f"[dim]Check status: ivybloom jobs status {job_id} --stream[/dim]"
                )
                return
            except Exception as exc:  # pragma: no cover - defensive path
                progress.update(task, description=f"Error: {exc}")
                time.sleep(1)
                return

    console.print()
    try:
        final_status = client.get_job_status(job_id)
        status = final_status.get("status")
        if status == "completed":
            print_success("🎉 Job completed successfully!")
            console.print(
                f"[dim]Get results: ivybloom jobs results {job_id} --format table[/dim]"
            )
        elif status == "failed":
            print_error("❌ Job failed!")
            console.print(
                f"[dim]Check logs: ivybloom jobs status {job_id} --stream --logs[/dim]"
            )
        else:
            print_warning(f"Job ended with status: {status}")
    except Exception as exc:  # pragma: no cover - defensive path
        console.print(f"[red]Error getting final status: {exc}[/red]")


def _render_table_summary(
    job_result: Mapping[str, Any], tool_name: str, job_data: Mapping[str, Any]
) -> None:
    """Render human-friendly summary for a job submission."""
    job_id = job_result.get("job_id", "Unknown")
    status = job_result.get("status", "unknown")
    console.print("[green]✅ Job submitted successfully![/green]")
    console.print(f"   Job ID: [cyan]{job_id}[/cyan]")
    console.print(f"   Status: [yellow]{status}[/yellow]")
    console.print(f"   Tool: [blue]{tool_name}[/blue]")
    if project_id := job_data.get("project_id"):
        console.print(f"   Project: [magenta]{project_id}[/magenta]")
    if job_title := job_data.get("job_title"):
        console.print(f"   Title: [green]{job_title}[/green]")
    console.print()
    console.print("[dim]📋 Next steps:[/dim]")
    console.print(f"   [dim]• Monitor: ivybloom jobs status {job_id} --stream[/dim]")
    console.print(f"   [dim]• Results: ivybloom jobs results {job_id}[/dim]")
    console.print(f"   [dim]• Download: ivybloom jobs download {job_id}[/dim]")


def _render_missing_tool(tool_name: str) -> None:
    """Show friendly error when tool schema cannot be found."""
    console.print(f"[red]❌ Tool '{tool_name}' not found or not available[/red]")
    console.print("Run 'ivybloom tools list' to see available tools.")

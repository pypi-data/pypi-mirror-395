"""
Exports orchestrator commands for IvyBloom CLI (optional surface)
"""

import click
from rich.console import Console

from ..utils.auth import AuthManager
from ..utils.config import Config
from ..client.api_client import IvyBloomAPIClient
from ..utils.colors import get_console
from ..utils.printing import emit_json

console = get_console()


@click.group(help="Create and retrieve multi-source exports (optional orchestrator).\n\nExamples:\n  ivybloom exports create --type project_summary --scope '{\"project_id\":\"proj_123\"}' --include jobs_table,metrics_overview --format zip\n  ivybloom exports status <export_id>\n  ivybloom exports results <export_id> --output ./results.json\n  ivybloom exports catalog")
def exports():
    """Create and retrieve multi-source exports (optional orchestrator)."""
    pass


@exports.command(help="Create an export orchestration. Supports idempotency and dry-run.")
@click.option('--type', 'export_type', required=True, help='Export type (e.g., project_summary)')
@click.option('--scope', help='JSON string for scope (e.g., {"project_id":"proj_123"})')
@click.option('--include', help='Comma-separated list of items to include')
@click.option('--format', 'fmt', default='zip', type=click.Choice(['zip', 'json']), help='Bundle format')
@click.option('--options', help='JSON string for extra options')
@click.option('--dry-run', is_flag=True, help='Plan without executing')
@click.option('--synchronous', is_flag=True, help='Attempt inline execution with short cap')
@click.option('--idempotency-key', help='Optional idempotency key to deduplicate')
@click.pass_context
def create(ctx, export_type, scope, include, fmt, options, dry_run, synchronous, idempotency_key):
    """Create an export using the orchestrator surface."""
    config = ctx.obj['config']
    auth_manager = AuthManager(config)
    if not auth_manager.is_authenticated():
        console.print("[red]❌ Not authenticated. Run 'ivybloom auth login' first.[/red]")
        return

    import json as _json
    spec = {
        "export_type": export_type,
        "format": fmt,
        "dry_run": bool(dry_run),
        "synchronous": bool(synchronous),
    }
    if scope:
        try:
            spec["scope"] = _json.loads(scope)
        except Exception:
            console.print("[red]❌ Invalid JSON for --scope[/red]")
            return
    if include:
        spec["include"] = [s.strip() for s in include.split(',') if s.strip()]
    if options:
        try:
            spec["options"] = _json.loads(options)
        except Exception:
            console.print("[red]❌ Invalid JSON for --options[/red]")
            return

    try:
        with IvyBloomAPIClient(config, auth_manager) as client:
            data = client.create_export(spec, idempotency_key=idempotency_key)
        emit_json(data)
    except Exception as e:
        console.print(f"[red]❌ Error creating export: {e}[/red]")


@exports.command(help="Get export status by export_id.")
@click.argument('export_id')
@click.pass_context
def status(ctx, export_id):
    """Get export status."""
    config = ctx.obj['config']
    auth_manager = AuthManager(config)
    if not auth_manager.is_authenticated():
        console.print("[red]❌ Not authenticated. Run 'ivybloom auth login' first.[/red]")
        return

    try:
        with IvyBloomAPIClient(config, auth_manager) as client:
            data = client.get_export_status(export_id)
        emit_json(data)
    except Exception as e:
        console.print(f"[red]❌ Error fetching export status: {e}[/red]")


@exports.command(help="Get export results (manifest and URLs). Optionally write to file.")
@click.argument('export_id')
@click.option('--output', '-o', help='Path to write results manifest JSON')
@click.pass_context
def results(ctx, export_id, output):
    """Get export results and manifest URLs."""
    config = ctx.obj['config']
    auth_manager = AuthManager(config)
    if not auth_manager.is_authenticated():
        console.print("[red]❌ Not authenticated. Run 'ivybloom auth login' first.[/red]")
        return

    try:
        with IvyBloomAPIClient(config, auth_manager) as client:
            data = client.get_export_results(export_id)
        if output:
            try:
                import json as _json
                with open(output, 'w') as f:
                    _json.dump(data, f, indent=2)
                console.print(f"[green]✅ Wrote results manifest to {output}[/green]")
                return
            except Exception as e:
                console.print(f"[yellow]⚠️ Could not write to {output}: {e}[/yellow]")
        emit_json(data)
    except Exception as e:
        console.print(f"[red]❌ Error fetching export results: {e}[/red]")


@exports.command(help="List export types and allowed items from the orchestrator.")
@click.pass_context
def catalog(ctx):
    """List export types and allowed items."""
    config = ctx.obj['config']
    auth_manager = AuthManager(config)
    if not auth_manager.is_authenticated():
        console.print("[red]❌ Not authenticated. Run 'ivybloom auth login' first.[/red]")
        return

    try:
        with IvyBloomAPIClient(config, auth_manager) as client:
            data = client.list_export_catalog()
        emit_json(data)
    except Exception as e:
        console.print(f"[red]❌ Error listing export catalog: {e}[/red]")



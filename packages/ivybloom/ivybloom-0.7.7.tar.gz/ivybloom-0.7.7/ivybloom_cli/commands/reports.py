"""
Reports/Exports commands for IvyBloom CLI (frontend unified surface)
"""

import click
from rich.console import Console

from ..utils.auth import AuthManager
from ..utils.config import Config
from ..client.api_client import IvyBloomAPIClient
from ..utils.colors import get_console
from ..utils.printing import emit_json

console = get_console()


@click.group(help="Preview, generate, and export reports via unified frontend endpoint.\n\nExamples:\n  ivybloom reports preview <job_id> --template study_summary --async\n  ivybloom reports generate <job_id> --template study_summary --format pdf --async --idempotency-key run-<job_id>-pdf\n  ivybloom reports export <job_id> --type package_zip --async --idempotency-key run-<job_id>-pkg")
def reports():
    """Preview, generate, and export reports via unified frontend endpoint."""
    pass


@reports.command(help="Preview a report for a job.\n\nPOST (with --async) triggers readiness; GET fetches preview JSON.")
@click.argument('job_id')
@click.option('--template', required=True, help='Report template identifier')
@click.option('--format', 'fmt', type=click.Choice(['json', 'zip', 'pdf']), default='json')
@click.option('--async', 'as_async', is_flag=True, help='Trigger readiness asynchronously (202) before fetching')
@click.option('--idempotency-key', help='Optional idempotency key for POST triggers')
@click.option('--output', '-o', help='Write response to file')
@click.pass_context
def preview(ctx, job_id, template, fmt, as_async, idempotency_key, output):
    """Preview a report for a job (uses /api/cli/reports?action=preview)"""
    config = ctx.obj['config']
    auth_manager = AuthManager(config)
    if not auth_manager.is_authenticated():
        console.print("[red]❌ Not authenticated. Run 'ivybloom auth login' first.[/red]")
        return

    try:
        with IvyBloomAPIClient(config, auth_manager) as client:
            if as_async:
                client.reports_post('preview', job_id=job_id, template=template, extra_params={'format': fmt}, idempotency_key=idempotency_key)
            data = client.reports_get('preview', job_id=job_id, template=template, format=fmt)

        if output:
            with open(output, 'w') as f:
                f.write(data if isinstance(data, str) else str(data))
            console.print(f"[green]✅ Wrote preview to {output}[/green]")
            return

        if isinstance(data, dict):
            emit_json(data)
        else:
            console.print(str(data))
    except Exception as e:
        console.print(f"[red]❌ Error previewing report: {e}[/red]")


@reports.command(help="Generate a report (pdf/zip).\n\nUse --no-follow-redirect to capture redirect URL instead of following it.")
@click.argument('job_id')
@click.option('--template', required=True, help='Report template identifier')
@click.option('--format', 'fmt', type=click.Choice(['pdf', 'zip']), default='pdf')
@click.option('--async', 'as_async', is_flag=True, help='Trigger readiness asynchronously (202) before fetching')
@click.option('--no-follow-redirect', is_flag=True, help='Return redirect target instead of following it')
@click.option('--idempotency-key', help='Optional idempotency key for POST triggers')
@click.pass_context
def generate(ctx, job_id, template, fmt, as_async, no_follow_redirect, idempotency_key):
    """Generate a report (pdf/zip). GET follows/provides redirect to content."""
    config = ctx.obj['config']
    auth_manager = AuthManager(config)
    if not auth_manager.is_authenticated():
        console.print("[red]❌ Not authenticated. Run 'ivybloom auth login' first.[/red]")
        return

    try:
        with IvyBloomAPIClient(config, auth_manager) as client:
            if as_async:
                client.reports_post('generate', job_id=job_id, template=template, format=fmt, idempotency_key=idempotency_key)
            data = client.reports_get('generate', job_id=job_id, template=template, format=fmt, follow_redirects=not no_follow_redirect)

        emit_json(data)
    except Exception as e:
        console.print(f"[red]❌ Error generating report: {e}[/red]")


@reports.command(help="Export artifacts via preset type (e.g., package_zip).\n\nUse --no-follow-redirect to capture redirect URL.")
@click.argument('job_id')
@click.option('--type', 'export_type', required=True, help='Export type preset (e.g., package_zip)')
@click.option('--async', 'as_async', is_flag=True, help='Trigger readiness asynchronously (202)')
@click.option('--no-follow-redirect', is_flag=True, help='Return redirect target instead of following it')
@click.option('--idempotency-key', help='Optional idempotency key for POST triggers')
@click.pass_context
def export(ctx, job_id, export_type, as_async, no_follow_redirect, idempotency_key):
    """Export artifacts via preset type (uses /api/cli/reports?action=export)."""
    config = ctx.obj['config']
    auth_manager = AuthManager(config)
    if not auth_manager.is_authenticated():
        console.print("[red]❌ Not authenticated. Run 'ivybloom auth login' first.[/red]")
        return

    try:
        with IvyBloomAPIClient(config, auth_manager) as client:
            if as_async:
                client.reports_post('export', job_id=job_id, export_type=export_type, idempotency_key=idempotency_key)
            data = client.reports_get('export', job_id=job_id, export_type=export_type, follow_redirects=not no_follow_redirect)

        emit_json(data)
    except Exception as e:
        console.print(f"[red]❌ Error exporting report: {e}[/red]")



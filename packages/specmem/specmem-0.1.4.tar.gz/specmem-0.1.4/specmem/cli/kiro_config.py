"""CLI commands for Kiro configuration indexing."""

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from specmem.kiro.indexer import KiroConfigIndexer


console = Console()


@click.group(name="kiro-config")
def kiro_config_group():
    """Kiro configuration management commands."""
    pass


@kiro_config_group.command(name="show")
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True, path_type=Path),
    default=".",
    help="Workspace path",
)
def show_config(path: Path):
    """Display summary of all Kiro configuration."""
    indexer = KiroConfigIndexer(path)
    indexer.index_all()
    summary = indexer.get_summary()

    # Steering files section
    if summary.steering_files:
        table = Table(title="📝 Steering Files", show_header=True)
        table.add_column("File", style="cyan")
        table.add_column("Inclusion", style="green")
        table.add_column("Pattern", style="yellow")

        for steering in summary.steering_files:
            table.add_row(
                steering.path.name,
                steering.inclusion,
                steering.file_match_pattern or "-",
            )
        console.print(table)
    else:
        console.print("[dim]No steering files found in .kiro/steering/[/dim]")

    console.print()

    # MCP servers section
    if summary.mcp_servers:
        table = Table(title="🔌 MCP Servers", show_header=True)
        table.add_column("Server", style="cyan")
        table.add_column("Command", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Auto-Approve", style="magenta")

        for server in summary.mcp_servers:
            status = "❌ Disabled" if server.disabled else "✅ Enabled"
            auto_approve = ", ".join(server.auto_approve) if server.auto_approve else "-"
            table.add_row(
                server.name,
                f"{server.command} {' '.join(server.args[:2])}",
                status,
                auto_approve[:30] + "..." if len(auto_approve) > 30 else auto_approve,
            )
        console.print(table)
    else:
        console.print("[dim]No MCP configuration found in .kiro/settings/mcp.json[/dim]")

    console.print()

    # Hooks section
    if summary.hooks:
        table = Table(title="🪝 Hooks", show_header=True)
        table.add_column("Hook", style="cyan")
        table.add_column("Trigger", style="green")
        table.add_column("Pattern", style="yellow")
        table.add_column("Status", style="magenta")

        for hook in summary.hooks:
            status = "✅ Active" if hook.enabled else "❌ Disabled"
            table.add_row(
                hook.name,
                hook.trigger,
                hook.file_pattern or "-",
                status,
            )
        console.print(table)
    else:
        console.print("[dim]No hooks found in .kiro/hooks/[/dim]")

    console.print()

    # Summary panel
    summary_text = f"""
Steering Files: {len(summary.steering_files)}
MCP Servers: {summary.enabled_servers} enabled / {len(summary.mcp_servers)} total
Hooks: {summary.active_hooks} active / {len(summary.hooks)} total
Tools: {summary.total_tools} available
"""
    console.print(Panel(summary_text.strip(), title="📊 Summary", border_style="blue"))


@click.command(name="steering")
@click.option(
    "--file",
    "-f",
    "file_path",
    type=str,
    help="Show steering files applicable to this file",
)
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True, path_type=Path),
    default=".",
    help="Workspace path",
)
def steering_command(file_path: str | None, path: Path):
    """Query steering files.

    Without --file, shows all steering files.
    With --file, shows only steering files applicable to that file.
    """
    indexer = KiroConfigIndexer(path)
    indexer.index_steering()

    if file_path:
        # Show steering for specific file
        applicable = indexer.get_steering_for_file(file_path)

        if not applicable:
            console.print(f"[yellow]No steering files apply to: {file_path}[/yellow]")
            return

        console.print(f"[bold]Steering files for: {file_path}[/bold]\n")

        for steering in applicable:
            console.print(
                Panel(
                    steering.body[:500] + ("..." if len(steering.body) > 500 else ""),
                    title=f"📝 {steering.title}",
                    subtitle=f"inclusion: {steering.inclusion}",
                    border_style="green",
                )
            )
            console.print()
    else:
        # Show all steering files
        summary = indexer.get_summary()

        if not summary.steering_files:
            console.print("[dim]No steering files found in .kiro/steering/[/dim]")
            return

        table = Table(title="📝 All Steering Files", show_header=True)
        table.add_column("File", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Inclusion", style="green")
        table.add_column("Pattern", style="yellow")

        for steering in summary.steering_files:
            table.add_row(
                steering.path.name,
                steering.title[:40] + "..." if len(steering.title) > 40 else steering.title,
                steering.inclusion,
                steering.file_match_pattern or "-",
            )

        console.print(table)

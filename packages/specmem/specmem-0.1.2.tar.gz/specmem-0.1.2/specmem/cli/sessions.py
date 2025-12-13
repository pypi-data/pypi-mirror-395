"""CLI commands for Kiro session search.

Provides commands for configuring, searching, and viewing Kiro sessions.
"""

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from specmem.sessions.config import SessionConfigManager
from specmem.sessions.discovery import SessionDiscovery
from specmem.sessions.exceptions import (
    InvalidSessionPathError,
    SessionNotConfiguredError,
    SessionNotFoundError,
)
from specmem.sessions.models import SearchFilters


app = typer.Typer(
    name="sessions",
    help="Search and manage Kiro coding sessions",
)

console = Console()


def get_storage_and_engine():
    """Get storage and search engine instances."""
    from specmem.sessions.search import SessionSearchEngine
    from specmem.sessions.storage import SessionStorage

    config_manager = SessionConfigManager()
    config = config_manager.get_config_or_raise()

    db_path = Path(".specmem") / "sessions.db"
    storage = SessionStorage(db_path)
    engine = SessionSearchEngine(storage)

    return storage, engine, config


@app.command("config")
def config_sessions(
    path: str | None = typer.Option(None, "--path", "-p", help="Path to Kiro sessions directory"),
    auto: bool = typer.Option(False, "--auto", help="Auto-discover without prompting"),
    workspace_only: bool = typer.Option(
        False, "--workspace-only", "-w", help="Only search sessions for current workspace"
    ),
) -> None:
    """Configure Kiro session search.

    Without arguments, prompts for permission to auto-discover the sessions directory.
    Use --path to provide an explicit path, or --auto to auto-discover without prompting.
    """
    config_manager = SessionConfigManager()
    discovery = SessionDiscovery()

    if path:
        # Direct path configuration
        sessions_path = Path(path).expanduser()
        try:
            config_manager.configure_with_path(sessions_path, workspace_only)
            console.print(f"[green]✓[/green] Session search configured: {sessions_path}")
        except InvalidSessionPathError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)
        return

    if auto:
        # Auto-discover without prompting
        result = discovery.discover()
        if not result.success:
            console.print(f"[red]Error:[/red] {result.error}")
            console.print("\n" + discovery.get_help_text())
            raise typer.Exit(1)

        sessions_path = result.found_paths[0]
        config_manager.configure_with_path(sessions_path, workspace_only)
        console.print(f"[green]✓[/green] Session search configured: {sessions_path}")
        return

    # Interactive mode - ask for permission
    console.print(
        Panel(
            "[bold]Kiro Session Search Configuration[/bold]\n\n"
            "This feature allows you to search through your past Kiro coding sessions.\n"
            "To do this, SpecMem needs to access your Kiro session data.",
            title="Session Search",
        )
    )

    permission = typer.confirm(
        "\nDo you give permission to auto-discover your Kiro sessions directory?",
        default=True,
    )

    if not permission:
        console.print("\n" + discovery.get_help_text())
        console.print("\nYou can configure manually with:")
        console.print("  [bold]specmem sessions config --path /path/to/workspace-sessions[/bold]")
        return

    # Auto-discover
    console.print("\n[dim]Searching for Kiro sessions...[/dim]")
    result = discovery.discover()

    if not result.success:
        console.print("\n[yellow]Could not find Kiro sessions directory.[/yellow]")
        console.print("\n" + discovery.get_help_text())
        raise typer.Exit(1)

    # Show found paths and ask for confirmation
    if len(result.found_paths) == 1:
        sessions_path = result.found_paths[0]
        console.print(f"\n[green]Found:[/green] {sessions_path}")

        confirm = typer.confirm("Is this correct?", default=True)
        if not confirm:
            console.print("\nPlease provide the path manually:")
            console.print(
                "  [bold]specmem sessions config --path /path/to/workspace-sessions[/bold]"
            )
            return
    else:
        # Multiple paths found - let user choose
        console.print("\n[green]Found multiple session directories:[/green]")
        for i, p in enumerate(result.found_paths, 1):
            console.print(f"  {i}. {p}")

        choice = typer.prompt("Enter number to select", type=int, default=1)
        if choice < 1 or choice > len(result.found_paths):
            console.print("[red]Invalid choice[/red]")
            raise typer.Exit(1)

        sessions_path = result.found_paths[choice - 1]

    # Configure
    config_manager.configure_with_path(sessions_path, workspace_only)
    console.print("\n[green]✓[/green] Session search configured!")
    console.print(f"  Path: {sessions_path}")
    console.print(f"  Workspace only: {workspace_only}")


@app.command("search")
def search_sessions(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", "-n", help="Maximum results"),
    days: int | None = typer.Option(None, "--days", "-d", help="Only last N days"),
    robot: bool = typer.Option(False, "--robot", "-r", help="Output JSON for AI agents"),
) -> None:
    """Search through Kiro sessions."""
    try:
        storage, engine, config = get_storage_and_engine()
    except SessionNotConfiguredError as e:
        if robot:
            print(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    # Build filters
    filters = SearchFilters(limit=limit)
    if days:
        import time

        filters.since_ms = int((time.time() - days * 86400) * 1000)

    # Search
    results = engine.search(query, filters)

    if robot:
        output = {
            "query": query,
            "count": len(results),
            "results": [r.to_dict() for r in results],
        }
        print(json.dumps(output, indent=2))
        return

    if not results:
        console.print("[yellow]No sessions found matching your query.[/yellow]")
        return

    # Display results
    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Session ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Score", style="green")
    table.add_column("Date", style="dim")

    for result in results:
        table.add_row(
            result.session.session_id[:12] + "...",
            result.session.title[:40] + ("..." if len(result.session.title) > 40 else ""),
            f"{result.score:.2f}",
            result.session.date_created.strftime("%Y-%m-%d"),
        )

    console.print(table)


@app.command("list")
def list_sessions(
    limit: int = typer.Option(10, "--limit", "-n", help="Maximum results"),
    workspace_only: bool = typer.Option(
        False, "--workspace-only", "-w", help="Only current workspace"
    ),
    robot: bool = typer.Option(False, "--robot", "-r", help="Output JSON for AI agents"),
) -> None:
    """List recent Kiro sessions."""
    try:
        storage, engine, config = get_storage_and_engine()
    except SessionNotConfiguredError as e:
        if robot:
            print(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    workspace = Path.cwd() if workspace_only else None
    sessions = engine.list_recent(limit=limit, workspace=workspace)

    if robot:
        output = {
            "count": len(sessions),
            "sessions": [s.to_dict() for s in sessions],
        }
        print(json.dumps(output, indent=2))
        return

    if not sessions:
        console.print("[yellow]No sessions found.[/yellow]")
        return

    table = Table(title="Recent Sessions")
    table.add_column("Session ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Messages", style="green")
    table.add_column("Date", style="dim")

    for session in sessions:
        table.add_row(
            session.session_id[:12] + "...",
            session.title[:40] + ("..." if len(session.title) > 40 else ""),
            str(session.message_count),
            session.date_created.strftime("%Y-%m-%d %H:%M"),
        )

    console.print(table)


@app.command("view")
def view_session(
    session_id: str = typer.Argument(..., help="Session ID to view"),
    robot: bool = typer.Option(False, "--robot", "-r", help="Output JSON for AI agents"),
) -> None:
    """View full conversation of a session."""
    try:
        storage, engine, config = get_storage_and_engine()
    except SessionNotConfiguredError as e:
        if robot:
            print(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    try:
        session = engine.get_session(session_id)
    except SessionNotFoundError as e:
        if robot:
            print(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    if robot:
        print(json.dumps(session.to_dict(), indent=2))
        return

    # Display session
    console.print(
        Panel(
            f"[bold]{session.title}[/bold]\n\n"
            f"Session ID: {session.session_id}\n"
            f"Workspace: {session.workspace_directory}\n"
            f"Created: {session.date_created.strftime('%Y-%m-%d %H:%M')}\n"
            f"Messages: {session.message_count}",
            title="Session Details",
        )
    )

    console.print("\n[bold]Conversation:[/bold]\n")

    for i, msg in enumerate(session.messages):
        role_color = "blue" if msg.role.value == "user" else "green"
        role_label = "You" if msg.role.value == "user" else "Kiro"

        console.print(f"[{role_color}][bold]{role_label}:[/bold][/{role_color}]")
        # Truncate long messages
        content = msg.content
        if len(content) > 500:
            content = content[:500] + "...\n[dim](truncated)[/dim]"
        console.print(content)
        console.print()


@app.command("index")
def index_sessions(
    workspace_only: bool = typer.Option(
        False, "--workspace-only", "-w", help="Only current workspace"
    ),
) -> None:
    """Index Kiro sessions for search."""
    from specmem.sessions.indexer import SessionIndexer
    from specmem.sessions.scanner import SessionScanner
    from specmem.sessions.storage import SessionStorage

    config_manager = SessionConfigManager()

    try:
        config = config_manager.get_config_or_raise()
    except SessionNotConfiguredError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    console.print("[dim]Scanning for sessions...[/dim]")

    scanner = SessionScanner(config)
    workspace = Path.cwd() if workspace_only else None
    sessions = scanner.scan(workspace_filter=workspace)

    console.print(f"Found {len(sessions)} sessions")

    db_path = Path(".specmem") / "sessions.db"
    storage = SessionStorage(db_path)
    indexer = SessionIndexer(storage)

    console.print("[dim]Indexing sessions...[/dim]")
    count = indexer.index_sessions(sessions)

    console.print(f"[green]✓[/green] Indexed {count} sessions")

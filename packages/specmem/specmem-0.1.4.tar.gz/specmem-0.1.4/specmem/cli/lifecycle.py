"""CLI commands for spec lifecycle management.

Provides commands for:
- prune: Archive or delete orphaned/stale specs
- generate: Create specs from code
- compress: Condense verbose specs
- health: Display spec health scores
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table


app = typer.Typer(
    name="lifecycle",
    help="Spec lifecycle management commands",
)

console = Console()


@app.command("prune")
def prune(
    spec_names: list[str] = typer.Argument(None, help="Specific spec names to prune"),
    mode: str = typer.Option("archive", "--mode", "-m", help="Mode: archive or delete"),
    dry_run: bool = typer.Option(True, "--dry-run/--no-dry-run", help="Preview without changes"),
    force: bool = typer.Option(False, "--force", "-f", help="Force delete without confirmation"),
    orphaned: bool = typer.Option(False, "--orphaned", help="Prune all orphaned specs"),
    stale: bool = typer.Option(False, "--stale", help="Prune all stale specs"),
    stale_days: int = typer.Option(90, "--stale-days", help="Days threshold for stale"),
    path: str = typer.Option(".", "--path", "-p", help="Repository path"),
) -> None:
    """Prune orphaned or stale specifications.

    Examples:
        specmem prune login                    # Prune specific spec
        specmem prune login auth --mode delete # Delete multiple specs
        specmem prune --orphaned               # Prune all orphaned specs
        specmem prune --stale --stale-days 60  # Prune specs older than 60 days
        specmem prune login --no-dry-run       # Actually prune (not just preview)
    """
    from specmem.lifecycle import HealthAnalyzer, PrunerEngine

    repo_path = Path(path)
    spec_base = repo_path / ".kiro" / "specs"
    archive_dir = repo_path / ".specmem" / "archive"

    if not spec_base.exists():
        console.print("[yellow]No specs found at .kiro/specs/[/yellow]")
        raise typer.Exit(1)

    # Validate mode
    if mode not in ("archive", "delete"):
        console.print(f"[red]Invalid mode:[/red] {mode}. Use 'archive' or 'delete'.")
        raise typer.Exit(1)

    # Create analyzer and pruner
    analyzer = HealthAnalyzer(
        spec_base_path=spec_base,
        stale_threshold_days=stale_days,
    )
    pruner = PrunerEngine(
        health_analyzer=analyzer,
        archive_dir=archive_dir,
    )

    results = []

    if spec_names:
        # Prune specific specs
        console.print(f"Pruning specs: {', '.join(spec_names)}")
        results = pruner.prune_by_name(
            spec_names=spec_names,
            mode=mode,  # type: ignore
            dry_run=dry_run,
            force=force,
        )
    elif orphaned:
        # Prune orphaned specs
        console.print("Pruning orphaned specs...")
        results = pruner.prune_orphaned(
            mode=mode,  # type: ignore
            dry_run=dry_run,
            force=force,
        )
    elif stale:
        # Prune stale specs
        console.print(f"Pruning specs not modified in {stale_days}+ days...")
        results = pruner.prune_stale(
            threshold_days=stale_days,
            mode=mode,  # type: ignore
            dry_run=dry_run,
        )
    else:
        # Show analysis
        console.print("Analyzing specs...")
        scores = pruner.analyze()

        if not scores:
            console.print("[yellow]No specs found.[/yellow]")
            return

        table = Table(title="Spec Health Analysis")
        table.add_column("Spec", style="cyan")
        table.add_column("Score", justify="right")
        table.add_column("Refs", justify="right")
        table.add_column("Status")

        for score in sorted(scores, key=lambda s: s.score):
            status_parts = []
            if score.is_orphaned:
                status_parts.append("[red]orphaned[/red]")
            if score.is_stale:
                status_parts.append("[yellow]stale[/yellow]")
            if not status_parts:
                status_parts.append("[green]healthy[/green]")

            table.add_row(
                score.spec_id,
                f"{score.score:.2f}",
                str(score.code_references),
                " ".join(status_parts),
            )

        console.print(table)
        console.print("\nUse --orphaned or --stale to prune, or specify spec names.")
        return

    # Display results
    if not results:
        console.print("[yellow]No specs to prune.[/yellow]")
        return

    table = Table(title="Prune Results")
    table.add_column("Spec", style="cyan")
    table.add_column("Action")
    table.add_column("Reason")

    for result in results:
        action_style = {
            "archived": "green",
            "deleted": "red",
            "skipped": "yellow",
        }.get(result.action, "white")

        table.add_row(
            result.spec_id,
            f"[{action_style}]{result.action}[/{action_style}]",
            result.reason[:50],
        )

    console.print(table)

    if dry_run:
        console.print("\n[yellow]This was a dry run. Use --no-dry-run to apply changes.[/yellow]")


@app.command("generate")
def generate(
    files: list[str] = typer.Argument(..., help="Code files or directories to generate specs from"),
    format: str = typer.Option("kiro", "--format", "-f", help="Output format (kiro, speckit)"),
    output: str = typer.Option(None, "--output", "-o", help="Output directory"),
    group_by: str = typer.Option(
        "directory", "--group-by", "-g", help="Grouping: file, directory, module"
    ),
    write: bool = typer.Option(False, "--write", "-w", help="Write specs to disk"),
    path: str = typer.Option(".", "--path", "-p", help="Repository path"),
) -> None:
    """Generate specifications from code files.

    Examples:
        specmem generate src/auth.py           # Generate from single file
        specmem generate src/                  # Generate from directory
        specmem generate src/ --group-by file  # One spec per file
        specmem generate src/ --write          # Write specs to disk
    """
    from specmem.lifecycle import GeneratorEngine

    repo_path = Path(path)
    output_dir = Path(output) if output else repo_path / ".kiro" / "specs"

    generator = GeneratorEngine(
        default_format=format,
        output_dir=output_dir,
    )

    all_specs = []

    for file_arg in files:
        file_path = Path(file_arg)
        if not file_path.is_absolute():
            file_path = repo_path / file_path

        if not file_path.exists():
            console.print(f"[red]Not found:[/red] {file_arg}")
            continue

        if file_path.is_file():
            spec = generator.generate_from_file(file_path)
            all_specs.append(spec)
        else:
            specs = generator.generate_from_directory(
                file_path,
                group_by=group_by,  # type: ignore
                output_format=format,
            )
            all_specs.extend(specs)

    if not all_specs:
        console.print("[yellow]No specs generated.[/yellow]")
        return

    console.print(f"\n[bold]Generated {len(all_specs)} spec(s)[/bold]\n")

    table = Table(title="Generated Specs")
    table.add_column("Name", style="cyan")
    table.add_column("Format")
    table.add_column("Sources")
    table.add_column("Size", justify="right")

    for spec in all_specs:
        table.add_row(
            spec.spec_name,
            spec.adapter_format,
            str(len(spec.source_files)),
            f"{len(spec.content)} chars",
        )

    console.print(table)

    if write:
        console.print("\nWriting specs to disk...")
        for spec in all_specs:
            written_path = generator.write_spec(spec)
            console.print(f"  [green]✓[/green] {written_path}")
    else:
        console.print("\n[yellow]Use --write to save specs to disk.[/yellow]")

        # Show preview of first spec
        if all_specs:
            console.print("\n[bold]Preview of first spec:[/bold]")
            preview = all_specs[0].content[:500]
            if len(all_specs[0].content) > 500:
                preview += "..."
            console.print(preview)


@app.command("compress")
def compress(
    spec_names: list[str] = typer.Argument(None, help="Specific specs to compress"),
    threshold: int = typer.Option(5000, "--threshold", "-t", help="Char threshold for verbose"),
    all_verbose: bool = typer.Option(False, "--all", "-a", help="Compress all verbose specs"),
    save: bool = typer.Option(False, "--save", "-s", help="Save compressed versions"),
    path: str = typer.Option(".", "--path", "-p", help="Repository path"),
) -> None:
    """Compress verbose specifications.

    Examples:
        specmem compress auth-feature          # Compress specific spec
        specmem compress --all                 # Compress all verbose specs
        specmem compress --all --threshold 3000 # Lower threshold
        specmem compress auth-feature --save   # Save compressed version
    """
    from specmem.lifecycle import CompressorEngine

    repo_path = Path(path)
    spec_base = repo_path / ".kiro" / "specs"
    compressed_dir = repo_path / ".specmem" / "compressed"

    if not spec_base.exists():
        console.print("[yellow]No specs found at .kiro/specs/[/yellow]")
        raise typer.Exit(1)

    compressor = CompressorEngine(
        verbose_threshold_chars=threshold,
        compression_storage_dir=compressed_dir,
    )

    # Discover specs
    specs: list[tuple[str, Path]] = []
    for item in spec_base.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            specs.append((item.name, item))

    if not specs:
        console.print("[yellow]No specs found.[/yellow]")
        return

    results = []

    if spec_names:
        # Compress specific specs
        for name in spec_names:
            spec_path = spec_base / name
            if not spec_path.exists():
                console.print(f"[red]Spec not found:[/red] {name}")
                continue
            compressed = compressor.compress_spec(name, spec_path)
            results.append(compressed)
    elif all_verbose:
        # Compress all verbose specs
        results = compressor.compress_all(specs)
    else:
        # Show verbose specs
        verbose = compressor.get_verbose_specs(specs, threshold)

        if not verbose:
            console.print(f"[green]No specs exceed {threshold} characters.[/green]")
            return

        console.print(f"\n[bold]Verbose Specs (>{threshold} chars):[/bold]\n")
        for name in verbose:
            console.print(f"  • {name}")

        console.print("\nUse --all to compress all verbose specs, or specify names.")
        return

    if not results:
        console.print("[yellow]No specs compressed.[/yellow]")
        return

    table = Table(title="Compression Results")
    table.add_column("Spec", style="cyan")
    table.add_column("Original", justify="right")
    table.add_column("Compressed", justify="right")
    table.add_column("Ratio", justify="right")
    table.add_column("Criteria", justify="right")

    for result in results:
        table.add_row(
            result.spec_id,
            f"{result.original_size:,}",
            f"{result.compressed_size:,}",
            f"{result.compression_ratio:.1%}",
            str(len(result.preserved_criteria)),
        )

    console.print(table)

    if save:
        console.print("\nSaving compressed versions...")
        for result in results:
            saved_path = compressor.save_compressed(result)
            console.print(f"  [green]✓[/green] {saved_path}")


@app.command("health")
def health(
    spec_name: str = typer.Argument(None, help="Specific spec to analyze"),
    sort_by: str = typer.Option("score", "--sort", "-s", help="Sort by: score, name, refs"),
    path: str = typer.Option(".", "--path", "-p", help="Repository path"),
) -> None:
    """Display spec health scores and recommendations.

    Examples:
        specmem health                  # Show all specs
        specmem health auth-feature     # Show specific spec
        specmem health --sort refs      # Sort by code references
    """
    from specmem.lifecycle import HealthAnalyzer

    repo_path = Path(path)
    spec_base = repo_path / ".kiro" / "specs"

    if not spec_base.exists():
        console.print("[yellow]No specs found at .kiro/specs/[/yellow]")
        raise typer.Exit(1)

    analyzer = HealthAnalyzer(spec_base_path=spec_base)

    if spec_name:
        # Analyze specific spec
        spec_path = spec_base / spec_name
        if not spec_path.exists():
            console.print(f"[red]Spec not found:[/red] {spec_name}")
            raise typer.Exit(1)

        score = analyzer.analyze_spec(spec_name, spec_path)

        console.print(f"\n[bold]Health Report:[/bold] {spec_name}\n")
        console.print(f"Score: {score.score:.2f}")
        console.print(f"Code References: {score.code_references}")
        console.print(f"Last Modified: {score.last_modified}")
        console.print(f"Query Count: {score.query_count}")

        status = []
        if score.is_orphaned:
            status.append("[red]Orphaned[/red]")
        if score.is_stale:
            status.append("[yellow]Stale[/yellow]")
        if not status:
            status.append("[green]Healthy[/green]")
        console.print(f"Status: {' '.join(status)}")

        if score.recommendations:
            console.print("\n[bold]Recommendations:[/bold]")
            for rec in score.recommendations:
                console.print(f"  • {rec}")
        return

    # Analyze all specs
    scores = analyzer.analyze_all()

    if not scores:
        console.print("[yellow]No specs found.[/yellow]")
        return

    # Sort
    if sort_by == "score":
        scores.sort(key=lambda s: s.score)
    elif sort_by == "name":
        scores.sort(key=lambda s: s.spec_id)
    elif sort_by == "refs":
        scores.sort(key=lambda s: s.code_references, reverse=True)

    # Summary
    summary = analyzer.get_summary()
    console.print("\n[bold]Spec Health Summary[/bold]\n")
    console.print(f"Total Specs: {summary['total_specs']}")
    console.print(f"Orphaned: {summary['orphaned_count']}")
    console.print(f"Stale: {summary['stale_count']}")
    console.print(f"Average Score: {summary['average_score']:.2f}")

    # Table
    table = Table(title="\nSpec Health Scores")
    table.add_column("Spec", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Refs", justify="right")
    table.add_column("Status")
    table.add_column("Recommendation")

    for score in scores:
        status_parts = []
        if score.is_orphaned:
            status_parts.append("[red]orphaned[/red]")
        if score.is_stale:
            status_parts.append("[yellow]stale[/yellow]")
        if not status_parts:
            status_parts.append("[green]healthy[/green]")

        rec = score.recommendations[0][:30] + "..." if score.recommendations else "-"

        table.add_row(
            score.spec_id,
            f"{score.score:.2f}",
            str(score.code_references),
            " ".join(status_parts),
            rec,
        )

    console.print(table)

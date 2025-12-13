"""Coverage CLI commands for SpecMem.

Provides the `specmem cov` command group for spec coverage analysis.
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from specmem.coverage import CoverageEngine


app = typer.Typer(
    name="cov",
    help="Spec coverage analysis commands",
)

console = Console()


@app.callback(invoke_without_command=True)
def cov_main(
    ctx: typer.Context,
    path: str = typer.Option(".", "--path", "-p", help="Workspace path"),
) -> None:
    """Show spec coverage summary.

    Displays overall coverage percentage and per-feature breakdown.
    """
    if ctx.invoked_subcommand is not None:
        return

    engine = CoverageEngine(Path(path))
    result = engine.analyze_coverage()

    # Overall summary
    status = "✅" if result.coverage_percentage >= 80 else "⚠️"
    console.print()
    console.print(f"📊 [bold]Spec Coverage Report[/bold] {status}")
    console.print("=" * 40)
    console.print(
        f"Overall: [bold]{result.covered_criteria}/{result.total_criteria}[/bold] "
        f"criteria covered ([bold]{result.coverage_percentage:.1f}%[/bold])"
    )
    console.print()

    # Feature table
    table = Table(title="Coverage by Feature")
    table.add_column("Feature", style="cyan")
    table.add_column("Tested", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Coverage", justify="right")
    table.add_column("Gap", justify="right")

    for feature in result.features:
        status = "✅" if feature.coverage_percentage >= 80 else "⚠️"
        table.add_row(
            feature.feature_name,
            str(feature.tested_count),
            str(feature.total_count),
            f"{feature.coverage_percentage:.1f}%",
            f"{feature.gap_percentage:.1f}% {status}",
        )

    console.print(table)
    console.print()
    console.print("Run [bold]specmem cov report <feature>[/bold] for details.")
    console.print("Run [bold]specmem cov suggest <feature>[/bold] for test suggestions.")


@app.command()
def report(
    feature: str = typer.Argument(None, help="Feature name to report on"),
    path: str = typer.Option(".", "--path", "-p", help="Workspace path"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
) -> None:
    """Show detailed coverage report for a feature.

    If no feature is specified, shows all features.
    """
    engine = CoverageEngine(Path(path))

    if feature:
        coverage = engine.analyze_feature(feature)
        features = [coverage]
    else:
        result = engine.analyze_coverage()
        features = result.features

    for feat in features:
        console.print()
        status = "✅" if feat.coverage_percentage >= 80 else "⚠️"
        console.print(f"[bold]{feat.feature_name}[/bold] {status}")
        console.print(
            f"Coverage: {feat.tested_count}/{feat.total_count} ({feat.coverage_percentage:.1f}%)"
        )
        console.print()

        for match in feat.criteria:
            if match.is_covered:
                icon = "✅"
                test_info = ""
                if match.test:
                    test_info = f" → {match.test.file_path}:{match.test.line_number}"
            else:
                icon = "⚠️"
                test_info = " → NO TEST FOUND"

            console.print(
                f"  {icon} AC {match.criterion.number}: {match.criterion.text[:60]}...{test_info}"
            )

        console.print()


@app.command()
def suggest(
    feature: str = typer.Argument(..., help="Feature name to get suggestions for"),
    path: str = typer.Option(".", "--path", "-p", help="Workspace path"),
) -> None:
    """Get test suggestions for uncovered criteria.

    Shows recommended test file, function name, and verification points.
    """
    engine = CoverageEngine(Path(path))
    suggestions = engine.get_suggestions(feature)

    if not suggestions:
        console.print(f"[green]✅ All criteria in '{feature}' are covered![/green]")
        return

    console.print()
    console.print(f"📝 [bold]Test Suggestions for: {feature}[/bold]")
    console.print("=" * 50)
    console.print()

    for i, suggestion in enumerate(suggestions, 1):
        console.print(f"[bold]{i}. AC {suggestion.criterion.number}:[/bold]")
        console.print(f'   "{suggestion.criterion.text[:80]}..."')
        console.print()
        console.print("   [cyan]Suggested test approach:[/cyan]")
        console.print(f"   - Test file: [green]{suggestion.suggested_file}[/green]")
        console.print(f"   - Test name: [green]{suggestion.suggested_name}[/green]")
        console.print("   - What to verify:")
        for point in suggestion.verification_points:
            console.print(f"     • {point}")
        console.print()

    console.print("💡 Copy these suggestions to your agent to generate the actual tests.")


@app.command()
def badge(
    path: str = typer.Option(".", "--path", "-p", help="Workspace path"),
    output: str = typer.Option(None, "--output", "-o", help="Output file path"),
) -> None:
    """Generate coverage badge markdown.

    Outputs a shields.io badge URL that can be added to README.
    """
    engine = CoverageEngine(Path(path))
    badge_md = engine.generate_badge()

    if output:
        Path(output).write_text(badge_md + "\n")
        console.print(f"[green]✓[/green] Badge written to {output}")
    else:
        console.print(badge_md)


@app.command()
def export(
    format: str = typer.Option("json", "--format", "-f", help="Export format (json, markdown)"),
    path: str = typer.Option(".", "--path", "-p", help="Workspace path"),
    output: str = typer.Option(None, "--output", "-o", help="Output file path"),
) -> None:
    """Export coverage data in specified format.

    Supports JSON and Markdown formats.
    """
    engine = CoverageEngine(Path(path))
    data = engine.export(format)

    if output:
        Path(output).write_text(data)
        console.print(f"[green]✓[/green] Coverage data exported to {output}")
    else:
        console.print(data)

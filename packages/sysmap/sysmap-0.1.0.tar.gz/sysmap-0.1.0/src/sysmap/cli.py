"""Command-line interface for SysMap."""

import click
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import box

from .core.scanner import SystemScanner
from .core.config import Config
from .exporters import (
    MarkdownExporter,
    JSONExporter,
    CSVExporter,
    HTMLExporter,
    YAMLExporter,
)
from .utils.diff import DiffTool
from .utils.watch import WatchMode

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="sysmap")
@click.pass_context
def main(ctx: click.Context) -> None:
    """
    SysMap - A comprehensive system inventory tool.

    Track installed software, versions, and configurations across multiple platforms.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config()


@main.command()
@click.option(
    "--format",
    "-f",
    type=click.Choice(["markdown", "json", "yaml", "csv", "html"], case_sensitive=False),
    default="markdown",
    help="Output format",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path",
)
@click.option(
    "--check-updates",
    is_flag=True,
    help="Check for available package updates",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration file",
)
@click.pass_context
def scan(
    ctx: click.Context,
    format: str,
    output: Optional[str],
    check_updates: bool,
    config: Optional[str],
) -> None:
    """Scan system and generate inventory report."""
    # Load config
    cfg = Config(config) if config else ctx.obj["config"]

    console.print(Panel.fit(
        "[bold cyan]SysMap System Scanner[/bold cyan]\n"
        "Scanning installed packages...",
        border_style="cyan"
    ))

    # Scan with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning package managers...", total=None)
        scanner = SystemScanner(cfg.data)
        data = scanner.scan_all(check_updates=check_updates)
        progress.update(task, completed=True)

    # Display summary
    _display_summary(data)

    # Export data
    exporters = {
        "markdown": MarkdownExporter,
        "json": JSONExporter,
        "yaml": YAMLExporter,
        "csv": CSVExporter,
        "html": HTMLExporter,
    }

    exporter = exporters[format.lower()](data)

    if output:
        exporter.save(output)
        console.print(f"\n[green]✓[/green] Report saved to: [bold]{output}[/bold]")
    else:
        # Default output paths
        default_paths = {
            "markdown": "SYSTEM_SUMMARY.md",
            "json": "system_inventory.json",
            "yaml": "system_inventory.yaml",
            "csv": "system_inventory.csv",
            "html": "system_inventory.html",
        }
        output_path = default_paths[format.lower()]
        exporter.save(output_path)
        console.print(f"\n[green]✓[/green] Report saved to: [bold]{output_path}[/bold]")


@main.command()
@click.argument("baseline", type=click.Path(exists=True))
@click.argument("current", type=click.Path(exists=True), required=False)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["text", "json", "html"], case_sensitive=False),
    default="text",
    help="Diff output format",
)
@click.pass_context
def diff(
    ctx: click.Context,
    baseline: str,
    current: Optional[str],
    format: str,
) -> None:
    """Compare two system snapshots.

    BASELINE: Path to baseline snapshot file

    CURRENT: Path to current snapshot file (optional, will scan if not provided)
    """
    diff_tool = DiffTool()

    if current:
        result = diff_tool.compare_files(baseline, current)
    else:
        # Scan current system
        console.print("[cyan]Scanning current system...[/cyan]")
        scanner = SystemScanner(ctx.obj["config"].data)
        current_data = scanner.scan_all()
        result = diff_tool.compare_with_data(baseline, current_data)

    if format == "text":
        diff_tool.display_diff_console(result)
    elif format == "json":
        import json
        console.print(json.dumps(result, indent=2))
    elif format == "html":
        html_output = diff_tool.export_diff_html(result)
        output_path = "diff_report.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        console.print(f"[green]✓[/green] Diff report saved to: [bold]{output_path}[/bold]")


@main.command()
@click.option(
    "--interval",
    "-i",
    type=int,
    default=60,
    help="Check interval in seconds",
)
@click.option(
    "--alert",
    is_flag=True,
    help="Send alerts on changes",
)
@click.pass_context
def watch(
    ctx: click.Context,
    interval: int,
    alert: bool,
) -> None:
    """Watch for system changes in real-time."""
    watch_mode = WatchMode(ctx.obj["config"], interval=interval, alert=alert)
    try:
        watch_mode.start()
    except KeyboardInterrupt:
        console.print("\n[yellow]Watch mode stopped.[/yellow]")


@main.command()
@click.pass_context
def summary(ctx: click.Context) -> None:
    """Display a quick summary of installed packages."""
    scanner = SystemScanner(ctx.obj["config"].data)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning...", total=None)
        data = scanner.scan_all()
        progress.update(task, completed=True)

    _display_summary(data)


@main.command()
@click.argument("output", type=click.Path(), default=".sysmap.yaml")
def init(output: str) -> None:
    """Create a default configuration file."""
    Config.create_default_config(output)
    console.print(f"[green]✓[/green] Configuration file created: [bold]{output}[/bold]")
    console.print("\nEdit this file to customize SysMap behavior.")


@main.command()
@click.option(
    "--format",
    "-f",
    type=click.Choice(["table", "json"], case_sensitive=False),
    default="table",
    help="Output format",
)
@click.pass_context
def updates(ctx: click.Context, format: str) -> None:
    """Check for available package updates."""
    scanner = SystemScanner(ctx.obj["config"].data)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Checking for updates...", total=None)
        data = scanner.scan_all(check_updates=True)
        progress.update(task, completed=True)

    if format == "table":
        _display_updates_table(data)
    elif format == "json":
        import json
        updates_data = {
            pm: pm_data.get("updates", [])
            for pm, pm_data in data.get("package_managers", {}).items()
            if pm_data.get("updates")
        }
        console.print(json.dumps(updates_data, indent=2))


def _display_summary(data: dict) -> None:
    """Display summary table in console."""
    table = Table(title="Package Summary", box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Package Manager", style="yellow")
    table.add_column("Packages", justify="right", style="green")

    if any("updates" in pm for pm in data.get("package_managers", {}).values()):
        table.add_column("Updates", justify="right", style="red")

    for pm_name, pm_data in data.get("package_managers", {}).items():
        count = pm_data.get("count", 0)
        row = [pm_name.title(), str(count)]

        if "updates" in pm_data:
            updates_count = len(pm_data.get("updates", []))
            row.append(str(updates_count) if updates_count > 0 else "-")

        table.add_row(*row)

    # Add total row
    total_packages = sum(pm.get("count", 0) for pm in data.get("package_managers", {}).values())
    total_row = ["[bold]Total[/bold]", f"[bold]{total_packages}[/bold]"]

    if any("updates" in pm for pm in data.get("package_managers", {}).values()):
        total_updates = sum(len(pm.get("updates", [])) for pm in data.get("package_managers", {}).values())
        total_row.append(f"[bold]{total_updates}[/bold]")

    table.add_row(*total_row)

    console.print()
    console.print(table)


def _display_updates_table(data: dict) -> None:
    """Display available updates in a table."""
    has_updates = False

    for pm_name, pm_data in data.get("package_managers", {}).items():
        updates = pm_data.get("updates", [])
        if not updates:
            continue

        has_updates = True
        table = Table(
            title=f"{pm_name.title()} Updates ({len(updates)})",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        table.add_column("Package", style="yellow")
        table.add_column("Current", style="red")
        table.add_column("Available", style="green")

        for update in updates:
            table.add_row(
                update.get("name", ""),
                update.get("current_version", ""),
                update.get("available_version", ""),
            )

        console.print()
        console.print(table)

    if not has_updates:
        console.print("\n[green]✓[/green] All packages are up to date!")


if __name__ == "__main__":
    main()

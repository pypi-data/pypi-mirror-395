"""Diff utility for comparing system snapshots."""

import json
from typing import Any, Dict, List, Set
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


class DiffTool:
    """Tool for comparing system snapshots."""

    def compare_files(self, baseline_path: str, current_path: str) -> Dict[str, Any]:
        """Compare two snapshot files."""
        with open(baseline_path, "r", encoding="utf-8") as f:
            baseline = json.load(f)

        with open(current_path, "r", encoding="utf-8") as f:
            current = json.load(f)

        return self.compare(baseline, current)

    def compare_with_data(self, baseline_path: str, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare baseline file with current data."""
        with open(baseline_path, "r", encoding="utf-8") as f:
            baseline = json.load(f)

        return self.compare(baseline, current_data)

    def compare(self, baseline: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two system snapshots."""
        result: Dict[str, Any] = {
            "baseline_timestamp": baseline.get("timestamp", "Unknown"),
            "current_timestamp": current.get("timestamp", "Unknown"),
            "changes": {},
        }

        baseline_pms = baseline.get("package_managers", {})
        current_pms = current.get("package_managers", {})

        # Compare each package manager
        all_pms = set(baseline_pms.keys()) | set(current_pms.keys())

        for pm_name in all_pms:
            baseline_packages = self._get_package_dict(baseline_pms.get(pm_name, {}))
            current_packages = self._get_package_dict(current_pms.get(pm_name, {}))

            added = self._find_added(baseline_packages, current_packages)
            removed = self._find_removed(baseline_packages, current_packages)
            updated = self._find_updated(baseline_packages, current_packages)

            if added or removed or updated:
                result["changes"][pm_name] = {
                    "added": added,
                    "removed": removed,
                    "updated": updated,
                }

        return result

    def _get_package_dict(self, pm_data: Dict[str, Any]) -> Dict[str, str]:
        """Convert package list to dict with name as key and version as value."""
        packages = pm_data.get("packages", [])
        return {
            pkg.get("name", pkg.get("id", "")): pkg.get("version", "")
            for pkg in packages
        }

    def _find_added(self, baseline: Dict[str, str], current: Dict[str, str]) -> List[Dict[str, str]]:
        """Find packages added in current."""
        added_names = set(current.keys()) - set(baseline.keys())
        return [{"name": name, "version": current[name]} for name in sorted(added_names)]

    def _find_removed(self, baseline: Dict[str, str], current: Dict[str, str]) -> List[Dict[str, str]]:
        """Find packages removed from baseline."""
        removed_names = set(baseline.keys()) - set(current.keys())
        return [{"name": name, "version": baseline[name]} for name in sorted(removed_names)]

    def _find_updated(self, baseline: Dict[str, str], current: Dict[str, str]) -> List[Dict[str, str]]:
        """Find packages with version changes."""
        common_names = set(baseline.keys()) & set(current.keys())
        updated = []

        for name in sorted(common_names):
            if baseline[name] != current[name]:
                updated.append({
                    "name": name,
                    "old_version": baseline[name],
                    "new_version": current[name],
                })

        return updated

    def display_diff_console(self, diff_result: Dict[str, Any]) -> None:
        """Display diff results in console with rich formatting."""
        console.print(f"\n[bold]Baseline:[/bold] {diff_result['baseline_timestamp']}")
        console.print(f"[bold]Current:[/bold] {diff_result['current_timestamp']}\n")

        changes = diff_result.get("changes", {})

        if not changes:
            console.print("[green]✓ No changes detected![/green]")
            return

        for pm_name, pm_changes in changes.items():
            console.print(f"\n[bold cyan]{pm_name.title()}[/bold cyan]")

            # Added packages
            if pm_changes["added"]:
                table = Table(title="Added", box=box.SIMPLE, show_header=True, header_style="bold green")
                table.add_column("Package", style="green")
                table.add_column("Version", style="green")

                for pkg in pm_changes["added"]:
                    table.add_row(pkg["name"], pkg["version"])

                console.print(table)

            # Removed packages
            if pm_changes["removed"]:
                table = Table(title="Removed", box=box.SIMPLE, show_header=True, header_style="bold red")
                table.add_column("Package", style="red")
                table.add_column("Version", style="red")

                for pkg in pm_changes["removed"]:
                    table.add_row(pkg["name"], pkg["version"])

                console.print(table)

            # Updated packages
            if pm_changes["updated"]:
                table = Table(title="Updated", box=box.SIMPLE, show_header=True, header_style="bold yellow")
                table.add_column("Package", style="yellow")
                table.add_column("Old Version", style="red")
                table.add_column("New Version", style="green")

                for pkg in pm_changes["updated"]:
                    table.add_row(pkg["name"], pkg["old_version"], pkg["new_version"])

                console.print(table)

    def export_diff_html(self, diff_result: Dict[str, Any]) -> str:
        """Export diff results as HTML."""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>System Diff Report</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        h1 { color: #333; }
        .meta { color: #666; margin-bottom: 20px; }
        .section { margin: 30px 0; }
        .added { color: #27ae60; }
        .removed { color: #e74c3c; }
        .updated { color: #f39c12; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th { background: #3498db; color: white; padding: 10px; text-align: left; }
        td { padding: 8px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>System Diff Report</h1>
        <div class="meta">
            <p><strong>Baseline:</strong> {baseline}</p>
            <p><strong>Current:</strong> {current}</p>
        </div>
""".format(
            baseline=diff_result["baseline_timestamp"],
            current=diff_result["current_timestamp"]
        )

        changes = diff_result.get("changes", {})
        for pm_name, pm_changes in changes.items():
            html += f'<div class="section"><h2>{pm_name.title()}</h2>'

            if pm_changes["added"]:
                html += '<h3 class="added">Added</h3><table>'
                html += "<tr><th>Package</th><th>Version</th></tr>"
                for pkg in pm_changes["added"]:
                    html += f"<tr><td>{pkg['name']}</td><td>{pkg['version']}</td></tr>"
                html += "</table>"

            if pm_changes["removed"]:
                html += '<h3 class="removed">Removed</h3><table>'
                html += "<tr><th>Package</th><th>Version</th></tr>"
                for pkg in pm_changes["removed"]:
                    html += f"<tr><td>{pkg['name']}</td><td>{pkg['version']}</td></tr>"
                html += "</table>"

            if pm_changes["updated"]:
                html += '<h3 class="updated">Updated</h3><table>'
                html += "<tr><th>Package</th><th>Old Version</th><th>New Version</th></tr>"
                for pkg in pm_changes["updated"]:
                    html += f"<tr><td>{pkg['name']}</td><td>{pkg['old_version']}</td><td>{pkg['new_version']}</td></tr>"
                html += "</table>"

            html += "</div>"

        html += "</div></body></html>"
        return html

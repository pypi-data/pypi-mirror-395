"""Watch mode for continuous monitoring."""

import time
import json
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich import box

from ..core.scanner import SystemScanner
from ..core.config import Config

console = Console()


class WatchMode:
    """Watch for system changes in real-time."""

    def __init__(self, config: Config, interval: int = 60, alert: bool = False) -> None:
        """Initialize watch mode."""
        self.config = config
        self.interval = interval
        self.alert = alert
        self.scanner = SystemScanner(config.data)
        self.baseline: Optional[Dict[str, Any]] = None
        self.watch_file = Path(".sysmap_watch_baseline.json")

    def start(self) -> None:
        """Start watching for changes."""
        console.print("[bold cyan]SysMap Watch Mode[/bold cyan]")
        console.print(f"Monitoring system every {self.interval} seconds...")
        console.print("Press Ctrl+C to stop\n")

        # Get initial baseline
        self.baseline = self.scanner.scan_all()
        self._save_baseline()

        iteration = 0
        while True:
            iteration += 1
            console.print(f"[dim]Scan #{iteration} - {datetime.now().strftime('%H:%M:%S')}[/dim]")

            # Scan current state
            current = self.scanner.scan_all()

            # Check for changes
            changes = self._detect_changes(self.baseline, current)

            if changes:
                self._display_changes(changes)
                if self.alert:
                    self._send_alert(changes)

                # Update baseline
                self.baseline = current
                self._save_baseline()
            else:
                console.print("[green]No changes detected[/green]")

            # Wait for next iteration
            time.sleep(self.interval)

    def _detect_changes(
        self, baseline: Dict[str, Any], current: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detect changes between baseline and current state."""
        changes: Dict[str, Any] = {}

        baseline_pms = baseline.get("package_managers", {})
        current_pms = current.get("package_managers", {})

        for pm_name in set(baseline_pms.keys()) | set(current_pms.keys()):
            baseline_packages = self._get_package_set(baseline_pms.get(pm_name, {}))
            current_packages = self._get_package_set(current_pms.get(pm_name, {}))

            added = current_packages - baseline_packages
            removed = baseline_packages - current_packages

            if added or removed:
                changes[pm_name] = {
                    "added": sorted(list(added)),
                    "removed": sorted(list(removed)),
                }

        return changes

    def _get_package_set(self, pm_data: Dict[str, Any]) -> set:
        """Get set of package names."""
        packages = pm_data.get("packages", [])
        return {pkg.get("name", pkg.get("id", "")) for pkg in packages}

    def _display_changes(self, changes: Dict[str, Any]) -> None:
        """Display detected changes."""
        console.print("\n[bold yellow]Changes detected![/bold yellow]\n")

        for pm_name, pm_changes in changes.items():
            console.print(f"[bold]{pm_name.title()}[/bold]")

            if pm_changes["added"]:
                console.print(f"  [green]+ Added ({len(pm_changes['added'])}):[/green]")
                for pkg in pm_changes["added"]:
                    console.print(f"    - {pkg}")

            if pm_changes["removed"]:
                console.print(f"  [red]- Removed ({len(pm_changes['removed'])}):[/red]")
                for pkg in pm_changes["removed"]:
                    console.print(f"    - {pkg}")

            console.print()

    def _send_alert(self, changes: Dict[str, Any]) -> None:
        """Send alert notification (placeholder for future implementation)."""
        # Future: Integrate with notification systems (email, Slack, Discord, etc.)
        pass

    def _save_baseline(self) -> None:
        """Save current baseline to file."""
        with open(self.watch_file, "w", encoding="utf-8") as f:
            json.dump(self.baseline, f, indent=2)

    def _load_baseline(self) -> Optional[Dict[str, Any]]:
        """Load baseline from file if exists."""
        if self.watch_file.exists():
            with open(self.watch_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

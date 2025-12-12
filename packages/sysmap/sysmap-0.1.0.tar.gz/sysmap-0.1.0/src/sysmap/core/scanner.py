"""Core scanner functionality for collecting system information."""

import subprocess
import json
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime
import platform


class Scanner:
    """Base scanner class for package managers."""

    def __init__(self) -> None:
        self.name = "base"

    def is_available(self) -> bool:
        """Check if this package manager is available on the system."""
        raise NotImplementedError

    def scan(self) -> List[Dict[str, str]]:
        """Scan and return list of installed packages."""
        raise NotImplementedError

    def check_updates(self) -> List[Dict[str, Any]]:
        """Check for available updates."""
        return []

    @staticmethod
    def run_command(cmd: List[str]) -> str:
        """Run a shell command and return output as text."""
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True, timeout=30
            )
            return result.stdout
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return ""


class WingetScanner(Scanner):
    """Scanner for Windows Package Manager (winget)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "winget"

    def is_available(self) -> bool:
        """Check if winget is available."""
        return platform.system() == "Windows" and bool(self.run_command(["winget", "--version"]))

    def scan(self) -> List[Dict[str, str]]:
        """Scan installed Windows applications via winget."""
        import re

        output = self.run_command(["winget", "list"])
        apps = []

        if not output:
            return apps

        lines = output.splitlines()
        for line in lines[5:]:  # Skip header lines
            if not line.strip():
                continue
            parts = re.split(r"\s{2,}", line)
            if len(parts) >= 3:
                apps.append({"name": parts[0], "id": parts[1], "version": parts[2]})
        return apps

    def check_updates(self) -> List[Dict[str, Any]]:
        """Check for available winget updates."""
        output = self.run_command(["winget", "upgrade"])
        updates = []

        if not output:
            return updates

        import re
        lines = output.splitlines()
        for line in lines[5:]:
            if not line.strip() or "available" not in line.lower():
                continue
            parts = re.split(r"\s{2,}", line)
            if len(parts) >= 4:
                updates.append({
                    "name": parts[0],
                    "id": parts[1],
                    "current_version": parts[2],
                    "available_version": parts[3],
                })
        return updates


class PipScanner(Scanner):
    """Scanner for Python packages (pip)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "pip"

    def is_available(self) -> bool:
        """Check if pip is available."""
        try:
            self.run_command([sys.executable, "-m", "pip", "--version"])
            return True
        except Exception:
            return False

    def scan(self) -> List[Dict[str, str]]:
        """Scan installed Python packages."""
        output = self.run_command([sys.executable, "-m", "pip", "list"])
        packages = []
        lines = output.splitlines()
        for line in lines[2:]:  # Skip header
            parts = line.split()
            if len(parts) >= 2:
                packages.append({"name": parts[0], "version": parts[1]})
        return packages

    def check_updates(self) -> List[Dict[str, Any]]:
        """Check for outdated pip packages."""
        output = self.run_command([sys.executable, "-m", "pip", "list", "--outdated", "--format=json"])
        try:
            data = json.loads(output)
            return [
                {
                    "name": pkg["name"],
                    "current_version": pkg["version"],
                    "available_version": pkg["latest_version"],
                }
                for pkg in data
            ]
        except (json.JSONDecodeError, KeyError):
            return []


class NpmScanner(Scanner):
    """Scanner for Node.js global packages (npm)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "npm"

    def is_available(self) -> bool:
        """Check if npm is available."""
        return bool(self.run_command(["npm", "--version"]))

    def scan(self) -> List[Dict[str, str]]:
        """Scan installed npm global packages."""
        output = self.run_command(["npm", "list", "-g", "--depth=0", "--json"])
        try:
            data = json.loads(output)
            packages = [
                {"name": k, "version": v["version"]}
                for k, v in data.get("dependencies", {}).items()
            ]
            return packages
        except (json.JSONDecodeError, KeyError):
            return []

    def check_updates(self) -> List[Dict[str, Any]]:
        """Check for outdated npm packages."""
        output = self.run_command(["npm", "outdated", "-g", "--json"])
        try:
            data = json.loads(output)
            return [
                {
                    "name": name,
                    "current_version": info.get("current", ""),
                    "available_version": info.get("latest", ""),
                }
                for name, info in data.items()
            ]
        except (json.JSONDecodeError, KeyError):
            return []


class BrewScanner(Scanner):
    """Scanner for Homebrew packages (macOS/Linux)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "brew"

    def is_available(self) -> bool:
        """Check if Homebrew is available."""
        return bool(self.run_command(["brew", "--version"]))

    def scan(self) -> List[Dict[str, str]]:
        """Scan installed Homebrew packages."""
        output = self.run_command(["brew", "list", "--versions"])
        packages = []
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                packages.append({"name": parts[0], "version": " ".join(parts[1:])})
        return packages

    def check_updates(self) -> List[Dict[str, Any]]:
        """Check for outdated Homebrew packages."""
        output = self.run_command(["brew", "outdated", "--json"])
        try:
            data = json.loads(output)
            return [
                {
                    "name": pkg["name"],
                    "current_version": pkg["installed_versions"][0] if pkg.get("installed_versions") else "",
                    "available_version": pkg.get("current_version", ""),
                }
                for pkg in data
            ]
        except (json.JSONDecodeError, KeyError):
            return []


class ChocoScanner(Scanner):
    """Scanner for Chocolatey packages (Windows)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "chocolatey"

    def is_available(self) -> bool:
        """Check if Chocolatey is available."""
        return platform.system() == "Windows" and bool(self.run_command(["choco", "--version"]))

    def scan(self) -> List[Dict[str, str]]:
        """Scan installed Chocolatey packages."""
        output = self.run_command(["choco", "list", "--local-only"])
        packages = []
        for line in output.splitlines():
            if " " in line and not line.startswith("Chocolatey"):
                parts = line.split()
                if len(parts) >= 2:
                    packages.append({"name": parts[0], "version": parts[1]})
        return packages

    def check_updates(self) -> List[Dict[str, Any]]:
        """Check for outdated Chocolatey packages."""
        output = self.run_command(["choco", "outdated", "--limit-output"])
        updates = []
        for line in output.splitlines():
            parts = line.split("|")
            if len(parts) >= 3:
                updates.append({
                    "name": parts[0],
                    "current_version": parts[1],
                    "available_version": parts[2],
                })
        return updates


class ScoopScanner(Scanner):
    """Scanner for Scoop packages (Windows)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "scoop"

    def is_available(self) -> bool:
        """Check if Scoop is available."""
        return platform.system() == "Windows" and bool(self.run_command(["scoop", "--version"]))

    def scan(self) -> List[Dict[str, str]]:
        """Scan installed Scoop packages."""
        output = self.run_command(["scoop", "list"])
        packages = []
        lines = output.splitlines()
        for line in lines[2:]:  # Skip header
            parts = line.split()
            if len(parts) >= 2:
                packages.append({"name": parts[0], "version": parts[1]})
        return packages


class SnapScanner(Scanner):
    """Scanner for Snap packages (Linux)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "snap"

    def is_available(self) -> bool:
        """Check if Snap is available."""
        return platform.system() == "Linux" and bool(self.run_command(["snap", "--version"]))

    def scan(self) -> List[Dict[str, str]]:
        """Scan installed Snap packages."""
        output = self.run_command(["snap", "list"])
        packages = []
        lines = output.splitlines()
        for line in lines[1:]:  # Skip header
            parts = line.split()
            if len(parts) >= 2:
                packages.append({"name": parts[0], "version": parts[1]})
        return packages


class FlatpakScanner(Scanner):
    """Scanner for Flatpak packages (Linux)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "flatpak"

    def is_available(self) -> bool:
        """Check if Flatpak is available."""
        return platform.system() == "Linux" and bool(self.run_command(["flatpak", "--version"]))

    def scan(self) -> List[Dict[str, str]]:
        """Scan installed Flatpak packages."""
        output = self.run_command(["flatpak", "list", "--app", "--columns=name,version"])
        packages = []
        for line in output.splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                packages.append({"name": parts[0], "version": parts[1]})
        return packages


class SystemScanner:
    """Main system scanner that coordinates all package manager scanners."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the system scanner with optional configuration."""
        self.config = config or {}
        self.scanners: List[Scanner] = [
            WingetScanner(),
            PipScanner(),
            NpmScanner(),
            BrewScanner(),
            ChocoScanner(),
            ScoopScanner(),
            SnapScanner(),
            FlatpakScanner(),
        ]

    def scan_all(self, check_updates: bool = False) -> Dict[str, Any]:
        """Scan all available package managers and return combined results."""
        results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "node": platform.node(),
            },
            "package_managers": {},
        }

        enabled_scanners = self.config.get("scanners", {})

        for scanner in self.scanners:
            # Skip if disabled in config
            if enabled_scanners and not enabled_scanners.get(scanner.name, True):
                continue

            if scanner.is_available():
                packages = scanner.scan()
                pm_data: Dict[str, Any] = {
                    "count": len(packages),
                    "packages": packages,
                }

                if check_updates:
                    updates = scanner.check_updates()
                    pm_data["updates_available"] = len(updates)
                    pm_data["updates"] = updates

                results["package_managers"][scanner.name] = pm_data

        return results

    def get_summary(self) -> Dict[str, int]:
        """Get a summary count of packages per package manager."""
        data = self.scan_all()
        return {
            name: pm["count"]
            for name, pm in data["package_managers"].items()
        }

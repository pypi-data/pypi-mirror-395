"""CSV exporter."""

import csv
import io
from .base import BaseExporter


class CSVExporter(BaseExporter):
    """Export system data as CSV."""

    def export(self) -> str:
        """Export data to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(["Package Manager", "Package Name", "Version"])

        # Write package data
        for pm_name, pm_data in self.data.get("package_managers", {}).items():
            for package in pm_data.get("packages", []):
                writer.writerow([
                    pm_name,
                    package.get("name", package.get("id", "")),
                    package.get("version", ""),
                ])

        return output.getvalue()

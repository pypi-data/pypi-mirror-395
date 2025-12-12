"""JSON exporter."""

import json
from .base import BaseExporter


class JSONExporter(BaseExporter):
    """Export system data as JSON."""

    def export(self) -> str:
        """Export data to JSON format."""
        return json.dumps(self.data, indent=2, ensure_ascii=False)

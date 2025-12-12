"""YAML exporter."""

import yaml
from .base import BaseExporter


class YAMLExporter(BaseExporter):
    """Export system data as YAML."""

    def export(self) -> str:
        """Export data to YAML format."""
        return yaml.dump(self.data, default_flow_style=False, sort_keys=False, allow_unicode=True)

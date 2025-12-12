"""Base exporter class."""

from typing import Any, Dict
from abc import ABC, abstractmethod


class BaseExporter(ABC):
    """Base class for all exporters."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize exporter with data."""
        self.data = data

    @abstractmethod
    def export(self) -> str:
        """Export data to string format."""
        pass

    def save(self, path: str) -> None:
        """Save exported data to file."""
        content = self.export()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

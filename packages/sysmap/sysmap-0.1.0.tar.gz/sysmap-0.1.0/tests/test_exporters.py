"""Tests for exporter modules."""

import pytest
import json
import yaml
from sysmap.exporters import (
    MarkdownExporter,
    JSONExporter,
    YAMLExporter,
    CSVExporter,
    HTMLExporter,
)


@pytest.fixture
def sample_data():
    """Sample system data for testing."""
    return {
        "timestamp": "2024-01-01T12:00:00",
        "platform": {
            "system": "Windows",
            "release": "11",
            "version": "10.0.22631",
            "machine": "AMD64",
            "node": "DESKTOP-TEST",
        },
        "package_managers": {
            "winget": {
                "count": 2,
                "packages": [
                    {"name": "Git", "id": "Git.Git", "version": "2.52.0"},
                    {"name": "Python", "id": "Python.Python.3.11", "version": "3.11.5"},
                ],
            },
            "pip": {
                "count": 1,
                "packages": [
                    {"name": "click", "version": "8.1.0"},
                ],
            },
        },
    }


class TestMarkdownExporter:
    """Test MarkdownExporter."""

    def test_export(self, sample_data):
        """Test markdown export."""
        exporter = MarkdownExporter(sample_data)
        result = exporter.export()

        assert "# System Inventory Report" in result
        assert "Windows" in result
        assert "Git" in result
        assert "2.52.0" in result

    def test_export_with_updates(self, sample_data):
        """Test markdown export with update information."""
        sample_data["package_managers"]["pip"]["updates"] = [
            {
                "name": "click",
                "current_version": "8.1.0",
                "available_version": "8.2.0",
            }
        ]
        exporter = MarkdownExporter(sample_data)
        result = exporter.export()

        assert "Available Updates" in result


class TestJSONExporter:
    """Test JSONExporter."""

    def test_export(self, sample_data):
        """Test JSON export."""
        exporter = JSONExporter(sample_data)
        result = exporter.export()

        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed["timestamp"] == "2024-01-01T12:00:00"
        assert "package_managers" in parsed


class TestYAMLExporter:
    """Test YAMLExporter."""

    def test_export(self, sample_data):
        """Test YAML export."""
        exporter = YAMLExporter(sample_data)
        result = exporter.export()

        # Should be valid YAML
        parsed = yaml.safe_load(result)
        assert parsed["timestamp"] == "2024-01-01T12:00:00"
        assert "package_managers" in parsed


class TestCSVExporter:
    """Test CSVExporter."""

    def test_export(self, sample_data):
        """Test CSV export."""
        exporter = CSVExporter(sample_data)
        result = exporter.export()

        lines = result.strip().split("\n")
        assert "Package Manager,Package Name,Version" in lines[0]
        assert len(lines) == 4  # Header + 3 packages


class TestHTMLExporter:
    """Test HTMLExporter."""

    def test_export(self, sample_data):
        """Test HTML export."""
        exporter = HTMLExporter(sample_data)
        result = exporter.export()

        assert "<!DOCTYPE html>" in result
        assert "System Inventory Report" in result
        assert "Git" in result
        assert "<table>" in result

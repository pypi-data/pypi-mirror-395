"""Tests for scanner module."""

import pytest
from unittest.mock import Mock, patch
from sysmap.core.scanner import (
    Scanner,
    WingetScanner,
    PipScanner,
    NpmScanner,
    BrewScanner,
    SystemScanner,
)


class TestScanner:
    """Test base Scanner class."""

    def test_run_command_success(self):
        """Test successful command execution."""
        scanner = Scanner()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = Mock(stdout="test output")
            result = scanner.run_command(["echo", "test"])
            assert result == "test output"

    def test_run_command_failure(self):
        """Test failed command execution."""
        scanner = Scanner()
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = scanner.run_command(["nonexistent"])
            assert result == ""


class TestWingetScanner:
    """Test WingetScanner class."""

    def test_scan_empty(self):
        """Test scanning with no output."""
        scanner = WingetScanner()
        with patch.object(scanner, "run_command", return_value=""):
            result = scanner.scan()
            assert result == []

    def test_scan_with_packages(self):
        """Test scanning with package data."""
        scanner = WingetScanner()
        mock_output = """Name                     Id                          Version
----                     --                          -------
Git                      Git.Git                     2.52.0
Python                   Python.Python.3.11          3.11.5
"""
        with patch.object(scanner, "run_command", return_value=mock_output):
            result = scanner.scan()
            assert len(result) == 2
            assert result[0]["name"] == "Git"
            assert result[0]["version"] == "2.52.0"


class TestPipScanner:
    """Test PipScanner class."""

    def test_scan_with_packages(self):
        """Test scanning pip packages."""
        scanner = PipScanner()
        mock_output = """Package    Version
---------- -------
click      8.1.0
pytest     7.4.0
"""
        with patch.object(scanner, "run_command", return_value=mock_output):
            result = scanner.scan()
            assert len(result) == 2
            assert result[0]["name"] == "click"
            assert result[0]["version"] == "8.1.0"


class TestSystemScanner:
    """Test SystemScanner class."""

    def test_scan_all(self):
        """Test scanning all package managers."""
        scanner = SystemScanner()

        # Mock all scanners to return empty results
        with patch.object(WingetScanner, "is_available", return_value=True):
            with patch.object(WingetScanner, "scan", return_value=[]):
                with patch.object(PipScanner, "is_available", return_value=False):
                    result = scanner.scan_all()

        assert "package_managers" in result
        assert "timestamp" in result
        assert "platform" in result

    def test_get_summary(self):
        """Test getting package summary."""
        scanner = SystemScanner()

        with patch.object(scanner, "scan_all") as mock_scan:
            mock_scan.return_value = {
                "package_managers": {
                    "winget": {"count": 10, "packages": []},
                    "pip": {"count": 5, "packages": []},
                }
            }
            summary = scanner.get_summary()

        assert summary == {"winget": 10, "pip": 5}

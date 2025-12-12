"""Tests for exe2txt.cli module."""

from __future__ import annotations

import pytest

from exe2txt.cli import create_parser, main


class TestCLI:
    """Tests for CLI functionality."""

    def test_parser_version(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test --version flag."""
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--version"])
        assert exc_info.value.code == 0

    def test_main_file_not_found(self) -> None:
        """Test main with nonexistent file."""
        result = main(["/nonexistent/file.exe"])
        assert result == 1

    def test_parser_requires_file(self) -> None:
        """Test that parser requires a file argument."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([])

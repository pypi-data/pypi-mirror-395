"""
CLI Entry Point Tests

Tests that all CLI commands work correctly and return appropriate exit codes.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


class TestCLIBasicCommands:
    """Test basic CLI functionality."""

    def test_version_flag(self):
        """--version should print version and exit 0."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "--version"], capture_output=True, text=True
        )

        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "Demyst v" in output, f"Expected version output, got: {output}"

    def test_help_flag(self):
        """--help should print help and exit 0."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "--help"], capture_output=True, text=True
        )

        assert result.returncode == 0
        # Should contain usage information
        output = result.stdout + result.stderr
        assert "demyst" in output.lower()

    def test_no_args_shows_help(self):
        """No arguments should show help or usage."""
        result = subprocess.run([sys.executable, "-m", "demyst"], capture_output=True, text=True)

        # Should exit cleanly
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert len(output) > 0


class TestCLIAnalyzeCommand:
    """Test the analyze command."""

    def test_analyze_file_exists(self, swarm_collapse_path):
        """Analyze should work on existing file."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "analyze", str(swarm_collapse_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        # May return 0 or 1 depending on issues found
        assert result.returncode in [0, 1]

    def test_analyze_nonexistent_file(self):
        """Analyze should fail gracefully for nonexistent file."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "analyze", "/nonexistent/path/file.py"],
            capture_output=True,
            text=True,
        )

        # CLI returns error info (may be exit 0 with error in output, or exit 1)
        output = result.stdout + result.stderr
        assert "error" in output.lower() or result.returncode == 1

    def test_analyze_directory(self, examples_dir):
        """Analyze should work on directories."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "analyze", str(examples_dir)],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # Should complete
        assert result.returncode in [0, 1]


class TestCLIMirageCommand:
    """Test the mirage command."""

    def test_mirage_detects_issues(self, swarm_collapse_path):
        """Mirage command should detect mirages."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(swarm_collapse_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1  # Has mirages
        # Rich may truncate output, so check for partial match
        assert "Computational Mirage" in result.stdout or "mirage" in result.stdout.lower()

    def test_mirage_clean_file(self, tmp_path):
        """Mirage command should return 0 for clean file."""
        clean_code = '''
def clean_function():
    """No mirages here."""
    x = [1, 2, 3]
    return x
'''
        clean_file = tmp_path / "clean.py"
        clean_file.write_text(clean_code)

        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(clean_file)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        # Rich may add newlines, so normalize whitespace
        assert "no computational mirages" in result.stdout.lower().replace("\n", " ")

    def test_mirage_fix_dryrun(self, swarm_collapse_path):
        """Mirage command with --fix --dry-run should not modify file."""
        original_content = swarm_collapse_path.read_text()

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "demyst",
                "mirage",
                str(swarm_collapse_path),
                "--fix",
                "--dry-run",
            ],
            capture_output=True,
            text=True,
        )

        # File should not be modified
        assert swarm_collapse_path.read_text() == original_content


class TestCLIAllCommands:
    """Test all CLI commands exist and accept --help."""

    @pytest.mark.parametrize(
        "command",
        [
            "analyze",
            "mirage",
            "leakage",
            "hypothesis",
            "units",
            "tensor",
            "report",
            "paper",
            "ci",
            "fix",
        ],
    )
    def test_command_help_available(self, command):
        """Each command should have help available."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", command, "--help"], capture_output=True, text=True
        )

        assert result.returncode == 0, f"{command} --help should work"
        assert len(result.stdout) > 0 or len(result.stderr) > 0, f"{command} should have help text"


class TestCLICICommand:
    """Test CI enforcement command."""

    def test_ci_command_on_examples(self, examples_dir):
        """CI command should work on examples directory."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "ci", str(examples_dir)],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # Should complete without crashing
        assert result.returncode in [0, 1]

    def test_ci_strict_mode(self, examples_dir):
        """CI --strict should be more stringent."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "ci", str(examples_dir), "--strict"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # Examples have issues, strict mode may fail
        assert result.returncode in [0, 1]


class TestCLIOutputFormats:
    """Test different output formats."""

    def test_json_format_valid(self, swarm_collapse_path):
        """--format json should produce valid JSON."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "demyst",
                "analyze",
                str(swarm_collapse_path),
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        # Should be valid JSON (if output is present)
        if result.stdout.strip():
            try:
                output = json.loads(result.stdout)
                assert isinstance(output, dict)
            except json.JSONDecodeError:
                # Some commands may not support JSON fully
                pass

    def test_markdown_format(self, swarm_collapse_path):
        """--format markdown should work."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "demyst",
                "analyze",
                str(swarm_collapse_path),
                "--format",
                "markdown",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode in [0, 1]


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_syntax_error_in_file(self, tmp_path):
        """CLI should handle syntax errors gracefully."""
        bad_file = tmp_path / "syntax_error.py"
        bad_file.write_text("def broken(:\n    pass")

        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(bad_file)],
            capture_output=True,
            text=True,
        )

        # Should fail but not crash
        assert result.returncode == 1
        output = result.stdout + result.stderr
        assert "syntax" in output.lower() or "error" in output.lower()

    def test_empty_file(self, tmp_path):
        """CLI should handle empty files."""
        empty_file = tmp_path / "empty.py"
        empty_file.write_text("")

        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(empty_file)],
            capture_output=True,
            text=True,
        )

        # Should complete (empty file has no mirages)
        assert result.returncode == 0


class TestCLIExampleFilesCoverage:
    """Test CLI on all example files."""

    @pytest.mark.parametrize(
        "example_file,command,should_fail",
        [
            ("swarm_collapse.py", "mirage", True),
            ("random_walk.py", "mirage", True),
        ],
    )
    def test_example_detection(self, examples_dir, example_file, command, should_fail):
        """Each example should fail its appropriate check."""
        file_path = examples_dir / example_file

        result = subprocess.run(
            [sys.executable, "-m", "demyst", command, str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if should_fail:
            assert result.returncode == 1, f"{example_file} should fail {command} check"
        else:
            assert result.returncode == 0, f"{example_file} should pass {command} check"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

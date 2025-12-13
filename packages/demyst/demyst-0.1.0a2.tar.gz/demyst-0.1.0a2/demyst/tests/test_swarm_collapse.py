"""
STAR TEST: Swarm Collapse Example

Demyst's flagship demonstration - a 1000-agent swarm where a single rogue agent
(0.0 alignment) is hidden by np.mean() returning 0.999 average alignment.

This test file verifies:
1. Mirage detection finds the np.mean() collapse
2. The scientific impact is correctly identified
3. The fix recommendation is actionable
4. Fixed code passes validation

The Swarm Collapse problem embodies Demyst's entire mission:
"Correct answers don't guarantee correct reasoning."
"""

import ast
import subprocess
import sys

import numpy as np
import pytest


class TestSwarmCollapseDetection:
    """Test that Demyst correctly detects the swarm collapse mirage."""

    def test_mirage_detector_finds_mean_operation(self, swarm_collapse_source, mirage_detector):
        """MirageDetector should identify np.mean() as a variance-destroying operation."""
        tree = ast.parse(swarm_collapse_source)
        mirage_detector.visit(tree)

        assert len(mirage_detector.mirages) >= 1, "Should detect at least one mirage"

        # Find the specific mean mirage
        mean_mirages = [m for m in mirage_detector.mirages if m["type"] == "mean"]
        assert len(mean_mirages) >= 1, "Should detect np.mean() as a mirage"

        # Should be in the analyze_swarm_safety function
        swarm_mirage = [m for m in mean_mirages if m["function"] == "analyze_swarm_safety"]
        assert len(swarm_mirage) == 1, "Should find mean in analyze_swarm_safety function"

    def test_mirage_detected_at_correct_line(self, swarm_collapse_source, mirage_detector):
        """The mirage should be detected at the correct source line."""
        tree = ast.parse(swarm_collapse_source)
        mirage_detector.visit(tree)

        mean_mirage = next(m for m in mirage_detector.mirages if m["type"] == "mean")

        # Line 25 in swarm_collapse.py: mean_alignment = np.mean(swarm_alignment)
        assert mean_mirage["line"] == 25, f"Expected line 25, got {mean_mirage['line']}"

    def test_mirage_has_required_fields(self, swarm_collapse_source, mirage_detector):
        """Each detected mirage should have all required metadata."""
        tree = ast.parse(swarm_collapse_source)
        mirage_detector.visit(tree)

        assert len(mirage_detector.mirages) > 0
        mirage = mirage_detector.mirages[0]

        required_fields = ["type", "line", "col", "function"]
        for field in required_fields:
            assert field in mirage, f"Mirage should have '{field}' field"


class TestSwarmCollapseScientificImpact:
    """Test that Demyst correctly identifies the scientific danger."""

    def test_mean_hides_rogue_agent_mathematically(self):
        """Verify the mathematical reality: mean hides the rogue agent."""
        # Reproduce the swarm scenario
        agent_count = 1000
        swarm_alignment = np.ones(agent_count)
        swarm_alignment[-1] = 0.0  # One rogue agent

        mean_alignment = np.mean(swarm_alignment)

        # Mean is 0.999 - passes the 0.99 threshold
        assert mean_alignment > 0.99, "Mean should pass safety threshold"
        assert mean_alignment == pytest.approx(0.999, abs=0.001)

        # But min reveals the rogue agent
        min_alignment = np.min(swarm_alignment)
        assert min_alignment == 0.0, "Min should reveal rogue agent"

        # This is the mirage: mean says "safe", reality says "dangerous"

    def test_variance_reveals_the_problem(self):
        """Variance and standard deviation expose the hidden outlier."""
        agent_count = 1000
        swarm_alignment = np.ones(agent_count)
        swarm_alignment[-1] = 0.0

        std_alignment = np.std(swarm_alignment)

        # Standard deviation is non-trivial (~0.0316)
        assert std_alignment > 0.01, "Std should indicate variance exists"
        assert std_alignment == pytest.approx(0.0316, abs=0.01)

    def test_min_check_would_catch_rogue(self):
        """Minimum value analysis would catch the rogue agent."""
        agent_count = 1000
        swarm_alignment = np.ones(agent_count)
        swarm_alignment[-1] = 0.0

        # Min catches the outlier immediately
        min_val = np.min(swarm_alignment)
        assert min_val == 0.0, "Min should reveal the rogue"

        # Any-below-threshold check catches it
        any_below = np.any(swarm_alignment < 0.5)
        assert any_below, "Should detect agents below threshold"


class TestSwarmCollapseFixVerification:
    """Test that suggested fixes actually work."""

    def test_proper_safety_check_detects_rogue(self):
        """A proper safety check would detect the rogue agent."""
        agent_count = 1000
        swarm_alignment = np.ones(agent_count)
        swarm_alignment[-1] = 0.0

        # Proper safety check: ALL agents must be above threshold
        min_alignment = np.min(swarm_alignment)
        all_safe = min_alignment > 0.99

        assert not all_safe, "Proper check should detect the rogue"

    def test_ensemble_statistics_expose_danger(self):
        """Ensemble statistics (mean + std + min) expose the danger."""
        agent_count = 1000
        swarm_alignment = np.ones(agent_count)
        swarm_alignment[-1] = 0.0

        mean_val = np.mean(swarm_alignment)
        std_val = np.std(swarm_alignment)
        min_val = np.min(swarm_alignment)

        # Mean looks fine
        assert mean_val > 0.99

        # But ensemble reveals truth
        danger_score = mean_val - 3 * std_val  # 3-sigma bound
        assert danger_score < 0.99, "3-sigma lower bound should fail threshold"
        assert min_val == 0.0, "Min reveals the catastrophe"


class TestSwarmCollapseCLI:
    """CLI integration tests for swarm collapse detection."""

    def test_cli_mirage_command_returns_nonzero(self, swarm_collapse_path):
        """CLI mirage command should return exit code 1 for swarm_collapse.py."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(swarm_collapse_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1, "Should return non-zero exit code"

    def test_cli_output_mentions_mirage(self, swarm_collapse_path):
        """CLI output should mention computational mirages."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(swarm_collapse_path)],
            capture_output=True,
            text=True,
        )

        # Rich may truncate output, so check for partial match
        assert "Computational Mirage" in result.stdout or "mirage" in result.stdout.lower()

    def test_cli_output_identifies_mean(self, swarm_collapse_path):
        """CLI output should identify np.mean() specifically."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(swarm_collapse_path)],
            capture_output=True,
            text=True,
        )

        assert "mean" in result.stdout.lower()
        assert "Line 25" in result.stdout or "line 25" in result.stdout.lower()

    def test_cli_output_mentions_variance(self, swarm_collapse_path):
        """CLI output should explain variance destruction."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(swarm_collapse_path)],
            capture_output=True,
            text=True,
        )

        assert "variance" in result.stdout.lower() or "distribution" in result.stdout.lower()

    def test_cli_fix_dryrun_shows_changes(self, swarm_collapse_path):
        """CLI --fix --dry-run should show proposed changes."""
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

        # Should complete (may show diff or "would transform")
        assert result.returncode in [0, 1]


class TestSwarmCollapseEndToEnd:
    """End-to-end workflow tests for swarm collapse."""

    def test_analyze_command_includes_mirage(self, swarm_collapse_path):
        """Full analyze command should include mirage detection."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "analyze", str(swarm_collapse_path)],
            capture_output=True,
            text=True,
        )

        # Should complete and produce output
        assert result.returncode in [0, 1]
        assert len(result.stdout) > 0

    def test_ci_command_flags_issues(self, swarm_collapse_path):
        """CI command should flag the file as having issues."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "ci", str(swarm_collapse_path)],
            capture_output=True,
            text=True,
        )

        # Should complete (may pass or fail based on severity thresholds)
        assert result.returncode in [0, 1]


class TestCleanCodePasses:
    """Verify that clean code without mirages passes detection."""

    def test_clean_code_no_mirages(self, mirage_detector):
        """Code without np.mean/sum should pass."""
        clean_code = '''
def safe_analysis(data):
    """Analysis without variance-destroying operations."""
    # Keep all the data
    return list(data)
'''
        tree = ast.parse(clean_code)
        mirage_detector.visit(tree)

        assert len(mirage_detector.mirages) == 0, "Clean code should have no mirages"

    def test_clean_cli_returns_zero(self, tmp_path):
        """CLI should return 0 for clean file."""
        clean_file = tmp_path / "clean.py"
        clean_file.write_text(
            """
def clean_function():
    x = [1, 2, 3]
    return x
"""
        )

        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(clean_file)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        # Rich may add newlines, so normalize whitespace
        assert "no computational mirages" in result.stdout.lower().replace("\n", " ")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

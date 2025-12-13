"""
Data Leakage Detection Tests for Example Files

Tests that LeakageHunter correctly detects issues in:
- ml_data_leakage.py
"""

import subprocess
import sys

import pytest


class TestMLDataLeakage:
    """Tests for ml_data_leakage.py leakage detection."""

    def test_leakage_hunter_analyzes_without_error(self, ml_data_leakage_source, leakage_hunter):
        """LeakageHunter should analyze the file without raising exceptions."""
        result = leakage_hunter.analyze(ml_data_leakage_source)
        assert "error" not in result or result.get("error") is None

    def test_detects_preprocessing_leakage(self, ml_data_leakage_source, leakage_hunter):
        """Should detect fit_transform() before train_test_split."""
        result = leakage_hunter.analyze(ml_data_leakage_source)

        preprocessing_violations = [
            v for v in result["violations"] if v["type"] == "preprocessing_leakage"
        ]

        assert (
            len(preprocessing_violations) >= 1
        ), "Should detect preprocessing leakage (fit_transform before split)"

    def test_summary_shows_critical_violations(self, ml_data_leakage_source, leakage_hunter):
        """Summary should report critical violations."""
        result = leakage_hunter.analyze(ml_data_leakage_source)

        assert result["summary"]["critical_count"] >= 1, "Should have critical violations"
        assert "FAIL" in result["summary"]["verdict"], "Verdict should indicate failure"

    def test_has_meaningful_recommendations(self, ml_data_leakage_source, leakage_hunter):
        """Each violation should have a recommendation."""
        result = leakage_hunter.analyze(ml_data_leakage_source)

        for violation in result["violations"]:
            assert violation.get(
                "recommendation"
            ), f"Violation at line {violation['line']} missing recommendation"


class TestLeakageCLI:
    """Test CLI leakage command on example files."""

    def test_leakage_command_detects_issues(self, examples_dir):
        """Leakage command should detect issues and return non-zero exit code."""
        file_path = examples_dir / "ml_data_leakage.py"

        result = subprocess.run(
            [sys.executable, "-m", "demyst", "leakage", str(file_path)],
            capture_output=True,
            text=True,
        )

        # Should fail (exit code 1) due to leakage
        assert result.returncode == 1, "ml_data_leakage.py should fail leakage check"
        # Output should mention leakage
        assert "leakage" in result.stdout.lower() or "leakage" in result.stderr.lower()


class TestLeakagePatterns:
    """Test specific leakage patterns are detected."""

    @pytest.mark.parametrize(
        "code_snippet,expected_type",
        [
            (
                """
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled)
""",
                "preprocessing_leakage",
            ),
        ],
    )
    def test_detects_specific_patterns(self, leakage_hunter, code_snippet, expected_type):
        """Should detect specific leakage patterns."""
        result = leakage_hunter.analyze(code_snippet)

        violation_types = [v["type"] for v in result["violations"]]
        assert (
            expected_type in violation_types
        ), f"Should detect {expected_type}, found: {violation_types}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

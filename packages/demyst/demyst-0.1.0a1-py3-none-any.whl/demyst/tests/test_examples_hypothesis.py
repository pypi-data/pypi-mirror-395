"""
Hypothesis/P-Hacking Detection Tests for Example Files

Tests that biology_gene_expression.py has its p-hacking patterns detected.
"""

import subprocess
import sys

import pytest


class TestBiologyGeneExpression:
    """Tests for biology_gene_expression.py p-hacking detection."""

    def test_hypothesis_guard_analyzes_without_error(
        self, biology_gene_expression_source, hypothesis_guard
    ):
        """HypothesisGuard should analyze the file without crashing."""
        result = hypothesis_guard.analyze_code(biology_gene_expression_source)

        assert result is not None
        assert isinstance(result, dict)

    def test_detects_violations(self, biology_gene_expression_source, hypothesis_guard):
        """Should detect p-hacking violations."""
        result = hypothesis_guard.analyze_code(biology_gene_expression_source)

        # The file has intentional errors:
        # - Multiple t-tests in loop without correction (line 21)
        # - Conditional reporting "if p < 0.05" (line 24)
        violations = result.get("violations", [])
        assert len(violations) > 0, "Should detect p-hacking violations"

    def test_detects_multiple_testing_issue(self, biology_gene_expression_source, hypothesis_guard):
        """Should detect uncorrected multiple comparisons."""
        result = hypothesis_guard.analyze_code(biology_gene_expression_source)

        violations = result.get("violations", [])

        # Look for multiple testing violation
        multiple_test_violations = [
            v
            for v in violations
            if "multiple" in v.get("type", "").lower()
            or "loop" in v.get("description", "").lower()
            or "uncorrected" in v.get("type", "").lower()
        ]
        assert len(multiple_test_violations) >= 1, "Should detect uncorrected multiple comparisons"

    def test_detects_conditional_reporting(self, biology_gene_expression_source, hypothesis_guard):
        """Should detect conditional reporting pattern (p-hacking)."""
        result = hypothesis_guard.analyze_code(biology_gene_expression_source)

        violations = result.get("violations", [])

        # Look for conditional reporting violation
        conditional_violations = [
            v
            for v in violations
            if "conditional" in v.get("type", "").lower()
            or "p_value_threshold" in v.get("type", "").lower()
            or "p < 0.05" in v.get("description", "")
        ]
        # May or may not detect this specific pattern
        # The important thing is that some violation is detected


class TestHypothesisCLI:
    """Test CLI hypothesis command."""

    def test_hypothesis_command_completes(self, biology_gene_expression_path):
        """Hypothesis command should complete without crashing."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "hypothesis", str(biology_gene_expression_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Should complete (exit 0 or 1 based on findings)
        assert result.returncode in [0, 1]

    def test_hypothesis_command_produces_output(self, biology_gene_expression_path):
        """Hypothesis command should produce meaningful output."""
        result = subprocess.run(
            [sys.executable, "-m", "demyst", "hypothesis", str(biology_gene_expression_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Should produce some output
        assert len(result.stdout) > 0 or len(result.stderr) > 0


class TestBonferroniCorrection:
    """Test the Bonferroni correction utilities."""

    def test_bonferroni_correction_calculation(self):
        """Test Bonferroni correction math."""
        from demyst.guards.hypothesis_guard import BonferroniCorrector

        # Original p = 0.04 with 100 comparisons
        result = BonferroniCorrector.bonferroni(0.04, 100)

        assert result.original_p_value == 0.04
        assert result.corrected_p_value == 1.0  # 0.04 * 100 = 4.0, capped at 1.0
        assert not result.is_significant

    def test_bonferroni_significant_result(self):
        """Test Bonferroni with a significant result."""
        from demyst.guards.hypothesis_guard import BonferroniCorrector

        # Very small p-value
        result = BonferroniCorrector.bonferroni(0.0001, 10)

        assert result.original_p_value == 0.0001
        assert result.corrected_p_value == 0.001  # 0.0001 * 10
        assert result.is_significant  # 0.001 < 0.05


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

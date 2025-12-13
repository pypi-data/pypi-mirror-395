"""
Scientific Validation Tests: Statistical Validity

Validates detection of p-hacking, HARKing, and other statistical malpractices.
"""

import textwrap

import pytest

from demyst.guards.hypothesis_guard import HypothesisGuard


class TestStatisticalValidity:

    def setup_method(self):
        self.guard = HypothesisGuard()

    def test_uncorrected_multiple_comparisons(self):
        """Should detect multiple t-tests in a loop without correction."""
        code = textwrap.dedent(
            """
            from scipy.stats import ttest_ind
            
            def check_features(data, labels):
                significant_features = []
                for feature in data.columns:
                    stat, p = ttest_ind(data[feature], labels)
                    # P-hacking: No correction for multiple comparisons
                    if p < 0.05:
                        significant_features.append(feature)
                return significant_features
        """
        )

        result = self.guard.analyze_code(code)

        # Check for conditional reporting or uncorrected multiple tests
        # The analyzer detects "conditional_reporting" (p < 0.05)
        # And potentially "uncorrected_multiple_tests" if it detects the loop context

        violations = [v for v in result["violations"] if v["type"] == "conditional_reporting"]
        assert len(violations) > 0

    def test_optional_stopping(self):
        """Should detect stopping data collection when p < 0.05."""
        code = textwrap.dedent(
            """
            from scipy.stats import ttest_ind
            
            def run_experiment_until_significant(generator):
                data = []
                while True:
                    data.extend(generator.get_batch())
                    stat, p = ttest_ind(data, control)
                    
                    # P-hacking: Early stopping on significance
                    if p < 0.05:
                        print("Found significance!")
                        break
        """
        )

        result = self.guard.analyze_code(code)
        violations = [
            v for v in result["violations"] if v["type"] == "selective_early_exit_on_significance"
        ]
        assert len(violations) > 0

    @pytest.mark.xfail(reason="HARKing pattern detection not yet implemented in HypothesisGuard.")
    def test_harking_pattern(self):
        """Should flag hypothesizing after results are known (HARKing)."""
        code = textwrap.dedent(
            """
            from scipy.stats import ttest_ind

            def analyze_and_reframe(data, labels):
                stat, p = ttest_ind(data, labels)
                if p < 0.05:
                    # Post-hoc hypothesis based on result
                    hypothesis = "Group A is superior"
                    return hypothesis, p
                return "no finding", p
        """
        )

        result = self.guard.analyze_code(code)
        violations = [v for v in result["violations"] if v["type"] == "harking_detected"]
        assert len(violations) > 0

    @pytest.mark.xfail(
        reason="Correction info not emitted yet; placeholder until guard supports BH/FDR metadata."
    )
    def test_multiple_comparisons_fdr(self):
        """Should recommend BH/FDR correction when many tests run."""
        code = textwrap.dedent(
            """
            import numpy as np
            from scipy import stats

            def many_tests(features, labels):
                ps = []
                for col in features.columns:
                    _, p = stats.ttest_ind(features[col], labels)
                    ps.append(p)
                # Report min p without correction
                return min(ps)
        """
        )

        result = self.guard.analyze_code(code)
        assert result["correction_info"] is not None
        assert result["correction_info"]["num_tests_detected"] > 1

    def test_domain_fishing_psychology(self):
        """Should detect questionnaire fishing without correction."""
        code = textwrap.dedent(
            """
            import numpy as np
            from scipy.stats import pearsonr

            def survey_fishing(responses, outcome):
                findings = []
                for question in responses.columns:
                    r, p = pearsonr(responses[question], outcome)
                    if p < 0.05:
                        findings.append(question)
                return findings
        """
        )

        result = self.guard.analyze_code(code)
        violations = [
            v
            for v in result["violations"]
            if v["type"] in {"conditional_reporting", "uncorrected_multiple_tests"}
        ]
        assert len(violations) > 0

    def test_physics_sigma_thresholds(self):
        """Should NOT flag legitimate 3-sigma/5-sigma checks in physics mode."""
        code = textwrap.dedent(
            """
            def check_discovery(p_value):
                # 5-sigma threshold (approx 2.87e-7)
                if p_value < 2.9e-7:
                    print("Discovery claimed!")
        """
        )

        # Standard mode: should flag p-value check
        guard_standard = HypothesisGuard()
        result_std = guard_standard.analyze_code(code)
        assert len(result_std["violations"]) > 0

        # Physics mode: should pass
        guard_physics = HypothesisGuard(config={"physics_mode": True})
        result_phy = guard_physics.analyze_code(code)
        assert len(result_phy["violations"]) == 0


class TestCherryPicking:
    """Tests for reporting bias and cherry picking."""

    def test_detects_cherry_picking_from_tracker(self):
        """Should flag when only the best result is reported from multiple runs."""
        guard = HypothesisGuard()
        tracker = guard.tracker

        # Simulate 20 experiments
        import random

        random.seed(42)
        for i in range(20):
            val = random.gauss(0, 1)
            tracker.record_experiment(
                hyperparameters={"run": i},
                seed=i,
                metric_name="accuracy",
                metric_value=val,
                code="experiment_code()",
            )

        # Report the best value (max)
        best_val = max(e.metric_value for e in tracker.experiments)

        # Check validation
        # Validate reporting a "statistically significant" result that is actually just the best of random noise
        # Note: accuracy isn't p-value, but let's assume we report a p-value
        # For p-values:
        for i in range(20):
            # Simulate uniform p-values (null hypothesis true)
            p = random.random()
            tracker.record_experiment(
                hyperparameters={"run": i},
                seed=i,
                metric_name="p_value_metric",
                metric_value=0.0,
                p_value=p,
            )

        # Find minimum p-value
        best_p = min(e.p_value for e in tracker.experiments if e.metric_name == "p_value_metric")

        validation = guard.validate_reported_result(
            reported_p=best_p, reported_metric=0.0, metric_name="p_value_metric"
        )

        assert validation["verdict"] == "INVALID"
        assert any(i["type"] == "cherry_picking_detected" for i in validation["issues"])

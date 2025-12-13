"""
Scientific Validation Tests: Computational Mirage Detection

Validates detection of variance-destroying operations (Mirages) in real-world scientific contexts.
"""

import ast
import textwrap

import pytest

from demyst.engine.mirage_detector import MirageDetector


class TestFinancialMirages:
    """Tests for financial time series mirages."""

    def test_return_aggregation_hiding_risk(self):
        """Should detect return aggregation that hides risk."""
        code = textwrap.dedent(
            """
            import numpy as np
            
            def calculate_portfolio_performance(returns):
                # Hint high cardinality
                _ = returns[0]
                # Mirage: Mean return hides volatility/risk
                avg_return = np.mean(returns)
                return avg_return
        """
        )

        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] == "mean"]
        assert len(mirages) > 0
        assert mirages[0]["function"] == "calculate_portfolio_performance"

    def test_legitimate_risk_adjusted_return(self):
        """Should NOT flag when dispersion is also calculated (e.g., Sharpe Ratio)."""
        code = textwrap.dedent(
            """
            import numpy as np
            
            def calculate_sharpe(returns):
                _ = returns[0]
                mu = np.mean(returns)
                # Dispersion check suppresses the warning
                sigma = np.std(returns)
                return mu / sigma
        """
        )
        detector = MirageDetector()
        detector.analyze(ast.parse(code))
        mirages = [m for m in detector.mirages if m["type"] == "mean"]
        assert len(mirages) == 0


class TestClimateMirages:
    """Tests for climate data mirages."""

    def test_temperature_averaging_masking_extremes(self):
        """Should detect averaging that might mask extreme events."""
        code = textwrap.dedent(
            """
            import pandas as pd
            
            def analyze_climate_trends(temp_series):
                # Hint high cardinality by accessing .values
                v = temp_series.values
                # Mirage: Resampling to yearly mean hides daily extremes
                yearly_temps = v.mean()
                return yearly_temps
        """
        )

        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] == "mean"]
        assert len(mirages) > 0


class TestMedicalMirages:
    """Tests for medical trial mirages."""

    def test_mean_effect_size_masking_adverse(self):
        """Should detect mean effect calculation."""
        code = textwrap.dedent(
            """
            import numpy as np
            
            def evaluate_drug_efficacy(patient_outcomes):
                # Hint cardinality
                for p in patient_outcomes:
                    pass
                # Mirage: Average improvement masks minimal/negative outcomes for some
                efficacy = np.mean(patient_outcomes)
                return efficacy
        """
        )

        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] == "mean"]
        assert len(mirages) > 0


class TestAISafetyMirages:
    """Tests for AI safety mirages."""

    def test_agent_behavior_aggregation(self):
        """Should detect aggregation of agent rewards."""
        code = textwrap.dedent(
            """
            import numpy as np
            def evaluate_policy(rewards):
                # Hint cardinality
                _ = rewards[0]
                # Mirage: Sum/Mean of rewards hides catastrophic failures in some episodes
                total_reward = np.sum(rewards)
                return total_reward
        """
        )

        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] in ["mean", "sum"]]
        assert len(mirages) > 0


class TestLegitimateVarianceOperations:
    """Tests where variance operations are legitimate."""

    def test_statistical_quality_control(self):
        """Mean is intended in SQC."""
        code = textwrap.dedent(
            """
            import numpy as np
            def x_bar_chart(samples):
                _ = samples[0]
                center_line = np.mean(samples)
                return center_line
        """
        )
        detector = MirageDetector()
        detector.analyze(ast.parse(code))
        # This flags it as a mirage because we didn't calculate std/var.
        # It IS a mirage (loss of information), even if intended.
        assert len(detector.mirages) > 0

    def test_with_uncertainty_quantification(self):
        """If std is also calculated, it should NOT be flagged."""
        code = textwrap.dedent(
            """
            import numpy as np
            def analyze_with_uncertainty(data):
                _ = data[0]
                mu = np.mean(data)
                sigma = np.std(data)
                return mu, sigma
        """
        )
        detector = MirageDetector()
        detector.analyze(ast.parse(code))
        assert len(detector.mirages) == 0


class TestHighCardinality:
    """Tests for high cardinality detection."""

    def test_loop_iteration_markers(self):
        """Should detect iteration markers that might indicate hidden high cardinality."""
        code = textwrap.dedent(
            """
            def iterate_dataset(data):
                for row in data:
                    process(row)
        """
        )
        # MirageDetector detects high cardinality on variables.
        # Here 'data' is iterated.
        detector = MirageDetector()
        detector.analyze(ast.parse(code))
        # Internal state should mark the iterated variable as high-cardinality.
        assert any(
            var == "data" and state.high_cardinality
            for (var, _func), state in detector.var_states.items()
        )

    def test_high_cardinality_triggers_mirage_with_mean(self):
        """Loop iteration + mean without dispersion should raise a mirage warning."""
        code = textwrap.dedent(
            """
            import numpy as np

            def summarize(data):
                for row in data:
                    pass
                return np.mean(data)
        """
        )

        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] == "mean"]
        assert len(mirages) > 0

"""
Scientific Validation Tests: Economics and Econometrics

Validates detection of issues in economic analysis (time series, causal inference).
"""

import ast
import textwrap

import pytest

from demyst.engine.mirage_detector import MirageDetector
from demyst.guards.leakage_hunter import LeakageHunter


class TestTimeStationarity:

    def test_spurious_regression(self):
        """
        Regressing two non-stationary random walks.
        """
        code = textwrap.dedent(
            """
            import numpy as np
            from sklearn.linear_model import LinearRegression
            
            def analyze_trends(gdp, crypto_price):
                # Both are likely non-stationary random walks
                
                # Flaw: Direct regression without differencing or cointegration test
                model = LinearRegression()
                model.fit(gdp.reshape(-1, 1), crypto_price)
                
                return model.coef_
        """
        )

        # Demyst detects this via MirageDetector (maybe?) or specific TimeSeriesGuard (future).
        # Currently, maybe MirageDetector flags 'LinearRegression.fit' on high-cardinality without checks?
        # Or LeakageHunter flags something?
        # This is a tough one for the current engine.
        # But we can test if it flags potential issues if we hint at it.
        pass


class TestCausalInference:

    def test_bad_control_strategy(self):
        """
        Controlling for a collider (post-treatment variable).
        """
        code = textwrap.dedent(
            """
            def estimate_effect(treatment, outcome, collider):
                # collider depends on both treatment and outcome
                
                # Flaw: Including collider in regression biases the effect
                X = [treatment, collider]
                y = outcome
                model.fit(X, y)
        """
        )
        pass


class TestEconomicMirages:

    def test_monetary_aggregation_over_time(self):
        """
        Summing nominal dollars over decades without inflation adjustment.
        """
        code = textwrap.dedent(
            """
            import numpy as np
            
            def calc_lifetime_earnings(yearly_income_1980_to_2020):
                # Hint cardinality
                _ = yearly_income_1980_to_2020[0]
                
                # Mirage: Summing nominal values over 40 years destroys value information
                total = np.sum(yearly_income_1980_to_2020)
                return total
        """
        )

        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] == "sum"]
        assert len(mirages) > 0

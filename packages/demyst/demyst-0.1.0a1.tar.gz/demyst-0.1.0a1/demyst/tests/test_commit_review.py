import ast
import os
import unittest

from demyst.config.manager import ConfigManager
from demyst.engine.mirage_detector import MirageDetector
from demyst.guards.hypothesis_guard import SIGMA_TO_PVALUE, HypothesisGuard
from demyst.guards.unit_guard import Dimension, UnitGuard, UnitInferenceEngine


class TestCommitReview(unittest.TestCase):
    """
    Tests added during review of commit 235a1a6 to verify new features.
    """

    def test_natural_units(self):
        """Verify Natural Units Support (c, hbar, G, kB treated as dimensionless)."""
        config = {"natural_units": True}
        guard = UnitGuard(config=config)

        # Test code where c is added to a dimensionless number (would fail in SI)
        # In natural units, c is dimensionless, so 1 + c is valid (1 is dimensionless)
        code = "x = 1 + c"
        result = guard.analyze(code)

        # Should be no violations
        violations = result["violations"]
        self.assertEqual(
            len(violations),
            0,
            f"Expected 0 violations for natural units, got {len(violations)}: {violations}",
        )

        # Test without natural units
        guard_si = UnitGuard(config={"natural_units": False})
        result_si = guard_si.analyze(code)
        # Should fail because 1 is dimensionless and c is Velocity
        self.assertTrue(len(result_si["violations"]) > 0, "Expected violations in SI units")

    def test_physics_sigma_thresholds(self):
        """Verify Physics Sigma Thresholds."""
        config = {"physics_mode": True, "discovery_sigma": 5.0}
        guard = HypothesisGuard(config=config)

        # 5 sigma p-value is approx 2.87e-7.
        # Code checking if p < 3e-7 should be allowed in physics mode.
        code = """
if p_value < 3e-7:
    print("Discovery!")
"""
        result = guard.analyze_code(code)
        violations = result["violations"]

        # Should be no violations because 3e-7 is <= 5-sigma threshold roughly
        self.assertEqual(
            len(violations),
            0,
            f"Expected 0 violations for physics sigma, got {len(violations)}: {violations}",
        )

        # Test standard p-hacking check
        code_bad = "if p_value < 0.05: print('Significant')"
        result_bad = guard.analyze_code(code_bad)
        self.assertTrue(len(result_bad["violations"]) > 0, "Expected violations for p<0.05")

    def test_variance_context(self):
        """Verify Variance Context Checking."""
        detector = MirageDetector(config={"check_variance_context": True})

        # Case 1: Mean with Std nearby (Should pass - no mirage)
        code_context = """
import numpy as np
def analyze(data):
    m = np.mean(data)
    s = np.std(data)
    return m, s
"""
        tree = ast.parse(code_context)
        mirages = detector.analyze(tree)
        self.assertEqual(len(mirages), 0, f"Expected 0 mirages with context, got {len(mirages)}")

        # Case 2: Mean without Std (Should fail - mirage)
        code_no_context = """
import numpy as np
def analyze(data):
    m = np.mean(data)
    return m
"""
        tree = ast.parse(code_no_context)
        mirages = detector.analyze(tree)
        self.assertTrue(len(mirages) > 0, "Expected mirage without context")

        # Case 3: Mean with Std on DIFFERENT variable (Should fail)
        code_diff_var = """
import numpy as np
def analyze(x, y):
    m = np.mean(x)
    s = np.std(y)
    return m, s
"""
        tree = ast.parse(code_diff_var)
        mirages = detector.analyze(tree)
        self.assertTrue(len(mirages) > 0, "Expected mirage when std is on different variable")

    def test_sigma_values(self):
        """Check the sigma to p-value conversions."""
        # 5.0: 2.87e-7.
        val = SIGMA_TO_PVALUE[5.0]
        self.assertAlmostEqual(val, 2.87e-7, delta=0.1e-7)


if __name__ == "__main__":
    unittest.main()

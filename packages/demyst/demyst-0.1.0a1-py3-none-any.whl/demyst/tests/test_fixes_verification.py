import ast

import pytest

from demyst.guards.hypothesis_guard import HypothesisAnalyzer, HypothesisGuard
from demyst.guards.unit_guard import Dimension, UnitGuard, UnitInferenceEngine


class TestBugFixVerification:

    def test_hypothesis_guard_patterns(self):
        """Verify HypothesisGuard fix for p-value name matching."""
        analyzer = HypothesisAnalyzer()

        # Test cases: (variable_name, should_match)
        cases = [
            # True positives
            ("p", True),
            ("p_value", True),
            ("pvalue", True),
            ("pval", True),
            ("p_val", True),
            ("my_p_value", True),
            ("significance_level", True),
            ("final_p", True),
            ("p_hat", True),
            # True negatives (previously false positives)
            ("shape_size", False),
            ("temp", False),
            ("step", False),
            ("epoch", False),
            ("epsilon", False),
            ("kappa", False),
            # Edge cases requested
            ("ap", False),
            ("up", False),
            ("stop", False),
            ("map", False),
            ("push", False),
            ("keep", False),
            ("loop", False),
            # Tricky ones
            ("probability", False),
            ("probs", False),
        ]

        for name, expected in cases:
            # Use a threshold that is NOT in the suspicious list [0.05, 0.01, 0.001, 0.1]
            # to test purely variable name matching.
            node = ast.Compare(
                left=ast.Name(id=name, ctx=ast.Load()),
                ops=[ast.Lt()],
                comparators=[ast.Constant(value=0.042)],
            )

            result = analyzer._is_p_value_check(node)
            assert result == expected, f"Name '{name}': Expected {expected}, got {result}"

    def test_unit_guard_ml_mode(self):
        """Verify UnitGuard behavior in Default (ML) mode."""
        engine = UnitInferenceEngine(config={"ml_patterns": True})

        # In ML mode, width/height are Dimensionless
        assert engine.infer_from_name("width") == Dimension.dimensionless()
        assert engine.infer_from_name("height") == Dimension.dimensionless()
        assert engine.infer_from_name("depth") == Dimension.dimensionless()
        assert engine.infer_from_name("image_width") == Dimension.dimensionless()

        # ML variables should be Dimensionless
        assert engine.infer_from_name("y_pred") == Dimension.dimensionless()
        assert engine.infer_from_name("X_train") == Dimension.dimensionless()
        assert engine.infer_from_name("logits") == Dimension.dimensionless()
        assert engine.infer_from_name("attention_mask") == Dimension.dimensionless()
        assert engine.infer_from_name("bbox") == Dimension.dimensionless()
        assert engine.infer_from_name("val_loss") == Dimension.dimensionless()

        # Physics variables should still be detected if not overridden
        assert engine.infer_from_name("velocity") == Dimension.velocity()
        assert engine.infer_from_name("force") == Dimension.force()

    def test_unit_guard_physics_mode(self):
        """Verify UnitGuard behavior in Physics mode (ml_patterns=False)."""
        engine = UnitInferenceEngine(config={"ml_patterns": False})

        # In Physics mode, width/height are Length
        assert engine.infer_from_name("width") == Dimension.length()
        assert engine.infer_from_name("height") == Dimension.length()
        assert engine.infer_from_name("depth") == Dimension.length()

        # ML variables might be misclassified if they look like physics vars
        # This documents the known behavior:
        # y_pred -> matches y -> Length
        # X_train -> matches x -> Length
        # This is expected behavior when ML patterns are disabled.

        assert engine.infer_from_name("y_pred") == Dimension.length()
        assert engine.infer_from_name("velocity") == Dimension.velocity()

        # Variables that don't match physics patterns should be None
        assert engine.infer_from_name("logits") is None
        assert engine.infer_from_name("dropout") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

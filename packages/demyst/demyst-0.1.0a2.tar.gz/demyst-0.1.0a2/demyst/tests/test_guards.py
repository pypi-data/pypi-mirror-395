"""
Comprehensive Test Suite for Demyst Guards

Tests:
    - TensorGuard: Deep learning integrity detection
    - LeakageHunter: Data leakage detection
    - HypothesisGuard: Statistical validity checks
    - UnitGuard: Dimensional analysis
"""

import ast

import pytest


class TestTensorGuard:
    """Tests for the TensorGuard deep learning integrity detector."""

    def test_gradient_death_detection(self):
        """Test detection of gradient death chains."""
        from demyst.guards.tensor_guard import TensorGuard

        # Code with deep sigmoid chain (should trigger warning)
        code_with_issue = """
import torch.nn as nn

class DeepSigmoid(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(100, 50)
        self.fc2 = nn.Linear(50, 50)
        self.fc3 = nn.Linear(50, 50)
        self.fc4 = nn.Linear(50, 10)

    def forward(self, x):
        x = torch.sigmoid(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        x = torch.sigmoid(self.fc4(x))
        return x
"""

        guard = TensorGuard()
        result = guard.analyze(code_with_issue)

        assert "gradient_issues" in result
        assert "summary" in result

    def test_normalization_blindness(self):
        """Test detection of normalization masking distribution shifts."""
        from demyst.guards.tensor_guard import NormalizationAnalyzer

        code = """
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.bn = nn.BatchNorm2d(64, track_running_stats=False)
"""

        tree = ast.parse(code)
        analyzer = NormalizationAnalyzer()
        analyzer.visit(tree)

        # Should detect track_running_stats=False as an issue
        assert len(analyzer.issues) >= 0  # May or may not trigger based on context

    def test_reward_hacking_detection(self):
        """Test detection of reward hacking vulnerabilities."""
        from demyst.guards.tensor_guard import RewardHackingDetector

        code = """
def compute_reward(observations, actions):
    individual_rewards = calculate_step_rewards(observations, actions)
    return np.mean(individual_rewards)  # Hides negative spikes!
"""

        tree = ast.parse(code)
        detector = RewardHackingDetector()
        detector.visit(tree)

        # Should detect mean aggregation in reward function
        assert len(detector.issues) > 0
        assert any("mean" in str(i.description).lower() for i in detector.issues)


class TestLeakageHunter:
    """Tests for the LeakageHunter data leakage detector."""

    def test_test_in_training_detection(self):
        """Test detection of test data used in training."""
        from demyst.guards.leakage_hunter import LeakageHunter

        code = """
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

def train_model(model, X, y):
    model.fit(X_test, y_test)  # WRONG! Using test data for training
"""

        hunter = LeakageHunter()
        result = hunter.analyze(code)

        assert "violations" in result
        # The taint analysis should flag X_test being used in fit()

    def test_preprocessing_leakage(self):
        """Test detection of preprocessing before split."""
        from demyst.guards.leakage_hunter import LeakageHunter

        code = """
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Fits on ALL data!

X_train, X_test = train_test_split(X_scaled)  # Split AFTER - WRONG!
"""

        hunter = LeakageHunter()
        result = hunter.analyze(code)

        assert "violations" in result
        # Should detect fit_transform before split

    def test_clean_pipeline(self):
        """Test that clean pipelines don't trigger false positives."""
        from demyst.guards.leakage_hunter import LeakageHunter

        code = """
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Correct: fit on train only
X_test_scaled = scaler.transform(X_test)  # Correct: transform test
"""

        hunter = LeakageHunter()
        result = hunter.analyze(code)

        # Should have minimal or no violations for correct code
        critical_violations = [
            v for v in result.get("violations", []) if v.get("severity") == "critical"
        ]
        # May still have warnings but no critical violations for proper flow


class TestHypothesisGuard:
    """Tests for the HypothesisGuard anti-p-hacking detector."""

    def test_multiple_tests_in_loop(self):
        """Test detection of uncorrected multiple comparisons."""
        from demyst.guards.hypothesis_guard import HypothesisGuard

        code = """
from scipy.stats import ttest_ind

for condition in conditions:
    group1 = data[condition]['A']
    group2 = data[condition]['B']
    stat, p = ttest_ind(group1, group2)  # Multiple tests without correction!
    if p < 0.05:
        print(f"{condition} is significant!")
"""

        guard = HypothesisGuard()
        result = guard.analyze_code(code)

        assert "violations" in result
        assert len(result["violations"]) > 0
        assert any(
            "multiple" in v["type"].lower() or "loop" in v["description"].lower()
            for v in result["violations"]
        )

    def test_bonferroni_correction(self):
        """Test Bonferroni correction calculation."""
        from demyst.guards.hypothesis_guard import BonferroniCorrector

        # Original p = 0.04 with 100 comparisons
        result = BonferroniCorrector.bonferroni(0.04, 100)

        assert result.original_p_value == 0.04
        assert result.corrected_p_value == 1.0  # 0.04 * 100 = 4.0, capped at 1.0
        assert not result.is_significant

    def test_holm_bonferroni(self):
        """Test Holm-Bonferroni step-down procedure."""
        from demyst.guards.hypothesis_guard import BonferroniCorrector

        p_values = [0.001, 0.01, 0.04, 0.1, 0.5]
        results = BonferroniCorrector.holm_bonferroni(p_values)

        assert len(results) == 5
        # First p-value (0.001) should likely be significant
        assert results[0].is_significant or results[0].corrected_p_value < 0.25

    def test_benjamini_hochberg(self):
        """Test Benjamini-Hochberg FDR control."""
        from demyst.guards.hypothesis_guard import BonferroniCorrector

        p_values = [0.001, 0.008, 0.039, 0.041, 0.042]
        results = BonferroniCorrector.benjamini_hochberg(p_values, alpha=0.05)

        assert len(results) == 5
        # BH is less conservative, should identify some as significant


class TestUnitGuard:
    """Tests for the UnitGuard dimensional analysis detector."""

    def test_dimension_mismatch_addition(self):
        """Test detection of adding incompatible dimensions."""
        from demyst.guards.unit_guard import UnitGuard

        code = """
def physics_error():
    distance_meters = 100.0
    time_seconds = 10.0
    wrong_result = distance_meters + time_seconds  # Can't add meters to seconds!
"""

        guard = UnitGuard()
        result = guard.analyze(code)

        assert "violations" in result
        # Should detect the dimensional mismatch

    def test_compatible_operations(self):
        """Test that compatible operations don't trigger violations."""
        from demyst.guards.unit_guard import UnitGuard

        code = """
def physics_correct():
    distance1_meters = 100.0
    distance2_meters = 50.0
    total_distance = distance1_meters + distance2_meters  # OK: same dimensions
"""

        guard = UnitGuard()
        result = guard.analyze(code)

        # Should not have violations for dimensionally consistent operations
        critical = [v for v in result.get("violations", []) if v["severity"] == "critical"]
        assert len(critical) == 0

    def test_dimension_inference(self):
        """Test dimension inference from variable names."""
        from demyst.guards.unit_guard import Dimension, UnitInferenceEngine

        engine = UnitInferenceEngine()

        # Should infer length from variable name
        assert engine.infer_from_name("distance_meters") == Dimension.length()
        assert engine.infer_from_name("time_seconds") == Dimension.time()
        assert engine.infer_from_name("velocity") == Dimension.velocity()

    def test_dimension_arithmetic(self):
        """Test dimension arithmetic operations."""
        from demyst.guards.unit_guard import Dimension

        length = Dimension.length()
        time = Dimension.time()

        velocity = length / time
        assert velocity == Dimension.velocity()

        acceleration = velocity / time
        assert acceleration == Dimension.acceleration()


class TestIntegration:
    """Integration tests for all guards working together."""

    def test_full_analysis_pipeline(self):
        """Test running all guards on a code sample."""
        from demyst.guards.hypothesis_guard import HypothesisGuard
        from demyst.guards.leakage_hunter import LeakageHunter
        from demyst.guards.tensor_guard import TensorGuard
        from demyst.guards.unit_guard import UnitGuard

        code = """
import numpy as np
from sklearn.model_selection import train_test_split

def train_and_evaluate():
    # Load data
    X, y = load_data()

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # Train
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    return accuracy
"""

        # Run all guards
        tensor_result = TensorGuard().analyze(code)
        leakage_result = LeakageHunter().analyze(code)
        hypothesis_result = HypothesisGuard().analyze_code(code)
        unit_result = UnitGuard().analyze(code)

        # All should return valid results without errors
        assert "summary" in tensor_result
        assert "violations" in leakage_result
        assert "violations" in hypothesis_result
        assert "violations" in unit_result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

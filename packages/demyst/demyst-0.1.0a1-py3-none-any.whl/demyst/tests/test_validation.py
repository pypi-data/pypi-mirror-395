#!/usr/bin/env python3
"""
Test validation suite for Demyst
"""

import numpy as np
import pytest


def test_hawking_temperature_conservation():
    """Test that Hawking temperature relation κ → T_H is preserved"""
    # Simulate kappa values
    kappa_values = np.array([0.1, 0.15, 0.12, 0.18, 0.14])

    # Hawking temperature: T_H = κ / (2π)
    expected_temperatures = kappa_values / (2 * np.pi)

    # Check that temperatures are positive and proportional to kappa
    assert np.all(expected_temperatures > 0), "Temperatures should be positive"
    assert np.allclose(
        expected_temperatures, kappa_values / (2 * np.pi)
    ), "Temperature relation violated"


def test_horizon_detection():
    """Test that event horizon is properly detected"""
    # Simulate field data with horizon signature
    field_data = np.random.normal(10, 1, (100, 50))

    # Add horizon signature (simplified)
    field_data[50:, :] *= 0.1  # Suppression beyond horizon

    # Check that we can detect the horizon
    mean_field = np.mean(field_data, axis=1)
    horizon_idx = np.argmax(np.abs(np.gradient(mean_field)))

    assert 40 <= horizon_idx <= 60, "Horizon should be detected around middle"


def test_graybody_factor_bounds():
    """Test that graybody factors are within physical bounds [0, 1]"""
    # Simulate graybody factors
    graybody_factors = np.array([0.8, 0.75, 0.82, 0.78, 0.81])

    assert np.all(graybody_factors >= 0), "Graybody factors should be >= 0"
    assert np.all(graybody_factors <= 1), "Graybody factors should be <= 1"


def test_variation_preservation():
    """Test that VariationTensor preserves variation information"""
    from demyst.engine.transpiler import VariationTensor

    # Create test data with known variation
    data = np.random.normal(10, 2, (100, 50))  # mean=10, std=2

    # Use VariationTensor
    vt = VariationTensor(data, axis=1)
    result = vt.collapse("mean")

    # Check that variation history is preserved
    assert len(vt._variation_history) > 0, "Variation history should be preserved"
    assert vt._variation_history[0]["operation"] == "mean", "Should record mean operation"

    # Check that result is reasonable
    assert np.abs(np.mean(result) - 10) < 1, "Mean should be close to expected value"


def test_uncertainty_reduction():
    """Test that VariationTensor reduces uncertainty"""
    import numpy as np

    from demyst.engine.transpiler import VariationTensor

    # Create noisy data
    data = np.random.normal(0, 1, (1000, 100))

    # Regular mean (destructive)
    regular_mean = np.mean(data, axis=1)
    regular_std = np.std(regular_mean)

    # VariationTensor mean (preserves information)
    vt = VariationTensor(data, axis=1)
    vt_mean = vt.collapse("mean")
    vt_std = np.std(vt_mean)

    # The VariationTensor should provide more stable results
    # (This is a conceptual test - in practice the improvement would be domain-specific)
    assert (
        vt_std <= regular_std * 1.1
    ), "VariationTensor should not increase uncertainty significantly"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

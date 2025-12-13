"""
Real Paper Reproduction Tests: Physics

Reproducing code snippets and analysis patterns from major physics papers/projects
to verify Demyst detects potential issues.
"""

import ast
import textwrap

import pytest

from demyst.engine.mirage_detector import MirageDetector
from demyst.guards.hypothesis_guard import HypothesisGuard
from demyst.guards.unit_guard import UnitGuard


class TestLIGOGravitationalWaves:
    """
    Based on analysis patterns in GW detection.
    Focus: Signal processing and filtering.
    """

    def test_naive_bandpass_filtering(self):
        """
        Simulate a naive filtering approach that might induce phase errors or mirages.
        Real LIGO analysis is very careful, but we test if Demyst catches the 'naive' version.
        """
        code = textwrap.dedent(
            """
            import numpy as np
            from scipy.signal import butter, lfilter
            
            def filter_strain_data(strain, fs):
                # Hint high cardinality
                _ = strain[0]
                
                b, a = butter(4, [50, 200], btype='band', fs=fs)
                filtered = lfilter(b, a, strain)
                
                # Hint high cardinality for filtered (as detector doesn't track flow through lfilter)
                _ = filtered[0]
                
                # Mirage: Aggregating filtered signal without noise floor estimation
                avg_strain = np.mean(filtered)
                return avg_strain
        """
        )

        # We expect MirageDetector to flag the 'mean' on the filtered time series
        # because it hides the noise characteristics essential for GW detection.
        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] == "mean"]
        assert len(mirages) > 0


class TestCERNParticlePhysics:
    """
    Based on High Energy Physics (HEP) analysis.
    Focus: Look-elsewhere effect / Multiple testing.
    """

    def test_look_elsewhere_effect(self):
        """
        Simulate searching for a resonance peak across many mass bins (multiple testing).
        """
        code = textwrap.dedent(
            """
            from scipy.stats import poisson
            
            def search_for_resonance(mass_bins, background_model, observed_data):
                significant_bumps = []
                
                # Scanning through 1000 mass bins
                for bin_i in range(len(mass_bins)):
                    obs = observed_data[bin_i]
                    exp = background_model[bin_i]
                    
                    # Compute local p-value
                    p_val = poisson.sf(obs, exp)
                    
                    # Flaw: Checking local significance (5 sigma) without global correction
                    # (Look-Elsewhere Effect)
                    if p_val < 2.87e-7:  # 5 sigma
                        significant_bumps.append(bin_i)
                        
                return significant_bumps
        """
        )

        # We analyze WITHOUT physics mode to ensure the uncorrected check is flagged.
        # Even with 5-sigma, looking in 1000 places requires correction (Look-Elsewhere).
        guard = HypothesisGuard()
        result = guard.analyze_code(code)

        # Should flag "conditional_reporting" (checking p-value)
        # or "uncorrected_multiple_tests" (loop)
        violations = [
            v
            for v in result["violations"]
            if v["type"] in ["uncorrected_multiple_tests", "conditional_reporting"]
        ]
        assert len(violations) > 0


class TestClimateModeling:
    """
    Based on climate model analysis patterns.
    Focus: Averaging and Grid cells.
    """

    def test_grid_cell_averaging(self):
        """
        Averaging temperature over grid cells without area weighting (poles vs equator).
        This is a dimensional/geometric error, but often manifests as a Mirage (simple mean).
        """
        code = textwrap.dedent(
            """
            import numpy as np
            
            def global_average_temperature(grid_temps):
                # grid_temps is a 2D array [lat, lon]
                # Flaw: Simple mean assumes all grid cells have equal area. 
                # (Incorrect for lat/lon grids).
                
                # Hint cardinality
                _ = grid_temps[0]
                
                # Mirage: Mean destroys spatial information and is mathematically wrong without weights
                global_avg = np.mean(grid_temps)
                return global_avg
        """
        )

        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] == "mean"]
        assert len(mirages) > 0

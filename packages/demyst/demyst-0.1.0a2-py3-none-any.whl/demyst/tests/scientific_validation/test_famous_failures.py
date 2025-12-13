"""
Famous Scientific Failures Tests

Simulating code patterns that led to historical scientific errors/controversies.
"""

import textwrap

import pytest

from demyst.engine.mirage_detector import MirageDetector
from demyst.guards.hypothesis_guard import HypothesisGuard
from demyst.guards.unit_guard import UnitGuard


class TestHockeyStickControversy:
    """
    Mann et al. (1998) - PCA centering issue.
    The controversy involved decentralized PCA on red-noise data mining for hockey stick shapes.

    Issue: Performing PCA without proper centering (subtracting mean) or standardization
    can inflate the variance of the first principal component if the data has a trend.
    """

    def test_pca_without_centering(self):
        """
        Simulate PCA on decentralized data.
        """
        code = textwrap.dedent(
            """
            import numpy as np
            from sklearn.decomposition import PCA
            
            def reconstruct_climate(tree_rings):
                # tree_rings: [n_years, n_sites]
                
                # Flaw: No mean subtraction / centering before PCA
                # (sklearn PCA centers by default, but SVD doesn't)
                
                # Let's use SVD which is the raw mechanism often used
                u, s, vh = np.linalg.svd(tree_rings, full_matrices=False)
                
                # First PC
                pc1 = u[:, 0] * s[0]
                return pc1
        """
        )
        # Fallback heuristic: expect no mirage now; mark as xfail until an AlgorithmicValidity guard is added.
        pytest.xfail("PCA centering detection not implemented; placeholder for future guard.")


class TestOPERANeutrinoAnomaly:
    """
    Faster-than-light neutrinos (2011).
    Cause: Loose fiber optic cable + clock oscillator frequency error.
    Code equivalent: Incorrect time delta calculation or missing systematic correction.
    """

    def test_time_of_flight_calculation(self):
        """
        Simulate subtracting times from different clocks without synchronization correction.
        """
        code = textwrap.dedent(
            """
            def calc_neutrino_velocity(t_emit_cern, t_arrive_gran_sasso, distance):
                # t_emit_cern: time in CERN frame (GPS)
                # t_arrive_gran_sasso: time in Gran Sasso frame (GPS)
                
                # Flaw: Naive subtraction without fiber delay correction (systematic error)
                time_of_flight = t_arrive_gran_sasso - t_emit_cern
                
                # velocity = d / t
                v = distance / time_of_flight
                return v
        """
        )
        pytest.xfail("Frame-aware time-of-flight validation not implemented; placeholder.")


class TestWakefieldVaccineStudy:
    """
    1998 study linking MMR to autism.
    Issues: Small sample size (n=12), uncontrolled design, selective sampling.
    """

    def test_small_sample_generalization(self):
        """
        Generalizing from n=12 to population.
        """
        code = textwrap.dedent(
            """
            def analyze_vaccine_risk(patients):
                # n = 12
                autism_cases = 0
                for p in patients:
                    if p.has_autism:
                        autism_cases += 1
                
                risk = autism_cases / len(patients)
                
                # Flaw: Reporting high confidence/generalization on n=12
                if risk > 0.5:
                    print("Significant association found!")
        """
        )

        # MirageDetector might flag the reduction if 'patients' is small?
        # No, it flags high cardinality.
        # HypothesisGuard might flag 'print("Significant...")' without p-value?
        # Or if we ran a test on n=12.

        code_with_test = textwrap.dedent(
            """
            from scipy.stats import fisher_exact
            
            def analyze_vaccine_risk(group_a, group_b):
                # n=12 total
                table = [[8, 4], [1, 11]] # Hypothetical small counts
                oddsr, p = fisher_exact(table)
                
                if p < 0.05:
                    print("Link proven!")
        """
        )

        # HypothesisGuard flags conditional reporting "if p < 0.05".
        guard = HypothesisGuard()
        result = guard.analyze_code(code_with_test)

        violations = [v for v in result["violations"] if v["type"] == "conditional_reporting"]
        assert len(violations) > 0


class TestSokalHoax:
    """
    Transgressing the Boundaries (1996).
    Issue: Meaningless use of physics/math terminology. Dimensional nonsense.
    """

    def test_dimensional_nonsense(self):
        """
        Adding unrelated physical quantities (Quantum Gravity + Hermeneutics?).
        """
        code = textwrap.dedent(
            """
            def quantum_hermeneutics(planck_const_J_s, light_speed_mps):
                # Meaningless addition: Energy*Time + Velocity
                # h [M L^2 T^-1] + c [L T^-1]
                
                result = planck_const_J_s + light_speed_mps
                return result
        """
        )

        guard = UnitGuard()
        result = guard.analyze(code)

        violations = [v for v in result["violations"] if v["type"] == "incompatible_addition"]
        assert len(violations) > 0

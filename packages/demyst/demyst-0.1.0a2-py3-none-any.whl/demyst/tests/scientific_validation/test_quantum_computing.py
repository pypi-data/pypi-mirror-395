"""
Scientific Validation Tests: Quantum Computing

Validates detection of issues specific to quantum circuits and information.
"""

import textwrap

import pytest

from demyst.engine.mirage_detector import MirageDetector
from demyst.guards.unit_guard import UnitGuard


class TestQuantumComputing:

    def test_qubit_decoherence_pattern(self):
        """
        Simulate a long circuit without dynamical decoupling or error correction,
        followed by a measurement. The 'Mirage' here is measuring a decohered state
        assuming it's pure.
        """
        code = textwrap.dedent(
            """
            def run_long_circuit(qubits, depth):
                for d in range(depth):
                    # Long sequence of gates
                    apply_gates(qubits)
                
                # Mirage: Measuring after long time T > T2 implies noise dominance
                # Naive expectation calculation
                exp_val = measure_expectation(qubits)
                return exp_val
        """
        )
        # This is a high-level semantic check. Static analysis might just see a loop.
        # Demyst doesn't have a QuantumGuard yet.
        # But we can test if MirageDetector flags the 'measure_expectation' (reduction)
        # if we hint high cardinality/complexity?
        pass

    def test_dimensional_analysis_in_hamiltonians(self):
        """
        Hamiltonian terms must have Energy dimensions.
        H = J * Z_i * Z_j + h * X_i
        J and h must be Energy.
        """
        code = textwrap.dedent(
            """
            def construct_hamiltonian(J_joules, h_meters):
                # Error: Adding Energy (J) to Length (h_meters * X operator)
                # Assuming operators are dimensionless
                H = J_joules * Z_op + h_meters * X_op
                return H
        """
        )

        guard = UnitGuard()
        result = guard.analyze(code)

        # J_joules * Z_op -> Energy (if Z_op is dimensionless)
        # h_meters * X_op -> Length
        # Addition -> Mismatch

        violations = [v for v in result["violations"] if v["type"] == "incompatible_addition"]
        assert len(violations) > 0

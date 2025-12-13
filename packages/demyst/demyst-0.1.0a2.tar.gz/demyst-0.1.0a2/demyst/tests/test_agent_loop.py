import json
import os
from unittest.mock import MagicMock

import pytest

from demyst.agents.langchain import DemystVerifier

# Test secret key for certificate signing tests
TEST_SECRET_KEY = "test_secret_key_for_demyst_tests_32chars!"


class TestAgentLoop:
    def test_self_healing_loop(self):
        # Set test secret key for signing
        old_key = os.environ.get("DEMYST_SECRET_KEY")
        os.environ["DEMYST_SECRET_KEY"] = TEST_SECRET_KEY

        try:
            verifier = DemystVerifier()

            # Step 1: Agent generates buggy code (Mirage)
            bad_code = """
import numpy as np
data = np.random.exponential(size=1000)
# Bad: Mean on skewed distribution
result = np.mean(data)
            """

            # Step 2: Agent calls Demyst
            feedback = verifier._run(bad_code)

            # Verify feedback contains error
            assert "VERIFICATION FAILED" in feedback
            assert "Computational mirage detected" in feedback
            assert "mean" in feedback

            # Step 3: Agent "fixes" code based on feedback
            fixed_code = """
import numpy as np

data = np.random.exponential(size=1000)
# Good: No variance-destroying operations on the raw data
# Agent keeps the full distribution for downstream analysis
result = data.tolist()  # Just convert for output, preserves all information
            """

            # Step 4: Agent calls Demyst again
            result = verifier._run(fixed_code)

            # Verify success
            assert "VERIFICATION PASSED" in result
            if "Certificate: " in result:
                # Python 3.10+ path with MCP signing available
                cert_str = result.split("Certificate: ")[1]
                cert = json.loads(cert_str)
                assert cert["verdict"] == "PASS"
                assert "signature" in cert
            else:
                # Python 3.9 path: signing unavailable, but pass message is enough
                assert "certificate" in result.lower()
        finally:
            # Restore original key state
            if old_key is None:
                os.environ.pop("DEMYST_SECRET_KEY", None)
            else:
                os.environ["DEMYST_SECRET_KEY"] = old_key

    def test_leakage_detection(self):
        verifier = DemystVerifier()

        leakage_code = """
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Bad: Scaling before splitting (Leakage)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)
        """

        feedback = verifier._run(leakage_code)

        assert "VERIFICATION FAILED" in feedback
        assert "Leakage" in feedback

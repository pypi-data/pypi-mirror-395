import json
import os
import sys

import pytest

# Skip entire module on Python < 3.10 BEFORE importing demyst.mcp
if sys.version_info < (3, 10):
    pytest.skip("MCP integration requires Python 3.10+", allow_module_level=True)

from demyst.mcp import check_units, detect_mirage, sign_verification

# Test secret key for certificate signing tests
TEST_SECRET_KEY = "test_secret_key_for_demyst_tests_32chars!"


class TestMCPServer:
    def test_detect_mirage_found(self):
        code = """
import numpy as np
x = np.random.randn(100)
m = np.mean(x)
        """
        result_json = detect_mirage(code)
        result = json.loads(result_json)

        assert result["has_mirages"] is True
        assert len(result["mirages"]) > 0
        assert result["mirages"][0]["type"] == "mean"

    def test_detect_mirage_clean(self):
        code = "x = 1 + 1"
        result_json = detect_mirage(code)
        result = json.loads(result_json)

        assert result["has_mirages"] is False
        assert len(result["mirages"]) == 0

    def test_check_units_found(self):
        code = """
mass = 10  # unit: kg
time = 5   # unit: s
result = mass + time
        """
        result_json = check_units(code)
        result = json.loads(result_json)

        assert result["consistent"] is False
        assert len(result["violations"]) > 0
        # Updated expectation: UnitGuard returns 'incompatible_addition' for this case
        assert result["violations"][0]["type"] == "incompatible_addition"

    def test_check_units_clean(self):
        code = """
mass = 10  # unit: kg
accel = 9.8 # unit: m/s^2
force = mass * accel
        """
        result_json = check_units(code)
        result = json.loads(result_json)

        if not result["consistent"]:
            print(f"Violations found: {result['violations']}")

        assert result["consistent"] is True
        assert len(result["violations"]) == 0

    def test_sign_verification(self):
        # Set test secret key for signing
        old_key = os.environ.get("DEMYST_SECRET_KEY")
        os.environ["DEMYST_SECRET_KEY"] = TEST_SECRET_KEY

        try:
            code = "print('Hello Science')"
            verdict = "PASS"

            cert_json = sign_verification(code, verdict)
            cert = json.loads(cert_json)

            assert "signature" in cert
            assert "code_hash" in cert
            assert cert["verdict"] == verdict

            # Verify signature changes with content
            cert_json2 = sign_verification(code + " ", verdict)
            cert2 = json.loads(cert_json2)

            assert cert["signature"] != cert2["signature"]
            assert cert["code_hash"] != cert2["code_hash"]
        finally:
            # Restore original key state
            if old_key is None:
                os.environ.pop("DEMYST_SECRET_KEY", None)
            else:
                os.environ["DEMYST_SECRET_KEY"] = old_key

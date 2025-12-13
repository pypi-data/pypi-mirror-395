import os
import unittest

import demyst.security as security


class TestSecurityFeatures(unittest.TestCase):
    def setUp(self):
        # Set a temporary secret key for testing
        self.original_key = os.environ.get("DEMYST_SECRET_KEY")
        os.environ["DEMYST_SECRET_KEY"] = "0" * 32  # 32 bytes

    def tearDown(self):
        # Restore original key
        if self.original_key:
            os.environ["DEMYST_SECRET_KEY"] = self.original_key
        else:
            del os.environ["DEMYST_SECRET_KEY"]

    def test_sign_and_verify(self):
        code = "print('hello world')"
        verdict = "PASS"

        cert = security.sign_code(code, verdict)

        # Verify valid certificate
        self.assertTrue(security.verify_certificate(cert))

        # Verify tampering
        cert_tampered = cert.copy()
        cert_tampered["verdict"] = "FAIL"
        self.assertFalse(security.verify_certificate(cert_tampered))

        # Verify invalid signature
        cert_bad_sig = cert.copy()
        cert_bad_sig["signature"] = "a" * 64
        self.assertFalse(security.verify_certificate(cert_bad_sig))


if __name__ == "__main__":
    unittest.main()

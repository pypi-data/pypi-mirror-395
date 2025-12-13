"""
Real Paper Reproduction: LIGO Gravitational Wave Analysis Snippet

Validates Demyst detects variance-destroying resampling/averaging that can mask transients.
"""

import ast
import textwrap

from demyst.engine.mirage_detector import MirageDetector


class TestLIGOResampling:
    def test_resampling_masks_transients(self):
        """
        In gravitational wave pipelines, aggressive resampling/averaging can hide short transients.
        Expect a mirage when downsampling/averaging high-cardinality strain data without dispersion checks.
        """
        code = textwrap.dedent(
            """
            import numpy as np

            def process_strain(strain_series):
                # High cardinality implied by indexing
                _ = strain_series[0]
                # Mirage: averaging raw strain to 1 Hz without dispersion context
                averaged = np.mean(strain_series)
                return averaged
            """
        )

        detector = MirageDetector()
        detector.analyze(ast.parse(code))

        mirages = [m for m in detector.mirages if m["type"] == "mean"]
        assert len(mirages) > 0

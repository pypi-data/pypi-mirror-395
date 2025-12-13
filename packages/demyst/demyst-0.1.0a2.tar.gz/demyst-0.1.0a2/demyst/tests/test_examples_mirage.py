"""
Mirage Detection Tests for Example Files

Tests that each example file with known mirages is correctly detected.
Covers: swarm_collapse.py, random_walk.py
"""

import ast
import subprocess
import sys

import pytest


class TestSwarmCollapseMirage:
    """Tests for swarm_collapse.py mirage detection."""

    def test_detects_mean_operation(self, swarm_collapse_source, mirage_detector):
        """Should detect np.mean() on line 24."""
        tree = ast.parse(swarm_collapse_source)
        mirage_detector.visit(tree)

        mean_mirages = [m for m in mirage_detector.mirages if m["type"] == "mean"]
        assert len(mean_mirages) == 1
        assert mean_mirages[0]["line"] == 25
        assert mean_mirages[0]["function"] == "analyze_swarm_safety"

    def test_total_mirages_count(self, swarm_collapse_source, mirage_detector):
        """Should detect exactly 1 mirage in swarm_collapse.py."""
        tree = ast.parse(swarm_collapse_source)
        mirage_detector.visit(tree)

        assert len(mirage_detector.mirages) == 1


class TestRandomWalkMirage:
    """Tests for random_walk.py mirage detection."""

    def test_detects_mean_operation(self, random_walk_source, mirage_detector):
        """Should detect np.mean() as mirage."""
        tree = ast.parse(random_walk_source)
        mirage_detector.visit(tree)

        mean_mirages = [m for m in mirage_detector.mirages if m["type"] == "mean"]
        assert len(mean_mirages) >= 1, "Should detect mean operation"

    def test_detects_premature_discretization(self, random_walk_source, mirage_detector):
        """int() applied after reduction should be flagged as discretization."""
        tree = ast.parse(random_walk_source)
        mirage_detector.visit(tree)

        disc_mirages = [
            m for m in mirage_detector.mirages if m["type"] == "premature_discretization"
        ]
        assert len(disc_mirages) >= 1, "Should detect int() discretization"

    def test_total_mirages_count(self, random_walk_source, mirage_detector):
        """Should detect exactly 2 mirages: mean and int()."""
        tree = ast.parse(random_walk_source)
        mirage_detector.visit(tree)

        # np.mean on line 13, int() on line 17
        assert len(mirage_detector.mirages) == 2


class TestAllExamplesMirageCount:
    """Verify expected mirage counts for all examples."""

    @pytest.mark.parametrize(
        "example_name,expected_min_mirages",
        [
            ("swarm_collapse", 1),
            ("random_walk", 2),
        ],
    )
    def test_minimum_mirages_detected(self, examples_dir, example_name, expected_min_mirages):
        """Each example should have at least the expected number of mirages."""
        from demyst.engine.mirage_detector import MirageDetector

        source_path = examples_dir / f"{example_name}.py"
        source = source_path.read_text()

        detector = MirageDetector()
        tree = ast.parse(source)
        detector.visit(tree)

        assert (
            len(detector.mirages) >= expected_min_mirages
        ), f"{example_name}.py should have at least {expected_min_mirages} mirages"


class TestMirageCLI:
    """Test CLI mirage command on example files."""

    @pytest.mark.parametrize(
        "example_file,should_fail",
        [
            ("swarm_collapse.py", True),
            ("random_walk.py", True),
        ],
    )
    def test_mirage_command_exit_codes(self, examples_dir, example_file, should_fail):
        """Mirage command should return appropriate exit codes."""
        file_path = examples_dir / example_file

        result = subprocess.run(
            [sys.executable, "-m", "demyst", "mirage", str(file_path)],
            capture_output=True,
            text=True,
        )

        if should_fail:
            assert result.returncode == 1, f"{example_file} should fail mirage check"
        else:
            assert result.returncode == 0, f"{example_file} should pass mirage check"


class TestInlineSuppression:
    """Test inline suppression comments."""

    def test_demyst_ignore_suppresses_mirage(self):
        """# demyst: ignore should suppress mirage detection."""
        from demyst.engine.mirage_detector import MirageDetector

        source = """
import numpy as np
data = np.array([1, 2, 3, 4, 5])
mean_val = np.mean(data)  # demyst: ignore
"""
        detector = MirageDetector()
        tree = ast.parse(source)
        mirages = detector.analyze(tree, source=source)

        assert len(mirages) == 0, "Suppressed line should not be flagged"

    def test_demyst_ignore_mirage_suppresses(self):
        """# demyst: ignore-mirage should suppress mirage detection."""
        from demyst.engine.mirage_detector import MirageDetector

        source = """
import numpy as np
data = np.array([1, 2, 3, 4, 5])
mean_val = np.mean(data)  # demyst: ignore-mirage
"""
        detector = MirageDetector()
        tree = ast.parse(source)
        mirages = detector.analyze(tree, source=source)

        assert len(mirages) == 0, "Suppressed line should not be flagged"

    def test_unsuppressed_line_still_flagged(self):
        """Lines without suppression should still be flagged."""
        from demyst.engine.mirage_detector import MirageDetector

        source = """
import numpy as np
data = np.array([1, 2, 3, 4, 5])
mean_val = np.mean(data)
"""
        detector = MirageDetector()
        tree = ast.parse(source)
        mirages = detector.analyze(tree, source=source)

        assert len(mirages) >= 1, "Unsuppressed line should be flagged"

    def test_wrong_guard_suppression_does_not_apply(self):
        """# demyst: ignore-leakage should NOT suppress mirage detection."""
        from demyst.engine.mirage_detector import MirageDetector

        source = """
import numpy as np
data = np.array([1, 2, 3, 4, 5])
mean_val = np.mean(data)  # demyst: ignore-leakage
"""
        detector = MirageDetector()
        tree = ast.parse(source)
        mirages = detector.analyze(tree, source=source)

        assert len(mirages) >= 1, "Wrong guard suppression should not apply"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

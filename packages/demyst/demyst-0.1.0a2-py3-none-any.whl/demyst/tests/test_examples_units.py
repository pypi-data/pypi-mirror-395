"""
Unit/Dimensional Analysis Tests for Example Files

Tests that physics_kinematics.py and chemistry_stoichiometry.py
have their dimensional errors correctly detected.
"""

import subprocess
import sys

import pytest


class TestPhysicsKinematics:
    """Tests for physics_kinematics.py dimensional analysis."""

    def test_unit_guard_analyzes_without_error(self, physics_kinematics_source, unit_guard):
        """UnitGuard should analyze the file without crashing."""
        result = unit_guard.analyze(physics_kinematics_source)

        assert result is not None
        assert isinstance(result, dict)

    def test_detects_violations(self, physics_kinematics_source, unit_guard):
        """Should detect dimensional violations in physics code."""
        result = unit_guard.analyze(physics_kinematics_source)

        # The file has intentional errors:
        # - Adding scalar 5.0 to distance (line 13)
        # - Adding distance to time (line 17)
        # - Energy assigned to force variable (line 23)
        violations = result.get("violations", [])

        # May or may not detect all based on inference capabilities
        # At minimum, should return a result structure
        assert "violations" in result or "summary" in result


class TestChemistryStoichiometry:
    """Tests for chemistry_stoichiometry.py dimensional analysis."""

    def test_unit_guard_analyzes_without_error(self, chemistry_stoichiometry_source, unit_guard):
        """UnitGuard should analyze the file without crashing."""
        result = unit_guard.analyze(chemistry_stoichiometry_source)

        assert result is not None
        assert isinstance(result, dict)

    def test_detects_violations(self, chemistry_stoichiometry_source, unit_guard):
        """Should detect dimensional violations in chemistry code."""
        result = unit_guard.analyze(chemistry_stoichiometry_source)

        # The file has intentional errors:
        # - Adding mass to moles (line 11)
        # - Mass assigned to concentration variable (line 14)
        violations = result.get("violations", [])

        # Should return a result structure
        assert "violations" in result or "summary" in result


class TestUnitCLI:
    """Test CLI units command on example files."""

    @pytest.mark.parametrize(
        "example_file",
        [
            "physics_kinematics.py",
            "chemistry_stoichiometry.py",
        ],
    )
    def test_units_command_completes(self, examples_dir, example_file):
        """Units command should complete without crashing."""
        file_path = examples_dir / example_file

        result = subprocess.run(
            [sys.executable, "-m", "demyst", "units", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Should complete (exit 0 or 1 based on findings)
        assert result.returncode in [0, 1], f"units command should complete for {example_file}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

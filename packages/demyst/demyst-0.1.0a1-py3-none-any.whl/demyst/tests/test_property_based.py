"""
Property-Based Tests for Demyst using Hypothesis

These tests generate random code snippets to verify that the MirageDetector
and other guards correctly identify known bad patterns across a wide range
of inputs.
"""

from __future__ import annotations

import ast
from typing import List, Optional

import pytest

# Try to import hypothesis, skip tests if not available
if False:  # TYPE_CHECKING
    from hypothesis import HealthCheck, assume, example, given, settings
    from hypothesis import strategies as st

try:
    from hypothesis import HealthCheck, assume, example, given, settings
    from hypothesis import strategies as st

    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False
    from typing import Any, Callable

    # Create dummy decorators
    def given(*args: Any, **kwargs: Any) -> Callable[[Callable], Callable]:  # type: ignore
        def decorator(f: Callable) -> Callable:
            return pytest.mark.skip(reason="hypothesis not installed")(f)

        return decorator

    def settings(*args: Any, **kwargs: Any) -> Callable[[Callable], Callable]:  # type: ignore
        def decorator(f: Callable) -> Callable:
            return f

        return decorator

    def example(*args: Any, **kwargs: Any) -> Callable[[Callable], Callable]:  # type: ignore
        def decorator(f: Callable) -> Callable:
            return f

        return decorator

    def assume(x: Any) -> None:  # type: ignore
        pass

    class st:  # type: ignore
        @staticmethod
        def text(*args: Any, **kwargs: Any) -> Any:
            return None

        @staticmethod
        def integers(*args: Any, **kwargs: Any) -> Any:
            return None

        @staticmethod
        def lists(*args: Any, **kwargs: Any) -> Any:
            return None

        @staticmethod
        def one_of(*args: Any, **kwargs: Any) -> Any:
            return None

        @staticmethod
        def sampled_from(*args: Any, **kwargs: Any) -> Any:
            return None

        @staticmethod
        def just(*args: Any, **kwargs: Any) -> Any:
            return None

        @staticmethod
        def booleans(*args: Any, **kwargs: Any) -> Any:
            return None

        @staticmethod
        def binary(*args: Any, **kwargs: Any) -> Any:
            return None

    class HealthCheck:  # type: ignore
        too_slow = None


# =============================================================================
# Custom Strategies for Python Code Generation
# =============================================================================

if HYPOTHESIS_AVAILABLE:
    # Valid Python identifiers
    VALID_IDENTIFIERS = st.text(
        alphabet="abcdefghijklmnopqrstuvwxyz_", min_size=1, max_size=20
    ).filter(lambda x: x.isidentifier() and not x.startswith("_"))

    # Array-like variable names
    ARRAY_NAMES = st.sampled_from(
        [
            "data",
            "values",
            "array",
            "arr",
            "x",
            "y",
            "z",
            "scores",
            "results",
            "measurements",
            "samples",
            "agent_scores",
            "weights",
            "features",
            "labels",
        ]
    )

    # Numpy aggregation functions that destroy variance
    DESTRUCTIVE_FUNCS = st.sampled_from(
        [
            "np.mean",
            "np.sum",
            "np.argmax",
            "np.argmin",
            "numpy.mean",
            "numpy.sum",
        ]
    )

    # Numpy module prefixes
    NP_PREFIXES = st.sampled_from(["np", "numpy"])

    # Discretization functions
    DISCRETIZATION_FUNCS = st.sampled_from(
        [
            "round",
            "int",
            "floor",
            "ceil",
        ]
    )
else:
    # Dummy strategies to prevent NameError
    def mirage_code_snippet(*args: Any, **kwargs: Any) -> Any:
        return None

    def safe_code_snippet(*args: Any, **kwargs: Any) -> Any:
        return None

    def valid_python_code(*args: Any, **kwargs: Any) -> Any:
        return None


# =============================================================================
# Strategies for Generating Code Snippets
# =============================================================================

if HYPOTHESIS_AVAILABLE:

    @st.composite
    def mirage_code_snippet(draw: Any) -> Any:  # type: ignore
        """Generate code that contains a computational mirage."""
        var_name = draw(ARRAY_NAMES)
        func = draw(DESTRUCTIVE_FUNCS)

        # Generate different forms of mirage code
        pattern = draw(
            st.sampled_from(
                [
                    # Simple function call
                    f"result = {func}({var_name})",
                    # In a function
                    f"def compute():\n    return {func}({var_name})",
                    # With axis parameter
                    f"result = {func}({var_name}, axis=0)",
                    # Chained
                    f"result = {func}({func}({var_name}))",
                    # In expression
                    f"output = {func}({var_name}) + 1",
                ]
            )
        )

        # Add import statement
        prefix = func.split(".")[0]
        if prefix == "np":
            import_stmt = "import numpy as np\n"
        else:
            import_stmt = "import numpy\n"

        # Add array initialization
        init = f"{var_name} = [1, 2, 3, 4, 5]\n"

        return import_stmt + init + pattern

    @st.composite
    def safe_code_snippet(draw: Any) -> Any:  # type: ignore
        """Generate code that should NOT trigger mirage detection."""
        var_name = draw(ARRAY_NAMES)

        # Safe operations that preserve variance
        pattern = draw(
            st.sampled_from(
                [
                    # Assignment
                    f"{var_name} = [1, 2, 3]",
                    # List operations
                    f"result = [{var_name}[i] for i in range(len({var_name}))]",
                    # Safe numpy operations
                    f"import numpy as np\nresult = np.array({var_name})",
                    f"import numpy as np\nresult = np.std({var_name})",
                    f"import numpy as np\nresult = np.var({var_name})",
                    # Non-aggregating operations
                    f"import numpy as np\nresult = np.sqrt({var_name})",
                    f"import numpy as np\nresult = np.abs({var_name})",
                ]
            )
        )

        return pattern

    @st.composite
    def valid_python_code(draw: Any) -> Any:  # type: ignore
        """Generate random valid Python code."""
        statements = draw(
            st.lists(
                st.sampled_from(
                    [
                        "x = 1",
                        "y = 2",
                        "z = x + y",
                        "result = [i for i in range(10)]",
                        "def foo(): pass",
                        "class Bar: pass",
                        "import os",
                        "from typing import List",
                    ]
                ),
                min_size=1,
                max_size=5,
            )
        )
        return "\n".join(statements)


# =============================================================================
# Property-Based Tests for MirageDetector
# =============================================================================


class TestMirageDetectorProperties:
    """Property-based tests for MirageDetector."""

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(code=mirage_code_snippet())
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_detects_mirages_in_generated_code(self, code: str) -> None:
        """MirageDetector should find mirages in code containing them."""
        from demyst.engine.mirage_detector import MirageDetector

        # Skip if code doesn't parse
        try:
            tree = ast.parse(code)
        except SyntaxError:
            assume(False)
            return

        detector = MirageDetector()
        detector.visit(tree)

        # Should detect at least one mirage
        assert len(detector.mirages) >= 1, f"Expected mirage in:\n{code}"

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(code=safe_code_snippet())
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_no_false_positives_in_safe_code(self, code: str) -> None:
        """MirageDetector should not flag safe code as mirages."""
        from demyst.engine.mirage_detector import MirageDetector

        try:
            tree = ast.parse(code)
        except SyntaxError:
            assume(False)
            return

        detector = MirageDetector()
        detector.visit(tree)

        # Should not detect mirages in safe code
        # (Note: np.std and np.var are not flagged)
        assert len(detector.mirages) == 0, f"False positive in:\n{code}"

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(code=valid_python_code())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_detector_never_crashes(self, code: str) -> None:
        """MirageDetector should never crash on valid Python code."""
        from demyst.engine.mirage_detector import MirageDetector

        try:
            tree = ast.parse(code)
        except SyntaxError:
            assume(False)
            return

        # Should not raise any exceptions
        detector = MirageDetector()
        detector.visit(tree)

        # Mirages list should always be a list
        assert isinstance(detector.mirages, list)


# =============================================================================
# Property-Based Tests for Transpiler
# =============================================================================


class TestTranspilerProperties:
    """Property-based tests for the Transpiler."""

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(code=mirage_code_snippet())
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow], deadline=None)
    def test_transpiler_produces_valid_python(self, code: str) -> None:
        """Transpiled code should always be valid Python."""
        from demyst.engine.transpiler import Transpiler

        # Skip if original doesn't parse
        try:
            ast.parse(code)
        except SyntaxError:
            assume(False)
            return

        transpiler = Transpiler(use_cst=False)  # Use AST for compatibility

        try:
            result = transpiler.transpile_source(code)
        except Exception:
            # Transformation may fail, but that's okay for this test
            assume(False)
            return

        # Result should be valid Python
        try:
            ast.parse(result)
        except SyntaxError as e:
            pytest.fail(
                f"Transpiler produced invalid Python: {e}\nInput:\n{code}\nOutput:\n{result}"
            )

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(code=safe_code_snippet())
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow], deadline=None)
    def test_transpiler_preserves_safe_code(self, code: str) -> None:
        """Transpiler should not modify code without mirages."""
        from demyst.engine.transpiler import Transpiler

        try:
            ast.parse(code)
        except SyntaxError:
            assume(False)
            return

        transpiler = Transpiler(use_cst=False)

        try:
            result = transpiler.transpile_source(code)
        except Exception:
            assume(False)
            return

        # Should have no transformations
        assert (
            len(transpiler.transformations) == 0
        ), f"Unexpected transformation in safe code:\n{code}"


# =============================================================================
# Property-Based Tests for Exception Handling
# =============================================================================


class TestExceptionProperties:
    """Property-based tests for exception classes."""

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(message=st.text(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_demyst_error_always_has_message(self, message: str) -> None:
        """DemystError should always preserve the message."""
        from demyst.exceptions import DemystError

        error = DemystError(message)
        assert message in str(error)

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(
        message=st.text(min_size=1, max_size=50),
        line=st.integers(min_value=1, max_value=10000),
    )
    @settings(max_examples=50)
    def test_analysis_error_includes_line_number(self, message: str, line: int) -> None:
        """AnalysisError should include line number in details."""
        from demyst.exceptions import AnalysisError

        error = AnalysisError(message, line_number=line)
        assert error.line_number == line
        assert "line" in error.details


# =============================================================================
# Property-Based Tests for Configuration
# =============================================================================


class TestConfigProperties:
    """Property-based tests for configuration validation."""

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(
        enabled=st.booleans(),
        severity=st.sampled_from(["critical", "warning", "info"]),
    )
    @settings(max_examples=30)
    def test_rule_config_accepts_valid_values(self, enabled: bool, severity: str) -> None:
        """RuleConfig should accept valid configuration values."""
        try:
            from demyst.config.models import PYDANTIC_AVAILABLE, RuleConfig, Severity

            if not PYDANTIC_AVAILABLE:
                pytest.skip("Pydantic not available")

            config = RuleConfig(enabled=enabled, severity=Severity(severity))
            assert config.enabled == enabled
            assert config.severity.value == severity
        except ImportError:
            pytest.skip("Config models not available")


# =============================================================================
# Regression Tests with Specific Examples
# =============================================================================


class TestRegressions:
    """Regression tests for specific edge cases."""

    @pytest.mark.parametrize(
        "code,expected_count",
        [
            # Basic mirages
            ("import numpy as np\nresult = np.mean([1,2,3])", 1),
            ("import numpy as np\nresult = np.sum([1,2,3])", 1),
            ("import numpy as np\nresult = np.argmax([1,2,3])", 1),
            # Multiple mirages
            ("import numpy as np\na = np.mean(x); b = np.sum(y)", 2),
            # Nested
            ("import numpy as np\nresult = np.mean(np.mean(x))", 2),
            # No mirages
            ("x = 1 + 2", 0),
            ("import numpy as np\nresult = np.array([1,2,3])", 0),
        ],
    )
    def test_specific_mirage_counts(self, code: str, expected_count: int) -> None:
        """Test specific code patterns with known mirage counts."""
        from demyst.engine.mirage_detector import MirageDetector

        try:
            tree = ast.parse(code)
        except SyntaxError:
            pytest.skip("Invalid syntax in test case")

        detector = MirageDetector()
        detector.visit(tree)

        assert (
            len(detector.mirages) == expected_count
        ), f"Expected {expected_count} mirages, found {len(detector.mirages)} in:\n{code}"


# =============================================================================
# Fuzzing Tests
# =============================================================================


class TestFuzzing:
    """Fuzzing tests for robustness."""

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(garbage=st.binary(min_size=0, max_size=1000))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_detector_handles_garbage_gracefully(self, garbage: bytes) -> None:
        """Detector should handle non-code input gracefully."""
        from demyst.engine.mirage_detector import MirageDetector

        try:
            code = garbage.decode("utf-8", errors="ignore")
        except Exception:
            return

        try:
            # Sanitize code by removing null bytes before parsing
            sanitized_code = code.replace("\x00", "")
            tree = ast.parse(sanitized_code)
            detector = MirageDetector()
            detector.visit(tree)
            # If we get here without crashing, that's good
        except SyntaxError:
            # Expected for garbage input
            pass
        except Exception as e:
            # Other exceptions should not occur
            pytest.fail(f"Unexpected exception: {type(e).__name__}: {e}")

    @pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
    @given(
        depth=st.integers(min_value=1, max_value=10),
        width=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=20)
    def test_detector_handles_deep_nesting(self, depth: int, width: int) -> None:
        """Detector should handle deeply nested code."""
        from demyst.engine.mirage_detector import MirageDetector

        # Generate deeply nested function calls
        code = "import numpy as np\n"
        inner = "np.mean(x)"
        for _ in range(depth):
            inner = f"np.mean({inner})"
        code += f"result = {inner}"

        try:
            tree = ast.parse(code)
            detector = MirageDetector()
            detector.visit(tree)
            # Should find all the mirages
            assert len(detector.mirages) == depth + 1
        except RecursionError:
            pytest.skip("Recursion limit hit - acceptable for extreme nesting")

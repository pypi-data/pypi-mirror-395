"""
Edge Case Test Suite for Demyst

Tests for handling edge cases:
    - Empty files
    - Syntax errors
    - Unicode content
    - Large files
    - Malformed input
    - Encoding issues
"""

import os
import tempfile
from pathlib import Path

import pytest


class TestEmptyFiles:
    """Tests for handling empty files."""

    def test_empty_file_tensor_guard(self):
        """TensorGuard should handle empty files gracefully."""
        from demyst.guards.tensor_guard import TensorGuard

        guard = TensorGuard()
        result = guard.analyze("")

        assert result is not None
        assert "error" not in result or result["error"] is None
        assert result.get("gradient_issues", []) == []
        assert result.get("normalization_issues", []) == []
        assert result.get("reward_issues", []) == []

    def test_empty_file_leakage_hunter(self):
        """LeakageHunter should handle empty files gracefully."""
        from demyst.guards.leakage_hunter import LeakageHunter

        hunter = LeakageHunter()
        result = hunter.analyze("")

        assert result is not None
        assert "error" not in result or result["error"] is None
        assert result.get("violations", []) == []

    def test_empty_file_hypothesis_guard(self):
        """HypothesisGuard should handle empty files gracefully."""
        from demyst.guards.hypothesis_guard import HypothesisGuard

        guard = HypothesisGuard()
        result = guard.analyze_code("")

        assert result is not None
        assert "error" not in result or result["error"] is None
        assert result.get("violations", []) == []

    def test_empty_file_unit_guard(self):
        """UnitGuard should handle empty files gracefully."""
        from demyst.guards.unit_guard import UnitGuard

        guard = UnitGuard()
        result = guard.analyze("")

        assert result is not None
        assert "error" not in result or result["error"] is None
        assert result.get("violations", []) == []

    def test_whitespace_only_file(self):
        """All guards should handle whitespace-only files."""
        from demyst.guards.hypothesis_guard import HypothesisGuard
        from demyst.guards.leakage_hunter import LeakageHunter
        from demyst.guards.tensor_guard import TensorGuard
        from demyst.guards.unit_guard import UnitGuard

        whitespace_code = "   \n\t\n   \n"

        # All guards should handle whitespace-only code
        for guard, method in [
            (TensorGuard(), "analyze"),
            (LeakageHunter(), "analyze"),
            (HypothesisGuard(), "analyze_code"),
            (UnitGuard(), "analyze"),
        ]:
            result = getattr(guard, method)(whitespace_code)
            assert result is not None
            assert "error" not in result or result["error"] is None


class TestSyntaxErrors:
    """Tests for handling syntax errors."""

    def test_syntax_error_tensor_guard(self):
        """TensorGuard should handle syntax errors gracefully."""
        from demyst.guards.tensor_guard import TensorGuard

        bad_code = "def broken( x y z:\n    return"

        guard = TensorGuard()
        result = guard.analyze(bad_code)

        assert result is not None
        assert "error" in result
        assert "syntax" in result["error"].lower() or "Syntax" in result["error"]

    def test_syntax_error_leakage_hunter(self):
        """LeakageHunter should handle syntax errors gracefully."""
        from demyst.guards.leakage_hunter import LeakageHunter

        bad_code = "if True\n    print('missing colon')"

        hunter = LeakageHunter()
        result = hunter.analyze(bad_code)

        assert result is not None
        assert "error" in result

    def test_syntax_error_hypothesis_guard(self):
        """HypothesisGuard should handle syntax errors gracefully."""
        from demyst.guards.hypothesis_guard import HypothesisGuard

        bad_code = "class {\n}"

        guard = HypothesisGuard()
        result = guard.analyze_code(bad_code)

        assert result is not None
        assert "error" in result

    def test_syntax_error_unit_guard(self):
        """UnitGuard should handle syntax errors gracefully."""
        from demyst.guards.unit_guard import UnitGuard

        bad_code = "def f( return 1"

        guard = UnitGuard()
        result = guard.analyze(bad_code)

        assert result is not None
        assert "error" in result

    def test_incomplete_code(self):
        """Guards should handle incomplete code."""
        from demyst.guards.tensor_guard import TensorGuard

        incomplete = "def incomplete_function():"

        guard = TensorGuard()
        # This is actually valid Python (empty function body with implicit pass)
        result = guard.analyze(incomplete)
        # Should either parse successfully or report a sensible error
        assert result is not None


class TestUnicodeContent:
    """Tests for handling Unicode content."""

    def test_unicode_variable_names(self):
        """Guards should handle Unicode variable names."""
        from demyst.guards.tensor_guard import TensorGuard
        from demyst.guards.unit_guard import UnitGuard

        unicode_code = '''
def calculate_温度(入力_data):
    """Calculate temperature from input data."""
    результат = np.mean(入力_data)
    return результат

def calcul_vélocité(données):
    """French function name."""
    return données * 2
'''

        tensor_guard = TensorGuard()
        result = tensor_guard.analyze(unicode_code)
        assert result is not None
        assert "error" not in result or result["error"] is None

        unit_guard = UnitGuard()
        result = unit_guard.analyze(unicode_code)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_unicode_strings(self):
        """Guards should handle Unicode strings in code."""
        from demyst.guards.leakage_hunter import LeakageHunter

        unicode_code = """
message = "日本語テキスト 中文 한국어"
description = "Ñoño español café"
symbols = "∑∏∫∂∇"
"""

        hunter = LeakageHunter()
        result = hunter.analyze(unicode_code)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_unicode_comments(self):
        """Guards should handle Unicode comments."""
        from demyst.guards.hypothesis_guard import HypothesisGuard

        unicode_code = """
# 这是一个注释
# Комментарий на русском
# コメント

def function():
    # إضافة عربية
    pass
"""

        guard = HypothesisGuard()
        result = guard.analyze_code(unicode_code)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_emoji_in_strings(self):
        """Guards should handle emoji in strings."""
        from demyst.guards.tensor_guard import TensorGuard

        emoji_code = """
status = "✅ Success"
warning = "⚠️ Warning"
error = "❌ Error"
"""

        guard = TensorGuard()
        result = guard.analyze(emoji_code)
        assert result is not None
        assert "error" not in result or result["error"] is None


class TestLargeFiles:
    """Tests for handling large files."""

    def test_large_function_count(self):
        """Guards should handle files with many functions."""
        from demyst.guards.tensor_guard import TensorGuard

        # Generate code with 100 functions
        functions = "\n".join([f"def function_{i}(x):\n    return x + {i}\n" for i in range(100)])

        guard = TensorGuard()
        result = guard.analyze(functions)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_deeply_nested_code(self):
        """Guards should handle deeply nested code."""
        from demyst.guards.hypothesis_guard import HypothesisGuard

        # Generate deeply nested code (10 levels)
        nested = "x = 1\n"
        for i in range(10):
            indent = "    " * (i + 1)
            nested += f"{'    ' * i}if True:\n"
            nested += f"{indent}x = x + 1\n"

        guard = HypothesisGuard()
        result = guard.analyze_code(nested)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_long_lines(self):
        """Guards should handle very long lines."""
        from demyst.guards.unit_guard import UnitGuard

        # Use a moderate number to avoid Python's recursion limit in AST unparsing
        long_line = f"x = " + " + ".join(["1"] * 50)

        guard = UnitGuard()
        result = guard.analyze(long_line)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_many_imports(self):
        """Guards should handle files with many imports."""
        from demyst.guards.leakage_hunter import LeakageHunter

        imports = "\n".join([f"import module_{i}" for i in range(50)])

        hunter = LeakageHunter()
        result = hunter.analyze(imports)
        assert result is not None
        assert "error" not in result or result["error"] is None


class TestMalformedInput:
    """Tests for handling malformed input."""

    def test_binary_content(self):
        """Guards should handle accidental binary content."""
        from demyst.guards.tensor_guard import TensorGuard

        # This should fail to parse but not crash
        binary_like = "\x00\x01\x02\x03"

        guard = TensorGuard()
        result = guard.analyze(binary_like)
        assert result is not None
        # Should either report error or empty results
        assert "error" in result or result.get("gradient_issues", []) == []

    def test_null_characters(self):
        """Guards should handle null characters in code."""
        from demyst.guards.leakage_hunter import LeakageHunter

        code_with_nulls = "x = 1\x00\ny = 2"

        hunter = LeakageHunter()
        # Should handle gracefully
        try:
            result = hunter.analyze(code_with_nulls)
            assert result is not None
        except Exception:
            # It's acceptable to raise an exception for truly malformed input
            pass

    def test_mixed_line_endings(self):
        """Guards should handle mixed line endings."""
        from demyst.guards.hypothesis_guard import HypothesisGuard

        mixed_endings = "x = 1\r\ny = 2\rz = 3\n"

        guard = HypothesisGuard()
        result = guard.analyze_code(mixed_endings)
        assert result is not None
        assert "error" not in result or result["error"] is None


class TestCommentOnlyFiles:
    """Tests for handling comment-only files."""

    def test_comment_only_file(self):
        """Guards should handle files with only comments."""
        from demyst.guards.leakage_hunter import LeakageHunter
        from demyst.guards.tensor_guard import TensorGuard

        comment_only = '''
# This file contains only comments
# No actual code here
# Just documentation

"""
Docstring without any code
"""

# More comments
'''

        tensor_guard = TensorGuard()
        result = tensor_guard.analyze(comment_only)
        assert result is not None
        assert result.get("gradient_issues", []) == []

        hunter = LeakageHunter()
        result = hunter.analyze(comment_only)
        assert result is not None
        assert result.get("violations", []) == []


class TestSpecialPythonConstructs:
    """Tests for handling special Python constructs."""

    def test_async_functions(self):
        """Guards should handle async functions."""
        from demyst.guards.tensor_guard import TensorGuard

        async_code = """
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return [1, 2, 3]

async def process():
    data = await fetch_data()
    return sum(data)
"""

        guard = TensorGuard()
        result = guard.analyze(async_code)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_decorators(self):
        """Guards should handle decorators."""
        from demyst.guards.hypothesis_guard import HypothesisGuard

        decorated_code = """
@staticmethod
@classmethod
@property
@decorator_with_args(1, 2, 3)
def decorated_function(self):
    pass

@contextmanager
def context():
    yield
"""

        guard = HypothesisGuard()
        result = guard.analyze_code(decorated_code)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_type_hints(self):
        """Guards should handle type hints."""
        from demyst.guards.unit_guard import UnitGuard

        typed_code = """
from typing import List, Dict, Optional, Union

def typed_function(x: int, y: List[float]) -> Dict[str, Union[int, str]]:
    result: Dict[str, Union[int, str]] = {}
    value: Optional[int] = None
    return result
"""

        guard = UnitGuard()
        result = guard.analyze(typed_code)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_walrus_operator(self):
        """Guards should handle walrus operator (Python 3.8+)."""
        from demyst.guards.leakage_hunter import LeakageHunter

        walrus_code = """
if (n := len(data)) > 10:
    print(f"Large data: {n}")

while (line := file.readline()):
    process(line)
"""

        hunter = LeakageHunter()
        result = hunter.analyze(walrus_code)
        assert result is not None
        assert "error" not in result or result["error"] is None

    def test_match_statement(self):
        """Guards should handle match statement (Python 3.10+)."""
        import sys

        from demyst.guards.tensor_guard import TensorGuard

        if sys.version_info >= (3, 10):
            match_code = """
def process(command):
    match command:
        case "start":
            return 1
        case "stop":
            return 0
        case _:
            return -1
"""
            guard = TensorGuard()
            result = guard.analyze(match_code)
            assert result is not None


class TestCLIEdgeCases:
    """Tests for CLI edge cases."""

    def test_nonexistent_file(self):
        """CLI should handle nonexistent files gracefully."""
        import pytest

        from demyst.cli import safe_read_file

        with pytest.raises(FileNotFoundError):
            safe_read_file("/nonexistent/path/to/file.py")

    def test_directory_instead_of_file(self):
        """CLI should handle directories when file is expected."""
        import pytest

        from demyst.cli import safe_read_file

        with pytest.raises(IsADirectoryError):
            safe_read_file("/tmp")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

#!/usr/bin/env python3
"""
PIPRE Transpiler - Automatically refactors scientific code to preserve physical information

This module provides the main Transpiler class that orchestrates code transformations
to replace variance-destroying operations with VariationTensor equivalents.

The transpiler now uses LibCST for safe, syntax-preserving transformations. The original
AST-based approach is preserved as a fallback.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import os
import sys
from typing import Any, Dict, List, Optional, Union

from demyst.exceptions import (
    DemystError,
    FileReadError,
    ParseError,
    TransformationError,
    TranspilerError,
)

# Try to import LibCST-based transformer, fall back to AST if not available
try:
    from demyst.engine.cst_transformer import CSTTranspiler, TransformationRecord
    from demyst.engine.cst_transformer import detect_mirages as cst_detect_mirages

    CST_AVAILABLE = True
except ImportError:
    CST_AVAILABLE = False

# Import AST-based components (fallback)
from demyst.engine.mirage_detector import MirageDetector
from demyst.engine.variation_tensor import VariationTensor
from demyst.engine.variation_transformer import VariationTransformer


class Transpiler:
    """
    Main transpiler class that orchestrates the transformation process.

    This class provides a unified interface for code transformation, using
    LibCST when available for safe CST-based transformations, and falling
    back to AST-based transformations when LibCST is not installed.

    Attributes:
        transformations: List of transformation records
        use_cst: Whether to use CST-based transformations (default: True if available)
    """

    def __init__(self, use_cst: bool = True) -> None:
        """
        Initialize the transpiler.

        Args:
            use_cst: Whether to prefer CST-based transformations (requires libcst)
        """
        self.use_cst = use_cst and CST_AVAILABLE
        self.transformations: List[Dict[str, Any]] = []
        self._detector = MirageDetector()
        self._cst_transpiler: Optional["CSTTranspiler"] = None

        if self.use_cst:
            self._cst_transpiler = CSTTranspiler()

    @property
    def backend(self) -> str:
        """Return the transformation backend being used."""
        return "libcst" if self.use_cst else "ast"

    def transpile_file(self, file_path: str, target_line: Optional[int] = None) -> str:
        """
        Transpile a Python file to preserve physical information.

        Args:
            file_path: Path to the Python file
            target_line: Optional specific line to target

        Returns:
            Transformed source code

        Raises:
            FileReadError: If the file cannot be read
            ParseError: If the file contains invalid Python syntax
            TranspilerError: If transformation fails
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    source = f.read()
            except Exception as e:
                raise FileReadError(file_path, "Encoding error", e)
        except FileNotFoundError:
            raise FileReadError(file_path, "File not found")
        except PermissionError:
            raise FileReadError(file_path, "Permission denied")
        except Exception as e:
            raise FileReadError(file_path, str(e), e)

        return self.transpile_source(source, target_line, file_path=file_path)

    def transpile_source(
        self, source: str, target_line: Optional[int] = None, file_path: Optional[str] = None
    ) -> str:
        """
        Transpile Python source code to preserve physical information.

        Args:
            source: Python source code
            target_line: Optional specific line to target
            file_path: Optional file path for error reporting

        Returns:
            Transformed source code

        Raises:
            ParseError: If the source contains invalid Python syntax
            TranspilerError: If transformation fails
        """
        self.transformations = []

        # Use CST-based transformation if available
        if self.use_cst and self._cst_transpiler is not None:
            return self._transpile_with_cst(source, target_line, file_path)

        # Fall back to AST-based transformation
        return self._transpile_with_ast(source, target_line, file_path)

    def _transpile_with_cst(
        self, source: str, target_line: Optional[int], file_path: Optional[str]
    ) -> str:
        """Perform CST-based transformation."""
        assert self._cst_transpiler is not None

        try:
            transformed = self._cst_transpiler.transpile_source(source, target_line)
            # Convert CST transformation records to legacy format
            self.transformations = [
                {
                    "type": t.type.name.lower().replace("_to_variation", ""),
                    "line": t.line,
                    "function": t.function_context,
                    "transformation": t.description,
                }
                for t in self._cst_transpiler.transformations
            ]
            return transformed
        except DemystError:
            raise
        except Exception as e:
            raise TranspilerError(
                f"CST transformation failed: {e}", file_path=file_path, details={"error": str(e)}
            )

    def _transpile_with_ast(
        self, source: str, target_line: Optional[int], file_path: Optional[str]
    ) -> str:
        """Perform AST-based transformation (fallback)."""
        # Parse AST
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            raise ParseError(
                f"Invalid Python syntax: {e.msg}",
                file_path=file_path,
                line_number=e.lineno,
                column=e.offset,
                original_error=e,
            )

        # Detect mirages
        self._detector = MirageDetector()
        self._detector.visit(tree)

        # Filter by target line if specified
        mirages = self._detector.mirages
        if target_line is not None:
            mirages = [m for m in mirages if m["line"] == target_line]

        if not mirages:
            print(
                f"No destructive operations found{' at line ' + str(target_line) if target_line else ''}"
            )
            return source

        # Transform AST
        try:
            transformer = VariationTransformer(mirages)
            new_tree = transformer.visit(tree)

            # Fix line numbers and column offsets
            ast.fix_missing_locations(new_tree)

            # Generate new source
            new_source = ast.unparse(new_tree)
        except Exception as e:
            raise TranspilerError(
                f"AST transformation failed: {e}", file_path=file_path, details={"error": str(e)}
            )

        # Store transformation info
        self.transformations = [
            {
                "type": m["type"],
                "line": m["line"],
                "function": m["function"],
                "transformation": f"{m['type']} -> VariationTensor",
            }
            for m in mirages
        ]

        return new_source

    def get_diff(self, original: str, transformed: str) -> str:
        """
        Generate unified diff between original and transformed code.

        Args:
            original: Original source code
            transformed: Transformed source code

        Returns:
            Unified diff string
        """
        if self.use_cst and self._cst_transpiler is not None:
            return self._cst_transpiler.get_diff(original, transformed)

        original_lines = original.splitlines(keepends=True)
        transformed_lines = transformed.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            transformed_lines,
            fromfile="original",
            tofile="transformed",
            lineterm="",
        )

        return "".join(diff)

    def get_summary(self) -> str:
        """Get a summary of transformations performed."""
        if not self.transformations:
            return "No transformations performed"

        lines = [f"\n=== Demyst Transpiler Summary ({self.backend}) ==="]
        for t in self.transformations:
            func = t.get("function") or "module level"
            lines.append(f"Line {t['line']} in {func}: {t['transformation']}")
        lines.append(f"Total transformations: {len(self.transformations)}")
        return "\n".join(lines)

    def print_summary(self) -> None:
        """Print summary of transformations."""
        print(self.get_summary())


def main() -> int:
    """Command-line interface for the transpiler."""
    parser = argparse.ArgumentParser(
        description="PIPRE Transpiler - Preserve physical information in scientific code"
    )
    parser.add_argument("--target", required=True, help="Target file or file:line specification")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--diff", action="store_true", help="Show unified diff")
    parser.add_argument(
        "--backend",
        choices=["cst", "ast", "auto"],
        default="auto",
        help="Transformation backend to use",
    )

    args = parser.parse_args()

    # Parse target specification
    if ":" in args.target:
        file_path, line_str = args.target.rsplit(":", 1)
        try:
            target_line: Optional[int] = int(line_str)
        except ValueError:
            print(f"Invalid line number: {line_str}")
            return 1
    else:
        file_path = args.target
        target_line = None

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return 1

    # Configure backend
    use_cst = True
    if args.backend == "ast":
        use_cst = False
    elif args.backend == "cst" and not CST_AVAILABLE:
        print("Warning: LibCST not available, falling back to AST backend")
        use_cst = False

    # Run transpiler
    transpiler = Transpiler(use_cst=use_cst)

    try:
        with open(file_path, "r") as f:
            original_source = f.read()

        transformed_source = transpiler.transpile_file(file_path, target_line)

        if args.diff:
            diff = transpiler.get_diff(original_source, transformed_source)
            print(diff)
        else:
            if args.output:
                with open(args.output, "w") as f:
                    f.write(transformed_source)
                print(f"Transformed source written to {args.output}")
            else:
                print(transformed_source)

        transpiler.print_summary()
        return 0

    except DemystError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Transpilation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

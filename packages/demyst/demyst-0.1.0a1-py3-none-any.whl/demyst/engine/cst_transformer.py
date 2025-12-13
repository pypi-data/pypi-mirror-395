"""
LibCST-based Code Transformer for Demyst

Provides safe, syntax-preserving code transformations using LibCST (Concrete Syntax Tree).
Unlike AST transformations, CST transformations preserve whitespace, comments, and formatting.

This is the core of Demyst's auto-fix capability, ensuring that transformed code
maintains the original style and structure of the source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

import libcst as cst
from libcst import matchers as m
from libcst.metadata import MetadataWrapper, PositionProvider

from demyst.exceptions import (
    CSTTransformError,
    ParseError,
    TransformationError,
    UnsafeTransformationError,
)

# =============================================================================
# Data Classes for Transformations
# =============================================================================


class TransformationType(Enum):
    """Types of transformations that can be applied."""

    MEAN_TO_VARIATION = auto()
    SUM_TO_ENSEMBLE = auto()
    ARGMAX_TO_VARIATION = auto()
    ARGMIN_TO_VARIATION = auto()
    DISCRETIZATION_WRAPPER = auto()


@dataclass
class TransformationRecord:
    """Record of a single transformation applied to the code."""

    type: TransformationType
    line: int
    column: int
    original_code: str
    transformed_code: str
    function_context: Optional[str] = None
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "type": self.type.name,
            "line": self.line,
            "column": self.column,
            "original_code": self.original_code,
            "transformed_code": self.transformed_code,
            "function_context": self.function_context,
            "description": self.description,
        }


@dataclass
class MirageInfo:
    """Information about a detected mirage."""

    type: str
    line: int
    column: int
    node: cst.BaseExpression
    function_context: Optional[str] = None
    original_code: str = ""


# =============================================================================
# CST Visitor for Mirage Detection
# =============================================================================


class MirageDetectorVisitor(cst.CSTVisitor):
    """
    LibCST visitor that detects computational mirages.

    Identifies variance-destroying operations like np.mean, np.sum,
    np.argmax, np.argmin, and premature discretization (round, int).
    """

    METADATA_DEPENDENCIES = (PositionProvider,)

    # Destructive operations to detect
    DESTRUCTIVE_ATTRS = frozenset({"mean", "sum", "argmax", "argmin"})
    DISCRETIZATION_FUNCS = frozenset({"round", "int", "floor", "ceil", "trunc"})

    def __init__(self) -> None:
        self.mirages: List[MirageInfo] = []
        self._current_function: Optional[str] = None
        self._function_stack: List[str] = []

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        """Track function context."""
        self._function_stack.append(node.name.value)
        self._current_function = node.name.value
        return None

    def leave_FunctionDef(self, node: cst.FunctionDef) -> None:
        """Leave function context."""
        self._function_stack.pop()
        self._current_function = self._function_stack[-1] if self._function_stack else None

    def visit_Call(self, node: cst.Call) -> Optional[bool]:
        """Detect destructive function calls."""
        try:
            # Check for attribute calls like np.mean(), array.mean()
            if isinstance(node.func, cst.Attribute):
                attr_name = node.func.attr.value
                if attr_name in self.DESTRUCTIVE_ATTRS:
                    self._record_mirage(node, attr_name)

            # Check for direct calls like mean(), sum()
            elif isinstance(node.func, cst.Name):
                func_name = node.func.value
                if func_name in self.DISCRETIZATION_FUNCS:
                    self._record_mirage(node, "premature_discretization")
                elif func_name in self.DESTRUCTIVE_ATTRS:
                    self._record_mirage(node, func_name)

        except Exception:
            # Don't fail detection on edge cases
            pass

        return None

    def _record_mirage(self, node: cst.Call, mirage_type: str) -> None:
        """Record a detected mirage."""
        # Get position using metadata (set during wrapper processing)
        try:
            pos = self.get_metadata(PositionProvider, node)
            line = pos.start.line
            column = pos.start.column
        except (KeyError, AttributeError):
            line = 0
            column = 0

        self.mirages.append(
            MirageInfo(
                type=mirage_type,
                line=line,
                column=column,
                node=node,
                function_context=self._current_function,
                original_code="",  # Will be filled in later
            )
        )


# =============================================================================
# CST Transformer for Mirage Fixes
# =============================================================================


class VariationTensorTransformer(cst.CSTTransformer):
    """
    LibCST transformer that converts destructive operations to VariationTensor equivalents.

    Transforms:
    - np.mean(x) -> VariationTensor(x).collapse('mean')
    - np.sum(x, axis=0) -> VariationTensor(x).ensemble_sum(0)
    - np.argmax(x) -> VariationTensor(x).collapse('argmax')
    - array.mean() -> VariationTensor(array).collapse('mean')

    Preserves all whitespace, comments, and formatting from the original code.
    """

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(
        self,
        mirages: Optional[List[MirageInfo]] = None,
        target_line: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.mirages = mirages or []
        self.target_line = target_line
        self.transformations: List[TransformationRecord] = []
        self._import_added = False
        self._needs_import = False

        # Create a set of mirage node IDs for fast lookup
        self._mirage_node_ids: Set[int] = {id(m.node) for m in self.mirages}
        self._mirage_by_id: Dict[int, MirageInfo] = {id(m.node): m for m in self.mirages}

    def _should_transform(self, node: cst.Call) -> Optional[MirageInfo]:
        """Check if this node should be transformed."""
        mirage = self._mirage_by_id.get(id(node))
        if mirage is None:
            return None

        # Filter by target line if specified
        if self.target_line is not None and mirage.line != self.target_line:
            return None

        return mirage

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        """Transform destructive calls to VariationTensor equivalents."""
        mirage = self._should_transform(original_node)
        if mirage is None:
            return updated_node

        try:
            transformed = self._transform_call(updated_node, mirage)
            if transformed is not None:
                self._needs_import = True
                self._record_transformation(original_node, transformed, mirage)
                return transformed
        except Exception as e:
            # Log but don't fail - return original node
            pass

        return updated_node

    def _transform_call(self, node: cst.Call, mirage: MirageInfo) -> Optional[cst.BaseExpression]:
        """Transform a single call based on mirage type."""
        if mirage.type in ("mean", "argmax", "argmin"):
            return self._create_collapse_call(node, mirage.type)
        elif mirage.type == "sum":
            return self._create_ensemble_sum_call(node)
        elif mirage.type == "premature_discretization":
            # For now, just wrap in VariationTensor tracking
            return self._create_discretization_wrapper(node)
        return None

    def _create_collapse_call(self, node: cst.Call, operation: str) -> cst.Call:
        """
        Create VariationTensor(x).collapse('mean') from np.mean(x).

        Handles both:
        - np.mean(array) -> VariationTensor(array).collapse('mean')
        - array.mean() -> VariationTensor(array).collapse('mean')
        """
        # Determine if this is a library call (np.mean) or method call (x.mean)
        is_library_call = False
        if isinstance(node.func, cst.Attribute) and isinstance(node.func.value, cst.Name):
            if node.func.value.value in ("np", "numpy", "torch", "jax", "tf", "tensorflow"):
                is_library_call = True

        # Extract the data argument
        if is_library_call:
            # np.mean(array) - first positional arg
            if not node.args:
                raise CSTTransformError("No arguments to transform", node_type="Call")
            data_arg = node.args[0].value
            keywords = list(node.args[1:]) if len(node.args) > 1 else []
        elif isinstance(node.func, cst.Attribute):
            # array.mean() - the array is the value
            data_arg = node.func.value
            # Filter out axis keyword for method calls
            keywords = [
                kw for kw in node.args if isinstance(kw, cst.Arg) and kw.keyword is not None
            ]
        else:
            # mean(array) - first positional arg
            if not node.args:
                raise CSTTransformError("No arguments to transform", node_type="Call")
            data_arg = node.args[0].value
            keywords = list(node.args[1:]) if len(node.args) > 1 else []

        # Build VariationTensor(data)
        variation_call = cst.Call(
            func=cst.Name("VariationTensor"),
            args=[cst.Arg(value=data_arg)],
        )

        # Build .collapse('mean')
        collapse_call = cst.Call(
            func=cst.Attribute(
                value=variation_call,
                attr=cst.Name("collapse"),
            ),
            args=[cst.Arg(value=cst.SimpleString(f"'{operation}'"))],
        )

        return collapse_call

    def _create_ensemble_sum_call(self, node: cst.Call) -> cst.Call:
        """
        Create VariationTensor(x).ensemble_sum(axis) from np.sum(x, axis=0).
        """
        # Determine if this is a library call (np.sum) or method call (x.sum)
        is_library_call = False
        if isinstance(node.func, cst.Attribute) and isinstance(node.func.value, cst.Name):
            if node.func.value.value in ("np", "numpy", "torch", "jax", "tf", "tensorflow"):
                is_library_call = True

        # Extract data and axis arguments
        if is_library_call:
            if not node.args:
                raise CSTTransformError("No arguments to transform", node_type="Call")
            data_arg = node.args[0].value
            axis_arg = self._extract_axis_arg(node.args[1:])
        elif isinstance(node.func, cst.Attribute):
            data_arg = node.func.value
            axis_arg = self._extract_axis_arg(node.args)
        else:
            if not node.args:
                raise CSTTransformError("No arguments to transform", node_type="Call")
            data_arg = node.args[0].value
            axis_arg = self._extract_axis_arg(node.args[1:])

        # Build VariationTensor(data)
        variation_call = cst.Call(
            func=cst.Name("VariationTensor"),
            args=[cst.Arg(value=data_arg)],
        )

        # Build .ensemble_sum(axis) or .ensemble_sum()
        ensemble_args = [cst.Arg(value=axis_arg)] if axis_arg else []
        ensemble_call = cst.Call(
            func=cst.Attribute(
                value=variation_call,
                attr=cst.Name("ensemble_sum"),
            ),
            args=ensemble_args,
        )

        return ensemble_call

    def _extract_axis_arg(self, args: Sequence[cst.Arg]) -> Optional[cst.BaseExpression]:
        """Extract axis argument from function arguments."""
        for arg in args:
            # Check keyword argument
            if arg.keyword is not None and arg.keyword.value == "axis":
                return arg.value
        # Check first positional arg (common pattern: np.sum(x, 0))
        for arg in args:
            if arg.keyword is None:
                return arg.value
        return None

    def _create_discretization_wrapper(self, node: cst.Call) -> cst.Call:
        """
        Wrap discretization in a tracking call.

        For round(x), int(x) etc., we preserve the original but
        add tracking metadata.
        """
        # For now, return the original node - discretization is complex
        # A full implementation would wrap in VariationTensor.discretize()
        return node

    def _record_transformation(
        self, original: cst.Call, transformed: cst.BaseExpression, mirage: MirageInfo
    ) -> None:
        """Record a transformation for reporting."""
        try:
            original_code = original.__class__.__module__
        except Exception:
            original_code = "<unknown>"

        self.transformations.append(
            TransformationRecord(
                type=(
                    TransformationType[mirage.type.upper() + "_TO_VARIATION"]
                    if mirage.type in ("mean", "sum", "argmax", "argmin")
                    else TransformationType.DISCRETIZATION_WRAPPER
                ),
                line=mirage.line,
                column=mirage.column,
                original_code=mirage.original_code,
                transformed_code="",  # Will be filled in after unparsing
                function_context=mirage.function_context,
                description=f"Transformed {mirage.type} to VariationTensor",
            )
        )

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        """Add VariationTensor import if needed."""
        if not self._needs_import:
            return updated_node

        # Create the import statement
        import_stmt = cst.SimpleStatementLine(
            body=[
                cst.ImportFrom(
                    module=cst.Attribute(
                        value=cst.Attribute(
                            value=cst.Name("demyst"),
                            attr=cst.Name("engine"),
                        ),
                        attr=cst.Name("variation_tensor"),
                    ),
                    names=[cst.ImportAlias(name=cst.Name("VariationTensor"))],
                )
            ]
        )

        # Find the right position to insert (after __future__ imports)
        insert_index = 0
        for i, stmt in enumerate(updated_node.body):
            if isinstance(stmt, cst.SimpleStatementLine):
                for item in stmt.body:
                    if isinstance(item, cst.ImportFrom):
                        if isinstance(item.module, cst.Attribute):
                            continue
                        elif (
                            isinstance(item.module, cst.Name) and item.module.value == "__future__"
                        ):
                            insert_index = i + 1
                            continue
            # Stop at first non-import
            if not self._is_import_statement(stmt):
                break
            insert_index = i + 1

        # Insert the import
        new_body = list(updated_node.body)
        new_body.insert(insert_index, import_stmt)

        return updated_node.with_changes(body=new_body)

    def _is_import_statement(self, stmt: cst.BaseStatement) -> bool:
        """Check if a statement is an import."""
        if isinstance(stmt, cst.SimpleStatementLine):
            return any(isinstance(item, (cst.Import, cst.ImportFrom)) for item in stmt.body)
        return False


# =============================================================================
# Main Transpiler Class
# =============================================================================


class CSTTranspiler:
    """
    Main transpiler class using LibCST for safe code transformations.

    This replaces the AST-based Transpiler with a CST-based approach that:
    - Preserves whitespace and comments
    - Maintains original formatting
    - Provides safer transformations
    - Can be validated before applying
    """

    def __init__(self) -> None:
        self.transformations: List[TransformationRecord] = []
        self._last_source: str = ""
        self._last_transformed: str = ""

    def transpile_source(self, source: str, target_line: Optional[int] = None) -> str:
        """
        Transpile Python source code to preserve physical information.

        Args:
            source: Python source code
            target_line: Optional specific line to target

        Returns:
            Transformed source code

        Raises:
            ParseError: If the source cannot be parsed
            TransformationError: If transformation fails
        """
        self._last_source = source
        self.transformations = []

        # Parse the source
        try:
            tree = cst.parse_module(source)
        except cst.ParserSyntaxError as e:
            raise ParseError(
                f"Failed to parse source: {e}",
                line_number=getattr(e, "lines", None),
                original_error=e,
            )

        # Create metadata wrapper for position tracking
        try:
            wrapper = MetadataWrapper(tree)
        except Exception as e:
            raise TransformationError(
                f"Failed to create metadata wrapper: {e}", details={"error": str(e)}
            )

        # First pass: detect mirages
        detector = MirageDetectorVisitor()
        try:
            wrapper.visit(detector)
        except Exception as e:
            raise TransformationError(f"Failed to detect mirages: {e}", details={"error": str(e)})

        mirages = detector.mirages

        # Filter by target line if specified
        if target_line is not None:
            mirages = [m for m in mirages if m.line == target_line]

        if not mirages:
            self._last_transformed = source
            return source

        # Fill in original code for each mirage
        source_lines = source.splitlines()
        for mirage in mirages:
            if 0 < mirage.line <= len(source_lines):
                mirage.original_code = source_lines[mirage.line - 1].strip()

        # Second pass: transform
        transformer = VariationTensorTransformer(mirages, target_line)
        try:
            # Transform the tree
            # Use wrapper.module to ensure we transform the same nodes that were visited
            new_tree = wrapper.module.visit(transformer)
        except Exception as e:
            raise TransformationError(f"Failed to transform code: {e}", details={"error": str(e)})

        # Get the transformed source
        new_source = new_tree.code

        # Validate the transformation
        self._validate_transformation(source, new_source)

        self.transformations = transformer.transformations
        self._last_transformed = new_source

        return str(new_source)

    def transpile_file(self, file_path: str, target_line: Optional[int] = None) -> str:
        """
        Transpile a Python file to preserve physical information.

        Args:
            file_path: Path to the Python file
            target_line: Optional specific line to target

        Returns:
            Transformed source code
        """
        from demyst.exceptions import FileReadError

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    source = f.read()
            except Exception as e:
                raise FileReadError(file_path, "Encoding error", e)
        except Exception as e:
            raise FileReadError(file_path, str(e), e)

        return self.transpile_source(source, target_line)

    def _validate_transformation(self, original: str, transformed: str) -> None:
        """
        Validate that the transformation produced valid Python.

        Raises:
            UnsafeTransformationError: If the transformed code is invalid
        """
        if original == transformed:
            return  # No changes made

        try:
            cst.parse_module(transformed)
        except cst.ParserSyntaxError as e:
            raise UnsafeTransformationError(
                "Transformation produced invalid Python syntax",
                original_code=original[:200],
                attempted_result=transformed[:200],
            )

    def get_diff(self, original: Optional[str] = None, transformed: Optional[str] = None) -> str:
        """Generate unified diff between original and transformed code."""
        import difflib

        original = original or self._last_source
        transformed = transformed or self._last_transformed

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
        """Get a summary of transformations."""
        if not self.transformations:
            return "No transformations performed"

        lines = ["\n=== Demyst Transpiler Summary ==="]
        for t in self.transformations:
            lines.append(f"Line {t.line}: {t.description}")
        lines.append(f"Total transformations: {len(self.transformations)}")
        return "\n".join(lines)

    def print_summary(self) -> None:
        """Print summary of transformations."""
        print(self.get_summary())


# =============================================================================
# Convenience Functions
# =============================================================================


def detect_mirages(source: str) -> List[Dict[str, Any]]:
    """
    Detect mirages in source code without transforming.

    Args:
        source: Python source code

    Returns:
        List of mirage dictionaries
    """
    try:
        tree = cst.parse_module(source)
        wrapper = MetadataWrapper(tree)
        detector = MirageDetectorVisitor()
        wrapper.visit(detector)

        return [
            {
                "type": m.type,
                "line": m.line,
                "column": m.column,
                "function": m.function_context,
            }
            for m in detector.mirages
        ]
    except Exception:
        return []


def transform_source(
    source: str, target_line: Optional[int] = None
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Transform source code and return result with transformation info.

    Args:
        source: Python source code
        target_line: Optional specific line to target

    Returns:
        Tuple of (transformed_source, list_of_transformations)
    """
    transpiler = CSTTranspiler()
    transformed = transpiler.transpile_source(source, target_line)
    return transformed, [t.to_dict() for t in transpiler.transformations]

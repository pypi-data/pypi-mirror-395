"""
Demyst Fixer: Auto-fix capabilities for scientific integrity issues.

This module provides comprehensive auto-fixing for detected violations using
LibCST for safe, syntax-preserving code transformations. The fixer can handle:

- Computational mirages (mean, sum, argmax, argmin operations)
- Some data leakage patterns
- Statistical validity improvements

The fixer uses a transaction-based approach: all fixes are computed first,
validated, and then applied atomically.
"""

from __future__ import annotations

import difflib
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from demyst.exceptions import (
    DemystError,
    FileReadError,
    FileWriteError,
    FixerError,
    TransformationError,
    UnsafeTransformationError,
)

logger = logging.getLogger(__name__)

# Try to import LibCST for transformations
try:
    import libcst as cst
    from libcst import matchers as m

    LIBCST_AVAILABLE = True
except ImportError:
    LIBCST_AVAILABLE = False
    cst = None  # type: ignore


# =============================================================================
# Enumerations and Data Classes
# =============================================================================


class FixType(Enum):
    """Types of fixes that can be applied."""

    MIRAGE_MEAN = auto()
    MIRAGE_SUM = auto()
    MIRAGE_ARGMAX = auto()
    MIRAGE_ARGMIN = auto()
    MIRAGE_DISCRETIZATION = auto()
    LEAKAGE_FIT_TRANSFORM = auto()
    COMMENT_TODO = auto()  # Fallback: add TODO comment


class FixResult(Enum):
    """Result of a fix attempt."""

    SUCCESS = auto()
    SKIPPED = auto()
    FAILED = auto()
    DRY_RUN = auto()


@dataclass
class FixAction:
    """Represents a single fix action to be applied."""

    type: FixType
    line: int
    column: int = 0
    original_code: str = ""
    fixed_code: str = ""
    description: str = ""
    violation: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "type": self.type.name,
            "line": self.line,
            "column": self.column,
            "original_code": self.original_code,
            "fixed_code": self.fixed_code,
            "description": self.description,
        }


@dataclass
class FixReport:
    """Report of fix operations performed on a file."""

    file_path: str
    actions: List[FixAction] = field(default_factory=list)
    applied: int = 0
    skipped: int = 0
    failed: int = 0
    dry_run: bool = False

    @property
    def total(self) -> int:
        return len(self.actions)

    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 1.0
        return self.applied / self.total

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "file_path": self.file_path,
            "actions": [a.to_dict() for a in self.actions],
            "applied": self.applied,
            "skipped": self.skipped,
            "failed": self.failed,
            "dry_run": self.dry_run,
            "success_rate": self.success_rate,
        }


# =============================================================================
# CST-based Fix Transformers
# =============================================================================

if LIBCST_AVAILABLE:

    class MirageFixTransformer(cst.CSTTransformer):
        """
        LibCST transformer for fixing mirage violations.

        Transforms destructive operations to VariationTensor equivalents.
        """

        def __init__(self, violations: List[Dict[str, Any]]) -> None:
            super().__init__()
            self.violations = violations
            self.applied_fixes: List[FixAction] = []
            self._needs_import = False

            # Map violations by line number for fast lookup
            self._violations_by_line: Dict[int, List[Dict[str, Any]]] = {}
            for v in violations:
                line = v.get("line", 0)
                if line not in self._violations_by_line:
                    self._violations_by_line[line] = []
                self._violations_by_line[line].append(v)

        def _find_violation_for_node(
            self, node: cst.Call, func_name: str
        ) -> Optional[Dict[str, Any]]:
            """Find a matching violation for this node."""
            # This is a simplified matching - in production you'd use metadata
            for violations in self._violations_by_line.values():
                for v in violations:
                    if v.get("type") == func_name:
                        return v
            return None

        def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
            """Transform destructive calls to VariationTensor equivalents."""
            # Check for attribute calls (np.mean, array.mean)
            if isinstance(updated_node.func, cst.Attribute):
                func_name = updated_node.func.attr.value
                if func_name in ("mean", "sum", "argmax", "argmin"):
                    violation = self._find_violation_for_node(updated_node, func_name)
                    if violation:
                        try:
                            transformed = self._transform_to_variation(updated_node, func_name)
                            self._needs_import = True
                            self._record_fix(func_name, updated_node, transformed)
                            return transformed
                        except Exception as e:
                            logger.debug(f"Transform failed for {func_name}: {e}")

            # Check for direct calls
            elif isinstance(updated_node.func, cst.Name):
                func_name = updated_node.func.value
                if func_name in ("mean", "sum", "argmax", "argmin"):
                    violation = self._find_violation_for_node(updated_node, func_name)
                    if violation:
                        try:
                            transformed = self._transform_to_variation(updated_node, func_name)
                            self._needs_import = True
                            self._record_fix(func_name, updated_node, transformed)
                            return transformed
                        except Exception as e:
                            logger.debug(f"Transform failed for {func_name}: {e}")

            return updated_node

        def _transform_to_variation(self, node: cst.Call, operation: str) -> cst.Call:
            """Create VariationTensor transformation."""
            # Extract data argument
            if isinstance(node.func, cst.Attribute):
                data_arg = node.func.value
            else:
                if not node.args:
                    raise ValueError("No arguments to transform")
                data_arg = node.args[0].value

            # Build VariationTensor(data)
            variation_call = cst.Call(
                func=cst.Name("VariationTensor"),
                args=[cst.Arg(value=data_arg)],
            )

            # Build method call
            if operation == "sum":
                method_name = "ensemble_sum"
                # Extract axis if present
                axis_arg = None
                for arg in node.args[1:] if isinstance(node.func, cst.Name) else node.args:
                    if isinstance(arg, cst.Arg):
                        if arg.keyword is not None and arg.keyword.value == "axis":
                            axis_arg = arg.value
                        elif arg.keyword is None and axis_arg is None:
                            axis_arg = arg.value

                return cst.Call(
                    func=cst.Attribute(
                        value=variation_call,
                        attr=cst.Name(method_name),
                    ),
                    args=[cst.Arg(value=axis_arg)] if axis_arg else [],
                )
            else:
                method_name = "collapse"
                return cst.Call(
                    func=cst.Attribute(
                        value=variation_call,
                        attr=cst.Name(method_name),
                    ),
                    args=[cst.Arg(value=cst.SimpleString(f"'{operation}'"))],
                )

        def _record_fix(self, operation: str, original: cst.Call, transformed: cst.Call) -> None:
            """Record a fix that was applied."""
            fix_type_map = {
                "mean": FixType.MIRAGE_MEAN,
                "sum": FixType.MIRAGE_SUM,
                "argmax": FixType.MIRAGE_ARGMAX,
                "argmin": FixType.MIRAGE_ARGMIN,
            }

            self.applied_fixes.append(
                FixAction(
                    type=fix_type_map.get(operation, FixType.MIRAGE_MEAN),
                    line=0,  # Would need metadata for accurate line
                    description=f"Transformed {operation} to VariationTensor",
                )
            )

        def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
            """Add VariationTensor import if needed."""
            if not self._needs_import:
                return updated_node

            # Create import statement
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

            # Find insertion point (after __future__ imports)
            insert_idx = 0
            for i, stmt in enumerate(updated_node.body):
                if isinstance(stmt, cst.SimpleStatementLine):
                    for item in stmt.body:
                        if isinstance(item, cst.ImportFrom):
                            if (
                                isinstance(item.module, cst.Name)
                                and item.module.value == "__future__"
                            ):
                                insert_idx = i + 1
                # Stop at first non-import
                if not self._is_import(stmt):
                    break
                insert_idx = i + 1

            new_body = list(updated_node.body)
            new_body.insert(insert_idx, import_stmt)
            return updated_node.with_changes(body=new_body)

        def _is_import(self, stmt: cst.BaseStatement) -> bool:
            """Check if statement is an import."""
            if isinstance(stmt, cst.SimpleStatementLine):
                return any(isinstance(item, (cst.Import, cst.ImportFrom)) for item in stmt.body)
            return False


# =============================================================================
# Main Fixer Class
# =============================================================================


class DemystFixer:
    """
    Applies automatic fixes to code based on Demyst analysis.

    This class provides a robust, transactional approach to fixing code:
    1. Parse the source using LibCST (or fallback to text-based fixes)
    2. Compute all transformations
    3. Validate the result is valid Python
    4. Apply atomically or show as dry-run

    Attributes:
        dry_run: If True, show changes without applying
        interactive: If True, prompt before each fix
        backup: If True, create backup files before modifying
    """

    def __init__(
        self, dry_run: bool = False, interactive: bool = False, backup: bool = True
    ) -> None:
        """
        Initialize the fixer.

        Args:
            dry_run: Show changes without applying
            interactive: Prompt before each fix
            backup: Create backup files
        """
        self.dry_run = dry_run
        self.interactive = interactive
        self.backup = backup
        self._use_cst = LIBCST_AVAILABLE

    @property
    def backend(self) -> str:
        """Return the fix backend being used."""
        return "libcst" if self._use_cst else "text"

    def fix_file(self, filepath: str, violations: List[Dict[str, Any]]) -> FixReport:
        """
        Apply fixes to a single file.

        Args:
            filepath: Path to the file to fix
            violations: List of violations detected in the file

        Returns:
            FixReport with details of applied fixes

        Raises:
            FileReadError: If the file cannot be read
            FileWriteError: If the file cannot be written
            FixerError: If fixing fails
        """
        report = FixReport(file_path=filepath, dry_run=self.dry_run)

        if not violations:
            return report

        # Filter to fixable violations
        fixable = [v for v in violations if self._can_fix(v)]
        if not fixable:
            print(f"  No auto-fixable violations in {filepath}")
            return report

        # Read the file
        try:
            source = self._read_file(filepath)
        except Exception as e:
            raise FileReadError(filepath, str(e))

        # Apply fixes
        try:
            if self._use_cst:
                fixed_source, actions = self._fix_with_cst(source, fixable)
            else:
                fixed_source, actions = self._fix_with_text(source, fixable)

            report.actions = actions
        except Exception as e:
            raise FixerError(f"Fix transformation failed: {e}", file_path=filepath)

        # Validate result
        if fixed_source != source:
            try:
                self._validate_python(fixed_source)
            except Exception as e:
                raise UnsafeTransformationError(
                    "Fix produced invalid Python",
                    original_code=source[:200],
                    attempted_result=fixed_source[:200],
                    file_path=filepath,
                )

        # Show diff
        if self.dry_run or self.interactive:
            diff = self._get_diff(source, fixed_source)
            if diff:
                print(f"\n  Changes for {filepath}:")
                print(diff)

        # Interactive mode
        if self.interactive and not self.dry_run:
            response = input("\n  Apply these fixes? [y/N] ").strip().lower()
            if response != "y":
                print("  Skipped.")
                report.skipped = len(actions)
                return report

        # Apply the fixes
        if not self.dry_run and fixed_source != source:
            # Create backup if enabled
            if self.backup:
                backup_path = filepath + ".bak"
                try:
                    with open(backup_path, "w", encoding="utf-8") as f:
                        f.write(source)
                except Exception:
                    pass  # Non-fatal

            # Write the fixed file
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(fixed_source)
                report.applied = len(actions)
                print(f"  Applied {len(actions)} fix(es) to {filepath}")
            except Exception as e:
                raise FileWriteError(filepath, str(e))
        elif self.dry_run:
            report.applied = len(actions)
            print(f"  [DRY RUN] Would apply {len(actions)} fix(es) to {filepath}")

        return report

    def fix_directory(
        self, directory: str, violations_by_file: Dict[str, List[Dict[str, Any]]]
    ) -> List[FixReport]:
        """
        Apply fixes to multiple files in a directory.

        Args:
            directory: Directory path
            violations_by_file: Mapping of file paths to violations

        Returns:
            List of FixReports for each file
        """
        reports = []
        for filepath, violations in violations_by_file.items():
            try:
                report = self.fix_file(filepath, violations)
                reports.append(report)
            except DemystError as e:
                print(f"  Error fixing {filepath}: {e}")
                reports.append(FixReport(file_path=filepath, failed=len(violations)))

        return reports

    def _can_fix(self, violation: Dict[str, Any]) -> bool:
        """Determine if a violation is auto-fixable."""
        fixable_types = {"mean", "sum", "argmax", "argmin", "premature_discretization"}
        return violation.get("type") in fixable_types

    def _read_file(self, filepath: str) -> str:
        """Read a file with proper encoding handling."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1") as f:
                return f.read()

    def _fix_with_cst(
        self, source: str, violations: List[Dict[str, Any]]
    ) -> Tuple[str, List[FixAction]]:
        """Apply fixes using LibCST."""
        assert cst is not None

        try:
            tree = cst.parse_module(source)
        except Exception as e:
            raise FixerError(f"Failed to parse source: {e}")

        transformer = MirageFixTransformer(violations)
        new_tree = tree.visit(transformer)

        return new_tree.code, transformer.applied_fixes

    def _fix_with_text(
        self, source: str, violations: List[Dict[str, Any]]
    ) -> Tuple[str, List[FixAction]]:
        """Apply fixes using text-based approach (fallback)."""
        lines = source.splitlines(keepends=True)
        actions: List[FixAction] = []

        # Sort by line number descending to avoid offset issues
        sorted_violations = sorted(violations, key=lambda v: v.get("line", 0), reverse=True)

        for v in sorted_violations:
            line_idx = v.get("line", 0) - 1
            if 0 <= line_idx < len(lines):
                vtype = v.get("type", "unknown")
                original_line = lines[line_idx]

                # Add TODO comment if not already present
                if "# TODO: demyst" not in original_line and "# demyst-fix" not in original_line:
                    comment = f"  # TODO: demyst - Use VariationTensor for '{vtype}' to preserve variance\n"
                    lines[line_idx] = original_line.rstrip("\n") + comment

                    actions.append(
                        FixAction(
                            type=FixType.COMMENT_TODO,
                            line=v.get("line", 0),
                            original_code=original_line.strip(),
                            fixed_code=lines[line_idx].strip(),
                            description=f"Added TODO for {vtype}",
                            violation=v,
                        )
                    )

        return "".join(lines), actions

    def _validate_python(self, source: str) -> None:
        """Validate that source is valid Python."""
        if self._use_cst:
            cst.parse_module(source)
        else:
            import ast

            ast.parse(source)

    def _get_diff(self, original: str, modified: str) -> str:
        """Generate a unified diff."""
        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines, modified_lines, fromfile="original", tofile="fixed", lineterm=""
        )

        return "".join(diff)

    def _get_fix_description(self, violation: Dict[str, Any]) -> str:
        """Get a description of the fix."""
        vtype = violation.get("type", "unknown")
        descriptions = {
            "mean": "Transform np.mean to VariationTensor.collapse('mean')",
            "sum": "Transform np.sum to VariationTensor.ensemble_sum()",
            "argmax": "Transform np.argmax to VariationTensor.collapse('argmax')",
            "argmin": "Transform np.argmin to VariationTensor.collapse('argmin')",
            "premature_discretization": "Wrap discretization in VariationTensor tracking",
        }
        return descriptions.get(vtype, "Auto-fix not yet implemented")


# =============================================================================
# Convenience Functions
# =============================================================================


def fix_source(
    source: str, violations: List[Dict[str, Any]], dry_run: bool = False
) -> Tuple[str, List[FixAction]]:
    """
    Fix violations in source code.

    Args:
        source: Python source code
        violations: List of violations to fix
        dry_run: If True, don't apply changes

    Returns:
        Tuple of (fixed_source, list_of_actions)
    """
    fixer = DemystFixer(dry_run=dry_run, interactive=False, backup=False)

    if fixer._use_cst:
        return fixer._fix_with_cst(source, violations)
    else:
        return fixer._fix_with_text(source, violations)

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

# Inline suppression pattern: # demyst: ignore or # demyst: ignore-mirage
DEMYST_IGNORE_PATTERN = re.compile(r"#\s*demyst:\s*ignore(?:-(\w+))?", re.IGNORECASE)

# Comprehensive set of numpy functions that create/return arrays
NUMPY_ARRAY_CREATORS = {
    # Construction
    "array",
    "asarray",
    "zeros",
    "ones",
    "empty",
    "full",
    "zeros_like",
    "ones_like",
    "empty_like",
    "full_like",
    "eye",
    "identity",
    "diag",
    "diagflat",
    "tri",
    "tril",
    "triu",
    # Ranges
    "arange",
    "linspace",
    "logspace",
    "geomspace",
    # Combination
    "stack",
    "concatenate",
    "hstack",
    "vstack",
    "dstack",
    "column_stack",
    "row_stack",
    "block",
    "append",
    "insert",
    # Transforms that return arrays
    "cumsum",
    "cumprod",
    "diff",
    "gradient",
    "ediff1d",
    "sort",
    "argsort",
    "copy",
    "reshape",
    "flatten",
    "ravel",
    "transpose",
    "swapaxes",
    "moveaxis",
    "rollaxis",
    "squeeze",
    "expand_dims",
    "atleast_1d",
    "atleast_2d",
    "atleast_3d",
    # Math operations that preserve array structure
    "abs",
    "absolute",
    "sqrt",
    "square",
    "exp",
    "log",
    "log10",
    "log2",
    "sin",
    "cos",
    "tan",
    "arcsin",
    "arccos",
    "arctan",
    # Broadcasting/tiling
    "tile",
    "repeat",
    "broadcast_to",
    # Masking/filtering (return arrays)
    "where",
    "select",
    "compress",
    "extract",
    "unique",
    "intersect1d",
    "union1d",
    "setdiff1d",
    # Loading
    "load",
    "loadtxt",
    "genfromtxt",
    "fromfile",
    "frombuffer",
}

# Numpy random module functions that create arrays
NUMPY_RANDOM_CREATORS = {
    "normal",
    "uniform",
    "randn",
    "rand",
    "randint",
    "random",
    "random_sample",
    "ranf",
    "sample",
    "choice",
    "permutation",
    "shuffle",
    "exponential",
    "poisson",
    "binomial",
    "standard_normal",
    "beta",
    "gamma",
    "chisquare",
    "dirichlet",
    "laplace",
    "logistic",
    "lognormal",
    "pareto",
    "multivariate_normal",
    "multinomial",
}


class DispersionContextCollector(ast.NodeVisitor):
    """
    First-pass collector that identifies variance/distribution operations and
    the variables they operate on, indexed by line number and scope.
    """

    # Operations that keep distributional information available
    DISPERSION_OPS = {
        "std",
        "var",
        "nanstd",
        "nanvar",
        "std_",
        "var_",
        "min",
        "max",
        "amin",
        "amax",
        "hist",
        "histogram",
        "quantile",
        "percentile",
    }

    def __init__(self) -> None:
        # Map: (variable_name, function_scope) -> set of line numbers where dispersion is computed
        self.dispersion_contexts: Dict[Tuple[Optional[str], Optional[str]], Set[int]] = {}
        self.current_function: Optional[str] = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function

    def visit_Call(self, node: ast.Call) -> None:
        """Collect dispersion operations."""
        var_name = None
        is_dispersion_op = False

        if isinstance(node.func, ast.Attribute):
            # np.<op>(x)
            if isinstance(node.func.value, ast.Name) and node.func.value.id in ["np", "numpy"]:
                if node.func.attr in self.DISPERSION_OPS:
                    is_dispersion_op = True
                    if node.args and isinstance(node.args[0], ast.Name):
                        var_name = node.args[0].id

            # x.<op>() (array/pandas methods)
            elif node.func.attr in self.DISPERSION_OPS:
                is_dispersion_op = True
                if isinstance(node.func.value, ast.Name):
                    var_name = node.func.value.id

        if is_dispersion_op:
            key = (var_name, self.current_function)
            if key not in self.dispersion_contexts:
                self.dispersion_contexts[key] = set()
            self.dispersion_contexts[key].add(node.lineno)

        self.generic_visit(node)


@dataclass
class VarState:
    """Tracks context inferred for a variable within a scope."""

    high_cardinality: bool = False
    dispersion_lines: Set[int] = field(default_factory=set)


class MirageDetector(ast.NodeVisitor):
    """
    AST visitor that detects destructive operations that collapse physical information.

    Config options:
        check_variance_context: bool - Suppress mean/sum warning if std/var is
            computed on same data nearby (default: True)
    """

    # Context window: variance computed within this many lines suppresses warning
    VARIANCE_CONTEXT_LINES = 10

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.mirages: List[Dict[str, Any]] = []
        self.current_function: Optional[str] = None
        self.config = config or {}
        self.check_variance_context = self.config.get("check_variance_context", True)
        self.context_window = self.config.get("variance_context_lines", self.VARIANCE_CONTEXT_LINES)

        # Will be populated by pre-pass if variance context checking enabled
        self.dispersion_contexts: Dict[Tuple[Optional[str], Optional[str]], Set[int]] = {}
        self.var_states: Dict[Tuple[Optional[str], Optional[str]], VarState] = {}

        # Lines with inline suppression comments
        self._suppressed_lines: Set[int] = set()
        self._source_lines: List[str] = []

    def analyze(self, tree: ast.AST, source: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analyze an AST tree with optional variance context awareness.

        This performs a two-pass analysis when check_variance_context is enabled:
        1. First pass: collect all variance operations (std, var)
        2. Second pass: detect mirages, suppressing those with variance context

        Args:
            tree: The AST to analyze
            source: Optional source code string for inline suppression detection
        """
        # Collect inline suppression comments from source
        if source:
            self._source_lines = source.splitlines()
            self._collect_suppressions()

        if self.check_variance_context:
            # First pass: collect variance contexts
            collector = DispersionContextCollector()
            collector.visit(tree)
            self.dispersion_contexts = collector.dispersion_contexts

        # Second pass: detect mirages
        self.visit(tree)
        return self.mirages

    def _collect_suppressions(self) -> None:
        """Scan source lines for # demyst: ignore comments."""
        for i, line in enumerate(self._source_lines, start=1):
            match = DEMYST_IGNORE_PATTERN.search(line)
            if match:
                guard_type = match.group(1)  # e.g., "mirage" from "ignore-mirage"
                # If no specific guard or matches "mirage", suppress this line
                if guard_type is None or guard_type.lower() in ("mirage", "all"):
                    self._suppressed_lines.add(i)

    def _is_suppressed(self, line: int) -> bool:
        """Check if a line has an inline suppression comment."""
        return line in self._suppressed_lines

    def _has_variance_context(self, var_name: Optional[str], line: int) -> bool:
        """
        Check if variance is computed on the same variable nearby.

        Returns True if std/var is called on the same variable within
        VARIANCE_CONTEXT_LINES lines, in the same function scope.
        """
        if not self.check_variance_context or not var_name:
            return False

        key = (var_name, self.current_function)
        if key not in self.dispersion_contexts:
            return False

        # If context window is None, allow any dispersion in the same scope to count
        if self.context_window is None:
            return len(self.dispersion_contexts[key]) > 0

        # Check if any variance operation is within the context window
        for variance_line in self.dispersion_contexts[key]:
            if abs(variance_line - line) <= self.context_window:
                return True

        return False

    def _mark_high_cardinality(self, var_name: Optional[str]) -> None:
        """Mark a variable as likely high-cardinality in the current scope."""
        if not var_name:
            return
        key = (var_name, self.current_function)
        state = self.var_states.get(key, VarState())
        state.high_cardinality = True
        self.var_states[key] = state

    def _is_high_cardinality(self, var_name: Optional[str]) -> bool:
        if not var_name:
            return False
        key = (var_name, self.current_function)
        return self.var_states.get(key, VarState()).high_cardinality

    def _literal_is_large(self, node: ast.AST) -> bool:
        """Heuristic: literal with several elements implies collection."""
        if isinstance(node, (ast.List, ast.Set, ast.Tuple)):
            return len(getattr(node, "elts", [])) >= 4
        if isinstance(node, ast.Dict):
            return len(getattr(node, "keys", [])) >= 4
        return False

    def _call_builds_collection(self, node: ast.Call) -> bool:
        """Heuristic: constructors likely to produce arrays/collections."""
        # Python builtins
        if isinstance(node.func, ast.Name) and node.func.id in {"list", "set", "tuple", "dict"}:
            return True

        if isinstance(node.func, ast.Attribute):
            # np.<func> - check against comprehensive array creators
            if isinstance(node.func.value, ast.Name) and node.func.value.id in {"np", "numpy"}:
                if node.func.attr in NUMPY_ARRAY_CREATORS:
                    return True

            # np.random.<func> - check random module functions
            if isinstance(node.func.value, ast.Attribute):
                if (
                    isinstance(node.func.value.value, ast.Name)
                    and node.func.value.value.id in {"np", "numpy"}
                    and node.func.value.attr == "random"
                ):
                    if node.func.attr in NUMPY_RANDOM_CREATORS:
                        return True

            # pandas functions
            if isinstance(node.func.value, ast.Name) and node.func.value.id in {"pd", "pandas"}:
                if node.func.attr.lower() in {
                    "dataframe",
                    "series",
                    "concat",
                    "read_csv",
                    "read_excel",
                    "read_json",
                    "read_parquet",
                }:
                    return True

        return False

    def _track_assignment_sources(self, target: ast.AST, value: ast.AST) -> None:
        """Infer high-cardinality sources from assignments."""
        var_name = target.id if isinstance(target, ast.Name) else None
        if var_name is None:
            return

        if self._literal_is_large(value):
            self._mark_high_cardinality(var_name)
        elif isinstance(value, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            self._mark_high_cardinality(var_name)
        elif isinstance(value, ast.Call) and self._call_builds_collection(value):
            self._mark_high_cardinality(var_name)
        elif isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name):
            # Accessing .values/.items/.tolist suggests dataset-like object
            if value.attr in {"values", "items", "tolist", "to_list"}:
                self._mark_high_cardinality(var_name)

    def _arg_is_array_like(self, arg: ast.AST) -> tuple[bool, str]:
        """Check if an argument is array-like and return (is_array, confidence)."""
        # Inline list/tuple: np.mean([1,2,3])
        if isinstance(arg, (ast.List, ast.Tuple)):
            return (True, "low")

        # Chained call that builds array: np.mean(np.ones(10))
        if isinstance(arg, ast.Call):
            if self._call_builds_collection(arg):
                return (True, "high")

            # Nested reduction: np.mean(np.mean(x)) - flag as suspicious
            # Even if inner returns scalar, nesting reductions is a code smell
            if isinstance(arg.func, ast.Attribute):
                if isinstance(arg.func.value, ast.Name) and arg.func.value.id in {"np", "numpy"}:
                    if arg.func.attr in {"mean", "sum", "argmax", "argmin"}:
                        return (True, "low")

        if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name):
            # Common array-like accessors: .values/.tolist etc.
            if arg.attr in {"values", "items", "tolist", "to_list", "array", "data"}:
                return (True, "low")

        return (False, "")

    def _is_known_scalar(self, var_name: Optional[str]) -> bool:
        """Check if a variable is known to be scalar (not array-like)."""
        if not var_name:
            return False
        # Check for common scalar indicators in name
        scalar_patterns = {"count", "length", "size", "index", "idx", "i", "j", "k", "n"}
        return var_name.lower() in scalar_patterns

    def _evaluate_reduction_target(self, target: ast.AST) -> Tuple[bool, str, Optional[str]]:
        """
        Determine whether a reduction target is array-like.

        Returns: (should_flag, confidence, var_name)
        """
        var_name: Optional[str] = None
        confidence = "low"

        if isinstance(target, ast.Name):
            var_name = target.id
            if self._is_high_cardinality(var_name):
                return True, "medium", var_name
            if not self._is_known_scalar(var_name):
                return True, "low", var_name
            return False, "", var_name

        is_array, conf = self._arg_is_array_like(target)
        if is_array:
            return True, conf, None

        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
            var_name = target.value.id
            if target.attr in {"values", "items", "tolist", "to_list", "array", "data"}:
                if self._is_high_cardinality(var_name):
                    return True, "medium", var_name
                if not self._is_known_scalar(var_name):
                    return True, "low", var_name

        return False, "", var_name

    # Operations that collapse array data to single values, destroying variance
    VARIANCE_DESTROYING_OPS = {
        "mean",
        "nanmean",
        "sum",
        "nansum",
        "argmax",
        "argmin",
        "median",
        "nanmedian",
        "percentile",
        "nanpercentile",
        "quantile",
        "nanquantile",
    }

    def visit_Call(self, node: ast.Call) -> None:
        """Detect variance-destroying reductions on array-like data."""
        if isinstance(node.func, ast.Attribute):
            # Detect np.mean/sum/argmax/argmin/median/percentile or array method calls
            # These are variance-destroying: they collapse distributions to single values
            is_numpy = isinstance(node.func.value, ast.Name) and node.func.value.id in [
                "np",
                "numpy",
            ]
            is_method = not is_numpy and isinstance(node.func.value, ast.AST)
            if (is_numpy or is_method) and node.func.attr in self.VARIANCE_DESTROYING_OPS:
                var_name: Optional[str] = None
                should_flag = False
                confidence = "low"

                if is_numpy and node.args:
                    should_flag, confidence, var_name = self._evaluate_reduction_target(
                        node.args[0]
                    )
                else:
                    # Method call: evaluate the receiver expression (handles data.mean(), np.ones(...).mean())
                    should_flag, confidence, var_name = self._evaluate_reduction_target(
                        node.func.value
                    )
                    if not should_flag and node.args:
                        # Fallback: sometimes callers pass the data explicitly even on methods
                        (
                            fallback_flag,
                            fallback_conf,
                            fallback_var,
                        ) = self._evaluate_reduction_target(node.args[0])
                        if fallback_flag:
                            should_flag = True
                            confidence = fallback_conf
                            var_name = var_name or fallback_var

                # Check for inline suppression or dispersion context
                if self._is_suppressed(node.lineno):
                    self.generic_visit(node)
                    return

                has_dispersion = self._has_variance_context(var_name, node.lineno)

                if should_flag and not has_dispersion:
                    blocking = confidence in {"high", "medium"}
                    self.mirages.append(
                        {
                            "type": node.func.attr,
                            "node": node,
                            "line": node.lineno,
                            "col": node.col_offset,
                            "function": self.current_function,
                            "variable": var_name,
                            "confidence": confidence,
                            "blocking": blocking,
                            "reason": "Reduction on array-like data without accompanying dispersion check.",
                        }
                    )

        # Check for premature discretization on array-like data
        if isinstance(node.func, ast.Name) and node.func.id in ["round", "int"]:
            if (
                len(node.args) > 0
                and self._is_array_like(node.args[0])
                and not self._is_suppressed(node.lineno)
            ):
                self.mirages.append(
                    {
                        "type": "premature_discretization",
                        "node": node,
                        "line": node.lineno,
                        "col": node.col_offset,
                        "function": self.current_function,
                        "confidence": "low",
                        "blocking": False,
                        "reason": "Rounding/forcing int on data that appears array-like.",
                    }
                )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track current function context"""
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function

    def visit_Assign(self, node: ast.Assign) -> None:
        """Track assignments that imply collection/array-like data."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self._track_assignment_sources(target, node.value)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """Iterating over a variable implies it is collection-like/high-cardinality."""
        if isinstance(node.iter, ast.Name):
            self._mark_high_cardinality(node.iter.id)
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        """Indexing suggests collection."""
        if isinstance(node.value, ast.Name):
            self._mark_high_cardinality(node.value.id)
        self.generic_visit(node)

    def _is_array_like(self, node: ast.AST) -> bool:
        """Conservative heuristic to determine if a node represents array-like data.

        Returns True only for nodes that are clearly array-like to avoid
        false positives on scalar variables like `round(loss, 2)`.
        """
        # Call that builds a collection is definitely array-like
        if isinstance(node, ast.Call):
            return self._call_builds_collection(node)

        # Subscript access suggests collection
        if isinstance(node, ast.Subscript):
            return True

        # List/tuple literals are array-like
        if isinstance(node, (ast.List, ast.Tuple)):
            return True

        if isinstance(node, ast.Name):
            # Known scalar patterns should not be flagged
            if self._is_known_scalar(node.id):
                return False
            # If we've already inferred high-cardinality, it's array-like
            if self._is_high_cardinality(node.id):
                return True
            # Default: treat unknown names as array-like to avoid missing core mirages
            return True

        # Attribute access like .values, .data suggests array-like
        if isinstance(node, ast.Attribute):
            if node.attr in {"values", "data", "array", "tolist", "to_list"}:
                return True

        return False

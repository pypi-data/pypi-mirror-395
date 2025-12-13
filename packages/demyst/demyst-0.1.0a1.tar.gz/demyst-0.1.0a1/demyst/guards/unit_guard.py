"""
UnitGuard: Dimensional Analysis and Unit Consistency

Detects:
    1. Unit mismatches (adding meters to seconds)
    2. Dimensionless assumptions that hide physical meaning
    3. Missing unit conversions
    4. Physics law violations through dimensional analysis

Philosophy: "The universe doesn't care about your naming conventions.
             It cares about dimensions."
"""

import ast
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple


class BaseDimension(Enum):
    """SI Base Dimensions."""

    LENGTH = "L"  # meters [m]
    MASS = "M"  # kilograms [kg]
    TIME = "T"  # seconds [s]
    CURRENT = "I"  # amperes [A]
    TEMPERATURE = "Θ"  # kelvin [K]
    AMOUNT = "N"  # moles [mol]
    LUMINOSITY = "J"  # candela [cd]
    DIMENSIONLESS = "1"  # no dimension


@dataclass(frozen=True)
class Dimension:
    """
    Represents a physical dimension as a product of base dimensions.

    Examples:
        Velocity: L^1 * T^-1
        Force: M^1 * L^1 * T^-2
        Energy: M^1 * L^2 * T^-2
    """

    exponents: Tuple[int, ...]  # (L, M, T, I, Θ, N, J)

    def __post_init__(self) -> None:
        if len(self.exponents) != 7:
            object.__setattr__(
                self, "exponents", tuple(list(self.exponents) + [0] * (7 - len(self.exponents)))
            )

    @classmethod
    def dimensionless(cls) -> "Dimension":
        return cls((0, 0, 0, 0, 0, 0, 0))

    @classmethod
    def length(cls) -> "Dimension":
        return cls((1, 0, 0, 0, 0, 0, 0))

    @classmethod
    def mass(cls) -> "Dimension":
        return cls((0, 1, 0, 0, 0, 0, 0))

    @classmethod
    def time(cls) -> "Dimension":
        return cls((0, 0, 1, 0, 0, 0, 0))

    @classmethod
    def temperature(cls) -> "Dimension":
        return cls((0, 0, 0, 0, 1, 0, 0))

    @classmethod
    def velocity(cls) -> "Dimension":
        return cls((1, 0, -1, 0, 0, 0, 0))

    @classmethod
    def acceleration(cls) -> "Dimension":
        return cls((1, 0, -2, 0, 0, 0, 0))

    @classmethod
    def force(cls) -> "Dimension":
        return cls((1, 1, -2, 0, 0, 0, 0))

    @classmethod
    def energy(cls) -> "Dimension":
        return cls((2, 1, -2, 0, 0, 0, 0))

    @classmethod
    def power(cls) -> "Dimension":
        return cls((2, 1, -3, 0, 0, 0, 0))

    @classmethod
    def pressure(cls) -> "Dimension":
        return cls((-1, 1, -2, 0, 0, 0, 0))

    def __mul__(self, other: "Dimension") -> "Dimension":
        """Multiply dimensions (add exponents)."""
        return Dimension(tuple(a + b for a, b in zip(self.exponents, other.exponents)))

    def __truediv__(self, other: "Dimension") -> "Dimension":
        """Divide dimensions (subtract exponents)."""
        return Dimension(tuple(a - b for a, b in zip(self.exponents, other.exponents)))

    def __pow__(self, n: int) -> "Dimension":
        """Raise dimension to power."""
        return Dimension(tuple(a * n for a in self.exponents))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dimension):
            return False
        return self.exponents == other.exponents

    def __hash__(self) -> int:
        return hash(self.exponents)

    def is_dimensionless(self) -> bool:
        return all(e == 0 for e in self.exponents)

    def __str__(self) -> str:
        if self.is_dimensionless():
            return "[1]"

        symbols = ["L", "M", "T", "I", "Θ", "N", "J"]
        parts = []
        for sym, exp in zip(symbols, self.exponents):
            if exp == 1:
                parts.append(sym)
            elif exp != 0:
                parts.append(f"{sym}^{exp}")

        return "[" + " ".join(parts) + "]"


@dataclass
class UnitViolation:
    """Represents a unit/dimensional analysis violation."""

    violation_type: str
    severity: str  # 'critical', 'warning', 'info'
    line: int
    col: int
    expression: str
    left_dimension: Optional[Dimension]
    right_dimension: Optional[Dimension]
    description: str
    physical_meaning: str
    recommendation: str


# Common unit patterns in variable names
UNIT_PATTERNS = {
    # Length
    r"(?:^|_)(distance|length|height|width|depth|radius|diameter|position|x|y|z)(?:_|$)": Dimension.length(),
    r"(?:^|_)(meter|metre|m)(?:_|s|$)": Dimension.length(),
    r"(?:^|_)(km|cm|mm|nm|um)(?:_|s|$)": Dimension.length(),
    # Mass
    r"(?:^|_)(mass|weight)(?:_|$)": Dimension.mass(),
    r"(?:^|_)(kg|gram|g)(?:_|s|$)": Dimension.mass(),
    # Time
    r"(?:^|_)(time|duration|period|dt|delta_t)(?:_|$)": Dimension.time(),
    r"(?:^|_)(second|sec|s|minute|min|hour|hr)(?:_|s|$)": Dimension.time(),
    # Temperature
    r"(?:^|_)(temp|temperature|T)(?:_|$)": Dimension.temperature(),
    r"(?:^|_)(kelvin|celsius|K)(?:_|s|$)": Dimension.temperature(),
    # Velocity
    r"(?:^|_)(velocity|speed|v|vel)(?:_|$)": Dimension.velocity(),
    r"(?:^|_)(m_per_s|mps)(?:_|s|$)": Dimension.velocity(),
    # Acceleration
    r"(?:^|_)(acceleration|accel|a)(?:_|$)": Dimension.acceleration(),
    # Force
    r"(?:^|_)(force|F)(?:_|$)": Dimension.force(),
    r"(?:^|_)(newton|N)(?:_|s|$)": Dimension.force(),
    # Energy
    r"(?:^|_)(energy|E|work|W)(?:_|$)": Dimension.energy(),
    r"(?:^|_)(joule|J|ev|eV)(?:_|s|$)": Dimension.energy(),
    # Power
    r"(?:^|_)(power|P)(?:_|$)": Dimension.power(),
    r"(?:^|_)(watt|W)(?:_|s|$)": Dimension.power(),
    # Pressure
    r"(?:^|_)(pressure|p|stress)(?:_|$)": Dimension.pressure(),
    r"(?:^|_)(pascal|Pa|bar|atm)(?:_|s|$)": Dimension.pressure(),
    # Dimensionless
    r"(?:^|_)(ratio|factor|coefficient|count|index|idx|n|num)(?:_|$)": Dimension.dimensionless(),
    r"(?:^|_)(probability|prob|p_value|fraction|percent)(?:_|$)": Dimension.dimensionless(),
}

# GR/Tensor convention patterns (enabled via tensor_conventions config)
TENSOR_CONVENTION_PATTERNS = {
    # Metric tensor components (g_tt, g_rr, g_θθ, g_φφ, g_tr, etc.)
    r"^g_[a-zA-Z]{2}$": Dimension.dimensionless(),
    r"^g[a-zA-Z]{2}$": Dimension.dimensionless(),  # Also gtt, grr without underscore
    # Riemann tensor components (R_abcd)
    r"^R_[a-zA-Z]{4}$": Dimension.dimensionless(),
    # Ricci tensor (R_ab)
    r"^R_[a-zA-Z]{2}$": Dimension.dimensionless(),
    # Stress-energy tensor (T_μν)
    r"^T_[a-zA-Z]{2}$": Dimension.dimensionless(),
    # Christoffel symbols (Gamma_abc, Γ_abc)
    r"^[Gg]amma_[a-zA-Z]{3}$": Dimension.dimensionless(),
    # Einstein tensor (G_ab)
    r"^G_[a-zA-Z]{2}$": Dimension.dimensionless(),
    # Weyl tensor (C_abcd)
    r"^C_[a-zA-Z]{4}$": Dimension.dimensionless(),
    # Generic indexed tensors (A_i, B_ij, etc.)
    r"^[A-Z]_[a-zA-Z]{1,4}$": Dimension.dimensionless(),
}

# Physical constants with known dimensions (SI units)
PHYSICAL_CONSTANTS = {
    "c": Dimension.velocity(),  # Speed of light
    "G": Dimension((3, -1, -2, 0, 0, 0, 0)),  # Gravitational constant L^3 M^-1 T^-2
    "h": Dimension((2, 1, -1, 0, 0, 0, 0)),  # Planck constant L^2 M T^-1
    "hbar": Dimension((2, 1, -1, 0, 0, 0, 0)),
    "k_B": Dimension((2, 1, -2, 0, -1, 0, 0)),  # Boltzmann constant
    "e": Dimension((0, 0, 1, 1, 0, 0, 0)),  # Elementary charge
    "pi": Dimension.dimensionless(),
    "tau": Dimension.dimensionless(),
}

# Constants that become dimensionless in natural units (c=hbar=G=kB=1)
NATURAL_UNIT_CONSTANTS = {
    "c",
    "speed_of_light",
    "hbar",
    "h",
    "h_bar",
    "planck",
    "G",
    "gravitational_constant",
    "k_B",
    "kB",
    "k_b",
    "boltzmann",
}

# ML-specific patterns (checked BEFORE physics patterns to avoid false positives)
# These override single-letter patterns like x, y, z which mean coordinates in physics
# but mean features/targets in ML
ML_PATTERNS = {
    # Target/prediction variables (y_true, y_pred, y_hat, etc.)
    r"^y_": Dimension.dimensionless(),
    r"^y$": Dimension.dimensionless(),  # bare y in ML context
    r"_pred$": Dimension.dimensionless(),
    r"_true$": Dimension.dimensionless(),
    r"_hat$": Dimension.dimensionless(),
    r"_label": Dimension.dimensionless(),
    r"_target": Dimension.dimensionless(),
    # Feature matrices (X_train, X_test, etc.)
    r"^X_": Dimension.dimensionless(),
    r"^X$": Dimension.dimensionless(),
    # Common ML variable patterns
    r"(?:^|_)(logits?|probs?|scores?|weights?|bias|loss|grad|gradient)(?:_|$)": Dimension.dimensionless(),
    r"(?:^|_)(hidden|embedding|feature|input|output|activation|mask|attention)(?:_|s|$)": Dimension.dimensionless(),
    r"(?:^|_)(batch|epoch|layer|channel|kernel|stride|padding|token|vocab)(?:_|s|$)": Dimension.dimensionless(),
    r"(?:^|_)(lr|learning_rate|momentum|dropout|epsilon|delta|gamma|alpha|beta)(?:_|$)": Dimension.dimensionless(),
    r"(?:^|_)(smooth|clip|threshold|margin|scale|fold)(?:_|$)": Dimension.dimensionless(),
    # Loss function variables
    r"(?:^|_)(tp|fp|tn|fn|precision|recall|f1|accuracy|auc|dice|iou|jaccard)(?:_|$)": Dimension.dimensionless(),
    r"(?:^|_)(tversky|focal|cross_entropy|mse|mae|rmse|bce|ground_truth|gt|target|label)(?:_|$)": Dimension.dimensionless(),
    # Validation/Test splits
    r"(?:^|_)(val|validation|test|train)(?:_|$)": Dimension.dimensionless(),
    # Computer Vision
    r"(?:^|_)(roi|bbox|box|rect|pixel)(?:_|$)": Dimension.dimensionless(),
    # Index/count variables (steps_x, x_start, num_x, etc.) - NOT coordinates
    r"(?:^|_)steps?_": Dimension.dimensionless(),
    r"_(?:start|end|min|max|size|len|count|num|idx|index)$": Dimension.dimensionless(),
    r"^(?:n|num|len|size|count|idx|index|step|offset|pointer)_": Dimension.dimensionless(),
    r"^(?:i|j|k|n|m)$": Dimension.dimensionless(),  # Common loop variables
    r"(?:^|_)(length|width|height|depth|shape|dim|axis)(?:_|$)": Dimension.dimensionless(),  # Array dimensions, not physical
    r"(?:^|_)(shared|global|local)_": Dimension.dimensionless(),  # Shared/global variables
}


class UnitInferenceEngine:
    """
    Infers dimensional types from code context.

    Uses:
        1. Variable naming conventions
        2. Physical constants
        3. Function signatures
        4. Type annotations

    Config options:
        natural_units: bool - Treat c, hbar, G, kB as dimensionless
        tensor_conventions: bool - Recognize GR tensor index notation
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.type_environment: Dict[str, Dimension] = {}

        # Build pattern list based on config
        # ML patterns are checked FIRST to avoid false positives on y_pred, X_train, etc.
        patterns: Dict[str, Dimension] = {}

        # Add ML patterns first (highest priority) unless explicitly disabled
        if self.config.get("ml_patterns", True):
            patterns.update(ML_PATTERNS)

        # Add physics unit patterns
        patterns.update(UNIT_PATTERNS)

        # Add tensor convention patterns if enabled
        if self.config.get("tensor_conventions", False):
            patterns.update(TENSOR_CONVENTION_PATTERNS)

        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), dim) for pattern, dim in patterns.items()
        ]

        # Track natural units mode
        self.natural_units = self.config.get("natural_units", False)

    def infer_from_name(self, name: str) -> Optional[Dimension]:
        """Infer dimension from variable name."""
        # In natural units mode, treat fundamental constants as dimensionless
        if self.natural_units and name in NATURAL_UNIT_CONSTANTS:
            return Dimension.dimensionless()

        # Check physical constants (with their actual dimensions)
        if name in PHYSICAL_CONSTANTS:
            return PHYSICAL_CONSTANTS[name]

        # Check patterns
        for pattern, dim in self.compiled_patterns:
            if pattern.search(name):
                return dim

        return None

    def infer_from_operation(
        self, op: str, left: Optional[Dimension], right: Optional[Dimension]
    ) -> Optional[Dimension]:
        """Infer dimension from binary operation."""
        if left is None or right is None:
            return None

        if op in ["Add", "Sub"]:
            # Addition/subtraction requires same dimensions
            if left == right:
                return left
            else:
                return None  # Violation

        elif op == "Mult":
            return left * right

        elif op == "Div":
            return left / right

        elif op == "Pow":
            # Power with dimensionless exponent
            if right.is_dimensionless():
                return left  # Simplified - should track exponent
            return None

        return None

    def register_type(self, name: str, dimension: Dimension) -> None:
        """Register a known type for a variable."""
        self.type_environment[name] = dimension

    def get_type(self, name: str) -> Optional[Dimension]:
        """Get type from environment or infer from name."""
        if name in self.type_environment:
            return self.type_environment[name]
        return self.infer_from_name(name)


class DimensionalAnalyzer(ast.NodeVisitor):
    """
    AST visitor that performs dimensional analysis.

    Tracks:
        1. Variable declarations with inferred units
        2. Operations between quantities
        3. Function parameters and returns
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.engine = UnitInferenceEngine(config)
        self.violations: List[UnitViolation] = []
        self.current_function: Optional[str] = None
        self.assignments: Dict[str, Dimension] = {}
        # Track available unit libraries to avoid false alarms when strong typing is used
        self.imported_units: Set[str] = set()
        self.annotated_dimensions: Dict[str, Dimension] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track function definitions and infer parameter dimensions."""
        old_function = self.current_function
        self.current_function = node.name

        # Infer dimensions from parameter names
        for arg in node.args.args:
            dim = self._dimension_from_annotation(arg.annotation) or self.engine.infer_from_name(
                arg.arg
            )
            if dim:
                self.engine.register_type(arg.arg, dim)

        self.generic_visit(node)
        self.current_function = old_function

    def visit_Assign(self, node: ast.Assign) -> None:
        """Track assignments and check dimensional consistency."""
        right_dim = self._infer_expression_dimension(node.value)

        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id
                annotated_dim = self.annotated_dimensions.get(name)
                expected_dim = annotated_dim or self.engine.infer_from_name(name)

                # If RHS is dimensionless (e.g. literal number), allow it to take the LHS annotated dimension
                if expected_dim and right_dim and right_dim.is_dimensionless():
                    right_dim = expected_dim

                if expected_dim and right_dim and expected_dim != right_dim:
                    severity = "critical" if annotated_dim else "warning"
                    self.violations.append(
                        UnitViolation(
                            violation_type="dimension_mismatch",
                            severity=severity,
                            line=node.lineno,
                            col=node.col_offset,
                            expression=ast.unparse(node) if hasattr(ast, "unparse") else str(node),
                            left_dimension=expected_dim,
                            right_dimension=right_dim,
                            description=(
                                f"Variable '{name}' expects dimension {expected_dim} "
                                f"but is assigned value with dimension {right_dim}."
                            ),
                            physical_meaning=(
                                "Assignment violates annotated or inferred dimension; likely missing conversion."
                            ),
                            recommendation=(
                                "Ensure RHS has the same dimension or convert explicitly."
                            ),
                        )
                    )

                # Register the inferred or assigned dimension
                if right_dim:
                    self.engine.register_type(name, right_dim)
                elif expected_dim:
                    self.engine.register_type(name, expected_dim)

        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Handle annotated assignments to get authoritative dimensions."""
        target = node.target
        dim = self._dimension_from_annotation(node.annotation)
        if isinstance(target, ast.Name) and dim:
            self.annotated_dimensions[target.id] = dim
            self.engine.register_type(target.id, dim)
        # Process the value side to detect violations on initialization
        if node.value:
            right_dim = self._infer_expression_dimension(node.value)
            if isinstance(target, ast.Name) and dim and right_dim and dim != right_dim:
                self.violations.append(
                    UnitViolation(
                        violation_type="dimension_mismatch",
                        severity="critical",
                        line=node.lineno,
                        col=node.col_offset,
                        expression=ast.unparse(node) if hasattr(ast, "unparse") else str(node),
                        left_dimension=dim,
                        right_dimension=right_dim,
                        description=(
                            f"Annotated dimension {dim} for '{target.id}' "
                            f"conflicts with assigned value dimension {right_dim}."
                        ),
                        physical_meaning="Initialization violates the declared physical dimension.",
                        recommendation="Convert the assigned value to the annotated units or fix the annotation.",
                    )
                )
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Check binary operations for dimensional consistency."""
        left_dim = self._infer_expression_dimension(node.left)
        right_dim = self._infer_expression_dimension(node.right)
        op_name = type(node.op).__name__

        # Check addition/subtraction
        if isinstance(node.op, (ast.Add, ast.Sub)):
            if left_dim and right_dim and left_dim != right_dim:
                self.violations.append(
                    UnitViolation(
                        violation_type="incompatible_addition",
                        severity="critical",
                        line=node.lineno,
                        col=node.col_offset,
                        expression=ast.unparse(node) if hasattr(ast, "unparse") else str(node),
                        left_dimension=left_dim,
                        right_dimension=right_dim,
                        description=(
                            f"Cannot {'add' if isinstance(node.op, ast.Add) else 'subtract'} "
                            f"quantities with dimensions {left_dim} and {right_dim}."
                        ),
                        physical_meaning=(
                            f"This is like adding {'meters to seconds' if left_dim == Dimension.length() else 'apples to oranges'}. "
                            "The result has no physical meaning."
                        ),
                        recommendation=(
                            "Check for missing unit conversions. Ensure both operands "
                            "represent the same physical quantity."
                        ),
                    )
                )

        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        """Check comparisons for dimensional consistency."""
        left_dim = self._infer_expression_dimension(node.left)

        for comparator in node.comparators:
            right_dim = self._infer_expression_dimension(comparator)

            if left_dim and right_dim and left_dim != right_dim:
                self.violations.append(
                    UnitViolation(
                        violation_type="incompatible_comparison",
                        severity="critical",
                        line=node.lineno,
                        col=node.col_offset,
                        expression=ast.unparse(node) if hasattr(ast, "unparse") else str(node),
                        left_dimension=left_dim,
                        right_dimension=right_dim,
                        description=(
                            f"Comparing quantities with incompatible dimensions: "
                            f"{left_dim} vs {right_dim}."
                        ),
                        physical_meaning=(
                            "Comparing physically incompatible quantities. "
                            "The comparison result is meaningless."
                        ),
                        recommendation=(
                            "Convert to same units before comparing, or verify "
                            "this comparison makes physical sense."
                        ),
                    )
                )

        self.generic_visit(node)

    def _infer_expression_dimension(self, node: ast.AST) -> Optional[Dimension]:
        """Infer dimension of an expression."""
        if isinstance(node, ast.Name):
            return self.engine.get_type(node.id)

        elif isinstance(node, ast.Constant):
            # Numeric constants are dimensionless
            if isinstance(node.value, (int, float)):
                return Dimension.dimensionless()
            return None

        elif isinstance(node, ast.BinOp):
            left = self._infer_expression_dimension(node.left)
            right = self._infer_expression_dimension(node.right)
            op_name = type(node.op).__name__
            return self.engine.infer_from_operation(op_name, left, right)

        elif isinstance(node, ast.Call):
            # Try to infer from function name
            func_name = self._get_func_name(node)
            if func_name:
                return self._infer_function_return_dimension(func_name, node)
            return None

        elif isinstance(node, ast.UnaryOp):
            return self._infer_expression_dimension(node.operand)

        elif isinstance(node, ast.Attribute):
            # For now, try to infer from attribute name
            # If this is a known unit-bearing library object, treat as dimensionless to avoid false positives
            if self._is_unit_library_object(node):
                return Dimension.dimensionless()
            return self.engine.infer_from_name(node.attr)

        return None

    def _dimension_from_annotation(self, annotation: Optional[ast.AST]) -> Optional[Dimension]:
        """Interpret type annotations for dimensions."""
        if annotation is None:
            return None

        # Annotated[T, "meters"] or Annotated[T, ("meters",)]
        if isinstance(annotation, ast.Subscript):
            base = annotation.value
            if isinstance(base, ast.Name) and base.id == "Annotated":
                # Expect annotation.slice to contain metadata
                meta = None
                if isinstance(annotation.slice, ast.Tuple) and len(annotation.slice.elts) >= 2:
                    meta = annotation.slice.elts[1]
                elif hasattr(ast, "Index") and isinstance(annotation.slice, ast.Index):  # py<3.9
                    idx_val = annotation.slice.value
                    if isinstance(idx_val, ast.Tuple) and len(idx_val.elts) >= 2:
                        meta = idx_val.elts[1]
                if isinstance(meta, ast.Constant) and isinstance(meta.value, str):
                    return self._dimension_from_string(meta.value)

        # Literal unit names as strings (fallback)
        if isinstance(annotation, ast.Constant) and isinstance(annotation.value, str):
            return self._dimension_from_string(annotation.value)

        return None

    def _dimension_from_string(self, unit: str) -> Optional[Dimension]:
        """Map common unit strings to dimensions."""
        normalized = unit.lower()
        if normalized in {"m", "meter", "metre", "meters", "metres"}:
            return Dimension.length()
        if normalized in {
            "cm",
            "centimeter",
            "centimetre",
            "mm",
            "millimeter",
            "millimetre",
            "km",
            "kilometer",
            "kilometre",
        }:
            return Dimension.length()
        if normalized in {"ft", "foot", "feet", "mile", "miles", "mi"}:
            return Dimension.length()
        if normalized in {"s", "sec", "second", "seconds"}:
            return Dimension.time()
        if normalized in {"ms", "millisecond", "milliseconds", "us", "microsecond", "microseconds"}:
            return Dimension.time()
        if normalized in {"hr", "hour", "hours", "min", "minute", "minutes"}:
            return Dimension.time()
        if normalized in {"kg", "kilogram", "kilograms"}:
            return Dimension.mass()
        if normalized in {"g", "gram", "grams"}:
            return Dimension.mass()
        if normalized in {"k", "kelvin"}:
            return Dimension.temperature()
        if normalized in {"m/s", "mps", "meter_per_second"}:
            return Dimension.velocity()
        if normalized in {"km/h", "kph", "kmph"}:
            return Dimension.velocity()
        if normalized in {"m/s^2", "meter_per_second_squared"}:
            return Dimension.acceleration()
        if normalized in {"n", "newton", "newtons"}:
            return Dimension.force()
        if normalized in {"j", "joule", "joules"}:
            return Dimension.energy()
        if normalized in {"w", "watt", "watts"}:
            return Dimension.power()
        return None

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name.split(".")[0] in {"pint", "astropy"}:
                self.imported_units.add(alias.name.split(".")[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            if node.module.split(".")[0] in {"pint", "astropy"}:
                self.imported_units.add(node.module.split(".")[0])
        self.generic_visit(node)

    def _is_unit_library_object(self, node: ast.Attribute) -> bool:
        """If code uses pint/astropy objects, avoid misclassifying by name."""
        if isinstance(node.value, ast.Name):
            if node.value.id in {"u", "units"} and "astropy" in self.imported_units:
                return True
            if node.value.id in {"ureg", "UnitRegistry"} and "pint" in self.imported_units:
                return True
        return False

    def _get_func_name(self, node: ast.Call) -> Optional[str]:
        """Extract function name from call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

    def _infer_function_return_dimension(
        self, func_name: str, node: ast.Call
    ) -> Optional[Dimension]:
        """Infer return dimension of known functions."""
        # Mathematical functions preserve dimensions or return dimensionless
        dimensionless_funcs = {
            "sin",
            "cos",
            "tan",
            "exp",
            "log",
            "log10",
            "sqrt",
            "abs",
            "ceil",
            "floor",
            "round",
        }

        if func_name in dimensionless_funcs:
            return Dimension.dimensionless()

        # sqrt returns half the exponent
        if func_name == "sqrt" and node.args:
            arg_dim = self._infer_expression_dimension(node.args[0])
            if arg_dim:
                return Dimension(tuple(e // 2 for e in arg_dim.exponents))

        return None


class UnitGuard:
    """
    Main interface for dimensional analysis.

    Usage:
        guard = UnitGuard()
        result = guard.analyze(source_code)

        for v in result['violations']:
            print(f"Line {v['line']}: {v['description']}")
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.analyzer: Optional[DimensionalAnalyzer] = None

    def analyze(self, source: str) -> Dict[str, Any]:
        """
        Analyze source code for dimensional consistency.

        Args:
            source: Python source code string

        Returns:
            Analysis results including violations and type inferences
        """
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return {
                "error": f"Syntax error: {e}",
                "violations": [],
                "inferred_dimensions": {},
                "summary": None,
            }

        self.analyzer = DimensionalAnalyzer(self.config)
        self.analyzer.visit(tree)

        # Compile inferred dimensions
        inferred = {name: str(dim) for name, dim in self.analyzer.engine.type_environment.items()}

        summary = self._generate_summary()

        return {
            "violations": [self._violation_to_dict(v) for v in self.analyzer.violations],
            "inferred_dimensions": inferred,
            "summary": summary,
        }

    def check_expression(
        self, expr: str, type_hints: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Check a single expression for dimensional consistency.

        Args:
            expr: Python expression string
            type_hints: Optional dict mapping variable names to dimension strings

        Returns:
            Analysis result for the expression
        """
        # Wrap expression in assignment for parsing
        source = f"__result__ = {expr}"
        result = self.analyze(source)

        # Filter for relevant results
        if result.get("violations"):
            result["violations"] = [
                v for v in result["violations"] if "__result__" not in v.get("expression", "")
            ]

        return result

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate analysis summary."""
        if not self.analyzer:
            return {"error": "No analysis performed"}

        violations = self.analyzer.violations
        critical = sum(1 for v in violations if v.severity == "critical")
        warning = sum(1 for v in violations if v.severity == "warning")

        if critical > 0:
            verdict = "FAIL: Critical dimensional inconsistencies detected."
        elif warning > 0:
            verdict = "WARNING: Potential dimensional issues detected."
        else:
            verdict = "PASS: No dimensional inconsistencies detected."

        return {
            "total_violations": len(violations),
            "critical_count": critical,
            "warning_count": warning,
            "variables_typed": len(self.analyzer.engine.type_environment),
            "verdict": verdict,
        }

    def _violation_to_dict(self, v: UnitViolation) -> Dict[str, Any]:
        """Convert violation to dictionary."""
        confidence = "high" if v.severity == "critical" else "low"
        return {
            "type": v.violation_type,
            "severity": v.severity,
            "line": v.line,
            "col": v.col,
            "expression": v.expression,
            "left_dimension": str(v.left_dimension) if v.left_dimension else None,
            "right_dimension": str(v.right_dimension) if v.right_dimension else None,
            "description": v.description,
            "physical_meaning": v.physical_meaning,
            "recommendation": v.recommendation,
            "confidence": confidence,
            "blocking": confidence == "high",
        }

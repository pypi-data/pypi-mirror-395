"""
LeakageHunter: Taint Analysis for Train/Test Data Leakage

The #1 error in machine learning is leaking test data into training.
This module implements static taint analysis to detect data leakage.

Philosophy: "If test data touches training, your benchmark is a lie."
"""

import ast
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, cast


class TaintLevel(Enum):
    """Taint levels for data flow tracking."""

    CLEAN = "clean"  # No taint, safe to use anywhere
    TRAIN = "train"  # Training data only
    TEST = "test"  # Test data - NEVER touch training
    VALIDATION = "validation"  # Validation data
    HYPERPARAMETER = "hyperparameter"  # Data used for hyperparameter tuning
    MIXED = "mixed"  # Contaminated - train and test mixed (CRITICAL)


@dataclass
class TaintSource:
    """Represents a source of tainted data."""

    name: str
    level: TaintLevel
    line: int
    col: int
    source_type: str  # 'load', 'split', 'assignment', 'parameter'


@dataclass
class LeakageViolation:
    """Represents a detected data leakage violation."""

    violation_type: str
    severity: str  # 'critical', 'warning', 'info'
    line: int
    col: int
    tainted_variable: str
    taint_source: str
    contaminated_context: str
    description: str
    scientific_impact: str
    recommendation: str


@dataclass
class DataFlowPath:
    """Represents a path of data flow through the code."""

    source: TaintSource
    transformations: List[Tuple[str, int]]  # (operation, line)
    sink: str
    sink_line: int


class DataFlowTracker:
    """
    Tracks data flow through variables using symbolic execution.

    This is a simplified version of taint analysis that tracks:
    1. Where data comes from (sources)
    2. How it transforms (operations)
    3. Where it goes (sinks)
    """

    def __init__(self) -> None:
        self.taint_map: Dict[str, TaintSource] = {}
        self.flow_paths: List[DataFlowPath] = []

    def add_source(
        self, name: str, level: TaintLevel, line: int, col: int, source_type: str
    ) -> None:
        """Register a new taint source."""
        self.taint_map[name] = TaintSource(
            name=name, level=level, line=line, col=col, source_type=source_type
        )

    def propagate(self, target: str, sources: List[str], line: int) -> None:
        """Propagate taint from sources to target."""
        source_levels = []
        for src in sources:
            if src in self.taint_map:
                source_levels.append(self.taint_map[src])

        if not source_levels:
            return

        # Determine combined taint level
        levels = {s.level for s in source_levels}

        if TaintLevel.TEST in levels and TaintLevel.TRAIN in levels:
            combined_level = TaintLevel.MIXED
        elif TaintLevel.TEST in levels:
            combined_level = TaintLevel.TEST
        elif TaintLevel.TRAIN in levels:
            combined_level = TaintLevel.TRAIN
        elif TaintLevel.VALIDATION in levels:
            combined_level = TaintLevel.VALIDATION
        else:
            combined_level = TaintLevel.CLEAN

        self.taint_map[target] = TaintSource(
            name=target, level=combined_level, line=line, col=0, source_type="propagation"
        )

    def get_taint(self, name: str) -> Optional[TaintSource]:
        """Get taint information for a variable."""
        return self.taint_map.get(name)

    def check_violation(self, variable: str, context: str, line: int) -> Optional[LeakageViolation]:
        """Check if using a variable in a context causes a violation."""
        taint = self.get_taint(variable)
        if not taint:
            return None

        # Test data in training context
        if taint.level == TaintLevel.TEST and context in ["train", "fit", "training_loop"]:
            return LeakageViolation(
                violation_type="test_in_training",
                severity="critical",
                line=line,
                col=0,
                tainted_variable=variable,
                taint_source=f"Line {taint.line}",
                contaminated_context=context,
                description=(
                    f"Test data '{variable}' is being used in training context '{context}'. "
                    "This completely invalidates your benchmark results."
                ),
                scientific_impact=(
                    "Your model has seen the test data during training. Any reported "
                    "accuracy/performance metrics are meaningless. This is the most "
                    "common form of scientific fraud in ML (often unintentional)."
                ),
                recommendation=(
                    "Ensure complete separation of test data. Use sklearn's train_test_split "
                    "or similar and verify test indices never appear in training loops."
                ),
            )

        # Test data in hyperparameter tuning
        if taint.level == TaintLevel.TEST and context in [
            "tune",
            "hyperparameter",
            "grid_search",
            "optuna",
        ]:
            return LeakageViolation(
                violation_type="test_in_tuning",
                severity="critical",
                line=line,
                col=0,
                tainted_variable=variable,
                taint_source=f"Line {taint.line}",
                contaminated_context=context,
                description=(
                    f"Test data '{variable}' is being used for hyperparameter tuning. "
                    "This causes 'double dipping' - your hyperparameters are optimized for the test set."
                ),
                scientific_impact=(
                    "Hyperparameters selected using test data will overfit to the test set. "
                    "Your generalization claims are invalid."
                ),
                recommendation=(
                    "Use a three-way split: train/validation/test. Tune on validation, "
                    "evaluate ONCE on test. Never iterate based on test performance."
                ),
            )

        # Mixed data is always a violation
        if taint.level == TaintLevel.MIXED:
            return LeakageViolation(
                violation_type="data_contamination",
                severity="critical",
                line=line,
                col=0,
                tainted_variable=variable,
                taint_source=f"Line {taint.line}",
                contaminated_context=context,
                description=(
                    f"Variable '{variable}' contains mixed train and test data. "
                    "The data splits have been contaminated."
                ),
                scientific_impact=(
                    "It is no longer possible to determine which data was used for "
                    "training vs evaluation. All results from this code are suspect."
                ),
                recommendation=(
                    "Trace back data flow and find where train/test data was combined. "
                    "Rebuild data pipeline with clear separation."
                ),
            )

        return None


class TaintAnalyzer(ast.NodeVisitor):
    """
    AST-based taint analysis for ML data leakage detection.
    """

    # Functions that load data
    DATA_LOADERS = {
        "load_dataset",
        "read_csv",
        "read_parquet",
        "load_data",
        "fetch_openml",
        "load_iris",
        "load_mnist",
        "load_cifar10",
        "ImageFolder",
        "DataLoader",
        "TensorDataset",
    }

    # Functions that split data
    DATA_SPLITTERS = {
        "train_test_split": ["X_train", "X_test", "y_train", "y_test"],
        "split": ["train", "test"],
        "random_split": ["train_dataset", "test_dataset"],
        "kfold": ["train_idx", "test_idx"],
    }

    # Training-related contexts
    TRAINING_CONTEXTS = {
        "fit",
        "train",
        "training_step",
        "train_epoch",
        "backward",
        "step",
        "optimize",
        "Trainer",  # HuggingFace Trainer
    }

    # Hyperparameter tuning contexts
    TUNING_CONTEXTS = {
        "tune",
        "hyperparameter_search",
        "grid_search",
        "random_search",
        "optuna",
        "ray_tune",
        "hyperopt",
        "cross_val_score",
    }

    # Operations that compute statistics from data (potential pre-split leakage)
    STAT_METHODS = {
        "mean",
        "std",
        "var",
        "fit",
        "fit_transform",
        "min",
        "max",
        "sum",
        "median",
        "mode",
    }

    def __init__(self) -> None:
        self.tracker = DataFlowTracker()
        self.violations: List[LeakageViolation] = []
        self.current_function: Optional[str] = None
        self.current_context: Optional[str] = None
        self.loop_vars: Set[str] = set()
        # Track pre-split data for leakage detection
        self.unsplit_sources: Set[str] = set()  # Variables from raw loaded data
        self.presplit_derivations: Dict[str, int] = {}  # var -> line where derived
        self.split_line: Optional[int] = None  # Line where split occurs

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track function context."""
        old_function = self.current_function
        old_context = self.current_context

        self.current_function = node.name

        # Treat function parameters as unsplit data sources until a split is seen.
        existing_unsplit = set(self.unsplit_sources)
        new_param_sources: Set[str] = set()
        for arg_node in (
            list(node.args.args)
            + list(getattr(node.args, "posonlyargs", []))
            + list(node.args.kwonlyargs)
        ):
            if arg_node.arg not in existing_unsplit:
                self.unsplit_sources.add(arg_node.arg)
                new_param_sources.add(arg_node.arg)
        if node.args.vararg and node.args.vararg.arg not in existing_unsplit:
            self.unsplit_sources.add(node.args.vararg.arg)
            new_param_sources.add(node.args.vararg.arg)
        if node.args.kwarg and node.args.kwarg.arg not in existing_unsplit:
            self.unsplit_sources.add(node.args.kwarg.arg)
            new_param_sources.add(node.args.kwarg.arg)

        # Determine context type
        name_lower = node.name.lower()
        if any(train in name_lower for train in self.TRAINING_CONTEXTS):
            self.current_context = "train"
        elif any(tune in name_lower for tune in self.TUNING_CONTEXTS):
            self.current_context = "tune"
        else:
            self.current_context = None

        self.generic_visit(node)

        # Remove temporary parameter sources to avoid leaking across functions
        for param in new_param_sources:
            self.unsplit_sources.discard(param)

        self.current_function = old_function
        self.current_context = old_context

    # Functions that are safe to receive any data (pure operations)
    SAFE_FUNCTIONS = {
        "print",
        "len",
        "type",
        "isinstance",
        "str",
        "repr",
        "shape",
        "dtype",
        "size",
        "ndim",  # Array introspection
        "save",
        "savefig",
        "to_csv",
        "to_parquet",  # Output operations
    }

    def visit_Call(self, node: ast.Call) -> None:
        """Track data loading and splitting operations."""
        func_name = self._get_func_name(node)

        if func_name:
            # Data loading
            if func_name in self.DATA_LOADERS:
                self._handle_data_load(node, func_name)

            # Data splitting
            if func_name in self.DATA_SPLITTERS:
                self._handle_data_split(node, func_name)

            # Check for fit/train calls with potentially tainted data
            # Also check constructors like Trainer()
            if func_name in self.TRAINING_CONTEXTS:
                self._check_training_call(node, func_name)

            # Check for tuning calls
            if func_name in self.TUNING_CONTEXTS:
                self._check_tuning_call(node, func_name)

            # Interprocedural check: warn when test data is passed to unknown functions
            # This catches helper functions like run_experiment(X_test)
            if (
                func_name not in self.DATA_LOADERS
                and func_name not in self.DATA_SPLITTERS
                and func_name not in self.SAFE_FUNCTIONS
            ):
                self._check_interprocedural_leakage(node, func_name)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Track assignments for taint propagation."""
        # Collect source variables from the right side
        sources = self._extract_variables(node.value)

        # Track derivations from unsplit data (before split occurs)
        if self.split_line is None:  # Haven't seen split yet
            for src in sources:
                if src in self.unsplit_sources:
                    # This assignment derives from unsplit data
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.presplit_derivations[target.id] = node.lineno
                            # Also mark as unsplit source for transitive tracking
                            self.unsplit_sources.add(target.id)
                        elif isinstance(target, ast.Tuple):
                            for elt in target.elts:
                                if isinstance(elt, ast.Name):
                                    self.presplit_derivations[elt.id] = node.lineno
                                    self.unsplit_sources.add(elt.id)
                    break

        # Propagate to targets
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.tracker.propagate(target.id, sources, node.lineno)
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.tracker.propagate(elt.id, sources, node.lineno)

        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """Track for loop iteration variables."""
        if isinstance(node.target, ast.Name):
            self.loop_vars.add(node.target.id)

            # Check if iterating over tainted data in wrong context
            iter_vars = self._extract_variables(node.iter)
            for var in iter_vars:
                if self.current_context:
                    violation = self.tracker.check_violation(var, self.current_context, node.lineno)
                    if violation:
                        self.violations.append(violation)

        self.generic_visit(node)

    def _get_func_name(self, node: ast.Call) -> Optional[str]:
        """Extract function name from call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

    def _handle_data_load(self, node: ast.Call, func_name: str) -> None:
        """Handle data loading function calls."""
        # Register loaded data as unsplit source for pre-split tracking
        parent = getattr(node, "_parent", None)
        if parent and isinstance(parent, ast.Assign):
            for target in parent.targets:
                if isinstance(target, ast.Name):
                    self.unsplit_sources.add(target.id)
                elif isinstance(target, ast.Tuple):
                    for elt in target.elts:
                        if isinstance(elt, ast.Name):
                            self.unsplit_sources.add(elt.id)

        # Check if this is a test/train split load
        for keyword in node.keywords:
            if keyword.arg == "split":
                if isinstance(keyword.value, ast.Constant):
                    split_name = keyword.value.value
                    if "test" in str(split_name).lower():
                        self._register_test_source(node, func_name)
                    elif "train" in str(split_name).lower():
                        self._register_train_source(node, func_name)

    def _handle_data_split(self, node: ast.Call, func_name: str) -> None:
        """Handle data splitting function calls."""
        # Record split line for pre-split tracking
        if self.split_line is None:
            self.split_line = node.lineno
            # Check for pre-split derivations that should be flagged
            self._check_presplit_contamination(node.lineno)

        # train_test_split typically returns (train, test) pairs
        parent = getattr(node, "_parent", None)
        if parent and isinstance(parent, ast.Assign):
            targets = parent.targets[0]
            if isinstance(targets, ast.Tuple):
                elts = targets.elts
                expected_outputs = self.DATA_SPLITTERS.get(func_name, [])

                for i, elt in enumerate(elts):
                    if isinstance(elt, ast.Name):
                        name = elt.id
                        name_lower = name.lower()

                        # Infer taint from variable name
                        if "test" in name_lower:
                            self.tracker.add_source(name, TaintLevel.TEST, node.lineno, 0, "split")
                        elif "train" in name_lower:
                            self.tracker.add_source(name, TaintLevel.TRAIN, node.lineno, 0, "split")
                        elif "val" in name_lower:
                            self.tracker.add_source(
                                name, TaintLevel.VALIDATION, node.lineno, 0, "split"
                            )

    def _check_training_call(self, node: ast.Call, func_name: str) -> None:
        """Check if training call uses test data."""
        # Check all arguments
        for arg in node.args:
            vars_used = self._extract_variables(arg)
            for var in vars_used:
                violation = self.tracker.check_violation(var, "train", node.lineno)
                if violation:
                    self.violations.append(violation)

        for keyword in node.keywords:
            vars_used = self._extract_variables(keyword.value)
            for var in vars_used:
                violation = self.tracker.check_violation(var, "train", node.lineno)
                if violation:
                    self.violations.append(violation)

    def _check_tuning_call(self, node: ast.Call, func_name: str) -> None:
        """Check if hyperparameter tuning uses test data."""
        for arg in node.args:
            vars_used = self._extract_variables(arg)
            for var in vars_used:
                violation = self.tracker.check_violation(var, "tune", node.lineno)
                if violation:
                    self.violations.append(violation)

    def _check_interprocedural_leakage(self, node: ast.Call, func_name: str) -> None:
        """Check if test data is passed to unknown functions.

        This catches patterns like:
            def run_experiment(data): model.fit(data, y)
            run_experiment(X_test)  # Leakage hidden in helper!
        """
        for arg in node.args:
            vars_used = self._extract_variables(arg)
            for var in vars_used:
                taint = self.tracker.get_taint(var)
                if taint and taint.level == TaintLevel.TEST:
                    self.violations.append(
                        LeakageViolation(
                            violation_type="test_data_to_function",
                            severity="warning",
                            line=node.lineno,
                            col=node.col_offset,
                            tainted_variable=var,
                            taint_source=f"Line {taint.line}",
                            contaminated_context=func_name,
                            description=(
                                f"Test data '{var}' is passed to function '{func_name}()'. "
                                f"If this function uses the data for training, your benchmark is invalid."
                            ),
                            scientific_impact=(
                                "Test data passed to helper functions may be used for training "
                                "without explicit detection. Audit the called function."
                            ),
                            recommendation=(
                                f"Verify that '{func_name}()' does not use '{var}' for training. "
                                f"If it does, pass only training data to this function."
                            ),
                        )
                    )

        # Also check keyword arguments
        for keyword in node.keywords:
            vars_used = self._extract_variables(keyword.value)
            for var in vars_used:
                taint = self.tracker.get_taint(var)
                if taint and taint.level == TaintLevel.TEST:
                    self.violations.append(
                        LeakageViolation(
                            violation_type="test_data_to_function",
                            severity="warning",
                            line=node.lineno,
                            col=node.col_offset,
                            tainted_variable=var,
                            taint_source=f"Line {taint.line}",
                            contaminated_context=func_name,
                            description=(
                                f"Test data '{var}' is passed to function '{func_name}()' "
                                f"via keyword argument '{keyword.arg}'. "
                                f"If this function uses the data for training, your benchmark is invalid."
                            ),
                            scientific_impact=(
                                "Test data passed to helper functions may be used for training "
                                "without explicit detection. Audit the called function."
                            ),
                            recommendation=(
                                f"Verify that '{func_name}()' does not use '{var}' for training. "
                                f"If it does, pass only training data to this function."
                            ),
                        )
                    )

    def _register_test_source(self, node: ast.Call, func_name: str) -> None:
        """Register a test data source."""
        parent = getattr(node, "_parent", None)
        if parent and isinstance(parent, ast.Assign):
            for target in parent.targets:
                if isinstance(target, ast.Name):
                    self.tracker.add_source(target.id, TaintLevel.TEST, node.lineno, 0, "load")

    def _register_train_source(self, node: ast.Call, func_name: str) -> None:
        """Register a train data source."""
        parent = getattr(node, "_parent", None)
        if parent and isinstance(parent, ast.Assign):
            for target in parent.targets:
                if isinstance(target, ast.Name):
                    self.tracker.add_source(target.id, TaintLevel.TRAIN, node.lineno, 0, "load")

    def _extract_variables(self, node: ast.AST) -> List[str]:
        """Extract all variable names from an AST node."""
        variables = []

        if isinstance(node, ast.Name):
            variables.append(node.id)
        elif isinstance(node, ast.Subscript):
            variables.extend(self._extract_variables(node.value))
        elif isinstance(node, ast.Attribute):
            variables.extend(self._extract_variables(node.value))
        elif isinstance(node, ast.Call):
            for arg in node.args:
                variables.extend(self._extract_variables(arg))
            for kw in node.keywords:
                variables.extend(self._extract_variables(kw.value))
        elif isinstance(node, ast.BinOp):
            variables.extend(self._extract_variables(node.left))
            variables.extend(self._extract_variables(node.right))
        elif isinstance(node, ast.List) or isinstance(node, ast.Tuple):
            for elt in node.elts:
                variables.extend(self._extract_variables(elt))

        return variables

    def _check_presplit_contamination(self, split_line: int) -> None:
        """Check for variables derived from unsplit data before the split.

        This catches patterns like:
            mu = X.mean(0)  # Computed on full dataset
            X_train, X_test = train_test_split(X)
            X_train_centered = X_train - mu  # mu contains test info!
        """
        for var_name, derivation_line in self.presplit_derivations.items():
            if derivation_line < split_line:
                # Mark this variable as potentially contaminated
                self.tracker.add_source(
                    var_name, TaintLevel.MIXED, derivation_line, 0, "presplit_derivation"
                )
                self.violations.append(
                    LeakageViolation(
                        violation_type="presplit_statistics",
                        severity="warning",
                        line=derivation_line,
                        col=0,
                        tainted_variable=var_name,
                        taint_source="unsplit_data",
                        contaminated_context="preprocessing",
                        description=(
                            f"Variable '{var_name}' is computed from the full dataset on line "
                            f"{derivation_line}, before train_test_split on line {split_line}. "
                            f"This statistic contains information from both train and test data."
                        ),
                        scientific_impact=(
                            "Pre-split statistics leak test information into training. "
                            "Any model using these statistics has implicitly seen the test set."
                        ),
                        recommendation=(
                            "Compute statistics AFTER splitting, using only training data:\n"
                            "  X_train, X_test = train_test_split(X)\n"
                            "  mu = X_train.mean(0)  # Only from training data"
                        ),
                    )
                )


class LeakageHunter:
    """
    Main interface for data leakage detection.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.analyzer: Optional[TaintAnalyzer] = None

    def analyze(self, source: str) -> Dict[str, Any]:
        """
        Analyze source code for data leakage.

        Args:
            source: Python source code string

        Returns:
            Dictionary containing analysis results
        """
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return {
                "error": f"Syntax error: {e}",
                "violations": [],
                "taint_map": {},
                "summary": None,
            }

        # Add parent references for context
        self._add_parent_refs(tree)

        # Run analysis
        self.analyzer = TaintAnalyzer()
        self.analyzer.visit(tree)

        # Also run pattern-based detection for common leakage patterns
        pattern_violations = self._pattern_based_detection(source)

        all_violations = self.analyzer.violations + pattern_violations

        # Generate summary
        summary = self._generate_summary(all_violations)

        return {
            "violations": [self._violation_to_dict(v) for v in all_violations],
            "taint_map": {
                name: {"level": src.level.value, "line": src.line}
                for name, src in self.analyzer.tracker.taint_map.items()
            },
            "summary": summary,
        }

    def _add_parent_refs(self, tree: ast.AST) -> None:
        """Add parent references to all AST nodes."""
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                child_any = cast(Any, child)
                child_any._parent = parent

    def _pattern_based_detection(self, source: str) -> List[LeakageViolation]:
        """Detect common leakage patterns using regex."""
        violations = []
        lines = source.split("\n")

        # Pattern 1: fit_transform on full data, then split
        fit_transform_pattern = re.compile(r"\.fit_transform\s*\(\s*(\w+)")
        split_pattern = re.compile(r"train_test_split")
        cross_val_pattern = re.compile(r"cross_val_score\s*\(")

        fit_transform_line = None
        fit_transform_var = None

        for i, line in enumerate(lines, 1):
            match = fit_transform_pattern.search(line)
            if match:
                fit_transform_line = i
                fit_transform_var = match.group(1)

            if fit_transform_line:
                # Check for split AFTER fit_transform
                if split_pattern.search(line) and i > fit_transform_line:
                    violations.append(
                        LeakageViolation(
                            violation_type="preprocessing_leakage",
                            severity="critical",
                            line=fit_transform_line,
                            col=0,
                            tainted_variable=fit_transform_var or "unknown",
                            taint_source="fit_transform",
                            contaminated_context="preprocessing",
                            description=(
                                f"fit_transform() called on line {fit_transform_line} BEFORE "
                                f"train_test_split on line {i}. Preprocessing statistics "
                                "(mean, std, etc.) are computed using test data."
                            ),
                            scientific_impact=(
                                "Preprocessing learns from test data. Features are scaled/normalized "
                                "using information that should be held out. This is subtle but "
                                "causes overestimation of model performance."
                            ),
                            recommendation=(
                                "Split data FIRST, then fit preprocessing on train only:\n"
                                "  X_train, X_test = train_test_split(X)\n"
                                "  scaler.fit(X_train)\n"
                                "  X_train = scaler.transform(X_train)\n"
                                "  X_test = scaler.transform(X_test)"
                            ),
                        )
                    )
                    fit_transform_line = None  # Reset

                # Check for cross_val_score AFTER fit_transform
                elif cross_val_pattern.search(line) and i > fit_transform_line:
                    violations.append(
                        LeakageViolation(
                            violation_type="preprocessing_leakage",
                            severity="critical",
                            line=fit_transform_line,
                            col=0,
                            tainted_variable=fit_transform_var or "unknown",
                            taint_source="fit_transform",
                            contaminated_context="cross_validation",
                            description=(
                                f"fit_transform() called on line {fit_transform_line} BEFORE "
                                f"cross_val_score on line {i}. Feature selection or scaling "
                                "must happen INSIDE the CV loop."
                            ),
                            scientific_impact="CV folds are contaminated with global statistics.",
                            recommendation="Use sklearn Pipeline for CV.",
                        )
                    )
                    fit_transform_line = None

        # Pattern 2: cross_val_score after target encoding/feature selection
        target_encoding_pattern = re.compile(r"(TargetEncoder|target_encode|WOEEncoder)\s*\(")
        cross_val_pattern = re.compile(r"cross_val_score\s*\(")

        for i, line in enumerate(lines, 1):
            if target_encoding_pattern.search(line):
                # Look for cross_val later
                for j, later_line in enumerate(lines[i:], i + 1):
                    if cross_val_pattern.search(later_line):
                        violations.append(
                            LeakageViolation(
                                violation_type="target_leakage",
                                severity="critical",
                                line=i,
                                col=0,
                                tainted_variable="encoded_features",
                                taint_source="target_encoding",
                                contaminated_context="cross_validation",
                                description=(
                                    f"Target encoding on line {i} before cross_val_score on line {j}. "
                                    "Target encoding MUST happen inside each CV fold."
                                ),
                                scientific_impact=(
                                    "Target encoding uses target values to create features. "
                                    "If done before CV, validation folds see encoded values "
                                    "computed from their own targets."
                                ),
                                recommendation=(
                                    "Use sklearn Pipeline to ensure encoding happens per-fold:\n"
                                    "  pipe = Pipeline([('encoder', TargetEncoder()), ('model', clf)])\n"
                                    "  cross_val_score(pipe, X, y)"
                                ),
                            )
                        )
                        break

        return violations

    def _generate_summary(self, violations: List[LeakageViolation]) -> Dict[str, Any]:
        """Generate analysis summary."""
        critical = sum(1 for v in violations if v.severity == "critical")
        warning = sum(1 for v in violations if v.severity == "warning")

        violation_types: Dict[str, int] = {}
        for v in violations:
            violation_types[v.violation_type] = violation_types.get(v.violation_type, 0) + 1

        if critical > 0:
            verdict = "FAIL: Critical data leakage detected. Results are invalid."
        elif warning > 0:
            verdict = "WARNING: Potential data leakage patterns detected."
        else:
            verdict = "PASS: No data leakage detected."

        return {
            "total_violations": len(violations),
            "critical_count": critical,
            "warning_count": warning,
            "violation_types": violation_types,
            "verdict": verdict,
        }

    def _violation_to_dict(self, v: LeakageViolation) -> Dict[str, Any]:
        """Convert violation to dictionary."""
        confidence = "high" if v.severity == "critical" else "medium"
        return {
            "type": v.violation_type,
            "severity": v.severity,
            "line": v.line,
            "col": v.col,
            "variable": v.tainted_variable,
            "source": v.taint_source,
            "context": v.contaminated_context,
            "description": v.description,
            "scientific_impact": v.scientific_impact,
            "recommendation": v.recommendation,
            "confidence": confidence,
            "blocking": confidence == "high",
        }

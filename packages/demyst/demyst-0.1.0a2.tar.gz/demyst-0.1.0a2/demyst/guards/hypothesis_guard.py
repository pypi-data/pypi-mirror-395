"""
HypothesisGuard: Anti-P-Hacking and Statistical Validity

Detects and prevents:
    1. Cherry-picking: Running many experiments, reporting the best
    2. P-hacking: Adjusting analysis until p < 0.05
    3. HARKing: Hypothesizing After Results are Known
    4. Multiple comparisons: Failing to correct for multiple tests

Philosophy: "If you ran 100 experiments, you need to report 100 experiments."
"""

import ast
import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, cast


class StatisticalRisk(Enum):
    """Risk levels for statistical validity issues."""

    VALID = "valid"
    QUESTIONABLE = "questionable"
    INVALID = "invalid"
    FRAUDULENT = "fraudulent"


@dataclass
class ExperimentRecord:
    """Record of a single experiment run."""

    experiment_id: str
    timestamp: str
    hyperparameters: Dict[str, Any]
    seed: int
    metric_name: str
    metric_value: float
    p_value: Optional[float]
    code_hash: str


@dataclass
class StatisticalViolation:
    """Represents a statistical validity violation."""

    violation_type: str
    severity: StatisticalRisk
    line: int
    description: str
    statistical_impact: str
    corrected_interpretation: str
    recommendation: str
    confidence: str = "medium"


@dataclass
class CorrectedResult:
    """Result after applying proper statistical corrections."""

    original_p_value: float
    corrected_p_value: float
    correction_method: str
    num_comparisons: int
    is_significant: bool
    explanation: str


@dataclass
class LoopContext:
    """Tracks behavior inside a single loop for p-hacking analysis."""

    tests: List[Dict[str, Any]] = field(default_factory=list)
    accumulates_results: bool = False
    significance_exits: List[int] = field(default_factory=list)


class BonferroniCorrector:
    """
    Applies Bonferroni and other multiple comparison corrections.

    The Bonferroni correction is conservative but ensures family-wise
    error rate (FWER) is controlled at the specified alpha level.
    """

    @staticmethod
    def bonferroni(p_value: float, num_comparisons: int, alpha: float = 0.05) -> CorrectedResult:
        """
        Apply Bonferroni correction.

        The corrected p-value is: p_corrected = p * n
        Alternatively, compare to corrected alpha: alpha / n
        """
        corrected_p = min(p_value * num_comparisons, 1.0)
        corrected_alpha = alpha / num_comparisons

        return CorrectedResult(
            original_p_value=p_value,
            corrected_p_value=corrected_p,
            correction_method="bonferroni",
            num_comparisons=num_comparisons,
            is_significant=corrected_p < alpha,
            explanation=(
                f"Original p={p_value:.4f} with {num_comparisons} comparisons. "
                f"Bonferroni-corrected p={corrected_p:.4f}. "
                f"{'SIGNIFICANT' if corrected_p < alpha else 'NOT SIGNIFICANT'} "
                f"at alpha={alpha}."
            ),
        )

    @staticmethod
    def holm_bonferroni(p_values: List[float], alpha: float = 0.05) -> List[CorrectedResult]:
        """
        Apply Holm-Bonferroni step-down procedure.

        Less conservative than Bonferroni while still controlling FWER.
        """
        n = len(p_values)
        indexed = [(p, i) for i, p in enumerate(p_values)]
        sorted_p = sorted(indexed)

        results: List[Optional[CorrectedResult]] = [None] * n
        rejected_any = False

        for rank, (p, original_idx) in enumerate(sorted_p):
            adjusted_alpha = alpha / (n - rank)
            corrected_p = min(p * (n - rank), 1.0)

            # Holm's procedure: if we fail to reject at any step, stop rejecting
            if not rejected_any and p <= adjusted_alpha:
                is_significant = True
            else:
                if p > adjusted_alpha:
                    rejected_any = True
                is_significant = False

            results[original_idx] = CorrectedResult(
                original_p_value=p,
                corrected_p_value=corrected_p,
                correction_method="holm-bonferroni",
                num_comparisons=n,
                is_significant=is_significant,
                explanation=(
                    f"Rank {rank+1}/{n}: p={p:.4f}, adjusted alpha={adjusted_alpha:.4f}. "
                    f"{'SIGNIFICANT' if is_significant else 'NOT SIGNIFICANT'}."
                ),
            )

        return cast(List[CorrectedResult], results)

    @staticmethod
    def benjamini_hochberg(p_values: List[float], alpha: float = 0.05) -> List[CorrectedResult]:
        """
        Apply Benjamini-Hochberg FDR control.

        Controls False Discovery Rate instead of FWER.
        More powerful than Bonferroni for large numbers of tests.
        """
        n = len(p_values)
        indexed = [(p, i) for i, p in enumerate(p_values)]
        sorted_p = sorted(indexed)

        results: List[Optional[CorrectedResult]] = [None] * n
        max_significant_rank = 0

        # Find largest k where p(k) <= k/n * alpha
        for rank, (p, original_idx) in enumerate(sorted_p, 1):
            threshold = (rank / n) * alpha
            if p <= threshold:
                max_significant_rank = rank

        # All tests with rank <= max_significant_rank are significant
        for rank, (p, original_idx) in enumerate(sorted_p, 1):
            corrected_p = min((n / rank) * p, 1.0)

            results[original_idx] = CorrectedResult(
                original_p_value=p,
                corrected_p_value=corrected_p,
                correction_method="benjamini-hochberg",
                num_comparisons=n,
                is_significant=rank <= max_significant_rank,
                explanation=(
                    f"Rank {rank}/{n}: p={p:.4f}, FDR threshold={(rank/n)*alpha:.4f}. "
                    f"{'SIGNIFICANT' if rank <= max_significant_rank else 'NOT SIGNIFICANT'}."
                ),
            )

        return cast(List[CorrectedResult], results)


class ExperimentTracker:
    """
    Tracks all experiments run to detect cherry-picking and p-hacking.

    Integration points:
        - WandB: Reads wandb run history
        - MLflow: Reads mlflow experiment data
        - Local: Tracks experiments in JSON files
    """

    def __init__(self, storage_path: Optional[str] = None) -> None:
        self.storage_path = storage_path or ".demyst_experiments.json"
        self.experiments: List[ExperimentRecord] = []
        self.code_hashes: Set[str] = set()
        self._load_history()

    def _load_history(self) -> None:
        """Load experiment history from storage."""
        try:
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                self.experiments = [ExperimentRecord(**exp) for exp in data.get("experiments", [])]
                self.code_hashes = set(data.get("code_hashes", []))
        except FileNotFoundError:
            self.experiments = []
            self.code_hashes = set()

    def _save_history(self) -> None:
        """Save experiment history to storage."""
        data = {
            "experiments": [
                {
                    "experiment_id": e.experiment_id,
                    "timestamp": e.timestamp,
                    "hyperparameters": e.hyperparameters,
                    "seed": e.seed,
                    "metric_name": e.metric_name,
                    "metric_value": e.metric_value,
                    "p_value": e.p_value,
                    "code_hash": e.code_hash,
                }
                for e in self.experiments
            ],
            "code_hashes": list(self.code_hashes),
        }
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2)

    def record_experiment(
        self,
        hyperparameters: Dict[str, Any],
        seed: int,
        metric_name: str,
        metric_value: float,
        p_value: Optional[float] = None,
        code: Optional[str] = None,
    ) -> ExperimentRecord:
        """Record a new experiment."""
        code_hash = hashlib.sha256(code.encode()).hexdigest()[:16] if code else "unknown"

        record = ExperimentRecord(
            experiment_id=hashlib.sha256(
                f"{datetime.now().isoformat()}{seed}{metric_value}".encode()
            ).hexdigest()[:16],
            timestamp=datetime.now().isoformat(),
            hyperparameters=hyperparameters,
            seed=seed,
            metric_name=metric_name,
            metric_value=metric_value,
            p_value=p_value,
            code_hash=code_hash,
        )

        self.experiments.append(record)
        self.code_hashes.add(code_hash)
        self._save_history()

        return record

    def get_experiment_count(
        self, code_hash: Optional[str] = None, metric_name: Optional[str] = None
    ) -> int:
        """Get count of experiments matching criteria."""
        filtered = self.experiments

        if code_hash:
            filtered = [e for e in filtered if e.code_hash == code_hash]

        if metric_name:
            filtered = [e for e in filtered if e.metric_name == metric_name]

        return len(filtered)

    def get_seeds_used(self, code_hash: Optional[str] = None) -> List[int]:
        """Get all seeds used in experiments."""
        filtered = self.experiments

        if code_hash:
            filtered = [e for e in filtered if e.code_hash == code_hash]

        return [e.seed for e in filtered]

    def analyze_reporting_bias(self, reported_result: float, metric_name: str) -> Dict[str, Any]:
        """
        Analyze if a reported result shows signs of cherry-picking.

        Checks:
            1. Is this the best result among all runs?
            2. How many experiments were run?
            3. What's the probability of seeing this by chance?
        """
        relevant = [e for e in self.experiments if e.metric_name == metric_name]

        if not relevant:
            return {"warning": "No experiment history found", "experiments_tracked": 0}

        values = [e.metric_value for e in relevant]
        n = len(values)

        # Calculate rank of reported result
        sorted_values = sorted(values, reverse=True)  # Assuming higher is better
        try:
            rank = sorted_values.index(reported_result) + 1
        except ValueError:
            rank = None

        # Calculate probability of seeing this or better by chance
        mean_val = sum(values) / n
        std_val = (sum((v - mean_val) ** 2 for v in values) / n) ** 0.5 if n > 1 else 0

        # If reporting the best result out of n, the probability is 1/n
        cherry_pick_probability = 1.0 / n if rank == 1 else None

        return {
            "experiments_run": n,
            "reported_value": reported_result,
            "rank": rank,
            "is_best": rank == 1,
            "mean_across_runs": mean_val,
            "std_across_runs": std_val,
            "cherry_pick_probability": cherry_pick_probability,
            "bonferroni_factor": n,
            "seeds_used": self.get_seeds_used(),
        }


# Physics sigma thresholds (sigma -> p-value, one-sided)
# In particle physics, 5-sigma is standard for discovery, 3-sigma for evidence
SIGMA_TO_PVALUE = {
    5.0: 2.87e-7,  # 5-sigma discovery threshold
    4.0: 3.17e-5,  # 4-sigma
    3.0: 0.00135,  # 3-sigma evidence threshold (one-sided: 0.00135)
    2.0: 0.0228,  # 2-sigma (one-sided: 0.0228)
    1.0: 0.159,  # 1-sigma
}


class HypothesisAnalyzer(ast.NodeVisitor):
    """
    AST analyzer for detecting p-hacking patterns in code.

    Detects:
        1. Multiple t-tests without correction
        2. Loops over different parameters with significance testing
        3. Conditional reporting based on p-values

    Config options:
        physics_mode: bool - Use physics sigma thresholds instead of p<0.05
        discovery_sigma: float - Sigma threshold for discovery (default 5.0)
        evidence_sigma: float - Sigma threshold for evidence (default 3.0)
    """

    P_VALUE_FUNCTIONS = {
        "ttest_ind",
        "ttest_rel",
        "ttest_1samp",
        "mannwhitneyu",
        "wilcoxon",
        "kruskal",
        "chi2_contingency",
        "fisher_exact",
        "pearsonr",
        "spearmanr",
        "kendalltau",
        "f_oneway",
        "anova",
        "anova_lm",
        "ranksums",
        "sf",  # Survival function (often used for p-value)
        "cdf",  # CDF (often used for p-value)
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.violations: List[StatisticalViolation] = []
        self.statistical_tests: List[Dict[str, Any]] = []
        self.current_function: Optional[str] = None
        self.in_loop: bool = False
        self.loop_depth: int = 0
        self.loop_stack: List[LoopContext] = []

        # Physics mode settings
        self.physics_mode = self.config.get("physics_mode", False)
        self.discovery_sigma = self.config.get("discovery_sigma", 5.0)
        self.evidence_sigma = self.config.get("evidence_sigma", 3.0)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track function context."""
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function

    def visit_For(self, node: ast.For) -> None:
        """Track loop context."""
        old_in_loop = self.in_loop
        self.in_loop = True
        self.loop_depth += 1
        # Push loop context
        self.loop_stack.append(LoopContext())
        self.generic_visit(node)
        ctx = self.loop_stack.pop()
        self._evaluate_loop_context(ctx, node)
        self.loop_depth -= 1
        self.in_loop = old_in_loop if self.loop_depth == 0 else True

    def visit_While(self, node: ast.While) -> None:
        """Track while loop context and detect optional stopping patterns."""
        # Check if loop condition is based on p-value threshold (optional stopping)
        if self._is_p_value_check(node.test):
            self.violations.append(
                StatisticalViolation(
                    violation_type="optional_stopping_while_loop",
                    severity=StatisticalRisk.INVALID,
                    line=node.lineno,
                    description=(
                        "While loop condition based on p-value threshold. "
                        "This implements optional stopping - continuing to collect data "
                        "until significance is achieved."
                    ),
                    statistical_impact=(
                        "Optional stopping inflates false positive rate and biases estimates. "
                        "Type I error rate is not controlled when stopping decisions depend on data."
                    ),
                    corrected_interpretation=(
                        "Specify maximum iterations beforehand with pre-registered stopping rules. "
                        "Do not condition loop termination on statistical significance."
                    ),
                    recommendation=(
                        "Replace p-value-dependent while loops with fixed iteration counts. "
                        "Use 'for i in range(max_iterations):' and aggregate results with "
                        "Bonferroni/FDR correction after all iterations complete."
                    ),
                    confidence="high",
                )
            )

        old_in_loop = self.in_loop
        self.in_loop = True
        self.loop_depth += 1
        self.loop_stack.append(LoopContext())
        self.generic_visit(node)
        ctx = self.loop_stack.pop()
        self._evaluate_loop_context(ctx, node)
        self.loop_depth -= 1
        self.in_loop = old_in_loop if self.loop_depth == 0 else True

    def visit_Call(self, node: ast.Call) -> None:
        """Detect statistical test calls."""
        func_name = self._get_func_name(node)

        if func_name and func_name in self.P_VALUE_FUNCTIONS:
            test_info = {
                "function": func_name,
                "line": node.lineno,
                "in_loop": self.in_loop,
                "containing_function": self.current_function,
            }
            self.statistical_tests.append(test_info)

            if self.loop_stack:
                self.loop_stack[-1].tests.append(test_info)

        # Detect accumulation into containers (Monte Carlo style)
        if isinstance(node.func, ast.Attribute) and node.func.attr in {"append", "extend"}:
            if isinstance(node.func.value, ast.Name) and self.loop_stack:
                self.loop_stack[-1].accumulates_results = True

        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Detect conditional logic based on p-values."""
        # Check for p < 0.05 patterns
        if self._is_p_value_check(node.test):
            if self.loop_stack and self._contains_early_exit_action(node):
                # Mark that this loop exits early on significance
                self.loop_stack[-1].significance_exits.append(node.lineno)

            # Keep a general conditional reporting notice (outside loop or non-early-exit)
            self.violations.append(
                StatisticalViolation(
                    violation_type="conditional_reporting",
                    severity=StatisticalRisk.QUESTIONABLE,
                    line=node.lineno,
                    description=(
                        "Conditional logic based on p-value detected. "
                        "This pattern enables selective reporting."
                    ),
                    statistical_impact=(
                        "Conditioning on significance leads to publication bias. "
                        "Non-significant results are equally important for science."
                    ),
                    corrected_interpretation=(
                        "Report ALL results regardless of significance. "
                        "Use pre-registration to prevent outcome-dependent analysis."
                    ),
                    recommendation=(
                        "Remove conditional branching on p-values. Report effect sizes "
                        "and confidence intervals instead of just significance."
                    ),
                )
            )

        self.generic_visit(node)

    def _get_func_name(self, node: ast.Call) -> Optional[str]:
        """Extract function name from call."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

    def _is_p_value_check(self, node: ast.AST) -> bool:
        """Check if node is a p-value comparison.

        In physics_mode, we don't flag comparisons against sigma thresholds
        (e.g., p < 2.87e-7 for 5-sigma) since these are legitimate rigorous
        standards, not p-hacking.
        """
        if isinstance(node, ast.Compare):
            # Look for patterns like: p < 0.05, pvalue < 0.05
            is_p_variable = False
            if isinstance(node.left, ast.Name):
                name = node.left.id.lower()
                # Match actual p-value variable names, not just any word containing "p"
                # Valid patterns: p, p_value, pvalue, p_val, pval, p_values, significance
                p_value_patterns = (
                    name == "p"
                    or name.startswith("p_")
                    or name.startswith("pval")
                    or name.endswith("_p")
                    or name.endswith("_pvalue")
                    or name.endswith("_pval")
                    or "p_value" in name
                    or "pvalue" in name
                    or "significance" in name
                )
                if p_value_patterns:
                    is_p_variable = True

            for comparator in node.comparators:
                if isinstance(comparator, ast.Constant):
                    threshold = comparator.value

                    # In physics mode, allow sigma-based thresholds
                    if self.physics_mode and isinstance(threshold, (int, float)):
                        # Check if threshold matches a physics sigma level
                        # Allow thresholds <= 3-sigma p-value (rigorous physics standards)
                        discovery_p = SIGMA_TO_PVALUE.get(self.discovery_sigma, 2.87e-7)
                        evidence_p = SIGMA_TO_PVALUE.get(self.evidence_sigma, 0.00135)

                        # If using a threshold at or below 3-sigma, it's rigorous physics
                        if threshold <= evidence_p:
                            return False  # Don't flag - this is valid physics rigor

                    # Common alpha values that indicate potential p-hacking
                    if threshold in [0.05, 0.01, 0.001, 0.1]:
                        return True

            # If it's a p-value variable comparison, flag it
            if is_p_variable:
                return True

        return False

    def _contains_early_exit_action(self, node: ast.If) -> bool:
        """Detects break/return/continue/raise or immediate reporting within a conditional."""

        def _is_reporting_call(call: ast.Call) -> bool:
            if isinstance(call.func, ast.Name) and call.func.id == "print":
                return True
            if isinstance(call.func, ast.Attribute):
                if isinstance(call.func.value, ast.Name) and call.func.value.id in {
                    "logger",
                    "log",
                }:
                    return call.func.attr in {
                        "info",
                        "warning",
                        "warn",
                        "error",
                        "critical",
                        "debug",
                    }
            return False

        for stmt in ast.walk(ast.Module(body=node.body, type_ignores=[])):
            if isinstance(stmt, (ast.Break, ast.Continue, ast.Return, ast.Raise)):
                return True
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if _is_reporting_call(stmt.value):
                    return True
        return False

    def _evaluate_loop_context(self, ctx: LoopContext, node: ast.AST) -> None:
        """Create violations based on loop behavior."""
        if not ctx.tests:
            return

        if ctx.significance_exits:
            self.violations.append(
                StatisticalViolation(
                    violation_type="selective_early_exit_on_significance",
                    severity=StatisticalRisk.INVALID,
                    line=ctx.significance_exits[0],
                    description=(
                        "Loop aborts or reports immediately when a p-value passes the threshold. "
                        "This is a classic p-hacking pattern."
                    ),
                    statistical_impact=(
                        "Early stopping on significance inflates false positives and biases estimates."
                    ),
                    corrected_interpretation="Remove early exits; collect all results and correct p-values after.",
                    recommendation=(
                        "Accumulate results, apply multiple-comparison correction after the loop, "
                        "and pre-register stopping rules."
                    ),
                    confidence="high",
                )
            )
            return

        if ctx.accumulates_results:
            # Monte Carlo / bootstrap style accumulation; do not flag
            return

        # Tests in loop without accumulation: still risky for multiple comparisons
        severity = StatisticalRisk.INVALID if len(ctx.tests) > 1 else StatisticalRisk.QUESTIONABLE
        self.violations.append(
            StatisticalViolation(
                violation_type="uncorrected_multiple_tests",
                severity=severity,
                line=ctx.tests[0]["line"],
                description=(
                    "Statistical tests executed inside a loop without aggregation or correction. "
                    "Treat repeated tests as multiple comparisons."
                ),
                statistical_impact=(
                    "Repeated testing inflates the false positive rate; alpha must be adjusted."
                ),
                corrected_interpretation=(
                    "Aggregate p-values or metrics and apply Bonferroni/Holm/FDR after the loop."
                ),
                recommendation=(
                    "Collect p-values in a list, then use statsmodels.stats.multitest.multipletests "
                    "or similar to correct."
                ),
                confidence="medium" if severity == StatisticalRisk.INVALID else "low",
            )
        )


class HypothesisGuard:
    """
    Main interface for hypothesis testing validity analysis.

    Features:
        1. Detects p-hacking patterns in code
        2. Tracks experiments to detect cherry-picking
        3. Automatically applies multiple comparison corrections
        4. Generates corrected statistical interpretations
    """

    def __init__(
        self, config: Optional[Dict[str, Any]] = None, experiment_storage: Optional[str] = None
    ) -> None:
        self.config = config or {}
        self.corrector = BonferroniCorrector()
        self.tracker = ExperimentTracker(experiment_storage)
        self.analyzer: Optional[HypothesisAnalyzer] = None

    def analyze_code(self, source: str) -> Dict[str, Any]:
        """
        Analyze source code for p-hacking patterns.

        Args:
            source: Python source code string

        Returns:
            Analysis results including violations and recommendations
        """
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return {"error": f"Syntax error: {e}", "violations": [], "summary": None}

        # Pass config to analyzer for physics mode support
        self.analyzer = HypothesisAnalyzer(config=self.config)
        self.analyzer.visit(tree)

        # Calculate required corrections
        num_tests = len(self.analyzer.statistical_tests)
        correction_info = None

        if num_tests > 1:
            correction_info = {
                "num_tests_detected": num_tests,
                "bonferroni_alpha": 0.05 / num_tests,
                "recommendation": (
                    f"Detected {num_tests} statistical tests. "
                    f"Use alpha = {0.05/num_tests:.4f} for significance, "
                    f"or apply FDR correction."
                ),
            }

        summary = self._generate_summary()

        return {
            "violations": [self._violation_to_dict(v) for v in self.analyzer.violations],
            "statistical_tests": self.analyzer.statistical_tests,
            "correction_info": correction_info,
            "summary": summary,
        }

    def correct_result(
        self, p_value: float, num_experiments: int, method: str = "bonferroni"
    ) -> CorrectedResult:
        """
        Apply correction to a reported p-value.

        Args:
            p_value: Original p-value
            num_experiments: Number of experiments/comparisons
            method: Correction method ('bonferroni', 'holm', 'fdr_bh')

        Returns:
            CorrectedResult with corrected p-value and interpretation
        """
        if method == "bonferroni":
            return self.corrector.bonferroni(p_value, num_experiments)
        elif method == "holm":
            return self.corrector.holm_bonferroni([p_value] * num_experiments)[0]
        elif method == "fdr_bh":
            return self.corrector.benjamini_hochberg([p_value] * num_experiments)[0]
        else:
            raise ValueError(f"Unknown correction method: {method}")

    def validate_reported_result(
        self, reported_p: float, reported_metric: float, metric_name: str
    ) -> Dict[str, Any]:
        """
        Validate a result claimed in a paper/report against experiment history.

        Args:
            reported_p: The reported p-value
            reported_metric: The reported metric value
            metric_name: Name of the metric

        Returns:
            Validation report with potential issues
        """
        # Analyze for cherry-picking
        bias_analysis = self.tracker.analyze_reporting_bias(reported_metric, metric_name)

        issues = []
        corrected_p = reported_p

        # Check if multiple experiments were run
        n_experiments = bias_analysis.get("experiments_run", 0)

        if n_experiments > 1:
            # Apply Bonferroni correction
            corrected = self.correct_result(reported_p, n_experiments)
            corrected_p = corrected.corrected_p_value

            if reported_p < 0.05 and corrected_p >= 0.05:
                issues.append(
                    {
                        "type": "significance_lost_after_correction",
                        "severity": "critical",
                        "description": (
                            f"You ran {n_experiments} experiments. Your p-value of {reported_p:.4f} "
                            f"becomes {corrected_p:.4f} after Bonferroni correction. "
                            f"Result is {'NOT ' if corrected_p >= 0.05 else ''}SIGNIFICANT."
                        ),
                    }
                )

            if bias_analysis.get("is_best", False):
                issues.append(
                    {
                        "type": "cherry_picking_detected",
                        "severity": "critical",
                        "description": (
                            f"The reported result (rank 1/{n_experiments}) is the best outcome. "
                            f"Probability of this by chance: {1/n_experiments:.2%}. "
                            f"This constitutes cherry-picking."
                        ),
                    }
                )

        verdict = "VALID" if not issues else "INVALID"

        return {
            "original_p_value": reported_p,
            "corrected_p_value": corrected_p,
            "experiments_analyzed": n_experiments,
            "issues": issues,
            "bias_analysis": bias_analysis,
            "verdict": verdict,
        }

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate analysis summary."""
        if not self.analyzer:
            return {"error": "No analysis performed"}

        violations = self.analyzer.violations
        invalid = sum(1 for v in violations if v.severity == StatisticalRisk.INVALID)
        questionable = sum(1 for v in violations if v.severity == StatisticalRisk.QUESTIONABLE)

        if invalid > 0:
            verdict = "FAIL: Invalid statistical practices detected."
        elif questionable > 0:
            verdict = "WARNING: Questionable statistical practices detected."
        else:
            verdict = "PASS: No statistical validity issues detected."

        return {
            "total_violations": len(violations),
            "invalid_count": invalid,
            "questionable_count": questionable,
            "statistical_tests_found": len(self.analyzer.statistical_tests),
            "verdict": verdict,
        }

    def _violation_to_dict(self, v: StatisticalViolation) -> Dict[str, Any]:
        """Convert violation to dictionary."""
        return {
            "type": v.violation_type,
            "severity": v.severity.value,
            "line": v.line,
            "description": v.description,
            "statistical_impact": v.statistical_impact,
            "corrected_interpretation": v.corrected_interpretation,
            "recommendation": v.recommendation,
            "confidence": v.confidence,
            "blocking": v.severity in {StatisticalRisk.INVALID, StatisticalRisk.FRAUDULENT}
            and v.confidence in {"high", "medium"},
        }

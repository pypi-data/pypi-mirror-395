"""
Demyst MCP Server.

Exposes Demyst scientific integrity checks as Model Context Protocol (MCP) tools.
This allows AI agents (Claude, Cursor, etc.) to verify their own scientific code.

Available Tools:
    - detect_mirage: Detect variance-destroying operations
    - detect_leakage: Detect train/test data leakage
    - check_hypothesis: Check for p-hacking and statistical validity
    - check_tensor: Check deep learning integrity (gradients, normalization)
    - check_units: Check dimensional consistency
    - analyze_all: Run all guards and get comprehensive analysis
    - fix_mirages: Auto-fix computational mirages
    - generate_report: Generate integrity report in markdown/JSON
    - sign_verification: Generate cryptographic certificate

Note: This module requires Python 3.10+ (mcp package dependency).
"""

import sys

if sys.version_info < (3, 10):
    raise ImportError(
        "demyst.mcp requires Python 3.10 or later. "
        "The MCP (Model Context Protocol) package is not available on Python 3.9."
    )

import ast
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise ImportError(
        "Optional dependency 'mcp>=1.0.0' is required for demyst.mcp on Python >=3.10. "
        "Install with `pip install demyst[mcp]` or skip MCP features."
    ) from e

from pydantic import BaseModel, Field

from demyst.config.manager import ConfigManager
from demyst.engine.mirage_detector import MirageDetector
from demyst.guards.hypothesis_guard import HypothesisGuard
from demyst.guards.leakage_hunter import LeakageHunter
from demyst.guards.tensor_guard import TensorGuard
from demyst.guards.unit_guard import UnitGuard

# Initialize FastMCP server
mcp = FastMCP("demyst")

# Setup logging
logger = logging.getLogger("demyst.mcp")
logging.basicConfig(level=logging.INFO)


class MirageResult(BaseModel):
    """Result of mirage detection."""

    has_mirages: bool = Field(..., description="Whether any computational mirages were found")
    mirages: List[Dict[str, Any]] = Field(..., description="List of detected mirages")
    recommendations: List[str] = Field(..., description="Recommendations for fixing mirages")


class UnitResult(BaseModel):
    """Result of unit consistency check."""

    consistent: bool = Field(..., description="Whether units are consistent")
    violations: List[Dict[str, Any]] = Field(..., description="List of unit violations")
    inferred_dimensions: Dict[str, str] = Field(..., description="Inferred dimensions of variables")


class SignedCertificate(BaseModel):
    """Cryptographic proof of verification."""

    code_hash: str = Field(..., description="SHA-256 hash of the code")
    verdict: str = Field(..., description="Verification verdict (PASS/FAIL)")
    timestamp: str = Field(..., description="ISO timestamp of verification")
    signature: str = Field(..., description="HMAC-SHA256 signature")


class LeakageResult(BaseModel):
    """Result of data leakage detection."""

    has_leakage: bool = Field(..., description="Whether any data leakage was found")
    violations: List[Dict[str, Any]] = Field(..., description="List of leakage violations")
    taint_map: Dict[str, Any] = Field(..., description="Taint tracking map")
    summary: Optional[Dict[str, Any]] = Field(None, description="Summary statistics")
    recommendations: List[str] = Field(..., description="Recommendations for fixing leakage")


class HypothesisResult(BaseModel):
    """Result of hypothesis/p-hacking check."""

    has_issues: bool = Field(..., description="Whether any statistical validity issues were found")
    violations: List[Dict[str, Any]] = Field(
        ..., description="List of p-hacking/statistical violations"
    )
    experiment_count: int = Field(..., description="Number of statistical tests detected")
    recommendations: List[str] = Field(..., description="Recommendations for statistical validity")


class TensorResult(BaseModel):
    """Result of deep learning integrity check."""

    has_issues: bool = Field(
        ..., description="Whether any deep learning integrity issues were found"
    )
    gradient_issues: List[Dict[str, Any]] = Field(
        ..., description="Gradient death/vanishing issues"
    )
    normalization_issues: List[Dict[str, Any]] = Field(
        ..., description="Normalization blindness issues"
    )
    reward_issues: List[Dict[str, Any]] = Field(..., description="Reward hacking issues (RL)")
    recommendations: List[str] = Field(..., description="Recommendations for DL integrity")


class AnalysisResult(BaseModel):
    """Result of comprehensive analysis (all guards)."""

    overall_status: str = Field(..., description="Overall status: PASS/WARNING/FAIL")
    mirage: Dict[str, Any] = Field(..., description="Mirage detection results")
    leakage: Dict[str, Any] = Field(..., description="Data leakage results")
    hypothesis: Dict[str, Any] = Field(..., description="Statistical validity results")
    tensor: Dict[str, Any] = Field(..., description="Deep learning integrity results")
    units: Dict[str, Any] = Field(..., description="Dimensional consistency results")
    summary: Dict[str, Any] = Field(..., description="Summary with counts by severity")


class FixResult(BaseModel):
    """Result of auto-fix operation."""

    success: bool = Field(..., description="Whether fixes were applied successfully")
    fixed_code: str = Field(..., description="The fixed code (or original if dry_run)")
    actions: List[Dict[str, Any]] = Field(..., description="List of fix actions applied")
    diff: str = Field(..., description="Unified diff of changes")


@mcp.tool()
def detect_mirage(code: str) -> str:
    """
    Detects computational mirages (variance-destroying operations) in scientific code.

    Use this tool to check if code performs operations like `mean`, `sum`, or `argmax`
    on high-variance or heavy-tailed distributions without proper handling.

    Args:
        code: The Python code to analyze.

    Returns:
        JSON string containing detection results and recommendations.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return json.dumps({"error": f"Syntax error: {e}"})

    config_manager = ConfigManager()
    detector = MirageDetector(config=config_manager.get_rule_config("mirage"))
    detector.visit(tree)

    # Clean up mirages for serialization (remove AST nodes)
    serializable_mirages = []
    for m in detector.mirages:
        clean_m = m.copy()
        if "node" in clean_m:
            del clean_m["node"]
        serializable_mirages.append(clean_m)

    recommendations = []
    if serializable_mirages:
        recommendations.append("Use VariationTensor to preserve statistical metadata.")
        recommendations.append("Check if the distribution is heavy-tailed before aggregating.")

    result = MirageResult(
        has_mirages=bool(serializable_mirages),
        mirages=serializable_mirages,
        recommendations=recommendations,
    )

    return result.model_dump_json()


@mcp.tool()
def check_units(code: str) -> str:
    """
    Checks for dimensional consistency in scientific code.

    Use this tool to verify that physical units are handled correctly (e.g., not adding
    meters to seconds).

    Args:
        code: The Python code to analyze.

    Returns:
        JSON string containing consistency results and inferred dimensions.
    """
    config_manager = ConfigManager()
    guard = UnitGuard(config=config_manager.get_rule_config("unit"))

    try:
        analysis = guard.analyze(code)
    except Exception as e:
        return json.dumps({"error": f"Analysis failed: {e}"})

    violations = analysis.get("violations", [])

    result = UnitResult(
        consistent=len(violations) == 0,
        violations=violations,
        inferred_dimensions=analysis.get("inferred_dimensions", {}),
    )

    return result.model_dump_json()


@mcp.tool()
def sign_verification(code: str, verdict: str) -> str:
    """
    Generates a cryptographic certificate of integrity for verified code.

    Use this tool AFTER running checks to freeze the code state and prove it passed.

    Args:
        code: The verified Python code.
        verdict: The result of the checks (e.g., "PASS", "FAIL").

    Returns:
        JSON string containing the certificate with signature.
    """
    from demyst.security import sign_code

    cert_dict = sign_code(code, verdict)

    cert = SignedCertificate(
        code_hash=cert_dict["code_hash"],
        verdict=cert_dict["verdict"],
        timestamp=cert_dict["timestamp"],
        signature=cert_dict["signature"],
    )

    return cert.model_dump_json()


@mcp.tool()
def detect_leakage(code: str) -> str:
    """
    Detects train/test data leakage using taint analysis.

    Data leakage is the #1 error in machine learning - it occurs when test data
    contaminates training, making benchmarks unreliable. This tool detects:
    - fit_transform() before train_test_split()
    - Target encoding before cross-validation
    - Preprocessing leakage patterns

    Args:
        code: The Python code to analyze.

    Returns:
        JSON string containing leakage violations and taint map.
    """
    config_manager = ConfigManager()
    hunter = LeakageHunter(config=config_manager.get_rule_config("leakage"))

    try:
        analysis = hunter.analyze(code)
    except Exception as e:
        return json.dumps({"error": f"Analysis failed: {e}"})

    violations = analysis.get("violations", [])

    # Clean up violations for serialization
    serializable_violations = []
    for v in violations:
        if hasattr(v, "__dict__"):
            serializable_violations.append(v.__dict__)
        elif isinstance(v, dict):
            serializable_violations.append(v)
        else:
            serializable_violations.append(str(v))

    recommendations = []
    if serializable_violations:
        recommendations.append("Split data BEFORE any preprocessing (fit_transform, encoding).")
        recommendations.append(
            "Fit preprocessing only on training data, then transform both train and test."
        )
        recommendations.append("Use Pipeline with cross_val_score to ensure proper data handling.")

    # Clean taint_map for serialization
    taint_map = analysis.get("taint_map", {})
    serializable_taint = {}
    for k, v in taint_map.items():
        if hasattr(v, "__dict__"):
            serializable_taint[k] = v.__dict__
        else:
            serializable_taint[k] = str(v)

    result = LeakageResult(
        has_leakage=bool(serializable_violations),
        violations=serializable_violations,
        taint_map=serializable_taint,
        summary=analysis.get("summary"),
        recommendations=recommendations,
    )

    return result.model_dump_json()


@mcp.tool()
def check_hypothesis(code: str) -> str:
    """
    Checks for p-hacking and statistical validity issues.

    Detects patterns that inflate false positive rates:
    - Multiple comparisons without Bonferroni/FDR correction
    - Conditional reporting based on p-values
    - Cherry-picking patterns

    Args:
        code: The Python code to analyze.

    Returns:
        JSON string containing statistical validity results.
    """
    config_manager = ConfigManager()
    guard = HypothesisGuard(config=config_manager.get_rule_config("hypothesis"))

    try:
        analysis = guard.analyze_code(code)
    except Exception as e:
        return json.dumps({"error": f"Analysis failed: {e}"})

    violations = analysis.get("violations", [])

    # Clean up violations for serialization
    serializable_violations = []
    for v in violations:
        if hasattr(v, "__dict__"):
            serializable_violations.append(v.__dict__)
        elif isinstance(v, dict):
            serializable_violations.append(v)
        else:
            serializable_violations.append(str(v))

    recommendations = []
    if serializable_violations:
        recommendations.append("Apply Bonferroni correction for multiple comparisons.")
        recommendations.append("Report all tests conducted, not just significant ones.")
        recommendations.append("Pre-register analysis plan to prevent p-hacking.")

    result = HypothesisResult(
        has_issues=bool(serializable_violations),
        violations=serializable_violations,
        experiment_count=analysis.get("experiment_count", 0),
        recommendations=recommendations,
    )

    return result.model_dump_json()


@mcp.tool()
def check_tensor(code: str) -> str:
    """
    Checks deep learning code for integrity issues.

    Detects problems in PyTorch/JAX code:
    - Gradient death chains (vanishing gradients from deep sigmoid/tanh)
    - Normalization blindness (BatchNorm masking distribution shifts)
    - Reward hacking vulnerabilities in RL

    Args:
        code: The Python code to analyze.

    Returns:
        JSON string containing deep learning integrity results.
    """
    config_manager = ConfigManager()
    guard = TensorGuard(config=config_manager.get_rule_config("tensor"))

    try:
        analysis = guard.analyze(code)
    except Exception as e:
        return json.dumps({"error": f"Analysis failed: {e}"})

    # Extract issues by category
    gradient_issues = analysis.get("gradient_issues", [])
    normalization_issues = analysis.get("normalization_issues", [])
    reward_issues = analysis.get("reward_issues", [])

    # Also check for general violations
    all_violations = analysis.get("violations", [])

    # Clean up for serialization
    def clean_issues(issues):
        result = []
        for v in issues:
            if hasattr(v, "__dict__"):
                result.append(v.__dict__)
            elif isinstance(v, dict):
                result.append(v)
            else:
                result.append(str(v))
        return result

    gradient_issues = clean_issues(gradient_issues)
    normalization_issues = clean_issues(normalization_issues)
    reward_issues = clean_issues(reward_issues)

    has_issues = bool(gradient_issues or normalization_issues or reward_issues or all_violations)

    recommendations = []
    if gradient_issues:
        recommendations.append("Add residual connections to prevent gradient death.")
        recommendations.append("Use LayerNorm or careful initialization.")
    if normalization_issues:
        recommendations.append(
            "Ensure BatchNorm track_running_stats=True for distribution shift detection."
        )
    if reward_issues:
        recommendations.append("Track reward distribution statistics, not just mean.")

    result = TensorResult(
        has_issues=has_issues,
        gradient_issues=gradient_issues,
        normalization_issues=normalization_issues,
        reward_issues=reward_issues,
        recommendations=recommendations,
    )

    return result.model_dump_json()


@mcp.tool()
def analyze_all(code: str) -> str:
    """
    Runs all 5 scientific integrity guards and returns comprehensive analysis.

    This is the recommended tool for full code verification. It runs:
    1. Mirage detection (variance-destroying operations)
    2. Leakage detection (train/test contamination)
    3. Hypothesis guard (p-hacking/statistical validity)
    4. Tensor guard (deep learning integrity)
    5. Unit guard (dimensional consistency)

    Args:
        code: The Python code to analyze.

    Returns:
        JSON string containing results from all guards and overall status.
    """
    # Run all guards
    mirage_result = json.loads(detect_mirage(code))
    leakage_result = json.loads(detect_leakage(code))
    hypothesis_result = json.loads(check_hypothesis(code))
    tensor_result = json.loads(check_tensor(code))
    units_result = json.loads(check_units(code))

    # Determine overall status
    has_critical = mirage_result.get("has_mirages", False) or leakage_result.get(
        "has_leakage", False
    )
    has_warning = (
        hypothesis_result.get("has_issues", False)
        or tensor_result.get("has_issues", False)
        or not units_result.get("consistent", True)
    )

    if has_critical:
        overall_status = "FAIL"
    elif has_warning:
        overall_status = "WARNING"
    else:
        overall_status = "PASS"

    # Build summary
    summary = {
        "critical_count": sum(
            [
                len(mirage_result.get("mirages", [])),
                len(leakage_result.get("violations", [])),
            ]
        ),
        "warning_count": sum(
            [
                len(hypothesis_result.get("violations", [])),
                len(tensor_result.get("gradient_issues", [])),
                len(tensor_result.get("normalization_issues", [])),
                len(tensor_result.get("reward_issues", [])),
                len(units_result.get("violations", [])),
            ]
        ),
        "checks_run": ["mirage", "leakage", "hypothesis", "tensor", "units"],
        "timestamp": datetime.now().isoformat(),
    }

    result = AnalysisResult(
        overall_status=overall_status,
        mirage=mirage_result,
        leakage=leakage_result,
        hypothesis=hypothesis_result,
        tensor=tensor_result,
        units=units_result,
        summary=summary,
    )

    return result.model_dump_json()


@mcp.tool()
def fix_mirages(code: str, dry_run: bool = True) -> str:
    """
    Auto-fixes computational mirage violations in code.

    Transforms variance-destroying operations (mean, sum, argmax, argmin)
    to use VariationTensor, which preserves statistical metadata.

    Args:
        code: The Python code to fix.
        dry_run: If True (default), returns diff without applying changes.
                 Set to False to get the actually fixed code.

    Returns:
        JSON string containing fixed code, diff, and applied actions.
    """
    import difflib

    from demyst.fixer import fix_source

    # First detect mirages to get violations
    config_manager = ConfigManager()
    detector = MirageDetector(config=config_manager.get_rule_config("mirage"))

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return json.dumps({"error": f"Syntax error: {e}", "success": False})

    detector.visit(tree)

    # Convert mirages to violation format expected by fixer
    violations = []
    for m in detector.mirages:
        violations.append(
            {
                "type": f"mirage_{m.get('operation', 'unknown')}",
                "line": m.get("line", 0),
                "column": m.get("column", 0),
                "operation": m.get("operation"),
                "variable": m.get("variable"),
            }
        )

    if not violations:
        return FixResult(
            success=True,
            fixed_code=code,
            actions=[],
            diff="",
        ).model_dump_json()

    try:
        fixed_code, actions = fix_source(code, violations, dry_run=dry_run)
    except Exception as e:
        return json.dumps({"error": f"Fix failed: {e}", "success": False})

    # Generate diff
    diff = "\n".join(
        difflib.unified_diff(
            code.splitlines(),
            fixed_code.splitlines(),
            fromfile="original",
            tofile="fixed",
            lineterm="",
        )
    )

    # Convert actions to dicts
    serializable_actions = []
    for action in actions:
        if hasattr(action, "to_dict"):
            serializable_actions.append(action.to_dict())
        elif hasattr(action, "__dict__"):
            serializable_actions.append(action.__dict__)
        else:
            serializable_actions.append(str(action))

    result = FixResult(
        success=True,
        fixed_code=fixed_code if not dry_run else code,
        actions=serializable_actions,
        diff=diff,
    )

    return result.model_dump_json()


@mcp.tool()
def generate_report(code: str, format: str = "markdown") -> str:
    """
    Generates a comprehensive scientific integrity report.

    Runs all guards and formats results into a readable report suitable
    for documentation, PRs, or paper methodology sections.

    Args:
        code: The Python code to analyze.
        format: Output format - "markdown" (default) or "json".

    Returns:
        Formatted report string.
    """
    from demyst.generators.report_generator import IntegrityReportGenerator

    # Run comprehensive analysis
    analysis = json.loads(analyze_all(code))

    # Create report generator
    generator = IntegrityReportGenerator(title="Demyst Scientific Integrity Report")
    generator.add_metadata("overall_status", analysis.get("overall_status", "UNKNOWN"))

    # Add mirage section
    mirage = analysis.get("mirage", {})
    generator.add_section(
        title="Computational Mirages",
        status="fail" if mirage.get("has_mirages") else "pass",
        content="Operations that destroy variance in high-variance distributions.",
        issues=mirage.get("mirages", []),
        recommendations=mirage.get("recommendations", []),
    )

    # Add leakage section
    leakage = analysis.get("leakage", {})
    generator.add_section(
        title="Data Leakage",
        status="fail" if leakage.get("has_leakage") else "pass",
        content="Train/test data contamination via preprocessing or feature engineering.",
        issues=leakage.get("violations", []),
        recommendations=leakage.get("recommendations", []),
    )

    # Add hypothesis section
    hypothesis = analysis.get("hypothesis", {})
    generator.add_section(
        title="Statistical Validity",
        status="warning" if hypothesis.get("has_issues") else "pass",
        content="P-hacking, multiple comparisons, and statistical validity issues.",
        issues=hypothesis.get("violations", []),
        recommendations=hypothesis.get("recommendations", []),
    )

    # Add tensor section
    tensor = analysis.get("tensor", {})
    all_tensor_issues = (
        tensor.get("gradient_issues", [])
        + tensor.get("normalization_issues", [])
        + tensor.get("reward_issues", [])
    )
    generator.add_section(
        title="Deep Learning Integrity",
        status="warning" if tensor.get("has_issues") else "pass",
        content="Gradient flow, normalization, and reward function issues.",
        issues=all_tensor_issues,
        recommendations=tensor.get("recommendations", []),
    )

    # Add units section
    units = analysis.get("units", {})
    generator.add_section(
        title="Dimensional Consistency",
        status="warning" if not units.get("consistent", True) else "pass",
        content="Physical unit compatibility and dimensional analysis.",
        issues=units.get("violations", []),
        recommendations=(
            ["Ensure all operations preserve dimensional consistency."]
            if units.get("violations")
            else []
        ),
    )

    # Generate output
    if format.lower() == "json":
        return generator.to_json()
    else:
        return generator.to_markdown()


if __name__ == "__main__":
    mcp.run()

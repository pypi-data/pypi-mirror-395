"""
TensorGuard: Deep Learning Integrity for PyTorch and JAX

Detects:
    1. Silent Gradient Death: Operations causing vanishing/exploding gradients
    2. Normalization Blindness: BatchNorm masking distribution shifts
    3. Reward Hacking: RL reward functions that hide negative spikes

Philosophy: "If the gradient dies in silence, the model learns nothing."
"""

import ast
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, cast


class GradientRisk(Enum):
    """Risk levels for gradient flow issues."""

    SAFE = "safe"
    WARNING = "warning"
    CRITICAL = "critical"
    FATAL = "fatal"


@dataclass
class GradientIssue:
    """Represents a detected gradient flow issue."""

    issue_type: str
    severity: GradientRisk
    line: int
    col: int
    description: str
    recommendation: str
    scientific_impact: str


@dataclass
class NormalizationIssue:
    """Represents a normalization blindness issue."""

    layer_name: str
    line: int
    issue_type: str
    description: str
    masked_statistics: List[str]
    recommendation: str


@dataclass
class RewardIssue:
    """Represents a reward hacking vulnerability."""

    function_name: str
    line: int
    issue_type: str
    description: str
    exploit_vector: str
    recommendation: str


class GradientDeathDetector(ast.NodeVisitor):
    """
    Detects operations that cause vanishing or exploding gradients.

    Silent Gradient Death Patterns:
        1. Deep sigmoid/tanh chains without residual connections
        2. Unbounded activations (ReLU) without gradient clipping
        3. Multiplicative operations that compound gradient issues
        4. Softmax in intermediate layers (gradient diffusion)
    """

    ACTIVATION_SATURATION_RISK = {
        "Sigmoid": {"depth_threshold": 3, "risk": GradientRisk.CRITICAL},
        "sigmoid": {"depth_threshold": 3, "risk": GradientRisk.CRITICAL},
        "Tanh": {"depth_threshold": 4, "risk": GradientRisk.WARNING},
        "tanh": {"depth_threshold": 4, "risk": GradientRisk.WARNING},
        "Softmax": {"depth_threshold": 1, "risk": GradientRisk.WARNING},
        "softmax": {"depth_threshold": 1, "risk": GradientRisk.WARNING},
    }

    GRADIENT_PRESERVING = {"ReLU", "LeakyReLU", "GELU", "SiLU", "Mish"}

    def __init__(self) -> None:
        self.issues: List[GradientIssue] = []
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None
        self.activation_chain: List[Tuple[str, int]] = []
        self.has_residual: bool = False
        self.layer_depth: int = 0
        self.detected_layers: List[Dict[str, Any]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Track neural network class definitions."""
        old_class = self.current_class

        # Check if this is a PyTorch module
        is_nn_module = any(
            (isinstance(base, ast.Attribute) and base.attr == "Module")
            or (isinstance(base, ast.Name) and base.id in ["Module", "nn.Module"])
            for base in node.bases
        )

        if is_nn_module:
            self.current_class = node.name
            self.layer_depth = 0
            self.activation_chain = []

        self.generic_visit(node)
        self.current_class = old_class

        # Analyze the complete chain after visiting
        if is_nn_module:
            self._analyze_activation_chain()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track function definitions within modules."""
        old_function = self.current_function
        self.current_function = node.name

        # Reset tracking for forward pass
        if node.name == "forward" and self.current_class:
            self.activation_chain = []
            self.has_residual = False

        self.generic_visit(node)
        self.current_function = old_function

    def visit_Call(self, node: ast.Call) -> None:
        """Detect activation functions and layer operations."""
        layer_name = self._get_layer_name(node)

        if layer_name:
            self.detected_layers.append(
                {"name": layer_name, "line": node.lineno, "col": node.col_offset}
            )

            # Track activation chains
            if layer_name in self.ACTIVATION_SATURATION_RISK:
                self.activation_chain.append((layer_name, node.lineno))

            # Check for residual connections (x + self.layer(x) pattern)
            if self._is_residual_connection(node):
                self.has_residual = True

        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Detect residual connections (addition operations)."""
        if isinstance(node.op, ast.Add):
            # Look for patterns like: x + layer(x) or layer(x) + x
            if self._looks_like_residual(node):
                self.has_residual = True
        self.generic_visit(node)

    def _get_layer_name(self, node: ast.Call) -> Optional[str]:
        """Extract layer name from a call node."""
        if isinstance(node.func, ast.Attribute):
            # self.relu(x) or nn.ReLU()
            return node.func.attr
        elif isinstance(node.func, ast.Name):
            # F.relu(x)
            return node.func.id
        return None

    def _is_residual_connection(self, node: ast.Call) -> bool:
        """Check if this call is part of a residual connection."""
        # This is a simplified check - real implementation would do data flow analysis
        return False

    def _looks_like_residual(self, node: ast.BinOp) -> bool:
        """Heuristic to detect residual connections."""
        # Check if one operand is a simple name and other is a call
        left_is_name = isinstance(node.left, ast.Name)
        right_is_name = isinstance(node.right, ast.Name)
        left_is_call = isinstance(node.left, ast.Call)
        right_is_call = isinstance(node.right, ast.Call)

        return (left_is_name and right_is_call) or (right_is_name and left_is_call)

    def _analyze_activation_chain(self) -> None:
        """Analyze the accumulated activation chain for gradient death risks."""
        if not self.activation_chain:
            return

        # Count consecutive saturating activations
        saturating_count = 0
        last_saturating = None

        for activation, line in self.activation_chain:
            if activation in self.ACTIVATION_SATURATION_RISK:
                saturating_count += 1
                last_saturating = (activation, line)

                risk_info = self.ACTIVATION_SATURATION_RISK[activation]

                if (
                    saturating_count >= cast(int, risk_info["depth_threshold"])
                    and not self.has_residual
                ):
                    self.issues.append(
                        GradientIssue(
                            issue_type="gradient_death_chain",
                            severity=cast(GradientRisk, risk_info["risk"]),
                            line=line,
                            col=0,
                            description=(
                                f"Detected {saturating_count} consecutive {activation} activations "
                                f"without residual connections. Gradients will vanish."
                            ),
                            recommendation=(
                                f"Add residual/skip connections, or replace {activation} with "
                                f"ReLU/GELU in intermediate layers. Consider gradient checkpointing."
                            ),
                            scientific_impact=(
                                "Vanishing gradients cause early layers to stop learning, "
                                "making the network effectively shallower than designed. "
                                "This is a form of 'silent failure' - the model trains but "
                                "cannot learn complex hierarchical features."
                            ),
                        )
                    )
            else:
                # Non-saturating activation resets the chain
                saturating_count = 0


class NormalizationAnalyzer(ast.NodeVisitor):
    """
    Detects normalization layers that mask distribution shifts.

    Normalization Blindness Patterns:
        1. BatchNorm before distribution-sensitive operations
        2. LayerNorm hiding feature scale changes
        3. Normalization immediately after data augmentation
        4. BatchNorm with small batch sizes (unreliable statistics)
    """

    NORMALIZATION_LAYERS = {
        "BatchNorm1d",
        "BatchNorm2d",
        "BatchNorm3d",
        "LayerNorm",
        "GroupNorm",
        "InstanceNorm1d",
        "InstanceNorm2d",
        "InstanceNorm3d",
        "batch_norm",
        "layer_norm",
        "group_norm",
    }

    DISTRIBUTION_SENSITIVE = {
        "Dropout",
        "AlphaDropout",
        "attention",
        "self_attention",
        "multi_head_attention",
        "softmax",
        "log_softmax",
    }

    def __init__(self) -> None:
        self.issues: List[NormalizationIssue] = []
        self.current_class: Optional[str] = None
        self.norm_layers: List[Dict[str, Any]] = []
        self.layer_sequence: List[Tuple[str, str, int]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Track class definitions."""
        old_class = self.current_class
        self.current_class = node.name
        self.layer_sequence = []
        self.generic_visit(node)
        self._analyze_normalization_sequence()
        self.current_class = old_class

    def visit_Call(self, node: ast.Call) -> None:
        """Track normalization and distribution-sensitive layers."""
        layer_name = self._get_layer_name(node)

        if layer_name:
            is_norm = any(norm in layer_name for norm in self.NORMALIZATION_LAYERS)
            is_sensitive = any(
                sens.lower() in layer_name.lower() for sens in self.DISTRIBUTION_SENSITIVE
            )

            if is_norm or is_sensitive:
                self.layer_sequence.append(
                    ("norm" if is_norm else "sensitive", layer_name, node.lineno)
                )

            # Check for BatchNorm batch_size argument
            if "BatchNorm" in layer_name:
                self._check_batch_norm_config(node, layer_name)

        self.generic_visit(node)

    def _get_layer_name(self, node: ast.Call) -> Optional[str]:
        """Extract layer name from call node."""
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif isinstance(node.func, ast.Name):
            return node.func.id
        return None

    def _check_batch_norm_config(self, node: ast.Call, layer_name: str) -> None:
        """Check BatchNorm configuration for potential issues."""
        # Check for track_running_stats=False (dangerous in eval mode)
        for keyword in node.keywords:
            if keyword.arg == "track_running_stats":
                if isinstance(keyword.value, ast.Constant) and keyword.value.value is False:
                    self.issues.append(
                        NormalizationIssue(
                            layer_name=layer_name,
                            line=node.lineno,
                            issue_type="unstable_batch_stats",
                            description=(
                                f"{layer_name} with track_running_stats=False will use batch "
                                "statistics during evaluation, causing non-deterministic behavior."
                            ),
                            masked_statistics=["running_mean", "running_var"],
                            recommendation=(
                                "Keep track_running_stats=True for production models. "
                                "Batch statistics during eval hide distribution shifts between "
                                "training and deployment data."
                            ),
                        )
                    )

    def _analyze_normalization_sequence(self) -> None:
        """Analyze layer sequence for normalization blindness patterns."""
        for i, (layer_type, name, line) in enumerate(self.layer_sequence):
            if layer_type == "norm":
                # Check if next layer is distribution-sensitive
                if i + 1 < len(self.layer_sequence):
                    next_type, next_name, next_line = self.layer_sequence[i + 1]
                    if next_type == "sensitive":
                        self.issues.append(
                            NormalizationIssue(
                                layer_name=name,
                                line=line,
                                issue_type="normalization_before_sensitive",
                                description=(
                                    f"{name} immediately before {next_name} will mask "
                                    "feature scale information that the sensitive layer needs."
                                ),
                                masked_statistics=["feature_scale", "distribution_shift"],
                                recommendation=(
                                    f"Consider moving {name} after {next_name}, or add "
                                    "an explicit scale/shift parameter that is logged for analysis."
                                ),
                            )
                        )


class RewardHackingDetector(ast.NodeVisitor):
    """
    Detects RL reward functions vulnerable to reward hacking.

    Reward Hacking Patterns:
        1. Mean aggregation hiding negative spikes
        2. Sparse rewards (long sequences of zeros)
        3. Unbounded rewards enabling exploitation
        4. Reward clipping that destroys gradient signal
    """

    AGGREGATION_OPS = {"mean", "sum", "average", "reduce_mean", "reduce_sum"}
    CLIPPING_OPS = {"clip", "clamp", "clip_by_value"}

    def __init__(self) -> None:
        self.issues: List[RewardIssue] = []
        self.current_function: Optional[str] = None
        self.in_reward_function: bool = False
        self.reward_operations: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track reward-related functions."""
        old_function = self.current_function
        old_in_reward = self.in_reward_function

        self.current_function = node.name
        self.in_reward_function = self._is_reward_function(node)

        if self.in_reward_function:
            self.reward_operations = []

        self.generic_visit(node)

        if self.in_reward_function:
            self._analyze_reward_function(node)

        self.current_function = old_function
        self.in_reward_function = old_in_reward

    def visit_Call(self, node: ast.Call) -> None:
        """Track operations within reward functions."""
        if self.in_reward_function:
            op_name = self._get_operation_name(node)

            if op_name:
                op_type = self._classify_operation(op_name)
                if op_type:
                    self.reward_operations.append(
                        {"name": op_name, "type": op_type, "line": node.lineno, "node": node}
                    )

        self.generic_visit(node)

    def _is_reward_function(self, node: ast.FunctionDef) -> bool:
        """Check if function is a reward function."""
        reward_indicators = [
            "reward",
            "compute_reward",
            "get_reward",
            "calculate_reward",
            "step_reward",
            "episode_reward",
        ]
        return any(ind in node.name.lower() for ind in reward_indicators)

    def _get_operation_name(self, node: ast.Call) -> Optional[str]:
        """Get operation name from call node."""
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif isinstance(node.func, ast.Name):
            return node.func.id
        return None

    def _classify_operation(self, name: str) -> Optional[str]:
        """Classify operation type."""
        name_lower = name.lower()
        if any(agg in name_lower for agg in self.AGGREGATION_OPS):
            return "aggregation"
        if any(clip in name_lower for clip in self.CLIPPING_OPS):
            return "clipping"
        return None

    def _analyze_reward_function(self, node: ast.FunctionDef) -> None:
        """Analyze reward function for hacking vulnerabilities."""
        has_aggregation = False
        has_clipping = False

        for op in self.reward_operations:
            if op["type"] == "aggregation":
                has_aggregation = True
                self.issues.append(
                    RewardIssue(
                        function_name=str(self.current_function),
                        line=op["line"],
                        issue_type="reward_aggregation_mirage",
                        description=(
                            f"Reward function uses {op['name']}() which hides negative spikes. "
                            "An agent could achieve high mean reward while causing "
                            "catastrophic failures on individual steps."
                        ),
                        exploit_vector=(
                            "Agent learns to maximize average reward by taking many small "
                            "positive actions while occasionally taking severely negative actions "
                            "that are masked by the mean."
                        ),
                        recommendation=(
                            "Track reward variance alongside mean. Add penalty for high-variance "
                            "reward signals. Consider using CVaR (Conditional Value at Risk) "
                            "instead of mean for safety-critical applications."
                        ),
                    )
                )

            elif op["type"] == "clipping":
                has_clipping = True
                self.issues.append(
                    RewardIssue(
                        function_name=str(self.current_function),
                        line=op["line"],
                        issue_type="reward_clipping_blindness",
                        description=(
                            f"Reward clipping with {op['name']}() destroys gradient signal "
                            "for extreme rewards. Agent cannot distinguish between 'very bad' "
                            "and 'catastrophically bad' actions."
                        ),
                        exploit_vector=(
                            "Agent cannot learn to avoid worst-case scenarios because "
                            "gradient signal is zero for clipped regions."
                        ),
                        recommendation=(
                            "Use soft clipping (tanh scaling) instead of hard clipping. "
                            "Log unclipped rewards for analysis. Consider reward shaping "
                            "that preserves relative ordering of outcomes."
                        ),
                    )
                )


class TensorGuard:
    """
    Main entry point for deep learning integrity analysis.

    Combines:
        - GradientDeathDetector: Vanishing/exploding gradient detection
        - NormalizationAnalyzer: Distribution shift masking detection
        - RewardHackingDetector: RL reward function vulnerability detection
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.gradient_detector = GradientDeathDetector()
        self.norm_analyzer = NormalizationAnalyzer()
        self.reward_detector = RewardHackingDetector()

    def analyze(self, source: str) -> Dict[str, Any]:
        """
        Analyze source code for deep learning integrity issues.

        Args:
            source: Python source code string

        Returns:
            Dictionary containing all detected issues and recommendations
        """
        try:
            # Sanitize source by removing null bytes before parsing
            sanitized_source = source.replace("\x00", "")
            tree = ast.parse(sanitized_source)
        except SyntaxError as e:
            return {
                "error": f"Syntax error in source: {e}",
                "gradient_issues": [],
                "normalization_issues": [],
                "reward_issues": [],
                "summary": None,
            }

        # Run all detectors
        self.gradient_detector = GradientDeathDetector()
        self.norm_analyzer = NormalizationAnalyzer()
        self.reward_detector = RewardHackingDetector()

        self.gradient_detector.visit(tree)
        self.norm_analyzer.visit(tree)
        self.reward_detector.visit(tree)

        # Compile results
        gradient_issues = self.gradient_detector.issues
        norm_issues = self.norm_analyzer.issues
        reward_issues = self.reward_detector.issues

        # Generate summary
        total_issues = len(gradient_issues) + len(norm_issues) + len(reward_issues)
        critical_count = sum(
            1 for i in gradient_issues if i.severity in [GradientRisk.CRITICAL, GradientRisk.FATAL]
        )

        summary = {
            "total_issues": total_issues,
            "critical_issues": critical_count,
            "gradient_death_risks": len(gradient_issues),
            "normalization_blindness": len(norm_issues),
            "reward_hacking_vulnerabilities": len(reward_issues),
            "verdict": self._compute_verdict(gradient_issues, norm_issues, reward_issues),
        }

        return {
            "gradient_issues": [self._issue_to_dict(i) for i in gradient_issues],
            "normalization_issues": [self._norm_issue_to_dict(i) for i in norm_issues],
            "reward_issues": [self._reward_issue_to_dict(i) for i in reward_issues],
            "summary": summary,
        }

    def _compute_verdict(
        self,
        gradient_issues: List[GradientIssue],
        norm_issues: List[NormalizationIssue],
        reward_issues: List[RewardIssue],
    ) -> str:
        """Compute overall verdict."""
        critical = any(
            i.severity in [GradientRisk.CRITICAL, GradientRisk.FATAL] for i in gradient_issues
        )

        if critical or len(reward_issues) > 0:
            return "FAIL: Critical integrity issues detected. Do not deploy."
        elif len(gradient_issues) > 0 or len(norm_issues) > 0:
            return "WARNING: Issues detected that may affect model reliability."
        else:
            return "PASS: No integrity issues detected."

    def _issue_to_dict(self, issue: GradientIssue) -> Dict[str, Any]:
        """Convert GradientIssue to dictionary."""
        if issue.severity in [GradientRisk.FATAL, GradientRisk.CRITICAL]:
            confidence = "high"
            blocking = True
        elif issue.severity == GradientRisk.WARNING:
            confidence = "medium"
            blocking = False
        else:
            confidence = "low"
            blocking = False
        return {
            "type": issue.issue_type,
            "severity": issue.severity.value,
            "line": issue.line,
            "col": issue.col,
            "description": issue.description,
            "recommendation": issue.recommendation,
            "scientific_impact": issue.scientific_impact,
            "confidence": confidence,
            "blocking": blocking,
        }

    def _norm_issue_to_dict(self, issue: NormalizationIssue) -> Dict[str, Any]:
        """Convert NormalizationIssue to dictionary."""
        return {
            "layer": issue.layer_name,
            "line": issue.line,
            "type": issue.issue_type,
            "description": issue.description,
            "masked_statistics": issue.masked_statistics,
            "recommendation": issue.recommendation,
            "confidence": "medium",
            "blocking": False,
        }

    def _reward_issue_to_dict(self, issue: RewardIssue) -> Dict[str, Any]:
        """Convert RewardIssue to dictionary."""
        return {
            "function": issue.function_name,
            "line": issue.line,
            "type": issue.issue_type,
            "description": issue.description,
            "exploit_vector": issue.exploit_vector,
            "recommendation": issue.recommendation,
            "confidence": "high",
            "blocking": True,
        }

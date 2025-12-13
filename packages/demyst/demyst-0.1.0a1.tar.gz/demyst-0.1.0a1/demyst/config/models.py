"""
Pydantic Configuration Models for Demyst

Provides strict validation for all configuration options using Pydantic v2.
Supports both programmatic configuration and YAML/JSON file loading.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

try:
    from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False

    # Fallback for when pydantic is not installed
    class BaseModel:  # type: ignore[no-redef]
        """Fallback BaseModel when pydantic is not available."""

        def __init__(self, **data: Any) -> None:
            for key, value in data.items():
                setattr(self, key, value)

        def model_dump(self) -> Dict[str, Any]:
            return self.__dict__.copy()

    def Field(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        return kwargs.get("default")

    def field_validator(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        def decorator(func: Any) -> Any:
            return func

        return decorator

    def model_validator(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        def decorator(func: Any) -> Any:
            return func

        return decorator

    class ConfigDict:  # type: ignore[no-redef]
        pass


# =============================================================================
# Enumerations
# =============================================================================


class Severity(str, Enum):
    """Severity levels for rule violations."""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    DISABLED = "disabled"


class ProfileName(str, Enum):
    """Built-in profile names."""

    DEFAULT = "default"
    PHYSICS = "physics"
    BIOLOGY = "biology"
    CHEMISTRY = "chemistry"
    NEUROSCIENCE = "neuroscience"
    CLIMATE = "climate"
    ECONOMICS = "economics"
    STRICT = "strict"
    PERMISSIVE = "permissive"


class OutputFormat(str, Enum):
    """Supported output formats."""

    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"


class PaperStyle(str, Enum):
    """Supported LaTeX paper styles."""

    NEURIPS = "neurips"
    ICML = "icml"
    ICLR = "iclr"
    ARXIV = "arxiv"


# =============================================================================
# Rule Configuration Models
# =============================================================================


class RuleConfig(BaseModel):
    """Configuration for a single analysis rule."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(default=True, description="Whether this rule is enabled")
    severity: Severity = Field(
        default=Severity.WARNING, description="Severity level when rule is violated"
    )
    exclude: List[str] = Field(
        default_factory=list, description="Patterns to exclude from this rule"
    )

    # Rule-specific options
    options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional rule-specific options"
    )


class MirageRuleConfig(RuleConfig):
    """Configuration specific to mirage detection."""

    severity: Severity = Field(default=Severity.CRITICAL)

    # Mirage-specific options
    detect_mean: bool = Field(
        default=True, description="Detect np.mean and similar variance-destroying operations"
    )
    detect_sum: bool = Field(
        default=True, description="Detect aggregation operations that hide outliers"
    )
    detect_argmax: bool = Field(
        default=True, description="Detect premature discretization via argmax/argmin"
    )
    detect_rounding: bool = Field(default=True, description="Detect premature rounding operations")
    threshold_operations: int = Field(
        default=1, ge=1, description="Minimum number of operations before flagging as critical"
    )
    check_variance_context: bool = Field(
        default=True,
        description="Suppress mean/sum warning if std/var is computed on same data nearby",
    )


class LeakageRuleConfig(RuleConfig):
    """Configuration specific to data leakage detection."""

    severity: Severity = Field(default=Severity.CRITICAL)

    # Leakage-specific options
    track_fit_transform: bool = Field(
        default=True, description="Track sklearn fit_transform leakage patterns"
    )
    track_temporal: bool = Field(default=True, description="Detect time-series data leakage")
    track_target_leakage: bool = Field(default=True, description="Detect target variable leakage")


class HypothesisRuleConfig(RuleConfig):
    """Configuration specific to statistical validity checking."""

    severity: Severity = Field(default=Severity.WARNING)

    # Hypothesis-specific options
    default_alpha: float = Field(
        default=0.05, gt=0.0, lt=1.0, description="Default significance level"
    )
    require_correction: bool = Field(
        default=True, description="Require multiple comparison correction"
    )
    correction_method: str = Field(
        default="bonferroni",
        description="Default correction method (bonferroni, holm, benjamini_hochberg)",
    )

    # Physics-specific options
    physics_mode: bool = Field(
        default=False,
        description="Use physics sigma thresholds instead of standard p<0.05",
    )
    discovery_sigma: float = Field(
        default=5.0,
        ge=1.0,
        le=10.0,
        description="Sigma threshold for discovery claim (5 sigma = p~3e-7)",
    )
    evidence_sigma: float = Field(
        default=3.0,
        ge=1.0,
        le=10.0,
        description="Sigma threshold for evidence claim (3 sigma = p~0.0027)",
    )

    if PYDANTIC_AVAILABLE:

        @field_validator("correction_method")
        @classmethod
        def validate_correction_method(cls, v: str) -> str:
            allowed = {"bonferroni", "holm", "benjamini_hochberg", "none"}
            if v.lower() not in allowed:
                raise ValueError(f"correction_method must be one of {allowed}")
            return v.lower()


class UnitRuleConfig(RuleConfig):
    """Configuration specific to dimensional analysis."""

    severity: Severity = Field(default=Severity.WARNING)

    # Unit-specific options
    infer_from_names: bool = Field(default=True, description="Infer units from variable names")
    check_comparisons: bool = Field(
        default=True, description="Check dimensional consistency in comparisons"
    )
    check_assignments: bool = Field(
        default=True, description="Check dimensional consistency in assignments"
    )
    custom_dimensions: Dict[str, str] = Field(
        default_factory=dict,
        description="Custom dimension mappings (variable_pattern -> dimension)",
    )

    # Physics-specific options
    natural_units: bool = Field(
        default=False,
        description="Treat c, hbar, G, kB as dimensionless (natural units: c=hbar=G=kB=1)",
    )
    tensor_conventions: bool = Field(
        default=False,
        description="Recognize GR/tensor index notation (g_tt, R_abcd, Gamma_abc)",
    )


class TensorRuleConfig(RuleConfig):
    """Configuration specific to deep learning integrity."""

    severity: Severity = Field(default=Severity.CRITICAL)

    # Tensor-specific options
    check_gradients: bool = Field(
        default=True, description="Check for vanishing/exploding gradients"
    )
    check_normalization: bool = Field(default=True, description="Check for normalization issues")
    check_reward_hacking: bool = Field(
        default=True, description="Check for reward hacking vulnerabilities"
    )
    activation_depth_limit: int = Field(
        default=3, ge=1, description="Maximum depth of saturating activations before warning"
    )


# =============================================================================
# Rules Configuration (All Rules)
# =============================================================================


class RulesConfig(BaseModel):
    """Configuration for all analysis rules."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    mirage: MirageRuleConfig = Field(default_factory=MirageRuleConfig)
    leakage: LeakageRuleConfig = Field(default_factory=LeakageRuleConfig)
    hypothesis: HypothesisRuleConfig = Field(default_factory=HypothesisRuleConfig)
    unit: UnitRuleConfig = Field(default_factory=UnitRuleConfig)
    tensor: TensorRuleConfig = Field(default_factory=TensorRuleConfig)


# =============================================================================
# CLI Input Models
# =============================================================================


class AnalyzeInput(BaseModel):
    """Validated input for the analyze command."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    path: str = Field(description="File or directory to analyze")
    format: OutputFormat = Field(default=OutputFormat.MARKDOWN, description="Output format")
    config: Optional[str] = Field(default=None, description="Path to configuration file")

    if PYDANTIC_AVAILABLE:

        @field_validator("path")
        @classmethod
        def validate_path_exists(cls, v: str) -> str:
            if not Path(v).exists():
                raise ValueError(f"Path does not exist: {v}")
            return v


class MirageInput(BaseModel):
    """Validated input for the mirage command."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    path: str = Field(description="File to analyze")
    fix: bool = Field(default=False, description="Auto-fix detected mirages")
    output: Optional[str] = Field(default=None, description="Output file for fixed code")
    diff: bool = Field(default=False, description="Show diff of changes")
    dry_run: bool = Field(default=False, description="Show changes without applying")

    if PYDANTIC_AVAILABLE:

        @field_validator("path")
        @classmethod
        def validate_file_exists(cls, v: str) -> str:
            p = Path(v)
            if not p.exists():
                raise ValueError(f"File does not exist: {v}")
            if not p.is_file():
                raise ValueError(f"Path is not a file: {v}")
            return v

        @model_validator(mode="after")
        def validate_flags(self) -> "MirageInput":
            if self.dry_run and not self.fix:
                # dry_run implies fix behavior
                pass
            return self


class CIInput(BaseModel):
    """Validated input for the CI command."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    path: str = Field(default=".", description="Directory to analyze")
    strict: bool = Field(default=False, description="Fail on warnings")
    config: Optional[str] = Field(default=None, description="Path to configuration file")

    if PYDANTIC_AVAILABLE:

        @field_validator("path")
        @classmethod
        def validate_directory(cls, v: str) -> str:
            p = Path(v)
            if not p.exists():
                raise ValueError(f"Directory does not exist: {v}")
            if not p.is_dir():
                raise ValueError(f"Path is not a directory: {v}")
            return v


class PaperInput(BaseModel):
    """Validated input for the paper generation command."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    path: str = Field(description="File to analyze")
    output: Optional[str] = Field(default=None, description="Output file")
    title: str = Field(default="Methodology", description="Section title")
    style: PaperStyle = Field(default=PaperStyle.NEURIPS, description="Paper style")
    full: bool = Field(default=False, description="Generate full paper template")


# =============================================================================
# Main Configuration Model
# =============================================================================


class DemystConfig(BaseModel):
    """
    Main Demyst configuration model.

    This is the root configuration object that contains all settings
    for the Demyst platform. It can be loaded from a YAML file or
    constructed programmatically.
    """

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    # Profile selection
    profile: Union[ProfileName, str] = Field(
        default=ProfileName.DEFAULT, description="Configuration profile to use"
    )

    # Rule configurations
    rules: RulesConfig = Field(
        default_factory=RulesConfig, description="Configuration for analysis rules"
    )

    # Ignore patterns
    ignore_patterns: List[str] = Field(
        default_factory=lambda: [
            "**/test_*",
            "**/*_test.py",
            "**/tests/**",
            "**/.git/**",
            "**/venv/**",
            "**/.venv/**",
            "**/__pycache__/**",
            "**/node_modules/**",
            "**/build/**",
            "**/dist/**",
        ],
        description="Glob patterns for files to ignore",
    )

    # Output settings
    output: OutputSettings = Field(
        default_factory=lambda: OutputSettings(), description="Output configuration"
    )

    # Performance settings
    performance: PerformanceSettings = Field(
        default_factory=lambda: PerformanceSettings(), description="Performance configuration"
    )

    # Plugin settings
    plugins: PluginSettings = Field(
        default_factory=lambda: PluginSettings(), description="Plugin configuration"
    )

    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> "DemystConfig":
        """Load configuration from a YAML file."""
        import yaml

        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}

        return cls(**data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DemystConfig":
        """Create configuration from a dictionary."""
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to a dictionary."""
        if PYDANTIC_AVAILABLE:
            return self.model_dump()
        return {k: getattr(self, k) for k in self.__dict__}

    def merge_with(self, other: "DemystConfig") -> "DemystConfig":
        """Merge this configuration with another, other takes precedence."""
        base_dict = self.to_dict()
        other_dict = other.to_dict()
        merged = _deep_merge(base_dict, other_dict)
        return DemystConfig(**merged)


class OutputSettings(BaseModel):
    """Output-related configuration."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    format: OutputFormat = Field(default=OutputFormat.TEXT, description="Default output format")
    color: bool = Field(default=True, description="Enable colored output")
    verbose: bool = Field(default=False, description="Enable verbose output")
    show_context: bool = Field(default=True, description="Show code context in reports")
    context_lines: int = Field(
        default=3, ge=0, le=10, description="Number of context lines to show"
    )


class PerformanceSettings(BaseModel):
    """Performance-related configuration."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    parallel: bool = Field(default=True, description="Enable parallel analysis")
    max_workers: Optional[int] = Field(
        default=None, ge=1, description="Maximum number of parallel workers (None = auto)"
    )
    cache_enabled: bool = Field(default=True, description="Enable caching of analysis results")
    cache_dir: Optional[str] = Field(default=None, description="Directory for cache files")
    lazy_imports: bool = Field(default=True, description="Use lazy imports for heavy dependencies")
    timeout: Optional[int] = Field(
        default=300, ge=1, description="Timeout in seconds for analysis (None = no timeout)"
    )


class PluginSettings(BaseModel):
    """Plugin-related configuration."""

    if PYDANTIC_AVAILABLE:
        model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(default=True, description="Enable plugin system")
    discover: bool = Field(default=True, description="Auto-discover installed plugins")
    entry_point_group: str = Field(
        default="demyst.guards", description="Entry point group for guard plugins"
    )
    custom_guards: List[str] = Field(
        default_factory=list, description="List of custom guard module paths"
    )
    disabled_plugins: Set[str] = Field(
        default_factory=set, description="Names of plugins to disable"
    )


# =============================================================================
# Utility Functions
# =============================================================================


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries, with override taking precedence."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def validate_config(config: Dict[str, Any]) -> DemystConfig:
    """
    Validate a configuration dictionary and return a DemystConfig.

    Raises:
        ValidationError: If the configuration is invalid (when pydantic is available)
        ValueError: If the configuration is invalid (fallback)
    """
    return DemystConfig(**config)


def get_default_config() -> DemystConfig:
    """Get the default Demyst configuration."""
    return DemystConfig()

"""
Demyst: The Scientific Integrity Platform

A comprehensive tool for ensuring scientific integrity in machine learning
and data science code. Demyst detects computational mirages, data leakage,
statistical validity issues, dimensional inconsistencies, and deep learning
integrity problems.

Philosophy: "Good Code is Good Science."

Components:
    - MirageDetector: Detects variance-destroying operations
    - TensorGuard: Deep learning integrity (PyTorch/JAX)
    - LeakageHunter: Train/test data leakage detection
    - HypothesisGuard: Anti-p-hacking and statistical validity
    - UnitGuard: Dimensional analysis and unit consistency
    - PaperGenerator: LaTeX methodology section generator
    - CIEnforcer: CI/CD pipeline integration

Usage:
    from demyst.guards import TensorGuard, LeakageHunter, HypothesisGuard, UnitGuard
    from demyst.integrations import CIEnforcer
    from demyst.generators import PaperGenerator

CLI:
    demyst analyze ./src       # Run all integrity checks
    demyst mirage model.py     # Detect computational mirages
    demyst ci . --strict       # CI/CD mode
"""

try:
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("demyst")
    except PackageNotFoundError:
        __version__ = "0.0.0"
except Exception:
    __version__ = "0.0.0"
__author__ = "Demyst Team"
__description__ = "The Scientific Integrity Platform for AI Research"

# Lazy imports to avoid circular dependencies
from typing import Any


def __getattr__(name: str) -> Any:
    """Lazy loading of components to avoid import errors when dependencies aren't installed."""
    # Core Engine
    if name in ["MirageDetector"]:
        from demyst.engine.mirage_detector import MirageDetector

        return MirageDetector
    elif name in ["VariationTensor"]:
        from demyst.engine.variation_tensor import VariationTensor

        return VariationTensor
    elif name in ["Transpiler"]:
        from demyst.engine.transpiler import Transpiler

        return Transpiler
    elif name in ["CSTTranspiler"]:
        from demyst.engine.cst_transformer import CSTTranspiler

        return CSTTranspiler
    elif name in ["ParallelAnalyzer"]:
        from demyst.engine.parallel import ParallelAnalyzer

        return ParallelAnalyzer

    # Guards
    elif name in [
        "TensorGuard",
        "GradientDeathDetector",
        "NormalizationAnalyzer",
        "RewardHackingDetector",
    ]:
        from demyst.guards import tensor_guard

        return getattr(tensor_guard, name)
    elif name in ["LeakageHunter", "TaintAnalyzer", "DataFlowTracker"]:
        from demyst.guards import leakage_hunter

        return getattr(leakage_hunter, name)
    elif name in ["HypothesisGuard", "BonferroniCorrector", "ExperimentTracker"]:
        from demyst.guards import hypothesis_guard

        return getattr(hypothesis_guard, name)
    elif name in ["UnitGuard", "DimensionalAnalyzer", "UnitInferenceEngine", "Dimension"]:
        from demyst.guards import unit_guard

        return getattr(unit_guard, name)

    # Fixer
    elif name in ["DemystFixer", "fix_source"]:
        from demyst import fixer

        return getattr(fixer, name)

    # Integrations
    elif name in ["CIEnforcer", "ScientificIntegrityReport"]:
        from demyst.integrations import ci_enforcer

        return getattr(ci_enforcer, name)
    elif name in ["TorchVariation", "TorchModuleWrapper"]:
        from demyst.integrations import torch_hooks

        return getattr(torch_hooks, name)
    elif name in ["JaxVariation", "jax_safe_transform"]:
        from demyst.integrations import jax_hooks

        return getattr(jax_hooks, name)
    elif name in ["WandBIntegration", "MLflowIntegration"]:
        from demyst.integrations import experiment_trackers

        return getattr(experiment_trackers, name)

    # Generators
    elif name in ["PaperGenerator", "MethodologyExtractor"]:
        from demyst.generators import paper_generator

        return getattr(paper_generator, name)
    elif name in ["IntegrityReportGenerator"]:
        from demyst.generators import report_generator

        return getattr(report_generator, name)

    # Configuration
    elif name in ["DemystConfig", "ConfigManager"]:
        if name == "ConfigManager":
            from demyst.config.manager import ConfigManager

            return ConfigManager
        else:
            from demyst.config.models import DemystConfig

            return DemystConfig

    # Exceptions
    elif name in [
        "DemystError",
        "AnalysisError",
        "ConfigurationError",
        "TransformationError",
        "ParseError",
        "TranspilerError",
        "FixerError",
        "PluginError",
    ]:
        from demyst import exceptions

        return getattr(exceptions, name)

    # Plugins
    elif name in ["PluginRegistry", "GuardPlugin", "FixerPlugin", "get_registry"]:
        from demyst import plugins

        return getattr(plugins, name)

    # Console
    elif name in ["DemystConsole", "get_console"]:
        from demyst import console

        return getattr(console, name)

    # Lazy imports
    elif name in ["lazy_import", "require"]:
        from demyst import lazy

        return getattr(lazy, name)

    raise AttributeError(f"module 'demyst' has no attribute '{name}'")


__all__ = [
    # Version
    "__version__",
    # Core Engine
    "MirageDetector",
    "VariationTensor",
    "Transpiler",
    "CSTTranspiler",
    "ParallelAnalyzer",
    # Guards
    "TensorGuard",
    "GradientDeathDetector",
    "NormalizationAnalyzer",
    "RewardHackingDetector",
    "LeakageHunter",
    "TaintAnalyzer",
    "DataFlowTracker",
    "HypothesisGuard",
    "BonferroniCorrector",
    "ExperimentTracker",
    "UnitGuard",
    "DimensionalAnalyzer",
    "UnitInferenceEngine",
    "Dimension",
    # Fixer
    "DemystFixer",
    "fix_source",
    # Integrations
    "CIEnforcer",
    "ScientificIntegrityReport",
    "TorchVariation",
    "TorchModuleWrapper",
    "JaxVariation",
    "jax_safe_transform",
    "WandBIntegration",
    "MLflowIntegration",
    # Generators
    "PaperGenerator",
    "MethodologyExtractor",
    "IntegrityReportGenerator",
    # Configuration
    "DemystConfig",
    "ConfigManager",
    # Exceptions
    "DemystError",
    "AnalysisError",
    "ConfigurationError",
    "TransformationError",
    "ParseError",
    "TranspilerError",
    "FixerError",
    "PluginError",
    # Plugins
    "PluginRegistry",
    "GuardPlugin",
    "FixerPlugin",
    "get_registry",
    # Console
    "DemystConsole",
    "get_console",
    # Lazy imports
    "lazy_import",
    "require",
]

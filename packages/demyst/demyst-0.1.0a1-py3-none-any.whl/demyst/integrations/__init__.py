"""
Demyst Integrations - Framework Hooks and CI/CD

This module provides integrations with:
    - PyTorch: nn.Module wrappers with integrity checks
    - JAX: Functional transformations with safety guards
    - WandB/MLflow: Experiment tracking and hypothesis validation
    - GitHub Actions: CI/CD enforcement and reporting
"""

from .ci_enforcer import CIEnforcer, ScientificIntegrityReport
from .experiment_trackers import MLflowIntegration, WandBIntegration
from .jax_hooks import JaxVariation, jax_safe_transform
from .torch_hooks import TorchModuleWrapper, TorchVariation

__all__ = [
    "TorchModuleWrapper",
    "TorchVariation",
    "JaxVariation",
    "jax_safe_transform",
    "WandBIntegration",
    "MLflowIntegration",
    "CIEnforcer",
    "ScientificIntegrityReport",
]

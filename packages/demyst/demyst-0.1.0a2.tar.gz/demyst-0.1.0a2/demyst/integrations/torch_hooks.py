"""
PyTorch Integration: Module Wrappers with Scientific Integrity Checks

Provides:
    1. TorchModuleWrapper: Wraps nn.Module with integrity monitoring
    2. TorchVariation: VariationTensor equivalent for PyTorch tensors
    3. Gradient monitoring hooks
    4. Distribution shift detection
"""

import warnings
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class GradientStats:
    """Statistics about gradient flow."""

    layer_name: str
    mean: float
    std: float
    min_val: float
    max_val: float
    num_zeros: int
    total_elements: int
    is_vanishing: bool
    is_exploding: bool


@dataclass
class ActivationStats:
    """Statistics about layer activations."""

    layer_name: str
    mean: float
    std: float
    saturation_ratio: float  # Fraction of saturated neurons
    dead_ratio: float  # Fraction of always-zero neurons


class TorchVariation:
    """
    VariationTensor equivalent for PyTorch tensors.

    Wraps PyTorch operations to preserve statistical metadata
    about what information is being collapsed.

    Usage:
        import torch
        from demyst.integrations.torch_hooks import TorchVariation

        # Instead of:
        mean_value = tensor.mean()

        # Use:
        var_tensor = TorchVariation(tensor)
        mean_value = var_tensor.collapse('mean')
        print(var_tensor.variation_history)  # See what was lost
    """

    def __init__(self, tensor: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize TorchVariation wrapper.

        Args:
            tensor: PyTorch tensor to wrap
            metadata: Optional metadata dictionary
        """
        self._tensor = tensor
        self.metadata = metadata or {}
        self._variation_history: List[Dict[str, Any]] = []

    @property
    def tensor(self) -> Any:
        """Access underlying tensor."""
        return self._tensor

    @property
    def variation_history(self) -> List[Dict[str, Any]]:
        """Get history of variation-destroying operations."""
        return self._variation_history

    def collapse(
        self, operation: str = "mean", dim: Optional[int] = None, keepdim: bool = False
    ) -> Any:
        """
        Perform collapse operation while preserving variation history.

        Args:
            operation: 'mean', 'sum', 'max', 'min'
            dim: Dimension to reduce
            keepdim: Keep reduced dimension

        Returns:
            Collapsed tensor
        """
        try:
            import torch

            # Record pre-collapse statistics
            pre_stats = {
                "operation": operation,
                "input_shape": tuple(self._tensor.shape),
                "dim": dim,
                "mean_before": float(self._tensor.mean()),
                "std_before": float(self._tensor.std()),
                "min_before": float(self._tensor.min()),
                "max_before": float(self._tensor.max()),
            }

            # Perform operation
            if operation == "mean":
                result = (
                    self._tensor.mean(dim=dim, keepdim=keepdim)
                    if dim is not None
                    else self._tensor.mean()
                )
            elif operation == "sum":
                result = (
                    self._tensor.sum(dim=dim, keepdim=keepdim)
                    if dim is not None
                    else self._tensor.sum()
                )
            elif operation == "max":
                result = (
                    self._tensor.max(dim=dim, keepdim=keepdim)[0]
                    if dim is not None
                    else self._tensor.max()
                )
            elif operation == "min":
                result = (
                    self._tensor.min(dim=dim, keepdim=keepdim)[0]
                    if dim is not None
                    else self._tensor.min()
                )
            else:
                raise ValueError(f"Unknown operation: {operation}")

            # Record post-collapse statistics
            pre_stats["output_shape"] = tuple(result.shape) if hasattr(result, "shape") else ()
            pre_stats["std_after"] = (
                float(result.std()) if hasattr(result, "std") and result.numel() > 1 else 0.0
            )

            # Calculate information loss metrics
            std_before = float(pre_stats["std_before"])  # type: ignore
            std_after = float(pre_stats["std_after"])  # type: ignore
            pre_stats["variance_destroyed"] = std_before**2 - std_after**2
            pre_stats["elements_collapsed"] = self._tensor.numel() - (
                result.numel() if hasattr(result, "numel") else 1
            )

            self._variation_history.append(pre_stats)

            return result

        except ImportError:
            warnings.warn("PyTorch not available. Returning mock result.")
            return self._tensor

    def ensemble_sum(self, dim: int = 0) -> Any:
        """
        Sum while preserving ensemble variance information.

        Useful for aggregating over batch dimension while
        tracking the variance that is being hidden.
        """
        try:
            import torch

            result = self._tensor.sum(dim=dim)

            self._variation_history.append(
                {
                    "operation": "ensemble_sum",
                    "dim": dim,
                    "input_shape": tuple(self._tensor.shape),
                    "output_shape": tuple(result.shape),
                    "preserved_variance": float(self._tensor.var(dim=dim).mean()),
                    "element_wise_std": float(self._tensor.std(dim=dim).mean()),
                }
            )

            return result

        except ImportError:
            return self._tensor

    def safe_argmax(self, dim: Optional[int] = None) -> Any:
        """
        Argmax with warnings about information loss.

        Argmax destroys ALL magnitude information, keeping only
        the index of the maximum value.
        """
        try:
            import torch

            result = self._tensor.argmax(dim=dim)

            # Calculate how much information is being lost
            if dim is not None:
                max_vals = self._tensor.max(dim=dim)[0]
                second_max = self._tensor.topk(2, dim=dim)[0][..., 1]
                margin = float((max_vals - second_max).mean())
            else:
                sorted_flat = self._tensor.flatten().sort(descending=True)[0]
                margin = (
                    float(sorted_flat[0] - sorted_flat[1]) if len(sorted_flat) > 1 else float("inf")
                )

            self._variation_history.append(
                {
                    "operation": "argmax",
                    "dim": dim,
                    "input_shape": tuple(self._tensor.shape),
                    "max_margin": margin,
                    "warning": "argmax destroys all magnitude information",
                    "values_discarded": self._tensor.numel()
                    - (result.numel() if hasattr(result, "numel") else 1),
                }
            )

            return result

        except ImportError:
            return 0


class TorchModuleWrapper:
    """
    Wraps a PyTorch nn.Module with scientific integrity monitoring.

    Features:
        1. Gradient flow monitoring
        2. Activation distribution tracking
        3. Dead neuron detection
        4. Distribution shift alerts

    Usage:
        model = MyModel()
        wrapped = TorchModuleWrapper(model)
        wrapped.register_hooks()

        # Train normally
        output = wrapped.module(input)
        loss.backward()

        # Check integrity
        report = wrapped.get_integrity_report()
    """

    GRADIENT_VANISHING_THRESHOLD = 1e-7
    GRADIENT_EXPLODING_THRESHOLD = 1e3
    SATURATION_THRESHOLD = 0.99
    DEAD_NEURON_THRESHOLD = 0.01

    def __init__(self, module: Any) -> None:
        """
        Initialize wrapper.

        Args:
            module: PyTorch nn.Module to wrap
        """
        self.module = module
        self._gradient_stats: Dict[str, List[GradientStats]] = {}
        self._activation_stats: Dict[str, List[ActivationStats]] = {}
        self._hooks: List[Any] = []
        self._forward_hooks: List[Any] = []

    def register_hooks(self) -> None:
        """Register gradient and activation monitoring hooks."""
        try:
            import torch.nn as nn

            for name, layer in self.module.named_modules():
                if len(list(layer.children())) == 0:  # Leaf module
                    # Gradient hook
                    hook = layer.register_full_backward_hook(self._make_gradient_hook(name))
                    self._hooks.append(hook)

                    # Activation hook
                    fwd_hook = layer.register_forward_hook(self._make_activation_hook(name))
                    self._forward_hooks.append(fwd_hook)

        except ImportError:
            warnings.warn("PyTorch not available. Hooks not registered.")

    def remove_hooks(self) -> None:
        """Remove all registered hooks."""
        for hook in self._hooks + self._forward_hooks:
            hook.remove()
        self._hooks = []
        self._forward_hooks = []

    def _make_gradient_hook(self, layer_name: str) -> Callable:
        """Create a gradient monitoring hook for a layer."""

        def hook(module: Any, grad_input: Any, grad_output: Any) -> None:
            try:
                import torch

                if grad_output[0] is None:
                    return

                grad = grad_output[0]
                stats = GradientStats(
                    layer_name=layer_name,
                    mean=float(grad.mean()),
                    std=float(grad.std()),
                    min_val=float(grad.min()),
                    max_val=float(grad.max()),
                    num_zeros=int((grad.abs() < 1e-10).sum()),
                    total_elements=grad.numel(),
                    is_vanishing=float(grad.abs().mean()) < self.GRADIENT_VANISHING_THRESHOLD,
                    is_exploding=float(grad.abs().max()) > self.GRADIENT_EXPLODING_THRESHOLD,
                )

                if layer_name not in self._gradient_stats:
                    self._gradient_stats[layer_name] = []
                self._gradient_stats[layer_name].append(stats)

                # Warn on issues
                if stats.is_vanishing:
                    warnings.warn(
                        f"DEMYST: Vanishing gradient detected in {layer_name}. "
                        f"Mean gradient: {stats.mean:.2e}"
                    )
                if stats.is_exploding:
                    warnings.warn(
                        f"DEMYST: Exploding gradient detected in {layer_name}. "
                        f"Max gradient: {stats.max_val:.2e}"
                    )

            except Exception as e:
                pass  # Don't break training on monitoring errors

        return hook

    def _make_activation_hook(self, layer_name: str) -> Callable:
        """Create an activation monitoring hook for a layer."""

        def hook(module: Any, input: Any, output: Any) -> None:
            try:
                import torch

                if not isinstance(output, torch.Tensor):
                    return

                # Calculate saturation for sigmoid/tanh-like activations
                saturation_high = float((output > self.SATURATION_THRESHOLD).float().mean())
                saturation_low = float((output < -self.SATURATION_THRESHOLD).float().mean())
                saturation_ratio = saturation_high + saturation_low

                # Calculate dead neurons (always near zero)
                dead_ratio = float((output.abs() < self.DEAD_NEURON_THRESHOLD).float().mean())

                stats = ActivationStats(
                    layer_name=layer_name,
                    mean=float(output.mean()),
                    std=float(output.std()),
                    saturation_ratio=saturation_ratio,
                    dead_ratio=dead_ratio,
                )

                if layer_name not in self._activation_stats:
                    self._activation_stats[layer_name] = []
                self._activation_stats[layer_name].append(stats)

                # Warn on high saturation
                if saturation_ratio > 0.5:
                    warnings.warn(
                        f"DEMYST: High saturation in {layer_name}: {saturation_ratio:.1%}. "
                        f"Gradients will vanish."
                    )

                # Warn on dead neurons
                if dead_ratio > 0.5:
                    warnings.warn(
                        f"DEMYST: {dead_ratio:.1%} dead neurons in {layer_name}. "
                        f"Consider using LeakyReLU or check initialization."
                    )

            except Exception as e:
                pass

        return hook

    def get_integrity_report(self) -> Dict[str, Any]:
        """
        Generate a scientific integrity report for the model.

        Returns:
            Dictionary with gradient and activation analysis
        """
        report: Dict[str, Any] = {
            "gradient_health": {},
            "activation_health": {},
            "issues": [],
            "recommendations": [],
        }

        # Analyze gradient flow
        for layer_name, stats_list in self._gradient_stats.items():
            if not stats_list:
                continue

            recent = stats_list[-10:]  # Last 10 iterations
            vanishing_rate = sum(1 for s in recent if s.is_vanishing) / len(recent)
            exploding_rate = sum(1 for s in recent if s.is_exploding) / len(recent)

            report["gradient_health"][layer_name] = {
                "vanishing_rate": vanishing_rate,
                "exploding_rate": exploding_rate,
                "avg_magnitude": sum(abs(s.mean) for s in recent) / len(recent),
            }

            if vanishing_rate > 0.5:
                report["issues"].append(
                    f"Layer {layer_name}: Frequent vanishing gradients ({vanishing_rate:.0%})"
                )
                report["recommendations"].append(
                    f"Add residual connections around {layer_name} or use gradient-preserving activations"
                )

            if exploding_rate > 0.1:
                report["issues"].append(
                    f"Layer {layer_name}: Exploding gradients detected ({exploding_rate:.0%})"
                )
                report["recommendations"].append(
                    f"Add gradient clipping or reduce learning rate for {layer_name}"
                )

        # Analyze activations
        for layer_name, act_stats_list in self._activation_stats.items():
            if not act_stats_list:
                continue

            act_recent = act_stats_list[-10:]
            avg_saturation = sum(s.saturation_ratio for s in act_recent) / len(act_recent)
            avg_dead = sum(s.dead_ratio for s in act_recent) / len(act_recent)

            report["activation_health"][layer_name] = {
                "avg_saturation": avg_saturation,
                "avg_dead_ratio": avg_dead,
            }

            if avg_saturation > 0.3:
                report["issues"].append(
                    f"Layer {layer_name}: High neuron saturation ({avg_saturation:.0%})"
                )

            if avg_dead > 0.3:
                report["issues"].append(f"Layer {layer_name}: Many dead neurons ({avg_dead:.0%})")

        # Overall verdict
        if report["issues"]:
            report["verdict"] = "WARNING: Model has integrity issues that may affect training"
        else:
            report["verdict"] = "PASS: No significant integrity issues detected"

        return report

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to wrapped module."""
        return getattr(self.module, name)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Forward call to wrapped module."""
        return self.module(*args, **kwargs)

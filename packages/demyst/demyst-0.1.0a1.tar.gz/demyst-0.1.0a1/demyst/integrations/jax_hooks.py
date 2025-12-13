"""
JAX Integration: Functional Transformations with Scientific Integrity

Provides:
    1. JaxVariation: VariationTensor equivalent for JAX arrays
    2. jax_safe_transform: Decorator for integrity-preserving transformations
    3. Gradient flow analysis for JAX functions
"""

import warnings
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, cast


@dataclass
class JaxOperationRecord:
    """Record of a JAX operation with preserved metadata."""

    operation: str
    input_shape: Tuple[int, ...]
    output_shape: Tuple[int, ...]
    variance_before: float
    variance_after: float
    information_lost: float


class JaxVariation:
    """
    VariationTensor equivalent for JAX arrays.

    Wraps JAX operations to track statistical information being collapsed.

    Usage:
        import jax.numpy as jnp
        from demyst.integrations.jax_hooks import JaxVariation

        arr = jnp.array([1.0, 2.0, 3.0, 4.0, 5.0])
        var_arr = JaxVariation(arr)

        # Instead of jnp.mean(arr)
        mean_val = var_arr.collapse('mean')

        # See what information was lost
        print(var_arr.variation_history)
    """

    def __init__(self, array: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize JaxVariation wrapper.

        Args:
            array: JAX array to wrap
            metadata: Optional metadata dictionary
        """
        self._array = array
        self.metadata = metadata or {}
        self._variation_history: List[JaxOperationRecord] = []

    @property
    def array(self) -> Any:
        """Access underlying array."""
        return self._array

    @property
    def variation_history(self) -> List[Dict[str, Any]]:
        """Get history of variation-destroying operations as dicts."""
        return [
            {
                "operation": r.operation,
                "input_shape": r.input_shape,
                "output_shape": r.output_shape,
                "variance_before": r.variance_before,
                "variance_after": r.variance_after,
                "information_lost": r.information_lost,
            }
            for r in self._variation_history
        ]

    def collapse(
        self, operation: str = "mean", axis: Optional[int] = None, keepdims: bool = False
    ) -> Any:
        """
        Perform collapse operation while preserving variation history.

        Args:
            operation: 'mean', 'sum', 'max', 'min'
            axis: Axis to reduce
            keepdims: Keep reduced dimension

        Returns:
            Collapsed array
        """
        try:
            import jax.numpy as jnp

            # Record pre-collapse statistics
            input_shape = tuple(self._array.shape)
            variance_before = float(jnp.var(self._array))

            # Perform operation
            if operation == "mean":
                result = jnp.mean(self._array, axis=axis, keepdims=keepdims)
            elif operation == "sum":
                result = jnp.sum(self._array, axis=axis, keepdims=keepdims)
            elif operation == "max":
                result = jnp.max(self._array, axis=axis, keepdims=keepdims)
            elif operation == "min":
                result = jnp.min(self._array, axis=axis, keepdims=keepdims)
            else:
                raise ValueError(f"Unknown operation: {operation}")

            # Record post-collapse statistics
            output_shape = tuple(result.shape) if hasattr(result, "shape") else ()
            variance_after = (
                float(jnp.var(result)) if hasattr(result, "shape") and result.size > 1 else 0.0
            )

            record = JaxOperationRecord(
                operation=operation,
                input_shape=input_shape,
                output_shape=output_shape,
                variance_before=variance_before,
                variance_after=variance_after,
                information_lost=variance_before - variance_after,
            )
            self._variation_history.append(record)

            return result

        except ImportError:
            warnings.warn("JAX not available. Returning original array.")
            return self._array

    def safe_reduce(
        self, reduce_fn: Callable, axis: Optional[int] = None, operation_name: str = "custom_reduce"
    ) -> Any:
        """
        Apply a custom reduction function while tracking variance loss.

        Args:
            reduce_fn: JAX reduction function (e.g., jnp.mean)
            axis: Axis to reduce
            operation_name: Name for logging

        Returns:
            Reduced array
        """
        try:
            import jax.numpy as jnp

            variance_before = float(jnp.var(self._array))
            result = reduce_fn(self._array, axis=axis)
            variance_after = (
                float(jnp.var(result)) if hasattr(result, "shape") and result.size > 1 else 0.0
            )

            record = JaxOperationRecord(
                operation=operation_name,
                input_shape=tuple(self._array.shape),
                output_shape=tuple(result.shape) if hasattr(result, "shape") else (),
                variance_before=variance_before,
                variance_after=variance_after,
                information_lost=variance_before - variance_after,
            )
            self._variation_history.append(record)

            return result

        except ImportError:
            return self._array


def jax_safe_transform(
    track_gradients: bool = True, warn_on_vanishing: bool = True, vanishing_threshold: float = 1e-7
) -> Callable:
    """
    Decorator for JAX functions that adds scientific integrity checks.

    Usage:
        @jax_safe_transform(track_gradients=True)
        def my_loss_fn(params, x, y):
            pred = model.apply(params, x)
            return jnp.mean((pred - y) ** 2)

    Args:
        track_gradients: Whether to track gradient statistics
        warn_on_vanishing: Whether to warn on vanishing gradients
        vanishing_threshold: Threshold for vanishing gradient detection
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = fn(*args, **kwargs)

            # If tracking gradients, wrap in gradient analysis
            if track_gradients:
                try:
                    import jax
                    import jax.numpy as jnp

                    # Get gradients if this is a scalar loss
                    if hasattr(result, "shape") and result.shape == ():
                        grad_fn = jax.grad(fn)
                        try:
                            grads = grad_fn(*args, **kwargs)

                            # Analyze gradients
                            def analyze_grad_tree(tree: Any, prefix: str = "") -> List[str]:
                                issues = []
                                if isinstance(tree, dict):
                                    for k, v in tree.items():
                                        issues.extend(analyze_grad_tree(v, f"{prefix}.{k}"))
                                elif hasattr(tree, "shape"):
                                    grad_magnitude = float(jnp.abs(tree).mean())
                                    if grad_magnitude < vanishing_threshold:
                                        issues.append(
                                            f"Vanishing gradient at {prefix}: {grad_magnitude:.2e}"
                                        )
                                return issues

                            # Only analyze if grads is a pytree structure we can handle
                            if isinstance(grads, (dict, tuple, list)) or hasattr(grads, "shape"):
                                issues = analyze_grad_tree(grads, fn.__name__)
                                if issues and warn_on_vanishing:
                                    for issue in issues[:5]:  # Limit warnings
                                        warnings.warn(f"DEMYST: {issue}")

                        except Exception:
                            pass  # Don't break on gradient analysis failures

                except ImportError:
                    pass

            return result

        # Attach metadata for introspection
        wrapper_with_attrs = cast(Any, wrapper)
        wrapper_with_attrs._demyst_tracked = True
        wrapper_with_attrs._demyst_config = {
            "track_gradients": track_gradients,
            "warn_on_vanishing": warn_on_vanishing,
            "vanishing_threshold": vanishing_threshold,
        }

        return wrapper

    return decorator


class JaxIntegrityAnalyzer:
    """
    Analyzes JAX computation graphs for scientific integrity issues.

    Can detect:
        1. Collapse operations that hide variance
        2. Numerical stability issues
        3. Gradient flow problems
    """

    def __init__(self) -> None:
        self.operation_log: List[Dict[str, Any]] = []
        self.issues: List[str] = []

    def analyze_function(self, fn: Callable, sample_inputs: Tuple) -> Dict[str, Any]:
        """
        Analyze a JAX function for potential integrity issues.

        Args:
            fn: JAX function to analyze
            sample_inputs: Sample inputs for tracing

        Returns:
            Analysis report
        """
        report: Dict[str, Any] = {
            "function_name": fn.__name__ if hasattr(fn, "__name__") else str(fn),
            "collapse_operations": [],
            "numerical_risks": [],
            "recommendations": [],
        }

        try:
            import jax
            import jax.numpy as jnp
            from jax import make_jaxpr

            # Get JAXpr (computation graph)
            jaxpr = make_jaxpr(fn)(*sample_inputs)

            # Analyze operations in the graph
            for eqn in jaxpr.jaxpr.eqns:
                prim_name = eqn.primitive.name

                # Check for collapsing operations
                if prim_name in ["reduce_sum", "reduce_mean", "reduce_max", "reduce_min"]:
                    report["collapse_operations"].append(
                        {
                            "operation": prim_name,
                            "warning": f"{prim_name} destroys variance information",
                        }
                    )

                # Check for numerical stability risks
                if prim_name in ["exp", "log", "div"]:
                    report["numerical_risks"].append(
                        {
                            "operation": prim_name,
                            "risk": f"{prim_name} can cause numerical overflow/underflow",
                        }
                    )

            # Generate recommendations
            if report["collapse_operations"]:
                report["recommendations"].append(
                    "Consider using JaxVariation wrapper to track variance loss"
                )

            if report["numerical_risks"]:
                report["recommendations"].append(
                    "Consider using jax.nn.log_softmax instead of log(softmax) for stability"
                )

        except ImportError:
            report["error"] = "JAX not available for analysis"
        except Exception as e:
            report["error"] = str(e)

        return report

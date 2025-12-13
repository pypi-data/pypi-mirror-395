"""
Lazy Import System for Demyst

Provides strict lazy loading for heavy dependencies (torch, jax, pandas, scipy, etc.)
to keep CLI startup time under 100ms. Dependencies are only imported when actually needed.

Usage:
    from demyst.lazy import torch, jax, pandas

    # The import happens lazily when first accessed
    if torch.available:
        tensor = torch.module.tensor([1, 2, 3])
"""

from __future__ import annotations

import importlib
import sys
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar, Union

# =============================================================================
# Lazy Module Implementation
# =============================================================================


@dataclass
class ImportStats:
    """Statistics about lazy imports."""

    module_name: str
    import_time_ms: float
    success: bool
    error: Optional[str] = None


class LazyModule:
    """
    A lazy-loading module wrapper.

    The actual module is only imported when first accessed.
    Provides availability checking and graceful error handling.
    """

    def __init__(
        self,
        module_name: str,
        package: Optional[str] = None,
        fallback: Optional[Callable[[], Any]] = None,
    ) -> None:
        """
        Initialize a lazy module.

        Args:
            module_name: Full module name (e.g., 'torch', 'jax.numpy')
            package: Optional package for relative imports
            fallback: Optional function to call if import fails
        """
        self._module_name = module_name
        self._package = package
        self._fallback = fallback
        self._module: Any = None
        self._loaded = False
        self._available: Optional[bool] = None
        self._import_error: Optional[Exception] = None
        self._import_time_ms: float = 0.0

    @property
    def module_name(self) -> str:
        """Get the module name."""
        return self._module_name

    @property
    def available(self) -> bool:
        """Check if the module is available (can be imported)."""
        if self._available is None:
            self._check_availability()
        return self._available or False

    @property
    def loaded(self) -> bool:
        """Check if the module has been loaded."""
        return self._loaded

    @property
    def module(self) -> Any:
        """
        Get the actual module, loading it if necessary.

        Returns:
            The imported module

        Raises:
            ImportError: If the module cannot be imported
        """
        if not self._loaded:
            self._load()
        if self._module is None:
            raise ImportError(
                f"Module '{self._module_name}' is not available: {self._import_error}"
            )
        return self._module

    @property
    def import_error(self) -> Optional[Exception]:
        """Get the import error if any."""
        return self._import_error

    @property
    def import_time_ms(self) -> float:
        """Get the import time in milliseconds."""
        return self._import_time_ms

    def _check_availability(self) -> None:
        """Check if the module can be imported without loading it."""
        try:
            # Use find_spec to check availability without importing
            import importlib.util

            spec = importlib.util.find_spec(self._module_name)
            self._available = spec is not None
        except (ImportError, ModuleNotFoundError, ValueError):
            self._available = False

    def _load(self) -> None:
        """Actually load the module."""
        if self._loaded:
            return

        start_time = time.perf_counter()

        try:
            self._module = importlib.import_module(self._module_name, self._package)
            self._available = True
        except Exception as e:
            self._import_error = e
            self._available = False
            if self._fallback:
                try:
                    self._module = self._fallback()
                except Exception:
                    pass

        self._import_time_ms = (time.perf_counter() - start_time) * 1000
        self._loaded = True

    def __getattr__(self, name: str) -> Any:
        """Proxy attribute access to the actual module."""
        return getattr(self.module, name)

    def __repr__(self) -> str:
        status = "loaded" if self._loaded else ("available" if self._available else "unavailable")
        return f"<LazyModule '{self._module_name}' ({status})>"

    def get_stats(self) -> ImportStats:
        """Get import statistics."""
        return ImportStats(
            module_name=self._module_name,
            import_time_ms=self._import_time_ms,
            success=self._available or False,
            error=str(self._import_error) if self._import_error else None,
        )


# =============================================================================
# Module Group for Related Imports
# =============================================================================


class LazyModuleGroup:
    """
    A group of related lazy modules that can be loaded together.

    Useful for loading an entire package's submodules efficiently.
    """

    def __init__(self, base_module: str) -> None:
        self._base_module = base_module
        self._modules: Dict[str, LazyModule] = {}
        self._base = LazyModule(base_module)

    @property
    def available(self) -> bool:
        """Check if the base module is available."""
        return self._base.available

    @property
    def base(self) -> Any:
        """Get the base module."""
        return self._base.module

    def submodule(self, name: str) -> LazyModule:
        """Get or create a submodule."""
        full_name = f"{self._base_module}.{name}"
        if full_name not in self._modules:
            self._modules[full_name] = LazyModule(full_name)
        return self._modules[full_name]

    def __getattr__(self, name: str) -> Any:
        """Access submodules as attributes."""
        if name.startswith("_"):
            raise AttributeError(name)
        return self.submodule(name).module


# =============================================================================
# Pre-configured Lazy Modules
# =============================================================================

# Deep Learning Frameworks
torch = LazyModule("torch")
jax = LazyModule("jax")
tensorflow = LazyModule("tensorflow")

# Data Science
numpy = LazyModule("numpy")
pandas = LazyModule("pandas")
scipy = LazyModule("scipy")

# ML Libraries
sklearn = LazyModule("sklearn")
xgboost = LazyModule("xgboost")
lightgbm = LazyModule("lightgbm")

# Visualization
matplotlib = LazyModule("matplotlib")
seaborn = LazyModule("seaborn")
plotly = LazyModule("plotly")

# Experiment Tracking
wandb = LazyModule("wandb")
mlflow = LazyModule("mlflow")

# NLP
transformers = LazyModule("transformers")
spacy = LazyModule("spacy")


# =============================================================================
# Import Manager
# =============================================================================


class ImportManager:
    """
    Central manager for lazy imports.

    Provides centralized tracking, profiling, and control over lazy imports.
    """

    def __init__(self) -> None:
        self._modules: Dict[str, LazyModule] = {}
        self._preload_list: Set[str] = set()
        self._stats: List[ImportStats] = []

    def register(self, module: LazyModule) -> None:
        """Register a lazy module."""
        self._modules[module.module_name] = module

    def get(self, module_name: str) -> LazyModule:
        """Get or create a lazy module."""
        if module_name not in self._modules:
            self._modules[module_name] = LazyModule(module_name)
        return self._modules[module_name]

    def preload(self, *module_names: str) -> None:
        """Mark modules for preloading."""
        self._preload_list.update(module_names)

    def do_preload(self) -> None:
        """Actually preload marked modules."""
        for name in self._preload_list:
            module = self.get(name)
            if module.available and not module.loaded:
                try:
                    _ = module.module
                    self._stats.append(module.get_stats())
                except ImportError:
                    pass

    def get_stats(self) -> List[ImportStats]:
        """Get import statistics for all loaded modules."""
        stats = []
        for module in self._modules.values():
            if module.loaded:
                stats.append(module.get_stats())
        return stats

    def get_total_import_time_ms(self) -> float:
        """Get total time spent importing modules."""
        return sum(s.import_time_ms for s in self.get_stats())

    def available_modules(self) -> List[str]:
        """List all available (importable) modules."""
        return [name for name, module in self._modules.items() if module.available]

    def loaded_modules(self) -> List[str]:
        """List all currently loaded modules."""
        return [name for name, module in self._modules.items() if module.loaded]


# Global import manager
_manager: Optional[ImportManager] = None


def get_import_manager() -> ImportManager:
    """Get the global import manager."""
    global _manager
    if _manager is None:
        _manager = ImportManager()
        # Register pre-configured modules
        for mod in [
            torch,
            jax,
            tensorflow,
            numpy,
            pandas,
            scipy,
            sklearn,
            xgboost,
            lightgbm,
            matplotlib,
            seaborn,
            plotly,
            wandb,
            mlflow,
            transformers,
            spacy,
        ]:
            _manager.register(mod)
    return _manager


# =============================================================================
# Convenience Functions
# =============================================================================


def lazy_import(module_name: str) -> LazyModule:
    """
    Create a lazy import for a module.

    Args:
        module_name: The module to import lazily

    Returns:
        LazyModule instance

    Example:
        np = lazy_import("numpy")
        # numpy is not imported yet
        arr = np.array([1, 2, 3])  # now numpy is imported
    """
    return get_import_manager().get(module_name)


def require(module_name: str, feature: str = "this feature") -> Any:
    """
    Require a module, raising a helpful error if unavailable.

    Args:
        module_name: The module to require
        feature: Description of the feature requiring this module

    Returns:
        The imported module

    Raises:
        ImportError: With helpful message if module unavailable
    """
    module = lazy_import(module_name)
    if not module.available:
        raise ImportError(
            f"Module '{module_name}' is required for {feature}. "
            f"Install it with: pip install {module_name}"
        )
    return module.module


def check_imports(*module_names: str) -> Dict[str, bool]:
    """
    Check availability of multiple modules.

    Args:
        *module_names: Names of modules to check

    Returns:
        Dict mapping module name to availability
    """
    return {name: lazy_import(name).available for name in module_names}


def import_time_report() -> str:
    """
    Generate a report of import times.

    Returns:
        Formatted string report
    """
    manager = get_import_manager()
    stats = manager.get_stats()

    if not stats:
        return "No modules loaded yet."

    lines = ["Module Import Time Report", "=" * 40]
    stats.sort(key=lambda s: s.import_time_ms, reverse=True)

    for s in stats:
        status = "OK" if s.success else f"FAILED: {s.error}"
        lines.append(f"  {s.module_name}: {s.import_time_ms:.1f}ms ({status})")

    total = manager.get_total_import_time_ms()
    lines.append("=" * 40)
    lines.append(f"Total: {total:.1f}ms")

    return "\n".join(lines)


# =============================================================================
# Type Hints Support
# =============================================================================

# For type checking, provide module type hints without importing
if False:  # TYPE_CHECKING
    import jax as _jax
    import numpy as _numpy
    import pandas as _pandas
    import scipy as _scipy
    import torch as _torch

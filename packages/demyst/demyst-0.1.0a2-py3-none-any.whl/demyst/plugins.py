"""
Demyst Plugin System

Provides a robust plugin architecture for extending Demyst with custom guards,
fixers, and analyzers. Plugins can be discovered via entry points or registered
programmatically.

Usage:
    # Define a custom guard plugin
    class MyCustomGuard(GuardPlugin):
        name = "my_guard"
        description = "My custom analysis"

        def analyze(self, source: str) -> Dict[str, Any]:
            # ... analysis logic
            return {"violations": [...]}

    # Register via entry points in pyproject.toml:
    # [project.entry-points."demyst.guards"]
    # my_guard = "my_package.guards:MyCustomGuard"
"""

from __future__ import annotations

import importlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Type, Union, cast

from demyst.exceptions import (
    PluginError,
    PluginLoadError,
    PluginNotFoundError,
    PluginValidationError,
)

logger = logging.getLogger(__name__)

# Entry point group names
GUARD_ENTRY_POINT = "demyst.guards"
FIXER_ENTRY_POINT = "demyst.fixers"
REPORTER_ENTRY_POINT = "demyst.reporters"


# =============================================================================
# Plugin Interfaces
# =============================================================================


class PluginInterface(ABC):
    """
    Base interface for all Demyst plugins.

    All plugin types must implement this interface.
    """

    # Required class attributes
    name: str = ""
    description: str = ""
    version: str = "1.0.0"

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration.

        Args:
            config: Plugin-specific configuration
        """
        pass

    def validate(self) -> List[str]:
        """
        Validate the plugin is properly configured.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        if not self.name:
            errors.append("Plugin must have a 'name' attribute")
        if not self.description:
            errors.append("Plugin must have a 'description' attribute")
        return errors


class GuardPlugin(PluginInterface):
    """
    Interface for guard plugins that analyze code.

    Guards detect issues in code without modifying it.
    """

    # Severity levels for issues
    SEVERITY_CRITICAL = "critical"
    SEVERITY_WARNING = "warning"
    SEVERITY_INFO = "info"

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize with default behavior."""
        self.config = config
        self.enabled = config.get("enabled", True)
        self.severity = config.get("severity", self.SEVERITY_WARNING)

    @abstractmethod
    def analyze(self, source: str) -> Dict[str, Any]:
        """
        Analyze source code for issues.

        Args:
            source: Python source code

        Returns:
            Dictionary with:
                - violations: List of detected violations
                - summary: Optional summary information
                - error: Optional error message if analysis failed
        """
        pass

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a file. Default implementation reads and calls analyze().

        Args:
            file_path: Path to the file

        Returns:
            Analysis results
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            return self.analyze(source)
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                source = f.read()
            return self.analyze(source)
        except Exception as e:
            return {"error": str(e), "violations": []}


class FixerPlugin(PluginInterface):
    """
    Interface for fixer plugins that modify code.

    Fixers automatically fix detected issues.
    """

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize with default behavior."""
        self.config = config
        self.dry_run = config.get("dry_run", False)

    @abstractmethod
    def can_fix(self, violation: Dict[str, Any]) -> bool:
        """
        Check if this fixer can fix a violation.

        Args:
            violation: Violation to check

        Returns:
            True if this fixer can handle the violation
        """
        pass

    @abstractmethod
    def fix(
        self, source: str, violations: List[Dict[str, Any]]
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Fix violations in source code.

        Args:
            source: Python source code
            violations: List of violations to fix

        Returns:
            Tuple of (fixed_source, list_of_applied_fixes)
        """
        pass


class ReporterPlugin(PluginInterface):
    """
    Interface for reporter plugins that format output.

    Reporters generate reports in various formats.
    """

    # Supported formats
    supported_formats: List[str] = []

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize with default behavior."""
        self.config = config

    @abstractmethod
    def generate(self, results: Dict[str, Any], format: str = "text") -> str:
        """
        Generate a report from analysis results.

        Args:
            results: Analysis results
            format: Output format

        Returns:
            Formatted report string
        """
        pass


# =============================================================================
# Plugin Discovery and Management
# =============================================================================


@dataclass
class PluginInfo:
    """Information about a registered plugin."""

    name: str
    plugin_class: Type[PluginInterface]
    plugin_type: str
    description: str = ""
    version: str = "1.0.0"
    entry_point: Optional[str] = None
    loaded: bool = False
    instance: Optional[PluginInterface] = None


class PluginRegistry:
    """
    Central registry for all Demyst plugins.

    Handles plugin discovery, loading, and lifecycle management.
    """

    def __init__(self) -> None:
        self._guards: Dict[str, PluginInfo] = {}
        self._fixers: Dict[str, PluginInfo] = {}
        self._reporters: Dict[str, PluginInfo] = {}
        self._discovered = False

    def discover_plugins(self, entry_point_groups: Optional[List[str]] = None) -> int:
        """
        Discover plugins from entry points.

        Args:
            entry_point_groups: List of entry point groups to scan

        Returns:
            Number of plugins discovered
        """
        if entry_point_groups is None:
            entry_point_groups = [
                GUARD_ENTRY_POINT,
                FIXER_ENTRY_POINT,
                REPORTER_ENTRY_POINT,
            ]

        count = 0

        try:
            # Try importlib.metadata (Python 3.9+)
            try:
                from importlib.metadata import entry_points

                eps_dict = entry_points()

                for group in entry_point_groups:
                    # Handle both dict-style and SelectableGroups
                    eps: Iterable[Any] = []
                    if hasattr(eps_dict, "select"):
                        eps = eps_dict.select(group=group)
                    elif hasattr(eps_dict, "get"):
                        eps = eps_dict.get(group, [])

                    for ep in eps:
                        try:
                            self._register_entry_point(ep, group)
                            count += 1
                        except Exception as e:
                            logger.warning(f"Failed to load plugin {ep.name}: {e}")

            except ImportError:
                # Fallback to pkg_resources
                import pkg_resources  # type: ignore

                for group in entry_point_groups:
                    for ep in pkg_resources.iter_entry_points(group):
                        try:
                            self._register_entry_point_legacy(ep, group)
                            count += 1
                        except Exception as e:
                            logger.warning(f"Failed to load plugin {ep.name}: {e}")

        except Exception as e:
            logger.debug(f"Plugin discovery failed: {e}")

        self._discovered = True
        return count

    def _register_entry_point(self, ep: Any, group: str) -> None:
        """Register a plugin from an entry point."""
        plugin_class = ep.load()
        self.register(plugin_class, entry_point=f"{group}:{ep.name}")

    def _register_entry_point_legacy(self, ep: Any, group: str) -> None:
        """Register a plugin from a pkg_resources entry point."""
        plugin_class = ep.load()
        self.register(plugin_class, entry_point=f"{group}:{ep.name}")

    def register(
        self, plugin_class: Type[PluginInterface], entry_point: Optional[str] = None
    ) -> PluginInfo:
        """
        Register a plugin class.

        Args:
            plugin_class: The plugin class to register
            entry_point: Optional entry point string

        Returns:
            PluginInfo for the registered plugin

        Raises:
            PluginValidationError: If the plugin is invalid
        """
        # Validate plugin class
        if not hasattr(plugin_class, "name") or not plugin_class.name:
            raise PluginValidationError(plugin_class.__name__, missing_interface="name attribute")

        # Determine plugin type
        if issubclass(plugin_class, GuardPlugin):
            plugin_type = "guard"
            registry = self._guards
        elif issubclass(plugin_class, FixerPlugin):
            plugin_type = "fixer"
            registry = self._fixers
        elif issubclass(plugin_class, ReporterPlugin):
            plugin_type = "reporter"
            registry = self._reporters
        else:
            raise PluginValidationError(
                plugin_class.__name__,
                validation_errors=[
                    "Plugin must inherit from GuardPlugin, FixerPlugin, or ReporterPlugin"
                ],
            )

        info = PluginInfo(
            name=plugin_class.name,
            plugin_class=plugin_class,
            plugin_type=plugin_type,
            description=getattr(plugin_class, "description", ""),
            version=getattr(plugin_class, "version", "1.0.0"),
            entry_point=entry_point,
        )

        registry[info.name] = info
        logger.debug(f"Registered {plugin_type} plugin: {info.name}")
        return info

    def get_guard(self, name: str, config: Optional[Dict[str, Any]] = None) -> GuardPlugin:
        """
        Get an initialized guard plugin by name.

        Args:
            name: Plugin name
            config: Optional configuration

        Returns:
            Initialized GuardPlugin instance

        Raises:
            PluginNotFoundError: If plugin not found
            PluginLoadError: If plugin fails to load
        """
        if name not in self._guards:
            if not self._discovered:
                self.discover_plugins()
            if name not in self._guards:
                raise PluginNotFoundError(name, GUARD_ENTRY_POINT)

        info = self._guards[name]
        return cast(GuardPlugin, self._get_instance(info, config or {}))

    def get_fixer(self, name: str, config: Optional[Dict[str, Any]] = None) -> FixerPlugin:
        """Get an initialized fixer plugin by name."""
        if name not in self._fixers:
            if not self._discovered:
                self.discover_plugins()
            if name not in self._fixers:
                raise PluginNotFoundError(name, FIXER_ENTRY_POINT)

        info = self._fixers[name]
        return cast(FixerPlugin, self._get_instance(info, config or {}))

    def get_reporter(self, name: str, config: Optional[Dict[str, Any]] = None) -> ReporterPlugin:
        """Get an initialized reporter plugin by name."""
        if name not in self._reporters:
            if not self._discovered:
                self.discover_plugins()
            if name not in self._reporters:
                raise PluginNotFoundError(name, REPORTER_ENTRY_POINT)

        info = self._reporters[name]
        return cast(ReporterPlugin, self._get_instance(info, config or {}))

    def _get_instance(self, info: PluginInfo, config: Dict[str, Any]) -> PluginInterface:
        """Get or create a plugin instance."""
        if info.instance is not None:
            return info.instance

        try:
            instance = info.plugin_class()
            instance.initialize(config)

            # Validate
            errors = instance.validate()
            if errors:
                raise PluginValidationError(info.name, validation_errors=errors)

            info.instance = instance
            info.loaded = True
            return instance

        except Exception as e:
            raise PluginLoadError(info.name, str(e), e)

    def list_guards(self) -> List[PluginInfo]:
        """List all registered guard plugins."""
        if not self._discovered:
            self.discover_plugins()
        return list(self._guards.values())

    def list_fixers(self) -> List[PluginInfo]:
        """List all registered fixer plugins."""
        if not self._discovered:
            self.discover_plugins()
        return list(self._fixers.values())

    def list_reporters(self) -> List[PluginInfo]:
        """List all registered reporter plugins."""
        if not self._discovered:
            self.discover_plugins()
        return list(self._reporters.values())

    def unregister(self, name: str) -> bool:
        """Unregister a plugin by name."""
        for registry in [self._guards, self._fixers, self._reporters]:
            if name in registry:
                del registry[name]
                return True
        return False

    def clear(self) -> None:
        """Clear all registered plugins."""
        self._guards.clear()
        self._fixers.clear()
        self._reporters.clear()
        self._discovered = False


# =============================================================================
# Global Registry Instance
# =============================================================================

# Global plugin registry
_registry: Optional[PluginRegistry] = None


def get_registry() -> PluginRegistry:
    """Get the global plugin registry."""
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry


def register_guard(plugin_class: Type[GuardPlugin]) -> Type[GuardPlugin]:
    """
    Decorator to register a guard plugin.

    Example:
        @register_guard
        class MyGuard(GuardPlugin):
            name = "my_guard"
            ...
    """
    get_registry().register(plugin_class)
    return plugin_class


def register_fixer(plugin_class: Type[FixerPlugin]) -> Type[FixerPlugin]:
    """Decorator to register a fixer plugin."""
    get_registry().register(plugin_class)
    return plugin_class


def register_reporter(plugin_class: Type[ReporterPlugin]) -> Type[ReporterPlugin]:
    """Decorator to register a reporter plugin."""
    get_registry().register(plugin_class)
    return plugin_class


# =============================================================================
# Built-in Plugin Wrappers
# =============================================================================


class MirageDetectorPlugin(GuardPlugin):
    """Built-in plugin wrapper for MirageDetector."""

    name = "mirage"
    description = "Detects computational mirages (variance-destroying operations)"
    version = "1.0.0"

    def analyze(self, source: str) -> Dict[str, Any]:
        import ast

        from demyst.engine.mirage_detector import MirageDetector

        try:
            tree = ast.parse(source)
            detector = MirageDetector()
            detector.visit(tree)
            return {
                "violations": detector.mirages,
                "summary": {"total": len(detector.mirages)},
            }
        except SyntaxError as e:
            return {"error": f"Syntax error: {e}", "violations": []}


class LeakageHunterPlugin(GuardPlugin):
    """Built-in plugin wrapper for LeakageHunter."""

    name = "leakage"
    description = "Detects data leakage patterns"
    version = "1.0.0"

    def analyze(self, source: str) -> Dict[str, Any]:
        from demyst.guards.leakage_hunter import LeakageHunter

        hunter = LeakageHunter()
        return hunter.analyze(source)


class HypothesisGuardPlugin(GuardPlugin):
    """Built-in plugin wrapper for HypothesisGuard."""

    name = "hypothesis"
    description = "Checks statistical validity and p-hacking patterns"
    version = "1.0.0"

    def analyze(self, source: str) -> Dict[str, Any]:
        from demyst.guards.hypothesis_guard import HypothesisGuard

        guard = HypothesisGuard()
        return guard.analyze_code(source)


class UnitGuardPlugin(GuardPlugin):
    """Built-in plugin wrapper for UnitGuard."""

    name = "unit"
    description = "Checks dimensional consistency"
    version = "1.0.0"

    def analyze(self, source: str) -> Dict[str, Any]:
        from demyst.guards.unit_guard import UnitGuard

        guard = UnitGuard()
        return guard.analyze(source)


class TensorGuardPlugin(GuardPlugin):
    """Built-in plugin wrapper for TensorGuard."""

    name = "tensor"
    description = "Checks deep learning integrity"
    version = "1.0.0"

    def analyze(self, source: str) -> Dict[str, Any]:
        from demyst.guards.tensor_guard import TensorGuard

        guard = TensorGuard()
        return guard.analyze(source)


def register_builtin_plugins() -> None:
    """Register all built-in plugins."""
    registry = get_registry()
    for plugin in [
        MirageDetectorPlugin,
        LeakageHunterPlugin,
        HypothesisGuardPlugin,
        UnitGuardPlugin,
        TensorGuardPlugin,
    ]:
        try:
            registry.register(plugin)  # type: ignore[type-abstract]
        except Exception as e:
            logger.debug(f"Failed to register built-in plugin: {e}")

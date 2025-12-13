"""
Demyst Custom Exception Hierarchy

A robust exception hierarchy for professional-grade error handling throughout the Demyst platform.
All exceptions inherit from DemystError for easy catching at the application boundary.
"""

from typing import Any, Dict, List, Optional


class DemystError(Exception):
    """
    Base exception for all Demyst-related errors.

    This is the root of the Demyst exception hierarchy. Catching this
    exception will catch all Demyst-specific errors.

    Attributes:
        message: Human-readable error description
        details: Optional dictionary with additional context
        suggestion: Optional suggestion for fixing the error
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        self.message = message
        self.details = details or {}
        self.suggestion = suggestion
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format the exception message with details and suggestion."""
        parts = [self.message]
        if self.details:
            details_str = ", ".join(f"{k}={v!r}" for k, v in self.details.items())
            parts.append(f"[{details_str}]")
        if self.suggestion:
            parts.append(f"Suggestion: {self.suggestion}")
        return " ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to a dictionary for JSON serialization."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
            "suggestion": self.suggestion,
        }


# =============================================================================
# Configuration Errors
# =============================================================================


class ConfigurationError(DemystError):
    """
    Raised when there's an issue with Demyst configuration.

    This includes invalid config files, missing required settings,
    or incompatible configuration combinations.
    """

    def __init__(
        self,
        message: str,
        config_path: Optional[str] = None,
        invalid_key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        details = details or {}
        if config_path:
            details["config_path"] = config_path
        if invalid_key:
            details["invalid_key"] = invalid_key
        super().__init__(message, details, suggestion)


class ProfileNotFoundError(ConfigurationError):
    """Raised when a specified profile cannot be found."""

    def __init__(self, profile_name: str, available_profiles: Optional[List[str]] = None) -> None:
        details: Dict[str, Any] = {"profile_name": profile_name}
        if available_profiles:
            details["available_profiles"] = available_profiles
        suggestion = f"Use one of the available profiles: {', '.join(available_profiles or [])}"
        super().__init__(
            f"Profile '{profile_name}' not found", details=details, suggestion=suggestion
        )


class InvalidConfigValueError(ConfigurationError):
    """Raised when a configuration value is invalid."""

    def __init__(
        self,
        key: str,
        value: Any,
        expected_type: Optional[str] = None,
        allowed_values: Optional[List[Any]] = None,
    ) -> None:
        details = {"key": key, "value": value}
        if expected_type:
            details["expected_type"] = expected_type
        if allowed_values:
            details["allowed_values"] = allowed_values

        suggestion = None
        if allowed_values:
            suggestion = f"Valid values are: {', '.join(str(v) for v in allowed_values)}"
        elif expected_type:
            suggestion = f"Expected a value of type: {expected_type}"

        super().__init__(
            f"Invalid configuration value for '{key}'",
            invalid_key=key,
            details=details,
            suggestion=suggestion,
        )


# =============================================================================
# Analysis Errors
# =============================================================================


class AnalysisError(DemystError):
    """
    Base exception for errors during code analysis.

    This covers parsing errors, invalid code structures,
    and failures in any of the guard/detector components.
    """

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        line_number: Optional[int] = None,
        column: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        details = details or {}
        if file_path:
            details["file_path"] = file_path
        if line_number is not None:
            details["line"] = line_number
        if column is not None:
            details["column"] = column
        super().__init__(message, details, suggestion)
        self.file_path = file_path
        self.line_number = line_number
        self.column = column


class ParseError(AnalysisError):
    """Raised when source code cannot be parsed."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        line_number: Optional[int] = None,
        column: Optional[int] = None,
        original_error: Optional[Exception] = None,
    ) -> None:
        details = {}
        if original_error:
            details["original_error"] = str(original_error)
        super().__init__(
            message,
            file_path=file_path,
            line_number=line_number,
            column=column,
            details=details,
            suggestion="Check the file for syntax errors",
        )
        self.original_error = original_error


class GuardError(AnalysisError):
    """Raised when a guard fails during analysis."""

    def __init__(
        self,
        guard_name: str,
        message: str,
        file_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        details["guard_name"] = guard_name
        super().__init__(f"[{guard_name}] {message}", file_path=file_path, details=details)
        self.guard_name = guard_name


class MirageDetectionError(GuardError):
    """Raised when mirage detection fails."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__("MirageDetector", message, file_path, details)


class LeakageDetectionError(GuardError):
    """Raised when leakage detection fails."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__("LeakageHunter", message, file_path, details)


class DimensionalAnalysisError(GuardError):
    """Raised when dimensional analysis fails."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__("UnitGuard", message, file_path, details)


class StatisticalValidityError(GuardError):
    """Raised when statistical validity analysis fails."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__("HypothesisGuard", message, file_path, details)


class TensorIntegrityError(GuardError):
    """Raised when tensor integrity analysis fails."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__("TensorGuard", message, file_path, details)


# =============================================================================
# Transformation Errors
# =============================================================================


class TransformationError(DemystError):
    """
    Base exception for errors during code transformation.

    This covers failures in the transpiler, fixer, and
    any CST/AST transformation operations.
    """

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        transformation_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        details = details or {}
        if file_path:
            details["file_path"] = file_path
        if transformation_type:
            details["transformation_type"] = transformation_type
        super().__init__(message, details, suggestion)
        self.file_path = file_path
        self.transformation_type = transformation_type


class TranspilerError(TransformationError):
    """Raised when the transpiler fails to transform code."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        target_line: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if target_line is not None:
            details["target_line"] = target_line
        super().__init__(
            message,
            file_path=file_path,
            transformation_type="transpile",
            details=details,
            suggestion="Try running with --dry-run to preview changes first",
        )


class FixerError(TransformationError):
    """Raised when the auto-fixer fails."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        violation_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if violation_type:
            details["violation_type"] = violation_type
        super().__init__(
            message,
            file_path=file_path,
            transformation_type="fix",
            details=details,
            suggestion="Manual intervention may be required",
        )


class CSTTransformError(TransformationError):
    """Raised when a CST transformation fails."""

    def __init__(
        self,
        message: str,
        node_type: Optional[str] = None,
        file_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if node_type:
            details["node_type"] = node_type
        super().__init__(
            message,
            file_path=file_path,
            transformation_type="cst",
            details=details,
            suggestion="Report this issue if it persists",
        )


class UnsafeTransformationError(TransformationError):
    """Raised when a transformation would produce invalid or unsafe code."""

    def __init__(
        self,
        message: str,
        original_code: Optional[str] = None,
        attempted_result: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> None:
        details = {}
        if original_code:
            details["original_code"] = (
                original_code[:100] + "..." if len(original_code or "") > 100 else original_code
            )
        if attempted_result:
            details["attempted_result"] = (
                attempted_result[:100] + "..."
                if len(attempted_result or "") > 100
                else attempted_result
            )
        super().__init__(
            message,
            file_path=file_path,
            transformation_type="unsafe",
            details=details,
            suggestion="The transformation was aborted to prevent code corruption",
        )


# =============================================================================
# File Operation Errors
# =============================================================================


class FileOperationError(DemystError):
    """Base exception for file operation failures."""

    def __init__(
        self,
        message: str,
        file_path: str,
        operation: str,
        details: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        details = details or {}
        details["file_path"] = file_path
        details["operation"] = operation
        super().__init__(message, details, suggestion)
        self.file_path = file_path
        self.operation = operation


class FileReadError(FileOperationError):
    """Raised when a file cannot be read."""

    def __init__(
        self,
        file_path: str,
        reason: Optional[str] = None,
        original_error: Optional[Exception] = None,
    ) -> None:
        details = {}
        if reason:
            details["reason"] = reason
        if original_error:
            details["original_error"] = str(original_error)
        super().__init__(
            f"Failed to read file: {file_path}",
            file_path=file_path,
            operation="read",
            details=details,
            suggestion="Check file permissions and encoding",
        )
        self.original_error = original_error


class FileWriteError(FileOperationError):
    """Raised when a file cannot be written."""

    def __init__(
        self,
        file_path: str,
        reason: Optional[str] = None,
        original_error: Optional[Exception] = None,
    ) -> None:
        details = {}
        if reason:
            details["reason"] = reason
        if original_error:
            details["original_error"] = str(original_error)
        super().__init__(
            f"Failed to write file: {file_path}",
            file_path=file_path,
            operation="write",
            details=details,
            suggestion="Check file permissions and disk space",
        )
        self.original_error = original_error


# =============================================================================
# Plugin System Errors
# =============================================================================


class PluginError(DemystError):
    """Base exception for plugin-related errors."""

    def __init__(
        self,
        message: str,
        plugin_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        details = details or {}
        if plugin_name:
            details["plugin_name"] = plugin_name
        super().__init__(message, details, suggestion)
        self.plugin_name = plugin_name


class PluginNotFoundError(PluginError):
    """Raised when a plugin cannot be found."""

    def __init__(self, plugin_name: str, entry_point_group: Optional[str] = None) -> None:
        details = {}
        if entry_point_group:
            details["entry_point_group"] = entry_point_group
        super().__init__(
            f"Plugin '{plugin_name}' not found",
            plugin_name=plugin_name,
            details=details,
            suggestion="Install the plugin package or check the plugin name",
        )


class PluginLoadError(PluginError):
    """Raised when a plugin fails to load."""

    def __init__(
        self, plugin_name: str, reason: str, original_error: Optional[Exception] = None
    ) -> None:
        details = {"reason": reason}
        if original_error:
            details["original_error"] = str(original_error)
        super().__init__(
            f"Failed to load plugin '{plugin_name}': {reason}",
            plugin_name=plugin_name,
            details=details,
            suggestion="Check plugin compatibility and dependencies",
        )
        self.original_error = original_error


class PluginValidationError(PluginError):
    """Raised when a plugin fails validation."""

    def __init__(
        self,
        plugin_name: str,
        missing_interface: Optional[str] = None,
        validation_errors: Optional[List[str]] = None,
    ) -> None:
        details: Dict[str, Any] = {}
        if missing_interface:
            details["missing_interface"] = missing_interface
        if validation_errors:
            details["validation_errors"] = validation_errors
        super().__init__(
            f"Plugin '{plugin_name}' failed validation",
            plugin_name=plugin_name,
            details=details,
            suggestion="Ensure the plugin implements the required interface",
        )


# =============================================================================
# CI/CD Errors
# =============================================================================


class CIEnforcementError(DemystError):
    """Raised when CI enforcement fails."""

    def __init__(
        self,
        message: str,
        failed_checks: Optional[List[str]] = None,
        exit_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if failed_checks:
            details["failed_checks"] = failed_checks
        if exit_code is not None:
            details["exit_code"] = exit_code
        super().__init__(
            message, details=details, suggestion="Fix the reported issues before merging"
        )
        self.failed_checks = failed_checks
        self.exit_code = exit_code


# =============================================================================
# Report Generation Errors
# =============================================================================


class ReportGenerationError(DemystError):
    """Raised when report generation fails."""

    def __init__(
        self,
        message: str,
        report_format: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if report_format:
            details["report_format"] = report_format
        super().__init__(message, details=details, suggestion="Try a different output format")
        self.report_format = report_format


class LaTeXGenerationError(ReportGenerationError):
    """Raised when LaTeX generation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, report_format="latex", details=details)


# =============================================================================
# Utility Functions
# =============================================================================


def wrap_exception(error: Exception, context: str, file_path: Optional[str] = None) -> DemystError:
    """
    Wrap a generic exception in a DemystError for consistent error handling.

    Args:
        error: The original exception
        context: Description of what operation was being performed
        file_path: Optional file path if applicable

    Returns:
        An appropriate DemystError subclass
    """
    if isinstance(error, DemystError):
        return error

    if isinstance(error, SyntaxError):
        return ParseError(
            f"{context}: {error.msg}",
            file_path=file_path or getattr(error, "filename", None),
            line_number=error.lineno,
            column=error.offset,
            original_error=error,
        )

    if isinstance(error, FileNotFoundError):
        return FileReadError(file_path or str(error), reason="File not found", original_error=error)

    if isinstance(error, PermissionError):
        return FileReadError(
            file_path or str(error), reason="Permission denied", original_error=error
        )

    if isinstance(error, UnicodeDecodeError):
        return FileReadError(
            file_path or "unknown", reason=f"Encoding error: {error.encoding}", original_error=error
        )

    # Default wrapper
    return DemystError(f"{context}: {error}", details={"original_type": type(error).__name__})

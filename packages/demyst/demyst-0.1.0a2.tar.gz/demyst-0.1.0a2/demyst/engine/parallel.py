"""
Parallel Analysis Engine for Demyst

Provides multiprocessing-based parallel analysis for processing large directories
of Python files efficiently. Uses a worker pool to analyze multiple files concurrently.

Key features:
- Automatic worker count based on CPU cores
- Progress tracking and reporting
- Graceful error handling per file
- Configurable timeouts
- Memory-efficient file processing
"""

from __future__ import annotations

import logging
import multiprocessing as mp
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, Union

from demyst.exceptions import AnalysisError, DemystError

logger = logging.getLogger(__name__)


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class FileAnalysisResult:
    """Result of analyzing a single file."""

    file_path: str
    success: bool
    duration_ms: float
    mirage_count: int = 0
    leakage_count: int = 0
    hypothesis_count: int = 0
    unit_count: int = 0
    tensor_count: int = 0
    error: Optional[str] = None
    results: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_issues(self) -> int:
        return (
            self.mirage_count
            + self.leakage_count
            + self.hypothesis_count
            + self.unit_count
            + self.tensor_count
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "success": self.success,
            "duration_ms": self.duration_ms,
            "total_issues": self.total_issues,
            "mirage_count": self.mirage_count,
            "leakage_count": self.leakage_count,
            "hypothesis_count": self.hypothesis_count,
            "unit_count": self.unit_count,
            "tensor_count": self.tensor_count,
            "error": self.error,
        }


@dataclass
class ParallelAnalysisReport:
    """Aggregated report from parallel analysis."""

    directory: str
    file_results: List[FileAnalysisResult] = field(default_factory=list)
    total_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    total_duration_ms: float = 0.0
    worker_count: int = 1

    @property
    def total_issues(self) -> int:
        return sum(r.total_issues for r in self.file_results)

    @property
    def success_rate(self) -> float:
        if self.total_files == 0:
            return 1.0
        return self.successful_files / self.total_files

    @property
    def avg_file_duration_ms(self) -> float:
        if not self.file_results:
            return 0.0
        return sum(r.duration_ms for r in self.file_results) / len(self.file_results)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "directory": self.directory,
            "total_files": self.total_files,
            "successful_files": self.successful_files,
            "failed_files": self.failed_files,
            "total_issues": self.total_issues,
            "total_duration_ms": self.total_duration_ms,
            "avg_file_duration_ms": self.avg_file_duration_ms,
            "success_rate": self.success_rate,
            "worker_count": self.worker_count,
            "files": [r.to_dict() for r in self.file_results],
        }


# =============================================================================
# Worker Functions (must be at module level for multiprocessing)
# =============================================================================


def _analyze_file_worker(args: Tuple[str, Dict[str, bool]]) -> FileAnalysisResult:
    """
    Worker function to analyze a single file.

    This function runs in a separate process, so it imports dependencies locally.

    Args:
        args: Tuple of (file_path, options_dict)

    Returns:
        FileAnalysisResult with analysis results
    """
    file_path, options = args
    start_time = time.perf_counter()

    try:
        # Read the file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                source = f.read()

        results: Dict[str, Any] = {}
        mirage_count = 0
        leakage_count = 0
        hypothesis_count = 0
        unit_count = 0
        tensor_count = 0

        # Run enabled analyses
        if options.get("mirage", True):
            try:
                import ast

                from demyst.engine.mirage_detector import MirageDetector

                tree = ast.parse(source)
                detector = MirageDetector()
                detector.visit(tree)
                mirage_count = len(detector.mirages)
                results["mirage"] = {"issues": detector.mirages}
            except Exception as e:
                results["mirage"] = {"error": str(e)}

        if options.get("leakage", True):
            try:
                from demyst.guards.leakage_hunter import LeakageHunter

                hunter = LeakageHunter()
                result = hunter.analyze(source)
                violations = result.get("violations", [])
                leakage_count = len(violations)
                results["leakage"] = result
            except Exception as e:
                results["leakage"] = {"error": str(e)}

        if options.get("hypothesis", True):
            try:
                from demyst.guards.hypothesis_guard import HypothesisGuard

                h_guard = HypothesisGuard()
                result = h_guard.analyze_code(source)
                violations = result.get("violations", [])
                hypothesis_count = len(violations)
                results["hypothesis"] = result
            except Exception as e:
                results["hypothesis"] = {"error": str(e)}

        if options.get("unit", True):
            try:
                from demyst.guards.unit_guard import UnitGuard

                u_guard = UnitGuard()
                result = u_guard.analyze(source)
                violations = result.get("violations", [])
                unit_count = len(violations)
                results["unit"] = result
            except Exception as e:
                results["unit"] = {"error": str(e)}

        if options.get("tensor", True):
            try:
                from demyst.guards.tensor_guard import TensorGuard

                t_guard = TensorGuard()
                result = t_guard.analyze(source)
                tensor_issues = (
                    len(result.get("gradient_issues", []))
                    + len(result.get("normalization_issues", []))
                    + len(result.get("reward_issues", []))
                )
                tensor_count = tensor_issues
                results["tensor"] = result
            except Exception as e:
                results["tensor"] = {"error": str(e)}

        duration_ms = (time.perf_counter() - start_time) * 1000

        return FileAnalysisResult(
            file_path=file_path,
            success=True,
            duration_ms=duration_ms,
            mirage_count=mirage_count,
            leakage_count=leakage_count,
            hypothesis_count=hypothesis_count,
            unit_count=unit_count,
            tensor_count=tensor_count,
            results=results,
        )

    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000
        return FileAnalysisResult(
            file_path=file_path,
            success=False,
            duration_ms=duration_ms,
            error=str(e),
        )


# =============================================================================
# Parallel Analyzer
# =============================================================================


class ParallelAnalyzer:
    """
    Parallel analysis engine for Demyst.

    Analyzes multiple Python files concurrently using a process pool.
    Automatically scales based on available CPU cores.

    Example:
        analyzer = ParallelAnalyzer(max_workers=4)
        report = analyzer.analyze_directory('/path/to/project')
        print(f"Found {report.total_issues} issues in {report.total_files} files")
    """

    # Default patterns to ignore
    DEFAULT_IGNORE_PATTERNS: Set[str] = {
        "__pycache__",
        ".git",
        ".venv",
        "venv",
        "node_modules",
        ".mypy_cache",
        ".pytest_cache",
        "build",
        "dist",
        ".eggs",
        "*.egg-info",
    }

    def __init__(
        self,
        max_workers: Optional[int] = None,
        use_processes: bool = True,
        timeout: Optional[float] = 60.0,
        ignore_patterns: Optional[Set[str]] = None,
        analysis_options: Optional[Dict[str, bool]] = None,
    ) -> None:
        """
        Initialize the parallel analyzer.

        Args:
            max_workers: Maximum number of parallel workers (default: CPU count)
            use_processes: Use processes (True) or threads (False)
            timeout: Timeout in seconds for each file (None = no timeout)
            ignore_patterns: Patterns to ignore (directories/files)
            analysis_options: Which analyses to run (mirage, leakage, etc.)
        """
        self.max_workers = max_workers or self._get_optimal_workers()
        self.use_processes = use_processes
        self.timeout = timeout
        self.ignore_patterns = ignore_patterns or self.DEFAULT_IGNORE_PATTERNS

        # Default analysis options - all enabled
        self.analysis_options = analysis_options or {
            "mirage": True,
            "leakage": True,
            "hypothesis": True,
            "unit": True,
            "tensor": True,
        }

        self._progress_callback: Optional[Callable[[int, int, str], None]] = None

    def _get_optimal_workers(self) -> int:
        """Get optimal number of workers based on CPU count."""
        cpu_count = os.cpu_count() or 1
        # Use slightly fewer workers than CPUs to leave room for system
        return max(1, cpu_count - 1)

    def set_progress_callback(self, callback: Callable[[int, int, str], None]) -> None:
        """
        Set a callback for progress updates.

        Args:
            callback: Function(current, total, current_file) for progress updates
        """
        self._progress_callback = callback

    def analyze_directory(
        self,
        directory: str,
        file_pattern: str = "*.py",
        recursive: bool = True,
    ) -> ParallelAnalysisReport:
        """
        Analyze all Python files in a directory in parallel.

        Args:
            directory: Directory to analyze
            file_pattern: Glob pattern for files (default: *.py)
            recursive: Search recursively (default: True)

        Returns:
            ParallelAnalysisReport with aggregated results
        """
        start_time = time.perf_counter()
        directory_path = Path(directory).resolve()

        # Find all matching files
        files = self._find_files(directory_path, file_pattern, recursive)

        if not files:
            return ParallelAnalysisReport(
                directory=str(directory_path),
                total_files=0,
                worker_count=self.max_workers,
            )

        # Analyze files in parallel
        results = self._analyze_files(files)

        # Build report
        total_duration_ms = (time.perf_counter() - start_time) * 1000
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        return ParallelAnalysisReport(
            directory=str(directory_path),
            file_results=results,
            total_files=len(files),
            successful_files=len(successful),
            failed_files=len(failed),
            total_duration_ms=total_duration_ms,
            worker_count=self.max_workers,
        )

    def analyze_files(
        self,
        file_paths: List[str],
    ) -> ParallelAnalysisReport:
        """
        Analyze a list of files in parallel.

        Args:
            file_paths: List of file paths to analyze

        Returns:
            ParallelAnalysisReport with results
        """
        start_time = time.perf_counter()

        if not file_paths:
            return ParallelAnalysisReport(
                directory="<multiple>",
                total_files=0,
                worker_count=self.max_workers,
            )

        results = self._analyze_files(file_paths)

        total_duration_ms = (time.perf_counter() - start_time) * 1000
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        return ParallelAnalysisReport(
            directory="<multiple>",
            file_results=results,
            total_files=len(file_paths),
            successful_files=len(successful),
            failed_files=len(failed),
            total_duration_ms=total_duration_ms,
            worker_count=self.max_workers,
        )

    def _find_files(self, directory: Path, pattern: str, recursive: bool) -> List[str]:
        """Find all matching files in directory."""
        files: List[str] = []

        if recursive:
            glob_pattern = f"**/{pattern}"
        else:
            glob_pattern = pattern

        for path in directory.glob(glob_pattern):
            if path.is_file() and self._should_include(path):
                files.append(str(path))

        return sorted(files)

    def _should_include(self, path: Path) -> bool:
        """Check if a file should be included in analysis."""
        # Check against ignore patterns
        parts = path.parts
        for pattern in self.ignore_patterns:
            if any(pattern in part for part in parts):
                return False

        # Skip test files by default
        if path.name.startswith("test_") or path.name.endswith("_test.py"):
            return False

        return True

    def _analyze_files(self, file_paths: List[str]) -> List[FileAnalysisResult]:
        """Analyze multiple files in parallel."""
        results: List[FileAnalysisResult] = []
        total = len(file_paths)

        # Prepare arguments for workers
        worker_args = [(fp, self.analysis_options) for fp in file_paths]

        # Choose executor type
        ExecutorClass = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor

        try:
            with ExecutorClass(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_file = {
                    executor.submit(_analyze_file_worker, args): args[0] for args in worker_args
                }

                # Collect results as they complete
                completed = 0
                for future in as_completed(future_to_file, timeout=self.timeout):
                    file_path = future_to_file[future]
                    completed += 1

                    try:
                        result = future.result(timeout=self.timeout)
                        results.append(result)
                    except Exception as e:
                        # Handle timeout or other errors
                        results.append(
                            FileAnalysisResult(
                                file_path=file_path,
                                success=False,
                                duration_ms=0,
                                error=f"Worker error: {e}",
                            )
                        )

                    # Progress callback
                    if self._progress_callback:
                        self._progress_callback(completed, total, file_path)

        except Exception as e:
            logger.error(f"Parallel analysis failed: {e}")
            # Return partial results
            pass

        return results


# =============================================================================
# Convenience Functions
# =============================================================================


def analyze_directory_parallel(
    directory: str,
    max_workers: Optional[int] = None,
    **kwargs: Any,
) -> ParallelAnalysisReport:
    """
    Convenience function to analyze a directory in parallel.

    Args:
        directory: Directory to analyze
        max_workers: Maximum number of workers
        **kwargs: Additional options passed to ParallelAnalyzer

    Returns:
        ParallelAnalysisReport with results
    """
    analyzer = ParallelAnalyzer(max_workers=max_workers, **kwargs)
    return analyzer.analyze_directory(directory)


def analyze_files_parallel(
    files: List[str],
    max_workers: Optional[int] = None,
    **kwargs: Any,
) -> ParallelAnalysisReport:
    """
    Convenience function to analyze files in parallel.

    Args:
        files: List of file paths
        max_workers: Maximum number of workers
        **kwargs: Additional options passed to ParallelAnalyzer

    Returns:
        ParallelAnalysisReport with results
    """
    analyzer = ParallelAnalyzer(max_workers=max_workers, **kwargs)
    return analyzer.analyze_files(files)

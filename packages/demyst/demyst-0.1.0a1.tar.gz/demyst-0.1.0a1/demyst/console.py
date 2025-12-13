"""
Rich Console Output for Demyst

Provides beautiful, readable CLI output with syntax highlighting,
progress bars, and formatted tables using the Rich library.

Falls back gracefully to plain text when Rich is not available.
"""

from __future__ import annotations

import sys
from contextlib import contextmanager
from typing import Any, Dict, Generator, Iterable, List, Optional, Union

# Try to import Rich components
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
        TimeElapsedColumn,
    )
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text
    from rich.theme import Theme
    from rich.tree import Tree

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# =============================================================================
# Custom Theme
# =============================================================================

DEMYST_THEME = {
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "critical": "bold white on red",
    "mirage": "magenta",
    "leakage": "red",
    "hypothesis": "yellow",
    "unit": "blue",
    "tensor": "cyan",
    "file": "bold blue",
    "line": "dim",
    "code": "green",
}


# =============================================================================
# Console Singleton
# =============================================================================


class DemystConsole:
    """
    Rich console wrapper for Demyst CLI output.

    Provides formatted output with fallback to plain text.
    """

    def __init__(self, force_terminal: bool = False, no_color: bool = False) -> None:
        """
        Initialize the console.

        Args:
            force_terminal: Force terminal mode
            no_color: Disable colors
        """
        self._use_rich = RICH_AVAILABLE and not no_color
        self._console: Optional["Console"] = None

        if self._use_rich:
            theme = Theme(DEMYST_THEME)
            self._console = Console(
                theme=theme,
                force_terminal=force_terminal,
                highlight=True,
            )

    @property
    def console(self) -> Optional["Console"]:
        """Get the underlying Rich console."""
        return self._console

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console."""
        if self._console:
            self._console.print(*args, **kwargs)
        else:
            print(*args, **kwargs)

    def print_error(self, message: str, **kwargs: Any) -> None:
        """Print an error message."""
        if self._console:
            self._console.print(f"[error]Error:[/error] {message}", **kwargs)
        else:
            print(f"Error: {message}", file=sys.stderr)

    def print_warning(self, message: str, **kwargs: Any) -> None:
        """Print a warning message."""
        if self._console:
            self._console.print(f"[warning]Warning:[/warning] {message}", **kwargs)
        else:
            print(f"Warning: {message}")

    def print_success(self, message: str, **kwargs: Any) -> None:
        """Print a success message."""
        if self._console:
            self._console.print(f"[success]{message}[/success]", **kwargs)
        else:
            print(message)

    def print_info(self, message: str, **kwargs: Any) -> None:
        """Print an info message."""
        if self._console:
            self._console.print(f"[info]{message}[/info]", **kwargs)
        else:
            print(message)

    def print_rule(self, title: str = "", **kwargs: Any) -> None:
        """Print a horizontal rule."""
        if self._console:
            self._console.rule(title, **kwargs)
        else:
            if title:
                print(f"\n{'=' * 20} {title} {'=' * 20}")
            else:
                print("=" * 60)

    def print_panel(
        self, content: str, title: Optional[str] = None, style: str = "default", **kwargs: Any
    ) -> None:
        """Print content in a panel."""
        if self._console:
            panel = Panel(content, title=title, style=style, **kwargs)
            self._console.print(panel)
        else:
            if title:
                print(f"\n[{title}]")
            print(content)
            if title:
                print()

    def print_code(
        self,
        code: str,
        language: str = "python",
        line_numbers: bool = True,
        highlight_lines: Optional[set[int]] = None,
        start_line: int = 1,
        **kwargs: Any,
    ) -> None:
        """Print syntax-highlighted code."""
        if self._console:
            syntax = Syntax(
                code,
                language,
                line_numbers=line_numbers,
                highlight_lines=highlight_lines,
                start_line=start_line,
                theme="monokai",
                **kwargs,
            )
            self._console.print(syntax)
        else:
            lines = code.splitlines()
            for i, line in enumerate(lines, start=start_line):
                marker = ">>>" if highlight_lines and i in highlight_lines else "   "
                print(f"{marker} {i:4d} | {line}")

    def print_table(
        self, columns: List[str], rows: List[List[str]], title: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Print a formatted table."""
        if self._console:
            table = Table(title=title, **kwargs)
            for col in columns:
                table.add_column(col)
            for row in rows:
                table.add_row(*row)
            self._console.print(table)
        else:
            # Simple plain text table
            if title:
                print(f"\n{title}")
            # Calculate column widths
            widths = [len(c) for c in columns]
            for row in rows:
                for i, cell in enumerate(row):
                    widths[i] = max(widths[i], len(str(cell)))

            # Header
            header = " | ".join(c.ljust(widths[i]) for i, c in enumerate(columns))
            print(header)
            print("-" * len(header))

            # Rows
            for row in rows:
                print(" | ".join(str(c).ljust(widths[i]) for i, c in enumerate(row)))

    def print_violations(
        self,
        violations: List[Dict[str, Any]],
        file_path: Optional[str] = None,
        source: Optional[str] = None,
        context_lines: int = 2,
    ) -> None:
        """Print a list of violations with context."""
        if not violations:
            self.print_success("No violations detected.")
            return

        # Read source if not provided
        if not source and file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    source = f.read()
            except Exception:
                pass

        source_lines = source.splitlines() if source else []

        for v in violations:
            violation_type = v.get("type", "unknown")
            line = v.get("line", 0)
            description = v.get("description", "")
            recommendation = v.get("recommendation", "")

            # Header
            type_style = self._get_violation_style(violation_type)
            if self._console:
                self._console.print()
                self._console.print(
                    f"[{type_style}]{violation_type.upper()}[/{type_style}] "
                    f"[line]Line {line}[/line]"
                    + (f" in [file]{file_path}[/file]" if file_path else "")
                )
            else:
                print(
                    f"\n{violation_type.upper()} Line {line}"
                    + (f" in {file_path}" if file_path else "")
                )

            # Description
            if description:
                if self._console:
                    self._console.print(f"  {description}")
                else:
                    print(f"  {description}")

            # Code context
            if source_lines and 0 < line <= len(source_lines):
                start = max(0, line - context_lines - 1)
                end = min(len(source_lines), line + context_lines)
                context = "\n".join(source_lines[start:end])

                if self._console:
                    syntax = Syntax(
                        context,
                        "python",
                        line_numbers=True,
                        start_line=start + 1,
                        highlight_lines={line},
                        theme="monokai",
                    )
                    self._console.print(syntax)
                else:
                    for i in range(start, end):
                        marker = ">>>" if i == line - 1 else "   "
                        print(f"{marker} {i + 1:4d} | {source_lines[i]}")

            # Recommendation
            if recommendation:
                if self._console:
                    self._console.print(f"  [info]Fix:[/info] {recommendation}")
                else:
                    print(f"  Fix: {recommendation}")

    def _get_violation_style(self, violation_type: str) -> str:
        """Get the style for a violation type."""
        type_styles = {
            "mean": "mirage",
            "sum": "mirage",
            "argmax": "mirage",
            "argmin": "mirage",
            "leakage": "leakage",
            "hypothesis": "hypothesis",
            "unit": "unit",
            "tensor": "tensor",
            "gradient": "tensor",
        }
        return type_styles.get(violation_type, "error")

    def print_summary(
        self,
        title: str,
        counts: Dict[str, int],
        status: str = "info",
    ) -> None:
        """Print a summary with counts."""
        if self._console:
            table = Table(title=title, show_header=False)
            table.add_column("Category")
            table.add_column("Count", justify="right")

            for category, count in counts.items():
                style = "success" if count == 0 else "warning"
                table.add_row(category, f"[{style}]{count}[/{style}]")

            self._console.print(table)
        else:
            print(f"\n{title}")
            print("-" * 40)
            for category, count in counts.items():
                print(f"  {category}: {count}")

    def print_diff(self, diff: str, title: str = "Changes") -> None:
        """Print a unified diff with colors."""
        if not diff:
            return

        if self._console:
            lines = diff.splitlines()
            self._console.print()
            self._console.print(f"[bold]{title}[/bold]")

            for line in lines:
                if line.startswith("+") and not line.startswith("+++"):
                    self._console.print(f"[green]{line}[/green]")
                elif line.startswith("-") and not line.startswith("---"):
                    self._console.print(f"[red]{line}[/red]")
                elif line.startswith("@@"):
                    self._console.print(f"[cyan]{line}[/cyan]")
                else:
                    self._console.print(line)
        else:
            print(f"\n{title}")
            print(diff)

    @contextmanager
    def progress(
        self,
        description: str = "Processing",
        total: Optional[int] = None,
    ) -> Generator[Any, None, None]:
        """Context manager for progress tracking."""
        if self._console:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=self._console,
            )
            with progress:
                task = progress.add_task(description, total=total)
                yield lambda n=1: progress.update(task, advance=n)
        else:
            # Fallback: simple counter
            current = [0]

            def update(n: int = 1) -> None:
                current[0] += n
                if total:
                    pct = current[0] / total * 100
                    print(f"\r{description}: {current[0]}/{total} ({pct:.1f}%)", end="")

            yield update
            print()  # Newline after progress

    def status(self, message: str) -> Any:
        """Show a status spinner."""
        if self._console:
            return self._console.status(message)
        else:
            print(message)
            return _NullContext()


class _NullContext:
    """Null context manager for fallback."""

    def __enter__(self) -> "_NullContext":
        return self

    def __exit__(self, *args: Any) -> None:
        pass


# =============================================================================
# Global Console Instance
# =============================================================================

_console: Optional["DemystConsole"] = None


def get_console(force_terminal: bool = False, no_color: bool = False) -> DemystConsole:
    """Get the global console instance."""

    global _console

    if _console is None:

        _console = DemystConsole(force_terminal=force_terminal, no_color=no_color)

    return _console


def configure_console(force_terminal: bool = False, no_color: bool = False) -> DemystConsole:
    """Configure and return a new console instance."""

    global _console

    _console = DemystConsole(force_terminal=force_terminal, no_color=no_color)

    return _console


# =============================================================================
# Report Formatting
# =============================================================================


def format_analysis_report(
    results: Dict[str, Any],
    file_path: Optional[str] = None,
) -> None:
    """Format and print a complete analysis report."""
    console = get_console()

    # Title
    if file_path:
        console.print_rule(f"Demyst Check: {file_path}")
    else:
        console.print_rule("Demyst Check")

    # Collect counts
    counts = {
        "Mirages": 0,
        "Data Leakage": 0,
        "Statistical Issues": 0,
        "Unit Issues": 0,
        "Tensor Issues": 0,
    }

    # Process each guard result
    if "mirage" in results and not results["mirage"].get("error"):
        issues = results["mirage"].get("issues", [])
        counts["Mirages"] = len(issues)
        if issues:
            console.print_violations(issues, file_path)

    if "leakage" in results and not results["leakage"].get("error"):
        violations = results["leakage"].get("violations", [])
        counts["Data Leakage"] = len(violations)
        if violations:
            console.print_violations(violations, file_path)

    if "hypothesis" in results and not results["hypothesis"].get("error"):
        violations = results["hypothesis"].get("violations", [])
        counts["Statistical Issues"] = len(violations)
        if violations:
            console.print_violations(violations, file_path)

    if "unit" in results and not results["unit"].get("error"):
        violations = results["unit"].get("violations", [])
        counts["Unit Issues"] = len(violations)
        if violations:
            console.print_violations(violations, file_path)

    if "tensor" in results and not results["tensor"].get("error"):
        gradient = results["tensor"].get("gradient_issues", [])
        norm = results["tensor"].get("normalization_issues", [])
        reward = results["tensor"].get("reward_issues", [])
        counts["Tensor Issues"] = len(gradient) + len(norm) + len(reward)
        for issues in [gradient, norm, reward]:
            if issues:
                console.print_violations(issues, file_path)

    # Summary
    total = sum(counts.values())
    status = "success" if total == 0 else "warning"
    console.print_summary("Summary", counts, status)

    if total == 0:
        console.print_success("\nDemyst Check Passed!")
    else:
        console.print_warning(f"\nDemyst Check Failed: Found {total} issue(s)")

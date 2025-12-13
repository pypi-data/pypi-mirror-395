"""
Inline suppression utilities for demyst guards.

Supports comments like:
    # demyst: ignore           - Suppress all guards on this line
    # demyst: ignore-mirage    - Suppress only mirage guard
    # demyst: ignore-leakage   - Suppress only leakage guard
    # demyst: ignore-hypothesis - Suppress only hypothesis guard
    # demyst: ignore-tensor    - Suppress only tensor guard
    # demyst: ignore-unit      - Suppress only unit guard
"""

import re
from typing import Dict, Optional, Set

# Pattern matches: # demyst: ignore or # demyst: ignore-<guard>
DEMYST_IGNORE_PATTERN = re.compile(r"#\s*demyst:\s*ignore(?:-(\w+))?", re.IGNORECASE)


def collect_suppressions(source: str, guard_name: Optional[str] = None) -> Set[int]:
    """
    Scan source code for inline suppression comments.

    Args:
        source: Source code string
        guard_name: Optional guard name to filter (e.g., "mirage", "leakage").
                   If None, returns lines with any suppression.

    Returns:
        Set of 1-indexed line numbers that should be suppressed.
    """
    suppressed: Set[int] = set()
    for i, line in enumerate(source.splitlines(), start=1):
        match = DEMYST_IGNORE_PATTERN.search(line)
        if match:
            specific_guard = match.group(1)  # e.g., "mirage" from "ignore-mirage"
            # Suppress if:
            # 1. No specific guard mentioned (ignore all)
            # 2. Specific guard matches our guard_name
            # 3. "all" is specified
            if specific_guard is None:
                suppressed.add(i)
            elif guard_name and specific_guard.lower() in (guard_name.lower(), "all"):
                suppressed.add(i)
            elif specific_guard.lower() == "all":
                suppressed.add(i)
    return suppressed


def collect_all_suppressions(source: str) -> Dict[str, Set[int]]:
    """
    Collect suppressions for all guard types.

    Returns:
        Dict mapping guard name -> set of suppressed line numbers.
        Special key "all" contains lines that suppress everything.
    """
    result: Dict[str, Set[int]] = {"all": set()}
    guard_names = ["mirage", "leakage", "hypothesis", "tensor", "unit"]

    for i, line in enumerate(source.splitlines(), start=1):
        match = DEMYST_IGNORE_PATTERN.search(line)
        if match:
            specific_guard = match.group(1)
            if specific_guard is None or specific_guard.lower() == "all":
                result["all"].add(i)
            else:
                guard = specific_guard.lower()
                if guard not in result:
                    result[guard] = set()
                result[guard].add(i)

    return result


def is_suppressed(
    line: int, suppressions: Set[int], all_suppressions: Optional[Set[int]] = None
) -> bool:
    """
    Check if a line is suppressed.

    Args:
        line: 1-indexed line number
        suppressions: Set of suppressed lines for specific guard
        all_suppressions: Optional set of lines that suppress all guards

    Returns:
        True if the line should be suppressed.
    """
    if line in suppressions:
        return True
    if all_suppressions and line in all_suppressions:
        return True
    return False

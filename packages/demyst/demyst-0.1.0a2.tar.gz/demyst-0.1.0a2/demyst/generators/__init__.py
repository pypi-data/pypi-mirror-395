"""
Demyst Generators - Automated Scientific Documentation

This module provides tools for generating scientific documentation
that is guaranteed to match the executed code.

Generators:
    - PaperGenerator: LaTeX methodology section generator
    - ReportGenerator: Scientific integrity report generator
"""

from .paper_generator import MethodologyExtractor, PaperGenerator
from .report_generator import IntegrityReportGenerator

__all__ = [
    "PaperGenerator",
    "MethodologyExtractor",
    "IntegrityReportGenerator",
]

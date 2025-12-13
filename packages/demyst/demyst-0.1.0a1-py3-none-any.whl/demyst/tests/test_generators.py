import json

import pytest

from demyst.generators.paper_generator import PaperGenerator
from demyst.generators.report_generator import IntegrityReportGenerator


def test_integrity_report_generator_empty_report():
    generator = IntegrityReportGenerator("Empty Report")
    html_output = generator.to_html()
    markdown_output = generator.to_markdown()
    json_output = generator.to_json()

    assert "Empty Report" in html_output
    assert "Empty Report" in markdown_output
    assert "Empty Report" in json_output
    assert '<span class="status-badge">PASS</span>' in html_output
    assert "Empty Report" in markdown_output

    json_data = json.loads(json_output)
    assert json_data["title"] == "Empty Report"
    assert len(json_data["sections"]) == 0


def test_integrity_report_generator_with_issues():
    generator = IntegrityReportGenerator("Report with Issues")

    mock_issues = [
        {
            "type": "mirage",
            "line": 10,
            "description": "Mean operation",
            "recommendation": "Use VariationTensor",
        },
        {
            "type": "leakage",
            "line": 25,
            "description": "Train-test leakage",
            "recommendation": "Split data first",
        },
    ]
    generator.add_section(
        "Computational Mirages",
        "fail",
        "Found mirage issues",
        [mock_issues[0]],
        [mock_issues[0]["recommendation"]],
    )
    generator.add_section(
        "Data Leakage",
        "fail",
        "Found leakage issues",
        [mock_issues[1]],
        [mock_issues[1]["recommendation"]],
    )

    html_output = generator.to_html()
    markdown_output = generator.to_markdown()
    json_output = generator.to_json()

    assert "Report with Issues" in html_output
    assert "Computational Mirages" in html_output
    assert "Mean operation" in html_output
    assert "Use VariationTensor" in html_output
    assert "Data Leakage" in html_output
    assert "Train-test leakage" in html_output
    assert "Split data first" in html_output

    assert "Report with Issues" in markdown_output
    assert "## :x: Computational Mirages" in markdown_output
    assert "**Line 10**" in markdown_output and "Mean operation" in markdown_output
    assert "Use VariationTensor" in markdown_output
    assert "## :x: Data Leakage" in markdown_output
    assert "**Line 25**" in markdown_output and "Train-test leakage" in markdown_output
    assert "Split data first" in markdown_output

    json_data = json.loads(json_output)
    assert json_data["title"] == "Report with Issues"
    assert len(json_data["sections"]) == 2
    assert json_data["sections"][0]["title"] == "Computational Mirages"
    assert json_data["sections"][0]["status"] == "fail"
    assert len(json_data["sections"][0]["issues"]) == 1


def test_paper_generator_basic_generation():
    source_code = """
import numpy as np
def func(x):
    return np.mean(x)
    """
    generator = PaperGenerator()
    latex_output = generator.generate(source_code, title="Test Methodology")

    assert "\\section{Test Methodology}" in latex_output
    assert "\\subsection{Reproducibility}" in latex_output
    assert (
        "All experiments are tracked using the Demyst scientific integrity framework."
        in latex_output
    )
    assert "The code is available at [REPOSITORY URL] and includes:" in latex_output


def test_paper_generator_full_paper_template():
    source_code = """
import pandas as pd
def load_data(path):
    return pd.read_csv(path)
"""
    generator = PaperGenerator(style="neurips")
    latex_output = generator.generate_full_paper_template(source_code)

    assert "\\documentclass{article}" in latex_output
    assert "\\title{[Paper Title]}" in latex_output
    assert "\\section{Methodology}" in latex_output
    assert "\\subsection{Reproducibility}" in latex_output
    assert (
        "All experiments are tracked using the Demyst scientific integrity framework."
        in latex_output
    )

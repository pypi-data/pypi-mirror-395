import json
import os
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from demyst import cli


@pytest.fixture
def mock_file(tmp_path):
    # Create a dummy Python file for testing
    file_content = """
import numpy as np

def process_data(data):
    # This is a potential mirage
    processed = np.mean(data)
    return processed

def another_func(x, y):
    return x + y
"""
    file_path = tmp_path / "test_file.py"
    file_path.write_text(file_content)
    return file_path


@pytest.fixture
def mock_directory(tmp_path):
    # Create a dummy directory with a file for testing
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    file_content = """
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def process_data_with_leakage(data_path):
    df = pd.read_csv(data_path)
    
    # Simulate leakage: fit scaler on full dataset before splitting
    scaler = StandardScaler()
    X = df['feature_col'].values.reshape(-1, 1) # Assume X is now a numpy array
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, df['target'], test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test

# Example usage (not directly run, but for analysis)
if __name__ == '__main__':
    # Assume 'data.csv' exists with 'feature_col' and 'target'
    process_data_with_leakage("data.csv")
"""
    (dir_path / "leakage_example.py").write_text(file_content)
    return dir_path


def test_analyze_single_file_markdown_output(capsys, monkeypatch, mock_file, tmp_path):
    monkeypatch.setattr(sys, "exit", lambda x: x)  # Mock sys.exit

    # Create an empty .demystrc.yaml in the mock_directory for the global config to pick up
    config_path = tmp_path / ".demystrc.yaml"
    config_content = "ignore_patterns: []"
    config_path.write_text(config_content)

    sys.argv = [
        "demyst",
        "--config",
        str(config_path),
        "analyze",
        str(mock_file),
        "--format",
        "markdown",
    ]

    exit_code = cli.main()
    captured = capsys.readouterr()
    output = captured.out  # Remove strip_ansi_codes

    assert exit_code == 1  # Expecting issues due to np.mean mirage
    assert "Demyst Analysis Report" in output
    assert f"# Demyst Analysis Report: `{mock_file}`" in output
    assert "## Computational Mirages" in output
    assert "- **Type**: Mirage" in output
    assert "  - **Line**: 6" in output
    assert (
        "  - **Description**: Reduction on array-like data without accompanying dispersion check."
        in output
    )
    assert (
        "  - **Recommendation**: Use VariationTensor to preserve statistical metadata during aggregations"
        in output
    )
    assert "## Summary" in output
    assert "| Check | Issues Found |" in output
    assert "|---|---|" in output
    assert "| Mirage | 1 |" in output
    assert "| Leakage | 0 |" in output
    assert "| Hypothesis | 0 |" in output
    assert "| Unit | 0 |" in output
    assert "| Tensor | 0 |" in output
    assert "| **Total** | **1** |" in output
    assert "**Demyst Check Failed: Found 1 issue(s).**" in output


def test_analyze_single_file_json_output(capsys, monkeypatch, mock_file, tmp_path):
    monkeypatch.setattr(sys, "exit", lambda x: x)  # Mock sys.exit

    # Create an empty .demystrc.yaml in the mock_directory for the global config to pick up
    config_path = tmp_path / ".demystrc.yaml"
    config_content = "ignore_patterns: []"
    config_path.write_text(config_content)

    sys.argv = [
        "demyst",
        "--config",
        str(config_path),
        "analyze",
        str(mock_file),
        "--format",
        "json",
    ]

    exit_code = cli.main()
    captured = capsys.readouterr()
    output = captured.out  # Remove strip_ansi_codes

    assert exit_code == 1
    data = json.loads(output)
    assert "mirage" in data
    assert len(data["mirage"]["issues"]) == 1
    assert data["mirage"]["issues"][0]["line"] == 6
    assert "Reduction on array-like data" in data["mirage"]["issues"][0]["description"]


@pytest.mark.skip(
    reason="Failing due to persistent Rich output capture issues in pytest environment"
)
def test_report_directory_html_output(capsys, monkeypatch, mock_directory):
    monkeypatch.setattr(sys, "exit", lambda x: x)  # Mock sys.exit

    # Create an empty .demystrc.yaml in the mock_directory for the global config to pick up
    (mock_directory / ".demystrc.yaml").write_text("ignore_patterns: []")
    sys.argv = [
        "demyst",
        "--config",
        str(mock_directory / ".demystrc.yaml"),
        "report",
        str(mock_directory),
        "--format",
        "html",
    ]

    exit_code = cli.main()
    captured = capsys.readouterr()
    output = captured.out + captured.err  # Remove strip_ansi_codes

    assert exit_code == 1  # Expecting issues due to leakage
    assert "Integrity Report" in output
    assert "Data Leakage" in output
    assert "leakage_example.py" in output


def test_report_single_file_html_output(capsys, monkeypatch, mock_file):
    monkeypatch.setattr(sys, "exit", lambda x: x)  # Mock sys.exit

    sys.argv = ["demyst", "report", str(mock_file), "--format", "html"]

    exit_code = cli.main()
    captured = capsys.readouterr()
    output = captured.out + captured.err

    assert exit_code == 1
    assert "Integrity Report: " in output
    assert "Computational Mirages" in output
    assert "Line 6" in output


def test_leakage_detection_in_mock_directory(capsys, monkeypatch, mock_directory):
    monkeypatch.setattr(sys, "exit", lambda x: x)  # Mock sys.exit

    # Create an empty .demystrc.yaml in the mock_directory for the global config to pick up
    config_path = mock_directory / ".demystrc.yaml"
    config_content = "ignore_patterns: []"
    config_path.write_text(config_content)

    sys.argv = [
        "demyst",
        "leakage",
        str(mock_directory / "leakage_example.py"),
        "--config",
        str(config_path),
    ]

    exit_code = cli.main()
    captured = capsys.readouterr()
    output = captured.out + captured.err  # Capture both stdout and stderr

    assert exit_code == 1  # Expecting leakage to be detected
    assert "Warning: Verdict: FAIL: Critical data leakage detected. Results are invalid." in output

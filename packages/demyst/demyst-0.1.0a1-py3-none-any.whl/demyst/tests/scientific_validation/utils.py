"""
Utilities for Scientific Validation Tests.

Includes generators for synthetic large codebases and stress test patterns.
"""

import os
import random
import string
import tempfile
from pathlib import Path
from typing import List, Optional


class SyntheticCodeGenerator:
    """Generates massive synthetic python files for performance testing."""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def generate_ml_snippet(self) -> str:
        """Generates a mock ML training loop snippet."""
        template = """
def train_model_{id}(X, y):
    model = Model()
    # Standard loop
    for epoch in range(10):
        pred = model(X)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()
    return model
"""
        return template.replace("{id}", self._random_id())

    def generate_physics_snippet(self) -> str:
        """Generates a mock physics calculation snippet."""
        template = """
def calc_energy_{id}(mass, velocity):
    # E = mc^2 approximation
    c = 3e8
    energy = mass * (c ** 2) + 0.5 * mass * (velocity ** 2)
    return energy
"""
        return template.replace("{id}", self._random_id())

    def generate_data_processing_snippet(self) -> str:
        """Generates pandas-style data processing."""
        template = """
def process_data_{id}(df):
    # Cleaning
    df = df.dropna()
    # Mirage potential?
    avg = df.mean()
    return avg
"""
        return template.replace("{id}", self._random_id())

    def generate_large_file(self, num_lines: int) -> str:
        """Generates a valid Python file with approximately num_lines."""
        lines = ["import numpy as np", "import pandas as pd", "import torch"]

        # Average snippet is ~8 lines.
        num_snippets = num_lines // 8

        generators = [
            self.generate_ml_snippet,
            self.generate_physics_snippet,
            self.generate_data_processing_snippet,
        ]

        for _ in range(num_snippets):
            gen = self.rng.choice(generators)
            lines.append(gen())

        return "\n".join(lines)

    def _random_id(self) -> str:
        return "".join(self.rng.choices(string.ascii_lowercase, k=8))

    def create_temp_file(self, num_lines: int) -> Path:
        """Creates a temporary file with generated code."""
        content = self.generate_large_file(num_lines)
        fd, path = tempfile.mkstemp(suffix=".py", text=True)
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return Path(path)

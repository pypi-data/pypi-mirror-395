"""
Demyst Test Configuration and Fixtures

Provides shared fixtures for all test modules:
- Path fixtures for project root and examples directory
- Source code fixtures for each example file
- Guard instance fixtures (mirage_detector, hypothesis_guard, unit_guard)
"""

from pathlib import Path

import pytest


# Project root detection
@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def examples_dir(project_root: Path) -> Path:
    """Return the examples directory."""
    return project_root / "examples"


@pytest.fixture(scope="session")
def swarm_collapse_path(examples_dir: Path) -> Path:
    """Return the path to swarm_collapse.py."""
    return examples_dir / "swarm_collapse.py"


@pytest.fixture(scope="session")
def random_walk_path(examples_dir: Path) -> Path:
    """Return the path to random_walk.py."""
    return examples_dir / "random_walk.py"


@pytest.fixture(scope="session")
def random_walk_source(random_walk_path: Path) -> str:
    """Return the source code of random_walk.py."""
    return random_walk_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def deep_learning_gradient_death_path(examples_dir: Path) -> Path:
    """Return the path to deep_learning_gradient_death.py."""
    return examples_dir / "deep_learning_gradient_death.py"


@pytest.fixture(scope="session")
def deep_learning_gradient_death_source(deep_learning_gradient_death_path: Path) -> str:
    """Return the source code of deep_learning_gradient_death.py."""
    return deep_learning_gradient_death_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def ml_data_leakage_path(examples_dir: Path) -> Path:
    """Return the path to ml_data_leakage.py."""
    return examples_dir / "ml_data_leakage.py"


@pytest.fixture(scope="session")
def ml_data_leakage_source(ml_data_leakage_path: Path) -> str:
    """Return the source code of ml_data_leakage.py."""
    return ml_data_leakage_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def biology_gene_expression_path(examples_dir: Path) -> Path:
    """Return the path to biology_gene_expression.py."""
    return examples_dir / "biology_gene_expression.py"


@pytest.fixture(scope="session")
def biology_gene_expression_source(biology_gene_expression_path: Path) -> str:
    """Return the source code of biology_gene_expression.py."""
    return biology_gene_expression_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def swarm_collapse_source(swarm_collapse_path: Path) -> str:
    """Return the source code of swarm_collapse.py."""
    return swarm_collapse_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def physics_kinematics_path(examples_dir: Path) -> Path:
    """Return the path to physics_kinematics.py."""
    return examples_dir / "physics_kinematics.py"


@pytest.fixture(scope="session")
def physics_kinematics_source(physics_kinematics_path: Path) -> str:
    """Return the source code of physics_kinematics.py."""
    return physics_kinematics_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def chemistry_stoichiometry_path(examples_dir: Path) -> Path:
    """Return the path to chemistry_stoichiometry.py."""
    return examples_dir / "chemistry_stoichiometry.py"


@pytest.fixture(scope="session")
def chemistry_stoichiometry_source(chemistry_stoichiometry_path: Path) -> str:
    """Return the source code of chemistry_stoichiometry.py."""
    return chemistry_stoichiometry_path.read_text(encoding="utf-8")


@pytest.fixture
def mirage_detector():
    """Return a MirageDetector instance."""
    from demyst.engine.mirage_detector import MirageDetector

    return MirageDetector()


@pytest.fixture
def unit_guard():
    """Return a UnitGuard instance."""
    from demyst.guards.unit_guard import UnitGuard

    return UnitGuard()


@pytest.fixture
def hypothesis_guard():
    """Return a HypothesisGuard instance."""
    from demyst.guards.hypothesis_guard import HypothesisGuard

    return HypothesisGuard()


@pytest.fixture
def tensor_guard():
    """Return a TensorGuard instance."""
    from demyst.guards.tensor_guard import TensorGuard

    return TensorGuard()


@pytest.fixture
def leakage_hunter():
    """Return a LeakageHunter instance."""
    from demyst.guards.leakage_hunter import LeakageHunter

    return LeakageHunter()

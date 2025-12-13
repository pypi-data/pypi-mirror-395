# Demyst

> **de·mys·ti·fy** /dēˈmistəˌfī/ — to make less obscure or confusing

[![PyPI version](https://badge.fury.io/py/demyst.svg)](https://badge.fury.io/py/demyst)
[![Tests](https://github.com/Hmbown/demyst/actions/workflows/ci.yml/badge.svg)](https://github.com/Hmbown/demyst/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/Hmbown/demyst)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A scientific linter for research code. Like `black` for formatting and `mypy` for types, `demyst` checks **scientific logic**.

```bash
pip install demyst
demyst analyze ./src
```

## Status

| | |
|---|---|
| **Stability** | Alpha — actively developed, API may change |
| **Python** | 3.8, 3.9, 3.10, 3.11, 3.12 |
| **Ecosystems** | NumPy, pandas, scikit-learn, PyTorch, JAX, SciPy |
| **Philosophy** | Prefer false positives over silent failures — use `# demyst: ignore` to suppress |

## What It Catches

| Check | What It Detects | Example |
|-------|-----------------|---------|
| `mirage` | Variance-destroying reductions | `np.mean()` hiding a rogue agent in a swarm |
| `leakage` | Train/test contamination | `fit_transform()` before `train_test_split()` |
| `hypothesis` | P-hacking, multiple comparisons | 20 t-tests without Bonferroni correction |
| `tensor` | Gradient death, normalization issues | Deep sigmoid chains, disabled BatchNorm stats |
| `units` | Dimensional mismatches | Adding meters to seconds |

## Try It in 30 Seconds

```bash
git clone https://github.com/Hmbown/demyst.git
cd demyst
pip install -e .
demyst mirage examples/swarm_collapse.py
```

You'll see demyst catch the "rogue agent" problem — where `np.mean()` returns 0.999 but one agent scores 0.0.

## Sample Output

```text
$ demyst analyze examples/leakage_example.py

─ Data Leakage Detected ─

CRITICAL Line 12 in examples/leakage_example.py
  fit_transform() called BEFORE train_test_split on line 15.
  Preprocessing statistics are computed using test data.
  
  10   X = load_data()
  11   scaler = StandardScaler()
❱ 12   X_scaled = scaler.fit_transform(X)  # LEAKS TEST INFO
  13   
  14   # Split happens AFTER fitting — too late!
  15   X_train, X_test = train_test_split(X_scaled)

  Fix: Split first, then fit on train only:
       X_train, X_test = train_test_split(X)
       X_train = scaler.fit_transform(X_train)
       X_test = scaler.transform(X_test)

Summary: 1 critical, 0 warnings
```

## Quick Examples

**Mirage** — aggregations that hide critical variance:

```python
# DANGEROUS: 999 agents score 1.0, one scores 0.0
np.mean(agent_scores)  # Returns 0.999 — you deploy, rogue agent destroys system
```

**Leakage** — the #1 ML benchmarking error:

```python
# WRONG: Leaks test statistics into training
scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled)

# CORRECT
X_train, X_test = train_test_split(X)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

**P-Hacking** — uncorrected multiple comparisons:

```python
# 20 tests at α=0.05 expects 1 false positive
for condition in conditions:
    if ttest(a[condition], b[condition]).pvalue < 0.05:
        print(f"{condition} significant!")  # No correction applied
```

## Usage

```bash
# Full analysis
demyst analyze your_code.py

# Individual guards
demyst mirage model.py
demyst leakage train.py
demyst hypothesis stats.py
demyst units physics.py
demyst tensor network.py

# Auto-fix mirages
demyst mirage model.py --fix

# CI mode
demyst ci . --strict
```

## Why Mirages Matter

These documented cases show how `np.mean()` hides critical information:

| Phenomenon | What Happened |
|------------|---------------|
| **Anscombe's Quartet** (1973) | Four datasets with identical mean (7.5) but completely different distributions |
| **Simpson's Paradox** (Berkeley 1973) | 44% male vs 35% female admission overall, but women admitted more in 4/6 departments |
| **Fat Tails in Finance** | Average daily return ~0.04% hides Black Monday's -22.6% single-day crash |
| **Outlier Masking** | Multiple outliers pull mean toward them, causing detection tests to fail |

Run `demyst mirage examples/real_world_mirages.py` to see detection in action.

## CI/CD

**GitHub Actions:**

```yaml
name: Demyst
on: [push, pull_request]
jobs:
  demyst:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install demyst
      - run: demyst ci . --strict
```

**Pre-commit:**

If you're already using `black` + `mypy` + `ruff`, drop this in next to them:

```yaml
repos:
  - repo: https://github.com/Hmbown/demyst
    rev: v1.2.0
    hooks:
      - id: demyst
```

See [`examples/configs/`](examples/configs/) for more templates.

## Suppressing False Positives

Use inline comments to suppress specific warnings:

```python
# Suppress all demyst warnings on this line
mean_value = np.mean(data)  # demyst: ignore

# Suppress only mirage warnings
dashboard_avg = np.mean(daily_views)  # demyst: ignore-mirage

# Suppress only leakage warnings  
scaler.fit_transform(X)  # demyst: ignore-leakage
```

Available suppressions: `ignore`, `ignore-mirage`, `ignore-leakage`, `ignore-hypothesis`, `ignore-tensor`, `ignore-unit`, `ignore-all`

## Configuration

Create `.demystrc.yaml`:

```yaml
profile: default  # Or: biology, physics, chemistry, economics

rules:
  mirage:
    enabled: true
    severity: critical
  leakage:
    enabled: true
    severity: critical

ignore_patterns:
  - "**/tests/**"
```

## Programmatic API

```python
from demyst import TensorGuard, LeakageHunter, HypothesisGuard, UnitGuard

source = open('model.py').read()
result = LeakageHunter().analyze(source)

if result['summary']['critical_count'] > 0:
    print("DATA LEAKAGE DETECTED")
```

## Design Principles

**Why your advisor / manager wants this:**

Silent failures in research code don't crash — they produce *wrong numbers that look right*. A model trains, metrics look good, paper gets submitted... then someone discovers the test set leaked into training. Demyst catches these before they become retractions.

**Our approach:**

| Principle | What It Means |
|-----------|---------------|
| **Yell early** | We prefer false positives over silent failures. Use `# demyst: ignore` to suppress. |
| **Static analysis** | AST-based heuristics + light dataflow. No runtime overhead, works on any Python. |
| **Actionable output** | Every warning includes the *why* and a concrete fix suggestion. |
| **Escape hatches** | Inline suppression (`# demyst: ignore-mirage`), config files, CI thresholds. |

**What we check:**

- **Mirage**: Detects 80+ NumPy array creators, tracks variable flow, checks for nearby variance operations
- **Leakage**: Tracks `fit`/`fit_transform` calls relative to `train_test_split`/`cross_val_score`
- **Hypothesis**: Counts statistical tests, checks for correction methods, detects p-value conditionals
- **Tensor**: Analyzes layer sequences for gradient death patterns, normalization misuse
- **Units**: Dimensional analysis via variable naming conventions and explicit annotations

## References

| Phenomenon | Finding | Source |
|------------|---------|--------|
| Anscombe's Quartet | Identical means hide different distributions | [Anscombe (1973)](https://en.wikipedia.org/wiki/Anscombe%27s_quartet) |
| Simpson's Paradox | Trends reverse when aggregated | [UC Berkeley (1975)](https://discovery.cs.illinois.edu/dataset/berkeley/) |
| Fat Tails | Normal assumptions hide crashes | [Mandelbrot (1963)](https://en.wikipedia.org/wiki/Fat-tailed_distribution) |
| Retraction Stats | 18.9% from computational errors | [PMC5395722](https://pmc.ncbi.nlm.nih.gov/articles/PMC5395722/) |

## Resources

- [Quick Start Guide](docs/quickstart.md)
- [Interactive Notebook](notebooks/quickstart.ipynb)
- [Configuration Templates](examples/configs/)
- [Full Documentation](docs/usage.md)

## License

MIT — See [LICENSE](LICENSE)

---

*"The first principle is that you must not fool yourself—and you are the easiest person to fool."* — Richard Feynman

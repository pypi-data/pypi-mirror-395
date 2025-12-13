"""
Neuroscience Domain Profile

Focus: Circular analysis, double-dipping.
"""

PROFILE = {
    "rules": {
        "leakage": {"enabled": True, "severity": "critical"},  # Double dipping (circular analysis)
        "hypothesis": {"enabled": True, "severity": "critical"},  # Multiple comparisons in fMRI
        "tensor": {"enabled": True, "severity": "warning"},  # Neural data often uses DL
    }
}

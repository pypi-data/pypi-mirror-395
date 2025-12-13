"""
Climate Science Domain Profile

Focus: Temporal leakage, ensemble handling.
"""

PROFILE = {
    "rules": {
        "leakage": {"enabled": True, "severity": "critical"},  # Temporal correlation is key
        "unit": {"enabled": True, "severity": "critical"},  # Physical consistency
        "mirage": {"enabled": True, "severity": "warning"},
    }
}

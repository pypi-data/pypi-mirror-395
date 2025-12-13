"""
Economics Domain Profile

Focus: Lookahead bias, autocorrelation.
"""

PROFILE = {
    "rules": {
        "leakage": {
            "enabled": True,
            "severity": "critical",  # Lookahead bias renders models useless
        },
        "hypothesis": {"enabled": True, "severity": "critical"},  # Spurious correlations
        "mirage": {"enabled": True, "severity": "warning"},
    }
}

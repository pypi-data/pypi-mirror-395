"""
Biology Domain Profile

Focus: Effect sizes, survival analysis checks, hypothesis testing.
"""

PROFILE = {
    "rules": {
        "hypothesis": {
            "enabled": True,
            "severity": "critical",  # p-hacking is a major issue in bio
        },
        "leakage": {
            "enabled": True,
            "severity": "critical",  # Train/test contamination in biomarkers
        },
        "unit": {"enabled": True, "severity": "warning"},
    }
}

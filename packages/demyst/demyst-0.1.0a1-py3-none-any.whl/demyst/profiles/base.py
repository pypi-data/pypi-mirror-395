"""
Default Demyst Profile
"""

PROFILE = {
    "rules": {
        "mirage": {"enabled": True, "severity": "critical"},
        "tensor": {"enabled": True, "severity": "critical"},
        "leakage": {"enabled": True, "severity": "critical"},
        "hypothesis": {"enabled": True, "severity": "warning"},
        "unit": {"enabled": True, "severity": "warning"},
    }
}

"""
Physics Domain Profile

Focus: Conservation laws, uncertainty propagation, dimensional consistency.

Key features:
    - Natural units support (c=hbar=G=kB=1)
    - General Relativity tensor naming conventions (g_tt, R_abcd, Gamma_abc)
    - Physics sigma thresholds (5-sigma discovery, 3-sigma evidence)
    - Variance context awareness (mean+std pairs not flagged)

Usage: demyst analyze --profile physics src/
"""

PROFILE = {
    "rules": {
        "unit": {
            "enabled": True,
            "severity": "critical",  # Dimensional errors are critical in physics
            # Natural units: c, hbar, G, kB treated as dimensionless
            "natural_units": True,
            # Recognize GR tensor index notation (g_tt, R_abcd, Gamma_abc)
            "tensor_conventions": True,
        },
        "mirage": {
            "enabled": True,
            "severity": "critical",  # Variance destruction is bad for error propagation
            # Don't flag mean() if std()/var() is computed on same data nearby
            "check_variance_context": True,
        },
        "hypothesis": {
            "enabled": True,
            "severity": "warning",
            # Use physics sigma thresholds instead of p<0.05
            "physics_mode": True,
            # 5-sigma for discovery (p ~ 2.87e-7)
            "discovery_sigma": 5.0,
            # 3-sigma for evidence (p ~ 0.00135)
            "evidence_sigma": 3.0,
        },
        "leakage": {"enabled": True, "severity": "warning"},
    }
}

"""
Demyst Jupyter Magic Extension.

Enables automatic scientific integrity checks in Jupyter notebooks.
Usage:
    %load_ext demyst
"""

import logging
from typing import Any, Dict, List, Optional

from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import Magics, line_magic, magics_class
from IPython.display import HTML, Markdown, display

from demyst.integrations.ci_enforcer import CIEnforcer

logger = logging.getLogger("demyst.magic")


@magics_class
class DemystMagics(Magics):
    """
    Jupyter Magic for Demyst.

    Intercepts cell execution and runs scientific integrity checks.
    """

    def __init__(self, shell: InteractiveShell):
        super().__init__(shell)
        self.shell = shell
        self.enforcer = CIEnforcer()
        # Ensure guards are imported
        if not self.enforcer._guards_available:
            logger.warning("Demyst guards not available. Magic will be disabled.")
            return

        self.shell.events.register("post_run_cell", self.post_run_cell)
        logger.info("Demyst magic loaded.")

    def post_run_cell(self, result: Any) -> None:
        """
        Callback executed after a cell is run.
        """
        if result.error_in_exec:
            return

        # Get the code from the cell
        # result.info.raw_cell contains the raw code
        code = result.info.raw_cell

        if not code or not code.strip():
            return

        # Run analysis
        try:
            issues = self._analyze_code(code)
            if issues:
                self._display_issues(issues)
        except Exception as e:
            logger.debug(f"Demyst analysis failed: {e}")

    def _analyze_code(self, source: str) -> List[Dict[str, Any]]:
        """
        Run integrity checks on the source code.
        Replicates logic from CIEnforcer.analyze_file but for string input.
        """
        all_issues = []

        # 1. Mirage Detection
        if self.enforcer.config_manager.is_rule_enabled("mirage"):
            try:
                import ast

                tree = ast.parse(source)
                detector = self.enforcer.MirageDetector(
                    config=self.enforcer.config_manager.get_rule_config("mirage")
                )
                detector.visit(tree)
                for m in detector.mirages:
                    all_issues.append(
                        {
                            "type": "Mirage",
                            "severity": "warning",
                            "title": "Computational Mirage Detected",
                            "description": f"{m['type']} operation destroys variance information.",
                            "details": f"Function: {m.get('function', 'module level')}",
                            "recommendation": f"Use VariationTensor({m['type']}).collapse('{m['type']}')",
                        }
                    )
            except Exception:
                pass

        # 2. Leakage Detection
        if self.enforcer.config_manager.is_rule_enabled("leakage"):
            try:
                hunter = self.enforcer.LeakageHunter(
                    config=self.enforcer.config_manager.get_rule_config("leakage")
                )
                res = hunter.analyze(source)
                for v in res.get("violations", []):
                    all_issues.append(
                        {
                            "type": "Leakage",
                            "severity": "critical" if v["severity"] == "critical" else "warning",
                            "title": "Data Leakage Detected",
                            "description": v["description"],
                            "details": f"Line {v.get('line', '?')}",
                            "recommendation": "Ensure strict separation of training and test data.",
                        }
                    )
            except Exception:
                pass

        # 3. Hypothesis Guard
        if self.enforcer.config_manager.is_rule_enabled("hypothesis"):
            try:
                h_guard = self.enforcer.HypothesisGuard(
                    config=self.enforcer.config_manager.get_rule_config("hypothesis")
                )
                res = h_guard.analyze_code(source)
                for v in res.get("violations", []):
                    all_issues.append(
                        {
                            "type": "Hypothesis",
                            "severity": "warning",
                            "title": "Statistical Validity Issue",
                            "description": v["description"],
                            "details": f"Line {v.get('line', '?')}",
                            "recommendation": v.get(
                                "recommendation", "Check statistical assumptions."
                            ),
                        }
                    )
            except Exception:
                pass

        # 4. Unit Guard
        if self.enforcer.config_manager.is_rule_enabled("unit"):
            try:
                u_guard = self.enforcer.UnitGuard(
                    config=self.enforcer.config_manager.get_rule_config("unit")
                )
                res = u_guard.analyze(source)
                for v in res.get("violations", []):
                    all_issues.append(
                        {
                            "type": "Units",
                            "severity": "warning",
                            "title": "Dimensional Consistency Issue",
                            "description": v["description"],
                            "details": f"Line {v.get('line', '?')}",
                            "recommendation": "Verify unit compatibility.",
                        }
                    )
            except Exception:
                pass

        # 5. Tensor Guard
        if self.enforcer.config_manager.is_rule_enabled("tensor"):
            try:
                t_guard = self.enforcer.TensorGuard(
                    config=self.enforcer.config_manager.get_rule_config("tensor")
                )
                res = t_guard.analyze(source)

                for issue in res.get("gradient_issues", []):
                    all_issues.append(
                        {
                            "type": "Tensor",
                            "severity": "warning",
                            "title": "Gradient Flow Issue",
                            "description": issue["description"],
                            "details": f"Line {issue.get('line', '?')}",
                            "recommendation": "Check gradient flow.",
                        }
                    )
                for issue in res.get("normalization_issues", []):
                    all_issues.append(
                        {
                            "type": "Tensor",
                            "severity": "warning",
                            "title": "Normalization Issue",
                            "description": issue["description"],
                            "details": f"Line {issue.get('line', '?')}",
                            "recommendation": "Verify normalization layers.",
                        }
                    )
                for issue in res.get("reward_issues", []):
                    all_issues.append(
                        {
                            "type": "Tensor",
                            "severity": "warning",
                            "title": "Reward Hacking Risk",
                            "description": issue["description"],
                            "details": f"Line {issue.get('line', '?')}",
                            "recommendation": "Review reward function design.",
                        }
                    )
            except Exception:
                pass

        return all_issues

    def _display_issues(self, issues: List[Dict[str, Any]]) -> None:
        """
        Display issues in the notebook using HTML.
        """
        if not issues:
            return

        html_content = """
        <div style="border: 1px solid #e0e0e0; border-left: 5px solid #ff9800; background-color: #fff3e0; padding: 10px; margin-top: 10px; font-family: sans-serif;">
            <h4 style="margin-top: 0; color: #e65100;">Demyst: Scientific Integrity Check</h4>
            <ul style="padding-left: 20px; margin-bottom: 0;">
        """

        for issue in issues:
            color = "#d32f2f" if issue["severity"] == "critical" else "#f57c00"
            html_content += f"""
                <li style="margin-bottom: 8px;">
                    <strong style="color: {color};">[{issue['type']}] {issue['title']}</strong><br>
                    {issue['description']}<br>
                    <span style="font-size: 0.9em; color: #555;">{issue['details']}</span><br>
                    <em style="font-size: 0.9em; color: #333;">Tip: {issue['recommendation']}</em>
                </li>
            """

        html_content += """
            </ul>
        </div>
        """

        display(HTML(html_content))


def load_ipython_extension(ipython: Any) -> None:
    """
    Entry point for %load_ext demyst
    """
    ipython.register_magics(DemystMagics)

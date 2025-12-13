"""
Demyst Silent Observer (Watchdog).

Monitors a directory for changes and runs scientific integrity checks in the background.
Logs critical alerts when "Catastrophic Mirages" are detected.
"""

import logging
import sys
import time
from pathlib import Path
from typing import Optional

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from demyst.integrations.ci_enforcer import CIEnforcer

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [WATCHDOG] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("demyst.watchdog")


class DemystEventHandler(FileSystemEventHandler):
    """Handles file system events."""

    def __init__(self) -> None:
        self.enforcer = CIEnforcer()

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        filename = str(event.src_path)
        if not filename.endswith(".py"):
            return

        self._analyze_file(str(filename))

    def _analyze_file(self, filepath: str) -> None:
        """Run Demyst analysis on the modified file."""
        try:
            logger.info(f"Analyzing {filepath}...")
            result = self.enforcer.analyze_file(filepath)

            # Check for critical issues
            critical_issues = []

            # Check Mirages
            if result.get("mirage") and not result["mirage"].get("error"):
                for m in result["mirage"].get("issues", []):
                    critical_issues.append(f"[MIRAGE] {m['description']}")

            # Check Leakage (Always Critical)
            if result.get("leakage") and not result["leakage"].get("error"):
                for v in result["leakage"].get("violations", []):
                    if v.get("severity") == "critical":
                        critical_issues.append(f"[LEAKAGE] {v['description']}")

            if critical_issues:
                self._trigger_alert(filepath, critical_issues)
            else:
                logger.info(f"Clean: {filepath}")

        except Exception as e:
            logger.error(f"Analysis failed for {filepath}: {e}")

    def _trigger_alert(self, filepath: str, issues: list[str]) -> None:
        """Log a security alert."""
        logger.warning(f"🚨 SECURITY ALERT: {filepath}")
        for issue in issues:
            logger.warning(f"  - {issue}")

        # In a real implementation, this could:
        # 1. Interrupt a Jupyter Kernel
        # 2. Send a Slack notification
        # 3. Block a git commit


def start_watchdog(path: str = ".") -> None:
    """Start the watchdog observer."""
    path_obj = Path(path).resolve()
    logger.info(f"Starting Silent Observer on {path_obj}")

    event_handler = DemystEventHandler()
    observer = Observer()
    observer.schedule(event_handler, str(path_obj), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    start_watchdog(target_path)

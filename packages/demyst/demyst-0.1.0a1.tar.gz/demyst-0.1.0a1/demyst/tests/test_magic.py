import sys
from unittest.mock import MagicMock, patch

import pytest
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import Magics, line_magic, magics_class
from IPython.display import HTML, Markdown, display

# Mock IPython modules BEFORE importing demyst.magic
# Force mock even if IPython is already loaded
sys.modules["IPython"] = MagicMock()
sys.modules["IPython.core"] = MagicMock()
sys.modules["IPython.core.magic"] = MagicMock()
sys.modules["IPython.display"] = MagicMock()
sys.modules["IPython.core.interactiveshell"] = MagicMock()


# Setup necessary attributes for inheritance and decorators
class MockMagics:
    def __init__(self, shell):
        self.shell = shell


sys.modules["IPython.core.magic"].Magics = MockMagics  # type: ignore


def magics_class(cls):
    return cls


sys.modules["IPython.core.magic"].magics_class = magics_class  # type: ignore
sys.modules["IPython.core.magic"].line_magic = lambda f: f  # type: ignore

# Setup display
sys.modules["IPython.display"].display = MagicMock()  # type: ignore
sys.modules["IPython.display"].HTML = MagicMock()  # type: ignore

import importlib

# Now we can import
import demyst.magic
from demyst.magic import DemystMagics, load_ipython_extension

importlib.reload(demyst.magic)


class TestDemystMagic:
    def setup_method(self):
        self.shell = MagicMock()
        self.shell.events = MagicMock()
        self.shell.events.callbacks = {"post_run_cell": []}

        def register(event, callback):
            self.shell.events.callbacks[event].append(callback)

        self.shell.events.register = register

    def test_load_extension(self):
        # Mock register_magics
        self.shell.register_magics = MagicMock()

        load_ipython_extension(self.shell)

        assert self.shell.register_magics.called

    @patch("demyst.magic.CIEnforcer")
    def test_mirage_detection(self, MockEnforcer):
        # Setup mock enforcer
        mock_enforcer_instance = MockEnforcer.return_value
        mock_enforcer_instance._guards_available = True
        mock_enforcer_instance.config_manager.is_rule_enabled.return_value = True

        # Mock MirageDetector
        mock_detector = MagicMock()
        mock_detector.mirages = [{"type": "mean", "line": 3, "function": None}]
        mock_enforcer_instance.MirageDetector.return_value = mock_detector

        # Instantiate magics
        magics = DemystMagics(self.shell)

        # Verify callback registration
        assert len(self.shell.events.callbacks["post_run_cell"]) > 0

        # Simulate execution
        code = "import numpy as np\nm = np.mean(x)"
        mock_result = MagicMock()
        mock_result.error_in_exec = False
        mock_result.info.raw_cell = code

        magics.post_run_cell(mock_result)

        # Verify display called
        from IPython.display import HTML, display

        assert display.called
        assert HTML.called

        # Verify content
        args, _ = HTML.call_args
        content = args[0]
        assert "Computational Mirage Detected" in content
        assert "mean" in content

    @patch("demyst.magic.CIEnforcer")
    def test_no_issues(self, MockEnforcer):
        mock_enforcer_instance = MockEnforcer.return_value
        mock_enforcer_instance._guards_available = True
        mock_enforcer_instance.config_manager.is_rule_enabled.return_value = True

        # Mock detectors to return no issues
        mock_enforcer_instance.MirageDetector.return_value.mirages = []
        mock_enforcer_instance.LeakageHunter.return_value.analyze.return_value = {}
        mock_enforcer_instance.HypothesisGuard.return_value.analyze_code.return_value = {}
        mock_enforcer_instance.UnitGuard.return_value.analyze.return_value = {}
        mock_enforcer_instance.TensorGuard.return_value.analyze.return_value = {}

        magics = DemystMagics(self.shell)

        mock_result = MagicMock()
        mock_result.error_in_exec = False
        mock_result.info.raw_cell = "x = 1"

        magics.post_run_cell(mock_result)

        from IPython.display import display

        display.reset_mock()

        assert not display.called

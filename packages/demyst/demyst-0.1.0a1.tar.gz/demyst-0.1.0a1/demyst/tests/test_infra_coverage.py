import pytest

from demyst.engine.parallel import ParallelAnalyzer
from demyst.exceptions import PluginValidationError
from demyst.fixer import DemystFixer, fix_source
from demyst.lazy import ImportManager, LazyModule, get_import_manager, import_time_report
from demyst.plugins import GuardPlugin, PluginRegistry
from demyst.red_team import RedTeamBenchmark


class _SimpleGuard(GuardPlugin):
    name = "simple_guard"
    description = "simple"

    def analyze(self, source: str):
        return {"violations": [{"line": 1, "type": "noop"}]}


class _BadGuard(GuardPlugin):
    # Missing name should trigger validation error
    description = "bad"

    def analyze(self, source: str):
        return {"violations": []}


def test_plugin_registry_registers_and_loads():
    registry = PluginRegistry()
    info = registry.register(_SimpleGuard)
    guard = registry.get_guard(info.name, {"enabled": True})
    assert guard.name == "simple_guard"
    listed = {p.name for p in registry.list_guards()}
    assert "simple_guard" in listed
    assert registry.unregister("simple_guard")


def test_plugin_registry_validation_error():
    registry = PluginRegistry()
    with pytest.raises(PluginValidationError):
        registry.register(_BadGuard)


def test_lazy_module_fallback_and_stats():
    lazy = LazyModule("definitely_missing_module_xyz", fallback=lambda: {"value": 1})
    assert not lazy.available
    loaded = lazy.module
    assert loaded == {"value": 1}
    stats = lazy.get_stats()
    assert stats.module_name == "definitely_missing_module_xyz"
    assert not stats.success


def test_import_manager_preload_and_report():
    manager: ImportManager = get_import_manager()
    extra = LazyModule("math")
    manager.register(extra)
    manager.preload("math")
    manager.do_preload()
    assert "math" in manager.loaded_modules()
    report = import_time_report()
    assert "Module Import Time Report" in report


def test_parallel_analyzer_threads_basic(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text("x = 1\n", encoding="utf-8")
    analyzer = ParallelAnalyzer(
        use_processes=False,
        analysis_options={
            "mirage": False,
            "leakage": False,
            "hypothesis": False,
            "unit": False,
            "tensor": False,
        },
        max_workers=1,
    )
    report = analyzer.analyze_files([str(sample)])
    assert report.total_files == 1
    assert report.successful_files == 1
    assert report.file_results[0].success


def test_fix_source_cst_and_text_paths(tmp_path):
    source = "import numpy as np\nx = np.mean([1, 2, 3])\n"
    fixed, actions = fix_source(source, [{"type": "mean", "line": 2}], dry_run=True)
    assert "VariationTensor" in fixed
    assert actions

    fixer = DemystFixer(dry_run=True, backup=False)
    fixer._use_cst = False  # force text path
    fixed_text, text_actions = fixer._fix_with_text(source, [{"type": "mean", "line": 2}])
    assert "# TODO: demyst" in fixed_text
    assert text_actions


def test_red_team_generates_50_cases():
    bench = RedTeamBenchmark()
    bench.generate_dataset()
    assert len(bench.test_cases) == 50
    categories = {case[0] for case in bench.test_cases}
    assert len(categories) == 10

from pathlib import Path

import pytest
from pytest_md.report import MarkDownReport
from pytest_md.fixtures import extras_stash_key
from pytest_md.report_data import ReportData
from pytest_md.utils import _read_template

# Ensure the extras fixture is registered
pytest_plugins = ['pytest_md']


class MarkdownPlugin:
    def __init__(self, config):
        self.md_path = config.getoption("mdpath")
        if self.md_path:
            resources_path = Path(__file__).parent.joinpath("res")
            report_template = _read_template([resources_path], "report.template.jinja2")
            report_data = ReportData(config)
            self.markdown_report = MarkDownReport(self.md_path, report_data, report_template)
        else:
            self.markdown_report = None

    @pytest.hookimpl(trylast=True)
    def pytest_runtest_logreport(self, report):
        if self.markdown_report:
            self.markdown_report.pytest_runtest_logreport(report)

    @pytest.hookimpl(trylast=True)
    def pytest_sessionstart(self, session):
        if self.markdown_report:
            self.markdown_report.pytest_sessionstart(session)

    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session):
        if self.markdown_report:
            self.markdown_report.pytest_sessionfinish(session)


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--md",
        action="store",
        dest="mdpath",
        metavar="path",
        default=None,
        help="create md report file at given path.",
    )


def pytest_configure(config):
    md_path = config.getoption("mdpath")
    if md_path:
        plugin = MarkdownPlugin(config)
        config.pluginmanager.register(plugin, "markdown")


def pytest_unconfigure(config):
    plugin = config.pluginmanager.getplugin("markdown")
    if plugin:
        config.pluginmanager.unregister(plugin)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        fixture_extras = item.config.stash.get(extras_stash_key, [])
        plugin_extras = getattr(report, "extras", [])
        report.extras = fixture_extras + plugin_extras

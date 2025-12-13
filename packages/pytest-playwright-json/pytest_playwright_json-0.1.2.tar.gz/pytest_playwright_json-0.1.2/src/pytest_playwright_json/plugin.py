"""pytest plugin to generate Playwright-compatible JSON reports"""

import json
from pathlib import Path
from typing import Any

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.reports import TestReport
from _pytest.terminal import TerminalReporter

from .attachments import match_attachments_to_test
from .collector import ResultCollector


def pytest_addoption(parser: Parser) -> None:
    """Add command line options for the plugin"""
    group = parser.getgroup("playwright-json", "Playwright JSON Report")

    group.addoption(
        "--playwright-json",
        action="store",
        dest="playwright_json_path",
        metavar="path",
        default=None,
        help="Generate a Playwright-compatible JSON report at the given path",
    )

    group.addoption(
        "--playwright-json-include-attachments",
        action="store_true",
        dest="playwright_json_attachments",
        default=True,
        help="Include attachment paths in the JSON report (default: True)",
    )

    group.addoption(
        "--playwright-json-test-results-dir",
        action="store",
        dest="playwright_json_test_results_dir",
        metavar="path",
        default=None,
        help="Directory containing test artifacts (default: auto-detected from --playwright-json path or 'test-results')",
    )


def pytest_configure(config: Config) -> None:
    """Configure the plugin"""
    json_path = config.option.playwright_json_path

    if json_path:
        # Create the reporter and register it
        reporter = PlaywrightJsonReporter(config, json_path)
        config._playwright_json_reporter = reporter
        config.pluginmanager.register(reporter, "playwright_json_reporter")


def pytest_unconfigure(config: Config) -> None:
    """Clean up after the test session"""
    reporter = getattr(config, "_playwright_json_reporter", None)
    if reporter:
        config.pluginmanager.unregister(reporter)
        del config._playwright_json_reporter


class PlaywrightJsonReporter:
    """Reporter that generates Playwright-compatible JSON output"""

    def __init__(self, config: Config, json_path: str):
        self.config = config
        self.json_path = Path(json_path)
        self.collector = ResultCollector(config)

        # Options
        self.include_attachments = config.option.playwright_json_attachments
        self.test_results_dir = self._resolve_test_results_dir(config)

    def _resolve_test_results_dir(self, config: Config) -> str:
        """
        Smart resolution of test results directory:
        1. Use explicit --playwright-json-test-results-dir if provided
        2. Use pytest-playwright's --output if available
        3. Infer from --playwright-json path's parent directory
        4. Fall back to 'test-results'
        """
        # 1. Explicit option takes priority
        explicit_dir = config.option.playwright_json_test_results_dir
        if explicit_dir:
            return explicit_dir

        # 2. Check pytest-playwright's --output option
        if hasattr(config.option, 'output') and config.option.output:
            return config.option.output

        # 3. Infer from JSON report path (parent directory)
        json_parent = self.json_path.parent
        if json_parent != Path('.') and json_parent.name:
            return str(json_parent)

        # 4. Default fallback
        return "test-results"

    def pytest_sessionstart(self, session: pytest.Session) -> None:  # noqa: ARG002
        """Called when the test session starts"""
        del session  # Unused but required by pytest hook signature
        self.collector.session_start()

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        """Called after each test phase (setup, call, teardown)"""
        # Handle call phase results
        if report.when == "call":
            # Add the test result
            self.collector.add_result(report)

            # Collect attachments if enabled
            if self.include_attachments:
                self._attach_artifacts(report)

        # Handle setup phase skips (skip markers cause skip during setup)
        elif report.when == "setup" and report.skipped:
            self.collector.add_result(report)

    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int) -> None:  # noqa: ARG002
        """Called after the test session finishes"""
        del session, exitstatus  # Unused but required by pytest hook signature
        self.collector.session_finish()

        # Build the final report
        report = self.collector.build_report()

        # Write to file
        self._write_report(report)

        # Print summary
        terminal = self.config.pluginmanager.get_plugin("terminalreporter")
        if terminal:
            self._print_summary(terminal, report)

    def _attach_artifacts(self, report: TestReport) -> None:
        """Attach artifacts (screenshots, videos, traces) to test results"""
        try:
            attachments = match_attachments_to_test(
                report.nodeid,
                self.test_results_dir,
            )

            if attachments:
                # Find the spec using the same parsing logic as add_result
                # Parse nodeid the same way collector does
                file_path, class_name, test_name = self.collector._parse_nodeid(report.nodeid)
                spec_id = f"{file_path}::{class_name}::{test_name}" if class_name else f"{file_path}::{test_name}"

                if spec_id in self.collector.tests:
                    test = self.collector.tests[spec_id]
                    if test.results:
                        test.results[-1].attachments.extend(attachments)
        except Exception as e:
            # Log attachment errors in verbose mode
            import sys
            print(f"Warning: Failed to attach artifacts for {report.nodeid}: {e}", file=sys.stderr)

    def _write_report(self, report: Any) -> None:
        """Write the JSON report to file"""
        # Ensure parent directory exists
        self.json_path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

    def _print_summary(self, terminal: TerminalReporter, report: Any) -> None:
        """Print summary to terminal"""
        terminal.write_sep("-", "Playwright JSON Report")
        terminal.write_line(f"Report written to: {self.json_path.absolute()}")
        terminal.write_line(
            f"Stats: {report.stats.expected} passed, "
            f"{report.stats.unexpected} failed, "
            f"{report.stats.skipped} skipped, "
            f"{report.stats.flaky} flaky"
        )

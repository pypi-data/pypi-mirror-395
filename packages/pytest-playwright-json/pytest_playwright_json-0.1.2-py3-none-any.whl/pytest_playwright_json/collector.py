"""Collect and transform pytest results to Playwright format"""

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from _pytest.reports import TestReport

from .models import (
    Annotation,
    Config,
    JSONReportError,
    Location,
    PlaywrightReport,
    ProjectConfig,
    Spec,
    Stats,
    Suite,
    Test,
    TestError,
    TestResult,
)


class ResultCollector:
    """Collects pytest results and transforms them to Playwright JSON format"""

    def __init__(self, config: Any):
        self.pytest_config = config
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        # Storage for test results grouped by file/class
        self.suites: Dict[str, Suite] = {}
        self.specs: Dict[str, Spec] = {}
        self.tests: Dict[str, Test] = {}

        # Statistics
        self.expected = 0
        self.unexpected = 0
        self.skipped = 0
        self.flaky = 0

        # Track retries
        self.retry_counts: Dict[str, int] = {}

        # Global errors
        self.errors: List[TestError] = []

    def session_start(self) -> None:
        """Called when test session starts"""
        self.start_time = datetime.now(timezone.utc)

    def session_finish(self) -> None:
        """Called when test session finishes"""
        self.end_time = datetime.now(timezone.utc)

    def add_result(self, report: TestReport) -> None:
        """Add a test result from pytest"""
        # Handle both call phase and setup-phase skips
        if report.when == "setup" and not report.skipped:
            # Only process setup phase if it's a skip
            return
        if report.when == "teardown":
            # Don't process teardown
            return

        # Parse node ID to get file, class, and test name
        file_path, class_name, test_name = self._parse_nodeid(report.nodeid)

        # Create unique IDs
        suite_id = file_path
        spec_id = f"{file_path}::{class_name}::{test_name}" if class_name else f"{file_path}::{test_name}"

        # Get or create suite
        if suite_id not in self.suites:
            self.suites[suite_id] = Suite(
                title=Path(file_path).name,
                file=file_path,
                line=0,
                column=0,
            )

        # Get or create spec
        if spec_id not in self.specs:
            # Generate unique ID for spec (matching Playwright format)
            spec_hash = self._generate_spec_id(spec_id)

            # Extract tags from markers
            tags = self._extract_tags(report)

            self.specs[spec_id] = Spec(
                title=test_name,
                ok=True,
                tags=tags,
                id=spec_hash,
                file=file_path,
                line=report.location[1] if report.location else 0,
                column=0,
            )

            # Detect browser from pytest-playwright
            browser = self._detect_browser(report)

            # Create test entry
            self.tests[spec_id] = Test(
                timeout=30000,
                annotations=self._extract_annotations(report),
                expectedStatus="passed",
                projectId=browser,
                projectName=browser,
                results=[],
                status="expected",
            )

        # Get retry count
        retry = self.retry_counts.get(spec_id, 0)
        self.retry_counts[spec_id] = retry + 1

        # Create test result
        test_result = self._create_test_result(report, retry)
        self.tests[spec_id].results.append(test_result)

        # Update spec and test status
        self._update_status(spec_id, report)

    def _parse_nodeid(self, nodeid: str) -> Tuple[str, Optional[str], str]:
        """Parse pytest nodeid into file, class, and test name"""
        # Format: path/to/test_file.py::TestClass::test_method
        # or: path/to/test_file.py::test_function

        parts = nodeid.split("::")
        file_path = parts[0]

        if len(parts) == 3:
            # Class-based test
            class_name = parts[1]
            test_name = parts[2]
        elif len(parts) == 2:
            # Function-based test
            class_name = None
            test_name = parts[1]
        else:
            class_name = None
            test_name = nodeid

        # Remove parametrize suffix for display
        if "[" in test_name:
            base_name = test_name.split("[")[0]
            param_id = test_name.split("[")[1].rstrip("]")
            test_name = f"{base_name} [{param_id}]"

        return file_path, class_name, test_name

    def _generate_spec_id(self, spec_id: str) -> str:
        """Generate a unique spec ID matching Playwright format"""
        hash1 = hashlib.md5(spec_id.encode()).hexdigest()[:20]
        hash2 = hashlib.md5(f"{spec_id}_salt".encode()).hexdigest()[:20]
        return f"{hash1}-{hash2}"

    def _detect_browser(self, report: TestReport) -> str:
        """Detect browser name from pytest-playwright"""
        browsers = {"chromium", "firefox", "webkit"}

        # Check keywords for browser name
        if hasattr(report, "keywords"):
            for keyword in report.keywords:
                if keyword in browsers:
                    return keyword

        # Check nodeid for browser in parametrize brackets
        # e.g., test_login[chromium] or test_login[valid-chromium]
        nodeid = report.nodeid
        if "[" in nodeid:
            bracket_content = nodeid.split("[")[-1].rstrip("]")
            # Check if browser is in the bracket content
            for browser in browsers:
                if browser in bracket_content:
                    return browser

        # Default to chromium (most common)
        return "chromium"

    def _extract_tags(self, report: TestReport) -> List[str]:
        """Extract tags from pytest markers"""
        tags = []

        # Known internal/built-in markers to skip
        skip_markers = {
            "parametrize", "usefixtures", "filterwarnings", "skip", "skipif",
            "xfail", "tryfirst", "trylast", "hookwrapper", "hookspec",
            "pytestmark",  # pytest internal
        }

        # Browser names to skip (from pytest-playwright)
        browser_names = {"chromium", "firefox", "webkit"}

        if hasattr(report, "keywords"):
            keywords = report.keywords
            for keyword in keywords:
                # Skip empty strings
                if not keyword or not keyword.strip():
                    continue
                # Skip internal pytest markers
                if keyword.startswith("_"):
                    continue
                # Skip built-in markers
                if keyword in skip_markers:
                    continue
                # Skip browser names
                if keyword in browser_names:
                    continue
                # Skip file/class/function names and paths
                if "::" in keyword or keyword.endswith(".py"):
                    continue
                # Skip bracket notation (parametrize IDs)
                if "[" in keyword or "]" in keyword:
                    continue
                # Skip known non-marker keywords (paths, test names)
                if "/" in keyword or keyword.startswith("test_") or keyword.startswith("Test"):
                    continue
                # Keep actual markers
                tags.append(keyword)

        return list(set(tags))  # Remove duplicates

    def _extract_annotations(self, report: TestReport) -> List[Annotation]:
        """Extract annotations from pytest markers"""
        annotations: List[Annotation] = []

        if hasattr(report, "keywords"):
            # Check for skip marker
            if "skip" in report.keywords or "skipif" in report.keywords:
                annotations.append(Annotation(type="skip", description=""))

            # Check for xfail marker
            if "xfail" in report.keywords:
                annotations.append(Annotation(type="fixme", description="Expected to fail"))

        return annotations

    def _create_test_result(self, report: TestReport, retry: int) -> TestResult:
        """Create a TestResult from pytest report"""
        # Determine status
        if report.passed:
            status = "passed"
        elif report.skipped:
            status = "skipped"
        elif report.failed:
            status = "failed"
        else:
            status = "failed"

        # Extract error info
        error = None
        errors: List[JSONReportError] = []

        # Capture error for failed tests (check status, not just report.failed for reruns)
        if (status == "failed" or report.failed) and report.longrepr:
            error = self._extract_error(report)
            if error:
                # Create JSONReportError for the errors array (simpler format)
                json_error = JSONReportError(
                    message=error.message,
                    location=error.location,
                )
                errors.append(json_error)

        # Get stdout/stderr (as {text: string} format per Playwright schema)
        stdout: List[Dict[str, str]] = []
        stderr: List[Dict[str, str]] = []

        # pytest stores captured output in report.sections as list of (name, content) tuples
        if hasattr(report, "sections"):
            for name, content in report.sections:
                if not content:
                    continue
                if "stdout" in name.lower() or "Captured stdout" in name:
                    for line in content.split("\n"):
                        if line.strip():
                            stdout.append({"text": line})
                elif "stderr" in name.lower() or "Captured stderr" in name:
                    for line in content.split("\n"):
                        if line.strip():
                            stderr.append({"text": line})
                elif "log" in name.lower() or "Captured log" in name:
                    # Also capture log output as stderr
                    for line in content.split("\n"):
                        if line.strip():
                            stderr.append({"text": line})

        # Fallback to capstdout/capstderr if sections is empty
        if not stdout and hasattr(report, "capstdout") and report.capstdout:
            for line in report.capstdout.split("\n"):
                if line.strip():
                    stdout.append({"text": line})
        if not stderr and hasattr(report, "capstderr") and report.capstderr:
            for line in report.capstderr.split("\n"):
                if line.strip():
                    stderr.append({"text": line})

        # Calculate test start time from report.start timestamp if available,
        # otherwise calculate from current time minus duration
        duration_ms = int(report.duration * 1000)
        now = datetime.now(timezone.utc)

        # pytest report has a 'start' attribute with the test start timestamp
        if hasattr(report, 'start'):
            # report.start is a float timestamp
            test_start = datetime.fromtimestamp(report.start, tz=timezone.utc)
        else:
            # Fallback: calculate from now - duration
            from datetime import timedelta
            test_start = now - timedelta(seconds=report.duration)

        # Format as ISO string with Z suffix (already UTC)
        start_time_str = test_start.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        return TestResult(
            workerIndex=0,
            parallelIndex=0,
            status=status,
            duration=duration_ms,
            error=error,
            errors=errors,
            stdout=stdout,
            stderr=stderr,
            retry=retry,
            startTime=start_time_str,
            annotations=[],
            attachments=[],  # Attachments handled separately
        )

    def _extract_error(self, report: TestReport) -> Optional[TestError]:
        """Extract error information from test report"""
        if not report.longrepr:
            return None

        message = ""
        stack = ""
        location = None

        # Get the string representation of the error
        if hasattr(report.longrepr, "reprcrash"):
            crash = report.longrepr.reprcrash
            message = crash.message if hasattr(crash, "message") else str(crash)

            location = Location(
                file=str(crash.path) if hasattr(crash, "path") else "",
                line=crash.lineno if hasattr(crash, "lineno") else 0,
                column=0,
            )

        # Get full traceback - try multiple ways
        if hasattr(report.longrepr, "reprtraceback"):
            # Full representation includes traceback + crash info
            stack = str(report.longrepr)
        elif hasattr(report.longrepr, "toterminal"):
            # Can convert to string
            stack = str(report.longrepr)
        else:
            stack = str(report.longrepr)

        # If message is empty, try to extract from stack
        if not message and stack:
            lines = stack.strip().split("\n")
            # Last line usually contains the error message
            if lines:
                message = lines[-1].strip()

        # Also capture any exception info from the report
        if hasattr(report, "excinfo") and report.excinfo:
            exc_type = report.excinfo.typename if hasattr(report.excinfo, "typename") else ""
            exc_value = str(report.excinfo.value) if hasattr(report.excinfo, "value") else ""
            if exc_type and exc_value and not message:
                message = f"{exc_type}: {exc_value}"

        return TestError(
            message=message or "Test failed",
            stack=stack,
            location=location,
        )

    def _update_status(self, spec_id: str, report: TestReport) -> None:
        """Update spec and test status based on result"""
        spec = self.specs[spec_id]
        test = self.tests[spec_id]

        if report.skipped:
            spec.ok = True
            test.status = "skipped"
            self.skipped += 1
        elif report.passed:
            # Check if this was a retry that passed (flaky)
            if len(test.results) > 1:
                # Had previous failures, now passed = flaky
                test.status = "flaky"
                spec.ok = True
                self.flaky += 1
            else:
                spec.ok = True
                test.status = "expected"
                self.expected += 1
        elif report.failed:
            spec.ok = False
            test.status = "unexpected"
            # Only count as unexpected if all retries failed
            # This will be adjusted in finalize()

    def finalize(self) -> None:
        """Finalize results after all tests complete"""
        # Reset counters for final calculation
        self.expected = 0
        self.unexpected = 0
        self.skipped = 0
        self.flaky = 0

        for spec_id, test in self.tests.items():
            spec = self.specs[spec_id]

            if not test.results:
                continue

            # Get final result (last one)
            final_result = test.results[-1]

            if final_result.status == "skipped":
                test.status = "skipped"
                spec.ok = True
                self.skipped += 1
            elif final_result.status == "passed":
                if len(test.results) > 1:
                    # Passed after retry = flaky
                    test.status = "flaky"
                    spec.ok = True
                    self.flaky += 1
                else:
                    test.status = "expected"
                    spec.ok = True
                    self.expected += 1
            else:
                # Failed
                test.status = "unexpected"
                spec.ok = False
                self.unexpected += 1

            # Link spec to tests
            spec.tests = [test]

        # Link specs to suites
        for spec_id, spec in self.specs.items():
            file_path = spec_id.split("::")[0]
            if file_path in self.suites:
                self.suites[file_path].specs.append(spec)

    def build_report(self) -> PlaywrightReport:
        """Build the final Playwright report"""
        self.finalize()

        # Calculate duration
        duration = 0.0
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds() * 1000

        # Build config
        root_dir = str(self.pytest_config.rootdir) if hasattr(self.pytest_config, "rootdir") else os.getcwd()

        # Collect unique browsers used in tests
        browsers_used = set()
        for test in self.tests.values():
            if test.projectName:
                browsers_used.add(test.projectName)
        if not browsers_used:
            browsers_used.add("chromium")

        # Create project configs for each browser
        projects = [
            ProjectConfig(
                id=browser,
                name=browser,
                testDir=root_dir,
                outputDir="test-results",
            )
            for browser in sorted(browsers_used)
        ]

        config = Config(
            configFile="pytest.ini",
            rootDir=root_dir,
            fullyParallel=False,
            version="pytest-playwright",
            workers=1,
            projects=projects,
            reporter=[
                ["pytest-playwright-json", {"outputFile": "playwright-report.json"}]
            ],
        )

        # Build stats - format start time properly as UTC ISO string
        if self.start_time:
            stats_start = self.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        else:
            stats_start = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        stats = Stats(
            startTime=stats_start,
            duration=duration,
            expected=self.expected,
            skipped=self.skipped,
            unexpected=self.unexpected,
            flaky=self.flaky,
        )

        return PlaywrightReport(
            config=config,
            suites=list(self.suites.values()),
            stats=stats,
            errors=self.errors,
        )

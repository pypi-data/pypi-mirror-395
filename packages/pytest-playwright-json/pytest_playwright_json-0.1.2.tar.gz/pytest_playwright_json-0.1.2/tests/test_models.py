"""Tests for Playwright JSON report models"""

import json
from datetime import datetime

import pytest

from pytest_playwright_json.models import (
    Annotation,
    Attachment,
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
    TestStep,
)


class TestLocation:
    """Tests for Location model"""

    def test_default_values(self):
        loc = Location()
        assert loc.file == ""
        assert loc.line == 0
        assert loc.column == 0

    def test_with_values(self):
        loc = Location(file="test.py", line=10, column=5)
        assert loc.file == "test.py"
        assert loc.line == 10
        assert loc.column == 5


class TestAnnotation:
    """Tests for Annotation model"""

    def test_required_type(self):
        ann = Annotation(type="skip")
        assert ann.type == "skip"
        assert ann.description is None

    def test_with_description(self):
        ann = Annotation(type="fixme", description="Expected to fail")
        assert ann.type == "fixme"
        assert ann.description == "Expected to fail"


class TestAttachment:
    """Tests for Attachment model"""

    def test_with_path(self):
        att = Attachment(name="screenshot", contentType="image/png", path="/path/to/screenshot.png")
        assert att.name == "screenshot"
        assert att.contentType == "image/png"
        assert att.path == "/path/to/screenshot.png"
        assert att.body is None

    def test_with_body(self):
        att = Attachment(name="inline", contentType="text/plain", body="SGVsbG8gV29ybGQ=")
        assert att.body == "SGVsbG8gV29ybGQ="
        assert att.path is None


class TestTestResult:
    """Tests for TestResult model"""

    def test_minimal(self):
        result = TestResult(status="passed", duration=100)
        assert result.status == "passed"
        assert result.duration == 100
        assert result.retry == 0
        assert result.errors == []
        assert result.attachments == []

    def test_with_error(self):
        error = TestError(message="Assertion failed", stack="at test.py:10")
        result = TestResult(
            status="failed",
            duration=50,
            error=error,
            errors=[JSONReportError(message="Error 1")],
        )
        assert result.error is not None
        assert result.error.message == "Assertion failed"
        assert len(result.errors) == 1


class TestTestStep:
    """Tests for TestStep model"""

    def test_simple_step(self):
        step = TestStep(title="Click button", duration=50)
        assert step.title == "Click button"
        assert step.duration == 50
        assert step.error is None
        assert step.steps is None

    def test_nested_steps(self):
        inner = TestStep(title="Wait for response", duration=30)
        outer = TestStep(title="Make API call", duration=100, steps=[inner])
        assert len(outer.steps) == 1
        assert outer.steps[0].title == "Wait for response"


class TestSpec:
    """Tests for Spec model"""

    def test_minimal(self):
        spec = Spec(title="test_login")
        assert spec.title == "test_login"
        assert spec.ok is True
        assert spec.tags == []
        assert spec.tests == []

    def test_with_tags(self):
        spec = Spec(title="test_login", tags=["smoke", "auth"])
        assert len(spec.tags) == 2
        assert "smoke" in spec.tags


class TestSuite:
    """Tests for Suite model"""

    def test_minimal(self):
        suite = Suite(title="test_login.py")
        assert suite.title == "test_login.py"
        assert suite.specs == []
        assert suite.suites is None

    def test_nested_suites(self):
        inner = Suite(title="TestLogin")
        outer = Suite(title="test_login.py", suites=[inner])
        assert len(outer.suites) == 1


class TestStats:
    """Tests for Stats model"""

    def test_all_fields(self):
        stats = Stats(
            startTime="2024-01-01T00:00:00.000Z",
            duration=5000.5,
            expected=10,
            skipped=2,
            unexpected=1,
            flaky=1,
        )
        assert stats.startTime == "2024-01-01T00:00:00.000Z"
        assert stats.duration == 5000.5
        assert stats.expected == 10
        assert stats.unexpected == 1
        assert stats.skipped == 2
        assert stats.flaky == 1


class TestPlaywrightReport:
    """Tests for complete PlaywrightReport model"""

    def test_minimal_report(self):
        stats = Stats(
            startTime="2024-01-01T00:00:00.000Z",
            duration=1000,
            expected=1,
        )
        report = PlaywrightReport(stats=stats)
        assert report.stats.expected == 1
        assert report.suites == []
        assert report.errors == []

    def test_full_report(self):
        """Test a complete report with all nested structures"""
        # Create attachment
        attachment = Attachment(
            name="screenshot",
            contentType="image/png",
            path="/path/to/screenshot.png",
        )

        # Create test result
        result = TestResult(
            workerIndex=0,
            parallelIndex=0,
            status="passed",
            duration=150,
            retry=0,
            startTime="2024-01-01T00:00:01.000Z",
            attachments=[attachment],
        )

        # Create test
        test = Test(
            timeout=30000,
            expectedStatus="passed",
            projectId="pytest",
            projectName="pytest",
            results=[result],
            status="expected",
        )

        # Create spec
        spec = Spec(
            title="test_valid_login",
            ok=True,
            tags=["smoke"],
            tests=[test],
            id="abc123-def456",
            file="test_login.py",
            line=10,
            column=0,
        )

        # Create suite
        suite = Suite(
            title="test_login.py",
            file="tests/test_login.py",
            specs=[spec],
        )

        # Create config
        config = Config(
            rootDir="/path/to/project",
            version="pytest",
            projects=[
                ProjectConfig(
                    id="pytest",
                    name="pytest",
                    testDir="/path/to/project/tests",
                )
            ],
        )

        # Create stats
        stats = Stats(
            startTime="2024-01-01T00:00:00.000Z",
            duration=5000,
            expected=1,
        )

        # Create full report
        report = PlaywrightReport(
            config=config,
            suites=[suite],
            stats=stats,
        )

        # Validate structure
        assert len(report.suites) == 1
        assert len(report.suites[0].specs) == 1
        assert len(report.suites[0].specs[0].tests) == 1
        assert len(report.suites[0].specs[0].tests[0].results) == 1
        assert report.suites[0].specs[0].tests[0].results[0].status == "passed"

    def test_to_dict(self):
        """Test serialization to dictionary"""
        stats = Stats(
            startTime="2024-01-01T00:00:00.000Z",
            duration=1000,
            expected=1,
        )
        report = PlaywrightReport(stats=stats)
        data = report.to_dict()

        assert "config" in data
        assert "suites" in data
        assert "stats" in data
        assert "errors" in data
        assert data["stats"]["expected"] == 1

    def test_to_json(self):
        """Test serialization to JSON string"""
        stats = Stats(
            startTime="2024-01-01T00:00:00.000Z",
            duration=1000,
            expected=1,
        )
        report = PlaywrightReport(stats=stats)
        json_str = report.to_json()

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed["stats"]["expected"] == 1

    def test_json_format_matches_playwright(self):
        """Test that generated JSON has correct Playwright format"""
        result = TestResult(
            workerIndex=0,
            parallelIndex=0,
            status="passed",
            duration=100,
            retry=0,
            startTime="2024-01-01T00:00:00.000Z",
        )

        test = Test(
            timeout=30000,
            expectedStatus="passed",
            projectId="pytest",
            projectName="pytest",
            results=[result],
            status="expected",
        )

        spec = Spec(
            title="test_example",
            ok=True,
            tests=[test],
            id="test-id",
            file="test.py",
        )

        suite = Suite(
            title="test.py",
            file="tests/test.py",
            specs=[spec],
        )

        stats = Stats(
            startTime="2024-01-01T00:00:00.000Z",
            duration=1000,
            expected=1,
            unexpected=0,
            skipped=0,
            flaky=0,
        )

        report = PlaywrightReport(suites=[suite], stats=stats)
        data = report.to_dict()

        # Check required top-level fields
        assert "config" in data
        assert "suites" in data
        assert "stats" in data
        assert "errors" in data

        # Check suite structure
        assert data["suites"][0]["title"] == "test.py"
        assert data["suites"][0]["file"] == "tests/test.py"
        assert "specs" in data["suites"][0]

        # Check spec structure
        spec_data = data["suites"][0]["specs"][0]
        assert spec_data["title"] == "test_example"
        assert spec_data["ok"] is True
        assert "tests" in spec_data

        # Check test structure
        test_data = spec_data["tests"][0]
        assert test_data["status"] == "expected"
        assert test_data["expectedStatus"] == "passed"
        assert "results" in test_data

        # Check result structure
        result_data = test_data["results"][0]
        assert result_data["status"] == "passed"
        assert result_data["duration"] == 100
        assert result_data["retry"] == 0

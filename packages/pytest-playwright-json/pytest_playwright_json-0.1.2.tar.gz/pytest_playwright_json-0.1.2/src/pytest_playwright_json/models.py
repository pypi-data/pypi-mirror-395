"""Pydantic models matching Playwright JSON report schema

Based on: https://github.com/microsoft/playwright/blob/main/packages/playwright/types/testReporter.d.ts
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class Location(BaseModel):
    """Source code location"""
    file: str = ""
    line: int = 0
    column: int = 0


class JSONReportError(BaseModel):
    """Error in JSON report format"""
    message: str = ""
    location: Optional[Location] = None


class TestError(BaseModel):
    """Full test error with stack trace"""
    message: str = ""
    stack: str = ""
    location: Optional[Location] = None
    snippet: str = ""


class Attachment(BaseModel):
    """Test attachment (screenshot, video, trace)"""
    name: str
    contentType: str
    path: Optional[str] = None
    body: Optional[str] = None  # Base64 encoded for inline attachments


class STDIOEntry(BaseModel):
    """Standard output entry - can be text or buffer"""
    text: Optional[str] = None
    buffer: Optional[str] = None  # Base64 encoded


class TestStep(BaseModel):
    """Test step within a result"""
    title: str
    duration: int  # milliseconds
    error: Optional[TestError] = None
    steps: Optional[List["TestStep"]] = None


# Enable forward reference for nested steps
TestStep.model_rebuild()


class Annotation(BaseModel):
    """Test annotation"""
    type: str
    description: Optional[str] = None


class TestResult(BaseModel):
    """Individual test result (one per retry)"""
    workerIndex: int = 0
    parallelIndex: int = 0
    status: Optional[str] = None  # "passed", "failed", "timedOut", "skipped", "interrupted"
    duration: int = 0  # milliseconds
    error: Optional[TestError] = None
    errors: List[JSONReportError] = Field(default_factory=list)
    stdout: List[Union[Dict[str, str], STDIOEntry]] = Field(default_factory=list)
    stderr: List[Union[Dict[str, str], STDIOEntry]] = Field(default_factory=list)
    retry: int = 0
    steps: Optional[List[TestStep]] = None
    startTime: str = ""  # ISO format
    attachments: List[Attachment] = Field(default_factory=list)
    annotations: List[Annotation] = Field(default_factory=list)
    errorLocation: Optional[Location] = None


class Test(BaseModel):
    """Test within a spec (JSONReportTest)"""
    timeout: int = 30000
    annotations: List[Annotation] = Field(default_factory=list)
    expectedStatus: str = "passed"  # TestStatus
    projectId: str = ""
    projectName: str = ""
    results: List[TestResult] = Field(default_factory=list)
    status: str = "expected"  # "expected", "unexpected", "flaky", "skipped"


class Spec(BaseModel):
    """Test specification (JSONReportSpec)"""
    title: str
    ok: bool = True
    tags: List[str] = Field(default_factory=list)
    tests: List[Test] = Field(default_factory=list)
    id: str = ""
    file: str = ""
    line: int = 0
    column: int = 0


class Suite(BaseModel):
    """Test suite (JSONReportSuite)"""
    title: str
    file: str = ""
    line: int = 0
    column: int = 0
    specs: List[Spec] = Field(default_factory=list)
    suites: Optional[List["Suite"]] = None


# Enable forward reference for nested suites
Suite.model_rebuild()


class ProjectConfig(BaseModel):
    """Project configuration"""
    outputDir: str = "test-results"
    repeatEach: int = 1
    retries: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    id: str = ""
    name: str = ""
    testDir: str = ""
    testIgnore: List[str] = Field(default_factory=list)
    testMatch: List[str] = Field(default_factory=list)
    timeout: int = 30000


class Config(BaseModel):
    """Playwright configuration (JSONReport.config)"""
    configFile: str = ""
    rootDir: str = ""
    forbidOnly: bool = False
    fullyParallel: bool = False
    globalSetup: Optional[str] = None
    globalTeardown: Optional[str] = None
    globalTimeout: int = 0
    grep: Dict[str, Any] = Field(default_factory=dict)
    grepInvert: Optional[Dict[str, Any]] = None
    maxFailures: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    preserveOutput: str = "always"
    reporter: List[List[Any]] = Field(default_factory=list)
    reportSlowTests: Dict[str, int] = Field(default_factory=lambda: {"max": 5, "threshold": 300000})
    quiet: bool = False
    projects: List[ProjectConfig] = Field(default_factory=list)
    shard: Optional[Dict[str, int]] = None
    updateSnapshots: str = "missing"
    updateSourceMethod: str = "patch"
    version: str = "1.0.0"
    workers: int = 1
    webServer: Optional[Dict[str, Any]] = None


class Stats(BaseModel):
    """Test run statistics"""
    startTime: str  # ISO format
    duration: float  # milliseconds
    expected: int = 0
    skipped: int = 0
    unexpected: int = 0
    flaky: int = 0


class PlaywrightReport(BaseModel):
    """Complete Playwright JSON report (JSONReport)"""
    config: Config = Field(default_factory=Config)
    suites: List[Suite] = Field(default_factory=list)
    stats: Stats
    errors: List[TestError] = Field(default_factory=list)

    def to_json(self) -> str:
        """Serialize to JSON string"""
        return self.model_dump_json(indent=2, exclude_none=True)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return self.model_dump(exclude_none=True)

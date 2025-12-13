"""Handle test attachments (screenshots, videos, traces) from pytest-playwright"""

from pathlib import Path
from typing import Dict, List, Optional

from .models import Attachment


# Content type mappings
CONTENT_TYPES: Dict[str, str] = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".webm": "video/webm",
    ".mp4": "video/mp4",
    ".zip": "application/zip",
    ".json": "application/json",
    ".html": "text/html",
    ".txt": "text/plain",
    ".log": "text/plain",
}


class AttachmentCollector:
    """Collects and processes test attachments from pytest-playwright"""

    def __init__(self, test_results_dir: str = "test-results"):
        self.test_results_dir = Path(test_results_dir)
        self.attachments: Dict[str, List[Attachment]] = {}

    def collect_for_test(self, nodeid: str) -> List[Attachment]:
        """Collect attachments for a specific test"""
        attachments: List[Attachment] = []

        # Convert nodeid to directory name (pytest-playwright convention)
        test_dir = self._nodeid_to_dir(nodeid)

        if not test_dir.exists():
            return attachments

        # Scan for attachment files
        for file_path in test_dir.iterdir():
            if file_path.is_file():
                attachment = self._create_attachment(file_path)
                if attachment:
                    attachments.append(attachment)

        return attachments

    def _nodeid_to_dir(self, nodeid: str) -> Path:
        """Convert pytest nodeid to test results directory path

        pytest-playwright creates directories like:
        tests-test_reporter-py-testfailing-test-element-not-found-chromium

        From nodeid: tests/test_reporter.py::TestFailing::test_element_not_found[chromium]
        """
        # Parse nodeid components
        parts = nodeid.split("::")
        file_part = parts[0] if parts else ""
        test_name = parts[-1] if parts else nodeid

        # Extract browser from parametrize brackets
        browser = "chromium"  # default
        if "[" in test_name:
            bracket_content = test_name.split("[")[1].rstrip("]")
            # Browser is usually the last part or only content
            if bracket_content in ("chromium", "firefox", "webkit"):
                browser = bracket_content
            elif "-" in bracket_content:
                # e.g., "valid-chromium" -> chromium
                last_part = bracket_content.split("-")[-1]
                if last_part in ("chromium", "firefox", "webkit"):
                    browser = last_part
            test_name = test_name.split("[")[0]

        # Build search patterns from nodeid
        # Convert: tests/test_reporter.py::TestFailing::test_element_not_found
        # To match: tests-test_reporter-py-testfailing-test-element-not-found-chromium

        # Create normalized search terms
        search_terms = []

        # Add test function name (most specific)
        search_terms.append(test_name.lower().replace("_", "-"))

        # Add class name if present
        if len(parts) >= 3:
            class_name = parts[1].lower()
            search_terms.append(class_name)

        # Look for matching directory
        if self.test_results_dir.exists():
            best_match = None
            best_score = 0

            for dir_path in self.test_results_dir.iterdir():
                if not dir_path.is_dir():
                    continue

                dir_name_lower = dir_path.name.lower()

                # Calculate match score
                score = 0
                for term in search_terms:
                    if term in dir_name_lower:
                        score += len(term)

                # Browser match is important
                if browser in dir_name_lower:
                    score += 10

                # Prefer exact test name match
                if test_name.lower().replace("_", "-") in dir_name_lower:
                    score += 20

                if score > best_score:
                    best_score = score
                    best_match = dir_path

            if best_match:
                return best_match

        # Fallback to constructed path
        return self.test_results_dir / test_name

    def _create_attachment(self, file_path: Path) -> Optional[Attachment]:
        """Create an Attachment object from a file"""
        suffix = file_path.suffix.lower()
        content_type = CONTENT_TYPES.get(suffix, "application/octet-stream")

        # Determine attachment name based on file type
        name = self._get_attachment_name(file_path)

        return Attachment(
            name=name,
            contentType=content_type,
            path=str(file_path.absolute()),
        )

    def _get_attachment_name(self, file_path: Path) -> str:
        """Get human-readable attachment name"""
        stem = file_path.stem.lower()
        suffix = file_path.suffix.lower()

        # Video
        if suffix in (".webm", ".mp4"):
            return "video"

        # Screenshot
        if suffix in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            if "failure" in stem or "failed" in stem:
                return "screenshot-on-failure"
            return "screenshot"

        # Trace
        if suffix == ".zip" and "trace" in stem:
            return "trace"

        # Default to filename
        return file_path.name

    def scan_test_results_dir(self) -> Dict[str, List[Path]]:
        """Scan the test-results directory for all attachments

        Returns mapping of test directory name -> list of attachment paths
        """
        results: Dict[str, List[Path]] = {}

        if not self.test_results_dir.exists():
            return results

        for test_dir in self.test_results_dir.iterdir():
            if not test_dir.is_dir():
                continue

            attachments = []
            for file_path in test_dir.iterdir():
                if file_path.is_file():
                    suffix = file_path.suffix.lower()
                    if suffix in CONTENT_TYPES:
                        attachments.append(file_path)

            if attachments:
                results[test_dir.name] = attachments

        return results


def collect_pytest_playwright_attachments(
    test_results_dir: str = "test-results",
    nodeid: Optional[str] = None,
) -> List[Attachment]:
    """Convenience function to collect attachments

    Args:
        test_results_dir: Path to test-results directory
        nodeid: Optional specific test nodeid to collect for

    Returns:
        List of Attachment objects
    """
    collector = AttachmentCollector(test_results_dir)

    if nodeid:
        return collector.collect_for_test(nodeid)

    # Collect all attachments
    all_attachments: List[Attachment] = []
    scan_results = collector.scan_test_results_dir()

    for _, file_paths in scan_results.items():
        for file_path in file_paths:
            attachment = collector._create_attachment(file_path)
            if attachment:
                all_attachments.append(attachment)

    return all_attachments


def match_attachments_to_test(
    nodeid: str,
    test_results_dir: str = "test-results",
    verbose: bool = False,
) -> List[Attachment]:
    """Match attachments from test-results directory to a specific test

    pytest-playwright stores attachments in directories named after tests:
    test-results/
        test-login-chromium/
            screenshot.png
            video.webm
            trace.zip

    Args:
        nodeid: pytest node ID (e.g., "tests/test_login.py::test_login")
        test_results_dir: Path to test-results directory
        verbose: Enable verbose logging

    Returns:
        List of Attachment objects for this test
    """
    collector = AttachmentCollector(test_results_dir)
    attachments = collector.collect_for_test(nodeid)

    if verbose:
        import sys
        print(f"[attachments] nodeid: {nodeid}", file=sys.stderr)
        print(f"[attachments] test_results_dir: {test_results_dir}", file=sys.stderr)
        print(f"[attachments] found: {len(attachments)} attachments", file=sys.stderr)
        for att in attachments:
            print(f"[attachments]   - {att.name}: {att.path}", file=sys.stderr)

    return attachments

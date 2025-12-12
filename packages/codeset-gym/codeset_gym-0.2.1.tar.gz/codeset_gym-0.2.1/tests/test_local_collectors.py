import os
import tempfile

import pytest

from codeset_gym.test_collectors.core_factory import CoreTestResultCollectorFactory


_MINIMAL_JUNIT = """
<testsuite name="demo" tests="1" failures="0">
  <testcase classname="Sample" name="test_ok"/>
</testsuite>
""".strip()


@pytest.mark.parametrize(
    "language, relative_path",
    [
        ("python", "report.xml"),
        ("java", os.path.join("target", "surefire-reports", "suite.xml")),
        ("javascript", os.path.join("test-results", "junit.xml")),
        ("typescript", os.path.join("test-results", "junit.xml")),
        ("go", "test-results.xml"),
        ("rust", os.path.join("target", "junit.xml")),
        ("csharp", os.path.join("TestResults", "results.xml")),
        ("c", "gtest_output.xml"),
        ("cpp", "gtest_output.xml"),
        ("c++", "gtest_output.xml"),
    ],
)
def test_core_collector_reads_local_results(language: str, relative_path: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        target_path = os.path.join(tmpdir, relative_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(_MINIMAL_JUNIT)

        collector = CoreTestResultCollectorFactory.get_collector(language)
        results = collector.get_test_results_from_path(tmpdir)

        assert results is not None
        assert len(results) > 0
        total_tests = sum(1 for _ in results)
        assert total_tests == 1



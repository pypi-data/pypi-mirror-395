import junitparser

from .core_collector import CoreTestResultCollector


class JavaScriptTestResultCollector(CoreTestResultCollector):
    """Core test result collector for JavaScript/TypeScript projects."""

    def get_test_results_from_path(self, working_dir: str) -> junitparser.JUnitXml:
        """
        Get test results from JavaScript projects, trying Jest, Mocha, then Vitest.

        Args:
            working_dir: Path to the working directory containing test results

        Returns:
            JUnitXml test suite from Jest, Mocha, or Vitest

        Raises:
            RuntimeError: If all test frameworks fail
        """
        # Try Jest first
        jest_result = self._try_single_xml_path(working_dir, "test-results/junit.xml")
        if jest_result:
            return jest_result

        # Try Mocha
        mocha_result = self._try_single_xml_path(working_dir, "test-results/test-results.xml")
        if mocha_result:
            return mocha_result

        # Try Vitest (same path as Jest but might be different content)
        vitest_result = self._try_single_xml_path(working_dir, "test-results/junit.xml")
        if vitest_result:
            return vitest_result

        raise RuntimeError(f"No Jest, Mocha, or Vitest test results found in {working_dir}")

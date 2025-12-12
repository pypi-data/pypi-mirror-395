import junitparser

from .core_collector import CoreTestResultCollector


class GoTestResultCollector(CoreTestResultCollector):
    """Core test result collector for Go projects."""

    def get_test_results_from_path(self, working_dir: str) -> junitparser.JUnitXml:
        """
        Get test results from Go projects.

        Args:
            working_dir: Path to the working directory containing test results

        Returns:
            JUnitXml test suite from Go test

        Raises:
            RuntimeError: If test results are not found
        """
        # Try standard Go test output
        go_result = self._try_single_xml_path(working_dir, "test-results.xml")
        if go_result:
            return go_result

        # Try alternative path
        go_result = self._try_single_xml_path(working_dir, "go-test-report.xml")
        if go_result:
            return go_result

        raise RuntimeError(f"No Go test results found in {working_dir}")

import junitparser

from .core_collector import CoreTestResultCollector


class CppTestResultCollector(CoreTestResultCollector):
    """Core test result collector for C++ projects."""

    def get_test_results_from_path(self, working_dir: str) -> junitparser.JUnitXml:
        """
        Get test results from C++ projects.

        Args:
            working_dir: Path to the working directory containing test results

        Returns:
            JUnitXml test suite from C++ test frameworks

        Raises:
            RuntimeError: If test results are not found
        """
        # Try Google Test output
        gtest_result = self._try_single_xml_path(working_dir, "gtest_output.xml")
        if gtest_result:
            return gtest_result

        # Try Catch2 output
        catch2_result = self._try_single_xml_path(working_dir, "test-results.xml")
        if catch2_result:
            return catch2_result

        # Try CTest output
        ctest_result = self._try_multiple_xml_pattern(working_dir, "Testing/*/Test.xml")
        if ctest_result:
            return ctest_result

        raise RuntimeError(f"No C++ test results found in {working_dir}")

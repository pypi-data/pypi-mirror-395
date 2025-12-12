import junitparser

from .core_collector import CoreTestResultCollector


class JavaTestResultCollector(CoreTestResultCollector):
    """Core test result collector for Java projects."""

    def get_test_results_from_path(self, working_dir: str) -> junitparser.JUnitXml:
        """
        Get test results from Java projects, trying Maven first, then Gradle.

        Args:
            working_dir: Path to the working directory containing test results

        Returns:
            JUnitXml test suite from either Maven or Gradle

        Raises:
            RuntimeError: If both Maven and Gradle methods fail
        """
        # Try Maven surefire reports first (specific files)
        maven_files = [
            "target/surefire-reports/suite.xml",
            "target/surefire-reports/TEST-*.xml",
            "target/surefire-reports/*.xml"
        ]
        
        for pattern in maven_files:
            if "*" in pattern:
                maven_result = self._try_multiple_xml_pattern(working_dir, pattern)
            else:
                maven_result = self._try_single_xml_path(working_dir, pattern)
            if maven_result:
                return maven_result

        # Fallback to Gradle test results
        gradle_result = self._try_multiple_xml_pattern(working_dir, "build/test-results/test/*.xml")
        if gradle_result:
            return gradle_result

        raise RuntimeError(f"No Maven or Gradle test results found in {working_dir}")

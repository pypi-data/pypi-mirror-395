import junitparser

from .core_collector import CoreTestResultCollector


class CSharpTestResultCollector(CoreTestResultCollector):
    """Core test result collector for C# projects."""

    def get_test_results_from_path(self, working_dir: str) -> junitparser.JUnitXml:
        """
        Get test results from C# projects.

        Args:
            working_dir: Path to the working directory containing test results

        Returns:
            JUnitXml test suite from .NET test

        Raises:
            RuntimeError: If test results are not found
        """
        # Try standard .NET test output (specific files first)
        dotnet_files = [
            "TestResults/results.xml",
            "TestResults/*.xml",
            "test-results.xml"
        ]
        
        for pattern in dotnet_files:
            if "*" in pattern:
                dotnet_result = self._try_multiple_xml_pattern(working_dir, pattern)
            else:
                dotnet_result = self._try_single_xml_path(working_dir, pattern)
            if dotnet_result:
                return dotnet_result

        raise RuntimeError(f"No .NET test results found in {working_dir}")

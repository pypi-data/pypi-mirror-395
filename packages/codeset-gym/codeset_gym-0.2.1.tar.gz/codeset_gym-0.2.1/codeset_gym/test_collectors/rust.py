import junitparser

from .core_collector import CoreTestResultCollector


class RustTestResultCollector(CoreTestResultCollector):
    """Core test result collector for Rust projects."""

    def get_test_results_from_path(self, working_dir: str) -> junitparser.JUnitXml:
        """
        Get test results from Rust projects.

        Args:
            working_dir: Path to the working directory containing test results

        Returns:
            JUnitXml test suite from Cargo test outputs

        Raises:
            RuntimeError: If test results are not found
        """
        # Common junit report path for cargo
        cargo_result = self._try_single_xml_path(working_dir, "target/junit.xml")
        if cargo_result:
            return cargo_result

        # Alternative commonly used path
        cargo_result = self._try_single_xml_path(working_dir, "test-results.xml")
        if cargo_result:
            return cargo_result

        raise RuntimeError(f"No Rust test results found in {working_dir}")

import os
import glob
from abc import ABC, abstractmethod
from typing import List, Optional

import junitparser


class CoreTestResultCollector(ABC):
    """Base class for container-agnostic test result collectors."""

    @abstractmethod
    def get_test_results_from_path(self, working_dir: str) -> junitparser.JUnitXml:
        """
        Get test results from a working directory path.

        Args:
            working_dir: Path to the working directory containing test results

        Returns:
            JUnitXml test suite

        Raises:
            Exception: If test results cannot be retrieved
        """
        pass

    def _find_xml_files(self, base_path: str, pattern: str) -> List[str]:
        """Find XML files matching a pattern in the base path."""
        search_pattern = os.path.join(base_path, pattern)
        return glob.glob(search_pattern, include_hidden=True, recursive=True)

    def _load_single_xml_file(self, xml_path: str) -> junitparser.JUnitXml:
        """Load a single XML file."""
        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"XML file not found: {xml_path}")
        return junitparser.JUnitXml.fromfile(xml_path)

    def _load_multiple_xml_files(self, xml_paths: List[str]) -> junitparser.JUnitXml:
        """Load and combine multiple XML files."""
        if not xml_paths:
            raise RuntimeError("No XML files found")

        combined_suite = junitparser.JUnitXml()

        for xml_path in xml_paths:
            try:
                xml_suite = junitparser.JUnitXml.fromfile(xml_path)
                combined_suite.add_testsuite(xml_suite)
            except Exception as e:
                print(f"Error loading XML file: {xml_path}")
                print(e)
                continue

        if len(combined_suite) == 0:
            raise RuntimeError("No valid XML files found")

        return combined_suite

    def _try_single_xml_path(self, working_dir: str, relative_path: str) -> Optional[junitparser.JUnitXml]:
        """Try to load a single XML file, return None if it fails."""
        try:
            xml_path = os.path.join(working_dir, relative_path)
            return self._load_single_xml_file(xml_path)
        except Exception:
            return None

    def _try_multiple_xml_pattern(self, working_dir: str, pattern: str) -> Optional[junitparser.JUnitXml]:
        """Try to load multiple XML files matching a pattern, return None if it fails."""
        try:
            xml_files = self._find_xml_files(working_dir, pattern)
            return self._load_multiple_xml_files(xml_files)
        except Exception as e:
            print(e)
            return None
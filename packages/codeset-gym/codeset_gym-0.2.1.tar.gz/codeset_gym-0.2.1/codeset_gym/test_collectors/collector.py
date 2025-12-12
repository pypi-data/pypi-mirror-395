import io
import tarfile
import tempfile
import os

import junitparser
from docker.models.containers import Container

from .core_factory import CoreTestResultCollectorFactory


class ContainerTestResultCollector:
    """Adapter that wraps core test collectors to work with Docker containers."""

    def __init__(self, language: str):
        """
        Initialize the container adapter for a specific language.

        Args:
            language: The programming language

        Raises:
            ValueError: If the language is not supported
        """
        language_lower = language.lower()
        self.language = language_lower
        # Delegate to the core factory for parser selection
        self.collector = CoreTestResultCollectorFactory.get_collector(language_lower)

    def get_test_results(self, instance_id: str, container: Container) -> junitparser.JUnitXml:
        """
        Get test results from the container by extracting files to a temporary directory.

        Args:
            instance_id: The instance ID being processed
            container: Docker container instance

        Returns:
            JUnitXml test suite

        Raises:
            Exception: If test results cannot be retrieved
        """
        repository = self._get_repository(instance_id)

        # Create a temporary directory to extract container files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the entire repository directory from the container
            try:
                archive_data, _ = container.get_archive(path=f"/{repository}")
                archive_bytes = b"".join(archive_data)

                # Extract the archive to the temporary directory
                with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as tar:
                    tar.extractall(temp_dir)

                # The extracted directory will be temp_dir/repository
                extracted_path = os.path.join(temp_dir, repository)

                # Use the core collector to parse the results
                return self.collector.get_test_results_from_path(extracted_path)

            except Exception as e:
                raise RuntimeError(f"Failed to extract and parse test results for {instance_id}: {e}")

    def _get_repository(self, instance_id: str) -> str:
        """Extract repository name from instance ID."""
        return instance_id.rsplit("-", 1)[0].split("__")[1]

    @classmethod
    def get_supported_languages(cls) -> list[str]:
        """Get list of supported languages."""
        return CoreTestResultCollectorFactory.get_supported_languages()
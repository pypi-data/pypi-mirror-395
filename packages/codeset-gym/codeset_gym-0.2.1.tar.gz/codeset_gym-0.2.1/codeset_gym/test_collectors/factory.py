from typing import Dict

from .collector import ContainerTestResultCollector


class ContainerTestResultCollectorFactory:
    """Factory for creating container test result collectors based on language."""

    _collectors: Dict[str, type] = {lang: ContainerTestResultCollector for lang in [
        "python", "java", "javascript", "typescript", "go", "rust", "csharp", "c", "cpp", "c++"
    ]}

    @classmethod
    def get_collector(cls, language: str):
        """
        Get a container test result collector for the specified language.

        Args:
            language: The programming language (e.g., 'python', 'java', 'javascript')

        Returns:
            ContainerTestResultCollector instance for the language

        Raises:
            ValueError: If the language is not supported
        """
        language_lower = language.lower()

        if language_lower not in cls._collectors:
            supported_languages = ", ".join(cls._collectors.keys())
            raise ValueError(
                f"Unsupported language: {language}. Supported languages: {supported_languages}"
            )

        collector_class = cls._collectors[language_lower]
        return collector_class(language_lower)

    @classmethod
    def get_supported_languages(cls) -> list[str]:
        """Get list of supported languages."""
        return list(cls._collectors.keys())

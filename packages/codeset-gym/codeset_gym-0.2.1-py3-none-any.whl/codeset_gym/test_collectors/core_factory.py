from typing import Dict, Type

from .core_collector import CoreTestResultCollector
from .python import PythonTestResultCollector
from .java import JavaTestResultCollector
from .javascript import JavaScriptTestResultCollector
from .go import GoTestResultCollector
from .rust import RustTestResultCollector
from .csharp import CSharpTestResultCollector
from .cpp import CppTestResultCollector


class CoreTestResultCollectorFactory:
    """Factory for creating container-agnostic test result collectors."""

    _collectors: Dict[str, Type[CoreTestResultCollector]] = {
        "python": PythonTestResultCollector,
        "java": JavaTestResultCollector,
        "javascript": JavaScriptTestResultCollector,
        "typescript": JavaScriptTestResultCollector,
        "go": GoTestResultCollector,
        "rust": RustTestResultCollector,
        "csharp": CSharpTestResultCollector,
        "c": CppTestResultCollector,
        "cpp": CppTestResultCollector,
        "c++": CppTestResultCollector,
    }

    @classmethod
    def get_collector(cls, language: str) -> CoreTestResultCollector:
        """
        Get a core test result collector for the specified language.

        Args:
            language: The programming language (e.g., 'python', 'java', 'javascript')

        Returns:
            CoreTestResultCollector instance for the language

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
        return collector_class()

    @classmethod
    def get_supported_languages(cls) -> list[str]:
        """Get list of supported languages."""
        return list(cls._collectors.keys())
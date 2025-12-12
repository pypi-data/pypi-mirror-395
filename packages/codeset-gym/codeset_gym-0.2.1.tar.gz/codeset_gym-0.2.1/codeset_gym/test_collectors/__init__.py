"""Test result collectors for different programming languages."""

# Container-based collectors (backward compatibility)
from .factory import ContainerTestResultCollectorFactory

# Core collectors (container-agnostic)
from .core_factory import CoreTestResultCollectorFactory
from .core_collector import CoreTestResultCollector

# Container adapter
from .collector import ContainerTestResultCollector

__all__ = [
    # Backward compatibility - container-based
    "ContainerTestResultCollectorFactory",

    # Core - container-agnostic
    "CoreTestResultCollectorFactory",
    "CoreTestResultCollector",

    # Container adapter
    "ContainerTestResultCollector",
]
"""
Standardized interface for transformation passes.

All passes (built-in and custom) implement this interface.
Enables custom pass registration and dependency resolution.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Set

from . import ManifestIR
from .transforms import PassMetadata


class Transform(ABC):
    """
    Base class for transformation passes.

    All passes (built-in and custom) implement this interface.
    """

    @property
    @abstractmethod
    def metadata(self) -> PassMetadata:
        """
        Pass metadata for dependency resolution.

        Returns:
            PassMetadata with name, description, dependencies, etc.
        """
        pass

    @property
    def name(self) -> str:
        """Convenience property to get pass name from metadata."""
        return self.metadata.name

    @abstractmethod
    def apply(self, ir: ManifestIR) -> ManifestIR:
        """
        Apply transformation.

        Args:
            ir: Input ManifestIR

        Returns:
            Transformed ManifestIR
        """
        pass


class ValidationPass(Transform):
    """
    Base class for validation-only passes (don't modify IR).

    Validation passes check IR correctness and raise errors if invalid.
    """

    @abstractmethod
    def validate(self, ir: ManifestIR) -> list[str]:
        """
        Validate IR.

        Args:
            ir: ManifestIR to validate

        Returns:
            List of error messages (empty if valid)
        """
        pass

    def apply(self, ir: ManifestIR) -> ManifestIR:
        """
        Validation passes don't modify IR, only check validity.

        Args:
            ir: ManifestIR to validate

        Returns:
            Unchanged ManifestIR

        Raises:
            RuntimeError: If validation fails
        """
        errors = self.validate(ir)
        if errors:
            error_msg = "; ".join(errors)
            raise RuntimeError(f"Validation failed: {error_msg}")
        return ir


class OptimizationPass(Transform):
    """
    Base class for optimization passes.

    Optimization passes modify IR to improve performance, reduce size, etc.
    """

    pass


class InstrumentationPass(Transform):
    """
    Base class for instrumentation passes (add metadata/observability).

    Instrumentation passes add metadata, tracing, or observability hooks
    without changing the semantic behavior of the IR.
    """

    pass


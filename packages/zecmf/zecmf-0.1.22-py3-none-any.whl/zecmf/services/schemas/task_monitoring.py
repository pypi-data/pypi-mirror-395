"""Task monitoring service schemas for internal data structures."""

from dataclasses import dataclass
from typing import Any


@dataclass
class ExceptionContext:
    """Typed structure for exception context information."""

    exception_type: str | None = None
    exception_message: str | None = None
    traceback: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {}
        if self.exception_type is not None:
            result["exception_type"] = self.exception_type
        if self.exception_message is not None:
            result["exception_message"] = self.exception_message
        if self.traceback is not None:
            result["traceback"] = self.traceback
        return result

    def is_empty(self) -> bool:
        """Check if the exception context is empty."""
        return (
            self.exception_type is None
            and self.exception_message is None
            and self.traceback is None
        )


@dataclass
class TaskContext:
    """Typed structure for task context information."""

    context_id: str | None = None
    context_step: str | None = None
    additional_data: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {}
        if self.context_id is not None:
            result["context_id"] = self.context_id
        if self.context_step is not None:
            result["context_step"] = self.context_step
        if self.additional_data is not None:
            result.update(self.additional_data)
        return result

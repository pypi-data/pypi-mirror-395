"""Task monitoring API request and response schemas."""

from dataclasses import dataclass
from typing import Any


@dataclass
class TaskExecutionQueryParams:
    """Query parameters for task execution endpoints."""

    status: str | None = None
    task_name: str | None = None
    page: int = 1
    per_page: int = 50

    def __post_init__(self) -> None:
        """Validate and normalize parameters."""
        # Ensure per_page doesn't exceed maximum
        self.per_page = min(self.per_page, 100)
        # Ensure page is at least 1
        self.page = max(self.page, 1)


@dataclass
class TaskLogQueryParams:
    """Query parameters for task log endpoints."""

    level: str | None = None
    page: int = 1
    per_page: int = 100

    def __post_init__(self) -> None:
        """Validate and normalize parameters."""
        # Ensure per_page doesn't exceed maximum
        self.per_page = min(self.per_page, 500)
        # Ensure page is at least 1
        self.page = max(self.page, 1)


@dataclass
class TaskExecutionResponse:
    """Response schema for task execution data."""

    id: int
    task_id: str
    task_name: str
    status: str
    started_at: str | None
    completed_at: str | None
    duration_seconds: float | None
    retry_count: int | None
    args: str | None
    kwargs: str | None
    result: str | None
    error_message: str | None
    worker_name: str | None
    created_at: str
    updated_at: str
    log_count: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "task_name": self.task_name,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_seconds": self.duration_seconds,
            "retry_count": self.retry_count,
            "args": self.args,
            "kwargs": self.kwargs,
            "result": self.result,
            "error_message": self.error_message,
            "worker_name": self.worker_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "log_count": self.log_count,
        }


@dataclass
class TaskLogResponse:
    """Response schema for task log data."""

    id: int
    task_execution_id: int
    level: str
    message: str
    timestamp: str
    context: str | None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "task_execution_id": self.task_execution_id,
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp,
            "context": self.context,
        }


@dataclass
class TaskStatsResponse:
    """Response schema for task execution statistics."""

    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    pending_tasks: int
    running_tasks: int
    average_duration_seconds: float | None
    last_24h_tasks: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "pending_tasks": self.pending_tasks,
            "running_tasks": self.running_tasks,
            "average_duration_seconds": self.average_duration_seconds,
            "last_24h_tasks": self.last_24h_tasks,
        }

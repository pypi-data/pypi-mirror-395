"""
Structured JSON logging for NudgeOps.

Provides CloudWatch/Datadog-friendly log output for monitoring
loop detection events and interventions.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from nudgeops.core.state import DetectionResult


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "event_data"):
            log_entry.update(record.event_data)

        return json.dumps(log_entry)


class GuardLogger:
    """
    Structured logger for NudgeOps events.

    Outputs JSON-formatted logs suitable for CloudWatch, Datadog,
    or other log aggregation services.

    Log structure:
    {
        "timestamp": "2024-01-15T10:30:00.000Z",
        "service": "NudgeOps",
        "event_type": "TRAJECTORY_NUDGE",
        "thread_id": "abc123",
        "step_id": "def456",
        "metrics": {
            "loop_score": 2.5,
            "detections": [...]
        },
        "intervention": "NUDGE"
    }
    """

    def __init__(self, name: str = "nudgeops") -> None:
        """
        Initialize the guard logger.

        Args:
            name: Logger name (default: "nudgeops")
        """
        self.logger = logging.getLogger(name)
        self._configured = False

    def configure(
        self,
        level: int = logging.INFO,
        json_format: bool = True,
    ) -> None:
        """
        Configure the logger.

        Args:
            level: Logging level
            json_format: Whether to use JSON formatting
        """
        if self._configured:
            return

        handler = logging.StreamHandler()
        handler.setLevel(level)

        if json_format:
            handler.setFormatter(JsonFormatter())
        else:
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )

        self.logger.addHandler(handler)
        self.logger.setLevel(level)
        self._configured = True

    def log_event(
        self,
        event_type: str,
        loop_score: float,
        detections: list[DetectionResult],
        step_id: str,
        thread_id: str,
        intervention: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """
        Log a trajectory guard event.

        Args:
            event_type: Event type (OBSERVE, NUDGE, STOP)
            loop_score: Current loop score
            detections: Detection results
            step_id: Current step ID
            thread_id: Session/thread ID
            intervention: Intervention taken
            extra: Additional fields to include
        """
        event_data = {
            "service": "NudgeOps",
            "event_type": f"TRAJECTORY_{event_type}",
            "thread_id": thread_id,
            "step_id": step_id,
            "metrics": {
                "loop_score": round(loop_score, 3),
                "detections": [
                    {
                        "type": d["loop_type"],
                        "detected": d["detected"],
                        "confidence": round(d["confidence"], 3),
                    }
                    for d in detections
                ],
            },
            "intervention": intervention,
        }

        if extra:
            event_data.update(extra)

        # Create log record with extra data
        record = self.logger.makeRecord(
            self.logger.name,
            logging.INFO if event_type == "OBSERVE" else logging.WARNING,
            "",
            0,
            f"{event_type} - score: {loop_score:.2f}",
            (),
            None,
        )
        record.event_data = event_data

        self.logger.handle(record)


# Global logger instance
_guard_logger: GuardLogger | None = None


def get_logger() -> GuardLogger:
    """Get the global guard logger instance."""
    global _guard_logger
    if _guard_logger is None:
        _guard_logger = GuardLogger()
    return _guard_logger


def configure_logging(
    level: int = logging.INFO,
    json_format: bool = True,
) -> None:
    """
    Configure NudgeOps logging.

    Args:
        level: Logging level
        json_format: Whether to use JSON formatting
    """
    logger = get_logger()
    logger.configure(level=level, json_format=json_format)


def log_event(
    event_type: str,
    loop_score: float,
    detections: list[DetectionResult],
    step_id: str = "",
    thread_id: str = "",
    intervention: str = "",
    extra: dict[str, Any] | None = None,
) -> None:
    """
    Log a trajectory guard event.

    Convenience function that uses the global logger.

    Args:
        event_type: Event type (OBSERVE, NUDGE, STOP)
        loop_score: Current loop score
        detections: Detection results
        step_id: Current step ID
        thread_id: Session/thread ID
        intervention: Intervention taken
        extra: Additional fields to include
    """
    logger = get_logger()
    logger.log_event(
        event_type=event_type,
        loop_score=loop_score,
        detections=detections,
        step_id=step_id,
        thread_id=thread_id,
        intervention=intervention,
        extra=extra,
    )

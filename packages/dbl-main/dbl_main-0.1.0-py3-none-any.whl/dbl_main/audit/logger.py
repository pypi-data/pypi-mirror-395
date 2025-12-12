# logger.py
#
# Audit logging for DBL Main.

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Optional

from dbl_core import BoundaryResult


class AuditLogger:
    """
    Audit logger for boundary evaluation results.
    """
    
    def __init__(
        self,
        writer: Optional[Callable[[Mapping[str, Any]], None]] = None,
    ) -> None:
        self._writer = writer or self._default_writer
        self._records: list[Mapping[str, Any]] = []
    
    def _default_writer(self, record: Mapping[str, Any]) -> None:
        """Default in-memory writer."""
        self._records.append(record)
    
    def log(self, result: BoundaryResult, extra: Optional[Mapping[str, Any]] = None) -> None:
        """Log a boundary evaluation result."""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.describe(),
        }
        if extra:
            record["extra"] = dict(extra)
        
        self._writer(record)
    
    def get_records(self) -> list[Mapping[str, Any]]:
        """Get all logged records (for in-memory writer)."""
        return list(self._records)
    
    def clear(self) -> None:
        """Clear all logged records."""
        self._records.clear()


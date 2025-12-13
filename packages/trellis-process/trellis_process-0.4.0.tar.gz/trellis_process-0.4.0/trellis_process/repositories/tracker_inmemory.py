# trellis_process/repositories/tracker_inmemory.py

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Iterable, Optional, Tuple

from ..tracker import StepTracker
from .tracker_base import StepTrackerRepository


class InMemoryStepTrackerRepository(StepTrackerRepository):
    """In-memory implementation for tests and demos."""

    def __init__(self) -> None:
        self._trackers: Dict[Tuple[str, str, str], StepTracker] = {}

    def add(self, tracker: StepTracker) -> None:
        key = (tracker.tenant_id, tracker.process_id, tracker.step_name)
        if key in self._trackers:
            raise ValueError(f"Tracker already exists: {key}")
        self._trackers[key] = tracker

    def save(self, tracker: StepTracker) -> None:
        key = (tracker.tenant_id, tracker.process_id, tracker.step_name)
        self._trackers[key] = tracker

    def get(self, tenant_id: str, process_id: str, step_name: str) -> Optional[StepTracker]:
        return self._trackers.get((tenant_id, process_id, step_name))

    def all_timed_out(self) -> Iterable[StepTracker]:
        now = datetime.now(timezone.utc)
        return [
            t for t in self._trackers.values()
            if t.has_timed_out(now) and not t.completed and not t.process_informed_of_timeout
        ]

    def all_timed_out_for_tenant(self, tenant_id: str) -> Iterable[StepTracker]:
        now = datetime.now(timezone.utc)
        return [
            t for t in self._trackers.values()
            if t.tenant_id == tenant_id
            and t.has_timed_out(now)
            and not t.completed
            and not t.process_informed_of_timeout
        ]

    def delete(self, tenant_id: str, process_id: str, step_name: str) -> None:
        key = (tenant_id, process_id, step_name)
        self._trackers.pop(key, None)

# trellis_process/repositories/tracker_base.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from ..tracker import StepTracker


class StepTrackerRepository(ABC):
    """Repository interface for step trackers."""

    @abstractmethod
    def add(self, tracker: StepTracker) -> None:
        ...

    @abstractmethod
    def save(self, tracker: StepTracker) -> None:
        ...

    @abstractmethod
    def get(self, tenant_id: str, process_id: str, step_name: str) -> Optional[StepTracker]:
        ...

    @abstractmethod
    def all_timed_out(self) -> Iterable[StepTracker]:
        """Return all trackers that have timed out and not yet completed."""
        ...

    @abstractmethod
    def all_timed_out_for_tenant(self, tenant_id: str) -> Iterable[StepTracker]:
        ...

    @abstractmethod
    def delete(self, tenant_id: str, process_id: str, step_name: str) -> None:
        ...

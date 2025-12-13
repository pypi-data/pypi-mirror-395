# trellis_process/tracker.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional


@dataclass(frozen=True)
class ProcessStepTimedOut:
    """Published when a step times out."""
    tenant_id: str
    process_id: str
    step_name: str
    retry_count: int
    retries_permitted: int
    _occurred_on: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def has_fully_timed_out(self) -> bool:
        return self.retry_count >= self.retries_permitted

    def allows_retries(self) -> bool:
        return self.retries_permitted > 0

    def occurred_on(self) -> datetime:
        return self._occurred_on


EventPublisher = Callable[[ProcessStepTimedOut], None]


@dataclass
class StepTracker:
    """
    Time-constrained tracker for a single process step.
    
    Based on Vaughn Vernon's TimeConstrainedProcessTracker pattern,
    scoped to individual steps for fine-grained timeout control.
    """
    tenant_id: str
    process_id: str
    step_name: str
    timeout_ms: int
    retries_permitted: int
    
    # State
    retry_count: int = 0
    timeout_occurs_on: Optional[datetime] = None
    completed: bool = False
    process_informed_of_timeout: bool = False

    def start(self) -> None:
        """Start the timeout clock."""
        now = datetime.now(timezone.utc)
        self.timeout_occurs_on = datetime.fromtimestamp(
            now.timestamp() + (self.timeout_ms / 1000),
            tz=timezone.utc
        )

    def has_timed_out(self, now: Optional[datetime] = None) -> bool:
        if self.timeout_occurs_on is None:
            return False
        if now is None:
            now = datetime.now(timezone.utc)
        return now >= self.timeout_occurs_on

    def inform_process_timed_out(self, publish: EventPublisher) -> None:
        """Emit timeout event with retry semantics."""
        if self.completed or self.process_informed_of_timeout or not self.has_timed_out():
            return

        self.retry_count += 1
        
        event = ProcessStepTimedOut(
            tenant_id=self.tenant_id,
            process_id=self.process_id,
            step_name=self.step_name,
            retry_count=self.retry_count,
            retries_permitted=self.retries_permitted,
        )
        
        if self.retry_count >= self.retries_permitted:
            self.process_informed_of_timeout = True
        else:
            # Reschedule next timeout
            self.timeout_occurs_on = datetime.fromtimestamp(
                self.timeout_occurs_on.timestamp() + (self.timeout_ms / 1000),
                tz=timezone.utc
            )
        
        publish(event)

    def mark_completed(self) -> None:
        self.completed = True

    @property
    def is_completed(self) -> bool:
        return self.completed

    @property
    def tracker_key(self) -> str:
        """Unique key for this tracker."""
        return f"{self.process_id}#{self.step_name}"

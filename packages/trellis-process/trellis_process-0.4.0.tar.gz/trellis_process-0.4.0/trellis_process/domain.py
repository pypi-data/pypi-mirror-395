# trellis_process/domain.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, List, Literal, Optional
from uuid import uuid4

if TYPE_CHECKING:
    from .tracker import StepTracker

ProcessState = Literal["pending", "in_progress", "completed", "failed"]
StepState = Literal["pending", "in_progress", "completed", "failed"]


@dataclass
class ProcessStep:
    name: str
    state: StepState = "pending"
    
    # Timeout configuration (optional per step)
    timeout_ms: int = 0  # 0 = no timeout
    retries_permitted: int = 0
    
    # Tracking
    retry_count: int = 0
    last_error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def has_timeout(self) -> bool:
        return self.timeout_ms > 0

    def can_retry(self) -> bool:
        return self.retry_count < self.retries_permitted

    def increment_retry(self) -> None:
        self.retry_count += 1

    def mark_in_progress(self) -> None:
        if self.state not in ("pending", "failed"):
            return
        self.state = "in_progress"
        if self.started_at is None:
            self.started_at = datetime.now(timezone.utc)

    def mark_completed(self) -> None:
        self.state = "completed"
        self.completed_at = datetime.now(timezone.utc)
        self.last_error = None

    def mark_failed(self, error: str) -> None:
        self.state = "failed"
        self.last_error = error

    def create_tracker(self, tenant_id: str, process_id: str) -> "StepTracker":
        """Factory method to create a tracker for this step."""
        from .tracker import StepTracker
        return StepTracker(
            tenant_id=tenant_id,
            process_id=process_id,
            step_name=self.name,
            timeout_ms=self.timeout_ms,
            retries_permitted=self.retries_permitted,
        )


@dataclass
class Process:
    id: str
    tenant_id: str
    process_type: str
    aggregate_type: str
    aggregate_id: str
    required_steps: List[str]
    state: ProcessState = "pending"
    steps: Dict[str, ProcessStep] = field(default_factory=dict)
    metadata: Dict[str, object] = field(default_factory=dict)
    version: int = 0

    def __post_init__(self) -> None:
        for step_name in self.required_steps:
            if step_name not in self.steps:
                self.steps[step_name] = ProcessStep(name=step_name)
        self._sync_state()

    @classmethod
    def start(
        cls,
        tenant_id: str,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
        steps: List[ProcessStep],
        metadata: Optional[Dict[str, object]] = None,
    ) -> "Process":
        return cls(
            id=str(uuid4()),
            tenant_id=tenant_id,
            process_type=process_type,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            required_steps=[s.name for s in steps],
            steps={s.name: s for s in steps},
            metadata=metadata or {},
        )

    # --- Step operations ---

    def start_step(self, step_name: str) -> Optional["StepTracker"]:
        """Mark step in progress and return its tracker if timeout enabled."""
        step = self._get_step(step_name)
        step.mark_in_progress()
        self._sync_state()
        
        if step.has_timeout():
            tracker = step.create_tracker(self.tenant_id, self.id)
            tracker.start()
            return tracker
        return None

    def complete_step(self, step_name: str) -> None:
        step = self._get_step(step_name)
        step.mark_completed()
        self._sync_state()

    def fail_step(self, step_name: str, error: str) -> None:
        step = self._get_step(step_name)
        step.mark_failed(error)
        self._sync_state()

    def increment_step_retry(self, step_name: str) -> None:
        step = self._get_step(step_name)
        step.increment_retry()

    # --- Convenience methods ---

    def mark_step_in_progress(self, step_name: str) -> None:
        """Legacy method - use start_step() for timeout support."""
        step = self._get_step(step_name)
        step.mark_in_progress()
        self._sync_state()

    def mark_step_completed(self, step_name: str) -> None:
        """Legacy method - use complete_step()."""
        self.complete_step(step_name)

    def mark_step_failed(self, step_name: str, error: str) -> None:
        """Legacy method - use fail_step()."""
        self.fail_step(step_name, error)

    def create_step_trackers(self) -> List["StepTracker"]:
        """Create trackers for all steps that have timeout configured."""
        return [
            step.create_tracker(self.tenant_id, self.id)
            for step in self.steps.values()
            if step.has_timeout()
        ]

    def is_completed(self) -> bool:
        return self.state == "completed"

    def has_failed(self) -> bool:
        return self.state == "failed"

    # --- Internals ---

    def _get_step(self, step_name: str) -> ProcessStep:
        if step_name not in self.steps:
            raise ValueError(f"Unknown step '{step_name}' for process {self.id}")
        return self.steps[step_name]

    def _sync_state(self) -> None:
        states = [s.state for s in self.steps.values()]
        if all(s == "completed" for s in states):
            self.state = "completed"
        elif any(s == "failed" for s in states):
            self.state = "failed"
        elif any(s in ("in_progress", "completed") for s in states):
            self.state = "in_progress"
        else:
            self.state = "pending"

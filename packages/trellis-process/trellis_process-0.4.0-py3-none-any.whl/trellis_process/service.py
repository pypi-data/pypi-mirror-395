# trellis_process/service.py

from __future__ import annotations

from typing import Dict, List, Optional

from .domain import Process, ProcessStep
from .tracker import StepTracker
from .repositories.base import ProcessRepository
from .repositories.tracker_base import StepTrackerRepository


class ProcessService:
    """
    High-level API for creating and updating processes with optional timeout tracking.
    """

    def __init__(
        self,
        process_repository: ProcessRepository,
        tracker_repository: Optional[StepTrackerRepository] = None,
    ) -> None:
        self._process_repo = process_repository
        self._tracker_repo = tracker_repository

    # --- creation ---

    def start_process(
        self,
        tenant_id: str,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
        steps: List[ProcessStep],
        metadata: Optional[Dict[str, object]] = None,
        auto_start_steps: bool = False,
    ) -> Process:
        """
        Create and persist a new process.
        
        If auto_start_steps=True and tracker_repository is configured,
        all steps will be started and their trackers created.
        """
        process = Process.start(
            tenant_id=tenant_id,
            process_type=process_type,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            steps=steps,
            metadata=metadata,
        )
        self._process_repo.add(process)

        if auto_start_steps:
            for step_name in process.steps:
                self.start_step(process, step_name)

        return process

    def get_process(
        self,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
    ) -> Optional[Process]:
        return self._process_repo.get_by_aggregate(
            process_type=process_type,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
        )

    def get_process_by_id(self, process_id: str) -> Optional[Process]:
        return self._process_repo.get_by_id(process_id)

    # --- step operations with tracker support ---

    def start_step(self, process: Process, step_name: str) -> Optional[StepTracker]:
        """
        Start a step and create its tracker if timeout is configured.
        
        Returns the tracker if one was created, None otherwise.
        """
        tracker = process.start_step(step_name)
        self._process_repo.save(process)

        if tracker and self._tracker_repo:
            self._tracker_repo.add(tracker)

        return tracker

    def complete_step(self, process: Process, step_name: str) -> None:
        """Complete a step and mark its tracker as completed."""
        process.complete_step(step_name)
        self._process_repo.save(process)

        if self._tracker_repo:
            tracker = self._tracker_repo.get(process.tenant_id, process.id, step_name)
            if tracker:
                tracker.mark_completed()
                self._tracker_repo.save(tracker)

    def fail_step(self, process: Process, step_name: str, error: str) -> None:
        """Fail a step and mark its tracker as completed."""
        process.fail_step(step_name, error)
        self._process_repo.save(process)

        if self._tracker_repo:
            tracker = self._tracker_repo.get(process.tenant_id, process.id, step_name)
            if tracker:
                tracker.mark_completed()
                self._tracker_repo.save(tracker)

    def increment_step_retry(self, process: Process, step_name: str) -> None:
        """Increment retry count on a step (called during retry handling)."""
        process.increment_step_retry(step_name)
        self._process_repo.save(process)

    # --- legacy methods for backward compatibility ---

    def mark_step_in_progress(
        self,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
        step_name: str,
    ) -> Process:
        process = self._require_process(process_type, aggregate_type, aggregate_id)
        process.mark_step_in_progress(step_name)
        self._process_repo.save(process)
        return process

    def mark_step_completed(
        self,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
        step_name: str,
    ) -> Process:
        process = self._require_process(process_type, aggregate_type, aggregate_id)
        process.mark_step_completed(step_name)
        self._process_repo.save(process)
        return process

    def mark_step_failed(
        self,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
        step_name: str,
        error: str,
    ) -> Process:
        process = self._require_process(process_type, aggregate_type, aggregate_id)
        process.mark_step_failed(step_name, error)
        self._process_repo.save(process)
        return process

    # --- internals ---

    def _require_process(
        self,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
    ) -> Process:
        process = self.get_process(process_type, aggregate_type, aggregate_id)
        if process is None:
            raise KeyError(
                f"Process not found for "
                f"type={process_type}, aggregate={aggregate_type}, id={aggregate_id}"
            )
        return process

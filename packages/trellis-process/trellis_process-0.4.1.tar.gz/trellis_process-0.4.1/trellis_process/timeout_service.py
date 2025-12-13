# trellis_process/timeout_service.py

from __future__ import annotations

from typing import Callable, Optional

from .tracker import ProcessStepTimedOut, StepTracker
from .repositories.tracker_base import StepTrackerRepository


EventPublisher = Callable[[ProcessStepTimedOut], None]


class TimeoutCheckerService:
    """
    Scans for timed-out step trackers and publishes events.
    
    Run this on a schedule (e.g., every 30 seconds via cron, 
    CloudWatch Events, or a background thread).
    
    Based on Vaughn Vernon's ProcessApplicationService pattern.
    """

    def __init__(
        self,
        tracker_repository: StepTrackerRepository,
        publish_event: EventPublisher,
        tenant_id: Optional[str] = None,
    ) -> None:
        self._tracker_repo = tracker_repository
        self._publish = publish_event
        self._tenant_id = tenant_id

    def check_for_timed_out_steps(self) -> int:
        """
        Check for timed-out steps and publish events.
        
        Returns the number of timeout events published.
        """
        if self._tenant_id:
            trackers = self._tracker_repo.all_timed_out_for_tenant(self._tenant_id)
        else:
            trackers = self._tracker_repo.all_timed_out()

        count = 0
        for tracker in trackers:
            tracker.inform_process_timed_out(self._publish)
            self._tracker_repo.save(tracker)
            count += 1

        return count

# trellis_process/repositories/tracker_dynamodb.py

"""
DynamoDB implementation of StepTrackerRepository.

Expected table schema:
  PK: tenant_id (String)
  SK: tracker_key (String) = "{process_id}#{step_name}"

GSI (default name: "timeout-index"):
  PK: tenant_id (String)
  SK: timeout_occurs_on_ms (Number)
  
  Filter on: completed = false AND process_informed_of_timeout = false
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from ..tracker import StepTracker
from .tracker_base import StepTrackerRepository


class DynamoDBStepTrackerRepository(StepTrackerRepository):
    def __init__(self, table: Any, timeout_index_name: str = "timeout-index") -> None:
        self._table = table
        self._timeout_index = timeout_index_name

    def add(self, tracker: StepTracker) -> None:
        item = self._serialize(tracker)
        self._table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(tenant_id) AND attribute_not_exists(tracker_key)"
        )

    def save(self, tracker: StepTracker) -> None:
        item = self._serialize(tracker)
        self._table.put_item(Item=item)

    def get(self, tenant_id: str, process_id: str, step_name: str) -> Optional[StepTracker]:
        tracker_key = f"{process_id}#{step_name}"
        resp = self._table.get_item(Key={"tenant_id": tenant_id, "tracker_key": tracker_key})
        item = resp.get("Item")
        return self._deserialize(item) if item else None

    def all_timed_out(self) -> Iterable[StepTracker]:
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        
        # Scan with filter - for production, consider per-tenant queries
        resp = self._table.scan(
            FilterExpression="timeout_occurs_on_ms <= :now AND completed = :false AND process_informed_of_timeout = :false",
            ExpressionAttributeValues={
                ":now": now_ms,
                ":false": False,
            }
        )
        return [self._deserialize(item) for item in resp.get("Items", [])]

    def all_timed_out_for_tenant(self, tenant_id: str) -> Iterable[StepTracker]:
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        
        resp = self._table.query(
            IndexName=self._timeout_index,
            KeyConditionExpression="tenant_id = :tid AND timeout_occurs_on_ms <= :now",
            FilterExpression="completed = :false AND process_informed_of_timeout = :false",
            ExpressionAttributeValues={
                ":tid": tenant_id,
                ":now": now_ms,
                ":false": False,
            }
        )
        return [self._deserialize(item) for item in resp.get("Items", [])]

    def delete(self, tenant_id: str, process_id: str, step_name: str) -> None:
        tracker_key = f"{process_id}#{step_name}"
        self._table.delete_item(Key={"tenant_id": tenant_id, "tracker_key": tracker_key})

    def _serialize(self, tracker: StepTracker) -> Dict[str, Any]:
        return {
            "tenant_id": tracker.tenant_id,
            "tracker_key": f"{tracker.process_id}#{tracker.step_name}",
            "process_id": tracker.process_id,
            "step_name": tracker.step_name,
            "timeout_ms": tracker.timeout_ms,
            "retries_permitted": tracker.retries_permitted,
            "retry_count": tracker.retry_count,
            "timeout_occurs_on_ms": int(tracker.timeout_occurs_on.timestamp() * 1000) if tracker.timeout_occurs_on else 0,
            "completed": tracker.completed,
            "process_informed_of_timeout": tracker.process_informed_of_timeout,
        }

    def _deserialize(self, item: Dict[str, Any]) -> StepTracker:
        timeout_ms_val = item.get("timeout_occurs_on_ms", 0)
        timeout_occurs_on = (
            datetime.fromtimestamp(timeout_ms_val / 1000, tz=timezone.utc)
            if timeout_ms_val > 0 else None
        )
        
        return StepTracker(
            tenant_id=item["tenant_id"],
            process_id=item["process_id"],
            step_name=item["step_name"],
            timeout_ms=item["timeout_ms"],
            retries_permitted=item["retries_permitted"],
            retry_count=item.get("retry_count", 0),
            timeout_occurs_on=timeout_occurs_on,
            completed=item.get("completed", False),
            process_informed_of_timeout=item.get("process_informed_of_timeout", False),
        )

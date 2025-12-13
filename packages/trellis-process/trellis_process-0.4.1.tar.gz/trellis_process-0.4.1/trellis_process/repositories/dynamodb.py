"""
DynamoDB implementation of ProcessRepository.

Expected table schema:
  PK: id (String)

GSI (default name: "aggregate-index"):
  PK: aggregate_key (String) = "{process_type}#{aggregate_type}#{aggregate_id}"
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .base import ProcessRepository
from ..domain import Process, ProcessStep


class DynamoDBProcessRepository(ProcessRepository):
    def __init__(self, table: Any, index_name: str = "aggregate-index") -> None:
        self._table = table
        self._index_name = index_name

    def add(self, process: Process) -> None:
        item = self._serialize(process)
        self._table.put_item(Item=item, ConditionExpression="attribute_not_exists(id)")

    def save(self, process: Process) -> None:
        item = self._serialize(process)
        self._table.put_item(Item=item)

    def get_by_id(self, process_id: str) -> Optional[Process]:
        resp = self._table.get_item(Key={"id": process_id})
        item = resp.get("Item")
        return self._deserialize(item) if item else None

    def get_by_aggregate(
        self,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
    ) -> Optional[Process]:
        key = f"{process_type}#{aggregate_type}#{aggregate_id}"
        resp = self._table.query(
            IndexName=self._index_name,
            KeyConditionExpression="aggregate_key = :ak",
            ExpressionAttributeValues={":ak": key},
            Limit=1,
        )
        items = resp.get("Items", [])
        return self._deserialize(items[0]) if items else None

    def _serialize(self, process: Process) -> Dict[str, Any]:
        return {
            "id": process.id,
            "tenant_id": process.tenant_id,
            "process_type": process.process_type,
            "aggregate_type": process.aggregate_type,
            "aggregate_id": process.aggregate_id,
            "aggregate_key": f"{process.process_type}#{process.aggregate_type}#{process.aggregate_id}",
            "required_steps": process.required_steps,
            "state": process.state,
            "steps": {name: self._serialize_step(s) for name, s in process.steps.items()},
            "metadata": process.metadata,
            "version": process.version,
        }

    def _serialize_step(self, step: ProcessStep) -> Dict[str, Any]:
        return {
            "name": step.name,
            "state": step.state,
            "timeout_ms": step.timeout_ms,
            "retries_permitted": step.retries_permitted,
            "retry_count": step.retry_count,
            "last_error": step.last_error,
            "started_at": step.started_at.isoformat() if step.started_at else None,
            "completed_at": step.completed_at.isoformat() if step.completed_at else None,
        }

    def _deserialize(self, item: Dict[str, Any]) -> Process:
        steps = {name: self._deserialize_step(s) for name, s in item["steps"].items()}
        return Process(
            id=item["id"],
            tenant_id=item.get("tenant_id", ""),
            process_type=item["process_type"],
            aggregate_type=item["aggregate_type"],
            aggregate_id=item["aggregate_id"],
            required_steps=item["required_steps"],
            state=item["state"],
            steps=steps,
            metadata=item.get("metadata", {}),
            version=item.get("version", 0),
        )

    def _deserialize_step(self, data: Dict[str, Any]) -> ProcessStep:
        return ProcessStep(
            name=data["name"],
            state=data["state"],
            timeout_ms=data.get("timeout_ms", 0),
            retries_permitted=data.get("retries_permitted", 0),
            retry_count=data.get("retry_count", 0),
            last_error=data.get("last_error"),
            started_at=self._parse_dt(data.get("started_at")),
            completed_at=self._parse_dt(data.get("completed_at")),
        )

    def _parse_dt(self, val: Optional[str]) -> Optional[datetime]:
        if not val:
            return None
        return datetime.fromisoformat(val)

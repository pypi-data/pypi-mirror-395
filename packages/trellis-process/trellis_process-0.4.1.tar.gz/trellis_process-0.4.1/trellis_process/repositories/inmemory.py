# trellis/repositories/inmemory.py

from __future__ import annotations

from typing import Dict, Optional, Tuple

from ..domain import Process
from .base import ProcessRepository


class InMemoryProcessRepository(ProcessRepository):
    """
    Simple in-memory implementation for demos and unit tests.
    Not safe for concurrent production use.
    """

    def __init__(self) -> None:
        self._by_id: Dict[str, Process] = {}
        self._by_key: Dict[Tuple[str, str, str], str] = {}

    def add(self, process: Process) -> None:
        if process.id in self._by_id:
            raise ValueError(f"Process with id {process.id} already exists")
        self._by_id[process.id] = process
        key = (process.process_type, process.aggregate_type, process.aggregate_id)
        self._by_key[key] = process.id

    def save(self, process: Process) -> None:
        if process.id not in self._by_id:
            # Depending on preference, you could auto-add here
            raise KeyError(f"Process with id {process.id} not found")
        self._by_id[process.id] = process

    def get_by_id(self, process_id: str) -> Optional[Process]:
        return self._by_id.get(process_id)

    def get_by_aggregate(
        self,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
    ) -> Optional[Process]:
        key = (process_type, aggregate_type, aggregate_id)
        process_id = self._by_key.get(key)
        if not process_id:
            return None
        return self._by_id.get(process_id)

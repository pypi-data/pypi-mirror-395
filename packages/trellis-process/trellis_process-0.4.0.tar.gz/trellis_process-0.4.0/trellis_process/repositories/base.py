# trellis/repositories/base.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from ..domain import Process


class ProcessRepository(ABC):
    """
    Storage-agnostic repository contract for Process aggregates.

    Implement this interface in your infrastructure layer
    (e.g. Postgres, DynamoDB, etc).
    """

    @abstractmethod
    def add(self, process: Process) -> None:
        """Persist a new process. Should fail if the ID already exists."""
        raise NotImplementedError

    @abstractmethod
    def save(self, process: Process) -> None:
        """
        Persist changes to an existing process.

        Implementations are encouraged to use optimistic concurrency via
        the `version` field, but this library does not enforce it.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, process_id: str) -> Optional[Process]:
        raise NotImplementedError

    @abstractmethod
    def get_by_aggregate(
        self,
        process_type: str,
        aggregate_type: str,
        aggregate_id: str,
    ) -> Optional[Process]:
        """
        Load a process by its (process_type, aggregate_type, aggregate_id) triple.
        """
        raise NotImplementedError

from __future__ import annotations

from typing import Protocol

from src.storage.domain.repository import StorageOperationRepository

# Unit of Work Port (выходной порт)


class UnitOfWork(Protocol):
    storage_operations: StorageOperationRepository

    def __enter__(self) -> "UnitOfWork": ...
    def __exit__(self, exc_type, exc, tb) -> None: ...

    def commit(self) -> None: ...
    def rollback(self) -> None: ...

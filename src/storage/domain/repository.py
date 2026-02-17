from abc import ABC, abstractmethod
from typing import Any

from src.storage.domain.model import StorageOperation, Location

# Repository Port (выходной порт)


class StorageOperationRepository(ABC):

    @abstractmethod
    def add(self, operation: StorageOperation) -> None:
        pass

    @abstractmethod
    def save(self, event: Any) -> None:
        pass

    @abstractmethod
    def get_available_amount(self, product_id: str) -> int:
        pass

    @abstractmethod
    def get_location(self, location_id: str) -> Location | None:
        pass

    @abstractmethod
    def update_stock(self, product_id: str, delta: int) -> None:
        pass

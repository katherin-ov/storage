from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

# Value Objects


class StorageType(StrEnum):
    """Тип операции со складом"""

    RECEIVE = "RECEIVE"
    PLACE = "PLACE"
    DELIVERY = "DELIVERY"


class DeliveryStatus(StrEnum):
    """Статус отгрузки товара"""

    SCHEDULED = "SCHEDULED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


@dataclass(frozen=True)
class Dimensions:
    """Габариты товара"""

    length: int
    width: int
    height: int


@dataclass(frozen=True)
class Location:
    """Место на складе"""

    location_id: str
    name: str
    is_available: bool | None = None


@dataclass
class ProductLocation:
    """Место товара на складе"""

    location_id: str
    product_id: str


@dataclass(frozen=True)
class Product:
    """Товар"""

    product_id: str
    amount: int
    weight: int
    id_position: int
    dimensions: Dimensions
    location: Location | None = None

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("Amount can not be less than or equal to zero")


# Entity


class StorageOperation:
    def __init__(
        self,
        operation_id: UUID,
        type: StorageType,
        product: Product,
        location: Location | None = None,
        order_id: str | None = None,
        date: datetime | None = None,
        status_delivery: DeliveryStatus | None = None,
    ):
        self.operation_id = operation_id
        self.type = type
        self.product = product
        self.location = location
        self.order_id = order_id
        self.date = date
        self.status_delivery = status_delivery

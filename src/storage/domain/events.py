from dataclasses import dataclass
from datetime import datetime

from src.storage.domain.model import Product, Location

# Domain Events (Факт, который произошёл в домене и может вызвать реакции)


@dataclass(frozen=True)
class ProductReceived:
    """Товар получен"""

    operation_id: str
    supplier_id: str
    products: list[Product]
    date: datetime


@dataclass(frozen=True)
class ProductPlaced:
    """Товар размещен на складе"""

    operation_id: str
    product: Product
    location: Location
    date: datetime


@dataclass(frozen=True)
class DeliveryEvent:
    operation_id: str
    date: datetime
    product: Product
    order_id: str


@dataclass(frozen=True)
class DeliveryScheduled(DeliveryEvent):
    """Доставка запланирована"""

    pass


@dataclass(frozen=True)
class DeliveryCancelled(DeliveryEvent):
    """Доставка отменена"""

    pass

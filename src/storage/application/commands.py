from dataclasses import dataclass
from datetime import datetime

from src.storage.domain.model import Product, Location


@dataclass(frozen=True)
class ReceiveProductCommand:
    """Прием товаров"""

    supplier_id: str
    date: datetime
    products: list[Product]


@dataclass(frozen=True)
class PlaceProductCommand:
    """Размещение товара на полке"""

    product: Product
    location: Location


@dataclass(frozen=True)
class DeliveryProductCommand:
    """Отгрузка товара"""

    date: datetime
    product: Product
    order_id: str
    requested_amount: int


@dataclass(frozen=True)
class DeliveryProductCancelledCommand:
    """Отмена отгрузки товара"""

    date: datetime
    product: Product
    order_id: str
    requested_amount: int

from datetime import datetime
from uuid import uuid4

from src.storage.domain.model import (
    Product,
    StorageOperation,
    StorageType,
    Location,
    DeliveryStatus,
)

# Factory (Объект/функция, создающая сложные агрегаты, скрывая детали)


class StorageOperationFactory:

    @staticmethod
    def receive(
        products: list[Product], date: datetime = None
    ) -> list[StorageOperation]:
        operations = []
        if not products:
            raise ValueError("Receive operation must have at least one product")
        for product in products:
            operations.append(
                StorageOperation(
                    operation_id=uuid4(),
                    type=StorageType.RECEIVE,
                    product=product,
                    location=None,
                    date=date or datetime.utcnow(),
                )
            )
        return operations

    @staticmethod
    def place(product: Product, location: Location) -> StorageOperation:
        return StorageOperation(
            operation_id=uuid4(),
            type=StorageType.PLACE,
            product=product,
            location=location,
            date=datetime.utcnow(),
        )

    @staticmethod
    def delivery(
        product: Product, order_id: str, status: DeliveryStatus, date: datetime = None
    ) -> StorageOperation:
        return StorageOperation(
            operation_id=uuid4(),
            type=StorageType.DELIVERY,
            status_delivery=status,
            product=product,
            order_id=order_id,
            date=date,
        )

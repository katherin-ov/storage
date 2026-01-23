from datetime import datetime

from sqlalchemy.orm import Session

from src.storage.domain.repository import StorageOperationRepository
from src.storage.infrastructure.persistense import (
    StorageOperationModel,
    ProductModel,
    LocationModel,
    DomainEventModel,
)


class SQLStorageRepository(StorageOperationRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, operation):
        product_id = None
        if operation.product.product_id:
            product = operation.product
            product_model = (
                self.session.query(ProductModel)
                .filter_by(product_id=product.product_id)
                .first()
            )

            if not product_model:
                dims = getattr(product, "dimensions", None)
                if dims is not None:
                    if hasattr(dims, "__dict__"):
                        dims = dims.__dict__
                    else:
                        dims = dict(dims)
                product_model = ProductModel(
                    product_id=product.product_id,
                    amount=product.amount,
                    weight=getattr(product, "weight", 0),
                    id_position=getattr(product, "id_position", 0),
                    dimensions=dims,
                    location_id=(
                        getattr(product.location.location_id, "location_id", None)
                        if getattr(product, "location", None)
                        else None
                    ),
                )
                self.session.add(product_model)
                self.session.commit()

            product_id = product_model.product_id

        operation_model = StorageOperationModel(
            operation_id=str(operation.operation_id),
            type=operation.type.value,
            date=operation.date,
            product_id=product_id,
        )

        self.session.add(operation_model)
        self.session.commit()

    def save(self, event):
        payload = {
            "supplier_id": getattr(event, "supplier_id", None),
            "products": [
                {"product_id": p.product_id, "amount": p.amount}
                for p in getattr(event, "products", [])
            ],
            "order_id": getattr(event, "order_id", None),
            "date": (
                getattr(event, "date", None).isoformat()
                if getattr(event, "date", None)
                else None
            ),
        }

        event_model = DomainEventModel(
            operation_id=event.operation_id,
            type=type(event).__name__,
            payload=payload,
            date=getattr(event, "date", datetime.utcnow()),
        )

        self.session.add(event_model)
        self.session.commit()

    def get_product_by_id(self, product_id: str):
        return self.session.query(ProductModel).filter_by(product_id=product_id).first()

    def get_location(self, location_id: str):
        return (
            self.session.query(LocationModel).filter_by(location_id=location_id).first()
        )

    def update_stock(self, product_id: str, delta: int):
        stock = (
            self.session.query(ProductModel).filter_by(product_id=product_id).first()
        )
        if not stock:
            stock = ProductModel(
                product_id=product_id,
                amount=max(0, delta),
                weight=0,
                id_position=0,
                dimensions=None,
                location_id=None,
            )
            self.session.add(stock)
        else:
            stock.amount = max(0, stock.amount + delta)
        self.session.commit()

    def get_available_amount(self, product_id: str) -> int:
        stock = (
            self.session.query(ProductModel).filter_by(product_id=product_id).first()
        )
        return stock.amount if stock else 0

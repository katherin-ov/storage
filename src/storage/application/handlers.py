import logging

from src.storage.application.commands import (
    ReceiveProductCommand,
    PlaceProductCommand,
    DeliveryProductCommand,
    DeliveryProductCancelledCommand,
)
from src.storage.application.unit_of_work import UnitOfWork
from src.storage.domain.events import (
    ProductReceived,
    ProductPlaced,
    DeliveryScheduled,
    DeliveryCancelled,
)
from src.storage.domain.factory import StorageOperationFactory
from src.storage.domain.model import StorageOperation, DeliveryStatus
from src.storage.domain.services import StorageService

logger = logging.getLogger(__name__)


class ReceiveStorageHandler:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.domain_service = StorageService

    def __call__(self, command: ReceiveProductCommand) -> list[StorageOperation]:
        operations = StorageOperationFactory.receive(
            command.products, date=command.date
        )
        for operation in operations:
            self.uow.storage_operations.add(operation)
            event = ProductReceived(
                operation_id=str(operation.operation_id),
                supplier_id=command.supplier_id,
                products=command.products,
                date=operation.date,
            )
            self.uow.storage_operations.save(event)
            self.uow.storage_operations.update_stock(
                operation.product.product_id, delta=operation.product.amount
            )
        return operations


class PlaceStorageHandler:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.domain_service = StorageService

    def __call__(self, command: PlaceProductCommand):
        self.domain_service(self.uow.storage_operations).can_place(
            command.location.location_id
        )
        operation = StorageOperationFactory.place(
            command.product, location=command.location
        )
        self.uow.storage_operations.add(operation)

        event = ProductPlaced(
            str(operation.operation_id),
            product=command.product,
            location=command.location,
            date=operation.date,
        )
        self.uow.storage_operations.save(event)
        return operation


class DeliveryStorageHandler:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.domain_service = StorageService

    def __call__(
        self, command: DeliveryProductCommand | DeliveryProductCancelledCommand
    ):
        if isinstance(command, DeliveryProductCommand):
            self.domain_service(self.uow.storage_operations).can_deliver(
                product_id=command.product.product_id,
                requested_amount=command.requested_amount,
            )

        mapping = {
            DeliveryProductCommand: (DeliveryStatus.SCHEDULED, DeliveryScheduled),
            DeliveryProductCancelledCommand: (
                DeliveryStatus.CANCELLED,
                DeliveryCancelled,
            ),
        }

        operation = StorageOperationFactory.delivery(
            command.product,
            status=mapping[type(command)][0],
            order_id=command.order_id,
            date=command.date,
        )
        self.uow.storage_operations.add(operation)

        event = mapping[type(command)][1](
            operation_id=str(operation.operation_id),
            date=operation.date,
            product=command.product,
            order_id=command.order_id,
        )
        self.uow.storage_operations.save(event)
        self.uow.storage_operations.update_stock(
            operation.product.product_id, delta=-operation.product.amount
        )
        return operation

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from src.storage.application.commands import (
    ReceiveProductCommand,
    PlaceProductCommand,
    DeliveryProductCommand,
    DeliveryProductCancelledCommand,
)
from src.storage.application.handlers import (
    ReceiveStorageHandler,
    PlaceStorageHandler,
    DeliveryStorageHandler,
)
from src.storage.infrastructure.db import get_session
from src.storage.infrastructure.uow import PostgreSQLUnitOfWork

app = FastAPI()


def get_uow(session: Session = Depends(get_session)):
    return PostgreSQLUnitOfWork(lambda: session)


@app.post("/receive")
def receive_products(
    dto: ReceiveProductCommand, uow: PostgreSQLUnitOfWork = Depends(get_uow)
):
    handler = ReceiveStorageHandler(uow)
    try:
        operation = handler(dto)
        return {
            "status": "ok",
            "operation_id": [str(op.operation_id) for op in operation],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/place")
def place_products(
    dto: PlaceProductCommand, uow: PostgreSQLUnitOfWork = Depends(get_uow)
):
    handler = PlaceStorageHandler(uow)
    try:
        operation = handler(dto)
        return {"status": "ok", "operation_id": str(operation.operation_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/delivery")
def delivery_products(
    dto: DeliveryProductCommand, uow: PostgreSQLUnitOfWork = Depends(get_uow)
):
    handler = DeliveryStorageHandler(uow)
    try:
        operation = handler(dto)
        return {"status": "ok", "operation_id": str(operation.operation_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/cancel-delivery")
def cancel_delivery_products(
    dto: DeliveryProductCancelledCommand, uow: PostgreSQLUnitOfWork = Depends(get_uow)
):
    handler = DeliveryStorageHandler(uow)
    try:
        operation = handler(dto)
        return {"status": "ok", "operation_id": str(operation.operation_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

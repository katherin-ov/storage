from datetime import datetime

from src.storage.infrastructure.persistense import DomainEventModel


def test_api_delivery(client, in_memory_session):
    payload = {
        "date": datetime.utcnow().isoformat(),
        "product": {
            "product_id": "product_1",
            "amount": 10,
            "weight": 100,
            "id_position": 1,
            "dimensions": {"length": 10, "width": 10, "height": 5},
            "location": None,
        },
        "order_id": "Order_1",
        "requested_amount": 5,
    }

    response = client.post("/delivery", json=payload)
    data = response.json()
    op_id = data["operation_id"]
    domain_event = (
        in_memory_session.query(DomainEventModel).filter_by(operation_id=op_id).first()
    )

    assert response.status_code == 200
    assert "operation_id" in data
    assert domain_event is not None
    assert domain_event.type == "DeliveryScheduled"


def test_api_delivery__not_enough_products(client, in_memory_session):
    payload = {
        "date": datetime.utcnow().isoformat(),
        "product": {
            "product_id": "product_1",
            "amount": 5,
            "weight": 100,
            "id_position": 1,
            "dimensions": {"length": 10, "width": 10, "height": 5},
            "location": None,
        },
        "order_id": "Order_1",
        "requested_amount": 50,
    }

    response = client.post("/delivery", json=payload)
    data = response.json()

    assert response.status_code == 400
    assert (
        "Not enough products for order, only 10 amount is available" in data["detail"]
    )


def test_api_delivery_cancelled(client, in_memory_session):
    payload = {
        "date": datetime.utcnow().isoformat(),
        "product": {
            "product_id": "product_1",
            "amount": 5,
            "weight": 100,
            "id_position": 1,
            "dimensions": {"length": 10, "width": 10, "height": 5},
            "location": None,
        },
        "order_id": "Order_1",
        "requested_amount": 10,
    }

    response = client.post("/cancel-delivery", json=payload)
    data = response.json()
    op_id = data["operation_id"]
    domain_event = (
        in_memory_session.query(DomainEventModel).filter_by(operation_id=op_id).first()
    )

    assert response.status_code == 200
    assert "operation_id" in data
    assert domain_event is not None
    assert domain_event.type == "DeliveryCancelled"

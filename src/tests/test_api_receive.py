from datetime import datetime

from src.storage.infrastructure.persistense import DomainEventModel


def test_api_receive(client, in_memory_session):
    payload = {
        "supplier_id": "supplier_1",
        "date": datetime.utcnow().isoformat(),
        "products": [
            {
                "product_id": "p1",
                "amount": 10,
                "weight": 100,
                "id_position": 1,
                "dimensions": {"length": 10, "width": 10, "height": 5},
                "location": None,
            }
        ],
    }

    response = client.post("/receive", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "operation_id" in data

    op_id = data["operation_id"][0]

    domain_event = (
        in_memory_session.query(DomainEventModel).filter_by(operation_id=op_id).first()
    )
    assert domain_event is not None
    assert domain_event.type == "ProductReceived"

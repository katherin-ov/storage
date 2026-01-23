from src.storage.infrastructure.persistense import DomainEventModel


def test_api_place__with_engaged_place(client, in_memory_session):
    payload = {
        "product": {
            "product_id": "product_1",
            "amount": 10,
            "weight": 100,
            "id_position": 1,
            "dimensions": {"length": 10, "width": 10, "height": 5},
            "location": None,
        },
        "location": {
            "location_id": "location_1",
            "name": "Shelf A1",
        },
    }

    response = client.post("/place", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Location location_1 is engaged"


def test_api_place(client, in_memory_session):
    payload = {
        "product": {
            "product_id": "product_1",
            "amount": 10,
            "weight": 100,
            "id_position": 1,
            "dimensions": {"length": 10, "width": 10, "height": 5},
            "location": None,
        },
        "location": {
            "location_id": "location_2",
            "name": "Shelf A1",
            "is_available": True,
        },
    }

    response = client.post("/place", json=payload)
    data = response.json()
    domain_event = (
        in_memory_session.query(DomainEventModel)
        .filter_by(operation_id=data["operation_id"])
        .first()
    )

    assert response.status_code == 200
    assert "operation_id" in data
    assert domain_event.operation_id == data["operation_id"]
    assert domain_event is not None
    assert domain_event.type == "ProductPlaced"

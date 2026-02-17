import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from src.storage.entrypoints.app import app
from src.storage.infrastructure.persistense import Base, LocationModel, ProductModel
from src.storage.infrastructure.db import get_session


@pytest.fixture
def in_memory_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    location_1 = LocationModel(
        location_id="location_1", name="test", is_available=False
    )
    location_2 = LocationModel(location_id="location_2", name="test", is_available=True)
    product = ProductModel(
        product_id="product_1",
        amount=10,
        weight=100,
        id_position=1,
        dimensions={"length": 10, "width": 10, "height": 5},
        location_id="location_1",
    )
    session.add_all([location_1, location_2, product])
    session.commit()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(in_memory_session):
    def override_get_session():
        return in_memory_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

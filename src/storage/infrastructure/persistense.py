from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StorageOperationModel(Base):
    __tablename__ = "storage_operations"

    operation_id = Column(String, primary_key=True)
    type = Column(String)
    product_id = Column(String, ForeignKey("products.product_id"))
    date = Column(DateTime)
    order_id = Column(String)


class DomainEventModel(Base):
    __tablename__ = "domain_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    operation_id = Column(String)
    type = Column(String)
    payload = Column(JSON)
    date = Column(DateTime)


class ProductModel(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    amount = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    id_position = Column(Integer, nullable=False)
    dimensions = Column(JSON, nullable=True)
    location_id = Column(String, ForeignKey("locations.location_id"))


class LocationModel(Base):
    __tablename__ = "locations"

    location_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    is_available = Column(Boolean)

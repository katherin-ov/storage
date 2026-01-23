from __future__ import annotations

# Domain Service (Функция предметной области, которая не принадлежит ни одной сущности, но относится к бизнес-логике)


class StorageService:
    def __init__(self, repository):
        self.repository = repository

    def can_place(self, location_id: str) -> bool:
        """Проверка, что место свободно"""
        location = self.repository.get_location(location_id)
        if location and location.is_available is False:
            raise ValueError(f"Location {location_id} is engaged")
        return True

    def can_deliver(self, product_id: str, requested_amount: int) -> bool:
        """Проверка, что на складе достаточное количество товаров для отгрузки"""
        available = self.repository.get_available_amount(product_id)
        if requested_amount > available:
            raise ValueError(
                f"Not enough products for order, only {available} amount is available"
            )
        return True

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_add_product_to_fridge(ac: AsyncClient):
    """Тест успішного додавання продукту в холодильник"""

    payload = {
        "product_name": "Тестове молоко",
        "expiration_date": "2026-06-20",
        "quantity": 2,
        "category": "dairy",
    }
    
    # Надсилаємо POST запит через наш асинхронний клієнт 'ac'
    response = await ac.post("/fridge/products", json=payload)
    
    # Перевіряємо, що статус відповіді 201 Created
    assert response.status_code == 201
    
    data = response.json()
    # Перевіряємо, що дані збереглися правильно
    assert data["product_name"] == "Тестове молоко"
    assert data["quantity"] == 2
    assert data["category"] == "dairy"
    assert "id" in data
    assert "user_id" in data


async def test_get_fridge_status(ac: AsyncClient):
    """Тест перевірки структурованого статусу холодильника"""
    
    # Викликаємо наш GET-роут аналітики
    response = await ac.get("/fridge/status")
    
    assert response.status_code == 200
    
    data = response.json()
    # Перевіряємо, що структура відповіді чітко містить наші три DTO-блоки
    assert "expired" in data
    assert "spoiling_soon" in data
    assert "fresh" in data
    
    # Перевіряємо, що це списки (масиви)
    assert isinstance(data["expired"], list)
    assert isinstance(data["spoiling_soon"], list)
    assert isinstance(data["fresh"], list)
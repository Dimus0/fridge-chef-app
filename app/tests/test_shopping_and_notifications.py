import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_shopping_flow(ac: AsyncClient):
    create_response = await ac.post("/shopping/items", json={"item_name": "Milk"})
    item_id = create_response.json()["id"]

    list_response = await ac.get("/shopping/items")
    toggle_response = await ac.patch(f"/shopping/items/{item_id}/toggle")

    assert create_response.status_code == 201
    assert len(list_response.json()) == 1
    assert toggle_response.status_code == 200
    assert toggle_response.json()["is_bought"] is True


async def test_notification_endpoint(ac: AsyncClient):
    await ac.post(
        "/fridge/products",
        json={
            "product_name": "Yogurt",
            "expiration_date": "2026-06-01",
            "quantity": 1,
            "category": "dairy",
        },
    )

    response = await ac.get("/notifications/")

    assert response.status_code == 200
    assert response.json()[0]["type"] in {"expired", "expiring_soon"}

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_user(ac: AsyncClient):
    response = await ac.post(
        "/auth/",
        json={
            "username": "new-user",
            "email": "new-user@example.com",
            "password": "supersecret",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "User created successfully"


async def test_get_current_profile(ac: AsyncClient):
    response = await ac.get("/auth/me")

    assert response.status_code == 200
    payload = response.json()
    assert payload["username"] == "test-user"
    assert payload["is_superuser"] is True

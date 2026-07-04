import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health_and_readiness(ac: AsyncClient):
    health_response = await ac.get("/health")
    ready_response = await ac.get("/ready")

    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok"}
    assert ready_response.status_code == 200
    assert ready_response.json()["status"] == "ready"


async def test_admin_audit_logs(ac: AsyncClient):
    await ac.post(
        "/auth/",
        json={
            "username": "audited-user",
            "email": "audited@example.com",
            "password": "supersecret",
        },
    )

    response = await ac.get("/admin/audit-logs")

    assert response.status_code == 200
    assert len(response.json()) >= 1

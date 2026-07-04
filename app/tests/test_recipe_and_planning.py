import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def seed_recipe_and_products(ac: AsyncClient) -> None:
    await ac.post(
        "/fridge/products",
        json={
            "product_name": "egg",
            "expiration_date": "2026-07-01",
            "quantity": 6,
            "category": "protein",
        },
    )
    await ac.post(
        "/fridge/products",
        json={
            "product_name": "bread",
            "expiration_date": "2026-07-01",
            "quantity": 1,
            "category": "bakery",
        },
    )
    await ac.post(
        "/recipes/",
        json={
            "title": "Egg Toast",
            "ingredients": "egg, bread, butter",
            "instruction": "Toast bread and add egg.",
            "prep_time": 10,
        },
    )


async def test_create_and_update_recipe(ac: AsyncClient):
    create_response = await ac.post(
        "/recipes/",
        json={
            "title": "Salad",
            "ingredients": "tomato, cucumber",
            "instruction": "Mix ingredients.",
            "prep_time": 5,
        },
    )
    recipe_id = create_response.json()["id"]

    update_response = await ac.put(
        f"/recipes/{recipe_id}",
        json={"title": "Updated Salad", "prep_time": 7},
    )

    assert create_response.status_code == 201
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Salad"
    assert update_response.json()["prep_time"] == 7


async def test_inventory_recommendation_and_planning_endpoints(ac: AsyncClient):
    await seed_recipe_and_products(ac)

    inventory_response = await ac.get("/inventory/overview")
    recommendation_response = await ac.get("/recommendations/recipes")
    shopping_plan_response = await ac.get("/shopping-planner/missing-items")
    meal_plan_response = await ac.get("/meal-plan/daily")

    assert inventory_response.status_code == 200
    assert inventory_response.json()["total_items"] == 7

    assert recommendation_response.status_code == 200
    assert recommendation_response.json()[0]["missing_ingredients"] == ["butter"]

    assert shopping_plan_response.status_code == 200
    assert shopping_plan_response.json()[0]["missing_items"] == ["butter"]

    assert meal_plan_response.status_code == 200
    assert meal_plan_response.json()["breakfast"] == "Egg Toast"

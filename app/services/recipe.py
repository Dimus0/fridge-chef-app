import uuid
from fastapi import HTTPException,status
from sqlalchemy import select, update,delete
from sqlalchemy.ext.asyncio import AsyncSession
import json
from openai import AsyncOpenAI
import requests
from app.models.recipe import Recipe as RecipeModel
from app.models.product import Product as ProductModel

from app.schemas.recipe import RecipeCreate, RecipeUpdate,RecipeGenerateRequest,RecipeGenerateResponse
from app.schemas.product import ProductBase,ProductRead

ai_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "FridgeChef App",
    }
)

class RecipeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_recipe(self, recipe_request: RecipeCreate, user_id: uuid.UUID) -> RecipeModel:
        new_recipe = RecipeModel(
            user_id=user_id,
            title=recipe_request.title,
            ingredients=recipe_request.ingredients,
            instruction=recipe_request.instruction,
            prep_time=recipe_request.prep_time,
        )
        self.db.add(new_recipe)
        await self.db.commit()
        await self.db.refresh(new_recipe)
        
        return {"status": "success", "message": "Recipe created successfully", "data": new_recipe}

    async def get_all_recipe_for_user(self, user_id: uuid.UUID):
        result = await self.db.execute(
            select(RecipeModel).where(RecipeModel.user_id == user_id)
        )

        return result.scalars().all()
    
    async def get_recipe_by_id(self, recipe_id: uuid.UUID, user_id: uuid.UUID) -> RecipeModel:
        result = await self.db.execute(
            select(RecipeModel).where(RecipeModel.id == recipe_id, RecipeModel.user_id == user_id)
        )
        recipe = result.scalar_one_or_none()
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        return recipe
    
    async def update_recipe(self, recipe_id: uuid.UUID, recipe_request: RecipeUpdate, user_id: uuid.UUID) -> RecipeModel:
        recipe = await self.get_recipe_by_id(recipe_id, user_id)

        # Конвертуємо Pydantic схему в словник, виключаючи непередані поля (None)
        update_data = recipe_request.dict(exclude_unset=True)

        if update_data:
            await self.db.execute(
                update(RecipeModel)
                .where(RecipeModel.id == recipe_id).values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(recipe)
        
        return {"status": "success", "message": "Recipe updated successfully", "data": recipe}

    async def delete_recipe(self, recipe_id: uuid.UUID, user_id: uuid.UUID) -> dict:
        recipe = await self.get_recipe_by_id(recipe_id, user_id)

        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        
        await self.db.execute(
            delete(RecipeModel).where(RecipeModel.id == recipe_id)
        )
        await self.db.commit()

        return {"status": "success", "message": "Recipe deleted successfully"}
    
    async def generate_recipe_ai(self, request_data: RecipeGenerateRequest, user_id: uuid.UUID) -> RecipeModel:

        ingredients_string = ", ".join(request_data.ingredients)

        prompt = (
            "Ти — шеф-кухар додатку FridgeChef. Твоє завдання — згенерувати один кулінарний рецепт "
            "на основі наданих інгредієнтів. Ти ПОВИНЕН повернути відповідь СТРОГО у форматі JSON. "
            "Не пиши жодних вступів, пояснень чи підсумків. Тільки чистий JSON-об'єкт.\n"
            "Структура JSON має бути наступною:\n"
            "{\n"
            '  "title": "Назва страви",\n'
            '  "ingredients": "перелік інгредієнтів через кому",\n'
            '  "instruction": "Покрокова інструкція приготування"\n'
            '  "prep_time": 30,\n'
            "}"
        )
        
        response = await ai_client.chat.completions.create(
            model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
            messages=[
                {"role":"system","content":prompt},
                {"role": "user", "content": f"Мої інгрідієнти: {ingredients_string}"}
            ],

            # response_format={"type": "json-object"}
        )

        raw_ai_content = response.choices[0].message.content

        cleaned_content = raw_ai_content.strip()
        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[7:]
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]
        cleaned_content = cleaned_content.strip()

        recipe_dictionary = json.loads(cleaned_content)

        new_recipe= RecipeModel(
            **recipe_dictionary,
            user_id=user_id
        )

        self.db.add(new_recipe)
        await self.db.commit()
        await self.db.refresh(new_recipe)

        return new_recipe

    # Потрібне тестування
    async def recipe_matching(self, user_id: uuid.UUID) -> list:
        products = await self.db.execute(
            select(ProductModel).where(ProductModel.user_id == user_id)
        )
        db_products = products.scalars().all()
        fridge_set = {p.product_name.strip().lower() for p in db_products}

        recipies = await self.get_all_recipe_for_user(user_id=user_id)

        available_recipes = []

        for recipe in recipies:

            recipe_ingredients_list = [ingr.strip().lower() for ingr in recipe.ingredients.split(",")]

            recipe_set = set(recipe_ingredients_list)

            if recipe_set.issubset(fridge_set):
                available_recipes.append(recipe)

        return available_recipes


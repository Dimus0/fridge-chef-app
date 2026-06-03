import uuid
from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.schemas.recipe import RecipeCreate, RecipeRead, RecipeUpdate,RecipeGenerateRequest,RecipeGenerateResponse
from app.services.recipe import RecipeService
from app.routers.auth import get_current_user_dependency
from app.models.user import User

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
user_dependency = Annotated[User, Depends(get_current_user_dependency)]

def get_recipe_service(db: db_dependency) -> RecipeService:
    return RecipeService(db)

recipe_service_dependency = Annotated[RecipeService, Depends(get_recipe_service)]

@router.post("/", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_request: RecipeCreate,
    recipe_service: recipe_service_dependency,
    current_user: user_dependency,
):
    return await recipe_service.create_recipe(recipe_request, user_id=current_user.id)

@router.get("/{recipe_id}", response_model=RecipeRead)
async def read_recipe(
    recipe_id: uuid.UUID,
    recipe_service: recipe_service_dependency,
    current_user: user_dependency
):
    return await recipe_service.get_recipe_by_id(user_id=current_user.id, recipe_id=recipe_id)

@router.put("/{recipe_id}", status_code=status.HTTP_200_OK)
async def update_recipe(
    recipe_id: uuid.UUID,
    recipe_service: recipe_service_dependency,
    current_user: user_dependency
):
    return await recipe_service.update_recipe(recipe_id=recipe_id, user_id=current_user.id)

@router.post("/generate/", response_model=RecipeGenerateResponse,status_code=status.HTTP_200_OK)
async def generate_recipe_endpoint(
    request_data: RecipeGenerateRequest,
    recipe_service: recipe_service_dependency,
    current_user: user_dependency
):
    return await recipe_service.generate_recipe_ai(request_data,user_id=current_user.id)
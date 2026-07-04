import uuid
from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.routers.auth import get_current_user_dependency
from app.models.user import User
from app.schemas.shopping import ShoppingItemCreate, ShoppingItemRead
from app.services.shopping import ShoppingService

router = APIRouter(
    prefix="/shopping",
    tags=["shopping list"],
)

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
user_dependency = Annotated[User, Depends(get_current_user_dependency)]

def get_shopping_service(db: db_dependency) -> ShoppingService:
    return ShoppingService(db)

shopping_service_dependency = Annotated[ShoppingService, Depends(get_shopping_service)]


# 1. Додати товар у список
@router.post("/items", response_model=ShoppingItemRead, status_code=status.HTTP_201_CREATED)
async def add_item_to_shopping_list(
    request: ShoppingItemCreate,
    service: shopping_service_dependency,
    current_user: user_dependency
):
    return await service.create_item(request=request, user_id=current_user.id)


# 2. Переглянути весь список покупок юзера
@router.get("/items", response_model=List[ShoppingItemRead])
async def get_my_shopping_list(
    service: shopping_service_dependency,
    current_user: user_dependency
):
    return await service.get_all_items(user_id=current_user.id)


# 3. Перемикач стану "Куплено" (Toggle)
@router.patch("/items/{item_id}/toggle", response_model=ShoppingItemRead)
async def toggle_shopping_item(
    item_id: uuid.UUID,
    service: shopping_service_dependency,
    current_user: user_dependency
):
    return await service.toggle_item_status(item_id=item_id, user_id=current_user.id)
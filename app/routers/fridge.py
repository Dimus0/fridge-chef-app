import uuid
from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.routers.auth import get_current_user_dependency
from app.models.user import User
from app.models.product import Product
from app.schemas.product import ProductBase,ProductCreate,ProductRead,FridgeStatusResponse
from app.services.fridge import FridgeService

router = APIRouter(
    prefix="/fridge",
    tags=["fridge"],
)

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
user_dependency = Annotated[User, Depends(get_current_user_dependency)]

def get_fridge_service(db: db_dependency) -> FridgeService:
    return FridgeService(db)

fridge_service_dependency = Annotated[FridgeService, Depends(get_fridge_service)]

@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def app_product_to_fridge(
    request: ProductCreate, 
    service: fridge_service_dependency, 
    current_user: user_dependency
):
    return await service.create_product(request=request, user_id=current_user.id)


@router.get("/status", response_model=FridgeStatusResponse)
async def get_fridge_status(
    service: fridge_service_dependency, 
    current_user: user_dependency
):
    return await service.get_fridge_status(user_id=current_user.id)

import uuid
from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.shoppingcart import ShoppingItem as ShoppingItemModel
from app.schemas.shopping import ShoppingItemCreate

class ShoppingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_item_into_cart(self, request: ShoppingItemCreate, user_id: uuid.UUID) -> ShoppingItemModel:
        new_items = ShoppingItemModel(
            user_id = user_id,
            item_name = request.item_name
        )

        self.db.add(new_items)
        await self.db.commit()
        await self.db.refresh(new_items)

        return new_items
    
    async def get_all_items(self, user_id: uuid.UUID):
        results = await self.db.execute(
            select(ShoppingItemModel).where(ShoppingItemModel.user_id == user_id)
        )

        return results.scalars().all()
    
    async def get_item_by_id(self, item_id: uuid.UUID, user_id: uuid.UUID) -> ShoppingItemModel:
        results = await self.db.execute(
            select(ShoppingItemModel).where(ShoppingItemModel.id == item_id, ShoppingItemModel.user_id == user_id)
        )

        item = results.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping item not found")
        
        return item
    
    async def toggle_item_status(self, item_id: uuid.UUID, user_id: uuid.UUID) -> ShoppingItemModel:
        item = await self.get_item_by_id(item_id,user_id)

        item.is_bought = not item.is_bought

        await self.db.commit()
        await self.db.refresh(item)
        
        return item
    
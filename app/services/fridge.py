import uuid
from fastapi import HTTPException,status
from sqlalchemy import select, update,delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.product import Product as ProductModel
from app.schemas.product import ProductCreate

from datetime import date,timedelta 

class FridgeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, request: ProductCreate, user_id: uuid.UUID) -> ProductModel:
        exp_date = request.expiration_date
        if hasattr(exp_date, "date"):
            exp_date = exp_date.date()
        
        new_product = ProductModel(
            user_id = user_id,
            product_name = request.product_name,
            expiration_date = exp_date
        )

        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)

        return new_product
    
    # test
    async def delete_product(self, product_id: uuid.UUID, user_id: uuid.UUID) -> dict:
        product = await self.get_product_by_id(product_id, user_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Product not found"
            )
        
        try:
            await self.db.execute(
                delete(ProductModel).where(ProductModel.id == product_id)
            )
            await self.db.commit()
            
            return {
                "status": "success",
                "message": "Product deleted successfully"
            }
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete product due to foreign key constraints"
            )
    # test
    async def cleaning_all_product_in_fridge(self, user_id: uuid.UUID):
        product = await self.db.execute(
            delete(ProductModel).where(ProductModel.user_id == user_id)
        )
        
        self.db.commit()

        return {
            "status": "success",
            "message": f"Fridge has been clear! {product.rowcount} products deleted"
        }
        
    async def get_all_product_for_user_in_fridge(self, user_id: uuid.UUID):
        result = await self.db.execute(
            select(ProductModel).where(ProductModel.user_id == user_id)
        )

        return result.scalars().all()
    
    async def get_product_by_id(self, product_id: uuid.UUID, user_id: uuid.UUID) -> ProductModel:
        result = await self.db.execute(
            select(ProductModel).where(ProductModel.id == product_id, ProductModel.user_id == user_id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prodcut not found on fridge")
        
        return product
    
    async def get_fridge_status(self, user_id: uuid.UUID) -> dict:

        products = await self.get_all_product_for_user_on_fridge(user_id=user_id)

        expired_list = []
        spoiling_soon_list = []
        fresh_list = []

        today = date.today()

        spoiling_deadline = today + timedelta(days=2)

        for product in products:
            prod_date = product.expiration_date
            
            if hasattr(prod_date, "date"):
                prod_date = prod_date.date()

            # 🔴 Перевірка 1: Продукт зіпсувався (дата в минулому)
            if prod_date < today:
                expired_list.append(product)
            
            # 🟡 Перевірка 2: Зіпсується сьогодні, завтра або післязавтра
            elif today <= prod_date <= spoiling_deadline:
                spoiling_soon_list.append(product)
            
            # 🟢 Перевірка 3: Продукт свіжий (термін придатності більше ніж 2 дні)
            else:
                fresh_list.append(product)


        return {
            "expired": expired_list,
            "spoiling_soon": spoiling_soon_list,
            "fresh": fresh_list
        }
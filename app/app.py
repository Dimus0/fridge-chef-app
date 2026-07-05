from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth as auth_routers
from app.routers import recipe as recipe_routers
from app.routers import fridge as fridge_routers
from app.routers import shopping as shopping_routers
from contextlib import asynccontextmanager
from app.db.database import Base,engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title="FridgeChef API",
    swagger_ui_parameters={"persistAuthorization": True}, 
    )

app.include_router(router=auth_routers.router)
app.include_router(router=recipe_routers.router)
app.include_router(router=fridge_routers.router)
app.include_router(router=shopping_routers.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # адреса майбутнього React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
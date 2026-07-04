from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import create_db_tables
from contextlib import asynccontextmanager

from app.routers import auth as auth_routers
from app.routers import recipe as recipe_routers
from app.routers import fridge as fridge_routers
from app.routers import shopping as shopping_routers


app = FastAPI(title="FridgeChef API")

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
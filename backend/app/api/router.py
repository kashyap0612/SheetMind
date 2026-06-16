from fastapi import APIRouter
from app.api.routes import api_keys, chat, files, health, users

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(files.router)
api_router.include_router(chat.router)
api_router.include_router(api_keys.router)

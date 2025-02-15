from fastapi import APIRouter
from src.api.endpoints import devices, ws

api_router = APIRouter()

api_router.include_router(devices.router)
api_router.include_router(ws.router)

from fastapi import APIRouter

from src.api.routers.v1.messages import router as msg_router


v1_router = APIRouter(tags=["v1"], prefix="/api/v1")

v1_router.include_router(msg_router)

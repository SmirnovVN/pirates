from fastapi import APIRouter

from app.api.routes import ships


router = APIRouter()

router.include_router(ships.router, prefix="/ships")

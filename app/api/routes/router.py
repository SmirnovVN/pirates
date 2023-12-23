from fastapi import APIRouter

from app.api.routes import ships, game

router = APIRouter()

router.include_router(ships.router, prefix="/ships")
router.include_router(game.router, prefix="/game")

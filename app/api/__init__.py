from fastapi import APIRouter

from . import games, monitoring

router = APIRouter()
router.include_router(games.router, tags=["games"])
router.include_router(monitoring.router, tags=["monitoring"])

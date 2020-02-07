from fastapi import APIRouter

from app import db

router = APIRouter()


@router.get("/ping")
async def ping():
    """Health check for service"""
    return {"status": "OK"}


@router.get("/ping/db")
def ping_db():
    try:
        db.ping_db()
    except Exception:
        return {"status": "ERROR"}
    return {"status": "OK"}

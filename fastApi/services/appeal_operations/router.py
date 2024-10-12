from fastapi import APIRouter,  HTTPException, Depends

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func
from database import get_async_session

from services.appeal_operations.schemas import CreateAppeal

router = APIRouter(
    prefix="/operations",
    tags=["Analyzing"]
)

@router.post("/create_appeal")
def get(new_appeal: CreateAppeal):
    return new_appeal
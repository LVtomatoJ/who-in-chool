from typing import Annotated
from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import DBUser
from app.routers.schemas.common import UserRead


router = APIRouter()


@router.get("/user", response_model=UserRead)
def get_user(user_model: Annotated[DBUser, Depends(get_current_user)]):
    return user_model

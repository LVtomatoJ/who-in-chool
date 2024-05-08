from typing import Annotated
from sqlmodel import Session
from app.database import get_session
from fastapi import Depends

DBSessionDep = Annotated[Session, Depends(get_session)]

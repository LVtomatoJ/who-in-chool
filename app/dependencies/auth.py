from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.dependencies.db import DBSessionDep
from app.models.user import DBUser
from app.routers.schemas.common import TokenData
from app.routers.utils.common import get_user_by_user_id
from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from app.config import settings

SECRET_KEY = settings.token_secret
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ProxyJWTSessionDep(BaseModel):
    jw_session: str
    school_id: int
    user_model: DBUser


async def get_proxy_jw_session(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: DBSessionDep,
) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        jw_session: str = payload.get("jw_session")
        if jw_session is None:
            raise HTTPException(status_code=401, detail="user_id is None!")
        return jw_session
    except JWTError:
        raise HTTPException(status_code=401, detail="JWTError")


async def get_proxy_all_session(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: DBSessionDep,
) -> ProxyJWTSessionDep:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="user_id is None!")
        school_id: str = payload.get("school_id")
        if school_id is None:
            raise HTTPException(status_code=401, detail="school_id is None!")
        jw_session: str = payload.get("jw_session")
        if jw_session is None:
            raise HTTPException(status_code=401, detail="jw_session is None!")
    except JWTError:
        raise HTTPException(status_code=401, detail="JWTError")
    user: DBUser | None = get_user_by_user_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="not user")

    return ProxyJWTSessionDep(
        jw_session=jw_session, user_model=user, school_id=school_id
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: DBSessionDep,
) -> DBUser:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="user_id is None!")
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="JWTError")
    user: DBUser | None = get_user_by_user_id(
        session=session, user_id=token_data.user_id
    )
    if not user:
        raise HTTPException(status_code=401, detail="not user")
    return user


JWTUserAuthDep = Annotated[DBUser, Depends(get_current_user)]
JWTProxyJwSessionDep = Annotated[str, Depends(get_proxy_jw_session)]
JWTProxySessionDep = Annotated[ProxyJWTSessionDep, Depends(get_proxy_all_session)]

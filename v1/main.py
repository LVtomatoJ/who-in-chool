

from datetime import datetime, timedelta
from typing import Union
from fastapi import FastAPI, status, Request,Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import tool
app = FastAPI()

origins = [
    "http://localhost:3333",
    "localhost:3333"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


SECRET_KEY ='5d8788a74ba363c1b08329363b42f30c75d3cb762714aa32761cb0e214b5474d'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    r = await tool.get_user_by_email(token_data.username)
    if r['code']!=0:
        raise credentials_exception
    return {'code':0,'data':r['data']}

# async def get_current_active_user(current_user = Depends(get_current_user)):
#     # if current_user.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"code": 1, "message": "提交参数错误"})
    )


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    r = await tool.check_user_password_by_email(email=form_data.username,password=form_data.password)
    if r['code']!=0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/v1/reg",tags=["users"])
async def reg(email: EmailStr, open_id: str, password: str):
    r = await tool.check_user_exist(email=email, open_id=open_id)
    if r['code'] != 0:
        return r
    r = await tool.add_user(email=email, open_id=open_id, password=password)
    if r['code'] == 1:
        return r
    return r


@app.get("/")
# async def hello():
async def hello(d = Depends(get_current_user)):
    return {'hello':"22"}

@app.get("/v1/bind",tags=['binds'])
async def bind(user_id: int, password: str, bind_id: str, bind_password: str):
    r = await tool.check_user_password(user_id=user_id, password=password)
    if r['code'] != 0:
        return r
    max_bind = r['data']['user']['max_bind']
    r = await tool.check_bind_user_exist(bind_id=bind_id)
    if r['code'] != 0:
        return r

    r = await tool.check_bind_number(user_id=user_id, max_bind=max_bind)
    if r['code'] != 0:
        return r

    r = await tool.check_bind_user_password(bind_id=bind_id, bind_password=bind_password)
    if r['code'] != 0:
        return r
    jwsession = r['data']['jwsession']
    r = await tool.add_bind_user(user_id=user_id, bind_id=bind_id, bind_password=bind_password, jwsession=jwsession)
    if r['code'] == 1:
        return r
    return {"code": 0, "message": '绑定成功'}


@app.get('/v1/del_bind',tags=['binds'])
async def del_bind(user_id: int, password: str, bind_id):
    r = await tool.check_user_password(user_id=user_id, password=password)
    if r['code'] != 0:
        return r
    r = await tool.del_bind(bind_id=bind_id)
    if r['code'] != 0:
        return r
    return {"code": 0, "message": "删除成功"}


@app.get('/v1/get_binds',tags=['binds'])
async def get_user_binds(user_id: int, password: str):
    r = await tool.check_user_password(user_id=user_id, password=password)
    if r['code'] != 0:
        return r
    r = await tool.get_user_binds(user_id)
    if r['code'] != 0:
        return r
    return {'code': 0, "message": "查询成功", 'data': r['data']}


@app.get('/v1/get_user',tags=['users'])
async def get_user(user_id: int, password: str):
    r = await tool.check_user_password(user_id=user_id, password=password)
    if r['code'] != 0:
        return r
    r = await tool.get_user(user_id=user_id)
    if r['code'] != 0:
        return r
    return {'code': 0, "message": "查询成功", "data": r["data"]}

@app.get('/v1/get_user_by_email',tags=['users'])
async def get_user(email: str, password: str):
    r = await tool.check_user_password_by_email(email=email, password=password)
    if r['code'] != 0:
        return r
    user_id = r['data']['user_id']
    r = await tool.get_user(user_id=user_id)
    if r['code'] != 0:
        return r
    data:dict = r['data']
    data['user_id'] = user_id
    return {'code': 0, "message": "查询成功", "data": data}



@app.get('/v1/add_work',tags=['works'])
async def add_work(user_id: int, password: str, bind_id: str, time_type: int, work_type: int, state: int, hour: int, minute: int, weektime: int, template_id: int):
    r = await tool.check_user_password(user_id=user_id, password=password)
    if r['code'] != 0:
        return r
    max_work = r['data']['user']['max_work']
    r = await tool.check_template_exist(template_id=template_id)
    if r['code'] != 0:
        return r
    r = await tool.check_work_number(user_id=user_id, max_work=max_work)
    if r['code'] != 0:
        return r
    r = await tool.add_work(user_id=user_id, bind_id=bind_id, time_type=time_type, work_type=work_type, state=state, hour=hour, minute=minute, weektime=weektime, template_id=template_id)
    if r['code'] != 0:
        return r
    work_id = r['data']['work_id']
    return {'code': 0, 'message': "任务添加成功", 'data': {'work_id': work_id}}

@app.get('/v1/run_work',tags=['works'])
async def run_work(user_id:int,password:str,work_id:int):
    r = await tool.check_user_password(user_id=user_id, password=password)
    if r['code'] != 0:
        return r
    r = await tool.run_work(user_id=user_id,work_id=work_id)
    if r['code'] != 0:
        return r
    return {'code':0,"message":"运行任务成功"}
@app.get('/v1/del_work',tags=['works'])
async def del_work(user_id:int,password:str,work_id:int):
    r = await tool.check_user_password(user_id=user_id, password=password)
    if r['code'] != 0:
        return r
    r = await tool.del_work(work_id=work_id,user_id=user_id)
    if r['code'] !=0:
        return r
    return {'code':0,'message':"删除任务成功"}


@app.get('/v1/get_works',tags=['works'])
async def get_works(user_id:int,password:str):
    r = await tool.check_user_password(user_id=user_id, password=password)
    if r['code'] != 0:
        return r
    r = await tool.get_works(user_id=user_id)
    if r['code'] !=0:
        return r
    return {'code':0,'message':"查询任务成功","data":r["data"]}


@app.get('/test_work',tags=['test'])
async def test_work(work_id:int):
    r = await tool.test_work(work_id=work_id)
    if r['code'] !=0:
        return r
    return r


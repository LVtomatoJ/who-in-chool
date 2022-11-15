from datetime import datetime, timedelta
import time
from typing import Optional, Union
from fastapi import FastAPI, status, Request,Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import tools

app = FastAPI()


class UserInfo(BaseModel):
    email:str
    openid:str
    level:int
    maxbindnum:int
    maxworknum:int

class Template(BaseModel):
    
    templateid:str
    name:str
    status:int
    school:str

class Templates(BaseModel):
    templates:list[Template]


# origins = [
#     "http://localhost:3333",
#     "localhost:3333"
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

origins = [
    "http://localhost",
    "http://localhost:3333",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:3333",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY ='5d8788a74ba363c1b08329363b42f30c75d3cb762714aa32761cb0e214b5474d'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

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

async def get_current_user_by_email(token: str = Depends(oauth2_scheme)):
    """验证token[email]

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).

    Returns:
        dict: {
            code:[
                0:通过
                401:token格式错误
            ]
        }
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        #
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError as e:
        print(e.args,e.with_traceback)
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    r = await tools.check_user_exist_by_email(token_data.username)
    if r['code']!=0:
        raise credentials_exception
    return {'code':0,'email':email}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"code": 1, "message": "提交参数错误"})
    )

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    r = await tools.check_user_email_password(email=form_data.username,password=form_data.password)
    if r['code']!=0:
        return r
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {'code':0,"access_token": access_token, "token_type": "bearer"}


@app.get("/v2/")
# async def hello():
async def hello(auto = Depends(get_current_user_by_email)):
    return {'code':"hello"}

@app.get("/v2/getuserinfo")
# async def hello():
async def getuserinfo(auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.get_user_info_by_email(email=email)
    if res['code']!=0:
        return {'code':502,'msg':"获取失败，不存在该用户"}
    user = res['data']['user']
    return {'code':0,'data':{'user':UserInfo(**user)}}

@app.get('/v2/addbind')
async def addbind(bindid:str,password:str,notes:str,auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.add_bind(email=email,bindid=bindid,password=password,notes=notes)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'message':"添加成功"}

@app.get('/v2/getbinds')
async def getbinds(auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.get_binds(email=email)
    if res['code']!=0:
        return {'code':res['code','msg':res['msg']]}
    return {'code':0,'msg':"获取绑定成功",'data':{'binds':res['data']['binds']}}

@app.get('/v2/delbind')
async def delbind(bindid:str,auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res =  await tools.del_bind(email=email,bindid=bindid)
    if res['code']!=0:
        return {'code':res['code','msg':res['msg']]}
    return {'code':0,'msg':"删除绑定成功"}   

@app.get('/v2/gettemplates')
async def gettemplates(auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.get_templates(email=email)
    if res['code']!=0:
        return {'code':res['code','msg':res['msg']]}
    return {'code':0,'msg':"查找模板成功",'data':Templates(templates=res['data']['templates'])}  
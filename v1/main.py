

from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import tool
app = FastAPI()


origins = [
    "http://localhost:3000",
    "localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"code": 1, "message": "提交参数错误"})
    )

@app.get("/v1/reg",tags=["users"])
async def reg(email: EmailStr, open_id: str, password: str):
    r = await tool.check_user_exist(email=email, open_id=open_id)
    if r['code'] != 0:
        return r
    r = await tool.add_user(email=email, open_id=open_id, password=password)
    if r['code'] == 1:
        return r
    return r

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

@app.get('/test_work',tags=['works'])
async def test_work(work_id:int):
    r = await tool.test_work(work_id=work_id)
    if r['code'] !=0:
        return r
    return r


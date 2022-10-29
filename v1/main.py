

from fastapi import FastAPI, status,Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import tool
app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request:Request,exc:RequestValidationError):

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"code":1,"message":"提交参数错误"})
    )

@app.get("/v1/reg")
async def reg(email: EmailStr, open_id: str, password: str) :
    r = await tool.check_user_exist(email=email,open_id=open_id)
    if r['code']!=0:
        return r
    r = await tool.add_user(email=email,open_id=open_id,password=password)
    if r['code']==1:
        return r
    return r

@app.get("/v1/bind")
async def bind(user_id:int,password:str,bind_id:str,bind_password:str):
    r = await tool.check_user_password(user_id=user_id,password=password)
    if r['code']!=0:
        return r
    max_bind = r['data']['user']['max_bind']
    r = await tool.check_bind_user_exist(bind_id=bind_id)
    if r['code']!=0:
        return r
    
    r = await tool.check_bind_number(user_id=user_id,max_bind=max_bind)
    if r['code']!=0:
        return r

    r = await tool.check_bind_user_password(bind_id=bind_id,bind_password=bind_password)
    if r['code']!=0:
        return r
    jwsession = r['data']['jwsession']
    r = await tool.add_bind_user(user_id=user_id,bind_id=bind_id,bind_password=bind_password,jwsession=jwsession)
    if r['code']==1:
        return r
    return {"code":0,"message":'绑定成功'}


@app.get('/v1/delbind')
async def del_bind(user_id:int,password:str,bind_id):
    r = await tool.check_user_password(user_id=user_id,password=password)
    if r['code']!=0:
        return r
    r = await tool.del_bind(bind_id=bind_id)
    if r['code']!=0:
        return r
    return {"code":0,"message":"删除成功"}
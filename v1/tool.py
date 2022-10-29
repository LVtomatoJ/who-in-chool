from typing import Union
import tinydbtool as db
import nettool as net
async def check_user_exist(email:Union[str,None],open_id:Union[str,None])->dict:
    """通过数据库中是否有email和open_id判断是否已经存在该用户
    
    Args:
        email (Union[str,None]): 邮箱
        open_id (Union[str,None]): openid

    Returns:
        dict: 字典中code为1存在反之不存在 message为错误信息
    """
    if email:
        r = db.get_user_by_email(email=email)
        if r['code']!=0:
            return r
        if r['data']['user']!=None:
            # print(r['data']['user'].doc_id)
            return {'code':1,'message':"用户已存在"}
    if open_id:
        r = db.get_user_by_open_id(open_id=open_id)
        if r['code']!=0:
            return r
        if r['data']['user']!=None:
            return {'code':1,'message':"用户已存在"}
    return {'code':0,"message":""}

async def check_bind_user_exist(bind_id:str):
    r = db.get_bind_user_by_bind_id(bind_id=bind_id)
    if r['code']!=0:
        return r
    if r['data']['user']!=None:
        return {'code':1,'message':"用户已存在"}
    return {'code':0,"message":""}

async def check_user_password(user_id:int,password:str)->dict:
    r = db.get_user_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    user = r['data']['user']
    if user==None:
        return {'code':1,"message":"用户不存在"}
    if user['password']!=password:
        return {'code':1,"message":"密码错误"}
    return {"code":0,"message":"",'data':r['data']}   

async def check_bind_user_password(bind_id,bind_password)->dict:
    try:
        r = net.net_login(bind_id=bind_id,bind_password=bind_password)
        code = r['code']
        if code == 0:
            if r['data']['body']['code']!=0:
                return r['data']['body']
            jwsession = r['data']['cookies']['JWSESSION']
            return {'code':0,"message":"网络请求成功","data":{"jwsession":jwsession}}
        else:
            return r
    except Exception as e:
        return {'code':1,"message":"错误:"+str(e)}



async def check_bind_number(user_id:int,max_bind:Union[int,None]):
    if not max_bind:
        r = await get_user_max_bind(user_id=user_id)
        if r['code']!=0:
            return r
        max_bind = r['data']['user']['max_bind']
    r = await get_user_bind_count(user_id=user_id)
    if r['code']!=0:
        return r
    bind_count = r['data']['bind_count']
    if bind_count<max_bind:
        return {'code':0}
    else:
        return {'code':1}

async def get_user_max_bind(user_id:int):
    r = db.get_user_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    user = r['data']['user']
    if user==None:
        return {'code':1,"message":"用户不存在"}
    return {"code":0,"message":"",'data':{'max_bind':r['data']['user']['max_bind']}} 
    

async def get_user_bind_count(user_id:int):
    pass

async def add_user(email:str,open_id:str,password:str):
   return db.insert_user(email=email,open_id=open_id,password=password)

async def add_bind_user(user_id:int,bind_id:str,bind_password:str,jwsession:str):
    return db.insert_bind_user(user_id=user_id,bind_id=bind_id,bind_password=bind_password,jwsession=jwsession)
from typing import Union
import tinydbtool as db
import nettool as net
async def check_user_exist(email:Union[str,None],open_id:Union[str,None])->dict:
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

async def check_template_exist(template_id:int):
    r = db.get_template_by_id(template_id=template_id)
    if r['code']!=0:
        return r
    if r['data']['template']==None:
        return {'code':1,'message':"模板不存在"}
    return {'code':0,"message":"模板存在"}

async def check_bind_user_exist(bind_id:str):
    r = db.get_bind_user_by_bind_id(bind_id=bind_id)
    if r['code']!=0:
        return r
    if r['data']['bind_user']!=None:
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
        r = await get_user_max_count(user_id=user_id)
        if r['code']!=0:
            return r
        max_bind = r['data']['user']['max_bind']
    r = await get_user_bind_count(user_id=user_id)
    if r['code']!=0:
        return r
    bind_count = r['data']['bind_count']
    if bind_count<max_bind:
        return {'code':0,'message':""}
    else:
        return {'code':1,"message":"绑定失败,超出绑定数量限制"}


async def check_work_number(user_id:int,max_work:Union[int,None]):
    if not max_work:
        r = await get_user_max_count(user_id=user_id)
        if r['code']!=0:
            return r
        max_work = r['data']['user']['max_work']
    r = await get_user_work_count(user_id=user_id)
    if r['code']!=0:
        return r
    work_count = r['data']['work_count']
    if work_count<max_work:
        return {'code':0,'message':""}
    else:
        return {'code':1,"message":"添加失败,超出任务数量限制"}


#弃用
async def get_user_max_bind(user_id:int):
    r = db.get_user_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    user = r['data']['user']
    if user==None:
        return {'code':1,"message":"用户不存在"}
    return {"code":0,"message":"",'data':{'max_bind':r['data']['user']['max_bind']}} 

#弃用
async def get_user_max_work(user_id:int):
    r = db.get_user_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    user = r['data']['user']
    if user==None:
        return {'code':1,"message":"用户不存在"}
    return {"code":0,"message":"",'data':{'max_bind':r['data']['user']['max_work']}} 
    
async def get_user_max_count(user_id:int):
    r = db.get_user_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    user = r['data']['user']
    if user==None:
        return {'code':1,"message":"用户不存在"}
    return {"code":0,"message":"",'data':{'max_bind':user['max_work'],'max_bind':user['max_bind']}} 

async def get_user_bind_count(user_id:int):
    r = db.get_bind_users_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    bind_users:list = r['data']['bind_users']
    if bind_users==[]:
        return {"code":0,"message":"",'data':{'bind_count':0}} 
    return {"code":0,"message":"",'data':{'bind_count':len(bind_users)}} 
    
async def get_user_work_count(user_id:int):
    r = db.get_works_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    works:list = r['data']['works']
    if works==[]:
        return {"code":0,"message":"",'data':{'work_count':0}} 
    return {"code":0,"message":"",'data':{'work_count':len(works)}} 

async def get_user_binds(user_id:int):
    r = db.get_bind_users_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    bind_users = r['data']['bind_users']
    return r
    
async def get_user(user_id:int):
    r = db.get_user_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    user = r['data']['user']
    if user==None:
        return {'code':1,"message":"用户不存在"}
    return {"code":0,"message":"",'data':{'user':user}} 

async def get_works(user_id:int):
    r = db.get_works_by_user_id(user_id=user_id)
    if r['code']!=0:
        return r
    works = r['data']['works']
    return {"code":0,"message":"",'data':{'works':works}}    

async def add_user(email:str,open_id:str,password:str):
   return db.insert_user(email=email,open_id=open_id,password=password)

async def add_bind_user(user_id:int,bind_id:str,bind_password:str,jwsession:str):
    return db.insert_bind_user(user_id=user_id,bind_id=bind_id,bind_password=bind_password,jwsession=jwsession)

async def add_work(user_id:int,bind_id:str,time_type:int,work_type:int,state:int,hour:int,minute:int,weektime:int,template_id:int):
    return db.insert_work(user_id=user_id,bind_id=bind_id,time_type=time_type,work_type=work_type,state=state,hour=hour,minute=minute,weektime=weektime,template_id=template_id)


async def del_bind(bind_id:str):
    r = db.del_bind_user(bind_id=bind_id)
    if r['code']!=0:
        return r
    del_bind_users = r["data"]['del_bind_users']
    if del_bind_users==[]:
        return {'code':1,"message":"删除失败，未找到该用户"}
    return {'code':0,"message":"删除成功",'data':{"del_bind_users":del_bind_users}}

async def del_work(work_id:int,user_id:int):
    r = db.del_work(work_id=work_id,user_id=user_id)
    if r['code']!=0:
        return r
    del_works = r["data"]['del_works']
    if del_works==[]:
        return {'code':1,"message":"删除失败，未找到该任务"}
    return {'code':0,"message":"删除成功",'data':{"del_works":del_works}}
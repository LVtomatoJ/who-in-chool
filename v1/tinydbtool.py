
from tinydb import TinyDB,Query


user_db = TinyDB("users.db")
bind_user_db = TinyDB("bind_users.db")
template_db = TinyDB("templates.db")
work_db = TinyDB("works.db")
Querydb = Query()
# template_db.insert({"demo":"132"})
# Bind_User = Query()
def insert_user(email:str,open_id:str,password:str):
    try:
        user_id = user_db.insert({"email":email,'open_id':open_id,'password':password,'max_bind':1,'max_work':1,'level':1})
        return {"code":0,"message":"账户添加成功","data":{'user_id':user_id}}
    except Exception as e:
        return {"code":1,"message":"数据库添加出错"}

def insert_bind_user(user_id:int,bind_id:str,bind_password:str,jwsession:str):
    try:
        bind_doc_id = bind_user_db.insert({"user_id":user_id,'bind_id':bind_id,'bind_password':bind_password,"jwsession":jwsession,"state":0})
        return {"code":0,"message":"绑定用户添加成功","data":{'user_id':bind_doc_id}}
    except Exception as e:
        return {"code":1,"message":"数据库添加出错"}

def insert_work(user_id:int,bind_id:str,time_type:int,work_type:int,state:int,hour:int,minute:int,weektime:int,template_id:int):
    try:
        work_id = work_db.insert({'user_id':user_id,'bind_id':bind_id,'time_type':time_type,'work_type':work_type,'state':state,'hour':hour,'minute':minute,'weektime':weektime,'template_id':template_id})
        return {"code":0,"message":"任务添加成功","data":{'work_id':work_id}}
    except Exception as e:
        return {"code":1,"message":"数据库添加出错"}



def get_user_by_email(email:str):
    try:
        user = user_db.get(Querydb.email==email)
        return  {"code":0,"message":"db查询成功","data":{'user':user}}
    except Exception as e:
        return {"code":1,"message":"数据库查询出错"}

def get_user_by_open_id(open_id:str):
    try:
        user = user_db.get(Querydb.open_id==open_id)
        return  {"code":0,"message":"db查询成功","data":{'user':user}}
    except Exception as e:
        return {"code":1,"message":"数据库查询出错"}

def get_user_by_user_id(user_id:int):
    try:
        user = user_db.get(doc_id=user_id)
        return  {"code":0,"message":"db查询成功","data":{'user':user}}
    except Exception as e:
        return {"code":1,"message":"数据库查询出错"}

def get_bind_user_by_bind_id(bind_id:str):
    try:
        # bind_user = bind_user_db.get(Bind_User.bind_id == bind_id)
        bind_user = bind_user_db.get(Querydb.bind_id==bind_id)
        return  {"code":0,"message":"db查询成功","data":{'bind_user':bind_user}}
    except Exception as e:
        return {"code":1,"message":"数据库查询出错"}

def get_template_by_id(template_id:int):
    try:
        # bind_user = bind_user_db.get(Bind_User.bind_id == bind_id)
        template = template_db.get(doc_id=template_id)
        return  {"code":0,"message":"db查询成功","data":{'template':template}}
    except Exception as e:
        return {"code":1,"message":"数据库查询出错"}   

def get_bind_users_by_user_id(user_id):
    try:
        bind_users = bind_user_db.search(Querydb.user_id==user_id)
        return {'code':0,"message":"db查询成功","data":{"bind_users":bind_users}}
    except Exception as e:
        return {'code':1,"message":"数据库查询出错"}

def get_works_by_user_id(user_id):
    try:
        works = work_db.search(Querydb.user_id==user_id)
        return {'code':0,"message":"db查询成功","data":{"works":works}}
    except Exception as e:
        return {'code':1,"message":"数据库查询出错"}

def del_bind_user(bind_id:str):
    try:
        del_bind_users = bind_user_db.remove(Querydb.bind_id==bind_id)
        return {'code':0,"message":"db删除成功","data":{"del_bind_users":del_bind_users}}
    except Exception as e:
        return {"code":1,"message":"数据库删除出错"}


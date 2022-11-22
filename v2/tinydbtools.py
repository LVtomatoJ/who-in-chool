import random
import string
from tinydb import TinyDB,Query

user_db = TinyDB("main.db").table('users')
bind_db = TinyDB("main.db").table('binds')
template_db = TinyDB("main.db").table('templates')
work_db = TinyDB("main.db").table('works')
bindlog_db = TinyDB("log.db").table('bindlogs')
worklog_db = TinyDB('log.db').table('worklogs')

Querydb = Query()

def check_user_exist_by_email(email:str):
    """检查email对应用户是否存在

    Args:
        email (str): 邮箱
    Returns:
        boolean:用户是否存在
    """
    anser = user_db.contains(Querydb.email==email)
    return anser

def check_user_exist_by_openid(openid:str):
    """检查openid对应用户是否存在

    Args:
        openid (str): wechat_openid
    Returns:
        boolean:用户是否存在
    """
    anser = user_db.contains(Querydb.openid==openid)
    return anser

def check_bind_exist_by_bindid(bindid:str):
    """检查openid对应用户是否存在

    Args:
        openid (str): wechat_openid
    Returns:
        boolean:用户是否存在
    """
    anser = bind_db.contains(Querydb.bindid==bindid)
    return anser


def check_template_exist(templateid:str):
    """检查openid对应用户是否存在

    Args:
        openid (str): wechat_openid
    Returns:
        boolean:用户是否存在
    """
    anser = template_db.contains(Querydb.templateid==templateid)
    return anser

def get_user_by_email(email:str):
    """通过email获取user
    Args:
        email (str): 邮箱

    Returns:
        user
    """
    user = user_db.get(Querydb.email==email)
    return user


def add_user(email:str,password:str,openid:str,level:int,maxbindnum:int,maxworknum:int)->int:
    """添加用户

    Args:
        email (str): 邮箱
        password (str): 密码
        openid (str): wechat_openid
        level (int): 等级
        maxbindnum (int): 最大绑定数量
        maxworknum (int): 最大任务数量
    Returns:
        int: doc_id
    """
    doc_id = user_db.insert({'email':email,'password':password,'openid':openid,'level':level,'maxbindnum':maxbindnum,'maxworknum':maxworknum})
    return doc_id

def add_work(email:str,bindid:str,templateid:str,starttime:str,endtime:str,workid:str)->int:
    doc_id = work_db.insert({'email':email,'bindid':bindid,'templateid':templateid,'status':1,'starttime':starttime,'endtime':endtime,'workid':workid})
    return doc_id


def get_bind_count_by_email(email:str)->int:
    count = bind_db.count(Querydb.email == email)
    return count
def get_work_count_by_email(email:str)->int:
    count = work_db.count(Querydb.email == email)
    return count
def add_bind(email:str,bindid:str,password:str,jwsession:str,notes:str,school:str):
    doc_id = bind_db.insert({'email':email,"bindid":bindid,'password':password,'jwsession':jwsession,'notes':notes,'school':school,'status':1})
    return doc_id

def get_binds(email:str):
    binds = bind_db.search(Querydb.email == email)
    return binds

def get_works(email:str):
    works = work_db.search(Querydb.email == email)
    return works

def del_bind(bindid:str):
    delbinds = bind_db.remove(Querydb.bindid == bindid)
    return delbinds

def del_work(workid:str):
    delworks = work_db.remove(Querydb.workid == workid)
    return delworks

def get_templates():
    templates = template_db.all()
    return templates

def get_bind(bindid:str):
    bind = bind_db.get(Querydb.bindid==bindid)
    return bind

def get_work(workid:str):
    work = work_db.get(Querydb.workid==workid)
    return work

def get_template(templateid:str):
    template = template_db.get(Querydb.templateid==templateid)
    return template

def update_work_status(workid:str,status:int):
    works = work_db.update({'status':status},Querydb.workid==workid)
    return works

def update_bind_status(bindid:str,status:int):
    binds = bind_db.update({'status':status},Querydb.bindid==bindid)
    return binds

def update_bind_jwsession(bindid:str,jwsession):
    binds = bind_db.update({'status':1,"jwsession":jwsession},Querydb.bindid==bindid)

def get_all_works():
    works = work_db.all()
    return works

def add_work_log(email:str,bindid:str,workid:str,templateid:str,time:str,code:int,msg:str):
    doc_id = worklog_db.insert({'email':email,'bindid':bindid,'workid':workid,'templateid':templateid,'time':time,'code':code,'msg':msg})
    return doc_id


def get_work_log(email:str):
    worklogs = worklog_db.search(Querydb.email==email)
    return worklogs


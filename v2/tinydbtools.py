import random
import string
from tinydb import TinyDB,Query

user_db = TinyDB("main.db").table('users')
bind_db = TinyDB("main.db").table('binds')
template_db = TinyDB("main.db").table('templates')
work_db = TinyDB("main.db").table('works')

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



def get_bind_count_by_email(email:str)->int:
    count = bind_db.count(Querydb.email == email)
    return count

def add_bind(email:str,bindid:str,password:str,jwsession:str,notes:str,school:str):
    doc_id = bind_db.insert({'email':email,"bindid":bindid,'password':password,'jwsession':jwsession,'notes':notes,'school':school,'status':1})
    return doc_id

def get_binds(email:str):
    binds = bind_db.search(Querydb.email == email)
    return binds

def del_bind(bindid:str):
    delbinds = bind_db.remove(Querydb.bindid == bindid)
    return delbinds

def get_templates():
    templates = template_db.all()
    return templates
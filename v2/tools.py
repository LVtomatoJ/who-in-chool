import tinydbtools as dbtools


async def check_user_exist_by_email(email:str)->bool:
    """检查是否存在email对应用户

    Args:
        email (str): 邮箱

    Returns:
        bool: {
            code:[0:存在,502:不存在用户]
        }
    """
    if dbtools.check_user_exist_by_email(email=email):
        return {'code':0}
    return {'code':502}

async def check_user_exist_by_openid(openid:str)->bool:
    """检查是否存在openid对应用户

    Args:
        openid (str): wechat_openid

    Returns:
        bool: {
            code:[0:存在,502:不存在用户]
        }
    """
    if dbtools.check_user_exist_by_openid(openid=openid):
        return {'code':0}
    return {'code':502}
    


async def check_user_email_password(email:str,password:str):
    """检查email对应用户的password是否正确

    Args:
        email (str): 邮箱
        password (str): 密码

    Returns:
        dict: {
            code:[0:成功,502:不存在用户,402:密码错误]
        }
    """
    # # 是否存在
    # if not dbtools.check_user_exist_by_email(email):
    #     return {'code':502}
    # 获取用户信息
    user = dbtools.get_user_by_email(email)
    # code = r['code']
    # if not code == 0:
    #     return {'code':code}
    # user = r['data']['user']
    if not user:
        return {'code':502}
    if user['password']!=password:
        return {'code':402}
    return {'code':0}
    

async def add_default_user(email:str,password:str,openid:str)->dict:
    """添加默认用户 （等级1 绑定1 任务1）
    Args:
        email (str): 邮箱
        password (str): 密码
        open_id (str): wechat_openid

    Returns:
        dict: {code:[0:成功,403:已存在用户]}
    """
    #存在则不添加
    if dbtools.check_user_exist_by_email(email=email) or dbtools.check_user_exist_by_openid(openid=openid):
        return {'code':403}
    doc_id = dbtools.add_user(email=email,password=password,openid=openid,level=1,maxbindnum=1,maxworknum=1)
    return {'code:':0}

# print(add_default_user('992203755@qq.com','123','lvtomato'))

async def get_user_info_by_email(email:str):
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        return {'code':502}
    return {'code':0,'data':{'user':user}}
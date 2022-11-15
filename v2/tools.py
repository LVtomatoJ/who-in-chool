import tinydbtools as dbtools
import nettolls

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

async def add_bind(email:str,bindid:str,password:str,notes:str):
    """添加绑定

    Args:
        email (str): 邮箱
        bindid (str): 绑定id
        password (str): 绑定密码
        jwsession (str): session

    Returns:
        dict: {code:[
            0:成功
            502:用户不存在
            404:绑定用户达上线
            405:绑定用户已存在
        ]}
    """
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        return {'code':502,'msg':'用户不存在'}
    maxbindnum = user['maxbindnum']
    bindcount = dbtools.get_bind_count_by_email(email=email)
    if bindcount >= maxbindnum:
        return {'code':404,'msg':"绑定用户达到上限"}
    if dbtools.check_bind_exist_by_bindid(bindid=bindid):
        return {'code':405,'msg':"绑定用户已存在"}
    res = nettolls.getJwsession(bindid=bindid,password=password)
    code = res['code']
    if code!=0:
        if code==405:
            return {'code':405,'msg':res['msg']}
        else:
            return {'code':503,'msg':'网络请求失败'}
    jwsession = res['data']['jwsession']
    res = nettolls.getSchool(jwsession=jwsession)
    if code!=0:
        return {'code':res['code'],'msg':res['msg']}
    school = res['data']['school']
    doc_id = dbtools.add_bind(email=email,bindid=bindid,password=password,jwsession=jwsession,notes=notes,school=school)
    return {'code':0}

async def get_binds(email:str):
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        return {'code':502,'msg':"用户不存在"}
    users = dbtools.get_binds(email=email)
    return {'code':0,'data':{'binds':users}}

async def del_bind(email:str,bindid:str):
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        return {'code':502,'msg':"用户不存在"}
    if not dbtools.check_bind_exist_by_bindid(bindid=bindid):
        return {'code':406,"msg":"绑定用户不存在"}
    delbinds = dbtools.del_bind(bindid=bindid)
    if delbinds==[]:
        return {'code':504,'msg':"删除结果为空"}
    return {'code':0}

async def get_templates(email:str):
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        return {'code':502,'msg':"用户不存在"}
    templates = dbtools.get_templates()
    return {'code':0,'data':{'templates':templates}}
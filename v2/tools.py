import random
import string
from typing import Union
import tinydbtools as dbtools
import nettolls
from apscheduler.schedulers.background import BackgroundScheduler
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
    if user==None:
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

async def get_works(email:str):
    if not dbtools.check_user_exist_by_email(email=email):
        return {'code':502,'msg':'用户不存在'}
    works = dbtools.get_works(email=email)
    return {'code':0,'data':{'works':works}}

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

async def del_work(email:str,workid:str):
    if not dbtools.check_user_exist_by_email(email=email):
        return {'code':502,'msg':'用户不存在'}
    work = dbtools.get_work(workid=workid)
    if work==None:
        return {'code':410,'msg':"不存在任务"}
    if work['email']!=email:
        return {'code':409,'msg':"权限不足"}
    delworks = dbtools.del_work(workid=workid)
    if delworks==[]:
        return {'code':504,'msg':"删除结果为空"}
    return {'code':0}

async def update_work_status(email:str,workid:str,status:int,scheduler:Union[BackgroundScheduler,None]=None):
    if not dbtools.check_user_exist_by_email(email=email):
        return {'code':502,'msg':'用户不存在'}
    work = dbtools.get_work(workid=workid)
    if work==None:
        return {'code':410,'msg':"不存在任务"}
    if work['email']!=email:
        return {'code':409,'msg':"权限不足"}
    if status==1:
        if scheduler.get_job(job_id=workid)==None:
            
            scheduler.resume_job(job_id=workid)
            return {'code':0}
    updateworks = dbtools.update_work_status(workid=workid,status=status)
    if updateworks==[]:
        return {'code':507,'msg':"更新结果为空"}
    return {'code':0}


async def get_templates(email:str):
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        return {'code':502,'msg':"用户不存在"}
    templates = dbtools.get_templates()
    return {'code':0,'data':{'templates':templates}}




async def quick_work(email:str,templateid:str,bindid:str):
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        return {'code':502,'msg':"用户不存在"}
    # if not dbtools.check_bind_exist_by_bindid(bindid=bindid):
    #     return {'code':406,"msg":"绑定用户不存在"}
    # if not dbtools.check_bind_exist_by_bindid(bindid=bindid):
    #     return {'code':406,"msg":"绑定用户不存在"}
    # if not dbtools.check_template_exist(templateid=templateid)
    #     return {'code':407,'msg':"模板不存在"}

    bind = dbtools.get_bind(bindid=bindid)
    template = dbtools.get_template(templateid=templateid)
    if bind==None:
        return {'code':406,'msg':'绑定用户不存在'}
    if template==None:
        return {'code':407,'msg':"模板不存在"}
    data=template['data']
    jwsession=bind['jwsession']
    res = nettolls.doHeat(jwsession=jwsession,data=data)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"任务执行成功"}



def printhaha():
    print('hahahah')


def long_work(email:str,bindid:str,templateid:str,workid:str):

    #不存在任务直接停止
    work = dbtools.get_work(workid=workid)
    if work==None:
        return

    #参数缺失 删除任务后停止
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        r = dbtools.del_work(workid=workid)
        #add log
        return
    bind = dbtools.get_bind(bindid=bindid)
    if bind==None:
        r = dbtools.del_work(workid=workid)
        #add log
        return
    template = dbtools.get_template(templateid=templateid)
    if template==None:
        r = dbtools.del_work(workid=workid)
        #add log
        return

    # print("3")
    # print(workid)
    # work = dbtools.get_work(workid=workid)
    # print(work)

    #任务状态不为1 停止
    if work['status']!=1:
        return 

    data=template['data']
    jwsession=bind['jwsession']
    res = nettolls.doHeat(jwsession=jwsession,data=data)
    code = res['code']
    if code!=0:
        #失败操作
        if code==505:
            #bind status 2：失效
            dbtools.update_bind_status(bindid=bindid,status=2)
            #work status 2:暂停
            dbtools.update_work_status(workid=workid,status=2)
            #add log
            return
        else:
            dbtools.update_work_status(workid=workid,status=2)
            #add log
            return

    #add success log
    print('yes!')
    

async def add_work(email:str,bindid:str,templateid:str,scheduler:BackgroundScheduler,starttime:str,endtime:str):
    user = dbtools.get_user_by_email(email=email)
    if user==None:
        return {'code':502,'msg':"用户不存在"}
    bind = dbtools.get_bind(bindid=bindid)
    template = dbtools.get_template(templateid=templateid)
    if bind==None:
        return {'code':406,'msg':'绑定用户不存在'}
    if template==None:
        return {'code':407,'msg':"模板不存在"}
    maxbindnum:int = user['maxbindnum']
    workcount = dbtools.get_work_count_by_email(email=email)
    if maxbindnum<=workcount:
        return {'code':408,'msg':"任务数量超过限制"}
    workid= ''.join(random.sample(string.ascii_letters + string.digits, 10))
    docid = dbtools.add_work(email=email,bindid=bindid,templateid=templateid,starttime=starttime,endtime=endtime,workid=workid)
    job = scheduler.add_job(long_work,args=(email,bindid,templateid,workid,),trigger='interval',minutes=1,start_date=starttime,end_date=endtime,id=workid)
    return {'code':0}
    
    
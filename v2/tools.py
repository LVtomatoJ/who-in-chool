import json
import random
import string
import time
from typing import Union
import tinydbtools as dbtools
import nettolls
from apscheduler.schedulers.background import BackgroundScheduler
import mail
from default import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import datetime, timedelta


async def check_user_exist_by_email(email: str) -> bool:
    """检查是否存在email对应用户

    Args:
        email (str): 邮箱

    Returns:
        bool: {
            code:[0:存在,502:不存在用户]
        }
    """
    if dbtools.check_user_exist_by_email(email=email):
        return {'code': 0}
    return {'code': 502}


async def check_user_exist_by_openid(openid: str) -> bool:
    """检查是否存在openid对应用户

    Args:
        openid (str): wechat_openid

    Returns:
        bool: {
            code:[0:存在,502:不存在用户]
        }
    """
    if dbtools.check_user_exist_by_openid(openid=openid):
        return {'code': 0}
    return {'code': 502, 'msg': "不存在用户"}


async def check_user_email_password(email: str, password: str):
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
    if user == None:
        return {'code': 502}
    if user['password'] != password:
        return {'code': 402}
    return {'code': 0}


async def add_default_user(email: str, password: str, openid: str) -> dict:
    """添加默认用户 （等级1 绑定1 任务1）
    Args:
        email (str): 邮箱
        password (str): 密码
        open_id (str): wechat_openid
    Returns:
        dict: {code:[0:成功,403:已存在用户]}
    """
    # 存在则不添加
    if dbtools.check_user_exist_by_email(email=email) or dbtools.check_user_exist_by_openid(openid=openid):
        return {'code': 403}
    doc_id = dbtools.add_user(email=email, password=password,
                              openid=openid, level=1, maxbindnum=1, maxworknum=1)
    return {'code:': 0}

# print(add_default_user('992203755@qq.com','123','lvtomato'))


async def get_user_info_by_email(email: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502}
    return {'code': 0, 'data': {'user': user}}


async def add_bind(email: str, bindid: str, password: str, notes: str):
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
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    maxbindnum = user['maxbindnum']
    bindcount = dbtools.get_bind_count_by_email(email=email)
    if bindcount >= maxbindnum:
        return {'code': 404, 'msg': "绑定用户达到上限"}
    if dbtools.check_bind_exist_by_bindid(bindid=bindid):
        return {'code': 405, 'msg': "绑定用户已存在"}
    res = nettolls.getJwsession(bindid=bindid, password=password)
    code = res['code']
    if code != 0:
        if code == 405:
            return {'code': 405, 'msg': res['msg']}
        else:
            return {'code': 503, 'msg': '网络请求失败'}
    jwsession = res['data']['jwsession']
    res = nettolls.getSchool(jwsession=jwsession)
    if code != 0:
        return {'code': res['code'], 'msg': res['msg']}
    school = res['data']['school']
    doc_id = dbtools.add_bind(email=email, bindid=bindid, password=password,
                              jwsession=jwsession, notes=notes, school=school)
    return {'code': 0}


async def rebind(email: str, bindid: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    bind = dbtools.get_bind(bindid=bindid)
    if bind == None:
        return {'code': 406, "msg": "绑定用户不存在"}
    if bind['email'] != email:
        return {'code': 409, "msg": "权限不足"}

    password = bind["password"]
    bindid = bind['bindid']
    res = nettolls.getJwsession(bindid=bindid, password=password)
    if res['code'] != 0:
        return {'code': res['code'], 'msg': res['msg']}
    jwsession = res['data']['jwsession']
    newbind = dbtools.update_bind_jwsession(bindid=bindid, jwsession=jwsession)
    return {'code': 0, 'msg': "更新绑定成功"}


async def get_binds(email: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    users = dbtools.get_binds(email=email)
    return {'code': 0, 'data': {'binds': users}}


async def get_works(email: str):
    if not dbtools.check_user_exist_by_email(email=email):
        return {'code': 502, 'msg': '用户不存在'}
    works = dbtools.get_works(email=email)
    return {'code': 0, 'data': {'works': works}}


async def get_all_users(email: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    users = dbtools.get_all_users()
    return {'code': 0, 'msg': "查询所有用户成功", 'data': {'users': users}}


async def get_all_notics(email: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    notics = dbtools.get_all_notics()
    return {'code': 0, 'msg': "查询所有用户成功", 'data': {'notics': notics}}


async def get_all_binds(email: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    binds = dbtools.get_all_binds()
    return {'code': 0, 'msg': "查询所有用户成功", 'data': {'binds': binds}}


async def get_all_works(email: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    works = dbtools.get_all_works()
    return {'code': 0, 'msg': "查询所有任务成功", 'data': {'works': works}}


async def get_notics():
    notics = dbtools.get_notics()
    return {'code': 0, 'data': {'notics': notics}}


async def admin_change_user(myemail: str, email: str, password: str, openid: str, level: int, maxbindnum: int, maxworknum: int):
    user = dbtools.get_user_by_email(email=myemail)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    users: list = dbtools.change_user(
        email=email, password=password, openid=openid, level=level, maxbindnum=maxbindnum, maxworknum=maxworknum)
    if len(user) > 0:
        return {'code': 0, 'msg': "更新成功"}
    else:
        return {'code': 507, 'msg': "更新结果为空"}


async def admin_change_work(myemail: str, email: str, workid: str, templateid: str, bindid: str, status: int, starttime: str, endtime: str):
    user = dbtools.get_user_by_email(email=myemail)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    works: list = dbtools.change_work(email=email, workid=workid, templateid=templateid,
                                      bindid=bindid, status=status, starttime=starttime, endtime=endtime)
    if len(works) > 0:
        return {'code': 0, 'msg': "更新成功"}
    else:
        return {'code': 507, 'msg': "更新结果为空"}


async def admin_change_bind(myemail: str, email: str, password: str, jwsession: str, notes: str, school: str, status: int, bindid: str):
    user = dbtools.get_user_by_email(email=myemail)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    users: list = dbtools.change_bind(
        email=email, password=password, jwsession=jwsession, notes=notes, school=school, status=status, bindid=bindid)
    if len(user) > 0:
        return {'code': 0, 'msg': "更新成功"}
    else:
        return {'code': 507, 'msg': "更新结果为空"}


async def admin_change_notic(email: str, title: str, content: str, time: str, show: int, noticid: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    notics: list = dbtools.change_notic(
        noticid=noticid, title=title, content=content, show=show, time=time)
    if len(notics) > 0:
        return {'code': 0, 'msg': "更新成功"}
    else:
        return {'code': 507, 'msg': "更新结果为空"}


async def admin_add_notic(email: str, title: str, content: str, time: str, show: int, noticid: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': '用户不存在'}
    level = user['level']
    if level != 999:
        return {'code': 409, 'msg': "权限不足"}
    docid = dbtools.add_notic(
        noticid=noticid, title=title, content=content, show=show, time=time)
    return {'code': 0, 'msg': "更新成功"}


async def del_bind(email: str, bindid: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    if not dbtools.check_bind_exist_by_bindid(bindid=bindid):
        return {'code': 406, "msg": "绑定用户不存在"}
    delbinds = dbtools.del_bind(bindid=bindid)
    if delbinds == []:
        return {'code': 504, 'msg': "删除结果为空"}
    return {'code': 0}


async def del_work(email: str, workid: str):
    if not dbtools.check_user_exist_by_email(email=email):
        return {'code': 502, 'msg': '用户不存在'}
    work = dbtools.get_work(workid=workid)
    if work == None:
        return {'code': 410, 'msg': "不存在任务"}
    if work['email'] != email:
        return {'code': 409, 'msg': "权限不足"}
    delworks = dbtools.del_work(workid=workid)
    if delworks == []:
        return {'code': 504, 'msg': "删除结果为空"}
    return {'code': 0}


async def update_work_status(email: str, workid: str, status: int, scheduler: Union[BackgroundScheduler, None] = None):
    if not dbtools.check_user_exist_by_email(email=email):
        return {'code': 502, 'msg': '用户不存在'}
    work = dbtools.get_work(workid=workid)
    if work == None:
        return {'code': 410, 'msg': "不存在任务"}
    if work['email'] != email:
        return {'code': 409, 'msg': "权限不足"}
    if status == 1:
        if scheduler.get_job(job_id=workid) == None:

            scheduler.resume_job(job_id=workid)
            return {'code': 0}
    updateworks = dbtools.update_work_status(workid=workid, status=status)
    if updateworks == []:
        return {'code': 507, 'msg': "更新结果为空"}
    return {'code': 0}


async def get_templates(email: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    templates = dbtools.get_templates()
    return {'code': 0, 'data': {'templates': templates}}


async def quick_work(email: str, templateid: str, bindid: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    # if not dbtools.check_bind_exist_by_bindid(bindid=bindid):
    #     return {'code':406,"msg":"绑定用户不存在"}
    # if not dbtools.check_bind_exist_by_bindid(bindid=bindid):
    #     return {'code':406,"msg":"绑定用户不存在"}
    # if not dbtools.check_template_exist(templateid=templateid)
    #     return {'code':407,'msg':"模板不存在"}

    bind = dbtools.get_bind(bindid=bindid)
    template = dbtools.get_template(templateid=templateid)
    if bind == None:
        return {'code': 406, 'msg': '绑定用户不存在'}
    if template == None:
        return {'code': 407, 'msg': "模板不存在"}
    data = template['data']
    jwsession = bind['jwsession']
    res = nettolls.doHeat(jwsession=jwsession, data=data)
    if res['code'] != 0:
        return {'code': res['code'], 'msg': res['msg']}
    return {'code': 0, 'msg': "任务执行成功"}


def long_work(email: str, bindid: str, templateid: str, workid: str):

    # 不存在任务直接停止
    work = dbtools.get_work(workid=workid)
    if work == None:
        return
    # 参数缺失 删除任务后停止
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        r = dbtools.del_work(workid=workid)
        # add log
        docid = dbtools.add_work_log(email=email, bindid=bindid, workid=workid, templateid=templateid, time=time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), code=502, msg="定时任务执行失败【用户不存在】,已暂停运行")
        mail.send_async_mail_prepare(title='【谁在校园】您有任务失败啦，快去日志检查检查吧',content="", user_email=email)
        return
    bind = dbtools.get_bind(bindid=bindid)
    if bind == None:
        r = dbtools.del_work(workid=workid)
        # add log
        docid = dbtools.add_work_log(email=email, bindid=bindid, workid=workid, templateid=templateid, time=time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), code=406, msg="定时任务执行失败【绑定用户不存在】,已暂停运行")
        mail.send_async_mail_prepare(
            title='【谁在校园】您有任务失败啦，快去日志检查检查吧', content='', user_email=email)
        return
    template = dbtools.get_template(templateid=templateid)
    if template == None:
        r = dbtools.del_work(workid=workid)
        # add log
        docid = dbtools.add_work_log(email=email, bindid=bindid, workid=workid, templateid=templateid, time=time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), code=407, msg="定时任务执行失败【模板不存在】,已暂停运行")
        mail.send_async_mail_prepare(
            title='【谁在校园】您有任务失败啦，快去日志检查检查吧', content='', user_email=email)
        return

    # print("3")
    # print(workid)
    # work = dbtools.get_work(workid=workid)
    # print(work)

    # 任务状态不为1 停止
    if work['status'] != 1:
        return

    data = template['data']
    
    res = nettolls.getJwsession(bindid,bind['password'])
    code = res['code']
    if code != 0:
        if code == 405:
            return {'code': 405, 'msg': res['msg']}
        else:
            return {'code': 503, 'msg': '网络请求失败'}
    else:
        jwsession = res['data']['jwsession']
        print(jwsession)
        res = nettolls.doHeat(jwsession=jwsession, data=data)
        code = res['code']
        if code != 0:
            # 失败操作
            if code == 505:
                # bind status 2：失效
                dbtools.update_bind_status(bindid=bindid, status=2)
                # work status 2:暂停
                dbtools.update_work_status(workid=workid, status=2)
                # add log
                docid = dbtools.add_work_log(email=email, bindid=bindid, workid=workid, templateid=templateid, time=time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), code=505, msg="定时任务执行失败【绑定失效】,已暂停运行")
                mail.send_async_mail_prepare(
                    title='【谁在校园】您有任务失败啦，快去日志检查检查吧', content='', user_email=email)
                return
            else:
                dbtools.update_work_status(workid=workid, status=2)
                docid = dbtools.add_work_log(email=email, bindid=bindid, workid=workid, templateid=templateid, time=time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), code=code, msg="定时任务执行失败【"+res['msg']+"】,已暂停运行")
                mail.send_async_mail_prepare(
                    title='【谁在校园】您有任务失败啦，快去日志检查检查吧', content='', user_email=email)
                return
        # 执行成功
        docid = dbtools.add_work_log(email=email, bindid=bindid, workid=workid, templateid=templateid, time=time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), code=0, msg="定时任务执行成功")
        return


async def add_work(email: str, bindid: str, templateid: str, scheduler: BackgroundScheduler, starttime: str, endtime: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    bind = dbtools.get_bind(bindid=bindid)
    template = dbtools.get_template(templateid=templateid)
    if bind == None:
        return {'code': 406, 'msg': '绑定用户不存在'}
    if template == None:
        return {'code': 407, 'msg': "模板不存在"}
    maxbindnum: int = user['maxbindnum']
    workcount = dbtools.get_work_count_by_email(email=email)
    if maxbindnum <= workcount:
        return {'code': 408, 'msg': "任务数量超过限制"}
    workid = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    docid = dbtools.add_work(email=email, bindid=bindid, templateid=templateid,
                             starttime=starttime, endtime=endtime, workid=workid)
    try:
        job = scheduler.add_job(long_work, args=(email, bindid, templateid, workid,),
                            trigger='interval', hours=24, start_date=starttime, end_date=endtime, id=workid)
    except Exception as e:
        dbtools.del_work(workid=workid)
        return {'code':412,'msg':"添加任务失败"}
    docid = dbtools.add_work_log(email=email, bindid=bindid, workid=workid, templateid=templateid, time=time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), code=0, msg="添加任务成功")
    return {'code': 0}


async def get_worklogs(email: str):
    if not dbtools.check_user_exist_by_email(email=email):
        return {'code': 502, 'msg': "用户不存在"}
    worklogs = dbtools.get_work_log(email=email)
    return {'code': 0, 'data': {'worklogs': worklogs}}


async def do_latest_sign(email: str, bindid: str, templateid: str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    bind = dbtools.get_bind(bindid=bindid)
    template = dbtools.get_template(templateid=templateid)
    if bind == None:
        return {'code': 406, 'msg': '绑定用户不存在'}
    if template == None:
        return {'code': 407, 'msg': "模板不存在"}
    if bind['email'] != email:
        return {'code': 409, 'msg': "权限不足"}
    jwsession = bind['jwsession']
    r = nettolls.getSignList(jwsession=jwsession)
    if r['code'] != 0:
        return {'code': r['code'], 'msg': r['msg']}
    latestsign = r['data']['signlist'][0]
    id = latestsign['id']
    logId = latestsign['logId']
    data = template['data']
    data['signId'] = id
    data['id'] = logId
    res = nettolls.doSign(
        jwsession=jwsession, data=data)
    if r['code'] != 0:
        return {'code': r['code'], 'msg': r['msg']}
    return {'code': 0, 'msg': "签到成功"}

#已失效
async def custom_sign(email: str, bindid:str,city:str,longitude:str,country:str,district:str,township:str,latitude:str,province:str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    bind = dbtools.get_bind(bindid=bindid)
    if bind == None:
        return {'code': 406, 'msg': '绑定用户不存在'}
    if bind['email'] != email:
        return {'code': 409, 'msg': "权限不足"}
    jwsession = bind['jwsession']
    r = nettolls.getSignList(jwsession=jwsession)
    if r['code'] != 0:
        return {'code': r['code'], 'msg': r['msg']}
    latestsign = r['data']['signlist'][0]
    id = latestsign['id']
    logId = latestsign['logId']
    data = {
        "signId": id ,
        "city": city,
        "longitude":longitude,
        "id": logId,
        "country": country,
        "district": district,
        "township": township,
        "latitude": latitude,
        "province": province}
    res = nettolls.doSign(
        jwsession=jwsession, data=data)
    if r['code'] != 0:
        return {'code': r['code'], 'msg': r['msg']}
    return {'code': 0, 'msg': "签到成功"}


async def custom_sign_v2(email: str, bindid:str,city:str,longitude:str,country:str,district:str,township:str,latitude:str,province:str,nationcode:str,adccode:str,streetcode:str,citycode:str,towncode:str,street:str):
    user = dbtools.get_user_by_email(email=email)
    if user == None:
        return {'code': 502, 'msg': "用户不存在"}
    bind = dbtools.get_bind(bindid=bindid)
    if bind == None:
        return {'code': 406, 'msg': '绑定用户不存在'}
    if bind['email'] != email:
        return {'code': 409, 'msg': "权限不足"}
    jwsession = bind['jwsession']
    r = nettolls.getSignList_v2(jwsession=jwsession)
    if r['code'] != 0:
        return {'code': r['code'], 'msg': r['msg']}
    latestsign = r['data'][0]
    id = latestsign['id']
    signId = latestsign['signId']
    schoolId = latestsign['schoolId']
    area = r['data'][1]['areaList'][0]
    data = {
        "city": city,
        "longitude":longitude,
        "country": country,
        "district": district,
        "township": township,
        "latitude": latitude,
        "province": province,
        "nationcode":nationcode,
        "citycode":citycode,
        'adccode':adccode,
        'towncode':towncode,
        'streetcode':streetcode,
        'street':street,
        'inArea':1,
        'areaJSON':json.dumps({"type":area["shape"],"circle":{'latitude':area['latitude'],'longitude':area['longitude'],'radius':area['radius']},'id':area['id'],'name':area['name']})
        }
    res = nettolls.doSign_v2(
        jwsession=jwsession, data=data,schoolId=schoolId,id=id,signId=signId)
    if r['code'] != 0:
        return {'code': r['code'], 'msg': r['msg']}
    return {'code': 0, 'msg': "签到成功"}

async def minilogin(code: str):
    r = nettolls.getOpenid(code=code)
    if r['code'] != 0:
        return {'code': r['code'], 'msg': r['msg']}
    openid = r['data']['openid']
    if not dbtools.check_user_exist_by_openid(openid=openid):
        return {'code': 502, 'msg': "不存在用户"}
    user = dbtools.get_user_by_openid(openid=openid)
    email = user['email']

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    # if not dbtools.check_user_exist_by_openid(openid=openid):
    #     return {'code':0}
    # return {'code':502,'msg':"不存在用户"}
    return {'code': 0, 'msg': "登录成功", 'data': {"access_token": access_token, "token_type": "bearer"}}


async def minireg(code: str, email: str, password: str):
    r = nettolls.getOpenid(code=code)
    if r['code'] != 0:
        return {'code': r['code'], 'msg': r['msg']}
    openid = r['data']['openid']
    if dbtools.check_user_exist_by_openid(openid=openid):
        return {'code': 403, 'msg': "已存在用户"}
    if dbtools.check_user_exist_by_email(email=email):
        return {'code': 403, 'msg': "已存在用户"}
    doc_id = dbtools.add_user(email=email, password=password,
                              openid=openid, level=1, maxbindnum=1, maxworknum=1)
    return {'code': 0, 'msg': "用户注册成功"}

# 不安全


async def check_reg(openid: str):
    if not dbtools.check_user_exist_by_openid(openid=openid):
        return {'code': 502, 'msg': "不存在用户"}
    user = dbtools.get_user_by_openid(openid=openid)
    email = user['email']

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return {'code': 0, 'msg': '用户已注册', 'data': {"access_token": access_token, "token_type": "bearer"}}



long_work(email="992203755@qq.com", bindid="15389064060", templateid="1aLiX", workid="Dn1eO6iQXM")
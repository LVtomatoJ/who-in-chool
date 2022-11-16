from datetime import datetime, timedelta
import time
from typing import List, Optional, Union
from fastapi import FastAPI, status, Request,Depends,HTTPException,Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.job import Job
import tools
import tinydbtools as dbtool
app = FastAPI()



def init_jobs(jobs:List[Job]):
    works_dict = dict()
    works:List[dict] = dbtool.get_all_works()
    for work in works:
        works_dict[work['workid']] = work['status']
    workids = works_dict.keys()
    for job in jobs:
        jobid = job.id
        print("runtime:")
        print(job.next_run_time)
        if jobid not in workids:
            job.remove()
            continue
        if works_dict[jobid]==2:
            job.pause()
            continue
        if works_dict[jobid]==1:
            job.resume()
            continue
        
    


@app.on_event('startup')
def init_scheduler():
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    global scheduler
    
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores=jobstores)
    scheduler.start()
    jobs = scheduler.get_jobs()
    init_jobs(jobs=jobs)
    scheduler.print_jobs()
    

class UserInfo(BaseModel):
    email:str
    openid:str
    level:int
    maxbindnum:int
    maxworknum:int

class Template(BaseModel):
    
    templateid:str
    name:str
    status:int
    school:str

class Templates(BaseModel):
    templates:list[Template]


# origins = [
#     "http://localhost:3333",
#     "localhost:3333"
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

origins = [
    "http://localhost",
    "http://localhost:3333",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:3333",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY ='5d8788a74ba363c1b08329363b42f30c75d3cb762714aa32761cb0e214b5474d'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_by_email(token: str = Depends(oauth2_scheme)): 
    """验证token[email]

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).

    Returns:
        dict: {
            code:[
                0:通过
                401:token格式错误
            ]
        }
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        #
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError as e:
        print(e.args,e.with_traceback)
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    r = await tools.check_user_exist_by_email(token_data.username)
    if r['code']!=0:
        raise credentials_exception
    return {'code':0,'email':email}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"code": 1, "message": "提交参数错误"})
    )

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    # print("11111")
    # print('username:'+form_data.username)
    # print("password:"+form_data.password)

    r = await tools.check_user_email_password(email=form_data.username,password=form_data.password)
    if r['code']!=0:
        return r
    print(r)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {'code':0,"access_token": access_token, "token_type": "bearer"}


@app.get("/v2/")
# async def hello():
async def hello(auto = Depends(get_current_user_by_email)):
    return {'code':"hello"}

@app.get("/v2/getuserinfo")
# async def hello():
async def getuserinfo(auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.get_user_info_by_email(email=email)
    if res['code']!=0:
        return {'code':502,'msg':"获取失败，不存在该用户"}
    user = res['data']['user']
    return {'code':0,'data':{'user':UserInfo(**user)}}

@app.get('/v2/addbind')
async def addbind(bindid:str,password:str,notes:str,auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.add_bind(email=email,bindid=bindid,password=password,notes=notes)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'message':"添加成功"}

@app.get('/v2/getbinds')
async def getbinds(auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.get_binds(email=email)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"获取绑定成功",'data':{'binds':res['data']['binds']}}

@app.get('/v2/delbind')
async def delbind(bindid:str,auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res =  await tools.del_bind(email=email,bindid=bindid)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"删除绑定成功"}   

@app.get('/v2/delwork')
async def delwork(workid:str,auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res =  await tools.del_work(email=email,workid=workid)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"删除任务成功"}  

@app.get('/v2/updateworkstatus') 
async def updatework(workid:str,status:int,auth = Depends(get_current_user_by_email)):
    email = auth['email']
    if status not in [1,2]:
        return {'code':1,'msg':"提交参数错误"}

    if status==1:
        global scheduler
        res =  await tools.update_work_status(email=email,workid=workid,status=status,scheduler=scheduler)
    else:
        res =  await tools.update_work_status(email=email,workid=workid,status=status)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"更新任务状态成功"}

@app.get('/v2/gettemplates')
async def gettemplates(auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.get_templates(email=email)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"查找模板成功",'data':Templates(templates=res['data']['templates'])}  

@app.get('/v2/quickwork')
async def quckwork(bindid:str,templateid:str,auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.quick_work(email=email,templateid=templateid,bindid=bindid)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"任务执行成功"}  

@app.get('/v2/addwork')
async def addwork(bindid:str,templateid:str,starttime:str,endtime:str,auth = Depends(get_current_user_by_email)):
    email = auth['email']
    global scheduler
    res = await tools.add_work(email=email,bindid=bindid,templateid=templateid,scheduler=scheduler,starttime=starttime,endtime=endtime)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"任务添加成功"}  

@app.get('/v2/getworks')
async def getworkd(auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.get_works(email=email)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"任务获取成功",'data':{'works':res['data']['works']}}   


@app.get('/v2/getallworks')
async def printallworks():
    global scheduler
    scheduler.print_jobs()
    return{0}


@app.get('/v2/getworklogs')
async def getworks(auth = Depends(get_current_user_by_email)):
    email = auth['email']
    res = await tools.get_worklogs(email=email)
    if res['code']!=0:
        return {'code':res['code'],'msg':res['msg']}
    return {'code':0,'msg':"任务日志获取成功",'data':{'worklogs':res['data']['worklogs']}}   

# def printtime(name:str):
#     print("lalala")
#     return 0
# @app.get('/addwork')
# async def addwork():
#     global scheduler
#     scheduler.add_job(printtime,'cron',minutes=1)
#     return {"ok":'ok'}

# @app.get('/addwork')
# async def addwork():
#     global scheduler
#     job = scheduler.add_job(printtime,'interval',hours=2,minutes=1,jitter=60,args=[data, ])
#     return {"jobid":job.id}
from pydantic import BaseModel


class SchoolInfo(BaseModel):
    id: str
    isActive: int
    logo: str
    name: str


class SchoolListResp(BaseModel):
    data: list[dict]


class LoginResp(BaseModel):
    token: str


class AreaInfo(BaseModel):
    id: str
    latitude: str
    longitude: str
    name: str


class SignInfo(BaseModel):
    id: str
    signId: str
    signTitle: str
    createCollege: str
    teacher: str
    signMode: int  # 1是校区签到 2是定位签到
    start: int  # 开始时间
    end: int  # 结束时间
    signContext: str
    signStatus: int
    areaList: list[AreaInfo] = None  # 如果有多个校区位置就在这里
    # 如果是单个校区位置信息在这里
    latitude: str = None
    longitude: str = None
    schoolId: str


class SignListResp(BaseModel):
    data: list[SignInfo]

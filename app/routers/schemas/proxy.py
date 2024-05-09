from pydantic import BaseModel


class SchoolInfo(BaseModel):
    id: str
    isActive: int
    logo: str
    name: str


class SchoolListResp(BaseModel):
    data: list[dict]


class LoginResp(BaseModel):
    jw_session: str


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
    date: int  # 开始时间
    end: int  # 结束时间
    signContext: str
    signStatus: int
    areaList: list[AreaInfo]
    schoolId: str


class SignListResp(BaseModel):
    data: list[SignInfo]


class SuccessResp(BaseModel):
    message: str

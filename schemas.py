from pydantic import BaseModel
import datetime

class KeyValue(BaseModel):
    key: str
    value: str

class RequestResponseBase(BaseModel):
    method: str
    headers: list[object] = []
    params: list[object] = []
    body: object = {}

class AppBase(BaseModel):
    name: str

class RequestBase(BaseModel):
    url: str
    name: str
    description: str
    frecuency: str
    body: RequestResponseBase
    seach_params: list[object]

class TestBase(BaseModel):
    passed: bool
    response: object
    created_date: datetime.datetime

class Test(TestBase):
    id: int
    request_id: int

    class Config:
        orm_mode = True

class Request(RequestBase):
    id: int
    owner_id: int
    tests: list[Test]

    class Config:
        orm_mode = True

class App(AppBase):
    id: int
    requests = list[Request]

    class Config:
        orm_mode = True

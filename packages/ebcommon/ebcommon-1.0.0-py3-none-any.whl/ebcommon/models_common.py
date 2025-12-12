from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel, field_serializer
from datetime import datetime
from json import loads as jsloads
from requests.models import Response

class UserCred(BaseModel):
    username: str
    password: str


class UserId(BaseModel):
    email: str
    name: str


class UserObj(BaseModel):
    # Ready-only
    uuid: str
    # Might be updated/extended
    tags: Optional[List[str]]
    # Computed
    state: Optional[int]
    state_desc: Optional[str]  # In case of error, some information are kept there.


class MessageLevel(IntEnum):
    error = -2
    warning = -1
    ok = 0
    info = 1
    debug = 2


class MessageException(Exception):
    def __init__(self, message):
        if not isinstance(message, Message):
            try:              self.message = Message(message)
            except Exception: self.message = Message(exc=None, name=r'Unknown', message=message, error_level=MessageLevel.error)
        else:                 self.message = message
        super().__init__(self.message.error_level, self.message.name, self.message.message, self.message.details)

class Message(BaseModel):
    name: str = r'Undefined'
    message: str = r''
    error_level: int = MessageLevel.error
    details: dict = {}
    date: datetime

    def __init__(self, exc: Optional[Exception | str], **kw):
        if isinstance(exc, Exception):
            kw |= {"error_level": MessageLevel.error}
            if hasattr(exc, "name"):              kw["name"] = exc.name
            if hasattr(exc, "description"):       kw["message"] = exc.description
            if hasattr(exc, "details"):
                if isinstance(exc.details, dict): kw["details"] = exc.details
                else:                             kw["details"] = { "info": str(exc.details) }
        elif isinstance(exc, str):
            kw |= jsloads(exc)
        if "date" not in kw: kw["date"] = datetime.now()
        super().__init__(**kw)

    @field_serializer("date")
    def serialize_date(self, date: datetime) -> str:
        return date.isoformat()

    def error(self) -> bool:
        return self.error_level <= MessageLevel.error

    def level(self) -> bool:
        return self.error_level

    @staticmethod
    def castResponse(response: Response, cast: type = None):
        if response.status_code == 200:
            if cast:                     return cast(**response.json())
            else:                        return response.json()
        else:                            raise MessageException(response.text)

class MessageLogin(Message):
    token: str

    def __init__(self, access_token: [dict | str]):
        kw = access_token
        if isinstance(access_token, str):
            kw = {"name": r'LoginSuccessfull', "message": r'Login successfull.', "error_level": MessageLevel.ok, "token": access_token}
        super().__init__(None, **kw)

    def getAuthHeader(self):
        return {'Authorization': f"Bearer {self.token}", 'Content-Type': "application/json"} if self.token else {}

    @staticmethod
    def castResponse(response: Response):
        if response.status_code == 200:  return MessageLogin(response.json())
        else:                            raise MessageException(response.text)

class MessageData(Message):
    def __init__(self, content):
        kw = {"name": r'DownloadSuccessfull', "message": r'Download successfull.', "error_level": MessageLevel.ok}
        super().__init__(None, **kw)

    @staticmethod
    def castResponse(response: Response):
        if response.status_code == 200:  return response.content
        else:                            raise MessageException(response.text)

class MessageList(Message):
    def __init__(self, content):
        kw = {"name": r'DownloadSuccessfull', "message": r'Download successfull.', "error_level": MessageLevel.ok}
        super().__init__(None, **kw)

    @staticmethod
    def castNextResponse(response: Response, cast: type = None):
        if response.status_code == 200:
            try:
                for eb in response.json():
                    if cast: eb = cast(**eb)
                    yield eb
            except Exception as e:
                raise RuntimeError(r'Could not iterate on the result: %s: %s' % ((str(e), response.text)))
        else:
            raise MessageException(response.text)

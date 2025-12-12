from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel

class RuntimeStateEnum(IntEnum):
    error = -2
    deleted = -1
    disabled = 0
    initialized = 1
    created = 2
    ready = 3
    occupied = 4

class RuntimeRequest(BaseModel):
    name: Optional[str] = r'local::sh'
    accepted_mime_type: Optional[str] = r''
    policy_uid: Optional[str] = ''

    tags: Optional[List[str]] = []

class Runtime(BaseModel):
    uuid: str
    # Ready-only
    name: str
    # Might be updated/extended
    accepted_mime_type: Optional[str]
    policy_uid: Optional[str]
    tags: Optional[List[str]]
    # Computed
    jobs_uuid: List[str]
    state: Optional[RuntimeStateEnum]
    state_desc: Optional[str]  # In case of error, some information are kept there.

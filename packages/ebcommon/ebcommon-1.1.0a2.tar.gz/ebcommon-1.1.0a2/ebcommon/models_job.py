from enum import IntEnum, StrEnum
from typing import Optional, List, Tuple
from pydantic import BaseModel

class JobStateEnum(IntEnum):
    error = -2
    deleted = -1
    disabled = 0
    initialized = 1
    ready = 2
    scheduled = 3
    executed = 4

class JobRunStatusEnum(StrEnum):
    failed = r'FAILED'
    initialized = r'INITIALIZED'
    pending = r'PENDING'
    running = r'RUNNING'
    stopped = r'STOPPED'
    suspended = r'SUSPENDED'
    cancelled = r'CANCELLED'
    completed = r'COMPLETED'

class JobRunStatus(BaseModel):
    status: Optional[JobRunStatusEnum] = JobRunStatusEnum.initialized
    desc: Optional[str] = r''

class JobRequest(BaseModel):
    arguments: Optional[List[str]] = []
    ebin: Optional[List[str]] = []
    ebout: Optional[List[str]] = []
    tags: Optional[List[str]] = []

class Job(BaseModel):
    uuid: str
    # Ready-only
    appms_uuid: Optional[str]
    arguments: List[str]
    ebin: List[str]
    ebout: List[str]
    # Might be updated/extended
    tags: Optional[List[str]]
    result_values: List[bytes]
    run_status: Tuple[JobRunStatusEnum, str]
    # Computed
    runtime_uuid: Optional[str]
    state: Optional[JobStateEnum]
    state_desc: Optional[str]  # In case of error, some information are kept there.

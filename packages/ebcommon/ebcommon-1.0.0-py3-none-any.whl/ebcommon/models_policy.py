from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel

class PolicyStateEnum(IntEnum):
    error = -2
    deleted = -1
    disabled = 0
    initialized = 1
    created = 2

class PolicyAction(IntEnum):
    read = 0x04
    write = 0x02
    execute = 0x01

class PolicyRequest(BaseModel):
    scope: Optional[str] = r''
    rules: Optional[List[str]] = []
    tags: Optional[List[str]] = []

    # [subject]:[action][:condition]
    def addRule(self, subject: str, actions: List[PolicyAction], condition: str = r'') -> str:
        line = r'%s<%d:%s' % (subject, sum(actions), condition)
        self.rules.append(line)

class Policy(BaseModel):
    uuid: str
    # Read-only
    scope: str
    # Might be updated/extended
    rules: List[str]
    tags: Optional[List[str]]
    # Computed
    state: Optional[PolicyStateEnum]
    state_desc: Optional[str]  # In case of error, some information are kept there.

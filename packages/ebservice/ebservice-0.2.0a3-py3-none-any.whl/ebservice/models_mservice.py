from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel

class MicroserviceStateEnum(IntEnum):
    error = -2
    deleted = -1
    disabled = 0
    initialized = 1
    created = 2
    waiting = 3
    binded = 4

class MicroserviceRequest(BaseModel):
    name: Optional[str] = r''
    mime_type: Optional[str] = r''
    code: str = r''
    argument_names: Optional[List[str]] = []
    result_names: Optional[List[str]] = []
    ebin_names: Optional[List[str]] = []
    ebout_names: Optional[List[str]] = []
    policy_uid: Optional[str] = ''

    runtime_uuid: Optional[str] = r''
    tags: Optional[List[str]] = []

class Microservice(BaseModel):
    uuid: str
    # Ready-only
    name: str
    mime_type: str
    code: str
    argument_names: Optional[List[str]]
    result_names: Optional[List[str]]
    ebin_names: Optional[List[str]]
    ebout_names: Optional[List[str]]
    policy_uid: Optional[str]
    # Might be updated/extended
    runtime_uuid: Optional[str]
    tags: Optional[List[str]]
    # Computed
    jobs_uuid: List[str]
    state: Optional[MicroserviceStateEnum]
    state_desc: Optional[str]  # In case of error, some information are kept there.

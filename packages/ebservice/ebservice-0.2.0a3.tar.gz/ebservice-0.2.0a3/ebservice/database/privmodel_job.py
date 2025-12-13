import uuid
from typing import Optional, List, Tuple
from pydantic import BaseModel, field_serializer, model_serializer
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from ebuffer.database.privmodel_user import UserIdEntry
from ebuffer.database.privmodel_userobj import UserObjEntry
from ebservice.models_job import JobRequest, Job, JobStateEnum, JobRunStatusEnum, JobRunStatus

#
# Private Models

class JobEntry(UserObjEntry, table=True):
    __tablename__ = 'job'
    # Read-only
    appms_uuid: Optional[str] = Field(default=r'', nullable=True, foreign_key="microservice.uuid", exclude=True)

    # Mandatory
    arguments: List[str] = Field(default=[], sa_column=Column(JSON))
    ebin: List[str] = Field(default=[], sa_column=Column(JSON))
    ebout: List[str] = Field(default=[], sa_column=Column(JSON))

    # Might be updated/extended
    tags: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    result_values: List[str] = Field(default=[], sa_column=Column(JSON))
    run_status: Tuple[JobRunStatusEnum, str] = Field(sa_column=Column(JSON))

    # Computed
    runtime_uuid: str = Field(default=r'', foreign_key="runtime.uuid", exclude=True)
    state: JobStateEnum = Field(default=JobStateEnum.error)

    # Linked
    #owner: Optional[UserIdEntry] = Relationship(back_populates="buffers")  # userobj
    mservice: Optional["MicroserviceEntry"] = Relationship(back_populates="jobs")
    runtime: Optional["RuntimeEntry"] = Relationship(back_populates="jobs")

    #@field_serializer('run_status')
    #def ser_run_status(self, run_status: JobRunStatus):
    #    print(r'°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°', run_status, run_status.model_dump_json())
    #    return r''

    #@model_serializer
    #def ser_model(self):
    #    print(r'°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°', self, self.dict())
    #    return self.model_dump_json()

    def is_deleted(self):  self.state <= JobStateEnum.disabled
    def set_deleted(self): self.state = JobStateEnum.deleted

    def __init__(self, appms: str, njob: Job, **kw):
        kw[r'appms_uuid'] = appms
        kw[r'run_status'] = (JobRunStatusEnum.initialized, r'')
        kw[r'state'] = JobStateEnum.initialized
        super().__init__(njob, **kw)

    def refresh(self): pass

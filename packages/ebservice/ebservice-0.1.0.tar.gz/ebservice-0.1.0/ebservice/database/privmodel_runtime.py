import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from ebuffer.database.privmodel_user import UserIdEntry
from ebuffer.database.privmodel_userobj import UserObjEntry
from ebservice.models_runtime import Runtime, RuntimeStateEnum
from ebservice.database.privmodel_mimetypes import MimetypeEntry
from ebservice.database.privmodel_job import JobEntry
from ebservice.database.privmodel_policy import PolicyEntry

#
# Private Models

class RuntimeEntry(UserObjEntry, table=True):
    __tablename__ = 'runtime'
    # Mandatory
    name: str = Field(nullable=False, default=r'')

    # Might be updated/extended
    accepted_mime_type: Optional[str] = Field(default=r'', nullable=True, foreign_key="mimetype.name", exclude=True)
    policy_uid: Optional[str] = Field(default=r'', nullable=True, foreign_key="policy.uuid", exclude=True)
    tags: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))

    # Computed
    jobs_uuid: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    state: RuntimeStateEnum = Field(default=RuntimeStateEnum.error)

    # Linked
    #owner: Optional[UserIdEntry] = Relationship(back_populates="runtimes")
    mimetype: Optional[MimetypeEntry] = Relationship(back_populates="runtimes")
    jobs: Optional[JobEntry] = Relationship(back_populates="runtime")
    policy: Optional[PolicyEntry] = Relationship(back_populates="runtime")
    mservice: Optional["MicroserviceEntry"] = Relationship(back_populates="runtime")

    def is_deleted(self):  self.state <= RuntimeStateEnum.disabled
    def set_deleted(self):
        self.state = RuntimeStateEnum.deleted
        self.accepted_mime_type = None

    def matchesMimetype(self, mimetype: MimetypeEntry):
        return self.state == RuntimeStateEnum.ready and self.accepted_mime_type == mimetype

    def __init__(self, rt: Runtime, **kw):
        kw[r'state'] = RuntimeStateEnum.initialized
        super().__init__(rt, **kw)

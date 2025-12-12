import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from ebuffer.database.privmodel_user import UserIdEntry
from ebuffer.database.privmodel_userobj import UserObjEntry
from ebservice.config import logger
from ebservice.models_mservice import Microservice, MicroserviceStateEnum
from ebservice.database.privmodel_mimetypes import MimetypeEntry
from ebservice.database.privmodel_job import JobEntry
from ebservice.database.privmodel_policy import PolicyEntry
from ebservice.database.privmodel_runtime import RuntimeEntry

#
# Private Models

class MicroserviceEntry(UserObjEntry, table=True):
    __tablename__ = 'microservice'
    # Mandatory
    name: str = Field(nullable=False, default=r'')
    mime_type: str = Field(nullable=False, default=r'text/plain', foreign_key="mimetype.name", exclude=True)
    code: str = Field(nullable=False, default=r'')
    argument_names: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    result_names: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    ebin_names: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    ebout_names: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    runtime_uuid: Optional[str] = Field(default=r'', foreign_key="runtime.uuid", exclude=True)

    # Might be updated/extended
    policy_uid: Optional[str] = Field(default=r'', foreign_key="policy.uuid", exclude=True)
    tags: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))

    # Computed
    jobs_uuid: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    state: MicroserviceStateEnum = Field(default=MicroserviceStateEnum.error)

    # Linked
    #owner: Optional[UserIdEntry] = Relationship(back_populates="microservices")
    mimetype: Optional[MimetypeEntry] = Relationship(back_populates="mservices")
    jobs: Optional[JobEntry] = Relationship(back_populates="mservice")
    policy: Optional[PolicyEntry] = Relationship(back_populates="mservice")
    runtime: Optional[RuntimeEntry] = Relationship(back_populates="mservice")

    def is_deleted(self):  self.state <= MicroserviceStateEnum.disabled
    def set_deleted(self): self.state = MicroserviceStateEnum.deleted

    def matchesRuntime(self, runtime: RuntimeEntry):
        return self.state == MicroserviceStateEnum.waiting and (
            self.runtime_uuid == runtime.uuid or runtime.matchesMimetype(self.mime_type)
        )

    def __init__(self, mservice: Microservice, **kw):
        kw[r'state'] = MicroserviceStateEnum.initialized
        super().__init__(mservice, **kw)
        #logger.debug(f'*******  Create microservice \n{mservice}\n{self}')

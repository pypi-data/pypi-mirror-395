import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from ebservice.models_policy import Policy, PolicyStateEnum

#
# Private Models

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types

class MimetypeEntry(SQLModel, table=True):
    __tablename__ = 'mimetype'
    # Read-only
    name: str = Field(nullable=False, primary_key=True)

    # Linked
    mservices: Optional[List["MicroserviceEntry"]] = Relationship(back_populates="mimetype")
    runtimes: Optional[List["RuntimeEntry"]] = Relationship(back_populates="mimetype")

    def __init__(self, mimetype: str, **kw):
        kw[r'name'] = mimetype
        super().__init__(**kw)

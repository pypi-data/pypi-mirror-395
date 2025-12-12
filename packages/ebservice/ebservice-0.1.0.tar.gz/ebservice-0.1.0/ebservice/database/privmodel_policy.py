import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from ebuffer.errors import Eb_Exception
from ebuffer.database.privmodel_user import UserIdEntry
from ebuffer.database.privmodel_userobj import UserObjEntry
from ebservice.models_policy import Policy, PolicyStateEnum, PolicyAction

class Eb_PolicyForbidden(Eb_Exception):
    def __init__(self, scope: str = r''):
        super().__init__(401, "Eb_PolicyForbidden", "Access forbidden by policy.", r'scope: %s' % scope)

#
# Private Models

class PolicyACL():
    def __init__(self, line: str):
        subject = line.split(r'<')
        self.subject = subject[0]
        action = subject[1].split(r':')
        self.action = int(action[0])
        self.condition = action[1]

    def has(self, action: PolicyAction):
        return (self.action & action) > 0

class PolicyEntry(UserObjEntry, table=True):
    __tablename__ = 'policy'
    # Mandatory
    scope: str = Field(nullable=False, default=r'')

    # Might be updated/extended
    rules: List[str] = Field(default=[], sa_column=Column(JSON))
    tags: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))

    # Computed
    _acls: List[PolicyACL] = []
    state: PolicyStateEnum = Field(default=PolicyStateEnum.error)

    # Linked
    #owner: Optional[UserIdEntry] = Relationship(back_populates="buffers")  # userobj
    mservice: Optional[List["MicroserviceEntry"]] = Relationship(back_populates="policy")
    runtime: Optional[List["RuntimeEntry"]] = Relationship(back_populates="policy")

    def is_deleted(self):  self.state <= PolicyStateEnum.disabled
    def set_deleted(self): self.state = PolicyStateEnum.deleted

    def __init__(self, policy: Policy, **kw):
        kw[r'state'] = PolicyStateEnum.initialized
        super().__init__(policy, **kw)
        self.scope = self.scope.lower()
        self.refresh()

    def refresh(self):
        self._acls = []
        for ln in self.rules:
            self._acls.append(PolicyACL(ln))

    # [subject]:[action][:condition] Resource implicit, might be guided with the scope
    def isAllowed(self, scope: str, subject: UserIdEntry, actions: List[PolicyAction]) -> bool:
        if subject.email == self.user_email: return True

        scope = scope.lower()
        if scope == r'*' or scope == self.scope:
            for acl in self._acls:
                if acl.subject == r'*' or subject.matches(acl.subject):
                    found = []
                    for a in actions:
                        if acl.has(a): found.append(a)
                    for f in found: actions.remove(f)
                if not len(actions): return True
        raise Eb_PolicyForbidden()

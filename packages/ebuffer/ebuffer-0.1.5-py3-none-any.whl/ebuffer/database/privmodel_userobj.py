import uuid
from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from ebuffer.models_common import UserObj
from ebuffer.database.privmodel_user import UserIdEntry

#
# Private Models

class UserObjEntry(SQLModel, table=False):
    # Read-only
    uuid: str = Field(nullable=False, primary_key=True)  # userobj

    # Might be updated/extended
    tags: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))  # userobj

    # Computed
    user_email: str = Field(nullable=False, default=r'', foreign_key="users.email", exclude=True)  # userobj
    state_desc: str = Field(default=r'')

    # Linked
    #owner: Optional[UserIdEntry] = Relationship(back_populates="objects")  # userobj

    def __hash__(self) -> int:
        return self.uuid.__hash__() # or self.id.__hash__()

    def __init__(self, obj: UserObj, **kw):
        uid = uuid.uuid4()
        kw |= obj.dict()
        kw[r'uuid'] = str(uid)
        super().__init__(**kw)
        self.refresh()

    def refresh(self): pass

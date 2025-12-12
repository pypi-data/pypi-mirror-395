import uuid
from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from ebuffer.models_buffer import Buffer, BufferStateEnum
from ebuffer.database.privmodel_user import UserIdEntry
from ebuffer.database.privmodel_userobj import UserObjEntry

#
# Private Models

class BufferEntry(UserObjEntry, table=True):
    __tablename__ = 'buffers'
    # Mandatory
    reserved_size: Optional[int] = Field(default=1000)  # in bytes
    lifespan: Optional[int] = Field(default=30)  # in seconds

    # Computed
    expire_at: float = Field(nullable=False)  # optional userobj
    path: str = Field(default=r'')
    size: int = Field(default=0)
    lifetime: int = Field(default=-1)
    state: BufferStateEnum = Field(default=BufferStateEnum.error)

    def is_deleted(self):  self.state <= BufferStateEnum.disabled
    def set_deleted(self): self.state = BufferStateEnum.deleted

    def __init__(self, buffer: Buffer, startup_time, **kw):
        kw[r'expire_at'] = (datetime.now() + timedelta(seconds=startup_time)).timestamp()
        kw[r'state'] = BufferStateEnum.initialized
        super().__init__(buffer, **kw)
        self.refresh()

    def refresh(self):
        expat = datetime.fromtimestamp(self.expire_at)
        now = datetime.now()
        self.lifetime = (expat - now).seconds if expat > now else 0

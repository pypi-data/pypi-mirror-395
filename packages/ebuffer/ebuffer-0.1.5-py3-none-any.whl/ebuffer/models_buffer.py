from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel

class BufferStateEnum(IntEnum):
    error_deleted = -3
    error = -2
    deleted = -1
    disabled = 0
    initialized = 1
    created = 2
    full = 3

class BufferRequest(BaseModel):
    reserved_size: Optional[int] = -1
    lifespan: Optional[int] = -1
    tags: Optional[List[str]] = []


class Buffer(BaseModel):
    uuid: str
    # Ready-only
    reserved_size: Optional[int]
    # Might be updated/extended
    tags: Optional[List[str]]
    # Computed
    size: Optional[int]
    lifetime: Optional[int] = -1
    state: Optional[BufferStateEnum]
    state_desc: Optional[str]  # In case of error, some information are kept there.

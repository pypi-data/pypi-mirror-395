# https://gridcf.org/gct-docs/
# https://pylibacl.k1024.org/index.html
# https://github.com/gridcf/gct


from typing import Optional
from pydantic import BaseModel

class ACL_V(BaseModel):
    rwx : bytes[3]
    def __str__(self): return r'%c%c%c' % (self.rwx[0],self.rwx[1],self.rwx[2])

class ACL_U(BaseModel):
    ug: bool
    name: str
    value: ACL_V
    def __str__(self): return r'%s:%s:%s' % (r'user' if self.ug else r'group', self.name, self.value)

class ACL(BaseModel):
    user: str
    group: str
    vuser: ACL_V
    vgroup: ACL_V
    vother: ACL_V
    vmask: ACL_V
    aclist: [ ACL_U ]
    vattr: dict
    def __str__(self): return r'%s:%s:%s' % (r'user' if self.ug else r'group', self.name, self.value)

class Eb_Data(BaseModel):
    path: str

    def open(self): pass
    def write(self): pass
    def close(self): pass

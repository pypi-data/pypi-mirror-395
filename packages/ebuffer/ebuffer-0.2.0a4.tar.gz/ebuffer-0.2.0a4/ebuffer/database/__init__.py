from ebuffer.database.privmodel_user import UserIdEntry
from ebuffer.database.privmodel_userobj import UserObjEntry
from ebuffer.database.cruduser import get_user_db, get_user_by_email_db

from ebuffer.database.cruduserobj import Eb_UserObjCRUD

from ebuffer.database.privmodel_buffer import BufferEntry
class Eb_BufferCRUD(Eb_UserObjCRUD):
    def __init__(self): super().__init__(BufferEntry)

from ebuffer.database.database import Eb_Database

from ebuffer.database.database import Eb_DBError
from ebuffer.database.cruduser import Eb_MissingCred
from ebuffer.database.cruduserobj import Eb_ObjectNotFound

BufferExceptionList = Eb_MissingCred().model() | Eb_ObjectNotFound().model()

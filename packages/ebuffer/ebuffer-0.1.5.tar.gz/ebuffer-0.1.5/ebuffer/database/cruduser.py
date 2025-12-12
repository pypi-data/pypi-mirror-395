from asyncio import create_task
from sqlmodel import Session, select
from sqlalchemy.orm.exc import MultipleResultsFound

from ebuffer.models_common import UserId
from ebuffer.config import logger
from ebuffer.errors import Eb_Exception
from ebuffer.database.database import Eb_DBError
from ebuffer.database.privmodel_user import UserIdEntry

#
# UserID Management

class Eb_MissingCred(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(401, "MissingCred", "Missing credentials.", details)

async def _update_user_db(session: Session, user: UserIdEntry) -> UserIdEntry:
    if not isinstance(user, UserIdEntry): raise Eb_DBError("Internal Error CX001")
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        #logger.debug(r"[CRUD] update UserID %s", str(user))
    except Exception as e:
        logger.error(r"Could not add UserID %s: %s", str(user), str(e))
    return user

def get_user_db(session: Session, user: UserId, create: bool = False) -> [ UserIdEntry, None ]:
    sql = select(UserIdEntry).where(UserIdEntry.email == user.email)
    #logger.debug(r"Search user %s", str(user))
    try:
        fuser = session.exec(sql).one_or_none()
    except MultipleResultsFound as e:
        raise Eb_DBError("Multiple users '%s' in DB" % user.email, e)

    #if fuser: logger.debug('User found: %s: %s', fuser.json(), str(fuser.buffers))
    if fuser: return fuser
    if not create:
        raise Eb_MissingCred(r'User %s does not exists' % user.email)

    try:
        dbuser = UserIdEntry.model_validate(user)
    except Exception as e:
        logger.error(r"Could not validate UserID %s: %s", str(user), str(e))
        raise Eb_DBError("Internal Error CX002", e)

    create_task(_update_user_db(session, dbuser))
    return dbuser

def get_user_by_email_db(session: Session, email: str, create: bool = False) -> [ UserIdEntry, None ]:
    sql = select(UserIdEntry).where(UserIdEntry.email == email)
    #logger.debug(r"Search user %s", str(user))
    try:
        fuser = session.exec(sql).one_or_none()
    except MultipleResultsFound as e:
        raise Eb_DBError("Multiple users '%s' in DB" % email, e)

    return fuser

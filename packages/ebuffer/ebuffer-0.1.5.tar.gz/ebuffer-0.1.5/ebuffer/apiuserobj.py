from sqlmodel import Session
from asyncio import create_task, sleep

from ebuffer.config import logger
from ebuffer.models_common import UserId
from ebuffer.database import UserIdEntry, UserObjEntry, get_user_db, get_user_by_email_db
from ebuffer.database import Eb_UserObjCRUD, Eb_ObjectNotFound
from ebuffer.errors import Eb_Exception, Eb_TagSyntaxError

#
# CRUD Management of User's objects

class Eb_ObjectInvalid(Eb_Exception):
    def __init__(self, uuid: str = r''):
        super().__init__(430, "ObjectInvalid", "Object is invalid or was destroyed.", r'Id: %s' % uuid)

class Eb_UserObjAPI():

    def __init__(self, Objtype: type, config: object, uobjcrud: Eb_UserObjCRUD, backend: object = None):
        self.ObjEntry: type = Objtype
        self.conf = config
        self.uobjcrud = uobjcrud
        self.backend = backend

    #
    # Life cycle management

    def assert_correct_tags(self, tags: list[str]) -> bool:
        tag_min_size = self.conf.tag_min_size
        tag_max_size = self.conf.tag_max_size
        for t in tags:
            if len(t) < tag_min_size or len(t) > tag_max_size:
                raise Eb_TagSyntaxError(r'Invalid tag size %d ([%d:%d])' % (len(t), tag_min_size, tag_max_size))
        return True

    async def _destroy(self, session: Session, uobj: UserObjEntry, commit) -> None:
        if self.backend: await self.backend.destroy(session, uobj, commit=commit)
        else:            await self.uobjcrud.destroy(session, uobj, commit=commit)

    async def _destroy_after(self, session: Session, time_s: int, uobj: UserObjEntry, maxcount: int, commit) -> None:
        try:
            await sleep(time_s)
            # session: Session = next(app.g_db.get_session())
            await self._destroy(session, uobj, commit)
        except Exception as e:
            logger.debug(r"Could not finish a destroy operation: %s", str(e))
            if maxcount > 0:
                create_task(self._destroy_after(session, time_s, uobj, maxcount-1, commit))

    async def destroy_after(self, session: Session, time_s: int, uobj: UserObjEntry, maxcount: int = 5, commit=True) -> None:
        #create_task(self._destroy_after(session, time_s, uobj, maxcount, commit=True))
        if time_s: create_task(self._destroy_after(session, time_s, uobj, maxcount, commit=True))
        else:      self._destroy(session, uobj, commit)

    #
    # Main API

    async def create(self, uobj: UserObjEntry, blocking: bool, user: UserId, session: Session) -> UserObjEntry:
        self.assert_correct_tags(uobj.tags)
        # Only in order to register the used in the DB.
        userId: UserIdEntry = get_user_db(session, user, create=True)
        uobj.user_email = userId.email

        if blocking and self.backend:
            await self.backend.build(session, uobj)
        else:
            await self.uobjcrud.update(session, uobj)
            if self.backend:
                create_task(self.backend.build(session, uobj))
        logger.debug(r'[api] Register %s: %s', self.ObjEntry.__name__, uobj)
        return uobj

    async def search(self, session: Session = None, user: UserId = None,
                     limit: int = 0, skip: int = 0,
                     owner: str = None, tags: list[str] = [], all: bool = False, count: bool = False,
                     ofilter: callable = None) -> list[UserObjEntry] | int:
        self.assert_correct_tags(tags)
        if owner:
            owner = get_user_by_email_db(session, owner, create=False)
            if not owner:
                return 0 if count else []
        results = []

        # Warning : 'user' is not used, but shall be in order to check if the data has read policy.
        if count:
            #logger.debug("[searchObject]------ %s: %s [%s] --------", str(owner), str(tags), str(all))
            return self.uobjcrud.count(session, limit, skip, owner, tags, all, ofilter=ofilter)
        else:
            #logger.debug("[searchObject]------ %s: %s [%s] --------", str(owner), str(tags), str(all))
            for uobj in self.uobjcrud.search(session, limit, skip, owner, tags, all, ofilter=ofilter):
                # logger.debug("[searchObject]: found %s" % uobj)
                results.append(uobj)
            # logger.debug("[searchObject]+++++++++++++++")
            return results

    async def get(self, uid: str, owner: str, user: UserId, session: Session) -> UserObjEntry:
        if owner:
            owner = get_user_by_email_db(session, owner, create=False)
            if not owner: raise Eb_ObjectNotFound(uid)
        # Warning : 'user' is not used, but shall be in order to check if the data has read policy.
        return self.uobjcrud.get(session, uid, owner)

    async def delete(self, uid: str, user: UserId, session: Session) -> UserObjEntry:
        #userd = get_user_db(session, user, create=False)
        uobj = self.uobjcrud.get(session, uid, user)  # Warning: the for now, data has to belong to the user.
        if uobj.is_deleted(): return uobj
        uobj.set_deleted()
        await self.uobjcrud.update(session, uobj)
        await self.destroy_after(session, self.conf.grace_time, uobj)
        return uobj

    #
    # Tag API

    async def getTags(self, uid: str, owner: str, user: UserId, session: Session) -> UserObjEntry:
        uobj = await self.get(uid, owner, user, session)
        return uobj.tags if uobj else []

    async def addTag(self, uid: str, tag: str, user: UserId, session: Session) -> UserObjEntry:
        #userd = get_user_db(session, user, create=False)
        self.assert_correct_tags((tag,))
        uobj = self.uobjcrud.get(session, uid, user)  # Warning: the for now, data has to belong to the user.
        if uobj.is_deleted(): raise Eb_ObjectInvalid(uid)
        uobj.tags = list(uobj.tags)
        uobj.tags.append(tag)
        create_task(self.uobjcrud.update(session, uobj))
        return uobj

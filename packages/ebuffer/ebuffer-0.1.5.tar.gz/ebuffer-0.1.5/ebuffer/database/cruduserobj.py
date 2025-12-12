from datetime import datetime
from sqlmodel import Session, select
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import text
from traceback import format_exc

from ebuffer.models_common import UserId
from ebuffer.config import logger
from ebuffer.errors import Eb_Exception
from ebuffer.database.privmodel_userobj import UserObjEntry
from ebuffer.database.database import Eb_DBError

#
# CRUD Management of User's objects

class Eb_ObjectNotFound(Eb_Exception):
    def __init__(self, uuid: str = r'xxx-xxx-xxx'):
        super().__init__(404, "ObjectNotFound", "Object not found.", r'Status: %s' % uuid)

class Eb_UserObjCRUD():

    def __init__(self, Objtype: type):
        self.ObjEntry: type = Objtype

    def commit(self, session: Session) -> None:
        session.commit()

    async def update(self, session: Session, uobj: UserObjEntry, commit: bool = True) -> object:
        if not isinstance(uobj, self.ObjEntry): raise Eb_DBError("Internal Error CX003")
        try:
            session.add(uobj)
            if commit:
                session.commit()
                session.refresh(uobj)
            #logger.debug(r"[CRUD] update %s", str(uobj))
        except Exception as e:
            logger.error(r"Could not create/update ObjectEntry %s: %s:\n%s", str(uobj), str(e), format_exc())
        return uobj

    async def destroy(self, session: Session, uobj: UserObjEntry, commit: bool = True) -> object:
        if not isinstance(uobj, self.ObjEntry): raise Eb_DBError("Internal Error CX004")
        try:
            session.delete(uobj)
            if commit:
                session.commit()
            #logger.debug(r'Destroyed ObjectEntry: %s', uobj.uuid)
        except Exception as e:
            logger.error(r"Could not destroy ObjectEntry %s: %s", str(uobj), str(e))
        return uobj

    def get(self, session: Session, uuid: str, user: [UserId | None] = None) -> UserObjEntry:
        statement = select(self.ObjEntry)
        if   user: statement = statement.where(self.ObjEntry.uuid == uuid and self.ObjEntry.user_email == user.email)
        else:      statement = statement.where(self.ObjEntry.uuid == uuid)
        results = session.exec(statement)
        try:
            uobj = results.one_or_none()
        except MultipleResultsFound:
            raise Eb_DBError("Multiple identical ObjectEntries '%s' in DB" % uuid)

        if not uobj:
            raise Eb_ObjectNotFound(uuid)

        uobj.refresh()
        return uobj

    def get_expired(self, session: Session, interval: int) -> UserObjEntry:
        try:
            if not hasattr(self.ObjEntry, r'expire_at'): return
            now : int = datetime.now().timestamp() + interval
            statement = select(self.ObjEntry).where(self.ObjEntry.expire_at < now)
            results = session.exec(statement)
            for uobj in results:
                uobj.refresh()
                yield uobj

        except Exception as e:
            logger.error(r"Could not extract expired ObjectEntries: %s", format_exc())
            raise Eb_DBError("Internal Error CX005", e)

    def _search_obj(self, session: Session, limit: int, skip: int,
                    owner: [UserId | None] = None, tags: list[str] = [], all=False,
                    count=True) -> UserObjEntry:
        try:
            select = r'SELECT uuid'
            where_user = r''
            extra_sql = r''
            if count: select = r'SELECT COUNT(uuid)'
            else:
                if limit > 0: extra_sql += f' LIMIT {limit}'
                if skip > 0:  extra_sql += f' OFFSET {skip}'
            if owner:
                where_user = f' AND {self.ObjEntry.__tablename__}.user_email == "{owner.email}"'
            if not tags or len(tags) == 0:
                if owner: statement = text(f'{select} FROM {self.ObjEntry.__tablename__} WHERE {self.ObjEntry.__tablename__}.user_email == "{owner.email}"')
                else:    statement = text(f'{select} FROM {self.ObjEntry.__tablename__}')
            elif len(tags) == 1:
                tag = tags[0]
                statement = text(f"""
                {select} FROM {self.ObjEntry.__tablename__}
                WHERE :tag IN (SELECT value FROM json_each(tags)){where_user}
                """).bindparams(tag=tag)
            elif isinstance(tags, list):
                params = {f"t{i}": tag for i, tag in enumerate(tags)}
                if all:  # --- AND ---
                    svars = r' AND '.join([f":t{i} in (SELECT DISTINCT value FROM json_each(tags))" for i in range(len(tags))])
                    statement = text(f"""
                    {select}
                    FROM {self.ObjEntry.__tablename__}
                    WHERE {svars}
                    {where_user}
                    """).bindparams(**params)
                else:  # --- OR ---
                    svars = ", ".join([f":t{i}" for i in range(len(tags))])
                    statement = text(f"""
                    {select} FROM {self.ObjEntry.__tablename__}
                    WHERE EXISTS (
                        SELECT value FROM json_each(tags)
                        WHERE value IN ({svars})
                    ){where_user}
                    """).bindparams(**params)
            return session.exec(statement)

        except Exception as e:
            logger.error(r"Could not extract ObjectEntries by token: %s", format_exc())
            raise Eb_DBError("Internal Error CX006", e)

    def search(self, session: Session, limit: int, skip: int,
               owner: [UserId | None] = None, tags: list[str] = [], all=False,
               ofilter: callable = None) -> UserObjEntry:
        try:
            results = self._search_obj(session, limit, skip, owner, tags, all, False)
            for row in results:
                uobj = session.get(self.ObjEntry, row.uuid)
                uobj.refresh()
                if ofilter and not ofilter(uobj): continue
                yield uobj

        except Exception as e:
            logger.error(r"Could not extract ObjectEntries by token: %s", format_exc())
            raise Eb_DBError("Internal Error CX007", e)

    def count(self, session: Session, limit: int, skip: int,
              owner: [UserId | None] = None, tags: list[str] = [], all=False,
              ofilter: callable = None) -> UserObjEntry:
        try:
            if not ofilter:
                results = self._search_obj(session, limit, skip, owner, tags, all, True)
                count = results.one_or_none()
                return count[0]
            count = 0
            results = self._search_obj(session, limit, skip, owner, tags, all, False)
            for row in results:
                uobj = session.get(self.ObjEntry, row.uuid)
                uobj.refresh()
                if ofilter and not ofilter(uobj): continue
                count += 1
            return count

        except Exception as e:
            logger.error(r"Could not extract ObjectEntries by token: %s", format_exc())
            raise Eb_DBError("Internal Error CX008", e)

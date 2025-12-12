from io import BytesIO
from asyncio import create_task
from sqlmodel import Session
from typing import AsyncGenerator
from ebuffer.database import get_user_db
from ebuffer.apiuserobj import Eb_UserObjAPI, Eb_ObjectInvalid

from ebuffer.config import EbConfig, logger
from ebuffer.models_common import UserId
from ebuffer.models_buffer import BufferStateEnum
from ebuffer.database import BufferEntry, Eb_BufferCRUD
from ebuffer.backends import Eb_DataBackend, Eb_BackendReadError

Eb_BufferInvalid = Eb_ObjectInvalid

class Eb_BufferAPI(Eb_UserObjAPI):

    def __init__(self, config: EbConfig):
        self.config = config
        self.bufferCRUD = Eb_BufferCRUD()
        self.backend = Eb_DataBackend.getBackend(self.config, self.bufferCRUD)
        super().__init__(BufferEntry, config.base, self.bufferCRUD, self.backend)

    def destroy(self):
        self.backend.deep_clean()
        del self.backend

    #
    # Housekeeping
    #
    async def housekeeping(self, session: Session, interval: int, start: bool = False) -> None:
        grace_time = interval - 1

        for ebuffer in self.bufferCRUD.get_expired(session, interval):
            if  ebuffer.state == BufferStateEnum.error_deleted or ebuffer.state == BufferStateEnum.deleted:
                if not start: continue

            if   ebuffer.state == BufferStateEnum.initialized:
                ebuffer.state = BufferStateEnum.error
                ebuffer.state_desc = r'Never reached backend initialization.' if not ebuffer.state_desc else ebuffer.state_desc
            elif ebuffer.state == BufferStateEnum.error:
                grace_time = self.config.base.error_grace_time
                if ebuffer.lifetime < grace_time:
                    ebuffer.state = BufferStateEnum.error_deleted
            else:
                if ebuffer.lifetime < grace_time:
                    ebuffer.state = BufferStateEnum.deleted

            if  ebuffer.state == BufferStateEnum.error_deleted or ebuffer.state == BufferStateEnum.deleted:
                logger.debug("[housekeeping]: Destroy (%ds < %ds) %s", ebuffer.lifetime, grace_time, ebuffer)
                await self.bufferCRUD.update(session, ebuffer, commit=False)
                await self.destroy_after(session, grace_time, ebuffer, commit=False)
        self.bufferCRUD.commit(session)

    #
    # I/O operations
    #
    async def write(self, stream: AsyncGenerator[bytes, None], uid: str, user: UserId, session: Session) -> object:
        #userd = get_user_db(session, user, create=False)
        ebuffer = self.bufferCRUD.get(session, uid, user)  # Warning: the for now, data has to belong to the user.
        try:
            await self.backend.write(ebuffer, stream)
        finally:
            create_task(self.bufferCRUD.update(session, ebuffer))
        return ebuffer

    def _generate_bytesio_stream(self, data: BytesIO, chunk_size: int = 4 * 1024 * 1024) -> bytes:
        while chunk := data.read(chunk_size):
            yield chunk  # Envoie un morceau au client
        data.close()

    async def read(self, uid: str, sid: str, seek: int, limit: int, user: UserId, session: Session) -> object:
        # Warning : 'user' is not used, but shall be in order to check if the data has read policy.
        # userd : UserIdEntry = get_user_db(session, user, create=False)
        ebuffer = self.bufferCRUD.get(session, uid)
        data: BytesIO; clen: int
        clen, data = self.backend.fetch(ebuffer, sid, seek=seek, limit=limit) if sid else self.backend.fopen(ebuffer, seek=seek, limit=limit)
        if not data:
            raise Eb_BackendReadError(ebuffer.uuid, r'Empty data stream')
        return clen, self._generate_bytesio_stream(data)

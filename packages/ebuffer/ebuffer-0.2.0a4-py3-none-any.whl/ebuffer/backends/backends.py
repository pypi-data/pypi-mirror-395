from io import BytesIO
from math import floor, log10
from datetime import datetime, timedelta
from typing import AsyncGenerator
from sqlmodel import Session
from ebuffer.models_buffer import BufferStateEnum
from ebuffer.config import EbConfig, logger
from ebuffer.errors import Eb_Exception
from ebuffer.database import BufferEntry, Eb_BufferCRUD

class Eb_BackendDuplicatedError(Eb_Exception):
    def __init__(self, scheme: str):
        super().__init__(440, "BackendDuplicatedError", "Multiple storage backend defined with the same scheme (%s)." % scheme, "Check backend installation.")

class Eb_BackendMissingError(Eb_Exception):
    def __init__(self, scheme: str):
        super().__init__(440, "BackendMissingError", "Storage backend '%s' not found." % scheme, "Check backend installation.")

class Eb_BackendMissingBufferError(Eb_Exception):
    def __init__(self, uuid: str = r'xxx-xxx-xxx'):
        super().__init__(440, "BackendMissingBufferError", "Buffer '%s' not found in storage backend." % uuid)

class Eb_BackendWriteError(Eb_Exception):
    def __init__(self, uuid: str = r'xxx-xxx-xxx', details: str = r'', exc: Exception = None):
        super().__init__(440, "BackendWriteError", "Could not write data in buffer %s." % uuid, details, exc)

class Eb_BackendReadError(Eb_Exception):
    def __init__(self, uuid: str = r'xxx-xxx-xxx', details: str = r'', exc: Exception = None):
        super().__init__(440, "BackendReadError", "Could not read data from buffer %s." % uuid, details, exc)

class Eb_Data():
    def __init__(self, ebuffer: BufferEntry, backend):
        self.backend = backend
        self.ebuffer = ebuffer

    def validate(self) -> bool:                return True
    def used_size(self) -> int:                return 0
    def write(self, chunk: bytes) -> None:     pass
    def fetch(self) -> (int, BytesIO | None) : return 0, None
    def fopen(self) -> (int, BytesIO | None) : return None
    def flush(self) -> bool:                   return True
    def destroy(self) -> None :                pass

class Eb_DataBackend():
    g_backends: dict = {}

    def __init__(self, config: EbConfig, bufferCRUD: Eb_BufferCRUD, schema : str = r'none://'):
        self.config = config.base
        self.bufferCRUD = bufferCRUD
        self.schema : str = schema
        self.db = {}

    g_UNITS = ['', 'k', 'M', 'G'] + ([None] * 10) + ['f', 'p', 'n', u'\u03bc', 'm']         # U+03BC is Greek lowercase mu
    @staticmethod
    def eng_format(x, unit=''):
        po1k = int(floor(log10(x) // 3)) if x else 1
        exponent = 3 * po1k
        prefix = Eb_DataBackend.g_UNITS[po1k]
        if prefix is None:
            prefix = '*10^%d ' % exponent
        significand = x * 10**(-exponent)
        return '%.2f%s%s' % (significand, prefix, unit)

    @staticmethod
    def addBackend(schema: str, backend_class: type):
        if schema in Eb_DataBackend.g_backends: raise Eb_BackendDuplicatedError(schema)
        Eb_DataBackend.g_backends[schema] = backend_class

    @staticmethod
    def getBackend(config: EbConfig, bufferCRUD: Eb_BufferCRUD):
        schema = config.base.storage_backend
        if schema not in Eb_DataBackend.g_backends: raise Eb_BackendMissingError(schema)
        return Eb_DataBackend.g_backends[schema](config, bufferCRUD, schema)

    def schema(self): return self.schema

    def setPath(self, ebuffer):
        ebuffer.path = self.schema + str(ebuffer.uuid)

    async def build(self, session: Session, ebuffer: BufferEntry) -> bool:
        ebuffer.reserved_size = min(ebuffer.reserved_size, self.config.max_size) if ebuffer.reserved_size > 0  else self.config.default_size
        ebuffer.lifespan = min(ebuffer.lifespan, self.config.max_life_span)      if ebuffer.lifespan      > 0  else self.config.default_life_span
        ebuffer.expire_at = (datetime.now() + timedelta(seconds=ebuffer.lifespan)).timestamp()
        self.setPath(ebuffer)
        try:
            self.db[ebuffer.uuid] = self.newData(ebuffer)
            ebuffer.state = BufferStateEnum.created
            logger.debug(r'[backend] Create buffer: %s', ebuffer.model_dump())
            await self.bufferCRUD.update(session, ebuffer)
        except Eb_Exception as e:
            error = r'Buffer creation failed: %s' % str(e)
            ebuffer.state = BufferStateEnum.error
            ebuffer.state_desc = error
            await self.bufferCRUD.update(session, ebuffer)
            logger.error(r'[backend]: with %s %s', ebuffer.model_dump(), error)

    async def destroy(self, session: Session, ebuffer: BufferEntry, commit: bool = True) -> None:
        if commit:
            ebuffer.state = BufferStateEnum.disabled
            await self.bufferCRUD.update(session, ebuffer, commit)
        try:
            if ebuffer.uuid not in self.db: self.delData(ebuffer)
            else:
                edata = self.db[ebuffer.uuid]
                #logger.warning(r'Buffer <%s> data found: %s', ebuffer.uuid, str(edata))
                del self.db[ebuffer.uuid]
                edata.destroy()
                del edata
        except Exception as e:
            error = r'Buffer destruction failed: %s' % str(e)
            ebuffer.state = BufferStateEnum.error
            ebuffer.state_desc = error
            #await update_buffer_db(session, ebuffer, commit)
            logger.error(r'[backend]: with %s %s', ebuffer.model_dump(), error)
        logger.debug(r'[backend] Destroy buffer: %s', ebuffer.uuid)
        await self.bufferCRUD.destroy(session, ebuffer, commit)

    def newData(self, ebuffer: BufferEntry) -> Eb_Data:
        edata = Eb_Data(ebuffer, self)
        return edata

    def delData(self, ebuffer: BufferEntry) -> None:
        pass
        #raise Eb_BackendMissingBufferError(ebuffer.uuid)

    def __contains__(self, ebuffer: BufferEntry) -> bool:    return ebuffer.uuid in self.db
    def __getitem__(self, ebuffer: BufferEntry) -> Eb_Data:  return self.db[ebuffer.uuid]

    def get(self, ebuffer: BufferEntry) -> Eb_Data:
        if ebuffer not in self:
            #raise Eb_BackendMissingBufferError(ebuffer.uuid)
            self.db[ebuffer.uuid] = self.newData(ebuffer)
        return self[ebuffer]

    async def write(self, ebuffer: BufferEntry, stream: AsyncGenerator[bytes, None]) -> None:
        try:
            if ebuffer.state == BufferStateEnum.error:
                raise Eb_BackendWriteError(ebuffer.uuid, r'Buffer is in error state, write cancelled.')
            elif ebuffer.state == BufferStateEnum.disabled or ebuffer.state == BufferStateEnum.deleted:
                raise Eb_BackendWriteError(ebuffer.uuid, r'Buffer is disabled, write cancelled.')
            elif ebuffer.state == BufferStateEnum.initialized:
                raise Eb_BackendWriteError(ebuffer.uuid, r'Buffer is in disabled state, wait allocation completion before write.')
            edata = self.get(ebuffer)
            async for chunk in stream:
                edata.write(chunk)
                ebuffer.size = edata.used_size()
                if ebuffer.size >= ebuffer.reserved_size: ebuffer.state = BufferStateEnum.full
            edata.flush()
        except Eb_Exception as exc: raise exc
        except Exception as exc:
            try:
                error = r'Buffer write failed: %s' % str(exc)
                ebuffer.state = BufferStateEnum.error
                ebuffer.state_desc = error
                ebuffer.size = edata.used_size()
                edata.flush()
            except Exception: pass
            raise Eb_BackendWriteError(ebuffer.uuid, str(exc), exc)

    def _chekRead(self, ebuffer: BufferEntry) -> bool:
        if ebuffer.state == BufferStateEnum.initialized:
            raise Eb_BackendReadError(ebuffer.uuid, r'Buffer is in initialization state, wait allocation completion (and maybe a write) before read.')
        elif ebuffer.state == BufferStateEnum.disabled:
            raise Eb_BackendReadError(ebuffer.uuid, r'Buffer is in disabled state, read cancelled.')
        return True

    def fetch(self, ebuffer: BufferEntry, sid: str, seek: int = None, limit: int = None) -> (int, BytesIO | None):
        self._chekRead(ebuffer)
        try: return self.get(ebuffer).fetch(sid, seek, limit)
        except Eb_Exception as exc: raise exc
        except Exception as exc: raise Eb_BackendReadError(ebuffer.uuid, str(exc), exc)

    def fopen(self, ebuffer: BufferEntry, seek: int = None, limit: int = None) -> (int, BytesIO | None):
        self._chekRead(ebuffer)
        try: return self.get(ebuffer).fopen(seek, limit)
        except Eb_Exception as exc: raise exc
        except Exception as exc: raise Eb_BackendReadError(ebuffer.uuid, str(exc), exc)

    def deep_clean(self) -> None :
        for edata in self.db.values():
            edata.destroy()
            del edata
        del self.db
        self.db = {}

    def __del__(self) -> None :
        self.deep_clean()

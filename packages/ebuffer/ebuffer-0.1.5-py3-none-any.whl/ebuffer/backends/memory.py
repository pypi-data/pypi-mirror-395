from io import BytesIO
from asyncio import create_task, sleep, Task, CancelledError
from pydantic import BaseModel
from ebuffer.config import EbConfig, logger
from ebuffer.errors import Eb_Exception
from ebuffer.database import BufferEntry, Eb_BufferCRUD
from ebuffer.backends import Eb_Data, Eb_DataBackend

class Eb_BackendMemoryMaxSizeError(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(441, "BackendMemoryError", "Maximum size reached.", details)

class EbConfigBackendMemory(BaseModel):
    chunk_size: int = 4 * 1024 * 1024
    max_total_size: int = 1 * 1024 * 1024 * 1024
    session_apoptosis_s: int = 300

class Eb_DataMemorySession():
    def __init__(self, name: str, seek: int, limit : int):
        self.name = name
        self.seek = seek if seek and seek > 0 else 0
        self.limit = limit if limit else -1
        self.seek_read: int = seek if seek else 0
        self.stream : memoryview | None = None

    def getSteam(self, data: BytesIO) -> (int, BytesIO | None):
        if not self.stream or self.stream.closed:
            rawbuff = data.getbuffer()
            size = rawbuff.nbytes
            if self.limit > 0: size = self.seek + self.limit
            if self.seek_read >= size: return 0, BytesIO()
            self.stream = BytesIO(rawbuff)
            self.stream.truncate(size)
            self.stream.seek(self.seek_read)
            logger.debug(r'[backend::memory] Session buffer allocated: %s (%d)[%d:%d] %d', self.name, rawbuff.nbytes, self.seek, self.limit, self.seek_read)
            self.seek_read += size
        else: logger.debug(r'[backend::memory] Session buffer recovered: %s (%d)[%d:%d] %d (readable=%s)', self.name, data.getbuffer().nbytes, self.seek, self.limit, self.stream.tell(), str(self.stream.readable()))
        clen = self.stream.getbuffer().nbytes - self.stream.tell()
        return clen, self.stream

class Eb_DataMemory(Eb_Data):
    def __init__(self, ebuffer: BufferEntry, backend: Eb_DataBackend):
        self.backend = backend
        self.allocated = backend.allocate(ebuffer.reserved_size)
        self.ebuffer : BufferEntry = ebuffer
        self.data: BytesIO = BytesIO()
        self.size: int = 0
        self.seek_write: int = 0
        self.sessions : dict = {}
        self.tasks : [Task] = []

    def write(self, chunk: bytes) -> None:
        inc = len(chunk)
        nsize = self.size + inc
        if nsize > self.allocated:
            raise Eb_BackendMemoryMaxSizeError("Chunk required=%d, max buffer size=%d." % (nsize, self.allocated))
        seek_read = self.data.tell()
        self.data.seek(self.seek_write)
        self.data.write(chunk)
        self.size += inc
        self.seek_write = self.data.tell()
        self.data.seek(seek_read)
        logger.debug(r'[backend::memory] Write buffer %d: (%d)[%d:%d]', inc, self.data.getbuffer().nbytes, seek_read, self.seek_write)

    def used_size(self) -> int:
        return self.seek_write

    async def apoptosis(self, session: Eb_DataMemorySession):
        try:
            await sleep(self.backend.bk_config.session_apoptosis_s)
            if session in self.sessions:
                del self.sessions[session]
            logger.debug(r'[backend::file] Session buffer (%s:%s) destroyed', self.ebuffer.uuid, session.name)
            del session
        except CancelledError:
            logger.debug(r'[backend::file] Session buffer (%s) cancelled', self.ebuffer.uuid)
            pass

    def fetch(self, sid: str, seek: int = None, limit: int = None) -> (int, BytesIO | None) :
        if sid not in self.sessions:
            session = Eb_DataMemorySession(sid, seek, limit)
            self.sessions[sid] = session
            self.tasks.append(create_task(self.apoptosis(session)))
        else: session = self.sessions[sid]
        return session.getSteam(self.data)

    def fopen(self, seek: int = None, limit: int = None) -> (int, BytesIO | None) :
        rawbuff = self.data.getbuffer()
        stream = BytesIO(rawbuff)
        cursor = seek if seek and seek > 0 else 0
        if cursor: stream.seek(cursor)
        if limit and limit > 0: stream.truncate(cursor + limit)
        clen = stream.getbuffer().nbytes - stream.tell()
        return clen, stream

    def destroy(self) -> None :
        if not hasattr(self, r'data'): return
        for t in self.tasks: t.cancel()
        self.tasks = []
        if self.allocated:
            self.backend.free(self.allocated)
            self.allocated = 0
            del self.data
            logger.debug(r'[backend::memory] Buffer data (%s) destroyed', self.ebuffer.uuid)

    def __del__(self) -> None :
        self.destroy()

class Eb_DataBackendMemory(Eb_DataBackend):
    def __init__(self, config: EbConfig, bufferCRUD: Eb_BufferCRUD, scheme: str):
        super().__init__(config, bufferCRUD, scheme)
        self.total_memory = 0
        self.bk_config = config.open_section(r'backend::memory', EbConfigBackendMemory)

    def log_stats(self, comment: str = r'') -> None:
        ratio = self.total_memory/self.bk_config.max_total_size * 100
        logger.info(r'[backend::memory][%s] memory allocated: %s/%s %g%%', comment,
                    Eb_DataBackend.eng_format(self.total_memory), Eb_DataBackend.eng_format(self.bk_config.max_total_size), ratio)

    def allocate(self, size: int) -> int:
        needed = self.total_memory + size
        if needed > self.bk_config.max_total_size:
            raise Eb_BackendMemoryMaxSizeError("Current=%d, Required=%d, max global memory=%d." % (
                self.total_memory, size, self.bk_config.max_total_size))
        self.total_memory += size
        self.log_stats(r'post-allocation')
        return size

    def free(self, size: int) -> int:
        self.total_memory -= size
        self.log_stats(r'post-allocation')
        return size

    def newData(self, ebuffer: BufferEntry) -> Eb_DataMemory:
        return Eb_DataMemory(ebuffer, self)

Eb_DataBackend.addBackend(r'memory://', Eb_DataBackendMemory)

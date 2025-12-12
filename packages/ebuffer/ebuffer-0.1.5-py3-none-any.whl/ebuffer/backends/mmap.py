from io import BytesIO
from asyncio import create_task, sleep, Task, CancelledError
from mmap import mmap, MAP_PRIVATE, MAP_SHARED, PROT_READ, PROT_WRITE
from os import unlink
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel
from ebuffer.config import EbConfig, logger
from ebuffer.errors import Eb_Exception
from ebuffer.database import BufferEntry, Eb_BufferCRUD
from ebuffer.backends import Eb_Data, Eb_DataBackend

class Eb_BackendFileMaxSizeError(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(442, "BackendFileError", "Maximum size reached.", details)

class Eb_BackendFileCreateError(Eb_Exception):
    def __init__(self, details: str = r'', exc : Exception = None):
        super().__init__(442, "BackendFileCreateError", "Could not create a file for buffer.", details, exc)

class Eb_BackendFileInitStorage(Eb_Exception):
    def __init__(self, details: str = r'', exc: Exception = None):
        super().__init__(442, "BackendFileInitStorage", "Could not initialize file backend.", details, exc)

class EbConfigBackendFile(BaseModel):
    chunk_size: int = 4 * 1024 * 1024
    session_apoptosis_s: int = 120
    storage_namespace: str = r'/ebuffers.aqmo.org/'
    storage_dir: str = r'./.ephemeral_buffer_files'

class Eb_DataFileSession():
    def __init__(self, name: str, seek: int = None, limit : int = None):
        self.name = name
        self.seek = seek if seek and seek > 0 else 0
        self.limit = limit if limit else -1
        self.seek_read: int = seek if seek else 0
        self.mm : mmap.mmap | None = None
        self.stream : BytesIO | None = None

    def getSteam(self, mm) -> (int, BytesIO | None):
        if mm is not self.mm:
            self.mm = mm
            if self.stream and not self.stream.closed:
                self.seek_read = self.stream.tell()
                del self.stream
            self.stream = None
        if not self.stream or self.stream.closed:
            stream = BytesIO(self.mm)
            size = stream.getbuffer().nbytes
            if self.limit > 0: size = self.seek + self.limit
            if self.seek_read >= size: return 0, BytesIO()
            self.stream = stream
            self.stream.truncate(size)
            self.stream.seek(self.seek_read)
            logger.debug(r'[backend::file] Session buffer allocated: %s (%d)[%d:%d] %d', self.name, stream.getbuffer().nbytes, self.seek, self.limit, self.seek_read)
            self.seek_read += size
        else: logger.debug(r'[backend::file] Session buffer recovered: %s [%d:%d] %d (readable=%s)', self.name, self.seek, self.limit, self.stream.tell(), str(self.stream.readable()))
        clen = self.stream.getbuffer().nbytes - self.stream.tell()
        return clen, self.stream

#
# TODO: Serious developments missing here: sync read/write, sessions, perf
# - race conditions read/write
# - sessions not implemented
# - perf of reopening mmap

class Eb_DataFile(Eb_Data):

    def __init__(self, ebuffer: BufferEntry, backend: Eb_DataBackend, metadata_path: Path, storage_path: Path):
        self.ebuffer = ebuffer
        self.backend = backend
        self.sessions = {}
        self.tasks : [Task] = []
        self.metadata_path = metadata_path
        self.storage_path = storage_path
        self.size: int = 0
        self.seek_write: int = 0
        self.mm_f = None
        self.mm = None
        self.w_f = None
        try :
            self.storage_path.touch()
            with open(self.metadata_path, r'w') as f:
                f.write(self.ebuffer.model_dump_json())
        except Exception as exc:
            raise Eb_BackendFileCreateError(r'Initial storage creation', exc)

    def _allocate(self):
        f = open(self.storage_path, r'wb+')
        f.seek(self.backend.bk_config.chunk_size-1)
        f.write(bytearray(1))
        f.close()

    def _init_wfile(self) -> bool:
        if self.w_f: return True
        try:
            self.w_f = open(self.storage_path, r'wb+')
        except Exception as exc:
            raise Eb_BackendFileCreateError(r'Initial storage creation', exc)
        return True

    def _close_wfile(self) -> None:
        if self.w_f: self.w_f.close()

    def _init_mmap(self) -> bool:
        if not self.size: return False
        if self.mm: return True
        try:
            self.mm_f = open(self.storage_path, r'rb+')
            self.mm = mmap(self.mm_f.fileno(), 0, flags=MAP_SHARED, prot=PROT_READ)
        except Exception as exc:
            raise Eb_BackendFileCreateError(r'Initial storage creation', exc)
        return True

    def _close_mmap(self) -> None:
        if self.mm: self.mm.close()
        del self.mm; self.mm = None
        if self.mm_f: self.mm_f.close()
        del self.mm_f; self.mm_f = None

    def flush(self) -> bool:
        self._close_mmap()
        with open(self.metadata_path, r'w') as f:
            f.write(self.ebuffer.model_dump_json())
        return True

    def used_size(self) -> int:
        return self.size

    def write(self, chunk) -> None:
        inc = len(chunk)
        nsize = self.size + inc
        if nsize > self.ebuffer.reserved_size:
            raise Eb_BackendFileMaxSizeError("Required=%d, Max=%d." % (nsize, self.ebuffer.reserved_size))

        self._init_wfile()
        seek_read = self.w_f.tell()
        self.w_f.seek(self.seek_write)
        self.w_f.write(chunk)
        self.size += inc
        self.seek_write = self.w_f.tell()
        self.w_f.seek(seek_read)
        if self.mm: self.mm.flush()

    async def apoptosis(self, session: Eb_DataFileSession):
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
        if not self._init_mmap(): return 0, BytesIO()
        if sid not in self.sessions:
            session = Eb_DataFileSession(sid, seek, limit)
            self.sessions[sid] = session
            self.tasks.append(create_task(self.apoptosis(session)))
        else: session = self.sessions[sid]
        return session.getSteam(self.mm)

    def fopen(self, seek: int = None, limit: int = None) -> (int, BytesIO | None) :
        if not self._init_mmap(): return BytesIO(), 0
        stream = BytesIO(self.mm)
        cursor = seek if seek and seek > 0 else 0
        if cursor: stream.seek(cursor)
        if limit and limit > 0: stream.truncate(cursor + limit)
        clen = stream.getbuffer().nbytes - stream.tell()
        return clen, stream

    def destroy(self) -> None :
        for t in self.tasks: t.cancel()
        self.tasks = []
        self._close_mmap()
        self._close_wfile()
        if self.metadata_path: unlink(self.metadata_path)
        if self.storage_path: unlink(self.storage_path)
        self.metadata_path = self.storage_path = None
        logger.debug(r'[backend::file] Buffer data (%s) destroyed', self.ebuffer.uuid)

    def __del__(self) -> None :
        self.destroy()

class Eb_DataBackendFile(Eb_DataBackend):
    def __init__(self, config: EbConfig, bufferCRUD: Eb_BufferCRUD, scheme: str):
        super().__init__(config, bufferCRUD, scheme)
        self.bk_config = config.open_section(r'backend::file', EbConfigBackendFile)
        self._checkStorage()

    def _checkStorage(self):
        self.onDisk_folder_path = Path(self.bk_config.storage_dir)
        try:
            if not self.onDisk_folder_path.exists():
                self.onDisk_folder_path.mkdir(exist_ok=True)
            currentDate = datetime.now().strftime("%Y%m%d%H%M%S")
            # Try to create a temporary file
            test_file = Path(f'{self.onDisk_folder_path}/.__test__{currentDate}.txt')
            data = currentDate.encode(r'utf-8')
            with open(test_file, r'wb') as f:
                f.write(data)
        except Exception as e:
            raise Eb_BackendFileInitStorage(r'Could not create storage dir.', e)
        try:
            # Try to mmap the file
            with open(test_file, r'r+b') as f:
                mm = mmap(f.fileno(), 0, flags=MAP_PRIVATE, prot=PROT_WRITE | PROT_READ)
                rdata = mm.read(8)
                if rdata != data[:8]: raise Exception(r'Could not done mmap reading: %s!=%s' % (str(data), str(rdata)))
                data = b'remove content'
                mm.seek(0); rdata = mm.write(data)
                mm.seek(0); rdata = mm.read(8)
                if rdata != data[:8]: raise Exception(r'Invalid mmap reading: %s!=%s' % (str(data), str(rdata)))
                mm.close()
        except Exception as e:
            raise Eb_BackendFileInitStorage(r'Could not use storage dir.', e)
        finally:
            unlink(test_file)

    def newData(self, ebuffer: BufferEntry) -> Eb_DataFile:
        metadata_path = Path(f'{self.onDisk_folder_path}/{ebuffer.uuid}.json')
        storage_path = Path(f'{self.onDisk_folder_path}/{ebuffer.uuid}.data')
        return Eb_DataFile(ebuffer, self, metadata_path, storage_path)

    def setPath(self, ebuffer: BufferEntry):
        ebuffer.path = self.schema + self.bk_config.storage_namespace + str(ebuffer.uuid)

Eb_DataBackend.addBackend(r'file://', Eb_DataBackendFile)

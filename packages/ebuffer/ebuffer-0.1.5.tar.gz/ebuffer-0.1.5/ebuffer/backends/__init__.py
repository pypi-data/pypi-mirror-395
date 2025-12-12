from ebuffer.backends.backends import Eb_DataBackend, Eb_Data

from ebuffer.backends.backends import Eb_BackendDuplicatedError, Eb_BackendMissingError
from ebuffer.backends.backends import Eb_BackendMissingBufferError, Eb_BackendWriteError, Eb_BackendReadError
from ebuffer.backends.memory import Eb_BackendMemoryMaxSizeError
from ebuffer.backends.mmap import Eb_BackendFileMaxSizeError

DataAllocExceptionList = {}
DataWriteExceptionList = \
    Eb_BackendMissingBufferError().model() | \
    Eb_BackendMemoryMaxSizeError().model() | \
    Eb_BackendFileMaxSizeError().model()

DataReadExceptionList = \
    Eb_BackendMissingBufferError().model()

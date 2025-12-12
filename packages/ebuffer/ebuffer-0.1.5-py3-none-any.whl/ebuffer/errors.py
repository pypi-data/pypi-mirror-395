from functools import wraps
from traceback import format_exc
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from ebuffer.models_common import Message
from ebuffer.config import logger

def a_exc2msg(f):
    @wraps(f)
    async def inner(*a, **d):
        if r'request' not in d:
            return JSONResponse(status_code=500, content=Eb_HTTP_InternalError(Exception('Missing request')))
        request = d[r'request']
        #print("++++++++++++++++++++ ---------------------\n", a, d, "\n++++++++++++++++++++ ---------------------")
        try: return await f(*a, **d)
        except Eb_Exception as exc: return exc.response(request)
        except Exception as exc: return Eb_HTTP_InternalError(exc).response(request)
    return inner

def exc2msg(f):
    @wraps(f)
    def inner(*a, **d):
        if r'request' not in d:
            return JSONResponse(status_code=500, content=Eb_HTTP_InternalError(Exception('Missing request')))
        request = d[r'request']
        #print("++++++++++++++++++++ ---------------------\n", a, d, "\n++++++++++++++++++++ ---------------------")
        try: return f(*a, **d)
        except Eb_Exception as exc: return exc.response(request)
        except Exception as exc: return Eb_HTTP_InternalError(exc).response(request)
    return inner

class Eb_Exception(Exception):
    def __init__(self, status: int, name: str, description: str, details: [str | dict] = r'', exc: Exception = None):
        self.status = status
        self.name = name
        self.description = description
        self.details = str(exc) if not details and exc else details
        self.exc = exc
        self.headers = {}
        super().__init__(description, status, details, exc)

    def response(self, request: Request):
        if self.exc and not isinstance(self.exc, HTTPException): logger.debug(r"Exception: %s: %s", str(self.exc), format_exc())
        return JSONResponse(status_code=self.status, headers=self.headers, content=Message(self).model_dump())

    def model(self):
        return {self.status: {"model": Message, "description": self.description}}

    def desc(self):
        return f"{self.description}: {str(self.details)}"

class Eb_HTTP_Error(Eb_Exception):
    def __init__(self, exc: HTTPException = None, detail: str = r''):
        super().__init__(exc.status_code if exc and hasattr(exc, r'status_code') else 500, "HttpError", "Http Error.", detail, exc)

class Eb_HTTP_InternalError(Eb_Exception):
    def __init__(self, exc: HTTPException = None, detail: str = r''):
        super().__init__(exc.status_code if exc and hasattr(exc, r'status_code') else 500, "InternalError", "Internal Error.", detail, exc)

class Eb_HTTP_Validation_Error(Eb_Exception):
    def __init__(self, exc: RequestValidationError = None):
        super().__init__(422,
                         "HttpValidationError",
                         "One or more request parameters failed validation.", exc.errors() if exc else None, exc)
    def model(self):
        return {422: {"model": Message, "description": self.description, "content": {"application/json": { "example": {
                "name": "HttpValidationError",
                "message": "One or more request parameters failed validation.",
                "error_level": -2,
                "details": {"detail": [{"loc": ["string", 0], "msg": "string", "type": "string"  }]},
                "date": "string"
                }}}}}

class Eb_HTTP_MissingAuth_Error(Eb_Exception):
    def __init__(self, headers: dict = {}):
        super().__init__(401,
                         "HttpMissingAuthError",
                         "Missing authentication credentials.")
        self.headers = headers

class Eb_HouseKeepingError(Eb_Exception):
    def __init__(self, exc: Exception = None):
        super().__init__(431, "HouseKeepingError", "Could not finish an housekeeping session.", r'Aborted.', exc)

class Eb_TagSyntaxError(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(432, "TagSyntaxError", "Invalid tag.", details)

from typing import Annotated
from fastapi import APIRouter
from fastapi import Request, Depends, Path, Query, Body
from fastapi.responses import StreamingResponse, Response
from sqlmodel import Session

from ebuffer.application import app_g
from ebuffer.errors import a_exc2msg
from ebuffer.errors import Eb_HTTP_Validation_Error, Eb_TagSyntaxError
from ebuffer.auth import AuthExceptionList
from ebuffer.routers.routes_auth import check_token

from ebuffer.models_common import UserId
from ebuffer.models_buffer import BufferRequest, Buffer

from ebuffer.database import BufferEntry, BufferExceptionList
from ebuffer.apiebuffer import Eb_BufferInvalid
from ebuffer.backends import DataAllocExceptionList, DataWriteExceptionList, DataReadExceptionList

router = APIRouter(tags=["Buffers"], prefix="/eph_buffer")
router.rest_metadata = {
    "name": "Buffers",
    "description": "A *Buffer* as defined for ephemeral buffers",
    "externalDocs": {
        "description": "Items external docs",
        "url": "https://ebuffer.aqmo.org/",
    },
}

#
# -- Ephemeral Buffer DB Management
#

@router.post(
    "",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | DataAllocExceptionList | Eb_TagSyntaxError().model(),
    summary=r'Create a new Ephemeral Buffer.',
    description=r'Create a new Ephemeral Buffer. Parameters are given in the body of can be overloaded by the query parameters. By default the operation is non-blocking, as soon as a buffer could be initialized, the storage allocation is performed in background and my fail. When the request is as blocking, the buffer returns when the allocation is effective. Warning: for some backends and deployments, this may raise timeout event.',
    response_description=r'The newly created ephemeral buffer descriptor, including its UUID. Be aware that the ephemeral buffer status is typically set to "*initialized*" and not effectively created by the storage backend.',
)
@a_exc2msg
async def createBuffer(
    request: Request,
    ebuffer: Annotated[
        BufferRequest | int,
        Body(
            title="A descriptor of the ephemeral buffer, or directly the reserved size.", examples=[BufferRequest(reserved_size=65530, lifespan=3600, tags=["ISOK", "APP::DONE"])]
        ),
    ] = app_g.config.base.default_size,
    size: Annotated[int | None, Query(title="The reserved size for the buffer", ge=1, le=app_g.config.base.max_size)] = None,
    lifespan: Annotated[int | None, Query(title="The allocation time.", ge=0, le=app_g.config.base.max_life_span)] = None,
    blocking: Annotated[bool | None, Query(title="Set the buffer creation as blocking, ensuring a complete allocation of the buffer space.")] = False,
    user: UserId = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Buffer:
    if isinstance(ebuffer, int):
        ebuffer = BufferRequest(reserved_size=ebuffer)
    ebuffer = BufferEntry(ebuffer, startup_time=app_g.config.base.startup_time)
    if size:     ebuffer.reserved_size = size
    if lifespan: ebuffer.lifespan      = lifespan
    return await app_g.bufferAPI.create(ebuffer, blocking, user, session)

@router.get(
    "",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | BufferExceptionList | Eb_TagSyntaxError().model() | {200: {"content": {"text/plain": { "example": "42" }}}},
    summary=r'Count or fetch the list of ephemeral buffer.',
    description=r'Look for all the ephemeral buffers matching the filtering criteria. Be aware that unless the count is requested, the number of results is limited and has a default maximum value defined during the deployment. The full list can be retrieved with a loop and using the query parameters "*limit*" and "*skip*". Additional filters can be applied on the owner and the tags (all or them, or any of them).',
    response_description="Returns either the list of buffers' status or the number of elements.",
)
@a_exc2msg
async def searchBuffer(
    request: Request,
    limit: Annotated[int | None, Query(title="Maximum number of element returned", ge=1, le=app_g.config.base.search_max_limit)] = app_g.config.base.search_limit,
    skip: Annotated[int | None, Query(title="Number of element skipped", ge=0)] = 0,
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    tags: Annotated[list[str] | None, Query(title="A tag to match. The option can be added multiple times.")] = [],
    all: Annotated[bool | None, Query(title="Whether the ephemeral buffer matches all tags or just one tag.")] = False,
    count: Annotated[bool | None, Query(title="Returns the number of elements, and not the list itself. The parameters '*skip*' and '*limit*' are ignored.")] = False,
    user: UserId = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[Buffer] | int:
    result = await app_g.bufferAPI.search(session, user, limit, skip, owner, tags, all, count)
    return Response(content=str(result), media_type=r'text/plain') if isinstance(result, int) else result

#
# -- Ephemeral Buffer Object Management
#

@router.get(
    "/{uid}",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | BufferExceptionList,
    summary=r'Get an ephemeral buffer.',
    description=r'Get the descriptor of an ephemeral buffer.',
    response_description="The status of an ephemeral buffer, including its status, the remaining lifetime, and the current effective size.",
)
@a_exc2msg
async def getBuffer(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the buffer", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: UserId = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Buffer:
    return await app_g.bufferAPI.get(uid, owner, user, session)

@router.delete(
    "/{uid}",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | BufferExceptionList | Eb_BufferInvalid().model(),
    summary=r'Delete an ephemeral buffer.',
    description=r'Launch the destruction of an ephemeral buffer. If the buffer has already a deleted state, the operation is ignored. The destruction is started and is effectively completed in the background.',
    response_description="The status of the ephemeral buffer before destruction.",
)
@a_exc2msg
async def delBuffer(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the buffer", min_length=36, max_length=36)],
    user: UserId = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Buffer:
    return await app_g.bufferAPI.delete(uid, user, session)

#
# -- Ephemeral Buffer TAGS Management
#

@router.get(
    "/{uid}/tags",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | BufferExceptionList | {200: {"content": {"application/json": { "example": '["ISOK","DONE"]' }}}},
    summary=r'Get ephemeral buffer tags.',
    description=r'Return the list of tags associated to an ephemeral buffer.',
    response_description="The list of tokens as a Json list ot UTF-8 strings.",
)
@a_exc2msg
async def getTagsFromBuffer(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the buffer", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: UserId = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[str]:
    return await app_g.bufferAPI.getTags(uid, owner, user, session)


@router.post(
    "/{uid}/tags/{tag}",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | BufferExceptionList | Eb_TagSyntaxError().model(),
    summary=r'Add a tag to an ephemeral buffer.',
    description=r'Append a new tag to the list of tags of an ephemeral buffer. The tag order is kept and can be duplicated.',
    response_description="The status of the modified ephemeral buffer, including the new tag.",
)
@a_exc2msg
async def addTagToBuffer(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the buffer", min_length=36, max_length=36)],
    tag: Annotated[
        str,
        Path(
            title="A tag, an UTF-8 string with a size between %d and %d." % (app_g.config.base.tag_min_size, app_g.config.base.tag_max_size),
            min_length=app_g.config.base.tag_min_size,
            max_length=app_g.config.base.tag_max_size,
        ),
    ],
    user: UserId = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Buffer:
    return await app_g.bufferAPI.addTag(uid, tag, user, session)

#
# -- Ephemeral Buffer DATA Management
#

@router.put(
    "/{uid}/data",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | BufferExceptionList | DataWriteExceptionList,
    summary=r'Put binary data into an ephemeral buffer.',
    description=r'Send and store a stream of bytes at the end of the ephemeral buffer. May raise an error if too much data is sent. In that case, the effective impact on the buffer content is backend dependent.',
    response_description="The status of the modified ephemeral buffer, including the updated size.",
)
@a_exc2msg
async def writeBuffer(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the buffer", min_length=36, max_length=36)],
    user: UserId = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Buffer:
    return await app_g.bufferAPI.write(request.stream(), uid, user, session)

@router.get(
    "/{uid}/data",
    responses=Eb_HTTP_Validation_Error().model() | AuthExceptionList | BufferExceptionList | DataReadExceptionList | {200: {"content": {"application/octet-stream": { "example": "0123456789ABCDEF" }}}},
    summary=r'Fetch binary data from the ephemeral buffer.',
    description=r'Retrieve the buffer data in binary. A partial part of the raw data can be extracted using the delimiters "*seek*" marking the beginning, and "*limit*" fixing the maximum size. Multiple reading streams can be done in parallel, each of them operating independently on the binary data. A session identifier "*sid*" can be provided in order to keep track of the current status of the read, either if more data was added to the buffer or if the end of the buffer was not reached by previous reads. The behavior of concurrent reads with the same session identifier is implementation dependent.',
    response_description="The raw stream of binary data from the ephemeral buffer."
)
@a_exc2msg
async def readBuffer(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the buffer", min_length=36, max_length=36)],
    sid: Annotated[str | None, Query(title="The Stream ID of the read", min_length=8, max_length=36)] = None,
    seek: Annotated[int | None, Query(title="Start read at offset", ge=0)] = None,
    limit: Annotated[int | None, Query(title="Maximum bytes read", ge=1)] = None,
    user: UserId = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> StreamingResponse:
    clen, stream = await app_g.bufferAPI.read(uid, sid, seek, limit, user, session)
    return StreamingResponse(stream, media_type="application/octet-stream", headers={"Content-Length": str(clen)})

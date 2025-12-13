from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasicCredentials

from ebuffer.errors import exc2msg
from ebuffer.errors import Eb_HTTP_Validation_Error
from ebuffer.errors import Eb_HTTP_MissingAuth_Error
from ebuffer.auth import LoginExceptionList

from ebuffer.models_common import UserCred, UserId, MessageLogin
from ebuffer.application import app_g

def check_token_only(credentials: HTTPAuthorizationCredentials = Depends(app_g.security_token)) -> UserId:
    token = credentials.credentials
    return app_g.auth.verify_token(token)

def check_token(bearer: Optional[HTTPAuthorizationCredentials] = Depends(app_g.security_token),
                basic: Optional[HTTPBasicCredentials] = Depends(app_g.security_cred)) -> UserId:
    if bearer:
        return app_g.auth.verify_token(bearer.scheme, bearer.credentials)
    elif basic:
        return app_g.auth.verify_basic(basic.username, basic.password)
    else:
        raise Eb_HTTP_MissingAuth_Error(app_g.auth.getRealmHeader())

#
# -- Authentication
#
router = APIRouter(prefix="/auth", tags=["Authentication"])
router.rest_metadata = {
    "name": "Authentication",
    "description": "Authentication API, details may depends on the choosend backend.",
}

@router.post(
    "/login",
    responses=Eb_HTTP_Validation_Error().model() | LoginExceptionList,
    summary=r'Login to the ephemeral buffer service with credentials.',
    description=r'Login using credentials privided in the body. Errors raised may depend on the backend used, see documentation.',
    response_description="A standard message with an extra member **token** that can be used with a *Bearer authentication* mechanism.",
)
@exc2msg
def loginGet(
    request: Request,
    user: Annotated[UserCred, Body(title="The user's credentials.", examples=[UserCred(username=r'toto', password=r'motdepasse')])]
) -> MessageLogin:
    return app_g.auth.login(user, dict(request.headers))

@router.get(
    "/login",
    responses=Eb_HTTP_Validation_Error().model() | LoginExceptionList,
    summary=r'Login to the ephemeral buffer service with SSO.',
    description=r'Login requiring a web browser for logging with the IdP. Errors raised may depend on the backend used, see documentation.',
    response_description="A standard message with an extra member **token** that can be used with a *Bearer authentication* mechanism.",
)
@exc2msg
def loginPost(
    request: Request,
) -> MessageLogin:
    return app_g.auth.login(None, dict(request.headers))

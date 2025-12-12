import requests
from pydantic import BaseModel
from ebuffer.models_common import UserCred, UserId, MessageLogin
from ebuffer.config import EbConfig, logger
from ebuffer.errors import Eb_Exception
from ebuffer.auth import Eb_Auth, Eb_AuthError, Eb_AuthExpired

class Eb_OI_ConnectError(Eb_Exception):
    def __init__(self, srv: str = r'', exc: Exception = None):
        super().__init__(501, "OIDConnErr", "Could not connect to the OpenID server.", r'Server: %s' % srv, exc)

class Eb_OI_InternalError(Eb_Exception):
    def __init__(self, exc: Exception = None):
        super().__init__(500, "OIDInternalError", "OIDC Internal error.", "Check server configuration.", exc)

class Eb_OI_LoginError(Eb_Exception):
    def __init__(self, code: int = -1):
        super().__init__(401, "OIDLoginErr", "Could not login with OIDC credentials.", r'Code: %d' % code)

OIDLoginExceptionList = \
    Eb_OI_InternalError().model() | \
    Eb_OI_ConnectError().model() | \
    Eb_OI_LoginError().model()

OIDAuthExceptionList = \
    Eb_OI_InternalError().model() | \
    Eb_AuthError().model() | \
    Eb_AuthExpired().model()

class EbConfigOpenID(BaseModel):
    openid_base_url: str = r''
    openid_client_id: str = r''
    openid_client_secret: str = r''
    access_token_url: str
    introspect_url: str
    user_info_url: str
    logout_url: str

    def __init__(self, **kw):
        url = kw[r'openid_base_url'] if r'openid_base_url' in kw else r'https://localhost/realms'
        kw[r'access_token_url'] = f"{url}/protocol/openid-connect/token"
        kw[r'introspect_url'] = f"{url}/protocol/openid-connect/token/introspect"
        kw[r'user_info_url'] = f"{url}/protocol/openid-connect/userinfo"
        kw[r'logout_url'] = f"{url}/protocol/openid-connect/logout"
        super().__init__(**kw)

class Eb_AuthOpenID(Eb_Auth):

    def __init__(self, config: EbConfig, name : str):
        config = config.open_section(name, EbConfigOpenID)
        super().__init__(config, name)

    def login(self, user: UserCred | None, headers: dict) -> MessageLogin:
        logger.debug(r"----- OpenID %s ------", str(user))
        payload = {
            "client_id": self.config.openid_client_id,
            "client_secret": self.config.openid_client_secret,
            "grant_type": "password",
            "username": user.username,
            "password": user.password,
            "scope": "openid",
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = requests.post(self.config.access_token_url, data=payload, headers=headers)
        except requests.exceptions.ConnectionError as e:
            raise Eb_OI_ConnectError(self.config.access_token_url, e)

        if response.status_code != 200:
            raise Eb_OI_LoginError(response.status_code)

        result = response.json()
        return MessageLogin(result["access_token"])

    def verify_token(self, scheme: str, token: str) -> UserId:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payloads = {
            "token": token,
            "client_id": self.config.openid_client_id,
            "client_secret": self.config.openid_client_secret,
        }

        try:
            response = requests.post(self.config.introspect_url, data=payloads, headers=headers)
            if response.status_code != 200:
                raise Eb_AuthError(response.status_code)

            token_info = response.json()
            if not token_info.get("active"):
                raise Eb_AuthExpired(str(token_info))

            return UserId(**token_info)

        except requests.RequestException as e:
            raise Eb_OI_InternalError(e)

    def verify_basic(self, user: str, password: str) -> UserId:
        raise Eb_AuthError(-1)

Eb_Auth.addAuth(r'auth::openid', Eb_AuthOpenID)

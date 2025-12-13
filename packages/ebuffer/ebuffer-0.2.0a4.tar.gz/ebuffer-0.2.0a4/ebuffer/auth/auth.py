from ebuffer.config import EbConfig
from ebuffer.models_common import UserCred, UserId, MessageLogin
from ebuffer.errors import Eb_Exception

class Eb_AuthError(Eb_Exception):
    def __init__(self, code: int = -1):
        super().__init__(401, "AuthError", "Invalid credentials.", r'Code: %d' % code)

class Eb_AuthExpired(Eb_Exception):
    def __init__(self, status: str = r''):
        super().__init__(401, "AuthExpired", "Invalid or expired token.", r'Status: %s' % status)

class Eb_AuthDuplicatedError(Eb_Exception):
    def __init__(self, scheme: str):
        super().__init__(440, "AuthDuplicatedError", "Multiple authentication defined with the same scheme (%s)." % scheme, "Check authentication installation.")

class Eb_AuthMissingError(Eb_Exception):
    def __init__(self, scheme: str):
        super().__init__(440, "AuthMissingError", "Authentication '%s' not found." % scheme, "Check authentication installation.")

class Eb_Auth():
    g_auths: dict = {}

    def __init__(self, config: EbConfig, name : str = r'none'):
        self.config = config
        self.name : str = name

    @staticmethod
    def addAuth(name, auth_class):
        if name in Eb_Auth.g_auths: raise Eb_AuthDuplicatedError(name)
        Eb_Auth.g_auths[name] = auth_class

    @staticmethod
    def getAuth(config: EbConfig):
        name = config.base.auth_backend
        if name not in Eb_Auth.g_auths: raise Eb_AuthMissingError(name)
        return Eb_Auth.g_auths[name](config, name)

    def login(self, user: UserCred | None, headers: dict) -> MessageLogin:
        return MessageLogin(access_token=r'b3BlbmJhcg==')

    def verify_token(self, scheme: str, token: str) -> UserId:
        return UserId(name=self.config.base.default_user, email=self.config.base.default_email)

    def verify_basic(self, user: str, password: str) -> UserId:
        return UserId(name=self.config.base.default_user, email=self.config.base.default_email)

    def getRealmHeader(self) -> dict:
        return {}

Eb_Auth.addAuth(r'none', Eb_Auth)

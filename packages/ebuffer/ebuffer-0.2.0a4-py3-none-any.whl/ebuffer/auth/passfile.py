from json import loads as jsloads
from re import compile as re_compile
from json import loads as jsloads
from re import compile as re_compile
from pydantic import BaseModel
from ebuffer.models_common import UserCred, UserId, MessageLogin
from ebuffer.config import EbConfig, logger
from ebuffer.errors import Eb_Exception
from ebuffer.auth import Eb_Auth, Eb_AuthError, Eb_AuthExpired
from base64 import b64encode, b64decode
from os import urandom
from hashlib import sha256 as digest_method
import hmac

class Eb_AuthFile_LoginError(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(401, "AuthFileLoginError", "Could not login with local credentials.", details)

class Eb_AuthFile_InternalError(Eb_Exception):
    def __init__(self, exc : Exception = None):
        super().__init__(401, "AuthFileInternalError", "File based password error.", r'Invalid configuration', exc)

PassFileLoginExceptionList = \
    Eb_AuthFile_LoginError().model()

PassFileAuthExceptionList = \
    Eb_AuthError().model() | \
    Eb_AuthExpired().model()

class EbConfigPassFile(BaseModel):
    header_pass_through : bool = False
    header_check_kw: str = r'shib-authentication-method'
    header_check_val: str = r'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport'
    header_uid_kw: str = r'mail'
    header_name_kw: str = r'displayname'
    server_key: str = 'example'
    user_list : str = []  # Json

class Eb_AutPassFile(Eb_Auth):
    g_reEmail = re_compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def __init__(self, config: EbConfig, name : str):
        config = config.open_section(name, EbConfigPassFile)
        super().__init__(config, name)
        self.passdb = {}
        self.bearerdb = {}
        self.session_key : bytes = self._generate_hmac_key()
        try:
            user_list = config.user_list if isinstance(config.user_list, list) else jsloads(config.user_list)
            for (user, pasw, info) in user_list:
                self._add_user(user, pasw, info)
        except Exception as exc:
            raise Eb_AuthFile_InternalError(exc)

    def _generate_hmac_key(self, length=256) -> bytes:
        return self.config.server_key.encode('utf-8') if self.config.server_key else urandom(length)

    def _get_msgkey(self, user: str) -> bytes:
        return f'Ebuffer for {user}'.encode('utf-8')

    def _sign_hmac(self, user: str) -> str:
        mac = hmac.new(self.session_key, msg=self._get_msgkey(user), digestmod=digest_method)
        return b64encode(mac.digest()).decode('utf-8')

    def _verify_hmac(self, user: str, signature_b64: str) -> bool:
        mac = hmac.new(self.session_key, msg=self._get_msgkey(user), digestmod=digest_method)
        signature = b64decode(signature_b64)
        return hmac.compare_digest(mac.digest(), signature)

    def _user_from_bearer(self, bearerB64: str) -> UserId:
        try:
            if bearerB64 in self.bearerdb: return UserId(**self.bearerdb[bearerB64])

            bearer = b64decode(bearerB64).decode(r'utf8')
            if bearer.count(r':') != 1: raise Eb_AuthFile_LoginError(r'Malformed bearer', bearer)
            (user, signature_b64) = bearer.split(r':')
            valid = self._verify_hmac(user, signature_b64)
            if not valid:
                logger.warning(r"Rejected user %s", str(user))
                raise Eb_AuthFile_LoginError(r' Unauthorized token.')

            if user in self.passdb: info = self.passdb[user]
            else:
                email = user if self.g_reEmail.match(user) else f'{user}@aqmo.org'
                info = self._add_user(user, None, {r'name': r'<lost>', r'email' : email})
            logger.info(f"User {user} granted")
            return UserId(**info)
        except ValueError as e:         raise Eb_AuthFile_LoginError(f"Base64 decoding error : {bearerB64}")  from e
        except TypeError as e:          raise Eb_AuthFile_InternalError(f"Type error : {type(bearerB64)}")    from e
        except UnicodeDecodeError as e: raise Eb_AuthFile_LoginError(f"Unicode decoding error : {bearerB64}") from e

    def _add_user(self, user: str , pasw: str, info: dict) -> dict:
        if r'email' not in info: raise Eb_AuthFile_LoginError(r'Missing email in user DB')
        email = info[r'email']
        if not self.g_reEmail.match(email): raise Eb_AuthFile_LoginError(f'Invalid email: {email}')
        if r'name' not in info: info[r'name'] = user

        if not pasw:
            pasw = self._sign_hmac(user)

        bearer = b64encode(f"{user}:{pasw}".encode()).decode()
        self.passdb[user] = (pasw, info)
        logger.info(f'New user: {user}: {pasw} [{info}]' )

        info[r'access_token'] = bearer
        self.bearerdb[bearer] = info
        return info

    def login(self, user: UserCred | None, headers: dict) -> MessageLogin:
        #logger.debug("----- Login  %s ------\n%s\n", str(user), str(headers))
        userInfo = None
        if self.config.header_pass_through:
            check = self.config.header_check_kw
            content = self.config.header_check_val
            check = check.strip().lower()
            content = content.strip().lower()
            activated, h_uid, h_name = False, None, None
            for h, v in headers.items():
                hs = h.strip().lower()
                vs = v.strip().lower()
                if hs == check and content == vs: activated = True
                if hs == self.config.header_uid_kw: h_uid = v
                if hs == self.config.header_name_kw: h_name = v
            if activated:
                if not h_uid or not h_name: raise Eb_AuthFile_LoginError(r'Missing data for SSO login.')
                logger.debug(r"----- Header  %s ------", str(h_uid))
                if h_uid not in self.passdb:
                    email = user if self.g_reEmail.match(user) else f'{user}@aqmo.org'
                    self._add_user(h_uid, None, {r'name': h_name, r'email' : email})
                password, userInfo = self.passdb[h_uid]
                return MessageLogin(access_token=userInfo['access_token'])

        if user:
            logger.debug(r"----- PassFile %s ------", str(user))
            name = user.username
            if name not in self.passdb: raise Eb_AuthFile_LoginError(r'User %s not found.' % name)
            password, userInfo = self.passdb[name]
            if user.password != password: raise Eb_AuthFile_LoginError(r'Invalid password.')
        else:
            raise Eb_AuthFile_LoginError(r'Missing credential data for login.')

        return MessageLogin(access_token=userInfo['access_token'])

    def verify_token(self, scheme: str, token: str) -> UserId:
        if scheme == r'Bearer': return self._user_from_bearer(token)
        else:
            raise Eb_AuthFile_LoginError(f'Unsupported token scheme {scheme}.')

    def verify_basic(self, user: str, password: str) -> UserId:
        token = b64encode(f"{user}:{password}".encode()).decode()
        if token not in self.bearerdb: raise Eb_AuthError(-1)
        return UserId(**self.bearerdb[token])

    def getRealmHeader(self) -> dict:
        return {
            "WWW-Authenticate": 'Basic realm="Access to the secure endpoint", charset="UTF-8", Bearer'
        }

Eb_Auth.addAuth(r'auth::passfile', Eb_AutPassFile)

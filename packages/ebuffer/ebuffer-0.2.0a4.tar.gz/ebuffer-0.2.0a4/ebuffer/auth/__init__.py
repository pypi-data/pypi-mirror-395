from ebuffer.auth.auth import Eb_Auth

from ebuffer.auth.auth import Eb_AuthDuplicatedError, Eb_AuthMissingError
from ebuffer.auth.auth import Eb_AuthError, Eb_AuthExpired
from ebuffer.auth.openid import Eb_OI_ConnectError, Eb_OI_InternalError, Eb_OI_LoginError
from ebuffer.auth.passfile import Eb_AuthFile_LoginError

from ebuffer.auth.openid import OIDLoginExceptionList
from ebuffer.auth.openid import OIDAuthExceptionList

from ebuffer.auth.passfile import PassFileLoginExceptionList
from ebuffer.auth.passfile import PassFileAuthExceptionList

LoginExceptionList = {} | OIDLoginExceptionList | PassFileLoginExceptionList
AuthExceptionList = {} | OIDAuthExceptionList | PassFileAuthExceptionList

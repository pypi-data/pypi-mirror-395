from os import getenv
from asyncio import create_task, sleep
from traceback import format_exc
from ebuffer.config import EbConfig, logger
from ebuffer.database import Eb_Database
from ebuffer.auth import Eb_Auth
from ebuffer.apiebuffer import Eb_BufferAPI
from fastapi.security import HTTPBearer, HTTPBasic

class Eb_Application():

    def __init__(self):
        self.regexp_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.config = EbConfig(inifile=getenv(r'EBUFFER_INI', r'eb.ini'), secretfile=getenv(r'EBUFFER_SECRET_INI', r'.eb-secret.ini'))
        self.db = Eb_Database(self.config)
        self.bufferAPI = Eb_BufferAPI(self.config)
        self.auth = Eb_Auth.getAuth(self.config)
        self.security_token = HTTPBearer(auto_error=False)
        self.security_cred = HTTPBasic(auto_error=False)

    #
    # Housekeeping
    #
    async def housekeeping(self, start: bool = False) -> None:
        interval = self.config.base.housekeeping_interval
        await sleep(interval)
        #logger.debug(r"Start housekeeping (%ds) %s", interval, r'Initial' if start else r'')
        try:
            session = next(self.db.get_session())
            await self.bufferAPI.housekeeping(session, interval, start)
        except Exception as e:
            logger.error(r"Could not finish a housekeeping session %s: %s", str(e), format_exc())
            # raise Eb_HouseKeepingError(e)
        finally:
            create_task(self.housekeeping())

    def start(self):
        create_task(self.housekeeping(start=True))

    def destroy(self):
        self.bufferAPI.destroy()
        del self.db
        self.db = None

app_g = Eb_Application()

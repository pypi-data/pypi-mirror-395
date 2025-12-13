from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import StaticPool, QueuePool
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import Engine
from configparser import SectionProxy
from pydantic import BaseModel
from traceback import format_exc

from ebuffer.errors import Eb_Exception
from ebuffer.config import logger

class Eb_DBError(Eb_Exception):
    def __init__(self, details: str = r'Internal error', exc: Exception = None):
        super().__init__(500, "DBError", "Error in DB.", details, exc)

class EbConfigDatase(BaseModel):
    url: str = r'sqlite://'  # In memory database
    clean_startup: bool = False
    connect_args: dict = {"check_same_thread": False}

class Eb_Database:
    Default_pool_class = StaticPool
    #Default_pool_class = QueuePool

    def __init__(self, config: [SectionProxy | None] = None):
        if config: self.config = config.open_section(r'db', EbConfigDatase)
        else:      self.config = EbConfigDatase()
        self.create_db_and_tables()

    def create_db_and_tables(self) -> Engine:
        logger.debug(r'[DB] Create database %s' % self.config.url)
        self.engine = create_engine(self.config.url, connect_args=self.config.connect_args, poolclass=self.Default_pool_class)
        try:
            if self.config.clean_startup:
                logger.warning(r'[DB] Clean database %s' % self.config.url)
                SQLModel.metadata.drop_all(self.engine)
            SQLModel.metadata.create_all(self.engine)
            return self.engine

        except OperationalError as e:
            logger.error(r"Could not create SQL Models: %s", (str(e)))
            raise Eb_DBError("Internal Error DX001", e)

    def get_session(self):
        #logger.warning(r'RESTART GET_SESSION')
        try:
            with Session(self.engine) as session:
                yield session
        except Eb_Exception as e: raise e
        except Exception as e:
            logger.error('Could not yield a DB session (%s): %s', type(e), str(e))
            #raise Eb_DBError("Internal Error DX002", e)
            self.engine = create_engine(self.config.url, connect_args=self.config.connect_args, poolclass=self.Default_pool_class)
            return self.get_session()

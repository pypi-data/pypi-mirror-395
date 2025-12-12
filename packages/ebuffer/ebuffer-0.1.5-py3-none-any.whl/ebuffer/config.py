import logging
import configparser
from pydantic import BaseModel

logger = logging.getLogger(r'ebuffer')

class EbConfigDefault(BaseModel):
    root_path : str = r'api/v1'
    default_life_span: int = 300
    max_life_span: int = 3600
    tag_min_size: int = 3
    tag_max_size: int = 256

    log_level: int = 0
    data_dir : str = r'./'
    startup_time: int = 10
    grace_time: int = 2
    error_grace_time: int = 120
    housekeeping_interval: int = 5
    search_limit: int = 20
    search_max_limit: int = 300

    storage_backend: str = r'memory://'
    default_size: int = 65530
    max_size: int = 2500 * 1024*1024

    auth_backend: str = r'passfile'
    default_user: str = r'anonymous'
    default_email: str = r'anonymous@anonymous.org'


class EbConfig:
    g_default = r'default'
    def __init__(self, inifile=r'eb.ini', secretfile=r'.eb-secret.ini'):
        self.config = configparser.ConfigParser(default_section=self.g_default)
        self.base = EbConfigDefault()
        self.config.read((inifile, secretfile))
        #import sys; self.config.write(sys.stderr)
        if self.g_default in self.config:
            self.base = EbConfigDefault(**self.config[self.g_default])
            rp = self.base.root_path
            if rp[0] != r'/': self.base.root_path = f'/{rp}'

    def open_section(self, name, sectype):
        if not hasattr(self, name):
            sec = sectype(**self.config[name]) if name in self.config else sectype()
            setattr(self, name, sec)
        return getattr(self, name)

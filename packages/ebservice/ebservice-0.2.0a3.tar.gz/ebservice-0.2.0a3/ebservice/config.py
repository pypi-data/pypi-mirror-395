import logging
import configparser
from pydantic import BaseModel

logger = logging.getLogger(r'ebservice')

class AppMsConfigDefault(BaseModel):
    root_path : str = r'api/v1'
    log_level: int = 0
    data_dir : str = r'./'
    tag_min_size: int = 3
    tag_max_size: int = 256

    grace_time: int = 2
    error_grace_time: int = 120
    housekeeping_interval: int = 5
    search_limit: int = 20
    search_max_limit: int = 300

    execution_backend: str = r'cwl://'

    auth_backend: str = r'auth::passfile'
    default_user: str = r'anonymous'
    default_email: str = r'anonymous@anonymous.org'


class AppMsConfig:
    g_default = r'default'
    def __init__(self, inifile=r'ebservice.ini', secretfile=r'.ebservice-secret.ini'):
        self.config = configparser.ConfigParser(default_section=self.g_default)
        self.base = AppMsConfigDefault()
        self.config.read((inifile, secretfile))
        #import sys; self.config.write(sys.stderr)
        if self.g_default in self.config:
            self.base = AppMsConfigDefault(**self.config[self.g_default])
            rp = self.base.root_path
            if rp[0] != r'/': self.base.root_path = f'/{rp}'

    def open_section(self, name, sectype):
        if not hasattr(self, name):
            sec = sectype(**self.config[name]) if name in self.config else sectype()
            setattr(self, name, sec)
        return getattr(self, name)

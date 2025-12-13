from os import getenv
from asyncio import create_task, sleep
from traceback import format_exc
from ebuffer.database import Eb_Database
from ebuffer.auth import Eb_Auth
from fastapi.security import HTTPBearer, HTTPBasic

from ebservice.config import AppMsConfig, logger
from ebservice.apijob import Eb_JobAPI
from ebservice.apipolicy import Eb_PolicyAPI
from ebservice.apiruntime import Eb_RuntimeAPI
from ebservice.apimservice import Eb_MicroserviceAPI

class AppMS_Application():

    def __init__(self):
        self.regexp_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.config = AppMsConfig(inifile=getenv(r'EBSERVICE_INI', r'ebservice.ini'), secretfile=getenv(r'EBSERVICE_SECRET_INI', r'.ebservice-secret.ini'))
        self.db = Eb_Database(self.config)
        self.jobAPI = Eb_JobAPI(self.config)
        self.policyAPI = Eb_PolicyAPI(self.config)
        self.runtimeAPI = Eb_RuntimeAPI(self.config, self.jobAPI, self.policyAPI)
        self.mserviceAPI = Eb_MicroserviceAPI(self.config, self.jobAPI, self.policyAPI, self.runtimeAPI)
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
            await self.mserviceAPI.housekeeping(session, interval, start)
        except Exception as e:
            logger.error(r"Could not finish a housekeeping session %s: %s", str(e), format_exc())
            # raise Eb_HouseKeepingError(e)
        finally:
            create_task(self.housekeeping())

    def start(self):
        create_task(self.housekeeping(start=True))

    def destroy(self):
        del self.db
        self.db = None

app_g = AppMS_Application()

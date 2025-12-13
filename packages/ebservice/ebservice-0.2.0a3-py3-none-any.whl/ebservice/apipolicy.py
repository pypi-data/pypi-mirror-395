from sqlmodel import Session
from ebuffer.apiuserobj import Eb_UserObjAPI, Eb_ObjectInvalid

from ebservice.config import AppMsConfig
from ebservice.database import PolicyEntry, Eb_PolicyCRUD

Eb_PolicyInvalid = Eb_ObjectInvalid

class Eb_PolicyAPI(Eb_UserObjAPI):

    def __init__(self, config: AppMsConfig):
        self.config = config
        self.mserviceCRUD = Eb_PolicyCRUD()
        super().__init__(PolicyEntry, config.base, self.mserviceCRUD)

    def destroy(self):
        pass

    #
    # Housekeeping
    #
    async def housekeeping(self, session: Session, interval: int, start: bool = False) -> None:
        pass

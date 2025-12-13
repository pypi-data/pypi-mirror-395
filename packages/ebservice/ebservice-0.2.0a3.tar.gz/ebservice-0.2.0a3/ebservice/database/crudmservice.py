from sqlmodel import Session, select
from traceback import format_exc

from ebuffer.database.privmodel_userobj import UserObjEntry
from ebuffer.database.database import Eb_DBError
from ebuffer.database.cruduserobj import Eb_UserObjCRUD, Eb_ObjectNotFound

from ebservice.config import logger
from ebservice.models_mservice import MicroserviceStateEnum
from ebservice.database.privmodel_mservice import MicroserviceEntry

class Eb_MicroserviceCRUD(Eb_UserObjCRUD):
    def __init__(self): super().__init__(MicroserviceEntry)

    def get_by_state(self, session: Session, state: MicroserviceStateEnum) -> MicroserviceEntry:
        try:
            statement = select(self.ObjEntry).where(self.ObjEntry.state == state)
            results = session.exec(statement)
            for uobj in results:
                uobj.refresh()
                yield uobj

        except Exception as e:
            logger.error(r"Could not extract ObjectEntries by state: %s", format_exc())
            raise Eb_DBError("Internal Error EX005", e)

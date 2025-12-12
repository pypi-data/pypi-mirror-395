from sqlmodel import Session, select
from traceback import format_exc

from ebuffer.database.database import Eb_DBError
from ebuffer.database.cruduserobj import Eb_UserObjCRUD, Eb_ObjectNotFound

from ebservice.config import logger
from ebservice.models_runtime import RuntimeStateEnum
from ebservice.database.privmodel_runtime import RuntimeEntry

class Eb_RuntimeCRUD(Eb_UserObjCRUD):
    def __init__(self): super().__init__(RuntimeEntry)

    def available(self, session: Session) -> RuntimeEntry:
        try:
            statement = select(self.ObjEntry).where(self.ObjEntry.state == RuntimeStateEnum.ready)
            results = session.exec(statement)
            for uobj in results:
                uobj.refresh()
                yield uobj

        except Exception as e:
            logger.error(r"Could not extract available ObjectEntries: %s", format_exc())
            raise Eb_DBError("Internal Error FX005", e)

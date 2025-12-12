from ebuffer.database.privmodel_user import UserIdEntry
from ebuffer.database.cruduser import get_user_db, get_user_by_email_db

from ebuffer.database.cruduserobj import Eb_UserObjCRUD, Eb_ObjectNotFound

from ebservice.database.privmodel_job import JobEntry
from ebservice.database.privmodel_mservice import MicroserviceEntry
from ebservice.database.privmodel_policy import PolicyEntry, Eb_PolicyForbidden
from ebservice.database.privmodel_runtime import RuntimeEntry
from ebservice.database.privmodel_mimetypes import MimetypeEntry
from ebservice.database.crudmimetype import get_mimetype_db

from ebservice.database.crudmservice import Eb_MicroserviceCRUD
from ebservice.database.crudruntime import Eb_RuntimeCRUD

from ebuffer.database.database import Eb_Database, Eb_DBError
from ebuffer.database.database import Eb_DBError
from ebuffer.database.cruduser import Eb_MissingCred
from ebuffer.database.cruduserobj import Eb_ObjectNotFound
from ebservice.database.crudmimetype import Eb_MissingMimetype

JobExceptionList = Eb_MissingCred().model() | Eb_ObjectNotFound().model()
MicroserviceExceptionList = Eb_MissingCred().model() | Eb_ObjectNotFound().model()
PolicyExceptionList = Eb_MissingCred().model() | Eb_ObjectNotFound().model()
RuntimeExceptionList = Eb_MissingCred().model() | Eb_ObjectNotFound().model()

class Eb_JobCRUD(Eb_UserObjCRUD):
    def __init__(self): super().__init__(JobEntry)

class Eb_PolicyCRUD(Eb_UserObjCRUD):
    def __init__(self): super().__init__(PolicyEntry)

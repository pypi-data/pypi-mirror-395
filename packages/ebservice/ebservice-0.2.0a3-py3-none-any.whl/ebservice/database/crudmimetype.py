from asyncio import create_task
from sqlmodel import Session, select
from sqlalchemy.orm.exc import MultipleResultsFound

from ebuffer.errors import Eb_Exception
from ebuffer.database.database import Eb_DBError

from ebservice.config import logger
from ebservice.database.privmodel_mimetypes import MimetypeEntry

#
# Mimetype Management

class Eb_MissingMimetype(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(401, "MissingMimetype", "This mime-type was not found.", details)

async def _update_mimetype_db(session: Session, mimetype: [str | MimetypeEntry]) -> MimetypeEntry:
    if not isinstance(mimetype, MimetypeEntry): mimetype = MimetypeEntry(mimetype)
    if not isinstance(mimetype, MimetypeEntry): raise Eb_DBError("Internal Error MX001")
    try:
        session.add(mimetype)
        session.commit()
        session.refresh(mimetype)
    except Exception as e:
        logger.error(r"Could not add mimetype %s: %s", str(mimetype), str(e))
    return mimetype

def get_mimetype_db(session: Session, mimetype: [str | MimetypeEntry], create: bool = True) -> [ MimetypeEntry, None ]:
    if not isinstance(mimetype, MimetypeEntry): mimetype = MimetypeEntry(mimetype)
    sql = select(MimetypeEntry).where(MimetypeEntry.name == mimetype.name)
    #logger.debug(r"Search mimetype %s", str(mimetype))
    try:
        fmimetype = session.exec(sql).one_or_none()
    except MultipleResultsFound as e:
        raise Eb_DBError("Multiple mimetypes '%s' in DB" % mimetype.email, e)

    #if fmimetype: logger.debug('Mimetype found: %s: %s', fmimetype.json(), str(fmimetype.buffers))
    if fmimetype: return fmimetype
    if not create:
        raise Eb_MissingMimetype(r'Mimetype %s does not exists' % mimetype.email)

    #try:
    #    dbmimetype = MimetypeEntry.model_validate(mimetype)
    #except Exception as e:
    #    logger.error(r"Could not validate MimetypeID %s: %s", str(mimetype), str(e))
    #    raise Eb_DBError("Internal Error MX002", e)
    dbmimetype = mimetype

    create_task(_update_mimetype_db(session, dbmimetype))
    return dbmimetype

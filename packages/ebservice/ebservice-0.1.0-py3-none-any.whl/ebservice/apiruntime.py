from sqlmodel import Session
from asyncio import create_task, sleep

from ebuffer.models_common import UserId
#from ebuffer.database import get_user_db
from ebuffer.apiuserobj import Eb_UserObjAPI, Eb_ObjectInvalid

from ebservice.config import AppMsConfig, logger
from ebuffer.errors import Eb_Exception

from ebservice.models_runtime import RuntimeRequest, RuntimeStateEnum
from ebservice.models_job import JobRequest, JobRunStatusEnum, JobRunStatus
from ebservice.database import MimetypeEntry
from ebservice.database import JobEntry, Eb_ObjectNotFound
from ebservice.database import PolicyEntry
from ebservice.database import RuntimeEntry, Eb_RuntimeCRUD
from ebservice.database import get_mimetype_db

from ebservice.apijob import Eb_JobAPI
from ebservice.apipolicy import Eb_PolicyAPI

Eb_RuntimeInvalid = Eb_ObjectInvalid

class Eb_MimeTypeAlreadyBinded(Eb_Exception):
    def __init__(self, mimetype: str = r'', rtlst: str = r''):
        super().__init__(401, "MimeTypeAlreadyBinded", "Mimetype already binded.", r'Mimetype: %s, binded: %s' % (mimetype, rtlst))

class Eb_MicroserviceNotAttached(Eb_Exception):
    def __init__(self, appms_uid: str = r''):
        super().__init__(404, "MicroserviceNotAttached", "Microservice found but not already attached to runtime.", r'Microservice: %s' % appms_uid)

class Eb_RuntimeAPI(Eb_UserObjAPI):

    def __init__(self, config: AppMsConfig, jobAPI: Eb_JobAPI, policyAPI: Eb_PolicyAPI):
        self.config = config
        self.jobAPI = jobAPI
        self.policyAPI = policyAPI
        self.runtimeCRUD = Eb_RuntimeCRUD()
        super().__init__(RuntimeEntry, config.base, self.runtimeCRUD)

    def destroy(self):
        pass

    #
    # Housekeeping
    #
    async def housekeeping(self, session: Session, interval: int, start: bool = False) -> None:
        pass

    #
    # Register operations
    #

    async def register(self, runtime: RuntimeEntry, user: UserId, session: Session) -> RuntimeEntry:
        mimetype: MimetypeEntry = get_mimetype_db(session, runtime.accepted_mime_type, create=True)
        logger.debug(f'Register runtime to {mimetype} ({len(mimetype.runtimes)})')
        for rt in mimetype.runtimes:
            if rt.uuid != runtime.uuid:
                runtime.state = RuntimeStateEnum.error
                error = Eb_MimeTypeAlreadyBinded(mimetype.name, rt.uuid)
                runtime.state_desc = error.desc()
                logger.error(runtime.state_desc)
                break

        if runtime.state != RuntimeStateEnum.error:
            runtime.state = RuntimeStateEnum.ready

        create_task(self.runtimeCRUD.update(session, runtime))
        return runtime

    async def availRuntime(self, session: Session) -> list[RuntimeEntry]:
        return self.runtimeCRUD.available(session)

    #
    # Main operations
    #

    async def createAndRegister(self, rtreq: RuntimeRequest, blocking: bool, user: UserId, session: Session) -> RuntimeEntry:
        runtime = await self.create(RuntimeEntry(rtreq), blocking, user, session)
        if blocking: runtime = await self.register(runtime, user, session)
        else:        create_task(self.register(runtime, user, session))
        return runtime

    #
    # Job' operations
    #
    async def searchJobs(self, uid: str, msuid: str, limit: int, skip: int,
                         owner: str, tags: list[str], all: bool, runstatus: str | None, count: bool,
                         user: UserId, session: Session) -> list[JobEntry] | int:
        runtime : RuntimeEntry = self.runtimeCRUD.get(session, uid)
        policy : PolicyEntry = runtime.policy
        rs = self.toJobStatus(runstatus) if runstatus else None

        def ofilter(job: JobEntry):
            if rs and rs[0] != job.run_status[0]: return False
            #logger.debug('Policy: %s [%s:%s] ? %s', policy, job.runtime_uuid, job.uuid, user)
            return job.runtime_uuid == uid

        def ofilterMs(job: JobEntry):
            if rs and rs[0] != job.run_status[0]: return False
            #logger.debug('Policy: %s [%s:%s] ? %s', policy, job.runtime_uuid, job.uuid, user)
            return job.appms_uuid == msuid and job.runtime_uuid == uid

        jf = ofilterMs if msuid else ofilter
        return await self.jobAPI.search(session, user, limit, skip, owner, tags, all, count, jf)

    async def getJob(self, uid: str, msuid: str, jid: str, owner: str,
                     user: UserId, session: Session) -> JobEntry:
        runtime : RuntimeEntry = self.runtimeCRUD.get(session, uid)
        policy : PolicyEntry = runtime.policy

        job = await self.jobAPI.get(jid, owner, session)
        #logger.debug('Policy: %s [%s:%s] ? %s', policy, job.runtime_uuid, job.uuid, user)
        if job.runtime_uuid != uid: raise Eb_ObjectNotFound(uid)
        return job

    async def getJobTags(self, uid: str, jid: str, owner: str,
                         user: UserId, session: Session) -> JobEntry:
        runtime : RuntimeEntry = self.runtimeCRUD.get(session, uid)
        policy : PolicyEntry = runtime.policy

        job = await self.jobAPI.get(jid, owner, user, session)
        logger.debug('Policy: %s [%s:%s] ? %s', policy, job.runtime_uuid, job.uuid, user)
        if job.runtime_uuid != uid: raise Eb_ObjectNotFound(uid)
        return job.tags

    async def addJobTag(self, uid: str, jid: str, tag: str,
                        user: UserId, session: Session) -> JobEntry:
        runtime : RuntimeEntry = self.runtimeCRUD.get(session, uid)
        policy : PolicyEntry = runtime.policy

        job = await self.jobAPI.addTag(jid, tag, user, session)
        logger.debug('Policy: %s [%s] ? %s', policy, job.uuid, user)
        return job

    async def getJobStatus(self, uid: str, msuid: str, jid: str, owner: str,
                           user: UserId, session: Session) -> JobRunStatus:
        runtime : RuntimeEntry = self.runtimeCRUD.get(session, uid)
        policy : PolicyEntry = runtime.policy

        job = await self.jobAPI.get(jid, owner, user, session)
        #logger.debug('Policy: %s [%s:%s] ? %s', policy, job.runtime_uuid, job.uuid, user)
        if job.runtime_uuid != uid: raise Eb_ObjectNotFound(uid)
        rs = job.run_status
        return JobRunStatus(status=rs[0], desc=rs[1])

    async def postJobStatus(self, uid: str, msuid: str, jid: str, runstatus: str, desc: str,
                            user: UserId, session: Session) -> JobEntry:
        runtime : RuntimeEntry = self.runtimeCRUD.get(session, uid)
        policy : PolicyEntry = runtime.policy

        job = await self.jobAPI.get(jid, None, user, session)
        logger.debug('Policy: %s [%s:%s] ? %s', policy, job.runtime_uuid, job.uuid, user)
        if job.runtime_uuid != uid: raise Eb_ObjectNotFound(uid)
        job = await self.jobAPI.postJobStatus(job, runstatus, desc, user, session)
        return job

    async def postJobOutputs(self, uid: str, msuid: str, jid: str, name: str | None, values: list[str],
                             user: UserId, session: Session) -> JobEntry:
        runtime : RuntimeEntry = self.runtimeCRUD.get(session, uid)
        policy : PolicyEntry = runtime.policy

        job = await self.jobAPI.get(jid, None, user, session)
        logger.debug('Policy: %s [%s:%s] ? %s', policy, job.runtime_uuid, job.uuid, user)
        if job.runtime_uuid != uid: raise Eb_ObjectNotFound(uid)
        job = await self.jobAPI.postJobOutputs(job, name, values, user, session)
        return job

from sqlmodel import Session
from asyncio import create_task, sleep

from ebuffer.models_common import UserId
#from ebuffer.database import get_user_db
from ebuffer.apiuserobj import Eb_UserObjAPI, Eb_ObjectInvalid

from ebservice.config import AppMsConfig, logger
from ebuffer.errors import Eb_Exception

from ebservice.models_mservice import MicroserviceRequest, MicroserviceStateEnum
from ebservice.models_job import JobRequest, JobRunStatusEnum, JobRunStatus, JobStateEnum
from ebservice.models_runtime import RuntimeStateEnum
from ebservice.database import MimetypeEntry
from ebservice.database import JobEntry, Eb_ObjectNotFound
from ebservice.database import PolicyEntry
from ebservice.database import MicroserviceEntry, Eb_MicroserviceCRUD
from ebservice.database import get_mimetype_db

from ebservice.apijob import Eb_JobAPI
from ebservice.apipolicy import Eb_PolicyAPI
from ebservice.apiruntime import Eb_RuntimeAPI

Eb_MicroserviceInvalid = Eb_ObjectInvalid

class Eb_EitherMimetypeOrRuntimeRequired(Eb_Exception):
    def __init__(self, msreq: MicroserviceRequest = None):
        super().__init__(401, "EitherMimetypeOrRuntimeRequired", "Either a mime-type or a runtime uid shall be provided.", r'Microservice: %s' % msreq)

class Eb_MicroserviceAPI(Eb_UserObjAPI):

    def __init__(self, config: AppMsConfig, jobAPI: Eb_JobAPI, policyAPI: Eb_PolicyAPI, runtimeAPI: Eb_RuntimeAPI):
        self.config = config
        self.jobAPI = jobAPI
        self.policyAPI = policyAPI
        self.runtimeAPI = runtimeAPI
        self.mserviceCRUD = Eb_MicroserviceCRUD()
        super().__init__(MicroserviceEntry, config.base, self.mserviceCRUD)

    def destroy(self):
        pass

    #
    # Housekeeping
    #
    async def housekeeping(self, session: Session, interval: int, start: bool = False) -> None:
        runtimeList = list(await self.runtimeAPI.availRuntime(session))
        updateList = set()
        jobUpdateList = set()

        # Look for unbinded microservicese
        for mservice in self.mserviceCRUD.get_by_state(session, MicroserviceStateEnum.waiting):
            logger.debug(f'Unbinded microservice: {mservice.name}: [{mservice.runtime_uuid}] ({mservice.mime_type})')
            for rt in runtimeList:
                logger.debug(f'  => Check {rt.name} ({rt.accepted_mime_type}) [{rt.state}]')
                if mservice.matchesRuntime(rt):
                    mservice.runtime_uuid = rt.uuid
                    mservice.state = MicroserviceStateEnum.binded
                    updateList.add(mservice)
                    logger.warn(f'BIND microservice {mservice.name} to {rt.name} [{rt.uuid}] ({rt.accepted_mime_type})')
                    break

        for mservice in self.mserviceCRUD.get_by_state(session, MicroserviceStateEnum.binded):
            #logger.debug(f'Binded microservice: {mservice.name}: [{mservice.runtime_uuid}] ({mservice.mime_type})')

            if mservice.runtime_uuid:
                runtime = None
                for rt in runtimeList:
                    if rt.uuid != mservice.runtime_uuid: continue
                    runtime = rt
                    break
                if not runtime:
                    mservice.runtime_uuid = r''
                    logger.debug(f'  => Lost runtime {mservice.runtime_uuid}')
                elif runtime.state != RuntimeStateEnum.ready:
                    mservice.runtime_uuid = r''
                    logger.debug(f'  =>offline {runtime.name} ({runtime.accepted_mime_type}) [{runtime.state}]')

            if not mservice.runtime_uuid:
                mservice.state = MicroserviceStateEnum.waiting
                updateList.add(mservice)
                logger.warn(r'  => Disconnect runtime...')

        for job in await self.jobAPI.search(session=session):
            if job.state == JobStateEnum.error or \
               job.state == JobStateEnum.disabled or \
               job.state == JobStateEnum.deleted or \
               job.state == JobStateEnum.initialized: continue
            if job.state == JobStateEnum.executed:
                logger.warn(f'Job {job.uuid} executed.')
                continue

            if not job.mservice:
                logger.error(f'Job {job.uuid} lost its microservice...')
                job.state = JobStateEnum.error
                job.run_status = (JobRunStatusEnum.failed, r'Microservice lost.')
                job.state_desc = r'Lost contact with microservice'
                jobUpdateList.add(job)
                continue

            if job.state == JobStateEnum.scheduled:
                runst = job.run_status[0]
                if runst == JobRunStatusEnum.cancelled or \
                   runst == JobRunStatusEnum.completed or \
                   runst == JobRunStatusEnum.failed:
                    logger.warning(f'Job {job.uuid} over with run status {runst}.')
                    job.state = JobStateEnum.executed
                    jobUpdateList.add(job)

                elif job.mservice.state != MicroserviceStateEnum.binded:
                    logger.warning(f'Job {job.uuid} lost its queue.')
                    job.runtime_uuid = r''
                    job.state = JobStateEnum.ready
                    jobUpdateList.add(job)

            elif job.state == JobStateEnum.ready:
                if job.mservice.state == MicroserviceStateEnum.binded:
                    logger.warning(f'Job {job.uuid} scheduled.')
                    job.runtime_uuid = job.mservice.runtime_uuid
                    job.state = JobStateEnum.scheduled
                    jobUpdateList.add(job)

        for mservice in updateList:
            await self.mserviceCRUD.update(session, mservice, commit=False)
            logger.debug(f'  => Updated mservice: {mservice.uuid}')
        self.mserviceCRUD.commit(session)
        for job in jobUpdateList:
            await self.jobAPI.update(session, job, commit=False)
            logger.debug(f'  => Updated job: {job.uuid}')
        self.jobAPI.commit(session)

    #
    # Register operations
    #

    async def register(self, mservice: MicroserviceEntry, user: UserId, session: Session) -> MicroserviceEntry:
        mimetype: MimetypeEntry = get_mimetype_db(session, mservice.mime_type, create=True)
        logger.debug(f'Register microservice to {mimetype} ({mimetype.runtimes})')
        for rt in mimetype.runtimes:
            logger.debug(f'Check microservice with {rt}')

        mservice.state = MicroserviceStateEnum.waiting
        create_task(self.mserviceCRUD.update(session, mservice))
        return mservice

    #
    # Main operations
    #

    async def createAndRegister(self, msreq: MicroserviceRequest, blocking: bool, user: UserId, session: Session) -> MicroserviceEntry:
        mservice = await self.create(MicroserviceEntry(msreq), blocking, user, session)
        if not mservice.mime_type and not mservice.runtime_uuid:
            raise Eb_EitherMimetypeOrRuntimeRequired(msreq)

        if blocking: mservice = await self.register(mservice, user, session)
        else:        create_task(self.register(mservice, user, session))
        return mservice

    #
    # Job' operations
    #
    async def createJob(self, uid: str, jobreq: JobRequest, blocking: bool, user: UserId, session: Session) -> JobEntry:
        mservice : MicroserviceEntry = self.mserviceCRUD.get(session, uid)
        policy : PolicyEntry = mservice.policy
        logger.debug('Policy: %s ? %s', policy, user)

        job = await self.jobAPI.create(JobEntry(mservice.uuid, jobreq), blocking, user, session)

        if blocking: job = await self.jobAPI.register(session, job)
        else:        create_task(self.jobAPI.register(session, job))
        return job

    async def searchJobs(self, uid: str, limit: int, skip: int, owner: str, tags: list[str], all: bool, count: bool,
                         user: UserId, session: Session) -> list[JobEntry] | int:
        mservice : MicroserviceEntry = self.mserviceCRUD.get(session, uid)
        policy : PolicyEntry = mservice.policy

        def ofilter(job: JobEntry):
            #logger.debug('Policy: %s [%s:%s] ? %s', policy, job.appms_uuid, job.uuid, user)
            return job.appms_uuid == uid

        return await self.jobAPI.search(session, user, limit, skip, owner, tags, all, count, ofilter)

    async def getJob(self, uid: str, jid: str, owner: str,
                     user: UserId, session: Session) -> JobEntry:
        mservice : MicroserviceEntry = self.mserviceCRUD.get(session, uid)
        policy : PolicyEntry = mservice.policy

        job = await self.jobAPI.get(jid, owner, user, session)
        #logger.debug('Policy: %s [%s:%s] ? %s', policy, job.appms_uuid, job.uuid, user)
        if job.appms_uuid != uid: raise Eb_ObjectNotFound(uid)
        return job

    async def deleteJob(self, uid: str, jid: str,
                        user: UserId, session: Session) -> JobEntry:
        mservice : MicroserviceEntry = self.mserviceCRUD.get(session, uid)
        policy : PolicyEntry = mservice.policy

        logger.debug('Policy: %s ? %s', policy, user)
        job = await self.jobAPI.delete(jid, user, session)
        return job

    async def getJobTags(self, uid: str, jid: str, owner: str,
                         user: UserId, session: Session) -> JobEntry:
        mservice : MicroserviceEntry = self.mserviceCRUD.get(session, uid)
        policy : PolicyEntry = mservice.policy

        job = await self.jobAPI.get(jid, owner, user, session)
        logger.debug('Policy: %s [%s:%s] ? %s', policy, job.appms_uuid, job.uuid, user)
        if job.appms_uuid != uid: raise Eb_ObjectNotFound(uid)
        return job.tags

    async def addJobTag(self, uid: str, jid: str, tag: str,
                        user: UserId, session: Session) -> JobEntry:
        mservice : MicroserviceEntry = self.mserviceCRUD.get(session, uid)
        policy : PolicyEntry = mservice.policy

        job = await self.jobAPI.addTag(jid, tag, user, session)
        logger.debug('Policy: %s [%s] ? %s', policy, job.uuid, user)
        return job

    async def getJobStatus(self, uid: str, jid: str, owner: str,
                           user: UserId, session: Session) -> JobRunStatus:
        mservice : MicroserviceEntry = self.mserviceCRUD.get(session, uid)
        policy : PolicyEntry = mservice.policy

        job = await self.jobAPI.get(jid, owner, user, session)
        #logger.debug('Policy: %s [%s:%s] ? %s', policy, job.appms_uuid, job.uuid, user)
        if job.appms_uuid != uid: raise Eb_ObjectNotFound(uid)
        rs = job.run_status
        return JobRunStatus(status=rs[0], desc=rs[1])

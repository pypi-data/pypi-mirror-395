from asyncio import create_task
from sqlmodel import Session
from ebuffer.models_common import UserId
from ebuffer.errors import Eb_Exception
from ebuffer.apiuserobj import Eb_UserObjAPI, Eb_ObjectInvalid

from ebservice.config import AppMsConfig, logger

from ebservice.models_job import JobRequest, JobRunStatusEnum, JobRunStatus, JobStateEnum
from ebservice.database import JobEntry, Eb_JobCRUD

Eb_JobInvalid = Eb_ObjectInvalid

class Eb_JobRunStatusValue(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(432, "JobRunStatusValue", "Invalid run status.", details)

class Eb_JobInvalidReturnValue(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(432, "JobInvalidReturnValue", "Invalid result value for the job.", details)

class Eb_JobInvalidResultName(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(432, "JobInvalidResultName", "Invalid result name for the job.", details)

class Eb_JobMissingMicrosservice(Eb_Exception):
    def __init__(self, details: str = r''):
        super().__init__(432, "JobMissingMicrosservice", "Missing microservice for the job.", details)

class Eb_JobAPI(Eb_UserObjAPI):

    def __init__(self, config: AppMsConfig):
        self.config = config
        self.jobCRUD = Eb_JobCRUD()
        super().__init__(JobEntry, config.base, self.jobCRUD)

    def destroy(self):
        pass

    @staticmethod
    def toJobStatus(runstatus: str, desc: str = r'') -> JobRunStatusEnum:
        try: return (JobRunStatusEnum(runstatus), desc)
        except ValueError: raise Eb_JobRunStatusValue(runstatus)

    #
    # Housekeeping
    #
    async def housekeeping(self, session: Session, interval: int, start: bool = False) -> None:
        pass

    #
    # Register operations
    #
    def commit(self, session: Session) -> None:
        self.jobCRUD.commit(session)

    async def update(self, session: Session, job: JobEntry, commit=False) -> JobEntry:
        create_task(self.jobCRUD.update(session, job, commit=commit))
        return job

    async def register(self, session: Session, job: JobEntry) -> JobEntry:
        job.state = JobStateEnum.ready
        job.run_status = (JobRunStatusEnum.pending, r'')
        create_task(self.jobCRUD.update(session, job))
        return job

    #
    # Main operations
    #

    async def postJobStatus(self, job: JobEntry, runstatus: str, desc: str,
                            user: UserId, session: Session) -> JobEntry:
        job.run_status = self.toJobStatus(runstatus, desc)
        create_task(self.jobCRUD.update(session, job))
        return job

    async def postJobOutputs(self, job: JobEntry, name: str | None, values: list[str],
                             user: UserId, session: Session) -> JobEntry:

        logger.debug(f'Store Results: {job} <= {name}:{values}')
        if name:
            mservice = job.mservice
            if not mservice: raise Eb_JobMissingMicrosservice(f'Service: {job.appms_uuid}')
            try: index = mservice.result_names.index(name)
            except ValueError: raise Eb_JobInvalidResultName(name)
            for v in values:
                job.result_values[index] = v
                index += 1
        else: job.result_values = values

        #count = number + len(results)
        #extra = count - len(job.result_values)
        #if not len(job.result_values) or (number == 0 and extra == 0):
        #    job.result_values = results
        #else:
        #    if extra > 0: job.result_values.extend([b'']*extra)
        #    for i  in range(len(results)):
        #        job.result_values[number+i] = results[i]

        create_task(self.jobCRUD.update(session, job))
        return job

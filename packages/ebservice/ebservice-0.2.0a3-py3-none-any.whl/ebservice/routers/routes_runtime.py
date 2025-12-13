from typing import Annotated
from fastapi import APIRouter, Request, Depends, Path, Query, Body
from fastapi.responses import Response
from sqlmodel import Session

from ebuffer.errors import a_exc2msg

from ebservice.application import app_g
from ebservice.models_job import Job, JobRunStatusEnum
from ebservice.models_mservice import Microservice
from ebservice.models_runtime import RuntimeRequest, Runtime
from ebservice.database import MicroserviceEntry
from ebservice.apiruntime import Eb_MicroserviceNotAttached
from ebservice.routers.routes_auth import check_token

#
# -- Runtime Management
#

router = APIRouter(prefix="/runtime", tags=["Runtimes"])
router.rest_metadata = { "name": "Runtimes" }

@router.post("")
@a_exc2msg
async def createRuntime(
    request: Request,
    runtime: Annotated[ RuntimeRequest, Body() ],
    blocking: Annotated[bool | None, Query()] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Runtime:
    return await app_g.runtimeAPI.createAndRegister(runtime, blocking, user, session)

@router.get("")
@a_exc2msg
async def searchRuntime(
    request: Request,
    limit: Annotated[int | None, Query(title="Maximum number of element returned", ge=1, le=app_g.config.base.search_max_limit)] = app_g.config.base.search_limit,
    skip: Annotated[int | None, Query(title="Number of element skipped", ge=0)] = 0,
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    tags: Annotated[list[str] | None, Query(title="A tag to match. The option can be added multiple times.")] = [],
    all: Annotated[bool | None, Query(title="Whether it matches all tags or just one tag.")] = False,
    count: Annotated[bool | None, Query(title="Returns the number of elements, and not the list itself. The parameters '*skip*' and '*limit*' are ignored.")] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[Runtime] | int:
    result = await app_g.runtimeAPI.search(session, user, limit, skip, owner, tags, all, count)
    return Response(content=str(result), media_type=r'text/plain') if isinstance(result, int) else result

@router.get("/{uid}")
@a_exc2msg
async def getRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Runtime:
    return await app_g.runtimeAPI.get(uid, owner, user, session)

@router.delete("/{uid}")
@a_exc2msg
async def delRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Runtime:
    return await app_g.runtimeAPI.delete(uid, user, session)

#
# -- Runtime TAGS Management
#

@router.get("/{uid}/tags")
@a_exc2msg
async def getTagsFromRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[str]:
    return await app_g.runtimeAPI.getTags(uid, user, session)

@router.post("/{uid}/tags/{tag}")
@a_exc2msg
async def addTagsToRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    tag: Annotated[
        str,
        Path(
            title="A tag, an UTF-8 string with a size between %d and %d." % (app_g.config.base.tag_min_size, app_g.config.base.tag_max_size),
            min_length=app_g.config.base.tag_min_size,
            max_length=app_g.config.base.tag_max_size,
        ),
    ],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Runtime:
    return await app_g.runtimeAPI.addTag(uid, tag, user, session)

#
# -- Runtime Jobs' Management
#

@router.get("/{uid}/job")
@a_exc2msg
async def searchJobsFromRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the runtime", min_length=36, max_length=36)],
    limit: Annotated[int | None, Query(title="Maximum number of element returned", ge=1, le=app_g.config.base.search_max_limit)] = app_g.config.base.search_limit,
    skip: Annotated[int | None, Query(title="Number of element skipped", ge=0)] = 0,
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    tags: Annotated[list[str] | None, Query(title="A tag to match. The option can be added multiple times.")] = [],
    all: Annotated[bool | None, Query(title="Whether the runtime matches all tags or just one tag.")] = False,
    runstatus: Annotated[str | None, Query(title="The run state", min_length=4, max_length=16, pattern=app_g.regexp_email)] = None,
    count: Annotated[bool | None, Query(title="Returns the number of elements, and not the list itself. The parameters '*skip*' and '*limit*' are ignored.")] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[Job] | int:
    result = await app_g.runtimeAPI.searchJobs(uid, r'', limit, skip, owner, tags, all, runstatus, count, user, session)
    #print(r'°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°', result)
    return Response(content=str(result), media_type=r'text/plain') if isinstance(result, int) else result

@router.get("/{uid}/job/{jid}")
@a_exc2msg
async def getJobFromRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.runtimeAPI.getJob(uid, r'', jid, owner, user, session)

#
# -- Runtime Jobs' Tags Management
#

@router.get("/{uid}/job/{jid}/tags")
@a_exc2msg
async def getTagsFromJobInRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[str]:
    return await app_g.runtimeAPI.getJobTags(uid, jid, user, session)

@router.post("/{uid}/job/{jid}/tags/{tag}")
@a_exc2msg
async def addTagsToJobInRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    tag: Annotated[
        str,
        Path(
            title="A tag, an UTF-8 string with a size between %d and %d." % (app_g.config.base.tag_min_size, app_g.config.base.tag_max_size),
            min_length=app_g.config.base.tag_min_size,
            max_length=app_g.config.base.tag_max_size,
        ),
    ],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.runtimeAPI.addJobTag(uid, jid, tag, user, session)

#
# -- Runtime Jobs' Execution Management
#

@router.get("/{uid}/job/{jid}/status")
@a_exc2msg
async def getJobStatusToRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> JobRunStatusEnum:
    return await app_g.runtimeAPI.getJobStatus(uid, r'', jid, owner, user, session)

@router.post("/{uid}/job/{jid}/status/{runstatus}")
@a_exc2msg
async def postJobStatusToRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    runstatus: Annotated[JobRunStatusEnum, Path(title="The job status", min_length=5, max_length=10)],
    desc: Annotated[str | None, Query(title="The status description", max_length=200)] = r'',
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.runtimeAPI.postJobStatus(uid, r'', jid, runstatus, desc, user, session)

@router.post("/{uid}/job/{jid}/results")
@a_exc2msg
async def postJobOutputToRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    value: Annotated[list[str], Query(title="The result content. Several results can be added.", max_length=300)] = [],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.runtimeAPI.postJobOutputs(uid, r'', jid, None, value, user, session)

@router.post("/{uid}/job/{jid}/results/{name}")
@a_exc2msg
async def postJobOutputNumberToRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    name: Annotated[int, Path(title="The starting result number")],
    value: Annotated[list[str], Query(title="The result content.", max_length=300)] = [],
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.runtimeAPI.postJobOutputs(uid, r'', jid, name, value, user, session)

#
# -- Runtime Microservice' Management
#

@router.get(
    "/{uid}/app_service",
    summary=r'Count or fetch the list of microservice types attached to the runtime.',
    description=r'Look for all the microservice matching the filtering criteria. Be aware that unless the count is requested, the number of results is limited and has a default maximum value defined during the deployment. The full list can be retrieved with a loop and using the query parameters "*limit*" and "*skip*". Additional filters can be applied on the owner and the tags (all or them, or any of them).',
    response_description="Returns either the list of microservice' status or the number of elements.",
)
@a_exc2msg
async def searchMicroserviceFromRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the runtime", min_length=36, max_length=36)],
    limit: Annotated[int | None, Query(title="Maximum number of element returned", ge=1, le=app_g.config.base.search_max_limit)] = app_g.config.base.search_limit,
    skip: Annotated[int | None, Query(title="Number of element skipped", ge=0)] = 0,
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    tags: Annotated[list[str] | None, Query(title="A tag to match. The option can be added multiple times.")] = [],
    all: Annotated[bool | None, Query(title="Whether the microservice matches all tags or just one tag.")] = False,
    count: Annotated[bool | None, Query(title="Returns the number of elements, and not the list itself. The parameters '*skip*' and '*limit*' are ignored.")] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[Microservice] | int:
    def ofilter(appms: MicroserviceEntry):
        return appms.runtime_uuid == uid

    result = await app_g.mserviceAPI.search(session, user, limit, skip, owner, tags, all, count, ofilter)
    return Response(content=str(result), media_type=r'text/plain') if isinstance(result, int) else result

@router.get(
    "/{uid}/app_service/{msuid}",
    summary=r'Get an application microservice attached to a runtime.',
    description=r'Get the descriptor of an application microservice.',
    response_description="The status of an application microservice.",
)
@a_exc2msg
async def getMicroserviceFromRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the runtime", min_length=36, max_length=36)],
    msuid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Microservice:
    appms = await app_g.mserviceAPI.get(msuid, owner, user, session)
    if appms.runtime_uuid != uid: raise Eb_MicroserviceNotAttached(uid)
    return appms

#
# -- Runtime Jobs' Management from Microservice
#

@router.get("/{uid}/app_service/{msuid}/job")
@a_exc2msg
async def searchJobsFromMsRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the runtime", min_length=36, max_length=36)],
    msuid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
    limit: Annotated[int | None, Query(title="Maximum number of element returned", ge=1, le=app_g.config.base.search_max_limit)] = app_g.config.base.search_limit,
    skip: Annotated[int | None, Query(title="Number of element skipped", ge=0)] = 0,
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    tags: Annotated[list[str] | None, Query(title="A tag to match. The option can be added multiple times.")] = [],
    all: Annotated[bool | None, Query(title="Whether the runtime matches all tags or just one tag.")] = False,
    runstatus: Annotated[str | None, Query(title="The run state", min_length=4, max_length=16, pattern=app_g.regexp_email)] = None,
    count: Annotated[bool | None, Query(title="Returns the number of elements, and not the list itself. The parameters '*skip*' and '*limit*' are ignored.")] = False,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> list[Job] | int:
    result = await app_g.runtimeAPI.searchJobs(uid, msuid, limit, skip, owner, tags, all, runstatus, count, user, session)
    #print(r'°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°', result)
    return Response(content=str(result), media_type=r'text/plain') if isinstance(result, int) else result

@router.get("/{uid}/app_service/{msuid}/job/{jid}")
@a_exc2msg
async def getJobFromMsRuntime(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
    msuid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.runtimeAPI.getJob(uid, msuid, jid, owner, user, session)

#
# -- Runtime Jobs' Execution Management from Microservice
#

@router.get("/{uid}/app_service/{msuid}/job/status")
@a_exc2msg
async def getJobStatusToRuntimeByMicroservice(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
    msuid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
    owner: Annotated[str | None, Query(title="The owner", min_length=4, max_length=120, pattern=app_g.regexp_email)] = None,
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> JobRunStatusEnum:
    return await app_g.runtimeAPI.getJobStatus(uid, msuid, jid, owner, user, session)

@router.post("/{uid}/app_service/{msuid}/job/status/{runstatus}")
@a_exc2msg
async def postJobStatusToRuntimeByMicroservice(
    request: Request,
    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
    msuid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
    runstatus: Annotated[JobRunStatusEnum, Path(title="The job status", min_length=5, max_length=10)],
    desc: Annotated[str | None, Query(title="The status description", max_length=200)] = r'',
    user: dict = Depends(check_token),
    session: Session = Depends(app_g.db.get_session),
) -> Job:
    return await app_g.runtimeAPI.postJobStatus(uid, msuid, jid, runstatus, desc, user, session)

#@router.post("/{uid}/app_service/{msuid}/job/{jid}/results")
#@a_exc2msg
#async def postJobOutputToRuntime(
#    request: Request,
#    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
#    msuid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
#    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
#    value: Annotated[list[str], Query(title="The result content. Several results can be added.", max_length=300)] = [],
#    user: dict = Depends(check_token),
#    session: Session = Depends(app_g.db.get_session),
#) -> Job:
#    return await app_g.runtimeAPI.postJobOutputs(uid, msuid, jid, None, value, user, session)
#
#@router.post("/{uid}/app_service/{msuid}/job/{jid}/results/{name}")
#@a_exc2msg
#async def postJobOutputNumberToRuntime(
#    request: Request,
#    uid: Annotated[str, Path(title="The UID of the Runtime", min_length=36, max_length=36)],
#    msuid: Annotated[str, Path(title="The UID of the Microservice", min_length=36, max_length=36)],
#    jid: Annotated[str, Path(title="The UID of the Job", min_length=36, max_length=36)],
#    name: Annotated[int, Path(title="The starting result number")],
#    value: Annotated[list[str], Query(title="The result content.", max_length=300)] = [],
#    user: dict = Depends(check_token),
#    session: Session = Depends(app_g.db.get_session),
#) -> Job:
#    return await app_g.runtimeAPI.postJobOutputs(uid, msuid, jid, name, value, user, session)
